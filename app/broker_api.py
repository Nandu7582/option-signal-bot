# app/broker_api.py

from smartapi import SmartConnect
import pyotp
import time

# 🔐 Replace with your credentials
API_KEY = "LFIyC3E1"
CLIENT_CODE = "N305936"
PASSWORD = "Nandu7582@"
TOTP_SECRET = "12a2f370-be86-4000-b5d7-59eca3e55214"

# ✅ Authenticate
def get_connection():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = obj.generateSession(CLIENT_CODE, PASSWORD, totp)
    return obj

# 📈 Fetch live quote
def fetch_ltp(symbol="BANKNIFTY", exchange="NSE", token="26009"):
    obj = get_connection()
    try:
        data = obj.ltpData(exchange=exchange, tradingsymbol=symbol, symboltoken=token)
        return data['data']['ltp']
    except Exception as e:
        print("LTP fetch failed:", e)
        return None

# 📦 Place order
def place_order(symbol="BANKNIFTY", qty=1, price=None, order_type="MARKET", product_type="INTRADAY"):
    obj = get_connection()
    try:
        order = obj.placeOrder(
            variety="NORMAL",
            tradingsymbol=symbol,
            symboltoken="26009",
            transactiontype="BUY",
            exchange="NSE",
            ordertype=order_type,
            producttype=product_type,
            duration="DAY",
            price=price if price else 0,
            squareoff=0,
            stoploss=0,
            quantity=qty
        )
        return order
    except Exception as e:
        print("Order failed:", e)
        return None
