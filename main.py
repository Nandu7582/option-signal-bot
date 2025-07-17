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
import streamlit as st
import time
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

# 🔁 Auto-refresh every 5 minutes
st.experimental_set_query_params(refresh=str(time.time()))
st.markdown(
    "<meta http-equiv='refresh' content='300'>",
    unsafe_allow_html=True
)

# 🧠 Strategy Selector
st.sidebar.header("🧠 Strategy Selector")
strategy = st.sidebar.selectbox("Choose Strategy", ["Bull Call Spread", "Iron Condor", "Straddle", "Custom"])
st.sidebar.markdown(f"Selected Strategy: **{strategy}**")

signals = []
signal_health = {}

# 🏦 Bank Nifty
try:
    df_bn, fallback_bn, ts_bn = fetch_index_options("BANKNIFTY")
    signal_health["BANKNIFTY"] = f"{'Fallback' if fallback_bn else 'Live'} (Updated: {ts_bn})"
    if not df_bn.empty:
        df_bn = add_indicators(df_bn)
        signals += generate_signal("BANKNIFTY", df_bn, expiry="18JUL2024", strategy=strategy)
    else:
        st.warning("⚠️ Bank Nifty data unavailable. Skipping signal.")
except Exception as e:
    st.error(f"Bank Nifty fetch failed: {e}")
    signal_health["BANKNIFTY"] = "Error"

# 🏦 Nifty
try:
    df_nf, fallback_nf, ts_nf = fetch_index_options("NIFTY")
    signal_health["NIFTY"] = f"{'Fallback' if fallback_nf else 'Live'} (Updated: {ts_nf})"
    if not df_nf.empty:
        df_nf = add_indicators(df_nf)
        signals += generate_signal("NIFTY", df_nf, expiry="18JUL2024", strategy=strategy)
    else:
        st.warning("⚠️ Nifty data unavailable. Skipping signal.")
except Exception as e:
    st.error(f"Nifty fetch failed: {e}")
    signal_health["NIFTY"] = "Error"

# 📈 Nifty 500 Stocks
for stock in ["RELIANCE", "TCS", "INFY"]:
    try:
        df_stock, fallback_stock, ts_stock = fetch_stock_data(stock)
        signal_health[stock] = f"{'Fallback' if fallback_stock else 'Live'} (Updated: {ts_stock})"
        if not df_stock.empty:
            df_stock = add_indicators(df_stock)
            signals += generate_signal("STOCK", df_stock, strategy=strategy)
        else:
            st.warning(f"⚠️ {stock} data unavailable.")
    except Exception as e:
        st.error(f"{stock} fetch failed: {e}")
        signal_health[stock] = "Error"

# 🪙 Bitcoin
try:
    btc_price, fallback_btc, ts_btc = fetch_bitcoin_data()
    signal_health["BITCOIN"] = f"{'Fallback' if fallback_btc else 'Live'} (Updated: {ts_btc})"
    if btc_price:
        signals.append({
            "asset": "BITCOIN",
            "symbol": "BTC-INR",
            "price": btc_price,
            "target": round(btc_price * 1.1),
            "stop_loss": round(btc_price * 0.95),
            "logic": f"Price Momentum + RSI ({strategy})"
        })
    else:
        st.warning("⚠️ Bitcoin data unavailable.")
except Exception as e:
    st.error(f"Bitcoin fetch failed: {e}")
    signal_health["BITCOIN"] = "Error"

# 🪙 Gold
try:
    gold_price, fallback_gold, ts_gold = fetch_gold_data()
    signal_health["GOLD"] = f"{'Fallback' if fallback_gold else 'Live'} (Updated: {ts_gold})"
    if gold_price:
        signals.append({
            "asset": "GOLD",
            "symbol": "XAU-INR",
            "price": gold_price,
            "target": round(gold_price * 1.1),
            "stop_loss": round(gold_price * 0.95),
            "logic": f"Commodity Trend + RSI ({strategy})"
        })
    else:
        st.warning("⚠️ Gold data unavailable.")
except Exception as e:
    st.error(f"Gold fetch failed: {e}")
    signal_health["GOLD"] = "Error"

# 📊 Signal Health Section
st.subheader("📊 Signal Health Status")
for asset, status in signal_health.items():
    color = "🟢" if "Live" in status else "🟡" if "Fallback" in status else "🔴"
    st.markdown(f"{color} **{asset}**: {status}", unsafe_allow_html=True)

# 📬 Alerts + Dashboard
for signal in signals:
    try:
        plot_pl(signal['price'], 30, signal.get('strike', signal['price']), signal.get('strike', signal['price']) + 300)
        send_telegram_message(signal)
    except Exception as e:
        st.error(f"Signal error for {signal['symbol']}: {e}")

show_dashboard(signals)
