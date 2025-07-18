import os
from smartapi import SmartConnect
import pyotp

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

def create_session():
    obj = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = obj.generateSession(CLIENT_CODE, PASSWORD, totp)
    if data['status']:
        print("✅ SmartAPI login successful")
        return obj
    else:
        print("❌ SmartAPI login failed:", data['message'])
        return None
