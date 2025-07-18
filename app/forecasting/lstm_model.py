import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def forecast_with_lstm(df, lookback=60, forecast_steps=5):
    # Validate input
    if df.empty:
        print("⚠️ Input DataFrame is empty.")
        return pd.DataFrame()

    close_col = None
    for col in df.columns:
        if "close" in col.lower():
            close_col = col
            break

    if not close_col:
        print(f"❌ 'Close' column not found in DataFrame. Columns: {df.columns.tolist()}")
        return pd.DataFrame()

    if len(df) < lookback:
        print(f"❌ Not enough data for LSTM. Required: {lookback}, Found: {len(df)}")
        return pd.DataFrame()

    try:
        data = df[close_col].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)

        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i])
            y.append(scaled_data[i])

        X, y = np.array(X), np.array(y)

        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, epochs=10, batch_size=32, verbose=0)

        # Forecast next steps
        last_sequence = scaled_data[-lookback:]
        predictions = []
        input_seq = last_sequence.reshape(1, lookback, 1)

        for _ in range(forecast_steps):
            pred = model.predict(input_seq, verbose=0)
            predictions.append(pred[0][0])
            input_seq = np.append(input_seq[:, 1:, :], [[pred]], axis=1)

        forecast_values = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        future_dates = pd.date_range(start=pd.Timestamp.now().normalize(), periods=forecast_steps)

        return pd.DataFrame({
            "ds": future_dates,
            "yhat": forecast_values
        })

    except Exception as e:
        print(f"❌ LSTM forecasting error: {e}")
        return pd.DataFrame()
