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
            print(f"⏳ Timeout on attempt {attempt+1}. Retrying in {delay}s...")
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            break
    print("⚠️ All retries failed.")
    return None

def fetch_index_options(symbol="BANKNIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    data = safe_nse_fetch(url)

    if data:
        try:
            df = pd.DataFrame(data['records']['data'])

            # Save fallback cache
            fallback_path = f"app/static/{symbol}_fallback.json"
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            with open(fallback_path, "w") as f:
                json.dump(data, f)

            return df
        except Exception as e:
            print(f"⚠️ Error parsing NSE data: {e}")
            return pd.DataFrame()
    else:
        # Load fallback cache
        fallback_path = f"app/static/{symbol}_fallback.json"
        if os.path.exists(fallback_path):
            print(f"🔁 Using fallback data for {symbol}")
            with open(fallback_path, "r") as f:
                cached = json.load(f)
            try:
                return pd.DataFrame(cached['records']['data'])
            except Exception as e:
                print(f"⚠️ Error loading fallback: {e}")
                return pd.DataFrame()
        else:
            print(f"⚠️ No fallback available for {symbol}")
            return pd.DataFrame()
