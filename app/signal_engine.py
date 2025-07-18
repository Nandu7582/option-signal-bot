import pandas as pd
from app.telegram_alerts import send_alert
from app.signal_logic import generate_option_signals, suggest_hedge
from app.visualizer import strategy_summary
from app.data_feeds import fetch_option_chain  # You must implement this

def format_signal_card(signal):
    return f"""
📌 SIGNAL – {signal.get('symbol', 'Unknown')} {signal.get('expiry', 'Next')} Expiry 🟢 BUY {signal.get('buy_strike', 'N/A')} CE @ ₹{signal.get('entry_price', 'N/A')}
🎯 Target: ₹{signal.get('target', 'N/A')} | 🛑 SL: ₹{signal.get('stop_loss', 'N/A')}
📈 Confidence: {signal.get('confidence', 0)}% ✅ {"High" if signal.get('confidence', 0) >= 70 else "Moderate"}
📚 Strategy: {signal.get('type', 'Custom')}
🧮 Greeks: Delta {signal.get('delta', '0.55')} | Gamma {signal.get('gamma', '0.09')}
🧠 Signal Logic: {signal.get('logic', 'Technical + OI')}
💰 Hedge Idea: {signal.get('hedge', {}).get('hedge_type', 'None')} {signal.get('hedge', {}).get('strike', '')}
📊 Max Profit: ₹{signal.get('max_profit', 'N/A')} | Max Loss: ₹{signal.get('max_loss', 'N/A')}
📷 Chart: [Attached]
"""

def generate_signals():
    try:
        df = fetch_option_chain("BANKNIFTY")
    except Exception as e:
        print(f"❌ Failed to fetch live option chain: {e}")
        return {key: pd.DataFrame() for key in ["stocks", "index", "crypto", "commodities"]}

    required_cols = ["symbol", "optionType", "strikePrice", "openInterest", "impliedVolatility", "underlyingValue"]
    if df.empty or not all(col in df.columns for col in required_cols):
        print("⚠️ Invalid or incomplete option chain data.")
        return {key: pd.DataFrame() for key in ["stocks", "index", "crypto", "commodities"]}

    signals = {key: [] for key in ["stocks", "index", "crypto", "commodities"]}
    strategies = ["Bull Call Spread", "Iron Condor", "Straddle", "Covered Call", "Protective Put"]

    for strategy in strategies:
        print(f"🔍 Processing strategy: {strategy}")
        try:
            option_signals = generate_option_signals(df, strategy)
        except Exception as e:
            print(f"❌ Error in generate_option_signals for {strategy}: {e}")
            continue

        for sig in option_signals:
            try:
                sig["hedge"] = suggest_hedge(sig)
            except Exception as e:
                sig["hedge"] = {"hedge_type": "None"}

            sig.update({
                "entry_price": 142,
                "target": 190,
                "stop_loss": 118,
                "delta": 0.55,
                "gamma": 0.09,
                "expiry": "18 JULY",
                "close": df["underlyingValue"].iloc[0],
                "date": pd.Timestamp.now().normalize()
            })

            strikes = [sig.get("buy_strike"), sig.get("sell_strike")] if "sell_strike" in sig else [sig.get("strike")]
            summary = strategy_summary(sig["type"], strikes)
            sig["max_profit"] = summary.get("Max Profit", "N/A")
            sig["max_loss"] = summary.get("Max Loss", "N/A")

            signals["index"].append(sig)

            if sig.get("confidence", 0) >= 70:
                try:
                    card = format_signal_card(sig)
                    send_alert(card)
                    print(f"✅ Alert sent for {sig.get('symbol')}")
                except Exception as e:
                    print(f"❌ Telegram alert failed: {e}")

    for key in ["stocks", "crypto", "commodities"]:
        signals[key] = signals["index"].copy()

    for key in signals:
        try:
            signals[key] = pd.DataFrame(signals[key])
        except Exception as e:
            signals[key] = pd.DataFrame()
    
    return signals
