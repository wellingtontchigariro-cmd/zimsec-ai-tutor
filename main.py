@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("POST RECEIVED")
    print("DATA:", data)

    # Get the message and phone number
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        from_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        print(f"Message: {message} from {from_number}")
        
        # Simple reply - "I got: Food"
        send_whatsapp_message(from_number, f"You said: {message}. Zimsec AI Tutor is online!")
        
    except:
        pass
        
    return 'OK', 200

def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v25.0/1214809328390595/messages"
    headers = {
        "Authorization": "Bearer EAGSoiz...", # Paste your Access Token here
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)
