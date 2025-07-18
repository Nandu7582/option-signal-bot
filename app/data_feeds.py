import pandas as pd
import os
import pyotp
from smartapi import SmartConnect
from app.nse_scraper import fetch_nse_option_chain
import requests

def smartapi_login():
    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    data = obj.generateSession(os.getenv("CLIENT_CODE"), os.getenv("PASSWORD"), totp)
    obj.setAccessToken(data["data"]["access_token"])
    return obj

def enrich_with_ltp(df, symbol):
    obj = smartapi_login()
    enriched = []
    for _, row in df.iterrows():
        try:
            expiry_fmt = pd.to_datetime(row["expiry"]).strftime("%d%b").upper()
            tradingsymbol = f"{symbol}{expiry_fmt}{int(row['strikePrice'])}{row['optionType']}"
            scrip = obj.searchScrip(tradingsymbol)
            token = scrip["data"][0]["token"]
            quote = obj.ltpData(exchange="NFO", tradingsymbol=tradingsymbol, symboltoken=token)
            ltp = float(quote["data"]["ltp"])
            enriched.append({**row, "tradingsymbol": tradingsymbol, "ltp": ltp})
        except Exception as e:
            print(f"⚠️ Skipped {row['strikePrice']} {row['optionType']}: {e}")
    return pd.DataFrame(enriched)

def fetch_crypto_price(symbol="ETHUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url).json()
        return float(response["price"])
    except Exception as e:
        print(f"❌ Crypto price fetch failed: {e}")
        return 0

def fetch_gold_price():
    try:
        url = "https://www.mcxlive.org/gold-rate-india"
        # You can replace this with a proper API or scrape if needed
        return 60200  # Placeholder
    except Exception as e:
        print(f"❌ Gold price fetch failed: {e}")
        return 0

def fetch_option_chain(symbol="BANKNIFTY"):
    try:
        if symbol in ["BANKNIFTY", "NIFTY", "RELIANCE"]:
            df = fetch_nse_option_chain(symbol)
            if df.empty:
                print("⚠️ NSE data unavailable")
                return pd.DataFrame()
            return enrich_with_ltp(df, symbol)

        elif symbol == "ETHUSDT":
            price = fetch_crypto_price(symbol)
            return pd.DataFrame({
                "symbol": [symbol],
                "optionType": ["CE", "PE"],
                "strikePrice": [int(price), int(price)],
                "openInterest": [5000, 4800],
                "impliedVolatility": [60, 65],
                "underlyingValue": [price, price],
                "expiry": ["NA", "NA"],
                "tradingsymbol": [f"{symbol}CE", f"{symbol}PE"],
                "ltp": [320, 280]
            })

        elif symbol == "GOLD":
            price = fetch_gold_price()
            return pd.DataFrame({
                "symbol": ["GOLD"],
                "optionType": ["CE", "PE"],
                "strikePrice": [60000, 60000],
                "openInterest": [10000, 9500],
                "impliedVolatility": [22, 24],
                "underlyingValue": [price, price],
                "expiry": ["NA", "NA"],
                "tradingsymbol": ["GOLD60000CE", "GOLD60000PE"],
                "ltp": [180, 160]
            })

        else:
            print(f"⚠️ Unsupported symbol: {symbol}")
            return pd.DataFrame()

    except Exception as e:
        print(f"❌ fetch_option_chain error: {e}")
        return pd.DataFrame()
