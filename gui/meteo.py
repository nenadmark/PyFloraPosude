import requests
import xmltodict
import tkinter as tk
import random as rd
from models.crud_meteo import create_temperature_reading, create_humidity_reading, create_pressure_reading

class DataFaker:
    def generate_temperature_reading(self, response_temp):
        return round(rd.uniform(float(response_temp) - 5, float(response_temp) + 5), 1)

    def generate_humidity_reading(self, response_humidity):
        print(type(response_humidity))
        min_value = response_humidity - 5 if response_humidity - 5 >= 0 else 0
        max_value = response_humidity + 5 if response_humidity + 5 <= 100 else 0
        return round(rd.uniform(float(min_value), float(max_value)), 1)

    def generate_pressure_reading(self, response_pressure):
        return round(rd.uniform(float(response_pressure) - 8, float(response_pressure) + 8), 1)



class MeteoFrame:
    def __init__(self, parent, session):
        self.frame = tk.Frame(parent)
        self.session = session
        self.font_header = ("TimesNewRoman", 20, "bold")
        self.font_text = ("TimesNewRoman", 15, "bold")
        self.frame.config(bg="burlywood1")

        self.get_outdoor_data()
        self.create_sync_button()
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
                text="Sync",
                command=lambda: self.create_indoor_frame()
            )
        self.sync_button.grid(row=0, column=0, pady=5, ipady=5)
        self.sync_button.config(bg="lightblue1")

    def create_indoor_frame(self):
        self.indoor_frame = tk.LabelFrame(
            self.frame,
            text="Indoor values",
            width=400,
            height=400,
            font=self.font_header,
            bd=6
        )
        self.indoor_frame.grid(row=1, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.indoor_frame.config(bg="burlywood1")

        def refresh_values():
            self.create_inside_readings()
            self.frame.after(60000, refresh_values)

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
        self.outdoor_frame.grid(row=2, column=0, ipadx=20, ipady=20, padx=70, pady=30)
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
        self.wind_info_frame.grid(row=3, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.wind_info_frame.config(bg="burlywood1")

        self.create_wind_info_readings()

    def create_inside_readings(self):
        data_faker = DataFaker()
        responses = self.get_outdoor_data()

        responses_temp = responses[0]
        responses_humidity = responses[1]
        responses_pressure = responses[2]


        ###
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



        ###
        indoor_humidity_value = data_faker.generate_humidity_reading(round(float(responses_humidity), 1))

        create_humidity_reading(session=self.session, value=indoor_humidity_value)

        self.inside_humidity_label = tk.Label(
            self.indoor_frame,
            text=f"- Inside humidity: {indoor_humidity_value} %",
            font=self.font_text
        )
        self.inside_humidity_label.grid(row=1, column=0, padx=5, pady=5)
        self.inside_humidity_label.config(bg="burlywood1")
        
        
        
        ###
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