import tkinter as tk
from tkinter import messagebox
import sqlite3


def window_sal(dash):
    win = tk.Toplevel(dash)
    win.title("Salary Management")
    win.state("zoomed")
    win.config(bg="#ffffff")

    select_id = None

    # ================= FUNCTIONS =================

    def submit():
        emp_id = e_emp.get()
        month = e_month.get()

        if emp_id == "" or month == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            basic = float(e_basic.get())
            allow = int(e_allow.get())
            deduct = int(e_deduct.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers")
            return

        net = basic + allow - deduct

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("SELECT employee_id FROM employees WHERE employee_id=?", (emp_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Employee not found")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO salary
            (employee_id, basic_salary, allowances, Deductions, net_salary, pay_month)
            VALUES (?,?,?,?,?,?)
        """, (emp_id, basic, allow, deduct, net, month))

        conn.commit()
        conn.close()

        clear()
        fetch_data()
        messagebox.showinfo("Success", "Salary added successfully")

    def fetch_data():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM salary")
        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    def clear():
        e_emp.delete(0, tk.END)
        e_basic.delete(0, tk.END)
        e_allow.delete(0, tk.END)
        e_deduct.delete(0, tk.END)
        e_month.delete(0, tk.END)
        e_allow.insert(0, "0")
        e_deduct.insert(0, "0")

    def on_select(event):
            nonlocal select_id

            if not listbox.curselection():
                return

            index = listbox.curselection()[0]
            data = listbox.get(index)

            select_id = data[0]   # payroll_id

            e_emp.delete(0, tk.END)
            e_basic.delete(0, tk.END)
            e_allow.delete(0, tk.END)
            e_deduct.delete(0, tk.END)
            e_month.delete(0, tk.END)

            e_emp.insert(0, data[1])
            e_basic.insert(0, data[2])
            e_allow.insert(0, data[3])
            e_deduct.insert(0, data[4])
            e_month.insert(0, data[6])   # pay_month (skip net_salary at index 5)


    def delete():
        nonlocal select_id
        if select_id is None:
            messagebox.showerror("Error", "Select record to delete")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM salary WHERE payroll_id=?", (select_id,))
        conn.commit()
        conn.close()

        select_id = None
        clear()
        fetch_data()
        messagebox.showinfo("Success", "Record deleted")

    def update():
        nonlocal select_id
        if select_id is None:
            messagebox.showerror("Error", "Select record to update")
            return

        try:
            basic = float(e_basic.get())
            allow = int(e_allow.get())
            deduct = int(e_deduct.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers")
            return

        net = basic + allow - deduct

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE salary SET
                employee_id=?,
                basic_salary=?,
                allowances=?,
                Deductions=?,
                net_salary=?,
                pay_month=?
            WHERE payroll_id=?
        """, (
            e_emp.get(),
            basic,
            allow,
            deduct,
            net,
            e_month.get(),
            select_id
        ))

        conn.commit()
        conn.close()

        select_id = None
        clear()
        fetch_data()
        messagebox.showinfo("Success", "Record updated")
    def search_emp():
        emp_id = search_entry.get().strip()

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        listbox.delete(0, tk.END)

        if emp_id == "":
            cursor.execute("SELECT * FROM salary")
        else:
            cursor.execute("SELECT * FROM salary WHERE employee_id=?", (emp_id,))

        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    # ================= LEFT FRAME =================

    left = tk.Frame(win, bg="#ffffff", width=350)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    tk.Label(left, text="Salary Entry",
             font=("Arial", 18, "bold"),
             bg="#ffffff").grid(row=0, columnspan=2, pady=20)

    tk.Label(left, text="Employee ID", bg="#ffffff").grid(row=1, column=0)
    e_emp = tk.Entry(left)
    e_emp.grid(row=1, column=1)

    tk.Label(left, text="Basic Salary", bg="#ffffff").grid(row=2, column=0)
    e_basic = tk.Entry(left)
    e_basic.grid(row=2, column=1)

    tk.Label(left, text="Allowances", bg="#ffffff").grid(row=3, column=0)
    e_allow = tk.Entry(left)
    e_allow.insert(0, "0")
    e_allow.grid(row=3, column=1)

    tk.Label(left, text="Deductions", bg="#ffffff").grid(row=4, column=0)
    e_deduct = tk.Entry(left)
    e_deduct.insert(0, "0")
    e_deduct.grid(row=4, column=1)

    tk.Label(left, text="Pay Month (MM-YYYY)", bg="#ffffff").grid(row=5, column=0)
    e_month = tk.Entry(left)
    e_month.grid(row=5, column=1)

    tk.Button(left, text="Submit", bg="green", fg="white",
              width=12, command=submit).grid(row=6, column=0, pady=10)

    tk.Button(left, text="Clear", bg="gray", fg="white",
              width=12, command=clear).grid(row=6, column=1)

    tk.Button(left, text="Update", bg="blue", fg="white",
              width=12, command=update).grid(row=7, column=0)

    tk.Button(left, text="Delete", bg="red", fg="white",
              width=12, command=delete).grid(row=7, column=1)

    # ================= RIGHT FRAME =================

    rframe = tk.Frame(win, bg="#ffffff", padx=20, pady=20)
    rframe.pack(side="right", fill="both", expand=True)

    search_frame = tk.Frame(rframe, bg="#ffffff")
    search_frame.pack(fill="x")

    tk.Label(search_frame, text="Search by Employee ID",
             bg="#ffffff").grid(row=1,column=0)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=1,column=1)

    tk.Button(search_frame, text="Search", bg="#2196F3", fg="white",
              command=search_emp).grid(row=1,column=2)
   
    # container frame for listbox + scrollbars
    list_frame = tk.Frame(rframe)
    list_frame.pack(fill="both", expand=True)

# vertical scrollbar (right side)
    v_scroll = tk.Scrollbar(list_frame, orient="vertical")
    v_scroll.pack(side="right", fill="y")

# horizontal scrollbar (bottom)
    h_scroll = tk.Scrollbar(list_frame, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")

# listbox
    listbox = tk.Listbox(
    list_frame,
    height=20,
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set
   )
    listbox.pack(side="left", fill="both", expand=True)

# connect scrollbars to listbox
    v_scroll.config(command=listbox.yview)
    h_scroll.config(command=listbox.xview)

# bind selection
    listbox.bind("<<ListboxSelect>>", on_select)


    fetch_data()
    def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
    win.protocol("WM_DELETE_WINDOW", back_to_dashboard)