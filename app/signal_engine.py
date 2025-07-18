import pandas as pd
from app.telegram_alerts import send_alert
from app.signal_logic import generate_option_signals, suggest_hedge

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

    # Initialize signal containers
    signals = {
        "stocks": [],
        "index": [],
        "crypto": [],
        "commodities": []
    }

    strategies = ["Bull Call Spread", "Iron Condor", "Straddle"]

    for strategy in strategies:
        try:
            option_signals = generate_option_signals(df, strategy)
        except Exception as e:
            print(f"⚠️ Error generating signals for {strategy}: {e}")
            continue

        for sig in option_signals:
            try:
                hedge = suggest_hedge(sig)
                sig["hedge"] = hedge
            except Exception as e:
                print(f"⚠️ Error suggesting hedge for {sig.get('symbol')}: {e}")
                sig["hedge"] = {"hedge_type": "None"}

            signals["index"].append(sig)

            # Trigger Telegram alert for high-confidence signals
            if sig.get("confidence", 0) >= 5:
                try:
                    send_alert(
                        f"🔔 {sig.get('type', 'Option')} signal for {sig.get('symbol')}:\n"
                        f"Buy: {sig.get('buy_strike', 'N/A')}\n"
                        f"Sell: {sig.get('sell_strike', 'N/A')}\n"
                        f"Confidence: {sig.get('confidence')}\n"
                        f"Hedge: {sig['hedge'].get('hedge_type', 'None')}"
                    )
                except Exception as e:
                    print(f"⚠️ Telegram alert failed: {e}")

    # Reuse index signals for other tabs
    for key in ["stocks", "crypto", "commodities"]:
        signals[key] = signals["index"].copy()

    # Convert lists to DataFrames
    for key in signals:
        try:
            signals[key] = pd.DataFrame(signals[key])
        except Exception as e:
            print(f"⚠️ Error converting {key} signals to DataFrame: {e}")
            signals[key] = pd.DataFrame()

    return signals
