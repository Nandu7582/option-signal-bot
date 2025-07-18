import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
from app.signal_engine import generate_signals
from app.forecasting.prophet_model import forecast_with_prophet
from app.backtester import run_backtest  # Ensure this exists or wrap it
import os

app = dash.Dash(__name__)
app.title = "Option Signal Dashboard"

# Load signals
try:
    signals = generate_signals()
except Exception as e:
    print(f"⚠️ Error loading signals: {e}")
    signals = {
        "stocks": pd.DataFrame(),
        "index": pd.DataFrame(),
        "crypto": pd.DataFrame(),
        "commodities": pd.DataFrame()
    }

# Forecast wrapper
def run_forecast():
    forecast_result = {}
    for key in signals:
        try:
            df = signals[key]
            if not df.empty and "date" in df.columns and "close" in df.columns:
                forecast_result[key] = forecast_with_prophet(df)
            else:
                forecast_result[key] = pd.DataFrame()
        except Exception as e:
            print(f"⚠️ Forecast error for {key}: {e}")
            forecast_result[key] = pd.DataFrame()
    return forecast_result

# Load forecasts
prophet_forecast = run_forecast()

# Strategy options
strategies = ["Bull Call Spread", "Iron Condor", "Straddle", "Custom"]

def signal_table(df):
    if df.empty:
        return html.Div("No signals available.")
    return html.Table([
        html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
         for i in range(len(df))]
    )

def forecast_chart(df, title):
    if df.empty or "ds" not in df.columns or "yhat" not in df.columns:
        return html.Div("No forecast data available.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ds'], y=df['yhat'], mode='lines', name='Forecast'))
    fig.update_layout(title=title)
    return dcc.Graph(figure=fig, style={"height": "300px"})

def tradingview_iframe(symbol):
    return html.Iframe(
        src=f"https://s.tradingview.com/embed-widget/symbol-overview/?locale=en&symbol=NSE:{symbol}",
        style={"width": "100%", "height": "300px", "border": "none"}
    )

app.layout = html.Div([
    html.H1("📊 Option Signal Dashboard"),
    
    html.Label("Select Strategy"),
    dcc.Dropdown(
        options=[{"label": s, "value": s} for s in strategies],
        value="Bull Call Spread",
        id="strategy-selector"
    ),

    dcc.Tabs([
        dcc.Tab(label="Stocks", children=[
            html.H3("Signals"),
            signal_table(signals['stocks']),
            html.H3("Forecast"),
            forecast_chart(prophet_forecast['stocks'], "Stocks Forecast"),
            html.H3("Live Chart"),
            tradingview_iframe("RELIANCE")
        ]),
        dcc.Tab(label="Index", children=[
            html.H3("Signals"),
            signal_table(signals['index']),
            html.H3("Forecast"),
            forecast_chart(prophet_forecast['index'], "Index Forecast"),
            html.H3("Live Chart"),
            tradingview_iframe("BANKNIFTY")
        ]),
        dcc.Tab(label="Crypto", children=[
            html.H3("Signals"),
            signal_table(signals['crypto']),
            html.H3("Forecast"),
            forecast_chart(prophet_forecast['crypto'], "Crypto Forecast")
        ]),
        dcc.Tab(label="Commodities", children=[
            html.H3("Signals"),
            signal_table(signals['commodities']),
            html.H3("Forecast"),
            forecast_chart(prophet_forecast['commodities'], "Commodities Forecast")
        ]),
        dcc.Tab(label="Backtest", children=[
            html.H3("Backtest Results"),
            html.Pre(run_backtest("Bull Call Spread"))
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
