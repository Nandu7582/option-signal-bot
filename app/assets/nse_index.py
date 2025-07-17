import requests
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
