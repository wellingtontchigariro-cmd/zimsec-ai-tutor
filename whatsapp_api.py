import requests, os

TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
URL = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

async def send_message(to, message):
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    requests.post(URL, headers=headers, json=data)
