import tkinter as tk
from models.crud_inventory import get_data_pots

class PotsFrame:
    def __init__(self, parent):
        #self.session = session
        self.frame = tk.Frame(parent)
        self.font = ("TimesNewRoman", 10, "bold")
        self.frame.config(bg="palegreen1")

        self.create_pots_frame()

    def create_pots_frame(self):

        data_pots = get_data_pots()

        for i, pot in enumerate(data_pots):

            self.pot_frame = tk.LabelFrame(
                self.frame, text=f'{pot.id} - {pot.name}', width=450, height=140,
                font=self.font, bd=4)
            self.pot_frame.grid(row=i, column=0, padx=5, pady=1, ipadx=60, ipady=1, sticky="w")
            self.pot_frame.config(bg="palegreen1")

            image = tk.PhotoImage(file=pot.image_path)
            image.configure(width=120, height=120)
            label_image = tk.Label(self.pot_frame, image=image, font=self.font)
            label_image.image = image
            label_image.grid(row=i, column=0, padx=5, pady=7)
        
            label_name = tk.Label(self.pot_frame, text=f'Ø: {pot.radius}', font=self.font)
            label_name.grid(row=i, column=1, padx=5)
            label_name.config(bg="palegreen1")
        
            label_humidity = tk.Label(self.pot_frame, text=f'Name: {pot.name}', font=self.font)
            label_humidity.grid(row=i, column=2, padx=5)
            label_humidity.config(bg="palegreen1")
        
            label_temperature = tk.Label(self.pot_frame, text=f'Plant inside: {pot.p_code}', font=self.font)
            label_temperature.grid(row=i, column=3, padx=5)
            label_temperature.config(bg="palegreen1")