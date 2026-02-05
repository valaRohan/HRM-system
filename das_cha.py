import tkinter as tk
from tkinter import messagebox
import sqlite3


def window_cha(dash):
    win = tk.Toplevel(dash)
    win.title("Change Password")
    win.state("zoomed")
    win.config(bg="#FFFFFF")

    tk.Label(win, text="Change Password",
             font=("Arial", 16, "bold"),
             bg="#FFFFFF").pack(pady=10)

    # ===== Username =====
    tk.Label(win, text="Username", bg="#FFFFFF").pack(anchor="w", padx=40)
    e_user = tk.Entry(win)
    e_user.pack(padx=40, fill="x")

    # ===== Old Password =====
    tk.Label(win, text="Old Password", bg="#FFFFFF").pack(anchor="w", padx=40, pady=(10, 0))
    e_old = tk.Entry(win, show="*")
    e_old.pack(padx=40, fill="x")

    # ===== New Password =====
    tk.Label(win, text="New Password", bg="#FFFFFF").pack(anchor="w", padx=40, pady=(10, 0))
    e_new = tk.Entry(win, show="*")
    e_new.pack(padx=40, fill="x")

    # ===== Confirm Password =====
    tk.Label(win, text="Confirm Password", bg="#FFFFFF").pack(anchor="w", padx=40, pady=(10, 0))
    e_confirm = tk.Entry(win, show="*")
    e_confirm.pack(padx=40, fill="x")

    def update_password():
        username = e_user.get()
        old_pass = e_old.get()
        new_pass = e_new.get()
        confirm_pass = e_confirm.get()

        if  username=="" or old_pass=="" or new_pass=="" or  confirm_pass=="":
            messagebox.showerror("Error", "All fields are required")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM login WHERE username=?",
            (username,)
        )
        row = cursor.fetchone()

        if row is None:
            messagebox.showerror("Error", "User not found")
            conn.close()
            return

        if row[0] != old_pass:
            messagebox.showerror("Error", "Old password is incorrect")
            conn.close()
            return

        cursor.execute(
            "UPDATE login SET password=? WHERE username=?",
            (new_pass, username)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password changed successfully")
        win.destroy()

    tk.Button(win, text="Change Password",
              width=20, command=update_password).pack(pady=20)
    def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
    win.protocol("WM_DELETE_WINDOW", back_to_dashboard)
