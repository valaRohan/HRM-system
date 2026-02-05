import tkinter as tk
from tkinter import messagebox
import sqlite3

def window_lev(dash):
    win = tk.Toplevel(dash)
    win.title("Leave Management")
    win.state("zoomed")
    win.config(bg="#ffffff")

    select_id = None

    # ---------------- FUNCTIONS ----------------
    def submit():
            emp = e_emp.get()
            frm = e_from.get()
            to = e_to.get()
            reason = e_reason.get("1.0", tk.END).strip()
            status = e_status.get()

            if emp == "" or frm == "" or to == "":
                messagebox.showerror("Error", "All fields required")
                return

            conn = sqlite3.connect("hrm.db")
            cursor = conn.cursor()

            # check employee exists
            cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (emp,))
            data = cursor.fetchone()

            if data is None:
                  messagebox.showerror("Error", "Employee not found")
                  conn.close()
                  return

            # insert leave (only if employee exists)
            cursor.execute(
                "INSERT INTO leaves (employee_id, from_date, to_date, reason, status) VALUES (?,?,?,?,?)",
                (emp, frm, to, reason, status)
             )

            conn.commit()
            conn.close()

            fetch_data()
            clear()
    
    def fetch_data():
        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        listbox.delete(0, tk.END)
        cursor.execute("SELECT * FROM leaves")
        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    def clear():
        global select_id
        select_id = None
        e_emp.delete(0, tk.END)
        e_from.delete(0, tk.END)
        e_to.delete(0, tk.END)
        e_reason.delete("1.0", tk.END)
        e_status.set("Pending")

    def on_select(event):
        global select_id
        selected = listbox.curselection()
        if selected:
            data = listbox.get(selected[0])
            select_id = data[0]

            e_emp.delete(0, tk.END)
            e_from.delete(0, tk.END)
            e_to.delete(0, tk.END)
            e_reason.delete("1.0", tk.END)
        

            e_emp.insert(0, data[1])
            e_from.insert(0, data[2])
            e_to.insert(0, data[3])
            e_reason.insert(tk.END, data[4])
            e_status.set(data[5])

    def delete():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select record to delete")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leaves WHERE leave_id=?", (select_id,))
        conn.commit()
        conn.close()

        clear()
        fetch_data()

    def update():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select record to update")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE leaves SET
                employee_id=?,
                from_date=?,
                to_date=?,
                reason=?,
                status=?
            WHERE leave_id=?
        """, (
            e_emp.get(),
            e_from.get(),
            e_to.get(),
            e_reason.get("1.0", tk.END).strip(),
            e_status.get(),
            select_id
        ))
        conn.commit()
        conn.close()

        fetch_data()
        clear()
    
    def search_emp():
        emp_id = search_entry.get().strip()

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        listbox.delete(0, tk.END)

        if emp_id == "":
            cursor.execute("SELECT * FROM leaves")
        else:
            cursor.execute("SELECT * FROM leaves WHERE employee_id=?", (emp_id,))

        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    # ---------------- UI ----------------

    lframe = tk.Frame(win,width=850,bg="#ffffff",height=550)
    lframe.pack(side="left", fill="y")

    tk.Label(lframe, text="Employee ID",bg="#ffffff").grid(row=0, column=0, pady=10)
    e_emp = tk.Entry(lframe)
    e_emp.grid(row=0, column=1)

    tk.Label(lframe, text="From Date",bg="#ffffff").grid(row=1, column=0, pady=10)
    e_from = tk.Entry(lframe)
    e_from.grid(row=1, column=1)

    tk.Label(lframe, text="To Date",bg="#ffffff").grid(row=2, column=0, pady=10)
    e_to = tk.Entry(lframe)
    e_to.grid(row=2, column=1)

    tk.Label(lframe, text="Reason",bg="#ffffff").grid(row=3, column=0, pady=10)
    e_reason = tk.Text(lframe, height=4, width=20)
    e_reason.grid(row=3, column=1)

    tk.Label(lframe, text="Status",bg="#ffffff").grid(row=4, column=0, pady=10)
    e_status = tk.StringVar(lframe)
    e_status.set("Approved")
    tk.OptionMenu(lframe, e_status, "Pending", "Approved", "Rejected").grid(row=4, column=1)

    tk.Button(lframe, text="Submit", bg="green", fg="white", width=12,command=submit).grid(row=5, column=0, pady=20)
    tk.Button(lframe, text="Clear", bg="red", fg="white", width=12,command=clear).grid(row=5, column=1)
    tk.Button(lframe, text="Update", bg="blue", fg="white", width=12, command=update).grid(row=6, column=0)
    tk.Button(lframe, text="Delete", bg="red", fg="white", width=12, command=delete).grid(row=6, column=1)

    # ---------------- RIGHT FRAME ----------------

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
