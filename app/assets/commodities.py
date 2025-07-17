import requests
import json
import time

def fetch_gold_data():
    fallback_used = False
    try:
        price = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=INR&apikey=demo").json()['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return float(price), fallback_used, time.strftime("%H:%M:%S")
    except:
        with open("app/static/gold_fallback.json", "r") as f:
            cached = json.load(f)
        return cached['price'], True, time.strftime("%H:%M:%S")
