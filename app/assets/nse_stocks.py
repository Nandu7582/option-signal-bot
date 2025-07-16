def fetch_stock_data(stock_symbol):
    df = nse_eq(stock_symbol)
    return df  # Contains price, volume, etc.
