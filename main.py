import os
import sys
import subprocess
import streamlit as st

# 🔧 Force install smartapi-python at runtime
try:
    from smartapi.smartConnect import SmartConnect
except ModuleNotFoundError:
    st.warning("📦 Installing smartapi-python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "smartapi-python"])
    from smartapi.smartConnect import SmartConnect

# ✅ Load environment variables
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

# 🔐 Authenticate with SmartAPI
def get_token():
    import pyotp
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
st.success("✅ SmartAPI module loaded successfully!")

if st.button("🔐 Connect to SmartAPI"):
    obj = get_token()
    if obj:
        st.success("✅ Logged in successfully")
    else:
        st.error("❌ Login failed")
