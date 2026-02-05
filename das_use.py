import tkinter as tk
from tkinter import messagebox
import sqlite3



# ================= MAIN WINDOW =================
def window_use(dash):
    win = tk.Toplevel(dash)
    win.title("User Management")
    win.state("zoomed")
    win.config(bg="#ffffff")

    selected_id = None

    # ================= FUNCTIONS =================
    def submit():
        emp = e_emp.get()
        user = e_user.get()
        pwd = e_pass.get()
        login = e_login.get()

        if emp == "" or user == "" or pwd == "" or login == "":
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (employee_id, username, password, last_login)
            VALUES (?,?,?,?)
        """, (emp, user, pwd, login))
        conn.commit()
        conn.close()
        clear()
        fetch_data()

    def fetch_data():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        for row in cur.fetchall():
            listbox.insert(tk.END, row)
        conn.close()

    def clear():
        nonlocal selected_id
        selected_id = None
        e_emp.delete(0, tk.END)
        e_user.delete(0, tk.END)
        e_pass.delete(0, tk.END)
        e_login.delete(0, tk.END)

    def on_select(event):
        nonlocal selected_id
        if not listbox.curselection():
            return

        data = listbox.get(listbox.curselection()[0])
        selected_id = data[0]

        e_emp.delete(0, tk.END)
        e_user.delete(0, tk.END)
        e_pass.delete(0, tk.END)
        e_login.delete(0, tk.END)

        e_emp.insert(0, data[1])
        e_user.insert(0, data[2])
        e_pass.insert(0, data[3])
        e_login.insert(0, data[4])

    def update():
        if selected_id is None:
            messagebox.showerror("Error", "Select a record first")
            return

        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET
                employee_id=?,
                username=?,
                password=?,
                last_login=?
            WHERE user_id=?
        """, (
            e_emp.get(),
            e_user.get(),
            e_pass.get(),
            e_login.get(),
            selected_id
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User updated successfully")
        clear()
        fetch_data()

    def delete():
        if selected_id is None:
            messagebox.showerror("Error", "Select a record first")
            return

        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id=?", (selected_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "User deleted")
        clear()
        fetch_data()

    def search():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()

        if search_entry.get() == "":
            cur.execute("SELECT * FROM users")
        else:
            cur.execute("SELECT * FROM users WHERE employee_id=?",
                        (search_entry.get(),))

        for row in cur.fetchall():
            listbox.insert(tk.END, row)
        conn.close()

    # ================= UI =================
    left = tk.Frame(win, bg="#ffffff", width=350)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    right = tk.Frame(win, bg="#ffffff", padx=20, pady=20)
    right.pack(side="right", fill="both", expand=True)

    tk.Label(left, text="USER FORM", font=("Arial", 18, "bold"),
             bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(left, text="User ID", bg="#ffffff").grid(row=1, column=0, pady=8)
    e_emp = tk.Entry(left)
    e_emp.grid(row=1, column=1)

    tk.Label(left, text="Username", bg="#ffffff").grid(row=2, column=0, pady=8)
    e_user = tk.Entry(left)
    e_user.grid(row=2, column=1)

    tk.Label(left, text="Password", bg="#ffffff").grid(row=3, column=0, pady=8)
    e_pass = tk.Entry(left, show="*")
    e_pass.grid(row=3, column=1)

    tk.Label(left, text="Last Login", bg="#ffffff").grid(row=4, column=0, pady=8)
    e_login = tk.Entry(left)
    e_login.grid(row=4, column=1)

    tk.Button(left, text="Submit", bg="green", fg="white",
              width=12, command=submit).grid(row=5, column=0, pady=15)
    tk.Button(left, text="Clear", bg="orange",
              width=12, command=clear).grid(row=5, column=1)

    tk.Button(left, text="Update", bg="blue", fg="white",
              width=12, command=update).grid(row=6, column=0, pady=10)
    tk.Button(left, text="Delete", bg="red", fg="white",
              width=12, command=delete).grid(row=6, column=1)

    search_frame = tk.Frame(right, bg="#ffffff")
    search_frame.pack(fill="x")

    tk.Label(search_frame, text="Search by User ID",
             bg="#ffffff").grid(row=0, column=0)
    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1)
    tk.Button(search_frame, text="Search",
              command=search).grid(row=0, column=2)

    list_frame = tk.Frame(right)
    list_frame.pack(fill="both", expand=True)

    v_scroll = tk.Scrollbar(list_frame, orient="vertical")
    v_scroll.pack(side="right", fill="y")

    h_scroll = tk.Scrollbar(list_frame, orient="horizontal")
    h_scroll.pack(side="bottom", fill="x")

    listbox = tk.Listbox(list_frame,
                         yscrollcommand=v_scroll.set,
                         xscrollcommand=h_scroll.set)
    listbox.pack(fill="both", expand=True)

    v_scroll.config(command=listbox.yview)
    h_scroll.config(command=listbox.xview)

    listbox.bind("<<ListboxSelect>>", on_select)

    fetch_data()
    def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
    win.protocol("WM_DELETE_WINDOW", back_to_dashboard)
