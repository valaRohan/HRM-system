import tkinter as tk
from tkinter import messagebox
import sqlite3
def window_emp(dash):
 win=tk.Toplevel(dash) 
 win.title("employee detail")
 win.state("zoomed")
 win.config(bg="#ffffff")
 select_id = None


 
 def submit():
    id=e_id.get()
    name=e_name.get()
    last=e_last.get()
    email=e_email.get()
    mobil=e_mobile.get()
    gender=e_gen.get()
    birth=e_birth.get()
    hire=e_hire.get()
    department=e_dep.get()
    status=e_sta.get()

    conn=sqlite3.connect("hrm.db")
    cursor=conn.cursor()

    if id=="" or name=="" or last=="" or email=="" or mobil=="" or gender=="" or birth=="" or hire=="" or department=="" or status=="":
      messagebox.showinfo("data","data not successful")
    else:
       cursor.execute("insert into employees( employee_id,first_name,last_name,email,mobile,gender,date_of_birth,hire_date,department,status) values (?,?,?,?,?,?,?,?,?,?)",(id,name,last,email,mobil,gender,birth,hire,department,status))
       messagebox.showinfo("data","data save successful")
       conn.commit()
       conn.close()
       clear()
       fetch_data()

 def fetch_data():
   conn=sqlite3.connect("hrm.db")
   cursor=conn.cursor()

   listbox.delete(0,tk.END)
   cursor.execute("select * from employees")
   for row in cursor.fetchall():
        listbox.insert(tk.END,row)

 def clear():
   global select_id 
   select_id=None
   e_id.delete(0,tk.END)
   e_name.delete(0,tk.END)
   e_last.delete(0,tk.END)
   e_email.delete(0,tk.END)
   e_mobile.delete(0,tk.END)
   e_gen.set("male")
   e_birth.delete(0,tk.END)
   e_hire.delete(0,tk.END)
   e_dep.set("Human Resources")
   e_sta.set("Active")
 def on_select(event):
    
    global select_id
    selected=listbox.curselection()
    if selected:
        data=listbox.get(selected[0])
        select_id=data[0]
        
        e_id.delete(0,tk.END)
        e_name.delete(0,tk.END)
        e_last.delete(0,tk.END) 
        e_email.delete(0,tk.END)
        e_mobile.delete(0,tk.END) 
        e_birth.delete(0,tk.END)
        e_hire.delete(0,tk.END)
        

        e_id.insert(0,data[0])
        e_name.insert(0, data[1])
        e_last.insert(0, data[2])
        e_email.insert(0, data[3])
        e_mobile.insert(0, data[4])
        e_gen.set(data[5])
        e_birth.insert(0, data[6])
        e_hire.insert(0, data[7])
        e_dep.set(data[8])
        e_sta.set(data[9])
 def delete():
    global select_id

    if select_id is None:
        messagebox.showerror("Error", "Select a record to delete")
        return

    conn = sqlite3.connect("hrm.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE employee_id = ?",
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
        UPDATE employees SET
            employee_id = ?,
            first_name = ?,
            last_name = ?,
            email = ?,
            mobile = ?,
            gender = ?,
            date_of_birth = ?,
            hire_date = ?,
            department = ?,
            status = ?
        WHERE employee_id = ?
    """, (
       e_id.get(),
        e_name.get(),
        e_last.get(),
        e_email.get(),
        e_mobile.get(),
        e_gen.get(),
        e_birth.get(),
        e_hire.get(),
        e_dep.get(),
        e_sta.get(),
        select_id
    ))

    conn.commit()
    conn.close()

    clear()
    fetch_data()

    messagebox.showinfo("Success", "Record updated successfully")
 
 def search_emp():
    emp_id = search_entry.get().strip()

    conn = sqlite3.connect("hrm.db")
    cursor = conn.cursor()

    listbox.delete(0, tk.END)

    if emp_id == "":
        cursor.execute("SELECT * FROM employees")
    else:
        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = ?",
            (emp_id,)
        )

    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

    conn.close()


 tframe = tk.Frame(win, width=850,bg="#ffffff",height=200)
 tframe.pack(side="left",fill="y",expand=False)
 tframe.pack_propagate(False)

 e_id=tk.Label(tframe,text="id",bg="#ffffff",fg="black",font=("arial",12)).grid(row=0,column=1,padx=20,pady=25)
 e_id=tk.Entry(tframe,bd=1,relief="solid")
 e_id.grid(row=0,column=2,padx=25,pady=20)

 e_name=tk.Label(tframe,text="First Name",bg="#ffffff",fg="black",font=("arial",12)).grid(row=1,column=1,padx=20,pady=25)
 e_name=tk.Entry(tframe,bd=1,relief="solid")
 e_name.grid(row=1,column=2,padx=25,pady=20)

 tk.Label(tframe,text="Last Name",fg="black",bg="#ffffff",font=("arial",12)).grid(row=2,column=1,padx=20,pady=20)
 e_last=tk.Entry(tframe,bd=1,relief="solid")
 e_last.grid(row=2,column=2,padx=25,pady=20)

 tk.Label(tframe,text="E-mail",fg="black",bg="#ffffff",font=("arial",12)).grid(row=3,column=1,padx=20,pady=20)
 e_email=tk.Entry(tframe,bd=1,relief="solid")
 e_email.grid(row=3,column=2,padx=20,pady=20)

 tk.Label(tframe,text="Mobile",fg="black",bg="#ffffff",font=("arial",12)).grid(row=4,column=1,padx=20,pady=20)
 e_mobile=tk.Entry(tframe,bd=1,relief="solid")
 e_mobile.grid(row=4,column=2,padx=20,pady=20)

 tk.Label(tframe,text="gender",fg="black",bg="#ffffff",font=("arial",12)).grid(row=5,column=1,padx=20,pady=20)
 e_gen=tk.StringVar(tframe)
 e_gen.set("male")
 tk.OptionMenu(tframe,e_gen,"male","female","other").grid(row=5,column=2,padx=20,pady=20)
 
 tk.Label(tframe,text="Date of Birth",fg="black",bg="#ffffff",font=("arial",12)).grid(row=6,column=1,padx=20,pady=20)
 e_birth=tk.Entry(tframe,bd=1,relief="solid")
 e_birth.grid(row=6,column=2,padx=20,pady=20)

 tk.Label(tframe,text="Hire Date",fg="black",bg="#ffffff",font=("arial",12)).grid(row=7,column=1,padx=20,pady=20)
 e_hire=tk.Entry(tframe,bd=1,relief="solid")
 e_hire.grid(row=7,column=2,padx=20,pady=20)

 tk.Label(tframe,text="Department",fg="black",bg="#ffffff",font=("arial",12)).grid(row=8,column=1,padx=20,pady=20)
 e_dep=tk.StringVar(tframe)
 e_dep.set("Human Resources")
 tk.OptionMenu(tframe,e_dep,"Human Resources","Finance","Sales","Marketing","Operations","Administration","employee").grid(row=8,column=2,padx=20,pady=20)

 tk.Label(tframe,text="Status",fg="black",bg="#ffffff",font=("arial",12)).grid(row=9,column=1,padx=20,pady=20)
 e_sta=tk.StringVar(tframe)
 e_sta.set("Active")
 tk.OptionMenu(tframe,e_sta,"Active","On Probation","Confirmed","On Leave","Resigned","Terminated").grid(row=9,column=2,padx=5,pady=5)

 
 tk.Button(tframe,text="submit",fg="black",command=submit,bd=1,relief="solid",bg="green").grid(row=10,column=1)
 tk.Button(tframe,text="clear",fg="black",command=clear,bd=1,relief="solid",bg="red").grid(row=10,column=2)
 
 rframe = tk.Frame(win, bg="#ffffff", padx=20, pady=20)
 rframe.pack(side="right", fill="both", expand=True)

 rframe.grid_columnconfigure(0, weight=1)
 rframe.grid_columnconfigure(1, weight=2)
 rframe.grid_columnconfigure(2, weight=0)

 tk.Label(rframe, text="Search by Employee ID", bg="#ffffff",font=("Arial", 12)).grid(row=0, column=0, sticky="w")
 search_entry = tk.Entry(rframe)
 search_entry.grid(row=0, column=1, sticky="ew", padx=10)
 tk.Button(rframe, text="Search", bg="#2196F3", fg="white", command=search_emp).grid(row=0, column=2)

 listbox = tk.Listbox(rframe, height=18)
 listbox.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=15)
 
 rframe.grid_rowconfigure(1, weight=1)

 btn_frame = tk.Frame(rframe, bg="#ffffff")
 btn_frame.grid(row=2, column=0, columnspan=3)

 tk.Button(btn_frame, text="Delete", bg="red", fg="white", width=12, command=delete).pack(side="left", padx=10)
 tk.Button(btn_frame, text="Update", bg="green", fg="white", width=12, command=update).pack(side="left", padx=10)

 listbox.bind("<<ListboxSelect>>", on_select)

 fetch_data()
 def back_to_dashboard():
        win.destroy()
        dash.deiconify()
        dash.state("zoomed")
 win.protocol("WM_DELETE_WINDOW", back_to_dashboard)
