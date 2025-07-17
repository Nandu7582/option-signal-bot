import pandas as pd
import json
import os
import time
def fetch_stock_data(stock):
    fallback_used = False
    try:
        # Replace with actual live fetch logic
        df = pd.DataFrame(...)  # your live data
        return df, fallback_used, time.strftime("%H:%M:%S")
    except:
        fallback_path = f"app/static/{stock}_fallback.json"
        if os.path.exists(fallback_path):
            with open(fallback_path, "r") as f:
                cached = json.load(f)
            df = pd.DataFrame(cached)
            fallback_used = True
            return df, fallback_used, time.strftime("%H:%M:%S")
        return pd.DataFrame(), True, time.strftime("%H:%M:%S")
