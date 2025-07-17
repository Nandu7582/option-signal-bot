import streamlit as st
from app.broker_api import fetch_option_chain, fetch_ltp, place_order
from app.signal_engine import generate_option_signals, suggest_hedge
from app.visualizer import plot_payoff, strategy_summary
from app.backtester import simulate_bull_call, simulate_iron_condor, simulate_straddle, calculate_metrics
from app.telegram_alerts import send_telegram_message
from app.storage import save_signal
from app.forecasting.prophet_model import forecast_with_prophet
from app.forecasting.lstm_model import forecast_with_lstm
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Signal Bot", layout="centered")
st.title("📊 Multi-Asset Option Signal Bot")

strategy = st.sidebar.selectbox("Choose Strategy", ["Bull Call Spread", "Iron Condor", "Straddle"])
symbol = st.sidebar.selectbox("Choose Index", ["BANKNIFTY", "NIFTY"])
auto_order = st.sidebar.checkbox("Auto-place order for high-confidence signals")

df_chain, fallback, ts = fetch_option_chain(symbol)
spot = fetch_ltp(symbol)

if not df_chain.empty:
    expiry_list = sorted(df_chain['expiryDate'].unique())
    expiry = st.sidebar.selectbox("Choose Expiry", expiry_list)
    df_chain = df_chain[df_chain['expiryDate'] == expiry]

    st.subheader(f"📈 {symbol} Option Chain")
    st.markdown(f"Timestamp: `{ts}`")
    st.dataframe(df_chain)

    signals = generate_option_signals(df_chain, strategy)
    for sig in signals:
        st.markdown(f"### 🧠 Signal: {sig['type']} for {sig['symbol']}")
        st.write(f"Confidence: `{sig['confidence']}`")
        st.caption(sig['logic'])

        fig = plot_payoff(strategy, spot, [sig.get(k) for k in ['buy_strike', 'sell_strike', 'strike', 'sell_pe', 'buy_pe', 'sell_ce', 'buy_ce']])
        st.plotly_chart(fig, use_container_width=True)

        summary = strategy_summary(strategy, [sig.get(k) for k in ['buy_strike', 'sell_strike', 'strike', 'sell_pe', 'buy_pe', 'sell_ce', 'buy_ce']])
        st.markdown("📊 **Strategy Summary**")
        st.table(summary)

        hedge = suggest_hedge(sig)
        if hedge:
            st.markdown("🛡️ **Hedge Suggestion**")
            for k, v in hedge.items():
                st.write(f"{k}: {v}")

        if sig['confidence'] >= 3:
            send_telegram_message(sig)
            save_signal(sig)

        if auto_order and sig['confidence'] >= 4:
            place_order(symbol=sig['symbol'], qty=1)
            st.success(f"✅ Auto-order placed for {sig['symbol']}")

        # Forecasting
        df = yf.download(f"{symbol}.NS", period="6mo", interval="1d")
        prophet_forecast = forecast_with_prophet(df)
        lstm_forecast = forecast_with_lstm(df)
        st.write("📊 Prophet Forecast:", prophet_forecast['yhat'].values[-1])
        st.write("🧠 LSTM Forecast:", round(lstm_forecast, 2))

        # Backtest
        st.subheader("📈 Strategy Backtest")
        if strategy == "Bull Call Spread":
            bt_df = simulate_bull_call(df_chain, sig['buy_strike'], sig['sell_strike'])
        elif strategy == "Iron Condor":
            bt_df = simulate_iron_condor(df_chain, sig['sell_pe'], sig['buy_pe'], sig['sell_ce'], sig['buy_ce'])
        elif strategy == "Straddle":
            bt_df = simulate_straddle(df_chain, sig['strike'])

        fig_bt = px.line(bt_df, x='spot', y='payoff', title=f"{strategy} Backtest Payoff")
        st.plotly_chart(fig_bt, use_container_width=True)

        metrics = calculate_metrics(bt_df)
        st.markdown("📊 **Performance Metrics**")
        st.table(metrics)
