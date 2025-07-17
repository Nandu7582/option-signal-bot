import requests
import pandas as pd
import json
import os
import time

def safe_nse_fetch(url, retries=3, delay=5, timeout=15):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com"
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout:
            time.sleep(delay)
        except requests.exceptions.RequestException:
            break
    return None

def fetch_index_options(symbol="BANKNIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    data = safe_nse_fetch(url)
    fallback_used = False

    if data:
        try:
            df = pd.DataFrame(data['records']['data'])
            fallback_path = f"app/static/{symbol}_fallback.json"
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            with open(fallback_path, "w") as f:
                json.dump(data, f)
            return df, fallback_used, time.strftime("%H:%M:%S")
        except:
            pass

    fallback_path = f"app/static/{symbol}_fallback.json"
    if os.path.exists(fallback_path):
        with open(fallback_path, "r") as f:
            cached = json.load(f)
        try:
            df = pd.DataFrame(cached['records']['data'])
            fallback_used = True
            return df, fallback_used, time.strftime("%H:%M:%S")
        except:
            pass

    return pd.DataFrame(), True, time.strftime("%H:%M:%S")
