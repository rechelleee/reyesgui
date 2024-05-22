import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

background_color = "#845EC2"
main_color = "#4B4453"
small_color = "#9B89B3"

def add_employee():
    username = username_entry.get()
    password = password_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    middle_name = middle_name_entry.get()
    
    if not all((username, password, first_name, last_name, middle_name)):
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT,
                  first_name TEXT, last_name TEXT, middle_name TEXT)''')
    
    c.execute('''INSERT INTO employees (username, password, first_name, last_name, middle_name)
                 VALUES (?, ?, ?, ?, ?)''', (username, password, first_name, last_name, middle_name))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Employee Added", "Employee has been successfully added to the database.")

def log_in():
    username = username_login_entry.get()
    password = password_login_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM employees WHERE username=? AND password=?''', (username, password))
    employee = c.fetchone()
    
    if employee:
        employee_id = employee[0]
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute('''CREATE TABLE IF NOT EXISTS employee_logs
                     (id INTEGER PRIMARY KEY, employee_id INTEGER, login_time TEXT, logout_time TEXT)''')
        c.execute('''INSERT INTO employee_logs (employee_id, login_time) VALUES (?, ?)''', (employee_id, login_time))
        conn.commit()
        
        messagebox.showinfo("Log In", f"Welcome, {employee[3]}! You have logged in at {login_time}")
        show_log_data_button.config(state="normal")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    
    conn.close()

def log_out():
    username = username_logout_entry.get()
    password = password_logout_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM employees WHERE username=? AND password=?''', (username, password))
    employee = c.fetchone()
    
    if employee:
        employee_id = employee[0]
        logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute('''UPDATE employee_logs SET logout_time=? WHERE employee_id=? AND logout_time IS NULL''', (logout_time, employee_id))
        conn.commit()
        
        messagebox.showinfo("Log Out", f"Goodbye, {employee[3]}! You have logged out at {logout_time}")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    
    conn.close()

def delete_employee():
    username = username_delete_entry.get()
    password = password_delete_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM employees WHERE username=? AND password=?''', (username, password))
    employee = c.fetchone()
    
    if employee:
        employee_id = employee[0]
        
        c.execute('''DELETE FROM employees WHERE id=?''', (employee_id,))
        conn.commit()
        
        messagebox.showinfo("Employee Deleted", f"Employee {username} has been successfully deleted.")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    
    conn.close()

def show_log_data():
    username = username_login_entry.get()
    password = password_login_entry.get()
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM employees WHERE username=? AND password=?''', (username, password))
    employee = c.fetchone()
    
    if employee:
        employee_id = employee[0]
        
        c.execute('''SELECT * FROM employee_logs WHERE employee_id=?''', (employee_id,))
        log_data = c.fetchall()
        
        if log_data:
            log_data_str = "\n".join([f"Login Time: {data[2]}, Logout Time: {data[3]}" for data in log_data])
            messagebox.showinfo("Log Data", f"Log data for {username}:\n{log_data_str}")
        else:
            messagebox.showinfo("Log Data", "No log data available for this employee.")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    
    conn.close()

root = tk.Tk()
root.title("Employee Management App")
root.configure(background=background_color)

add_employee_frame = tk.LabelFrame(root, text="Add Employee", bg=background_color, fg=main_color)
add_employee_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

username_label = tk.Label(add_employee_frame, text="Username:", bg=background_color, fg=main_color)
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = tk.Entry(add_employee_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

password_label = tk.Label(add_employee_frame, text="Password:", bg=background_color, fg=main_color)
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(add_employee_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

first_name_label = tk.Label(add_employee_frame, text="First Name:", bg=background_color, fg=main_color)
first_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
first_name_entry = tk.Entry(add_employee_frame)
first_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

last_name_label = tk.Label(add_employee_frame, text="Last Name:", bg=background_color, fg=main_color)
last_name_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
last_name_entry = tk.Entry(add_employee_frame)
last_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

middle_name_label = tk.Label(add_employee_frame, text="Middle Name:", bg=background_color, fg=main_color)
middle_name_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
middle_name_entry = tk.Entry(add_employee_frame)
middle_name_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

add_employee_button = tk.Button(add_employee_frame, text="Add Employee", command=add_employee, bg=main_color, fg="white")
add_employee_button.grid(row=5, columnspan=2, padx=5, pady=10)

log_in_frame = tk.LabelFrame(root, text="Log In", bg=background_color, fg=main_color)
log_in_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

username_login_label = tk.Label(log_in_frame, text="Username:", bg=background_color, fg=main_color)
username_login_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_login_entry = tk.Entry(log_in_frame)
username_login_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

password_login_label = tk.Label(log_in_frame, text="Password:", bg=background_color, fg=main_color)
password_login_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_login_entry = tk.Entry(log_in_frame, show="*")
password_login_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

log_in_button = tk.Button(log_in_frame, text="Log In", command=log_in, bg=main_color, fg="white")
log_in_button.grid(row=2, columnspan=2, padx=5, pady=10)

log_out_frame = tk.LabelFrame(root, text="Log Out", bg=background_color, fg=main_color)
log_out_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

username_logout_label = tk.Label(log_out_frame, text="Username:", bg=background_color, fg=main_color)
username_logout_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_logout_entry = tk.Entry(log_out_frame)
username_logout_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

password_logout_label = tk.Label(log_out_frame, text="Password:", bg=background_color, fg=main_color)
password_logout_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_logout_entry = tk.Entry(log_out_frame, show="*")
password_logout_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

log_out_button = tk.Button(log_out_frame, text="Log Out", command=log_out, bg=main_color, fg="white")
log_out_button.grid(row=2, columnspan=2, padx=5, pady=10)

delete_employee_frame = tk.LabelFrame(root, text="Delete Employee", bg=background_color, fg=main_color)
delete_employee_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

username_delete_label = tk.Label(delete_employee_frame, text="Username:", bg=background_color, fg=main_color)
username_delete_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_delete_entry = tk.Entry(delete_employee_frame)
username_delete_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

password_delete_label = tk.Label(delete_employee_frame, text="Password:", bg=background_color, fg=main_color)
password_delete_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_delete_entry = tk.Entry(delete_employee_frame, show="*")
password_delete_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

delete_employee_button = tk.Button(delete_employee_frame, text="Delete Employee", command=delete_employee, bg=main_color, fg="white")
delete_employee_button.grid(row=2, columnspan=2, padx=5, pady=10)

show_log_data_button = tk.Button(root, text="Show Log Data", command=show_log_data, bg=main_color, fg="white", state="disabled")
show_log_data_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

root.mainloop()
