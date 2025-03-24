import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR GEMENI TOKEN")

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")  
    response = model.generate_content(prompt)
    return response.text  

# Start Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Scan QR code and press Enter...")

# Set the target contact name
contact = "YOUR CONTANCT"

# Search for the contact
search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
search_box.click()
search_box.send_keys(contact)
time.sleep(2)
search_box.send_keys(Keys.ENTER)

# Wait for chat to load
time.sleep(3)

def get_last_message():
    """Fetches the last received message"""
    messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
    return messages[-1].text if messages else None

def send_message(message):
    """Sends a message in the active chat"""
    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)

print("✅ AI WhatsApp Bot is Running...")

# Run chatbot loop (set to infinite loop for continuous running)
while True:
    last_message = get_last_message()
    if last_message:
        print("📩 Received:", last_message)
        ai_response = chat_with_gemini(last_message)
        print("🤖 AI Reply:", ai_response)
        send_message(ai_response)
    
    time.sleep(30)  # Check for new messages 
