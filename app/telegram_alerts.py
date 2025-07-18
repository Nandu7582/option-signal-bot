import os
import requests

def send_alert(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Telegram credentials missing. Skipping alert.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # Optional: use "HTML" or remove for plain text
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram alert sent successfully.")
        else:
            print(f"❌ Telegram alert failed. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Telegram request error: {e}")
