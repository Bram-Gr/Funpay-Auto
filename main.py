import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk

root = tkinter.Tk() 
root.title("Funpay Automation")  # Set the window title

root.geometry("600x250")  # Set the window size

mainframe = ttk.Frame(root)  # Specify the root as the parent for mainframe

# First Row
loginLabel = ttk.Label(mainframe, text="Login", font=("Arial", 15))
loginLabel.grid(row=0, column=1, pady=10)

login_entry = ttk.Entry(mainframe, exportselection=0, width=30, font=("Arial", 15))
login_entry.grid(row=1, column=1, padx=10)  # Decreased pady to 2

password_entry = ttk.Entry(mainframe, show="*", exportselection=0, width=30, font=("Arial", 15))
password_entry.grid(row=2, column=1, pady=10, padx=10)
password_entry.focus_set()

# Center the mainframe in the window
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)


sv_ttk.set_theme("dark")

button = ttk.Button(mainframe, text="Toggle theme", command=sv_ttk.toggle_theme)
button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()