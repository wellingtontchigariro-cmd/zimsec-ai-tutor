from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()
VERIFY_TOKEN = "zimsec2026"
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/webhook")
def verify(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return int(challenge)
    return "Invalid", 403

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Received:", data) # check Render logs
    
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = message['from']
        text = message['text']['body']
        
        # Reply back
        reply = f"Hi! I'm Zimsec AI Tutor 👋\nYou asked: {text}\n\nI'll help you with Zimsec questions!"
        send_message(from_number, reply)
    except:
        pass
        
    return {"status": "ok"}

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)
