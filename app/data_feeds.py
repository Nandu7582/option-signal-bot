import pandas as pd
import os
import pyotp
from smartapi import SmartConnect

def fetch_option_chain(symbol="BANKNIFTY"):
    try:
        obj = SmartConnect(api_key=os.getenv("API_KEY"))
        totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
        data = obj.generateSession(os.getenv("CLIENT_CODE"), os.getenv("PASSWORD"), totp)
        obj.setAccessToken(data["data"]["access_token"])

        # Replace with actual SmartAPI option chain endpoint
        # This is a placeholder structure
        option_data = obj.getOptionChain(symbol=symbol)

        # Parse into DataFrame (you’ll need to adapt this based on actual response)
        df = pd.DataFrame(option_data["data"])
        df["symbol"] = symbol
        df["underlyingValue"] = df["underlyingValue"].iloc[0]
        return df

    except Exception as e:
        print(f"❌ SmartAPI error: {e}")
        return pd.DataFrame()
