import requests
import xmltodict
import tkinter as tk
import random as rd
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
from models.crud_meteo import create_temperature_reading, create_humidity_reading, create_pressure_reading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.crud_meteo import TemperatureReading, HumidityReading, PressureReading
from models.models import Plant, Pot

engine = create_engine('sqlite:///PyFloraDB.db')
Session = sessionmaker(bind=engine)
session = Session()

class DataFaker:
    def generate_temperature_reading(self, response_temp):
        return round(rd.uniform(float(response_temp) - 3, float(response_temp) + 3), 1)

    def generate_humidity_reading(self, response_humidity):
        min_value = response_humidity - 4 if response_humidity - 4 >= 0 else 0
        max_value = response_humidity + 4 if response_humidity + 4 <= 100 else 0
        return round(rd.uniform(float(min_value), float(max_value)), 1)

    def generate_pressure_reading(self, response_pressure):
        return round(rd.uniform(float(response_pressure) - 6, float(response_pressure) + 8), 1)
    
    def generate_pot_reading_temperature(self):
        return round(rd.uniform(float(10), float(24)), 1)

    def generate_pot_reading_humidity(self):
        return round(rd.uniform(float(20), float(50)), 1)

    def generate_pot_reading_salinity(self):
        return round(rd.uniform(float(0.7), float(2.5)), 1)
                                
class MeteoFrame:
    def __init__(self, parent, session):
        self.frame = tk.Frame(parent)
        self.session = session
        self.font_header = ("TimesNewRoman", 20, "bold")
        self.font_text = ("TimesNewRoman", 15, "bold")
        self.frame.config(bg="burlywood1")

        self.get_outdoor_data()
        self.create_sync_button()
        self.create_add_plant_button()
        self.create_add_pot_button()
        self.create_temperature_graph_button()
        self.create_humidity_graph_button()
        self.create_pressure_graph_button()
        self.create_indoor_frame()
        self.create_outdoor_frame()
        self.create_wind_info_frame()

    def get_outdoor_data(self):
        response = requests.get("https://vrijeme.hr/hrvatska_n.xml")
        response_dict = xmltodict.parse(response.content)
        response_temp = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Temp"]
        response_humidity = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Vlaga"]
        response_pressure = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Tlak"]
        response_wind_speed = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["VjetarBrzina"]
        response_wind_direction = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["VjetarSmjer"]
        response_report = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Vrijeme"]

        return response_temp, response_humidity, response_pressure, response_wind_speed, response_wind_direction, response_report
    
    def create_sync_button(self):
        self.sync_button = tk.Button(
                self.frame,
                text="Fetch data",
                command=lambda: self.create_indoor_frame()
            )
        self.sync_button.grid(row=0, column=0, pady=5, ipady=5)
        self.sync_button.config(bg="lightblue1")

    def create_add_plant_button(self):
        self.add_plant_button = tk.Button(
            self.frame,
            text="Add Plant",
            command=self.create_add_plant_popup
        )
        self.add_plant_button.grid(row=1, column=0, pady=5, ipady=5)
        self.add_plant_button.config(bg="lightblue1")

    def create_add_pot_button(self):
        self.add_pot_button = tk.Button(
            self.frame,
            text="Add Pot",
            command=self.create_add_pot_popup
        )
        self.add_pot_button.grid(row=2, column=0, pady=5, ipady=5)
        self.add_pot_button.config(bg="lightblue1")

    def create_add_plant_popup(self):
        def save_plant():
            #from gui.plants import PlantsFrame
            name = name_entry.get()
            sort = sort_entry.get()
            ref_temperature = ref_temperature_entry.get()
            ref_humidity = ref_humidity_entry.get()
            ref_salinity = ref_salinity_entry.get()
            p_code = p_code_entry.get()
            image_path = image_path_var.get()

            session.add(Plant(
                name=name,
                sort=sort,
                ref_temperature=ref_temperature,
                ref_humidity=ref_humidity,
                ref_salinity=ref_salinity,
                p_code=p_code,
                image_path=image_path
            ))
            session.commit()
            popup.destroy()

        def open_file_dialog():
            filepath = filedialog.askopenfilename()
            image_path_var.set(filepath)

        popup = tk.Toplevel(self.frame)
        popup.title("Add Plant")

        tk.Label(popup, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Sort:").grid(row=1, column=0)
        sort_entry = tk.Entry(popup)
        sort_entry.grid(row=1, column=1)

        tk.Label(popup, text="Referent temp:").grid(row=2, column=0)
        ref_temperature_entry = tk.Entry(popup)
        ref_temperature_entry.grid(row=2, column=1)

        tk.Label(popup, text="Referent humidity:").grid(row=3, column=0)
        ref_humidity_entry = tk.Entry(popup)
        ref_humidity_entry.grid(row=3, column=1)

        tk.Label(popup, text="Referent salinity:").grid(row=4, column=0)
        ref_salinity_entry = tk.Entry(popup)
        ref_salinity_entry.grid(row=4, column=1)

        tk.Label(popup, text="P Code:").grid(row=5, column=0)
        p_code_entry = tk.Entry(popup)
        p_code_entry.grid(row=5, column=1)

        image_path_var = tk.StringVar()

        tk.Label(popup, text="Image Path:").grid(row=6, column=0)
        image_path_button = tk.Button(popup, text="Browse", command=open_file_dialog)
        image_path_button.grid(row=6, column=1)

        image_path_label = tk.Label(popup, textvariable=image_path_var)
        image_path_label.grid(row=7, column=1)

        save_button = tk.Button(popup, text="Save", command=save_plant)
        save_button.grid(row=8, column=1, pady=5)

        popup.mainloop()

    def create_add_pot_popup(self):
        def save_pot():
            name = name_entry.get()
            radius = radius_entry.get()
            image_path = image_path_var.get()
            humidity = humidity_entry.get()
            temperature = temperature_entry.get()

            session.add(Pot(
                name=name,
                radius=radius,
                image_path=image_path, 
                humidity=humidity,
                temperature=temperature
            ))
            session.commit()
            popup.destroy()

        def open_file_dialog():
            filepath = filedialog.askopenfilename()
            image_path_var.set(filepath)

        popup = tk.Toplevel(self.frame)
        popup.title("Add Pot")

        tk.Label(popup, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(popup)
        name_entry.grid(row=0, column=1)

        tk.Label(popup, text="Radius:").grid(row=1, column=0)
        radius_entry = tk.Entry(popup)
        radius_entry.grid(row=1, column=1)

        tk.Label(popup, text="Humidity:").grid(row=2, column=0)
        humidity_entry = tk.Entry(popup)
        humidity_entry.grid(row=2, column=1)

        tk.Label(popup, text="Temperature:").grid(row=3, column=0)
        temperature_entry = tk.Entry(popup)
        temperature_entry.grid(row=3, column=1)

        image_path_var = tk.StringVar()

        tk.Label(popup, text="Image Path:").grid(row=4, column=0)
        image_path_button = tk.Button(popup, text="Browse", command=open_file_dialog)
        image_path_button.grid(row=4, column=1)

        image_path_label = tk.Label(popup, textvariable=image_path_var)
        image_path_label.grid(row=5, column=1)

        save_button = tk.Button(popup, text="Save", command=save_pot)
        save_button.grid(row=6, column=1, pady=5)

        popup.mainloop()

    def create_temperature_graph_button(self):
        self.temp_graph_button = tk.Button(
                self.frame,
                text="Inside temperature graph",
                command=lambda: self.create_temperature_graph_window()
            )
        self.temp_graph_button.grid(row=3, column=0, pady=5, ipady=5)
        self.temp_graph_button.config(bg="lightblue1")

    def create_temperature_graph_window(self):
        temp_df = pd.read_sql(session.query(TemperatureReading).statement, engine)
        temp_df.set_index(pd.to_datetime(temp_df['timestamp']), inplace=True)
        temp_df = temp_df.iloc[::5, :]

        temp_df['value'].plot(kind='line')
        plt.title('Temperature vs. Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Temperature')
        plt.show()

    def create_humidity_graph_button(self):
        self.humid_graph_button = tk.Button(
                self.frame,
                text="Inside humidity graph",
                command=lambda: self.create_humidity_graph_window()
            )
        self.humid_graph_button.grid(row=4, column=0, pady=5, ipady=5)
        self.humid_graph_button.config(bg="lightblue1")

    def create_humidity_graph_window(self):
        humid_df = pd.read_sql(session.query(HumidityReading).statement, engine)
        humid_df.set_index(pd.to_datetime(humid_df['timestamp']), inplace=True)
        humid_df = humid_df.iloc[::5, :]

        humid_df['value'].plot(kind='line')
        plt.title('Humiditiy vs. Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Humiditiy')
        plt.show()

    def create_pressure_graph_button(self):
        self.press_graph_button = tk.Button(
                self.frame,
                text="Inside pressure graph",
                command=lambda: self.create_pressure_graph_window()
            )
        self.press_graph_button.grid(row=5, column=0, pady=5, ipady=5)
        self.press_graph_button.config(bg="lightblue1")

    def create_pressure_graph_window(self):
        press_df = pd.read_sql(session.query(PressureReading).statement, engine)
        press_df.set_index(pd.to_datetime(press_df['timestamp']), inplace=True)

        press_df['value'].plot(kind='line')
        plt.title('Pressure vs. Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Pressure')
        plt.show()

    def create_indoor_frame(self):
        self.indoor_frame = tk.LabelFrame(
            self.frame,
            text="Indoor values",
            width=400,
            height=400,
            font=self.font_header,
            bd=6
        )
        self.indoor_frame.grid(row=6, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.indoor_frame.config(bg="burlywood1")

        def refresh_values():
            self.create_inside_readings()
            self.frame.after(900000, refresh_values) # 15 min autoupdate

        self.create_inside_readings()
        refresh_values()

    def create_outdoor_frame(self):
        self.outdoor_frame = tk.LabelFrame(
            self.frame,
            text="Outdoor values",
            width=400,
            height=400,
            font=self.font_header,
            bd=6
        )
        self.outdoor_frame.grid(row=7, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.outdoor_frame.config(bg="burlywood1")

        self.create_outside_readings()

    def create_wind_info_frame(self):
        self.wind_info_frame = tk.LabelFrame(
            self.frame,
            text="Wind status and more info",
            width=400,
            height=400,
            font=self.font_header,
            bd=6
        )
        self.wind_info_frame.grid(row=8, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.wind_info_frame.config(bg="burlywood1")

        self.create_wind_info_readings()

    def create_inside_readings(self):
        data_faker = DataFaker()
        responses = self.get_outdoor_data()

        responses_temp = responses[0]
        responses_humidity = responses[1]
        responses_pressure = responses[2]
        indoor_temperature_value = data_faker.generate_temperature_reading(
            float(responses_temp)
        )
        
        create_temperature_reading(session=self.session, value=indoor_temperature_value)

        self.inside_temp_label = tk.Label(
            self.indoor_frame,
            text=f"- Inside temperature: {indoor_temperature_value}° C",
            font=self.font_text
        )
        self.inside_temp_label.grid(row=0, column=0, padx=5, pady=5)
        self.inside_temp_label.config(bg="burlywood1")
        
        indoor_humidity_value = data_faker.generate_humidity_reading(round(float(responses_humidity), 1))

        create_humidity_reading(session=self.session, value=indoor_humidity_value)

        self.inside_humidity_label = tk.Label(
            self.indoor_frame,
            text=f"- Inside humidity: {indoor_humidity_value} %",
            font=self.font_text
        )
        self.inside_humidity_label.grid(row=1, column=0, padx=5, pady=5)
        self.inside_humidity_label.config(bg="burlywood1")
        
        indoor_pressure_value = data_faker.generate_pressure_reading(round(float(responses_pressure), 1))

        create_pressure_reading(session=self.session, value=indoor_pressure_value)

        self.inside_pressure_label = tk.Label(
            self.indoor_frame,
            text=f"- Inside pressure: {indoor_pressure_value} hPa",
            font=self.font_text
        )
        self.inside_pressure_label.grid(row=2, column=0, padx=5, pady=5)
        self.inside_pressure_label.config(bg="burlywood1")

    def create_outside_readings(self):
        responses = self.get_outdoor_data()
        responses_temp = responses[0]
        responses_humidity = responses[1]
        responses_pressure = responses[2]

        self.outside_temp_label = tk.Label(
            self.outdoor_frame,
            text=f"- Outside temperature: {responses_temp}° C",
            font=self.font_text
        )
        self.outside_temp_label.grid(row=0, column=0, padx=5, pady=15)
        self.outside_temp_label.config(bg="burlywood1")

        self.outside_humidity_label = tk.Label(
            self.outdoor_frame,
            text=f"- Outside humidity: {responses_humidity} %",
            font=self.font_text
        )
        self.outside_humidity_label.grid(row=1, column=0, padx=5, pady=15)
        self.outside_humidity_label.config(bg="burlywood1")

        self.outside_pressure_label = tk.Label(
            self.outdoor_frame,
            text=f"- Outside pressure: {responses_pressure} hPa",
            font=self.font_text
        )
        self.outside_pressure_label.grid(row=2, column=0, padx=5, pady=15)
        self.outside_pressure_label.config(bg="burlywood1")

    def create_wind_info_readings(self):
        responses = self.get_outdoor_data()

        responses_wind_speed = responses[3]
        responses_wind_direction = responses[4]
        responses_wind_report = responses[5]

        self.wind_info_text = tk.Label(
            self.wind_info_frame,
            text=f"- Wind speed: {responses_wind_speed} m/s",
            font=self.font_text
        )
        self.wind_info_text.grid(row=0, column=0, padx=20, pady=20)
        self.wind_info_text.config(bg="burlywood1")

        self.wind_direction_text = tk.Label(
            self.wind_info_frame,
            text=f"- Wind direction: {responses_wind_direction}",
            font=self.font_text
        )
        self.wind_direction_text.grid(row=1, column=0, padx=20, pady=20)
        self.wind_direction_text.config(bg="burlywood1")

        self.report_text = tk.Label(
            self.wind_info_frame,
            text=f"- Meteo info: {responses_wind_report} !",
            font=self.font_text
        )
        self.report_text.grid(row=2, column=0, padx=20, pady=20)
        self.report_text.config(bg="burlywood1")