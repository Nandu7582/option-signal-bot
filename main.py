import streamlit as st
from app.assets.nse_index import fetch_index_options
from app.assets.nse_stocks import fetch_stock_data
from app.assets.crypto import fetch_bitcoin_data
from app.assets.commodities import fetch_gold_data
from app.indicators import add_indicators
from app.signal_engine import generate_signal
from app.dashboard import show_dashboard
from app.telegram_alerts import send_telegram_message
from app.pl_plotter import plot_pl

# 🔧 Streamlit Setup
st.set_page_config(page_title="Option Signal Bot", layout="wide")
st.title("📊 Option Signal Bot")
st.markdown("Real-time multi-asset signals with fallback protection.")

signals = []

# 🏦 Bank Nifty
try:
    df_bn = fetch_index_options("BANKNIFTY")
    if not df_bn.empty:
        df_bn = add_indicators(df_bn)
        signals += generate_signal("BANKNIFTY", df_bn, expiry="18JUL2024")
    else:
        st.warning("⚠️ Bank Nifty data unavailable. Skipping signal.")
except Exception as e:
    st.error(f"Bank Nifty fetch failed: {e}")

# 🏦 Nifty
try:
    df_nf = fetch_index_options("NIFTY")
    if not df_nf.empty:
        df_nf = add_indicators(df_nf)
        signals += generate_signal("NIFTY", df_nf, expiry="18JUL2024")
    else:
        st.warning("⚠️ Nifty data unavailable. Skipping signal.")
except Exception as e:
    st.error(f"Nifty fetch failed: {e}")

# 📈 Nifty 500 Stocks
for stock in ["RELIANCE", "TCS", "INFY"]:
    try:
        df_stock = fetch_stock_data(stock)
        if not df_stock.empty:
            df_stock = add_indicators(df_stock)
            signals += generate_signal("STOCK", df_stock)
        else:
            st.warning(f"⚠️ {stock} data unavailable.")
    except Exception as e:
        st.error(f"{stock} fetch failed: {e}")

# 🪙 Bitcoin
try:
    btc_price = fetch_bitcoin_data()
    if btc_price:
        signals.append({
            "asset": "BITCOIN",
            "symbol": "BTC-INR",
            "price": btc_price,
            "target": round(btc_price * 1.1),
            "stop_loss": round(btc_price * 0.95),
            "logic": "Price Momentum + RSI"
        })
    else:
        st.warning("⚠️ Bitcoin data unavailable.")
except Exception as e:
    st.error(f"Bitcoin fetch failed: {e}")

# 🪙 Gold
try:
    gold_price = fetch_gold_data()
    if gold_price:
        signals.append({
            "asset": "GOLD",
            "symbol": "XAU-INR",
            "price": gold_price,
            "target": round(gold_price * 1.1),
            "stop_loss": round(gold_price * 0.95),
            "logic": "Commodity Trend + RSI"
        })
    else:
        st.warning("⚠️ Gold data unavailable.")
except Exception as e:
    st.error(f"Gold fetch failed: {e}")

# 📬 Alerts + Dashboard
for signal in signals:
    try:
        plot_pl(signal['price'], 30, signal.get('strike', signal['price']), signal.get('strike', signal['price']) + 300)
        send_telegram_message(signal)
    except Exception as e:
        st.error(f"Signal error for {signal['symbol']}: {e}")

show_dashboard(signals)
