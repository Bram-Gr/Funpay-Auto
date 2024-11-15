import tkinter
import sv_ttk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
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
import json
import logging
import time

# Selenium setup
cService = webdriver.ChromeService(executable_path="E:\\chromedriver-win64\\chromedriver.exe")
driver = None

# File to store account-email associations
csv_file = "accounts_emails.csv"

# In-memory storage for account-email associations (loaded from CSV)
accounts_to_emails = {}

def check_rank(account_code):
    global driver
    
    tracker_link = accounts_to_emails.get(account_code, {}).get('tracker_link', None)
    
    if not tracker_link:
        print(f"No tracker link found for account code: {account_code}")
        return None
    
    
    driver.get(tracker_link)
    
    try:
        
        rank_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-v-8ed4ebc3][class="value"]'))
        )
        rank = rank_element.text
        print(f"Rank for account {account_code}: {rank}")
    except Exception as e:
        print(f"Error retrieving rank for account {account_code}: {e}")
        return
    
    
    if account_code in accounts_to_emails:
        accounts_to_emails[account_code]['rank'] = rank
        print(f"Updated rank for account code {account_code} to {rank}")
    else:
        print(f"Account code {account_code} not found in the data.")
        return
    
   
    save_accounts_to_csv()
    print(f"Rank saved to CSV for account code {account_code}")

# Function to retrieve the 6-digit code from the email subject
def get_firstmail_code(email_login_value, email_password_value, tries=10, delay=2):
    if tries == 0:
        logging.error("Out of tries.")
        return 0

    
    url = f"https://api.firstmail.ltd/v1/market/get/message?username={email_login_value}&password={email_password_value}"

    
    headers = {
        "accept": "application/json",
        "X-API-KEY": "c5816a11-b9eb-4325-91d4-94f3179a4ea3"
    }

    try:
       
        response = requests.get(url, headers=headers, timeout=10)

        
        if response.status_code == 200:
            try:
                email_data = response.json()  

                
                if email_data.get("has_message"):
                    subject = email_data.get("subject", "")

                    
                    match = re.search(r'\d{6}', subject)
                    if match:
                        return match.group(0)  
                    else:
                        logging.error("No code found in the subject.")
                else:
                    logging.error("No message found.")
            except ValueError:
                logging.error("Error parsing JSON response.")
        else:
            logging.error(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")

    # Retry after delay
    time.sleep(delay)
    return get_firstmail_code(email_login_value, email_password_value, tries - 1, delay * 2)
        

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
                    'account_login': row.get('account_login', ''),
                    'current_password': row.get('current_password', ''),
                    'tracker_link': row.get('tracker_link', ''),
                    'rank': row.get('rank', 'N/A')  
                }

# Save account-email associations to CSV
def save_accounts_to_csv():
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = ['account_code', 'website', 'login', 'password', 'account_login', 'current_password', 'tracker_link', 'rank']  
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for account_code, email_data in accounts_to_emails.items():
            writer.writerow({
                'account_code': account_code,
                'website': email_data['website'],
                'login': email_data['login'],
                'password': email_data['password'],
                'account_login': email_data.get('account_login', ''), 
                'current_password': email_data.get('current_password', ''),
                'tracker_link': email_data.get('tracker_link', ''),
                'rank': email_data.get('rank', 'N/A')
            })


# Call this function after associating an email and account info
def associate_email(website, login, password, account_code, account_login, current_password,tracker_link):
    accounts_to_emails[account_code] = {
        'website': website,
        'login': login,
        'password': password,
        'account_login': account_login,  
        'current_password': current_password,
        'tracker_link': tracker_link,
        'rank': 'N/A'
    }
    print(f"Associated {login} with account {account_code}")
    save_accounts_to_csv()  

# Show the account information form with pre-filled data if available
def show_email_association_form(account_code, link):
    email_window = Toplevel(root)
    email_window.title(f"{account_code} Account Info")

    
    existing_data = accounts_to_emails.get(account_code, {})

    
    ttk.Label(email_window, text="Email Website:").grid(row=0, column=0, padx=5, pady=5)
    email_website = ttk.Entry(email_window, width=30, font=("Arial", 10))
    email_website.grid(row=0, column=1, padx=5, pady=5)
    email_website.insert(0, existing_data.get('website', ''))

    ttk.Label(email_window, text="Email Login:").grid(row=1, column=0, padx=5, pady=5)
    email_login = ttk.Entry(email_window, width=30, font=("Arial", 10))
    email_login.grid(row=1, column=1, padx=5, pady=5)
    email_login.insert(0, existing_data.get('login', '')) 

    ttk.Label(email_window, text="Email Password:").grid(row=2, column=0, padx=5, pady=5)
    email_password = ttk.Entry(email_window, show="*", width=30, font=("Arial", 10))
    email_password.grid(row=2, column=1, padx=5, pady=5)
    email_password.insert(0, existing_data.get('password', ''))  


    ttk.Label(email_window, text="Account Login:").grid(row=3, column=0, padx=5, pady=5)
    account_login = ttk.Entry(email_window, width=30, font=("Arial", 10))
    account_login.grid(row=3, column=1, padx=5, pady=5)
    account_login.insert(0, existing_data.get('account_login', '')) 

    ttk.Label(email_window, text="Current Password:").grid(row=4, column=0, padx=5, pady=5)
    current_password = ttk.Entry(email_window, show="*", width=30, font=("Arial", 10))
    current_password.grid(row=4, column=1, padx=5, pady=5)
    current_password.insert(0, existing_data.get('current_password', '')) 

    ttk.Label(email_window, text=f"Tracker_link").grid(row=5, column=0, padx=5, pady=5)
    tracker_link = ttk.Entry(email_window, width=30, font=("Arial", 10))
    tracker_link.grid(row=5, column=1, padx=5, pady=5)
    tracker_link.insert(0, str(existing_data.get('tracker_link', '')))


    rank = existing_data.get('rank', 'N/A')
    ttk.Label(email_window, text=f"Current Rank: {rank}").grid(row=6, column=0, padx=5, pady=5)
    #ttk.Button(email_window, text="Update Rank", command=lambda: check_rank(account_code)).grid(row=5, column=1, padx=5, pady=5)

    # Function that changes account password
    def change_account_password():
        global driver
        driver.get("https://playvalorant.com/en-gb/")
        
        try:
           
            play_now_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-riotbar-link-id="play-now"]'))
            )
            driver.execute_script("arguments[0].click();", play_now_button)
            print("Clicked PLAY NOW button.")
            
            sleep(0.4)

            
            sign_in_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cta-primary"]'))
            )
            
            if len(sign_in_buttons) >= 2:
                
                driver.execute_script("arguments[0].click();", sign_in_buttons[1])
                print("Clicked second SIGN IN button.")
            else:
                print("Could not find both sign-in buttons.")

            
            username_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            driver.execute_script("arguments[0].focus();", username_element)
            username_element.send_keys(account_login.get())  

            
            password_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            driver.execute_script("arguments[0].focus();", password_element)
            password_element.send_keys(current_password.get())  
            
            
            password_element.send_keys(Keys.RETURN)

            
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
            
            sleep(3)

            login_code = get_firstmail_code(email_login_value, email_password_value)

            
            if login_code:
                print(f"Login code retrieved: {login_code}")
                
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
                
                current_pass_change_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__currentPassword"]'))
                )
                driver.execute_script("arguments[0].focus();", current_pass_change_element)
                current_pass_change_element.send_keys(current_password.get())
                
                pass_holder = pass_gen(12)
                print(pass_holder)
                
                new_pass_element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__newPassword"]'))
                )
                driver.execute_script("arguments[0].focus();",new_pass_element)
                new_pass_element.send_keys(pass_holder)

                confirm_new_pass_element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__confirmNewPassword"]'))
                )
                driver.execute_script("arguments[0].focus();", confirm_new_pass_element)
                confirm_new_pass_element.send_keys(pass_holder)
                
                apply_new_pass = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="password-card__submit-btn"]'))
                )
                driver.execute_script("arguments[0].click();", apply_new_pass)

                current_password.delete(0, END)
                current_password.insert(0, pass_holder)

                associate_email(
                    email_website.get(), email_login.get(), email_password.get(), account_code, account_login.get(), current_password.get(),tracker_link.get())
                sleep(0.1)
                
                driver.delete_all_cookies()
                check_rank(account_code)

                driver.get(link)
                sleep(0.1)

                summary_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, 'fields[summary][en]'))
                )

                current_summary = summary_input.get_attribute('value')
                print(f"Current Summary: {current_summary}")

                account_data = accounts_to_emails.get(account_code, {})
                new_rank = account_data.get('rank', 'N/A')
                print(f"New Rank: {new_rank}")

                updated_summary = re.sub(r"\{.*?\}", f"{{{new_rank}}}", current_summary)
                print(f"Updated Summary: {updated_summary}")

                

                print("Clearing")
                summary_input.clear()

                print("Sending updated summary")
                summary_input.send_keys(updated_summary)

                
                login_password_form = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "form-control.textarea-lot-secrets"))
                )
                login_password_form.clear()

                login_password_form.send_keys(f"Login:{account_login.get()} Password:{current_password.get()} Enjoy your games! And please leave a review <3")
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label:has(input[name='active'])"))
                )
                driver.execute_script("arguments[0].click();", checkbox)
                sleep(0.1)
                save_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-primary.btn-block.js-btn-save"))
                )
                driver.execute_script("arguments[0].click();", save_button)
                sleep(0.1)
                load_existing_offers()
            else:

                driver.delete_all_cookies()
                print("Failed to retrieve the login code.")

        except TimeoutException:
            print("Input field not found within the time limit.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        


    ttk.Button(email_window, text="Renew and publish offer",command=change_account_password).grid(row=2, column=2, padx=5)

    def toggle_password_visibility():
        if show_password_var.get():
            email_password.config(show="")
            current_password.config(show="")
        else:
            email_password.config(show="*")
            current_password.config(show="*")

    show_password_var = BooleanVar()
    show_password_checkbox = ttk.Checkbutton(email_window, text="Show Passwords", variable=show_password_var, command=toggle_password_visibility)
    show_password_checkbox.grid(row=7, column=1, padx=5, pady=5)

    associate_btn = ttk.Button(email_window, text="Associate", command=lambda: associate_email(
        email_website.get(), email_login.get(), email_password.get(), account_code, account_login.get(), current_password.get(),tracker_link.get()))
    associate_btn.grid(row=6, column=3, columnspan=2, pady=10)

# Generate a random password with a specified length    
def pass_gen(length=12):

    letters = string.ascii_letters
    digits = string.digits          
    special_chars = string.punctuation 

    all_characters = letters + digits + special_chars
    
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    password += random.choices(all_characters, k=length - len(password))
    
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
    sleep(0.5)  
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    inactive_offers = []
    active_offers = []

    for offer in soup.find_all('a', href=True, class_="tc-item"):
        offer_amount = offer.find(class_='tc-amount hidden-xxs').get_text(strip=True)
        if int(offer_amount) == 0:
            desc_text = offer.find(class_="tc-desc-text").get_text(strip=True)[:35] 
            offer_link = offer['href']
            inactive_offers.append((desc_text, offer_link))


    for offer in soup.find_all('a', href=True, class_="tc-item"):
        offer_amount = offer.find(class_='tc-amount hidden-xxs').get_text(strip=True)
        if int(offer_amount) == 1:
            desc_text = offer.find(class_="tc-desc-text").get_text(strip=True)[:35] 
            offer_link = offer['href']
            active_offers.append((desc_text, offer_link))
    
    for widget in accounts_frameX.winfo_children():
        widget.destroy()
    
    ttk.Label(accounts_frameX, text="Inactive Offers").grid(column=0, row=0, padx=2, pady=2)
    ttk.Label(accounts_frameX, text="Active Offers").grid(column=1, row=0, padx=2, pady=2)
    
    
    for idx, (desc_text, link) in enumerate(inactive_offers[:30], start=1):  
        btn = ttk.Button(accounts_frameX, text=desc_text, command=lambda url=link, desc=desc_text: open_offer_in_browser(url, desc))
        btn.grid(column=0, row=idx, padx=2, pady=2)
    
    
    for idx, (desc_text, link) in enumerate(active_offers[:30], start=1):  
        btn = ttk.Button(accounts_frameX, text=desc_text, command=lambda url=link, desc=desc_text: open_offer_in_browser(url, desc))
        btn.grid(column=1, row=idx, padx=2, pady=2)

# Start Selenium and handle login process
def login_button_click():
    global driver
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")
    
    driver = uc.Chrome(options=options)
    driver.set_window_size(750, 1000)
    screen_width = root.winfo_screenwidth()
    driver.set_window_position(screen_width - 770, 0)

    if remember_me_var.get() == True:
        
        driver.get("https://funpay.com/en/")
        
        load_cookies(driver)
        
        driver.get("https://funpay.com/en/")
        a = check_logged_in()

        if a == True:

            mainframe.place_forget()
            frame4.place(relx=0.5, rely=0.5, anchor=CENTER)
            save_cookies(driver)
            save_credentials(login_entry.get(), password_entry.get())

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

def save_credentials(login, password):
    credentials = {
        "login": login,
        "password": password
    }
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)

def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            credentials = json.load(file)
            return credentials["login"], credentials["password"]
    except FileNotFoundError:
        return None, None

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

        if remember_me_var.get():
            save_credentials(login_entry.get(), password_entry.get())

        return True
    
    except Exception as e:
        print(e)

def clear_default_text(event):
    if login_entry.get() == "Username":
        login_entry.delete(0, END)

def clear_password_text(event):
    if password_entry.get() == "Password":
        password_entry.delete(0, END)

root = tkinter.Tk() 
root.title("Funpay Automation") 
root.geometry("700x350")  

mainframe = ttk.Frame(root)  

instructionsframe = ttk.Frame(root)

frame3 = ttk.Frame(root)
login_successful_label = ttk.Label(frame3, text="Login successful!", font=("Arial", 15))
login_successful_label.grid(row=0, column=2, pady=10)

frame4 = ttk.Frame(root)
accounts_section_button = ttk.Button(frame4, text="Accounts", command=accounts_section_button_click)
accounts_section_button.grid(row=0, column=2, pady=10)

accounts_frameX = ttk.Frame(root)
accounts_frameX_label= ttk.Button(accounts_frameX, text="Load Existing Offers", command=load_existing_offers)
accounts_frameX_label.grid(row=0, column=2, pady=10)

instructions = ttk.Label(instructionsframe, text="Please complete the captcha manually", font=("Arial", 15))
instructions.grid(row=0, column=0, pady=10)
captcha_completed_button = ttk.Button(instructionsframe, text="Captcha completed", command=successful_login_button)

login,password = load_credentials()


# Username and password entries
login_entry = ttk.Entry(mainframe)
if login:
    login_entry.insert(0, login)
else:
    login_entry.insert(0, "Username")
login_entry.bind("<FocusIn>", clear_default_text)
login_entry.grid(row=1, column=2, padx=5, pady=5)

password_entry = ttk.Entry(mainframe, show="*")
if password:
    password_entry.insert(0, password)
else:
    password_entry.insert(0, "Password")
password_entry.bind("<FocusIn>", clear_password_text)
password_entry.grid(row=2, column=2, padx=5, pady=5)

#Remember me checkbox
remember_me_var = tkinter.BooleanVar()
remember_me = ttk.Checkbutton(mainframe, text="Remember me", variable=remember_me_var)
remember_me.grid(row=4, column=2, pady=10)


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

# Login button
login_button = ttk.Button(mainframe, text="Login", command=login_button_click, width=10)
login_button.grid(row=3, column=2, pady=10)

mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

sv_ttk.set_theme("dark")
button = ttk.Button(root, text="Toggle theme", command=sv_ttk.toggle_theme)
button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
load_accounts_from_csv() 

root.mainloop()
