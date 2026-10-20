
import requests


def send_message(to, text, access_token, phone_number_id):
    if not access_token or not phone_number_id:
        raise RuntimeError(
            "Missing WhatsApp access token or phone number ID"
        )

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=20,
    )

    print(
        f"WhatsApp send status: {response.status_code}"
    )
    print(f"WhatsApp send response: {response.text}")

    response.raise_for_status()
    return response.json()

