import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from time import sleep
from bs4 import BeautifulSoup

cService = webdriver.ChromeService(executable_path="E:\\chromedriver-win64\\chromedriver.exe")

driver = None

def login_button_click():
    global driver
    driver = webdriver.Chrome(service=cService)
    driver.get("https://funpay.com/en/")
    load_cookies(driver)
    driver.get("https://funpay.com/en/")
    a = check_logged_in()
    print(a)
    if a == True:
        mainframe.place_forget()
        frame4.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        driver.get("https://funpay.com/en/account/login")
        try:
            #Disable typing in the entry fields
            mainframe.place_forget()

            instructionsframe.place(relx=0.5, rely=0.5, anchor=CENTER)
            
            #Wait for the login page to load

            login_input = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.NAME, "login"))
            )
            passwrod_input = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.NAME,"password"))
            )
            #Enter the login and password
            login_input.send_keys(login_entry.get())
            passwrod_input.send_keys(password_entry.get())

        except Exception as e:
            print(e)


def check_logged_in():
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-link-name"))
        )
        return True
    except:
        return False 




def load_existing_offers():
    global driver
    driver.get("https://funpay.com/en/lots/612/trade")
    
    # Wait for the page to load (if necessary)
    sleep(3)  # or you can use WebDriverWait if you prefer more control
    
    # Extract page source
    page_source = driver.page_source
    
    # Use BeautifulSoup to parse the page content
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find all the offer links (<a href="https://funpay.com/en/lots/offerEdit?node=612&offer=)
    offer_links = soup.find_all('a', href=True)
    total_offers = len([link for link in offer_links if "https://funpay.com/en/lots/offerEdit?node=612&offer=" in link['href']])
    
    # Find all offers with stock (class tc-amount hidden-xxs that are > 0)
    active_offers = len([offer for offer in soup.find_all(class_='tc-amount hidden-xxs') if int(offer.get_text(strip=True)) > 0])
    
    # Calculate inactive offers
    inactive_offers = total_offers - active_offers
    
    # Print or display the results in your UI
    print(f"Total Offers: {total_offers}, Active: {active_offers}, Inactive: {inactive_offers}")
    
    # You can update a label in the UI to show this information
    accounts_frameX_label.config(text=f"Total Offers: {total_offers}, Active: {active_offers}, Inactive: {inactive_offers}")



def accounts_section_button_click():
    frame4.place_forget()
    accounts_frameX.place(relx=0.5, rely=0.5, anchor=CENTER)

def save_cookies(driver, path='cookies.pkl'):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookies(driver, path='cookies.pkl'):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def successful_login_button():
    global driver

    try:
        #Wait for the main page to load and find element
        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-link-name"))
        )
        driver.get("https://funpay.com/en/")
        save_cookies(driver)
        instructionsframe.place_forget()
        frame3.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        frame3.place_forget()
        frame4.place(relx=0.5, rely=0.5, anchor=CENTER)
        
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
instructionsframe = ttk.Frame(root)

#Frame after login was successful
frame3 = ttk.Frame(root)
login_successful_label = ttk.Label(frame3, text="Login successful!", font=("Arial", 15))
login_successful_label.grid(row=0, column=2, pady=10)

#Frame 4  
frame4 = ttk.Frame(root)
accounts_section_button = ttk.Button(frame4, text="Accounts", command=accounts_section_button_click)
accounts_section_button.grid(row=0, column=2, pady=10)

#Frame 5
accounts_frameX = ttk.Frame(root)
accounts_frameX_label= ttk.Button(accounts_frameX, text="Load Existing Offers", command=load_existing_offers)
accounts_frameX_label.grid(row=0, column=2, pady=10)

#Instructions label
instructions = ttk.Label(instructionsframe, text="Please complete the captcha and log in", font=("Arial", 15))
instructions.grid(row=1, column=2, pady=10)
check_logged_in_button = ttk.Button(instructionsframe, text="Check if logged in", command=successful_login_button)
check_logged_in_button.grid(row=2, column=2, pady=10)

# Login label and formatting
loginLabel = ttk.Label(mainframe, text="Login", font=("Arial", 15))
loginLabel.grid(row=0, column=1, pady=10)

# Login entry space and formatting
login_entry = ttk.Entry(mainframe, exportselection=0, width=30, font=("Arial", 15))
login_entry.grid(row=1, column=1, padx=10)  
login_entry.insert(0, "grandcrabst")  
login_entry.bind("<FocusIn>", clear_default_text) 

#Remember me checkbox
remember_me_var = tkinter.BooleanVar()
remember_me = ttk.Checkbutton(mainframe, text="Remember me", variable=remember_me_var)
remember_me.grid(row=4, column=1, pady=10)


#Saves the checkbox state
def save_remember_me_state(*args):
    with open('remember_me_state.pkl', 'wb') as f:
        pickle.dump(remember_me_var.get(), f)

remember_me_var.trace_add('write', save_remember_me_state)
#Loads the checkbox state
def load_remember_me_state():
    try:
        with open('remember_me_state.pkl', 'rb') as f:
            state = pickle.load(f)
            remember_me_var.set(state)
    except FileNotFoundError:
        remember_me_var.set(False)  # Default state if no file is found

load_remember_me_state()


# Password entry space and formatting
password_entry = ttk.Entry(mainframe, show="*", exportselection=0, width=30, font=("Arial", 15))
password_entry.grid(row=2, column=1, pady=10, padx=10)
password_entry.insert(0, "1234Az789") 
password_entry.bind("<FocusIn>", clear_password_text) 

#Login button
try_login_button = ttk.Button(mainframe, text="Login", command=login_button_click, width=20)
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
