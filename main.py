from app.assets.nse_index import fetch_index_options
from app.assets.nse_stocks import fetch_stock_data
from app.assets.crypto import fetch_bitcoin_data
from app.assets.commodities import fetch_gold_data
from app.indicators import add_indicators
from app.signal_engine import generate_signal
from app.dashboard import show_dashboard
from app.telegram_alerts import send_telegram_message
from app.pl_plotter import plot_pl

signals = []

# Bank Nifty
df_bn = fetch_index_options("BANKNIFTY")
df_bn = add_indicators(df_bn)
signals += generate_signal("BANKNIFTY", df_bn, expiry="18JUL2024")

# Nifty
df_nf = fetch_index_options("NIFTY")
df_nf = add_indicators(df_nf)
signals += generate_signal("NIFTY", df_nf, expiry="18JUL2024")

# Nifty 500 Stocks
for stock in ["RELIANCE", "TCS", "INFY"]:
    df_stock = fetch_stock_data(stock)
    df_stock = add_indicators(df_stock)
    signals += generate_signal("STOCK", df_stock)

# Bitcoin
btc_price = fetch_bitcoin_data()
signals.append({
    "asset": "BITCOIN",
    "symbol": "BTC-INR",
    "price": btc_price,
    "target": round(btc_price * 1.1),
    "stop_loss": round(btc_price * 0.95),
    "logic": "Price Momentum + RSI"
})

# Gold
gold_price = fetch_gold_data()
signals.append({
    "asset": "GOLD",
    "symbol": "XAU-INR",
    "price": gold_price,
    "target": round(gold_price * 1.1),
    "stop_loss": round(gold_price * 0.95),
    "logic": "Commodity Trend + RSI"
})

# Alerts + Dashboard
for signal in signals:
    plot_pl(signal['price'], 30, signal.get('strike', signal['price']), signal.get('strike', signal['price']) + 300)
    send_telegram_message(signal)

show_dashboard(signals)
