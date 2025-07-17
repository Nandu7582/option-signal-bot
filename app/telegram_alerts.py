import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(signal):
    if not BOT_TOKEN or not CHAT_ID:
        return

    msg = f"📢 *{signal['type']}*\nSymbol: `{signal['symbol']}`\nConfidence: `{signal['confidence']}`\nLogic: {signal['logic']}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram alert failed:", e)
