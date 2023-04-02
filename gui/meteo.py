import requests
import xmltodict
import tkinter as tk

from models.models_1 import Plants

print(Plants)

response = requests.get("https://vrijeme.hr/hrvatska_n.xml")
response_dict = xmltodict.parse(response.content)

response_temp = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Temp"]
inside_temp = "21"

response_humidity = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Vlaga"]
inside_humidity = "40"

response_pressure = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Tlak"]
inside_pressure = "1022"

response_wind_speed = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["VjetarBrzina"]
response_wind_direction = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["VjetarSmjer"]
response_report = response_dict["Hrvatska"]["Grad"][-3]["Podatci"]["Vrijeme"]

class MeteoFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.font_header = ("TimesNewRoman", 20, "bold")
        self.font_text = ("TimesNewRoman", 15, "bold")
        self.frame.config(bg="burlywood1")

        self.create_indoor_frame()
        self.create_outdoor_frame()
        self.create_wind_info_frame()

    def create_indoor_frame(self):
        self.indoor_frame = tk.LabelFrame(
            self.frame, text="Indoor values", width=400, height=400,
            font=self.font_header, bd=6
        )
        self.indoor_frame.grid(row=0, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.indoor_frame.config(bg="burlywood1")

        self.create_inside_readings()

    def create_outdoor_frame(self):
        self.outdoor_frame = tk.LabelFrame(
            self.frame, text="Outdoor values", width=400, height=400,
            font=self.font_header, bd=6
        )
        self.outdoor_frame.grid(row=1, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.outdoor_frame.config(bg="burlywood1")

        self.create_outside_readings()

    def create_wind_info_frame(self):
        self.wind_info_frame = tk.LabelFrame(
            self.frame, text="Wind status and more info", width=400, height=400,
            font=self.font_header, bd=6
        )
        self.wind_info_frame.grid(row=2, column=0, ipadx=20, ipady=20, padx=70, pady=30)
        self.wind_info_frame.config(bg="burlywood1")

        self.create_wind_info_readings()

    def create_inside_readings(self):
        self.inside_temp_label = tk.Label(self.indoor_frame, text=f"- Inside temperature: {inside_temp}° C", font=self.font_text)
        self.inside_temp_label.grid(row=0, column=0, padx=5, pady=5)
        self.inside_temp_label.config(bg="burlywood1")

        self.inside_humidity_label = tk.Label(self.indoor_frame, text=f"- Inside humidity: {inside_humidity} %", font=self.font_text)
        self.inside_humidity_label.grid(row=1, column=0, padx=5, pady=5)
        self.inside_humidity_label.config(bg="burlywood1")

        self.inside_pressure_label = tk.Label(self.indoor_frame, text=f"- Inside pressure: {inside_pressure} hPa", font=self.font_text)
        self.inside_pressure_label.grid(row=2, column=0, padx=5, pady=5)
        self.inside_pressure_label.config(bg="burlywood1")

    def create_outside_readings(self):
        self.outside_temp_label = tk.Label(self.outdoor_frame, text=f"- Outside temperature: {response_temp}° C", font=self.font_text)
        self.outside_temp_label.grid(row=0, column=0, padx=5, pady=15)
        self.outside_temp_label.config(bg="burlywood1")

        self.outside_humidity_label = tk.Label(self.outdoor_frame, text=f"- Outside humidity: {response_humidity} %", font=self.font_text)
        self.outside_humidity_label.grid(row=1, column=0, padx=5, pady=15)
        self.outside_humidity_label.config(bg="burlywood1")

        self.outside_pressure_label = tk.Label(self.outdoor_frame, text=f"- Outside pressure: {response_pressure} hPa", font=self.font_text)
        self.outside_pressure_label.grid(row=2, column=0, padx=5, pady=15)
        self.outside_pressure_label.config(bg="burlywood1")

    def create_wind_info_readings(self):
        self.wind_info_text = tk.Label(self.wind_info_frame, text=f"- Wind speed: {response_wind_speed} m/s", font=self.font_text)
        self.wind_info_text.grid(row=0, column=0, padx=20, pady=20)
        self.wind_info_text.config(bg="burlywood1")

        self.wind_direction_text = tk.Label(self.wind_info_frame, text=f"- Wind direction: {response_wind_direction}", font=self.font_text)
        self.wind_direction_text.grid(row=1, column=0, padx=20, pady=20)
        self.wind_direction_text.config(bg="burlywood1")

        self.report_text = tk.Label(self.wind_info_frame, text=f"- Meteo info: {response_report} !", font=self.font_text)
        self.report_text.grid(row=2, column=0, padx=20, pady=20)
        self.report_text.config(bg="burlywood1")