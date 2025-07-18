import pandas as pd
from nsepython import nse_eq

def fetch_nse_stock_data(symbols):
    stock_data = []

    for symbol in symbols:
        try:
            data = nse_eq(symbol)
            stock_data.append({
                "symbol": symbol,
                "lastPrice": data.get("priceInfo", {}).get("lastPrice"),
                "dayHigh": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("max"),
                "dayLow": data.get("priceInfo", {}).get("intraDayHighLow", {}).get("min"),
                "volume": data.get("priceInfo", {}).get("quantityTraded"),
                "change": data.get("priceInfo", {}).get("change"),
                "pChange": data.get("priceInfo", {}).get("pChange")
            })
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            stock_data.append({
                "symbol": symbol,
                "lastPrice": None,
                "dayHigh": None,
                "dayLow": None,
                "volume": None,
                "change": None,
                "pChange": None
            })

    return pd.DataFrame(stock_data)
