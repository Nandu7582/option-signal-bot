import dash
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
from app import signal_engine
from app.forecasting import prophet_model
import os

app = dash.Dash(__name__)
app.title = "Option Signal Dashboard"

# Load signals
signals = signal_engine.generate_signals()

# Forecasts
prophet_forecast = prophet_model.run_forecast()

def signal_table(df):
    return html.Table([
        html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
         for i in range(len(df))]
    )

def forecast_chart(df, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ds'], y=df['yhat'], mode='lines', name='Forecast'))
    return dcc.Graph(figure=fig, style={"height": "300px"})

app.layout = html.Div([
    html.H1("📊 Option Signal Dashboard"),
    dcc.Tabs([
        dcc.Tab(label="Stocks", children=[
            html.H3("Signals"),
            signal_table(signals['stocks']),
            html.H3("Forecast"),
            forecast_chart(prophet_forecast['stocks'], "Stocks Forecast"),
        ]),
        dcc.Tab(label="Index", children=[
            signal_table(signals['index']),
            forecast_chart(prophet_forecast['index'], "Index Forecast"),
        ]),
        dcc.Tab(label="Crypto", children=[
            signal_table(signals['crypto']),
            forecast_chart(prophet_forecast['crypto'], "Crypto Forecast"),
        ]),
        dcc.Tab(label="Commodities", children=[
            signal_table(signals['commodities']),
            forecast_chart(prophet_forecast['commodities'], "Commodities Forecast"),
        ]),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=3000)
