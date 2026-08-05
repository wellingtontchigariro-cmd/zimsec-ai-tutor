from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === PUT YOUR TOKENS HERE ===
VERIFY_TOKEN = "zimsec123" # Must match what you put in Meta
ACCESS_TOKEN = "EAGSoiz..." # Copy your Permanent Access Token from Meta
PHONE_NUMBER_ID = "1214809328390595" # Copy from Meta "From" number

# 1. VERIFY WEBHOOK - For Meta setup
@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200
    else:
        return "Verification failed", 403

# 2. RECEIVE MESSAGES
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("POST RECEIVED")
    print("DATA:", data)

    try:
        # Get message and sender
        message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        from_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        print(f"Message: {message} from {from_number}")
        
        # Reply back
        reply_text = f"Hey! I got: '{message}'\n\nZimsec AI Tutor is online 🚀"
        send_whatsapp_message(from_number, reply_text)
        
    except Exception as e:
        print("Error:", e)
        
    return 'OK', 200

# 3. FUNCTION TO SEND REPLY
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("Send Status:", r.status_code)

# 4. HEALTH CHECK
@app.route('/', methods=['GET'])
def home():
    return "Zimsec AI Tutor is running", 200
