import pandas as pd
import ta

def clean_price_data(df, price_column='close'):
    df[price_column] = pd.to_numeric(df[price_column], errors='coerce')
    df.dropna(subset=[price_column], inplace=True)
    return df

def add_macd(df, price_column='close'):
    macd = ta.trend.MACD(close=df[price_column])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def add_rsi(df, price_column='close'):
    rsi = ta.momentum.RSIIndicator(close=df[price_column])
    df['rsi'] = rsi.rsi()
    return df

def add_bollinger(df, price_column='close'):
    bb = ta.volatility.BollingerBands(close=df[price_column])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    return df

def add_vwap(df, price_column='close'):
    if 'volume' in df.columns:
        df['vwap'] = (df[price_column] * df['volume']).cumsum() / df['volume'].cumsum()
    return df

def add_indicators(df, price_column='close'):
    df = clean_price_data(df, price_column)
    df = add_macd(df, price_column)
    df = add_rsi(df, price_column)
    df = add_bollinger(df, price_column)
    df = add_vwap(df, price_column)
    df = df.dropna().reset_index(drop=True)
    return df
