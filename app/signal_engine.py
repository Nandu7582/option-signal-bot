import pandas as pd
from app.telegram_alerts import send_alert

from app.signal_logic import generate_option_signals, suggest_hedge

# Dummy option chain data for testing
def get_dummy_option_chain():
    return pd.DataFrame({
        "symbol": ["NIFTY"] * 6,
        "optionType": ["CE", "CE", "PE", "PE", "CE", "PE"],
        "strikePrice": [18200, 18400, 18200, 18000, 18600, 17800],
        "openInterest": [120000, 95000, 110000, 130000, 80000, 125000],
        "impliedVolatility": [22, 18, 25, 21, 19, 23],
        "underlyingValue": [18350] * 6
    })

def generate_signals():
    df = get_dummy_option_chain()

    signals = {
        "stocks": [],
        "index": [],
        "crypto": [],
        "commodities": []
    }

    for strategy in ["Bull Call Spread", "Iron Condor", "Straddle"]:
        option_signals = generate_option_signals(df, strategy)
        for sig in option_signals:
            sig["hedge"] = suggest_hedge(sig)
            signals["index"].append(sig)

            # Trigger Telegram alert for high-confidence signals
            if sig["confidence"] >= 5:
                send_alert(f"🔔 {sig['type']} signal for {sig['symbol']}:\nBuy: {sig.get('buy_strike')}\nSell: {sig.get('sell_strike')}\nConfidence: {sig['confidence']}\nHedge: {sig['hedge']['hedge_type']}")

    # For now, reuse index signals for all tabs
    signals["stocks"] = signals["index"]
    signals["crypto"] = signals["index"]
    signals["commodities"] = signals["index"]

    # Convert to DataFrames for Dash
    for key in signals:
        signals[key] = pd.DataFrame(signals[key])

    return signals
