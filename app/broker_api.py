import os
import pyotp
from smartapi.smartConnect import SmartConnect
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

# Example token map – replace with live fetch if needed
SYMBOL_TOKEN_MAP = {
    "NIFTY": "99926000",
    "BANKNIFTY": "99926001",
    "RELIANCE": "50032500"
}

def get_token():
    try:
        totp = pyotp.TOTP(TOTP_SECRET)
        otp = totp.now()

        obj = SmartConnect(api_key=API_KEY)
        data = obj.generateSession(CLIENT_CODE, PASSWORD, otp)

        if not data.get("status"):
            raise Exception(f"Login failed: {data}")
        print("✅ Angel One login successful.")
        return obj
    except Exception as e:
        print(f"❌ Token generation error: {e}")
        return None

def get_symbol_token(symbol):
    token = SYMBOL_TOKEN_MAP.get(symbol.upper())
    if not token:
        print(f"⚠️ Symbol token not found for: {symbol}")
    return token

def fetch_ltp(obj, symbol):
    token = get_symbol_token(symbol)
    if not token:
        return None
    try:
        response = obj.get_ltp_data(exchange="NSE", tradingsymbol=symbol, symboltoken=token)
        return response["data"]["ltp"]
    except Exception as e:
        print(f"❌ LTP fetch error for {symbol}: {e}")
        return None

def fetch_option_chain(obj, symbol, expiry):
    try:
        response = obj.get_option_chain(tradingsymbol=symbol, exchange="NFO", expirydate=expiry)
        return response.get("data", [])
    except Exception as e:
        print(f"❌ Option chain fetch error for {symbol}: {e}")
        return []

def place_order(obj, symbol, strike, option_type, qty=50, side="BUY"):
    token = get_symbol_token(symbol)
    if not token:
        return {"status": "error", "message": "Invalid symbol token"}

    tradingsymbol = f"{symbol}{strike}{option_type}"
    try:
        order = obj.placeOrder(
            variety="NORMAL",
            tradingsymbol=tradingsymbol,
            symboltoken=token,
            transactiontype=side,
            exchange="NFO",
            ordertype="MARKET",
            producttype="INTRADAY",
            duration="DAY",
            quantity=qty
        )
        print(f"✅ Order placed: {tradingsymbol}")
        return order
    except Exception as e:
        print(f"❌ Order error for {tradingsymbol}: {e}")
        return {"status": "error", "message": str(e)}
