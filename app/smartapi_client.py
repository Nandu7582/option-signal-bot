import os
from smartapi import SmartConnect
import pyotp

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

def create_session():
    try:
        obj = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = obj.generateSession(CLIENT_CODE, PASSWORD, totp)

        if data['status']:
            print("✅ SmartAPI login successful")

            # Extract and set access token
            access_token = data['data']['access_token']
            obj.setAccessToken(access_token)

            # Optional: print token info for debugging
            print("Access Token:", access_token)

            return obj  # ✅ Fully initialized session object
        else:
            print("❌ SmartAPI login failed:", data['message'])
            return None

    except Exception as e:
        print("❌ Exception during SmartAPI login:", str(e))
        return None
