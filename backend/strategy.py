import yfinance as yf
import datetime
import json
import os

NIFTY500 = ["SBIN.NS", "RELIANCE.NS", "ICICIBANK.NS", "INFY.NS", "HDFCBANK.NS"]

def calc_macd(close_prices):
    ema12 = close_prices.ewm(span=12).mean()
    ema26 = close_prices.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9).mean()
    return macd_line, signal_line

def generate_signals():
    signals = []
    for symbol in NIFTY500:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="60d")
        if len(hist) < 30:
            continue

        close = hist["Close"]
        ema20 = close.ewm(span=20).mean().iloc[-1]
        ema50 = close.ewm(span=50).mean().iloc[-1]
        last = close.iloc[-1]
        macd, signal = calc_macd(close)
        macd_val, signal_val = macd.iloc[-1], signal.iloc[-1]

        info = stock.info
        pe = info.get("trailingPE", 0)
        eps = info.get("trailingEps", 0)

        if macd_val > signal_val and ema20 > ema50 and pe > 0:
            signal = {
                "symbol": symbol.replace(".NS", ""),
                "entry": round(last, 2),
                "target": round(last * 1.05, 2),
                "sl": round(last * 0.97, 2),
                "reason": f"MACD crossover + EMA20>50 + PE {pe:.1f} + EPS {eps:.1f}",
                "duration": "1–2 weeks",
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            signals.append(signal)

    save_signal_history(signals)
    return signals

def save_signal_history(data):
    file = "signal_history.json"
    if os.path.exists(file):
        with open(file, "r") as f:
            history = json.load(f)
    else:
        history = []

    history += data
    with open(file, "w") as f:
        json.dump(history, f, indent=2)
