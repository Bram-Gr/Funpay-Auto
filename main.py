import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cService = webdriver.ChromeService(executable_path="E:\\chromedriver-win64\\chromedriver.exe")


def login_button_click():

    driver = webdriver.Chrome(service = cService)
    driver.get("https://funpay.com/en/account/login")
    try:
        #Disable typing in the entry fields
        mainframe.place_forget()

        instructions.grid(row=0, column=1, pady=10)
        sleep(5)
        
        #Wait for the login page to load

        login_input = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        passwrod_input = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.NAME,"password"))
        )
        #Enter the login and password
        login_input.send_keys(login_entry.get())
        passwrod_input.send_keys(password_entry.get())

    except Exception as e:
        print(e)















def clear_default_text(event):
    
    if login_entry.get() == "Username":
        login_entry.delete(0, END)
def clear_password_text(event):
    if password_entry.get() == "23423":
        password_entry.delete(0, END)

root = tkinter.Tk() 
root.title("Funpay Automation") 

root.geometry("600x250")  

#Main frame for the login page
mainframe = ttk.Frame(root)  

#Frame after login was pressed
afterloginframe = ttk.Frame(root)

afterloginframe.place(relx=0.5, rely=0.5, anchor=CENTER)
instructions = ttk.Label(afterloginframe, text="Please complete the captcha and log in", font=("Arial", 15))


# Login label and formatting
loginLabel = ttk.Label(mainframe, text="Login", font=("Arial", 15))
loginLabel.grid(row=0, column=1, pady=10)

# Login entry space and formatting
login_entry = ttk.Entry(mainframe, exportselection=0, width=30, font=("Arial", 15))
login_entry.grid(row=1, column=1, padx=10)  
login_entry.insert(0, "Username")  
login_entry.bind("<FocusIn>", clear_default_text) 

# Password entry space and formatting
password_entry = ttk.Entry(mainframe, show="*", exportselection=0, width=30, font=("Arial", 15))
password_entry.grid(row=2, column=1, pady=10, padx=10)
password_entry.insert(0, "23423") 
password_entry.bind("<FocusIn>", clear_password_text) 

#Login button
try_login_button = ttk.Button(mainframe, text="Login", command=login_button_click)
try_login_button.grid(row=3, column=1, pady=10)
# Set transparency for insert text
login_entry.configure(foreground="gray50")
login_entry.configure(foreground="gray50")

# Center the mainframe in the window
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

#Sets the theme
sv_ttk.set_theme("dark")

# Button to toggle the theme
button = ttk.Button(root, text="Toggle theme", command=sv_ttk.toggle_theme)
button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
