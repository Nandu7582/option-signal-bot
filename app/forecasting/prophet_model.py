# app/forecasting/prophet_model.py

from prophet import Prophet
import pandas as pd

def forecast_prices(df, periods=5):
    # Ensure df has 'ds' and 'y' columns
    model_df = df[['date', 'close']].rename(columns={'date': 'ds', 'close': 'y'})
    model = Prophet()
    model.fit(model_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
