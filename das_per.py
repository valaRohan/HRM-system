
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date

def window_per(dash):
    win = tk.Toplevel(dash)
    win.title("Employee Performance")
    win.state("zoomed")
    win.config(bg="#ffffff")

    select_id = None

    # ---------------- DATABASE FUNCTIONS ---------------- #

    def submit():
        emp_id = e_emp.get()
        rating = e_rating.get()
        review = e_review.get("1.0", tk.END).strip()
        rdate = e_date.get()

        if emp_id == "" or rating == "" or review == "":
            messagebox.showerror("Error", "All fields are required")
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
            INSERT INTO performance(employee_id, rating, review, review_date)
            VALUES (?, ?, ?, ?)
        """, (emp_id, rating, review, rdate))

        conn.commit()
        conn.close()

        clear()
        fetch_data()
        

    def fetch_data():
        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()

        listbox.delete(0, tk.END)
        cursor.execute("SELECT * FROM performance")
        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    def clear():
        global select_id
        select_id = None
        e_emp.delete(0, tk.END)
        e_rating.set("5")
        e_review.delete("1.0", tk.END)
        e_date.delete(0, tk.END)
        

    def on_select(event):
        global select_id
        selected = listbox.curselection()
        if selected:
            data = listbox.get(selected[0])
            select_id = data[0]

            e_emp.delete(0, tk.END)
            e_review.delete("1.0", tk.END)
            e_date.delete(0, tk.END)


            e_emp.insert(0, data[1])
            e_rating.set(data[2])
            e_review.insert(tk.END, data[3])
            e_date.insert(0, data[4])
          
          

    def delete():
        global select_id
        if select_id is None:
            messagebox.showerror("Error", "Select a record to delete")
            return

        conn = sqlite3.connect("hrm.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM performance WHERE performance_id=?", (select_id,))
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
            UPDATE performance SET
                employee_id=?,
                rating=?,
                review=?,
                review_date=?
            WHERE performance_id=?
        """, (
            e_emp.get(),
            e_rating.get(),
            e_review.get("1.0", tk.END),
            e_date.get(),
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
            cursor.execute("SELECT * FROM performance")
        else:
            cursor.execute("SELECT * FROM performance WHERE employee_id=?", (emp_id,))

        for row in cursor.fetchall():
            listbox.insert(tk.END, row)

        conn.close()

    # ---------------- LEFT FRAME (FORM) ---------------- #

    lframe = tk.Frame(win, bg="#ffffff", width=100)
    lframe.pack(side="left", fill="y", padx=20, pady=20)
    lframe.pack_propagate(False)

    
    tk.Label(lframe, text="Employee ID", bg="#f7f7f7").grid(row=1,column=1)
    e_emp = tk.Entry(lframe)
    e_emp.grid(row=1,column=2)

    tk.Label(lframe, text="Rating (1-5)", bg="#f7f7f7").grid(row=2,column=1)
    e_rating = tk.StringVar()
    e_rating.set("5")
    tk.OptionMenu(lframe, e_rating, "1", "2", "3", "4", "5").grid(row=2,column=2)

    tk.Label(lframe,text="Review", bg="#f7f7f7").grid(row=3,column=1)
    e_review = tk.Text(lframe, height=3)
    e_review.grid(row=3,column=2)

    tk.Label(lframe, text="Review Date", bg="#f7f7f7").grid(row=4,column=1)
    e_date = tk.Entry(lframe)
    e_date.grid(row=4,column=2)
    

    tk.Button(lframe, text="Submit", bg="green", fg="white",
              width=12, command=submit).grid(row=5,column=1,padx=5,pady=5)

    tk.Button(lframe, text="Clear", bg="gray", fg="white",
              width=12, command=clear).grid(row=5,column=2,padx=5,pady=5)
    
    tk.Button(lframe, text="Delete", bg="red", fg="white",
              width=12, command=delete).grid(row=6,column=1,padx=5,pady=5)

    tk.Button(lframe, text="Update", bg="blue", fg="white",
              width=12, command=update).grid(row=6,column=2,padx=5,pady=5)
    # ---------------- RIGHT FRAME (LIST) ---------------- #

    rframe = tk.Frame(win, bg="#ffffff",width=500)
    rframe.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    search_frame = tk.Frame(rframe, bg="#ffffff")
    search_frame.pack(fill="x")

    tk.Label(search_frame, text="Search by Employee ID",
             bg="#ffffff").pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)

    tk.Button(search_frame, text="Search", bg="#2196F3", fg="white",
              command=search_emp).pack(side="left", padx=5)

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


