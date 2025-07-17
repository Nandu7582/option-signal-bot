import requests
import json
import time

def fetch_bitcoin_data():
    fallback_used = False
    try:
        price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr").json()['bitcoin']['inr']
        return price, fallback_used, time.strftime("%H:%M:%S")
    except:
        with open("app/static/btc_fallback.json", "r") as f:
            cached = json.load(f)
        return cached['price'], True, time.strftime("%H:%M:%S")
