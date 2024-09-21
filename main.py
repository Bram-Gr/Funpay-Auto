import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pickle
from time import sleep
from bs4 import BeautifulSoup
import csv
import os
import undetected_chromedriver as uc
import requests
import random
import string
import requests
import re

# Selenium setup
cService = webdriver.ChromeService(executable_path="E:\\chromedriver-win64\\chromedriver.exe")
driver = None

# File to store account-email associations
csv_file = "accounts_emails.csv"

# In-memory storage for account-email associations (loaded from CSV)
accounts_to_emails = {}

def get_firstmail_code(email_login_value, email_password_value):
    # Construct the API URL
    url = f"https://api.firstmail.ltd/v1/market/get/message?username={email_login_value}&password={email_password_value}"

    # Define the headers with the API key
    headers = {
        "accept": "application/json",
        "X-API-KEY": "c5816a11-b9eb-4325-91d4-94f3179a4ea3"
    }

    try:
        # Make the request to the Firstmail API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            email_data = response.json()  # Parse the JSON response

            # Check if the email has a message and the subject contains the code
            if email_data.get("has_message"):
                subject = email_data.get("subject", "")

                # Use regex to extract the 6-digit code from the subject
                match = re.search(r'\d{6}', subject)
                if match:
                    return match.group(0)  # Return the code
                else:
                    print("Error: No code found in the subject.")
                    return None
            else:
                print("Error: No message found.")
                return None
        else:
            print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: An exception occurred while making the API request: {e}")
        return None




# Load existing account-email associations from CSV
def load_accounts_from_csv():
    global accounts_to_emails
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                accounts_to_emails[row['account_code']] = {
                    'website': row['website'],
                    'login': row['login'],
                    'password': row['password'],
                    'account_login': row.get('account_login', ''),  # New field with default empty string if missing
                    'current_password': row.get('current_password', '')  # New field with default empty string if missing
                }


# Save account-email associations to CSV
def save_accounts_to_csv():
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ['account_code', 'website', 'login', 'password', 'account_login', 'current_password']  # Updated fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for account_code, email_data in accounts_to_emails.items():
            writer.writerow({
                'account_code': account_code,
                'website': email_data['website'],
                'login': email_data['login'],
                'password': email_data['password'],
                'account_login': email_data.get('account_login', ''),  # New field with default empty string if missing
                'current_password': email_data.get('current_password', '')  # New field with default empty string if missing
            })


# Call this function after associating an email and account info
def associate_email(website, login, password, account_code, account_login, current_password):
    accounts_to_emails[account_code] = {
        'website': website,
        'login': login,
        'password': password,
        'account_login': account_login,  # Storing new account login
        'current_password': current_password  # Storing new current password
    }
    print(f"Associated {login} with account {account_code}")
    save_accounts_to_csv()  # Save to CSV after association


# Show the account information form with pre-filled data if available
def show_email_association_form(account_code, link):
    email_window = Toplevel(root)
    email_window.title(f"{account_code} Account Info")

    # Retrieve existing data for the account if available
    existing_data = accounts_to_emails.get(account_code, {})

    # Email-related fields
    ttk.Label(email_window, text="Email Website:").grid(row=0, column=0, padx=5, pady=5)
    email_website = ttk.Entry(email_window, width=30, font=("Arial", 10))
    email_website.grid(row=0, column=1, padx=5, pady=5)
    email_website.insert(0, existing_data.get('website', ''))  # Pre-fill if available

    ttk.Label(email_window, text="Email Login:").grid(row=1, column=0, padx=5, pady=5)
    email_login = ttk.Entry(email_window, width=30, font=("Arial", 10))
    email_login.grid(row=1, column=1, padx=5, pady=5)
    email_login.insert(0, existing_data.get('login', ''))  # Pre-fill if available

    ttk.Label(email_window, text="Email Password:").grid(row=2, column=0, padx=5, pady=5)
    email_password = ttk.Entry(email_window, show="*", width=30, font=("Arial", 10))
    email_password.grid(row=2, column=1, padx=5, pady=5)
    email_password.insert(0, existing_data.get('password', ''))  # Pre-fill if available

    # New fields for Account Login and Current Password
    ttk.Label(email_window, text="Account Login:").grid(row=3, column=0, padx=5, pady=5)
    account_login = ttk.Entry(email_window, width=30, font=("Arial", 10))
    account_login.grid(row=3, column=1, padx=5, pady=5)
    account_login.insert(0, existing_data.get('account_login', '')) 

    ttk.Label(email_window, text="Current Password:").grid(row=4, column=0, padx=5, pady=5)
    current_password = ttk.Entry(email_window, show="*", width=30, font=("Arial", 10))
    current_password.grid(row=4, column=1, padx=5, pady=5)
    current_password.insert(0, existing_data.get('current_password', '')) 


    # Function that changes account password
    def change_account_password():
        global driver
        driver.get("https://playvalorant.com/en-gb/")
        
        try:
            # Step 1: Click the "PLAY NOW" button
            play_now_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-riotbar-link-id="play-now"]'))
            )
            driver.execute_script("arguments[0].click();", play_now_button)
            print("Clicked PLAY NOW button.")
            
            sleep(2)

            # Step 2: Wait for and click the second "Sign In" button (assuming there are two)
            sign_in_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cta-primary"]'))
            )
            
            if len(sign_in_buttons) >= 2:
                # Click the second button (index 1)
                driver.execute_script("arguments[0].click();", sign_in_buttons[1])
                print("Clicked second SIGN IN button.")
            else:
                print("Could not find both sign-in buttons.")

            # Step 3: Wait for the username input field and fill it with account login
            username_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            driver.execute_script("arguments[0].focus();", username_element)
            username_element.send_keys(account_login.get())  # Replace with actual account login data

            # Step 4: Wait for the password field and fill it with the current password
            password_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            driver.execute_script("arguments[0].focus();", password_element)
            password_element.send_keys(current_password.get())  # Replace with actual password data
            
            # Submit the form or trigger login
            password_element.send_keys(Keys.RETURN)

            # Step 5: Pop up window with instructions for captcha
            riotinstructions = Toplevel(root)
            riotinstructions.title("Instructions")
            ttk.Label(riotinstructions, text="Please complete the captcha manually and then press the button below").grid(row=0, column=0, padx=5, pady=5)
            riotlogin_button = ttk.Button(riotinstructions, text="Captcha completed", command=lambda: continue_change_password(email_login.get(), email_password.get())).grid(row=1, column=1, padx=5, pady=5)

        except TimeoutException:
            print("Element not found within the time limit.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def continue_change_password(email_login_value, email_password_value):
        global driver

        try:
            settings_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="riotbar:account:link-settings"]'))
                )
            driver.execute_script("arguments[0].click();", settings_button)
            print("Clicked Settings button.")
            # Retrieve the login code from the Firstmail API
            sleep(7)
            login_code = get_firstmail_code(email_login_value, email_password_value)
            if login_code:
                print(f"Login code retrieved: {login_code}")
                
                # Simulate typing the code into the input fields
                first_input_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-ktEKTO.sc-jegxcv.ivhuoK.dUizNf.field input'))
                )
                first_input_field.send_keys(login_code)
                print(f"Entered login code: {login_code}")
                submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="btn-mfa-submit"]'))
                )
                driver.execute_script("arguments[0].click();", submit_button)
                print("Clicked submit button.")
                
                #Finds and enters the current password
                current_pass_change_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__currentPassword"]'))
                )
                driver.execute_script("arguments[0].focus();", current_pass_change_element)
                current_pass_change_element.send_keys(current_password.get())
                
                pass_holder = pass_gen(12)
                print(pass_holder)
                #Finds and enters a random password into to "new password" field
                new_pass_element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__newPassword"]'))
                )
                driver.execute_script("arguments[0].focus();",new_pass_element)
                new_pass_element.send_keys(pass_holder)

                #Second new pass field
                confirm_new_pass_element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__confirmNewPassword"]'))
                )
                driver.execute_script("arguments[0].focus();", confirm_new_pass_element)
                confirm_new_pass_element.send_keys(pass_holder)
                
                #Saves pass
                apply_new_pass = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__submit-btn"]'))
                )
                driver.execute_script("arguments[0].click();", apply_new_pass)
                
                current_password.delete(0, END)
                current_password.insert(0, pass_holder)
                associate_email(
                    email_website.get(), email_login.get(), email_password.get(), account_code, account_login.get(), current_password.get())
                sleep(5)

                driver.get(link)
                login_password_form = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "form-control.textarea-lot-secrets"))
                )
                login_password_form.send_keys(f"Login:{account_login.get()} Password:{current_password.get()} Enjoy your games! And please leave a review <3")
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label:has(input[name='active'])"))
                )
                driver.execute_script("arguments[0].click();", checkbox)
                sleep(4)
                save_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-primary.btn-block.js-btn-save"))
                )
                driver.execute_script("arguments[0].click();", save_button)
                sleep(4)
                load_existing_offers()
            else:
                print("Failed to retrieve the login code.")

        except TimeoutException:
            print("Input field not found within the time limit.")
        except Exception as e:
            print(f"An error occurred: {e}")


    ttk.Button(email_window, text="Change account password",command=change_account_password).grid(row=2, column=2, padx=5)

    # Function to toggle password visibility
    def toggle_password_visibility():
        if show_password_var.get():
            email_password.config(show="")
            current_password.config(show="")
        else:
            email_password.config(show="*")
            current_password.config(show="*")

    # Checkbox to show/hide passwords
    show_password_var = BooleanVar()
    show_password_checkbox = ttk.Checkbutton(email_window, text="Show Passwords", variable=show_password_var, command=toggle_password_visibility)
    show_password_checkbox.grid(row=5, column=1, padx=5, pady=5)

    # Associate button to save data
    associate_btn = ttk.Button(email_window, text="Associate", command=lambda: associate_email(
        email_website.get(), email_login.get(), email_password.get(), account_code, account_login.get(), current_password.get()))
    associate_btn.grid(row=6, column=0, columnspan=2, pady=10)

def pass_gen(length=12):
    # Define the character sets for password generation
    letters = string.ascii_letters  # a-z, A-Z
    digits = string.digits          # 0-9
    special_chars = string.punctuation  # Special characters like !, @, #

    # Ensure the password contains at least one character from each category
    all_characters = letters + digits + special_chars
    
    # Generate a random password
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest of the password with random characters from all categories
    password += random.choices(all_characters, k=length - len(password))
    
    # Shuffle the result to prevent predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

# Extract account code from description text (between [ and ])
def extract_account_code(desc_text):
    start = desc_text.find('[') + 1
    end = desc_text.find(']')
    return desc_text[start:end]

# Open the offer in the browser and show email association form
def open_offer_in_browser(link, desc_text):
    account_code = extract_account_code(desc_text)
    print(f"Opening offer with account code: {account_code}")
    driver.get(link)
    show_email_association_form(account_code,link)

# Load existing offers from the website
def load_existing_offers():
    global driver
    driver.get("https://funpay.com/en/lots/612/trade")
    sleep(3)  # Wait for the page to load
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    inactive_offers = []
    
    # Find inactive offers (those with amount = 0)
    for offer in soup.find_all('a', href=True, class_="tc-item"):
        offer_amount = offer.find(class_='tc-amount hidden-xxs').get_text(strip=True)
        if int(offer_amount) == 0:
            desc_text = offer.find(class_="tc-desc-text").get_text(strip=True)[:30]  # Get first 30 characters
            offer_link = offer['href']
            inactive_offers.append((desc_text, offer_link))
    
    # Clear previous content in the frame
    for widget in accounts_frameX.winfo_children():
        widget.destroy()
    
    # Create buttons for each inactive offer
    for desc_text, link in inactive_offers[:30]:  # Show only first 30 offers
        btn = ttk.Button(accounts_frameX, text=desc_text, command=lambda url=link, desc=desc_text: open_offer_in_browser(url, desc))
        btn.pack(pady=2)

# Start Selenium and handle login with default Chrome profile
def login_button_click():
    global driver
    options = uc.ChromeOptions()


    # Initialize the undetected Chrome driver with options
    driver = uc.Chrome(options=options)
    
    driver.get("https://funpay.com/en/")
    
    # Load cookies if available
    load_cookies(driver)
    
    # Try navigating to the site again to check if logged in
    driver.get("https://funpay.com/en/")
    a = check_logged_in()
    
    if a == True:
        mainframe.place_forget()
        frame4.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        driver.get("https://funpay.com/en/account/login")
        try:
            mainframe.place_forget()
            instructionsframe.place(relx=0.5, rely=0.5, anchor=CENTER)
            
            login_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "login"))
            )
            password_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            
            # Input the credentials into the login form
            login_input.send_keys(login_entry.get())
            password_input.send_keys(password_entry.get())
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

# Switch to the accounts section
def accounts_section_button_click():
    frame4.place_forget()
    accounts_frameX.place(relx=0.5, rely=0.5, anchor=CENTER)

# Save cookies to a file
def save_cookies(driver, path='cookies.pkl'):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

# Load cookies from a file
def load_cookies(driver, path='cookies.pkl'):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Login successful handler
def successful_login_button():
    global driver
    try:
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

# Clear default text in login entry
def clear_default_text(event):
    if login_entry.get() == "Username":
        login_entry.delete(0, END)

def clear_password_text(event):
    if password_entry.get() == "23423":
        password_entry.delete(0, END)

root = tkinter.Tk() 
root.title("Funpay Automation") 
root.geometry("600x250")  

# Main frame for the login page
mainframe = ttk.Frame(root)  

# Frame after login was pressed
instructionsframe = ttk.Frame(root)

# Frame after login was successful
frame3 = ttk.Frame(root)
login_successful_label = ttk.Label(frame3, text="Login successful!", font=("Arial", 15))
login_successful_label.grid(row=0, column=2, pady=10)

# Frame 4  
frame4 = ttk.Frame(root)
accounts_section_button = ttk.Button(frame4, text="Accounts", command=accounts_section_button_click)
accounts_section_button.grid(row=0, column=2, pady=10)

# Frame 5
accounts_frameX = ttk.Frame(root)
accounts_frameX_label= ttk.Button(accounts_frameX, text="Load Existing Offers", command=load_existing_offers)
accounts_frameX_label.grid(row=0, column=2, pady=10)

# Instructions label
instructions = ttk.Label(instructionsframe, text="Please complete the captcha manually", font=("Arial", 15))
instructions.grid(row=0, column=2, pady=10)

# Username and password entries
login_entry = ttk.Entry(mainframe)
login_entry.insert(0, "Username")
login_entry.bind("<FocusIn>", clear_default_text)
login_entry.grid(row=1, column=2, padx=5, pady=5)

password_entry = ttk.Entry(mainframe, show="*")
password_entry.insert(0, "23423")
password_entry.bind("<FocusIn>", clear_password_text)
password_entry.grid(row=2, column=2, padx=5, pady=5)

# Login button
login_button = ttk.Button(mainframe, text="Login", command=login_button_click)
login_button.grid(row=3, column=2, pady=10)

sv_ttk.set_theme("dark")
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

load_accounts_from_csv()  # Load accounts from CSV on startup

root.mainloop()
