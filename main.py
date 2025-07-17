import os
import sys
import subprocess
import pkg_resources
import streamlit as st

# 🔧 Force install smartapi-python if missing
try:
    from smartapi.smartConnect import SmartConnect
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "smartapi-python"])
    from smartapi.smartConnect import SmartConnect

# 📦 Show installed packages in sidebar for debugging
st.sidebar.write("📦 Installed packages:")
for dist in pkg_resources.working_set:
    st.sidebar.write(dist.project_name)

# 🔧 Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ✅ Your app logic continues here...
st.title("📊 Option Signal Bot")
st.write("Welcome to your deployed trading dashboard!")
