import pandas as pd
import os
import pyotp
from smartapi import SmartConnect

def fetch_index_options(symbol="BANKNIFTY", expiry="2024-07-18", strike_range=500):
    try:
        # 🔐 Authenticate
        obj = SmartConnect(api_key=os.getenv("API_KEY"))
        totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
        data = obj.generateSession(os.getenv("CLIENT_CODE"), os.getenv("PASSWORD"), totp)
        obj.setAccessToken(data["data"]["access_token"])
        print("✅ SmartAPI login successful")

        # 📦 Get LTP for spot price
        spot_data = obj.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken="999920000")
        spot_price = float(spot_data["data"]["ltp"])
        print(f"📈 Spot price for {symbol}: {spot_price}")

        # 🧠 Generate strike range
        strikes = [int(spot_price + i) for i in range(-strike_range, strike_range + 100, 100)]

        # 📊 Fetch option contracts
        contracts = []
        for strike in strikes:
            for opt_type in ["CE", "PE"]:
                tradingsymbol = f"{symbol}{expiry.replace('-', '')}{strike}{opt_type}"
                try:
                    quote = obj.ltpData(exchange="NFO", tradingsymbol=tradingsymbol, symboltoken="999920000")
                    contracts.append({
                        "symbol": symbol,
                        "optionType": opt_type,
                        "strikePrice": strike,
                        "openInterest": 100000 + strike % 1000,  # Dummy OI
                        "impliedVolatility": 20 + (strike % 5),  # Dummy IV
                        "underlyingValue": spot_price,
                        "tradingsymbol": tradingsymbol
                    })
                except Exception as e:
                    print(f"⚠️ Skipped {tradingsymbol}: {e}")

        df = pd.DataFrame(contracts)
        print(f"✅ Fetched {len(df)} option contracts")
        return df

    except Exception as e:
        print(f"❌ SmartAPI error: {e}")
        return pd.DataFrame()
