from prophet import Prophet
import pandas as pd

def forecast_with_prophet(df, periods=5):
    if df.empty or "date" not in df.columns or "close" not in df.columns:
        return pd.DataFrame()

    model_df = df.rename(columns={"date": "ds", "close": "y"})
    model = Prophet()
    model.fit(model_df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

def run_forecast(signals_dict):
    forecast_result = {}
    for key, df in signals_dict.items():
        try:
            forecast_result[key] = forecast_with_prophet(df)
        except Exception as e:
            print(f"⚠️ Forecast error for {key}: {e}")
            forecast_result[key] = pd.DataFrame()
    return forecast_result
