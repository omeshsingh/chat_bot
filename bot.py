from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Load the DialoGPT-medium model and tokenizer tis model is freely availbale on hugging face but i ma sure better models are present

# look  for ways to twek the seetings for tempersture for the model

# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # user_message="the wheather is nice"

# def get_ai_response(user_message, chat_history_ids=None):

#     # Generate a reply from DialoGPT using the latest user message and optional chat history.
#     # Returns the AI's response text and the updated chat history.

#     # Encode the new user message and append the end-of-string token
#     new_user_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')
    
#     # Concatenate with previous conversation if available
#     bot_input_ids = new_user_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    
#     # Generate a response
#     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
#     # Decode the last generated tokens to get the reply
#     ai_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
#     print(ai_response, chat_history_ids)
#     return ai_response, chat_history_ids


# get_ai_response(user_message, chat_history_ids=None)


# ----------------------------<yoho>------------------------------ 

# misteral is used her ein this function lets see if tis is any better
# Load Mistral 7B (or use LLaMA 2 if needed)

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

# from huggingface_hub import login
# login("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")


# Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct", trust_remote_code=True)

# from huggingface_hub import login
# login("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")

# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# ok nothing seems to wok so we will use gemenie 

# --------------------------------<yoho>----------------------------

# import google.generativeai as genai

# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# def chat_with_gemini(prompt):
#     response = genai.generate_text(model="gemini-pro", prompt=prompt)
#     return response.text

# print(chat_with_gemini("Hello, how are you?"))




def get_ai_response(user_message, chat_history=None):
    """
    Generate a reply from Mistral 7B using the user message and optional chat history.
    """
    # Prepare the input
    chat_input = f"User: {user_message}\nAI:"
    input_ids = tokenizer.encode(chat_input, return_tensors="pt")

    # Generate response
    output = model.generate(input_ids, max_length=200, pad_token_id=tokenizer.eos_token_id)
    
    # Decode response
    ai_response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return ai_response



# web driver staartup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com")
input("Scan QR code and press Enter")

# Set the target contact name isme naam add karna hota hai bas
contact = "YOUR CONTACT"

# Search for the contact using an updated XPath (adjust if necessary)
search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
search_box.click()
search_box.send_keys(contact)
time.sleep(2)
search_box.send_keys(Keys.ENTER)

# Wait for the chat to load 
# fixed time can be changed
time.sleep(2)

# Initialize chat history for DialoGPT 
# dont know yeet what tis is
chat_history_ids = None

def get_last_message():
    
    # Fetch the last received message from the active chat.
    # Adjust the XPath as needed based on WhatsApp's current structure.
    
    messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
    if messages:
        return messages[-1].text
    return None

def send_message(message):
    
    # Send a message in the active chat.
    # Adjust the XPath for the message input box if needed.
    
    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)

print("AI WhatsApp bot is running...")

i=0

# this is temporaray setting as we have to make tis thing run for longer wide

while i<10:
    last_message = get_last_message()
    if last_message:
        print("Received:", last_message)
        # Get AI response and update chat history
        ai_response, chat_history_ids = get_ai_response(last_message)
        print("AI Reply:", ai_response)
        send_message(ai_response)
    
    i+=1
    time.sleep(10)  
    # Wait 10 seconds before checking for new messages
    # THIS WHOLE FUNCTION CAN BE MODIFIED TO CAPTURE THE REPLIES


