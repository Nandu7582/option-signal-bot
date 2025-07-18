import pandas as pd
from app.telegram_alerts import send_alert
from app.signal_logic import generate_option_signals, suggest_hedge
from app.data_feeds import fetch_option_chain  # You must implement this

def generate_signals():
    try:
        df = fetch_option_chain("NIFTY")  # Replace with your live fetch logic
    except Exception as e:
        print(f"❌ Failed to fetch live option chain: {e}")
        return {key: pd.DataFrame() for key in ["stocks", "index", "crypto", "commodities"]}

    required_cols = ["symbol", "optionType", "strikePrice", "openInterest", "impliedVolatility", "underlyingValue"]
    if df.empty or not all(col in df.columns for col in required_cols):
        print("⚠️ Invalid or incomplete option chain data.")
        return {key: pd.DataFrame() for key in ["stocks", "index", "crypto", "commodities"]}

    signals = {key: [] for key in ["stocks", "index", "crypto", "commodities"]}
    strategies = ["Bull Call Spread", "Iron Condor", "Straddle"]

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
                print(f"⚠️ Hedge error for {sig.get('symbol', 'Unknown')}: {e}")
                sig["hedge"] = {"hedge_type": "None"}

            # Add dummy close and date for forecast compatibility
            sig["close"] = df["underlyingValue"].iloc[0]
            sig["date"] = pd.Timestamp.now().normalize()

            signals["index"].append(sig)

            if sig.get("confidence", 0) >= 5:
                try:
                    send_alert(
                        f"🔔 {sig.get('type', 'Option')} signal for {sig.get('symbol', 'Unknown')}:\n"
                        f"Buy: {sig.get('buy_strike', 'N/A')}\nSell: {sig.get('sell_strike', 'N/A')}\n"
                        f"Confidence: {sig.get('confidence')}\n"
                        f"Hedge: {sig['hedge'].get('hedge_type', 'None')}"
                    )
                    print(f"✅ Alert sent for {sig.get('symbol')}")
                except Exception as e:
                    print(f"❌ Telegram alert failed: {e}")

    # Reuse index signals for other tabs
    for key in ["stocks", "crypto", "commodities"]:
        signals[key] = signals["index"].copy()

    # Convert to DataFrames
    for key in signals:
        try:
            signals[key] = pd.DataFrame(signals[key])
            print(f"✅ {key} signals converted to DataFrame.")
        except Exception as e:
            print(f"❌ DataFrame conversion failed for {key}: {e}")
            signals[key] = pd.DataFrame()

    return signals
