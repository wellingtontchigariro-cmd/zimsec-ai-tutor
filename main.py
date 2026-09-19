import os
from flask import Flask, request
# import your other files
from whatsapp_api import send_message
from ai_logic import get_ai_response
from handlers import handle_message

app = Flask(__name__)

# === TOKENS FROM RENDER ENVIRONMENT ===
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "zimsec123")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route('/')
def home():
    return "ZIMSEC AI Tutor is running!", 200

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
    try:
        # your existing logic to handle WhatsApp messages
        handle_message(data, ACCESS_TOKEN, PHONE_NUMBER_ID)
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
