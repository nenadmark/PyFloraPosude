import tkinter as tk
from tkinter import Toplevel, Label, Entry, StringVar, Button
from models.crud_inventory import get_data_pots , delete_pot, update_pot

class PotsFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.font = ("TimesNewRoman", 10, "bold")
        self.frame.config(bg="palegreen1")

        self.create_pots_frame()

    def on_delete(self, pot):
        delete_pot(pot.id)

    def create_pots_frame(self):

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
    







    
    def open_edit_pot_popup(self, pot):
        def save_changes(pot):
            update_pot(
                pot.id,
                name=name_var.get(),
                radius=int(radius_var.get()),
                image_path=image_path_var.get(),
            )
            popup.destroy()

        popup = Toplevel(self.pot_frame)
        popup.title("Edit Pot")

        name_var = StringVar(value=pot.name)
        radius_var = StringVar(value=pot.radius)
        image_path_var = StringVar(value=pot.image_path)

        Label(popup, text="Name:").grid(row=0, column=0)
        Entry(popup, textvariable=name_var).grid(row=0, column=1)

        Label(popup, text="Radius:").grid(row=1, column=0)
        Entry(popup, textvariable=radius_var).grid(row=1, column=1)

        Label(popup, text="Image Path:").grid(row=2, column=0)
        Entry(popup, textvariable=image_path_var).grid(row=2, column=1)

        save_button = Button(popup, text="Save Changes", command=lambda: save_changes(pot))
        save_button.grid(row=3, column=1, pady=5)

        popup.mainloop()