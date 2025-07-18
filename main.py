import dash
from dash import dcc, html, Input, Output
import pandas as pd
from app.data_feeds import fetch_option_chain
from app.visualizer import plot_payoff, strategy_summary
from app.telegram_alerts import send_alert

app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])

strategies = ["Bull Call Spread", "Iron Condor", "Straddle", "Covered Call", "Protective Put"]

app.layout = html.Div([
    html.H2("📊 Option Signal Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(id="symbol-selector", options=[
            {"label": s, "value": s} for s in ["BANKNIFTY", "NIFTY", "RELIANCE", "ETHUSDT", "GOLD"]
        ], value="BANKNIFTY", style={"width": "200px"}),

        dcc.Dropdown(id="expiry-selector", placeholder="Select Expiry", style={"width": "200px"}),

        dcc.Dropdown(id="strategy-selector", options=[
            {"label": s, "value": s} for s in strategies
        ], value="Bull Call Spread", style={"width": "200px"}),

        dcc.RangeSlider(id="strike-slider", min=18000, max=50000, step=100,
                        value=[19000, 19500],
                        marks={i: str(i) for i in range(18000, 50001, 1000)}),

        dcc.Slider(id="oi-slider", min=0, max=200000, step=10000, value=100000,
                   marks={i: str(i) for i in range(0, 200001, 50000)},
                   tooltip={"placement": "bottom"}),

        html.Button("Export to CSV", id="export-btn"),
        html.Button("Send Telegram Alert", id="alert-btn"),
        dcc.Download(id="download")
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "20px"}),

    html.Div(id="signal-table"),
    html.Div(id="payoff-chart"),
    html.Div(id="strategy-summary")
])

# 🔄 Expiry options
@app.callback(
    Output("expiry-selector", "options"),
    Input("symbol-selector", "value")
)
def update_expiry_options(symbol):
    from app.nse_scraper import fetch_nse_option_chain
    raw = fetch_nse_option_chain(symbol, raw=True)
    expiries = raw["records"]["expiryDates"]
    return [{"label": e, "value": e} for e in expiries]

# 📊 Signal table + chart + summary
@app.callback(
    Output("signal-table", "children"),
    Output("payoff-chart", "figure"),
    Output("strategy-summary", "children"),
    Input("expiry-selector", "value"),
    Input("strike-slider", "value"),
    Input("oi-slider", "value"),
    Input("symbol-selector", "value"),
    Input("strategy-selector", "value")
)
def update_signals(expiry, strike_range, oi_threshold, symbol, strategy):
    df = fetch_option_chain(symbol, expiry)
    df = df[(df["strikePrice"] >= strike_range[0]) & (df["strikePrice"] <= strike_range[1])]
    df = df[df["openInterest"] >= oi_threshold]

    # 🧠 Confidence scoring
    df["confidence"] = (
        (df["openInterest"] / 100000).clip(0, 1) +
        (df["impliedVolatility"] > 20).astype(int) +
        (df["expiry"] == expiry).astype(int)
    ) * 33

    table = html.Table([
        html.Tr([html.Th(col) for col in df.columns])
    ] + [
        html.Tr([html.Td(row[col]) for col in df.columns]) for _, row in df.iterrows()
    ])

    if not df.empty:
        row = df.iloc[0]
        strikes = [row["strikePrice"], row["strikePrice"] + 300]
        fig = plot_payoff(strategy, row["underlyingValue"], strikes)
        summary = strategy_summary(strategy, strikes)
        summary_ui = html.Ul([html.Li(f"{k}: {v}") for k, v in summary.items()])
    else:
        fig = plot_payoff(strategy, 49000, [49000, 49300])
        summary_ui = html.Div("No signals to summarize.")

    return table, fig, summary_ui

# 📦 Export to CSV
@app.callback(
    Output("download", "data"),
    Input("export-btn", "n_clicks"),
    Input("expiry-selector", "value"),
    Input("strike-slider", "value"),
    Input("oi-slider", "value"),
    Input("symbol-selector", "value"),
    prevent_initial_call=True
)
def export_csv(n, expiry, strike_range, oi_threshold, symbol):
    df = fetch_option_chain(symbol, expiry)
    df = df[(df["strikePrice"] >= strike_range[0]) & (df["strikePrice"] <= strike_range[1])]
    df = df[df["openInterest"] >= oi_threshold]
    return dcc.send_data_frame(df.to_csv, "signals.csv")

# 🔔 Telegram alert
@app.callback(
    Output("alert-btn", "children"),
    Input("alert-btn", "n_clicks"),
    Input("expiry-selector", "value"),
    Input("strike-slider", "value"),
    Input("oi-slider", "value"),
    Input("symbol-selector", "value"),
    Input("strategy-selector", "value"),
    prevent_initial_call=True
)
def send_telegram_alert(n, expiry, strike_range, oi_threshold, symbol, strategy):
    df = fetch_option_chain(symbol, expiry)
    df = df[(df["strikePrice"] >= strike_range[0]) & (df["strikePrice"] <= strike_range[1])]
    df = df[df["openInterest"] >= oi_threshold]
    if df.empty:
        return "No signals to alert"
    row = df.iloc[0]
    msg = f"""
📌 SIGNAL – {symbol} {expiry} Expiry 🟢 BUY {row['strikePrice']} {row['optionType']} @ ₹{row['ltp']}
🎯 Strategy: {strategy}
📈 Confidence: {int(row['confidence'])}%
📊 OI: {row['openInterest']} | IV: {row['impliedVolatility']}
"""
    send_alert(msg)
    return "✅ Alert Sent"

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=5000)
