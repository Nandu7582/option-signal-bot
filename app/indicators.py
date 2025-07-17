import pandas as pd
import ta

def add_indicators(df, price_column='close'):
    df = df.copy()
    df = df.dropna().reset_index(drop=True)

    rsi = ta.momentum.RSIIndicator(close=df[price_column])
    df['RSI'] = rsi.rsi()

    macd = ta.trend.MACD(close=df[price_column])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    bb = ta.volatility.BollingerBands(close=df[price_column])
    df['BB_high'] = bb.bollinger_hband()
    df['BB_low'] = bb.bollinger_lband()
    df['BB_width'] = df['BB_high'] - df['BB_low']

    if 'volume' in df.columns:
        df['VWAP'] = (df[price_column] * df['volume']).cumsum() / df['volume'].cumsum()

    return df.dropna().reset_index(drop=True)
