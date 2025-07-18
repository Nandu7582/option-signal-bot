import pandas as pd
from app.telegram_alerts import send_alert
from app.signal_logic import generate_option_signals, suggest_hedge

def get_dummy_option_chain():
    try:
        df = pd.DataFrame({
            "symbol": ["NIFTY"] * 6,
            "optionType": ["CE", "CE", "PE", "PE", "CE", "PE"],
            "strikePrice": [18200, 18400, 18200, 18000, 18600, 17800],
            "openInterest": [120000, 95000, 110000, 130000, 80000, 125000],
            "impliedVolatility": [22, 18, 25, 21, 19, 23],
            "underlyingValue": [18350] * 6
        })
        return df
    except Exception as e:
        print(f"❌ Failed to create dummy option chain: {e}")
        return pd.DataFrame()

def generate_signals():
    df = get_dummy_option_chain()
    if df.empty or not all(col in df.columns for col in ["symbol", "optionType", "strikePrice", "openInterest"]):
        print("⚠️ Invalid or empty option chain data.")
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
