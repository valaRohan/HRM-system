import tkinter as tk
from tkinter import messagebox
import sqlite3
def window_dep(dash):


    win = tk.Toplevel(dash)
    win.state("zoomed")
    win.title("Departments")



    def fetch_data():
     conn=sqlite3.connect("hrm.db")
     cursor=conn.cursor()

     listbox.delete(0,tk.END)
     cursor.execute("select * from employees")
     for row in cursor.fetchall():
        listbox.insert(tk.END,row)

    def search_dmp():
     dep = search_entry.get().strip()

     conn = sqlite3.connect("hrm.db")
     cursor = conn.cursor()

     listbox.delete(0, tk.END)

     if dep == "":
        cursor.execute("SELECT * FROM employees")
     elif dep == "all":
        cursor.execute("SELECT * FROM employees")
     else:
        cursor.execute(
            "SELECT * from employees WHERE department= ?",
            (dep,)
        )

     for row in cursor.fetchall():
        listbox.insert(tk.END, row)

     conn.close()

    rframe = tk.Frame(win, bg="#ffffff", padx=20, pady=20)
    rframe.pack(side="right", fill="both", expand=True)

    rframe.grid_columnconfigure(0, weight=1)
    rframe.grid_columnconfigure(1, weight=2)
    rframe.grid_columnconfigure(2, weight=0)

    tk.Label(rframe, text="Search by Employee Departments", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
    search_entry = tk.StringVar(rframe)
    search_entry.set("Human Resources")
    level=tk.OptionMenu(rframe,search_entry,"Human Resources","Finance","Sales","Marketing","Operations","Administration","employee","all").grid(row=0, column=1, sticky="ew", padx=10)
    tk.Button(rframe, text="Search", bg="#2196F3", fg="white",command=search_dmp).grid(row=0, column=2)

    listbox = tk.Listbox(rframe, height=18)
    listbox.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=15)

    rframe.grid_rowconfigure(1, weight=1)


    listbox.bind("<<ListboxSelect>>")

    fetch_data()
    
    def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
    win.protocol("WM_DELETE_WINDOW", back_to_dashboard)