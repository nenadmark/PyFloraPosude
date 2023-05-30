import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from tkinter import Toplevel, Label, Entry, StringVar, Button, filedialog
from models.crud_inventory import get_data_pots , delete_pot, update_pot, get_temperature_readings, get_humidity_readings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PotsFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.font = ("TimesNewRoman", 10, "bold")
        self.frame.config(bg="palegreen1")

        self.create_pots_frame()

    def clear_pots_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def on_delete(self, pot):
        delete_pot(pot.id)
        self.create_pots_frame()

    def show_graphs(self, pot):
        temperature_readings = get_temperature_readings(pot.id)
        humidity_readings = get_humidity_readings(pot.id)
    
        temperature_values = [reading.value for reading in temperature_readings]
        temperature_times = [mdates.date2num(reading.timestamp) for reading in temperature_readings]
    
        humidity_values = [reading.value for reading in humidity_readings]
        humidity_times = [mdates.date2num(reading.timestamp) for reading in humidity_readings]
    
        popup = Toplevel(self.pot_frame)
        popup.title(f"Pot #{pot.id} Graphs")
    
        figure, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
        ax1.plot_date(temperature_times, temperature_values, 'r-')  # Red line
        ax1.set_title('Temperature Readings')
    
        ax2.plot_date(humidity_times, humidity_values, 'b-')  # Blue line
        ax2.set_title('Humidity Readings')
    
        # Set the locator and formatter for all axes
        for ax in [ax1, ax2]:
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
    
        canvas = FigureCanvasTkAgg(figure, popup)
        canvas.get_tk_widget().pack()
    
        popup.mainloop()

    def create_pots_frame(self):
        self.clear_pots_frame()
        data_pots = get_data_pots()

        for i, pot in enumerate(data_pots):

            self.pot_frame = tk.LabelFrame(
                self.frame,
                text=f'{pot.id} - {pot.name}',
                width=450,
                height=140,
                font=self.font,
                bd=4
            )
            self.pot_frame.grid(row=i, column=0, padx=5, pady=1, ipadx=60, ipady=1, sticky="w")
            self.pot_frame.config(bg="palegreen1")

            image = tk.PhotoImage(file=pot.image_path)
            image.configure(width=120, height=120)
            label_image = tk.Label(
                self.pot_frame,
                image=image,
                font=self.font
            )
            label_image.image = image
            label_image.grid(row=i, column=0, padx=5, pady=7)
        
            label_name = tk.Label(
                self.pot_frame,
                text=f'Ø: {pot.radius}',
                font=self.font
            )
            label_name.grid(row=i, column=1, padx=5)
            label_name.config(bg="palegreen1")
        
            label_humidity = tk.Label(
                self.pot_frame,
                text=f'Name: {pot.name}',
                font=self.font
            )
            label_humidity.grid(row=i, column=2, padx=5)
            label_humidity.config(bg="palegreen1")
        
            label_plant_inside = tk.Label(
                self.pot_frame,
                text=f'Plant inside: {pot.id}',
                font=self.font
            )
            label_plant_inside.grid(row=i, column=3, padx=5)
            label_plant_inside.config(bg="palegreen1")

            delete_button = tk.Button(
                self.pot_frame,
                text="Delete",
                command=lambda: self.on_delete(pot)
            )
            delete_button.grid(row=i+1, column=1, pady=1, ipady=1)
            delete_button.config(bg="lightgreen")

            edit_button = tk.Button(
                self.pot_frame,
                text="Edit",
                command=lambda current_plant=pot: self.open_edit_pot_popup(current_plant)
            )
            edit_button.grid(row=i+1, column=2, pady=1, ipady=1)
            edit_button.config(bg="lightgreen")

            graph_button = tk.Button(
                self.pot_frame,
                text="Graphs",
                command=lambda current_pot=pot: self.show_graphs(current_pot)
            )
            graph_button.grid(row=i+1, column=3, pady=1, ipady=1)
            graph_button.config(bg="lightgreen")
    
    def open_edit_pot_popup(self, pot):
        def save_changes(pot):
            update_pot(
                pot.id,
                name=name_var.get(),
                radius=int(radius_var.get()),
                humidity=int(humidity_var.get()),
                temperature=int(temperature_var.get()),
                image_path=image_path_var.get(),
            )
            popup.destroy()
            self.create_pots_frame()
        
        def open_file_dialog():
            filepath = filedialog.askopenfilename()
            image_path_var.set(filepath)

        popup = Toplevel(self.pot_frame)
        popup.title("Edit Pot")

        name_var = StringVar(value=pot.name)
        radius_var = StringVar(value=pot.radius)
        humidity_var = StringVar(value=pot.humidity)
        temperature_var = StringVar(value=pot.temperature)

        image_path_var = StringVar(value=pot.image_path)

        Label(popup, text="Name:").grid(row=0, column=0)
        Entry(popup, textvariable=name_var).grid(row=0, column=1)

        Label(popup, text="Radius:").grid(row=1, column=0)
        Entry(popup, textvariable=radius_var).grid(row=1, column=1)

        Label(popup, text="Humidity:").grid(row=2, column=0)
        Entry(popup, textvariable=humidity_var).grid(row=2, column=1)

        Label(popup, text="Temperature:").grid(row=3, column=0)
        Entry(popup, textvariable=temperature_var).grid(row=3, column=1)

        tk.Label(popup, text="Image Path:").grid(row=4, column=0)
        image_path_button = tk.Button(popup, text="Browse", command=open_file_dialog)
        image_path_button.grid(row=4, column=1)

        image_path_label = tk.Label(popup, textvariable=image_path_var)
        image_path_label.grid(row=5, column=1)

        save_button = Button(popup, text="Save Changes", command=lambda: save_changes(pot))
        save_button.grid(row=6, column=1, pady=5)

        popup.mainloop()