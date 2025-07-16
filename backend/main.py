from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strategy
import option_data
import json

app = FastAPI()

# CORS config (allows frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ Your trading bot is running."}

@app.get("/signal")
def get_signal():
    signal_text = strategy.generate_signal()
    return {"signal": signal_text}

@app.get("/options")
def get_options():
    return option_data.fetch_banknifty_options()

@app.get("/history")
def get_history():
    try:
        with open("signal_history.json", "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"error": str(e)}
