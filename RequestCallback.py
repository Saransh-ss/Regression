import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def wait_and_click(driver, xpath, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()

def wait_and_send_keys(driver, xpath, keys, timeout=15):
    field = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    field.send_keys(keys)
    return field

def click_random_request_callback(driver, text, timeout=15):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, f'//span[text()="{text}"]'))
    )
    if elements:
        element = random.choice(elements)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[text()="{text}"]'))
        )
        element.click()
        print("Clicked on a random 'Request Callback' button.")
    else:
        print("No 'Request Callback' buttons found.")

def click_available_date(driver, timeout=15):
    available_dates = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="th-auto-quotation-lead-form"]//div[@aria-disabled="false"]'))
    )
    if available_dates:
        random.choice(available_dates).click()
        print("Clicked on an available date.")
    else:
        print("No available dates found.")

def enter_random_number_and_submit(driver, timeout=15):
    random_number = random.randint(1, 100)
    number_field = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="th-auto-quotation-lead-form"]/div[4]/div[2]/input'))
    )
    number_field.send_keys(str(random_number))
    print(f"Entered random number: {random_number}")
    
    connect_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="lead-form-modal"]/div[2]/div/div/div/button'))
    )
    connect_button.click()
    print("Clicked on 'Connect with an Expert' button.")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.thrillophilia.com/")

try:
    try:
        wait_and_click(driver, '//*[@id="__next"]/div[1]/div/div[2]/div/div[1]/div[2]/div[2]/span')
        print("Clicked on login button.")
        
        wait_and_send_keys(driver, '/html/body/div[3]/div/div/div[2]/div/div[2]/div[2]/form/div[2]/div[1]/input', 'email')
        print("Entered username.")
        
        password_field = wait_and_send_keys(driver, '/html/body/div[3]/div/div/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/input', 'password')
        password_field.send_keys(Keys.RETURN)
        print("Entered password.")
        
        # Wait for the page to load completely after login
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]')))
        
        click_random_request_callback(driver, 'Request Callback')
        
        # Wait for the popup to appear and interact with the form
        mobile_number_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="th-auto-quotation-lead-form"]/div[3]/div[2]/div/input'))
        )
        
        mobile_number = str(random.choice([9, 8, 7, 6])) + ''.join([str(random.randint(0, 9)) for _ in range(9)])
        print(mobile_number)  # For testing purposes

        mobile_number_field.send_keys(mobile_number)
        print("Entered mobile number.")
        time.sleep(10)
        mobile_number_field.send_keys(Keys.TAB)
        print("Tabbed to next field.")
        
        # Wait for the calendar field to be present
        calendar_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="th-auto-quotation-lead-form"]/div[4]/div[1]/div/div'))
        )
        calendar_field.click()
        print("Opened calendar.")
        
        click_available_date(driver)

        done_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "th-custom-calendar-done-btn"))
        )
        done_button.click()
        print("Clicked on 'Done' button.")
        
        # Tab to next field and enter a random number
        calendar_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="th-auto-quotation-lead-form"]/div[4]/div[2]/input'))
        )
        calendar_field.click()
        
        print("Tabbed to next field after date selection.")
        
        enter_random_number_and_submit(driver)

        #Submit Request
        

        print("Waiting for 30 seconds before closing the browser...")
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {e}")
finally:
    print("Closing Browser")
    driver.quit()
