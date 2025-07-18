import os
import requests

def send_test_alert():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "✅ Test alert from Nand’s dashboard"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Telegram alert sent")
    else:
        print("❌ Telegram alert failed:", response.text)

send_test_alert()
