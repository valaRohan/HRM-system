import tkinter as tk
from tkinter import messagebox
import sqlite3
import dashboard
from PIL import Image, ImageTk

root=tk.Tk()
root.title('login')
root.state('zoomed')
root.config(bg="#EEEEEE")


def on_login_show():
   enter_name.delete(0,tk.END)
   enter_password.delete(0,tk.END)
   enter_name.focus_set()
def submit():
  use=enter_name.get()
  pas=enter_password.get()

  conn=sqlite3.connect("hrm.db")
  cursor=conn.cursor()

  cursor.execute("select * from login where username=? and password=?",(use,pas))
  result=cursor.fetchone()
    
  if result:
     root.withdraw()
     dashboard.open_dashboard(root,on_login_show)
    
  else:
     messagebox.showerror("not successful","login is not successful")   
  
  conn.commit()
  conn.close()
     



left_frame = tk.Frame(root, bg="#EEEEEE", width=400)
left_frame.pack(side="left", fill="y")
left_frame.pack_propagate(False)

# ===== Title =====
tk.Label(
    left_frame,
    text="Human Resource",
    bg="#EEEEEE",
    font=("Arial", 24, "bold")
).pack(pady=(60, 5))

tk.Label(
    left_frame,
    text="Management System",
    bg="#EEEEEE",
    font=("Arial", 20)
).pack(pady=(0, 40))

# ===== Username =====
tk.Label(
    left_frame,
    text="Username",
    bg="#EEEEEE",
    font=("Arial", 14)
).pack(anchor="w", padx=50)

enter_name = tk.Entry(left_frame, font=("Arial", 14), bd=2, relief="solid")
enter_name.pack(padx=50, pady=8, fill="x")

# ===== Password =====
tk.Label(
    left_frame,
    text="Password",
    bg="#EEEEEE",
    font=("Arial", 14)
).pack(anchor="w", padx=50, pady=(10,0))

enter_password = tk.Entry(left_frame, show="*", font=("Arial", 14), bd=2, relief="solid")
enter_password.pack(padx=50, pady=8, fill="x")

# ===== Login Button =====
tk.Button(
    left_frame,
    text="Login",
    font=("Arial", 14, "bold"),
    bg="#0A2540",
    fg="white",
    bd=0,
    padx=10,
    pady=8,command=submit
).pack(pady=30, padx=50, fill="x")





img = Image.open("image/image.jpg")
img = img.resize((700, 400))
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo)
label.image = photo
label.pack(padx=5,pady=85)

root.mainloop()