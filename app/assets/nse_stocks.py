def fetch_stock_data(stock):
    try:
        # Your live fetch logic
        df = pd.DataFrame(...)  # actual data
        return df, False
    except:
        # Load fallback if available
        fallback_path = f"app/static/{stock}_fallback.json"
        if os.path.exists(fallback_path):
            with open(fallback_path, "r") as f:
                cached = json.load(f)
            return pd.DataFrame(cached), True
        return pd.DataFrame(), True
