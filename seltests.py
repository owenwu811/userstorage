from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new Chrome browser instance
driver = webdriver.Chrome()

# Test registration
driver.get('http://localhost:5000/register')

# Using WebDriverWait to ensure the elements are present before interacting with them
username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
confirm_password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'confirm_password')))
register_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Register"]')))

username_input.send_keys('testuser')
password_input.send_keys('testpassword')
confirm_password_input.send_keys('testpassword')
register_button.click()
print("Clicked the Register button")

# Test login
driver.get('http://localhost:5000/login')
print("Navigated to the login page")
username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Login"]')))

username_input.send_keys('testuser')
password_input.send_keys('testpassword')
login_button.click()

# If there's a logout button or any other test scenarios, add them here

# Close the browser
driver.quit()

