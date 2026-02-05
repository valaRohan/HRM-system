import tkinter as tk
from tkinter import messagebox
from das_emp import window_emp
from das_dep import window_dep
from das_att import window_att
from das_use import window_use
from das_sal import window_sal
from das_per import window_per
from das_tra import window_tra
from das_lev import window_lev
from das_cha import window_cha
from PIL import Image, ImageTk


def open_dashboard(root, on_login_show):

    # ✅ FIX: use Toplevel, NOT Tk
    dash = tk.Toplevel(root)
    dash.title("menubar")
    dash.state("zoomed")
    dash.config(bg="#FFFFFF")

    root.withdraw()   # hide login window

    # ===== Title Frame =====
    title_frame = tk.Frame(dash, bg="#0A2540", pady=10)
    title_frame.pack(side="top", fill="x")

    man = tk.Label(
        title_frame,
        text="Human Resource Management System",
        font=("Georgia", 20, "bold"),
        bg="#0A2540",
        fg="#ffffff"
    )
    man.pack()

    # ===== Image Section =====
    image_frame = tk.Frame(dash, bg="#FFFFFF")
    image_frame.pack(pady=20)

    img = Image.open("image/menubar.jpg")
    img = img.resize((900, 400), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(image_frame, image=photo, bg="#FFFFFF")
    label.image = photo
    label.pack()

    # ===== MENUBAR Frame =====
    frame = tk.Frame(dash, bg="#0A2540", padx=30, pady=20)
    frame.pack(pady=30)

    tk.Button(frame, text="employee detail", width=20,
              command=lambda: open_emp(dash)).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(frame, text="roles", width=20,
              command=lambda: open_dep(dash)).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(frame, text="users", width=20,
              command=lambda: open_user(dash)).grid(row=1, column=3, padx=10, pady=10)

    tk.Button(frame, text="attendance", width=20,
              command=lambda: open_att(dash)).grid(row=1, column=4, padx=10, pady=10)

    tk.Button(frame, text="change password", width=20,
              command=lambda: open_cha(dash)).grid(row=1, column=5, padx=10, pady=10)

    tk.Button(frame, text="salary", width=20,
              command=lambda: open_sal(dash)).grid(row=2, column=1, padx=10, pady=10)
    
    

    tk.Button(frame, text="performance", width=20,
              command=lambda: open_per(dash)).grid(row=2, column=2, padx=10, pady=10)

    tk.Button(frame, text="employee_training", width=20,
              command=lambda: open_tra(dash)).grid(row=2, column=3, padx=10, pady=10)

    tk.Button(frame, text="leave", width=20,
              command=lambda: open_lev(dash)).grid(row=2, column=4, padx=10, pady=10)

    def logout():
        if messagebox.askyesno("logout", "are you sure you want to logout"):
            dash.destroy()
            root.deiconify()
            root.state("zoomed")
            root.lift()
            root.focus_force()
            on_login_show()

    tk.Button(frame, text="logout", width=20,
              command=logout).grid(row=2, column=5, rowspan=2, padx=10, pady=10)


# ===== Window Openers =====
def open_emp(dash):
    dash.withdraw()
    window_emp(dash)

def open_dep(dash):
    dash.withdraw()
    window_dep(dash)

def open_user(dash):
    dash.withdraw()
    window_use(dash)

def open_att(dash):
    dash.withdraw()
    window_att(dash)

def open_sal(dash):
    dash.withdraw()
    window_sal(dash)

def open_per(dash):
    dash.withdraw()
    window_per(dash)

def open_tra(dash):
    dash.withdraw()
    window_tra(dash)

def open_lev(dash):
    dash.withdraw()
    window_lev(dash)

def open_cha(dash):
    dash.withdraw()
    window_cha(dash)
