import os
import pyotp
from smartapi.smartConnect import SmartConnect  # ✅ Corrected import
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

def get_token():
    totp = pyotp.TOTP(TOTP_SECRET)
    otp = totp.now()

    obj = SmartConnect(api_key=API_KEY)
    data = obj.generateSession(CLIENT_CODE, PASSWORD, otp)
    if data.get("status") != True:
        raise Exception("Login failed:", data)
    return obj

def fetch_ltp(obj, symbol):
    try:
        return obj.get_ltp_data(exchange="NSE", tradingsymbol=symbol, symboltoken="99926000")["data"]["ltp"]
    except Exception as e:
        print("LTP fetch error:", e)
        return None

def fetch_option_chain(obj, symbol, expiry):
    try:
        return obj.get_option_chain(tradingsymbol=symbol, exchange="NFO", expirydate=expiry)["data"]
    except Exception as e:
        print("Option chain error:", e)
        return []

def place_order(obj, symbol, strike, option_type, qty=50, side="BUY"):
    try:
        order = obj.placeOrder(
            variety="NORMAL",
            tradingsymbol=f"{symbol}{strike}{option_type}",
            symboltoken="99926000",
            transactiontype=side,
            exchange="NFO",
            ordertype="MARKET",
            producttype="INTRADAY",
            duration="DAY",
            quantity=qty
        )
        return order
    except Exception as e:
        print("Order error:", e)
        return None
