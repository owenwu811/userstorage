from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create a new Chrome browser instance
driver = webdriver.Chrome()

# Test registration
driver.get('http://localhost:5000/register')
username_input = driver.find_element_by_name('username')
password_input = driver.find_element_by_name('password')
confirm_password_input = driver.find_element_by_name('confirm_password')
register_button = driver.find_element_by_name('register_button')

username_input.send_keys('testuser')
password_input.send_keys('testpassword')
confirm_password_input.send_keys('testpassword')
register_button.click()

# Test login
driver.get('http://localhost:5000/login')
username_input = driver.find_element_by_name('username')
password_input = driver.find_element_by_name('password')
login_button = driver.find_element_by_name('login_button')

username_input.send_keys('testuser')
password_input.send_keys('testpassword')
login_button.click()

# Test logout
logout_button = driver.find_element_by_name('logout_button')
logout_button.click()

# Close the browser
driver.quit()
