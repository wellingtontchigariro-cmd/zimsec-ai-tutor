from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "zimsec123" # Must match Meta
ACCESS_TOKEN = "PASTE_YOUR_TOKEN_HERE" # Paste full token
PHONE_NUMBER_ID = "1214809328390595"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("POST RECEIVED:", data)
    return 'OK', 200

@app.route('/', methods=['GET'])
def home():
    return "Zimsec AI Tutor is running", 200

# THIS IS THE IMPORTANT PART FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000)) # Use Render's PORT
    app.run(host="0.0.0.0", port=port)
