import sqlite3

conn=sqlite3.connect("hrm.db")
conn.execute("PRAGMA foreign_keys = ON")
course=conn.cursor()



course.execute(""" 
    create table if not exists login(
    id integer primary key autoincrement,
    username text,
    password text             
                
                
                )
  """)



course.execute(""" 
    create table if not exists employees(
     employee_id integer primary key, 
     first_name text,
     last_name text,
     email text,
     mobile integer,
     gender text,
     date_of_birth date,
     hire_date  date,
     department text,
     status  text       
             ) 

""")



course.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    username TEXT,
    password TEXT,
    last_login DATE


      
)
""")


course.execute(""" 
   create table if not exists attendance(
  
    attendance_id integer primary key autoincrement,
    employee_id integer,
    date date not null,
    check_in time,
    check_out time,
    status date  DEFAULT 'Present',
               
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)    )

""")


course.execute(""" 
  create table if not exists leaves(
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'pending',

   FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)        
               
                       )
 """)


course.execute(""" 
 create table if not exists salary(
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    basic_salary REAL NOT NULL,
    allowances integer DEFAULT 0,
    Deductions integer DEFAULT 0,
    net_salary integer NOT NULL,
    pay_month TEXT NOT NULL,
        
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)           
    
             )
""")

course.execute(""" 
   create table if not exists performance(
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    review TEXT,
    review_date DATE DEFAULT CURRENT_DATE,
               
     FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)  
     ) """)

course.execute(""" 
   create table if not exists employee_training(
    training_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    training_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    trainer TEXT,
          
      FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)      
     ) """)

course.execute("insert into login (username,password) values (?,?) ",('admin',1234))
conn.commit()
conn.close()
print("table")