import os
import pyotp
from smartapi import SmartConnect

def test_login():
    try:
        obj = SmartConnect(api_key=os.getenv("API_KEY"))
        totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
        data = obj.generateSession(os.getenv("CLIENT_CODE"), os.getenv("PASSWORD"), totp)
        obj.setAccessToken(data["data"]["access_token"])
        print("✅ SmartAPI login successful")
        print("Access Token:", data["data"]["access_token"])
    except Exception as e:
        print("❌ SmartAPI login failed:", e)

test_login()
