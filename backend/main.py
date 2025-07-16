from fastapi import FastAPI
from strategy import generate_signals
from send_telegram import send_signal
from option_data import get_banknifty_option_oi
import json

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Running"}

@app.get("/api/signal")
def signal():
    signals = generate_signals()
    for s in signals:
        send_signal(s)
    return signals

@app.get("/api/options")
def option_data():
    return get_banknifty_option_oi()

@app.get("/api/history")
def history():
    with open("signal_history.json", "r") as f:
        return json.load(f)
