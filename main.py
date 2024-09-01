import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk



















def clear_default_text(event):
    if login_entry.get() == "Username":
        login_entry.delete(0, END)

def clear_password_text(event):
    if password_entry.get() == "23423":
        password_entry.delete(0, END)

root = tkinter.Tk() 
root.title("Funpay Automation")  # Set the window title

root.geometry("600x250")  # Set the window size

mainframe = ttk.Frame(root)  # Specify the root as the parent for mainframe

# First Row
loginLabel = ttk.Label(mainframe, text="Login", font=("Arial", 15))
loginLabel.grid(row=0, column=1, pady=10)

login_entry = ttk.Entry(mainframe, exportselection=0, width=30, font=("Arial", 15))
login_entry.grid(row=1, column=1, padx=10)  # Decreased pady to 2
login_entry.insert(0, "Username")  # Set default text
login_entry.bind("<FocusIn>", clear_default_text)  # Bind the function to the FocusIn event

password_entry = ttk.Entry(mainframe, show="*", exportselection=0, width=30, font=("Arial", 15))
password_entry.grid(row=2, column=1, pady=10, padx=10)
password_entry.insert(0, "23423")  # Set default text
password_entry.bind("<FocusIn>", clear_password_text)  # Bind the function to the FocusIn event

# Set transparency
login_entry.configure(foreground="gray50")
login_entry.configure(foreground="gray50")

# Center the mainframe in the window
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

sv_ttk.set_theme("dark")

button = ttk.Button(mainframe, text="Toggle theme", command=sv_ttk.toggle_theme)
button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
