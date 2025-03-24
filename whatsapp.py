from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Open WhatsApp Web
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")
input("Scan QR code and press Enter")

contact = "yoUR CONTACT"
message = "Hello, this is an automated message!"

# Find the search box
search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
search_box.click()
search_box.send_keys(contact)
time.sleep(2)  # Wait for search results to appear
search_box.send_keys(Keys.ENTER)

# Wait for the chat to load
time.sleep(2)

# Find the message input box
message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
message_box.click()
message_box.send_keys(message)
message_box.send_keys(Keys.ENTER)

print("Message sent!")
time.sleep(2)
driver.quit()
