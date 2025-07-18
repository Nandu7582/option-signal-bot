import pandas as pd

def fetch_option_chain(symbol):
    return pd.DataFrame({
        "symbol": [symbol] * 6,
        "optionType": ["CE", "CE", "PE", "PE", "CE", "PE"],
        "strikePrice": [49000, 49300, 49000, 48700, 49500, 48500],
        "openInterest": [120000, 95000, 110000, 130000, 80000, 125000],
        "impliedVolatility": [22, 18, 25, 21, 19, 23],
        "underlyingValue": [49100] * 6
    })
