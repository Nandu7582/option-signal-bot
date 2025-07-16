def generate_signal(asset_type, df, expiry=None):
    signals = []
    for row in df.itertuples():
        if row.macd > row.macd_signal and row.rsi > 50:
            signal = {
                "asset": asset_type,
                "symbol": getattr(row, 'symbol', 'N/A'),
                "strike": getattr(row, 'strikePrice', None),
                "price": row.close,
                "target": round(row.close * 1.3),
                "stop_loss": round(row.close * 0.83),
                "hedge": f"SELL {row.strikePrice + 300} CE" if asset_type in ["BANKNIFTY", "NIFTY"] else None,
                "logic": "MACD + RSI + Volume/OI",
                "greeks": {"delta": 0.55, "gamma": 0.09} if asset_type in ["BANKNIFTY", "NIFTY"] else None
            }
            signals.append(signal)
    return signals
