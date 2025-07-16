from datetime import datetime

def generate_signal():
    # Example test logic — replace with real indicators later
    today = datetime.now().strftime("%d %b %Y")
    signal = f"""📌 SIGNAL – BANK NIFTY {today} Expiry 🟢 BUY 49,000 CE @ ₹142
🎯 Target: ₹190 | 🛑 SL: ₹118
📈 Confidence: 88% ✅ High
📚 Strategy: Bull Call Spread
🧮 Greeks: Delta 0.55 | Gamma 0.09
🧠 Signal Logic: MACD Crossover + RSI > 50 + Long OI
💰 Hedge Idea: Sell 49,300 CE
📊 Max Profit: ₹3,200 | Max Loss: ₹1,100"""

    # Save signal to history
    try:
        import json
        with open("signal_history.json", "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append({"date": today, "signal": signal})
    with open("signal_history.json", "w") as f:
        json.dump(history[-20:], f, indent=2)  # keep last 20

    return signal

