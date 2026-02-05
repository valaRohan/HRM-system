import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date

def window_tra(dash):
    win = tk.Toplevel(dash)
    win.title("Employee Training")
    win.state("zoomed")
    win.config(bg="#ffffff")

    select_id = None

    # ---------------- DB FUNCTIONS ---------------- #

    def submit():
        emp_id = e_emp.get()
        tname = e_name.get()
        sdate = e_start.get()
        edate = e_end.get()
        trainer = e_trainer.get()

        if emp_id == "" or tname == "" or sdate == "" or edate == "":
            messagebox.showerror("Error", "All required fields must be filled")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (emp_id,))
        data = cursor.fetchone()

        if data is None:
                messagebox.showerror("Error", "Employee not found")
                conn.close()
                return
        cursor.execute("""
            INSERT INTO employee_training
            (employee_id, training_name, start_date, end_date, trainer)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, tname, sdate, edate, trainer))

        conn.commit()
        conn.close()

        clear()
        fetch_data()
      

    def fetch_data():
        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        listbox.delete(0, tk.END)
        cursor.execute("SELECT * FROM employee_training")
        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    def clear():
        global select_id
        select_id = None

        e_emp.delete(0, tk.END)
        e_name.delete(0, tk.END)
        e_start.delete(0, tk.END)
        e_end.delete(0, tk.END)
        e_trainer.delete(0, tk.END)

    def on_select(event):
        global select_id
        selected = listbox.curselection()
        if selected:
            data = listbox.get(selected[0])
            select_id = data[0]

            e_emp.delete(0, tk.END)
            e_emp.insert(0, data[1])

            e_name.delete(0, tk.END)
            e_name.insert(0, data[2])

            e_start.delete(0, tk.END)
            e_start.insert(0, data[3])

            e_end.delete(0, tk.END)
            e_end.insert(0, data[4])

            e_trainer.delete(0, tk.END)
            e_trainer.insert(0, data[5])

    def delete():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select a record to delete")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM employee_training WHERE training_id=?",
            (select_id,)
        )
        conn.commit()
        conn.close()

        clear()
        fetch_data()

    def update():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select a record to update")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE employee_training SET
                employee_id=?,
                training_name=?,
                start_date=?,
                end_date=?,
                trainer=?
            WHERE training_id=?
        """, (
            e_emp.get(),
            e_name.get(),
            e_start.get(),
            e_end.get(),
            e_trainer.get(),
            select_id
        ))

        conn.commit()
        conn.close()

        clear()
        fetch_data()
      

    def search_emp():
        emp_id = search_entry.get().strip()

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        listbox.delete(0, tk.END)

        if emp_id == "":
            cursor.execute("SELECT * FROM employee_training")
        else:
            cursor.execute(
                "SELECT * FROM employee_training WHERE employee_id=?",
                (emp_id,)
            )

        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    # ---------------- LEFT FRAME (FORM) ---------------- #

    lframe = tk.Frame(win, bg="#ffffff", width=500)
    lframe.pack(side="left", fill="y", padx=20, pady=20)
    lframe.pack_propagate(False)



    tk.Label(lframe, text="Employee ID",bg="#f7f7f7").grid(row=1,column=1)
    e_emp = tk.Entry(lframe)
    e_emp.grid(row=1,column=2)

  
    tk.Label(lframe, text="Training Name",bg="#f7f7f7").grid(row=2,column=1)
    e_name = tk.Entry(lframe)
    e_name.grid(row=2,column=2)

    
    tk.Label(lframe, text="Start Date (dd-mm-yyyy)",bg="#f7f7f7").grid(row=3,column=1)
    e_start = tk.Entry(lframe)
    e_start.grid(row=3,column=2)

  
    tk.Label(lframe, text="End Date (dd-mm-yyyy)",bg="#f7f7f7").grid(row=4,column=1)
    e_end = tk.Entry(lframe)
    e_end.grid(row=4,column=2)

    
    tk.Label(lframe, text="Trainer Name",bg="#f7f7f7").grid(row=5,column=1)
    e_trainer = tk.Entry(lframe)
    e_trainer.grid(row=5,column=2)

    tk.Button(lframe, text="Submit",
              bg="green", fg="white",
              width=12, command=submit).grid(row=6,column=1,padx=5,pady=5)

    tk.Button(lframe, text="Clear",
              bg="gray", fg="white",
              width=12, command=clear).grid(row=6,column=2,padx=5,pady=5)
    
    tk.Button(lframe, text="Delete",
              bg="red", fg="white",
              width=12, command=delete).grid(row=7,column=1,padx=5,pady=5)

    tk.Button(lframe, text="Update",
              bg="blue", fg="white",
              width=12, command=update).grid(row=7,column=2,padx=5,pady=5)
    # ---------------- RIGHT FRAME (LIST) ---------------- #

    rframe = tk.Frame(win, bg="#ffffff")
    rframe.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    search_frame = tk.Frame(rframe, bg="#ffffff")
    search_frame.pack(fill="x")

    tk.Label(search_frame, text="Search by Employee ID",
             bg="#ffffff").grid(row=1,column=1)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=1,column=2)

    tk.Button(search_frame, text="Search",
              bg="#2196F3", fg="white",
              command=search_emp).grid(row=1,column=3)

    # Frame to hold listbox + scrollbars
    list_frame = tk.Frame(rframe)
    list_frame.pack(fill="both", expand=True, pady=10)

# Vertical scrollbar
    v_scroll = tk.Scrollbar(list_frame, orient="vertical")
    v_scroll.pack(side="right", fill="y")

# Horizontal scrollbar
    h_scroll = tk.Scrollbar(list_frame, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")

# Listbox
    listbox = tk.Listbox(
    list_frame,
    font=("Courier New", 10),
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set
   )
    listbox.pack(fill="both", expand=True)

# Connect scrollbars to listbox
    v_scroll.config(command=listbox.yview)
    h_scroll.config(command=listbox.xview)

# Bind selection event
    listbox.bind("<<ListboxSelect>>", on_select)
    fetch_data()
    def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
    win.protocol("WM_DELETE_WINDOW", back_to_dashboard)
