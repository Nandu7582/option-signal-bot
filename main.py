import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
from app import signal_engine, telegram_alerts, backtester
from app.forecasting import prophet_model
import os

app = dash.Dash(__name__)
app.title = "Option Signal Dashboard"

# Load signals and forecasts
signals = signal_engine.generate_signals()
prophet_forecast = prophet_model.run_forecast()

# Strategy options
strategies = ["Bull Call Spread", "Iron Condor", "Straddle", "Custom"]

def signal_table(df):
    return html.Table([
        html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
         for i in range(len(df))]
    )

def forecast_chart(df, title):
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
            signal_table(signals['index']),
            forecast_chart(prophet_forecast['index'], "Index Forecast"),
            tradingview_iframe("BANKNIFTY")
        ]),
        dcc.Tab(label="Crypto", children=[
            signal_table(signals['crypto']),
            forecast_chart(prophet_forecast['crypto'], "Crypto Forecast")
        ]),
        dcc.Tab(label="Commodities", children=[
            signal_table(signals['commodities']),
            forecast_chart(prophet_forecast['commodities'], "Commodities Forecast")
        ]),
        dcc.Tab(label="Backtest", children=[
            html.H3("Backtest Results"),
            html.Pre(backtester.run_backtest("Bull Call Spread"))
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
