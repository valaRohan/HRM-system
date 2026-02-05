import tkinter as tk
from tkinter import messagebox
import sqlite3
def window_att(dash):
  win=tk.Toplevel(dash)
  win.title("employee attendance")
  win.state("zoomed")
  
  def submit():
        emp_id = e_id.get()
        date = e_date.get()
        cin = e_in.get()
        cout = e_out.get()
        status = e_status.get()


        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

       

    
        if emp_id == "" or date == "":
            messagebox.showerror("Error", "Employee ID and Date are required")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance
            (employee_id, date, check_in, check_out, status)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, date, cin, cout, status))

        conn.commit()
        conn.close()

        fetch_data()
        clear()
       
  def fetch_data():
        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        listbox.delete(0, tk.END)
        cursor.execute("SELECT * FROM attendance")
        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()
  def on_select(event):
        global select_id
        selected = listbox.curselection()
        if selected:
            data = listbox.get(selected[0])
            select_id = data[0]

            e_id.delete(0, tk.END)
            e_date.delete(0, tk.END)
            e_in.delete(0, tk.END)
            e_out.delete(0, tk.END)

            e_id.insert(0, data[1])
            e_date.insert(0, data[2])
            e_in.insert(0, data[3])
            e_out.insert(0, data[4])
            e_status.set(data[5])
  def clear():
        global select_id
        select_id = None
        e_id.delete(0, tk.END)
        e_date.delete(0, tk.END)
        e_in.delete(0, tk.END)
        e_out.delete(0, tk.END)
        e_status.set("Present")
  def update():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select a record to update")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        cursor.execute("""UPDATE attendance SET employee_id = ?,date = ?,check_in = ?,check_out = ?,status = ? WHERE attendance_id = ?
        """, (e_id.get(),e_date.get(),e_in.get(),e_out.get(),e_status.get(),select_id))

        conn.commit()
        conn.close()

        fetch_data()
        clear()
    
  def delete():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select a record to delete")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM attendance WHERE attendance_id = ?",
            (select_id,)
        )

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
            cursor.execute("SELECT * FROM attendance")
        else:
            cursor.execute(
                "SELECT * FROM attendance WHERE employee_id=?",
                (emp_id,)
            )

        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

 
  tframe = tk.Frame(win, width=850, height=550, bg="#ffffff")
  tframe.pack(side="left",fill="y",expand=False)
  tframe.pack_propagate(False)
  
  tk.Label(tframe,text="employee_id",bg="#ffffff",fg="black",font=("arial",12)).grid(row=0,column=1,padx=20,pady=25)
  e_id=tk.Entry(tframe,bd=1,relief="solid")
  e_id.grid(row=0,column=2,padx=25,pady=20)

  tk.Label(tframe,text="Date (YYYY-MM-DD)",fg="black",bg="#ffffff",font=("arial",12)).grid(row=1,column=1,padx=20,pady=20)
  e_date=tk.Entry(tframe,bd=1,relief="solid")
  e_date.grid(row=1,column=2,padx=25,pady=20)

  tk.Label(tframe,text="Check In (HH:MM)",fg="black",bg="#ffffff",font=("arial",12)).grid(row=2,column=1,padx=20, pady=20)
  e_in=tk.Entry(tframe,bd=1,relief="solid")
  e_in.grid(row=2,column=2,padx=20,pady=20)

  tk.Label(tframe,text="Check Out (HH:MM)",fg="black",bg="#ffffff",font=("arial",12)).grid(row=3,column=1,padx=20, pady=20)
  e_out=tk.Entry(tframe,bd=1,relief="solid")
  e_out.grid(row=3,column=2,padx=20,pady=20)

  tk.Label(tframe,text="Status",fg="black",bg="#ffffff",font=("arial",12)).grid(row=4,column=1,padx=20, pady=20)
  e_status=tk.StringVar(tframe)
  e_status.set("Present")
  tk.OptionMenu(tframe,e_status,"Present","Absent","Late","Half-Day").grid(row=4,column=2,padx=20,pady=20)
  
  tk.Button(tframe,text="submit",bg="green",fg="white",command=submit,bd=1,relief="solid").grid(row=5,column=1,pady=5)
  tk.Button(tframe,text="clear",bg="#2196F3", fg="white",command=clear,bd=1,relief="solid").grid(row=5,column=2)
  tk.Button(tframe,text="update",bg="red", fg="white",command=update,bd=1,relief="solid").grid(row=6,column=1,pady=5)
  tk.Button(tframe,text="delete",bg="#9E9E9E", fg="white",command=delete,bd=1,relief="solid").grid(row=6,column=2)

  right = tk.Frame(win,bg="#ffffff")
  right.pack(side="right", fill="both", expand=True)

  search_frame = tk.Frame(right, bg="#ffffff")
  search_frame.pack(fill="x")

  tk.Label(search_frame, text="Search by Employee ID",
             bg="#ffffff").grid(row=1,column=1)

  search_entry = tk.Entry(search_frame)
  search_entry.grid(row=1,column=2)

  tk.Button(search_frame, text="Search",
              bg="#2196F3", fg="white",
              command=search_emp).grid(row=1,column=3)

  # Frame to hold listbox + scrollbars
  list_frame = tk.Frame(right)
  list_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Vertical Scrollbar (right side)
  v_scroll = tk.Scrollbar(list_frame, orient="vertical")
  v_scroll.pack(side="right", fill="y")

# Horizontal Scrollbar (bottom)
  h_scroll = tk.Scrollbar(list_frame, orient="horizontal")
  h_scroll.pack(side="bottom", fill="x")

# Listbox
  listbox = tk.Listbox(
    list_frame,
    font=("Consolas", 11),
    yscrollcommand=v_scroll.set,
    xscrollcommand=h_scroll.set
  )
  listbox.pack(side="left", fill="both", expand=True)

# Connect scrollbars to listbox
  v_scroll.config(command=listbox.yview)
  h_scroll.config(command=listbox.xview)

# Bind select event
  listbox.bind("<<ListboxSelect>>", on_select)

  
  fetch_data()
  def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
  win.protocol("WM_DELETE_WINDOW", back_to_dashboard)
