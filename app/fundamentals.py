import yfinance as yf

def fetch_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "pe_ratio": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0),
            "volume": info.get("volume", 0),
            "sector": info.get("sector", "Unknown")
        }
    except Exception as e:
        print(f"Fundamental fetch failed for {symbol}: {e}")
        return {}
