import tkinter as tk
from tkinter import Toplevel, Label, Entry, StringVar, Button, messagebox, filedialog
from models.crud_inventory import get_data_plants, get_data_pots, delete_plant, update_plant
from gui.meteo import DataFaker

class PlantsFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.font = ("TimesNewRoman", 10, "bold")
        self.frame.config(bg="skyblue2")

        self.create_plants_frame()
    
    def clear_plants_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def on_delete(self, plant):
            delete_plant(plant.id)
            self.create_plants_frame()

    def get_plant_status(self, plant, data_faker):
        gen_temperature = data_faker.generate_pot_reading_temperature()
        gen_humidity = data_faker.generate_pot_reading_humidity()
        gen_salinity = data_faker.generate_pot_reading_salinity()

        if gen_humidity < plant.ref_humidity:
            return "Needs Watering"
        elif gen_temperature < plant.ref_temperature:
            return "Needs More Temperature"
        elif gen_salinity < plant.ref_salinity:
            return "Needs More Salinity"
        else:
            return "Healthy"

    def create_plants_frame(self):
        self.clear_plants_frame()
        data_plants = get_data_plants()
        data_pots = get_data_pots()

        for i, plant in enumerate (data_plants):
            for j, pot in enumerate(data_pots):
                data_faker = DataFaker()
                plant_status = self.get_plant_status(plant, data_faker)

                def sync_and_show_message(current_plant=plant, df=data_faker):
                    self.get_plant_status(current_plant, df)
                    messagebox.showinfo("Success", f"Plant {current_plant.id} data synced!")

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
                    text=f'Humidity: {pot.humidity}',
                    font=self.font
                )
                label_humidity.grid(row=i, column=2, padx=5)
                label_humidity.config(bg="skyblue2")

                label_temperature = tk.Label(
                    self.plant_frame,
                    text=f'Temperature: {pot.temperature}',
                    font=self.font
                )
                label_temperature.grid(row=i, column=3, padx=5)
                label_temperature.config(bg="skyblue2")

                label_status = tk.Label(self.plant_frame,
                text=f'Status: {plant_status}',
                font=self.font)
                label_status.grid(row=i, column=4, padx=5)
                label_status.config(bg="skyblue2")

                delete_button = tk.Button(
                    self.plant_frame,
                    text="Delete",
                    command=lambda: self.on_delete(plant)
                )
                delete_button.grid(row=i+1, column=1, pady=1, ipady=1)
                delete_button.config(bg="lightblue1")

                edit_button = tk.Button(
                    self.plant_frame,
                    text="Edit",
                    command=lambda current_plant=plant: self.   open_edit_plant_popup(current_plant)
                )
                edit_button.grid(row=i+1, column=2, pady=1, ipady=1)
                edit_button.config(bg="lightblue1")

                sync_button = tk.Button(
                    self.plant_frame,
                    text="Sync",
                    command=sync_and_show_message
                )
                sync_button.grid(row=i+1, column=3, pady=1, ipady=1)
                sync_button.config(bg="lightblue1")

    def open_edit_plant_popup(self, plant):
        def save_changes(plant):
            update_plant(
                plant.id,
                name=name_var.get(),
                sort=sort_var.get(),
                ref_temperature=int(ref_temperature.get()),
                ref_humidity=int(ref_humidity.get()),
                ref_salinity=float(ref_salinity.get()),
                p_code=p_code_var.get(),
                image_path=image_path_var.get(),
            )
            popup.destroy()
            self.create_plants_frame()

        def open_file_dialog():
            filepath = filedialog.askopenfilename()
            image_path_var.set(filepath)

        popup = Toplevel(self.plant_frame)
        popup.title("Edit Plant")

        name_var = StringVar(value=plant.name)
        sort_var = StringVar(value=plant.sort)
        ref_temperature = StringVar(value=plant.ref_temperature)
        ref_humidity = StringVar(value=plant.ref_humidity)
        ref_salinity = StringVar(value=plant.ref_salinity)
        p_code_var = StringVar(value=plant.p_code)
        image_path_var = StringVar(value=plant.image_path)

        Label(popup, text="Name:").grid(row=0, column=0)
        Entry(popup, textvariable=name_var).grid(row=0, column=1)

        Label(popup, text="Sort:").grid(row=1, column=0)
        Entry(popup, textvariable=sort_var).grid(row=1, column=1)

        Label(popup, text="Ref temp:").grid(row=2, column=0)
        Entry(popup, textvariable=ref_temperature).grid(row=2, column=1)

        Label(popup, text="Ref humidity:").grid(row=3, column=0)
        Entry(popup, textvariable=ref_humidity).grid(row=3, column=1)

        Label(popup, text="Ref salinity:").grid(row=4, column=0)
        Entry(popup, textvariable=ref_salinity).grid(row=4, column=1)

        Label(popup, text="Pot:").grid(row=5, column=0)
        Entry(popup, textvariable=p_code_var).grid(row=5, column=1)

        tk.Label(popup, text="Image Path:").grid(row=6, column=0)
        image_path_button = tk.Button(popup, text="Browse", command=open_file_dialog)
        image_path_button.grid(row=6, column=1)

        image_path_label = tk.Label(popup, textvariable=image_path_var)
        image_path_label.grid(row=7, column=1)

        save_button = Button(popup, text="Save Changes", command=lambda: save_changes(plant))
        save_button.grid(row=8, column=1, pady=5)

        popup.mainloop()