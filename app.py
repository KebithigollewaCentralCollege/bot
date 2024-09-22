from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# Define the Selenium-based Replika response function
def get_replika_response_from_selenium(user_message):
    # Start a new browser session (headless mode for background operation)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to Replika login page
    driver.get("https://my.replika.com/login")
    time.sleep(3)

    # Automate the login process (Replace with your login credentials)
    username_field = driver.find_element_by_name("email")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys("nicojs000@gmail.com")  # Your Replika email
    password_field.send_keys("Pradeep99.")  # Your Replika password
    password_field.send_keys(Keys.RETURN)

    # Wait for the chat interface to load
    time.sleep(5)

    # Enter user message into the chatbox
    chatbox = driver.find_element_by_css_selector("textarea")
    chatbox.send_keys(user_message)
    chatbox.send_keys(Keys.RETURN)

    # Wait for Replika to respond
    time.sleep(5)

    # Get the last message from Replika (Replika's response)
    messages = driver.find_elements_by_css_selector(".message-text")
    replika_response = messages[-1].text  # Fetch the last response

    driver.quit()  # Close the browser session
    return replika_response

# Flask route to handle incoming WhatsApp messages
@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # Get the incoming message from WhatsApp
    incoming_msg = request.values.get('Body', '').lower()

    # Fetch the response from Replika using the Selenium scraper
    bot_response = get_replika_response_from_selenium(incoming_msg)

    # Respond to the user via WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(bot_response)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
