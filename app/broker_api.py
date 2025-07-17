import os
import time
import pyotp
import pandas as pd
from dotenv import load_dotenv
from smartapi import SmartConnect

load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

def get_connection():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    obj.generateSession(CLIENT_CODE, PASSWORD, totp)
    return obj

def fetch_ltp(symbol="BANKNIFTY", exchange="NSE", token="26009"):
    obj = get_connection()
    try:
        data = obj.ltpData(exchange=exchange, tradingsymbol=symbol, symboltoken=token)
        return data['data']['ltp']
    except Exception as e:
        print("LTP fetch failed:", e)
        return None

def fetch_option_chain(symbol="BANKNIFTY"):
    obj = get_connection()
    try:
        data = obj.getOptionChain(symbol=symbol)
        df = pd.DataFrame(data['data'])
        return df, False, time.strftime("%H:%M:%S")
    except Exception as e:
        print(f"Option chain fetch failed: {e}")
        return pd.DataFrame(), True, time.strftime("%H:%M:%S")

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
