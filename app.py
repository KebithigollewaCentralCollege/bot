from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
sid='TWILIO_ACCOUNT_SID'
authToken='TWILIO_AUTH_TOKEN'

app = Flask(__name__)

# Replace these with your Replika login credentials
REPLIKA_EMAIL = "nicojs000@gmail.com"
REPLIKA_PASSWORD = "Pradeep99."

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()

    # Call the function to get Replika's response
    bot_response = get_replika_response(incoming_msg)

    # Send response back to WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(bot_response)
    return str(resp)

message=client.message.create(to='whatsapp:+94743481092',
                              from_='whatsapp:+14155238886',
                                body='Test')

def get_replika_response(user_message):
    # Set up Selenium for headless browser automation
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Navigate to Replika login page
    driver.get("https://my.replika.com/login")
    time.sleep(3)

    # Automate login process
    username_field = driver.find_element_by_name("email")
    password_field = driver.find_element_by_name("password")

    username_field.send_keys(REPLIKA_EMAIL)
    password_field.send_keys(REPLIKA_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for the chat interface to load

    # Send the user's message to Replika's chatbox
    chatbox = driver.find_element_by_css_selector("textarea")
    chatbox.send_keys(user_message)
    chatbox.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for Replika to respond

    # Get Replika's response
    messages = driver.find_elements_by_css_selector(".message-text")
    replika_response = messages[-1].text  # Get the last message (Replika's response)

    driver.quit()  # Close the browser session
    return replika_response

if __name__ == '__main__':
    app.run(debug=True)
