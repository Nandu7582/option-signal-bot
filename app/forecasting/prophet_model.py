from prophet import Prophet
import pandas as pd

def forecast_with_prophet(df, periods=5):
    # Validate input
    if df.empty:
        print("⚠️ Input DataFrame is empty. Skipping forecast.")
        return pd.DataFrame()

    # Try to locate a valid date column
    date_col = None
    for col in df.columns:
        if "date" in col.lower():
            date_col = col
            break

    if not date_col or "close" not in df.columns:
        print(f"❌ Missing required columns. Found columns: {df.columns.tolist()}")
        return pd.DataFrame()

    try:
        model_df = df[[date_col, "close"]].rename(columns={date_col: "ds", "close": "y"})
        model_df["ds"] = pd.to_datetime(model_df["ds"])

        model = Prophet()
        model.fit(model_df)

        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    except Exception as e:
        print(f"❌ Forecasting error: {e}")
        return pd.DataFrame()
