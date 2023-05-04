import tkinter as tk
import sqlalchemy as db
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from tkinter import ttk
from tkinter import messagebox
from gui.plants import PlantsFrame
from gui.pots import PotsFrame
from gui.meteo import MeteoFrame
from models.crud_users import login_user
from models.models import MeteoBase

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
        self.password_entry = tk.Entry(self, show="*")
        
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
                messagebox.showinfo("Success", f"Welcome: {user.name}")
            else:
                messagebox.showinfo("Error", f"Wrong email or password")
        else:
            messagebox.showerror("Error", f"Wrong email or password")

def main():
    engine_readings = db.create_engine("sqlite:///readings.db", echo=True)
    MeteoBase.metadata.create_all(engine_readings, checkfirst=True)
    Session = sessionmaker(bind=engine_readings)
    session = Session()

    root = tk.Tk()
    root.withdraw()
    root.resizable(False, True)
    root.geometry("675x995")
    root.title("PyFloraPosude")

    login_window = Login(root)

    canvas = tk.Canvas(root, bg="white", height=970, width=650)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    notebook_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=notebook_frame, anchor="nw")
    
    def on_mouse_wheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    notebook = ttk.Notebook(notebook_frame)
    notebook.grid(row=0, column=0)

    plants_frame = PlantsFrame(notebook)
    pots_frame = PotsFrame(notebook)
    meteo_frame = MeteoFrame(notebook, session)
    notebook.add(plants_frame.frame, text="Plants")
    notebook.add(pots_frame.frame, text="Pots")
    notebook.add(meteo_frame.frame, text="Weather")

    notebook_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    root.mainloop()

if __name__ == "__main__":
    main()