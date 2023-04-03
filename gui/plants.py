import tkinter as tk
from models.crud_inventory import get_data_plants, delete_plant

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.on_configure)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class PlantsFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.font = ("TimesNewRoman", 10, "bold")
        self.frame.config(bg="skyblue2")

        self.create_plants_frame()

    def on_delete(self, plant):
            delete_plant(plant.id)

    def create_plants_frame(self):

        data_plants = get_data_plants()
        for i, plant in enumerate (data_plants):

            self.plant_frame = tk.LabelFrame(
                self.frame,
                text=f'{plant.id} - {plant.name}',
                width=450,
                height=140,
                font=self.font,
                bd=4
            )
            self.plant_frame.grid(row=i, column=0, padx=5, pady=1, ipadx=60, ipady=1, sticky="w")
            self.plant_frame.config(bg="skyblue2")

            image = tk.PhotoImage(file=plant.image_path)
            image.configure(width=120, height=120)
            label_image = tk.Label(
                self.plant_frame,
                image=image,
                font=self.font
            )
            label_image.image = image
            label_image.grid(row=i, column=0, padx=5, pady=5)
        
            label_name = tk.Label(
                self.plant_frame,
                text=plant.sort,
                font=self.font
            )
            label_name.grid(row=i, column=1, padx=5, ipadx=5)
            label_name.config(bg="skyblue2")
        
            label_humidity = tk.Label(
                self.plant_frame,
                text=f'Humidity: {plant.humidity}',
                font=self.font
            )
            label_humidity.grid(row=i, column=2, padx=5)
            label_humidity.config(bg="skyblue2")
        
            label_temperature = tk.Label(
                self.plant_frame,
                text=f'Temperature: {plant.temperature}',
                font=self.font
            )
            label_temperature.grid(row=i, column=3, padx=5)
            label_temperature.config(bg="skyblue2")

            delete_button = tk.Button(
                self.plant_frame,
                text="Delete",
                command=lambda: self.on_delete(plant)
            )
            delete_button.grid(row=i+1, column=1, pady=1, ipady=1)
            delete_button.config(bg="lightblue1")
            

