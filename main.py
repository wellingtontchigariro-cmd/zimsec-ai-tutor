
import os
import logging
from flask import Flask, request
from handlers import handle_message

# Configure logging for Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Read configuration from Render environment variables
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "zimsec123")
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")


# Home page: confirms that the application is running
@app.route("/", methods=["GET"])
def home():
    return "ZIMSEC AI Tutor is running!", 200


# Health check: used by Render to check the service
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


# WhatsApp webhook verification for Meta
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified successfully")
        return challenge or "", 200

    logger.warning("WhatsApp webhook verification failed")
    return "Verification failed", 403


# Receive incoming WhatsApp messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        logger.warning("Webhook received an invalid JSON payload")
        return "Invalid JSON", 400

    try:
        handle_message(data, ACCESS_TOKEN, PHONE_NUMBER_ID)
        return "OK", 200

    except Exception:
        logger.exception("Error processing incoming WhatsApp webhook")
        return "Internal server error", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

