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
from models.models import Base

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

        self.bind('<Return>', lambda event: self.login())

    def login(self):
        email_login = self.email_entry.get()
        password_login = self.password_entry.get()
        user = login_user(email_login, password_login)

        if user:
            if user.is_admin:
                print("OK LOGIN")
                self.withdraw()
                self.root.deiconify()
                messagebox.showinfo("Success.", f"Welcome: {user.name}")
            else:
                messagebox.showinfo("Error.", f"Wrong email or password")
        else:
            messagebox.showerror("Error.", f"Wrong email or password")

def main():
    engine_readings = db.create_engine("sqlite:///PyFloraDB.db", echo=True)
    Base.metadata.create_all(engine_readings, checkfirst=True)
    Session = sessionmaker(bind=engine_readings)
    session = Session()

    def on_mouse_wheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    def update_canvas_height():
        canvas_height = min(root.winfo_height() - 100, 970)  # Adjust the padding (100) as needed
        canvas.configure(height=canvas_height)
        #canvas.itemconfigure(canvas_frame, height=canvas_height - 4)  # Adjust the padding

    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_window_resize(event):
        update_canvas_height()
        update_scrollregion()

    root = tk.Tk()
    root.withdraw()
    root.resizable(False, True)
    root.geometry("650x950")
    root.title("PyFloraPosude")
    root.bind("<Configure>", on_window_resize)

    login_window = Login(root)

    canvas = tk.Canvas(root, bg="white", width=650)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    canvas_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw", width=650, height=0)

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    notebook = ttk.Notebook(canvas_frame)
    notebook.grid(row=0, column=0, sticky="nsew")

    plants_frame = PlantsFrame(notebook)
    pots_frame = PotsFrame(notebook)
    meteo_frame = MeteoFrame(notebook, session)
    notebook.add(plants_frame.frame, text="Plants")
    notebook.add(pots_frame.frame, text="Pots")
    notebook.add(meteo_frame.frame, text="Weather")

    root.update_idletasks()
    update_canvas_height()
    update_scrollregion()

    root.mainloop()


if __name__ == "__main__":
    main()



