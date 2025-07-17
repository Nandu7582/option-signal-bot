import os
import streamlit as st
from dotenv import load_dotenv
import pyotp
from app.smartapi_client import SmartConnect  # ✅ Local wrapper

# 🔧 Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

# 🔐 Authenticate with SmartAPI
def get_token():
    totp = pyotp.TOTP(TOTP_SECRET)
    otp = totp.now()

    obj = SmartConnect(api_key=API_KEY)
    data = obj.generateSession(CLIENT_CODE, PASSWORD, otp)
    if data.get("status") != True:
        st.error("❌ Login failed")
        return None
    return obj

# 📊 Streamlit UI
st.set_page_config(page_title="Option Signal Bot", layout="centered")
st.title("📊 Option Signal Bot")
st.write("Welcome to your deployed trading dashboard!")

if st.button("🔐 Connect to SmartAPI"):
    obj = get_token()
    if obj:
        st.success("✅ Logged in successfully")
    else:
        st.error("❌ Login failed")
