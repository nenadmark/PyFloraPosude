import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.plants import PlantsFrame
from gui.pots import PotsFrame
from gui.meteo import MeteoFrame
from models.models_1 import Base
from models.crud_login import login_user

class Login(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.root = root
        self.config(bg="slategray2")

        username_label = tk.Label(
            self, text="Username:",
            font= ('Helvetica 15 underline')
        )
        username_label.config(bg="slategray2")
        password_label = tk.Label(
            self,
            text="Password:",
            font= ('Helvetica 15 underline')
        )
        password_label.config(bg="slategray2")
        self.email_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self)
        submit = tk.Button(
            self,
            text="Login",
            command=self.login
        )
        
        username_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.email_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        password_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        submit.grid(row=2, column=1, sticky="e", padx=10, pady=10)

    def login(self):
        email_login = self.email_entry.get()
        password_login = self.password_entry.get()
        user = login_user(email_login, password_login)

        if user:
            if user.is_admin:
                print("OK LOGIN")
                self.withdraw()
                self.root.deiconify()
                messagebox.showinfo("Success.", f"Welcome {user.name}")
            else:
                messagebox.showinfo("Error.", f"Wrong email or password")
        else:
            messagebox.showerror("Error.", f"Wrong email or password")

def main():
    root = tk.Tk()
    root.withdraw()
    root.resizable(False, False)
    root.configure(height=500, width=500)
    root.geometry("575x995")
    root.resizable(False, True)
    root.title("PyPlant")

    login_window =  Login(root)

    notebook = ttk.Notebook(root)
    notebook.configure(width=700)
    notebook.grid(row=0, column=0)

    plants_frame = PlantsFrame(notebook)
    pots_frame = PotsFrame(notebook)
    meteo_frame = MeteoFrame(notebook)

    notebook.add(plants_frame.frame, text="Plants")
    notebook.add(pots_frame.frame, text="Pots")
    notebook.add(meteo_frame.frame, text="Weather")

    root.mainloop()

if __name__ == "__main__":
    main()

