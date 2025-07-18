from prophet import Prophet
import pandas as pd

def forecast_prices(df, periods=5):
    if "date" not in df.columns or "close" not in df.columns:
        return pd.DataFrame()
    model_df = df.rename(columns={"date": "ds", "close": "y"})
    model = Prophet()
    model.fit(model_df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
