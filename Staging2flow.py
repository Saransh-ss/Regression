from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://az-staging-2-partners.thrillo.dev/admin/login")

wait = WebDriverWait(driver, 15) 

def wait_and_click(xpath, error_msg, timeout=15):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        print(f"Clicked element: {xpath}")
    except Exception as e:
        print(f"{error_msg}: {e}")
        driver.quit()
        exit()


wait_and_click('//*[@title="Sign in with Google Button"]', "Login failed or could not confirm login")


try:
    main_window = driver.current_window_handle
    WebDriverWait(driver, 15).until(EC.new_window_is_opened)
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            print("Switched to Google login window.")
            break
except Exception as e:
    print("Failed to switch to Google login window:", e)
    driver.quit()
    exit()


try:
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    email_field.send_keys('saranshs@thrillophilia.com')
    email_field.send_keys(Keys.RETURN)
    print("Entered email ID.")
except Exception as e:
    print("Failed to enter email ID:", e)
    driver.quit()
    exit()


try:
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'Passwd')))
    password_field.send_keys('Saransh@11715')
    password_field.send_keys(Keys.RETURN)
    print("Entered password.")
except Exception as e:
    print("Failed to enter password:", e)
    driver.quit()
    exit()

time.sleep(5) 


try:
    driver.switch_to.window(main_window)
    print("Switched back to main window.")
except Exception as e:
    print("Failed to switch back to main window:", e)
    driver.quit()
    exit()

wait_and_click('//*[@id="admin-app"]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div/div', "Failed to click on the desired element")
wait_and_click('//*[@id="admin-app"]/div[2]/div/aside/div/ul/li[2]/div/span[2]', "Failed to click on quotations element")
wait_and_click('/html/body/div[1]/div[2]/div/aside/div/ul/li[2]/ul/li[1]', "Failed to click on packages")
wait_and_click('//*[@id="main-layout-content"]/div[3]/div[4]/div[1]/div[9]/div/p', "Failed to click on the quotation active element")


print("Waiting for 30 seconds before closing the browser...")
time.sleep(30)
driver.quit()
