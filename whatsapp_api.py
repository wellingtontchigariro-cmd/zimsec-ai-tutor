import requests

def send_message(to, text, access_token, phone_number_id):
    # Use tokens passed from main.py, not from os.getenv here
    if not access_token or not phone_number_id:
        print("ERROR: Missing ACCESS_TOKEN or PHONE_NUMBER_ID")
        return

    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Sent to {to}: {response.status_code} - {response.text}")
        return response.json()
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
