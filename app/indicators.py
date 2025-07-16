import pandas as pd
import ta  # Technical Analysis library

def clean_price_data(df, price_column='close'):
    """Ensure price column exists and is numeric."""
    df[price_column] = pd.to_numeric(df[price_column], errors='coerce')
    df.dropna(subset=[price_column], inplace=True)
    return df

def add_macd(df, price_column='close'):
    df['macd'] = ta.trend.macd(df[price_column])
    df['macd_signal'] = ta.trend.macd_signal(df[price_column])
    return df

def add_rsi(df, price_column='close'):
    df['rsi'] = ta.momentum.rsi(df[price_column])
    return df

def add_bollinger(df, price_column='close'):
    bb = ta.volatility.BollingerBands(close=df[price_column])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    return df

def add_vwap(df):
    if 'volume' in df.columns and 'close' in df.columns:
        df['vwap'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

def add_indicators(df, price_column='close'):
    df = clean_price_data(df, price_column)
    df = add_macd(df, price_column)
    df = add_rsi(df, price_column)
    df = add_bollinger(df, price_column)
    df = add_vwap(df)
    return df
