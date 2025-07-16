def fetch_banknifty_options():
    # Mock Open Interest data — replace with NSE scraper later
    return [
        {"strike": 48800, "call_oi": 75000, "put_oi": 60000},
        {"strike": 49000, "call_oi": 92000, "put_oi": 81000},
        {"strike": 49200, "call_oi": 112000, "put_oi": 45000},
        {"strike": 49500, "call_oi": 98000, "put_oi": 89000},
        {"strike": 49800, "call_oi": 70000, "put_oi": 95000}
    ]
