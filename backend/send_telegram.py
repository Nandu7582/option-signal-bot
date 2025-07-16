import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(data):
    msg = (
        f"📌 BUY: {data['symbol']} @ ₹{data['entry']}\n"
        f"🎯 Target: ₹{data['target']} | 🛑 SL: ₹{data['sl']}\n"
        f"📅 Duration: {data['duration']}\n"
        f"🧠 Reason: {data['reason']}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
