from nsepython import nse_optionchain_scrapper
import pandas as pd

def fetch_nse_option_chain(symbol="BANKNIFTY"):
    try:
        raw = nse_optionchain_scrapper(symbol)
        records = []
        spot = raw["records"]["underlyingValue"]
        expiry = raw["records"]["expiryDates"][0]
        for data in raw["records"]["data"]:
            strike = data["strikePrice"]
            if "CE" in data and data["CE"].get("expiryDate") == expiry:
                records.append({
                    "symbol": symbol,
                    "optionType": "CE",
                    "strikePrice": strike,
                    "openInterest": data["CE"]["openInterest"],
                    "impliedVolatility": data["CE"]["impliedVolatility"],
                    "underlyingValue": spot,
                    "expiry": expiry
                })
            if "PE" in data and data["PE"].get("expiryDate") == expiry:
                records.append({
                    "symbol": symbol,
                    "optionType": "PE",
                    "strikePrice": strike,
                    "openInterest": data["PE"]["openInterest"],
                    "impliedVolatility": data["PE"]["impliedVolatility"],
                    "underlyingValue": spot,
                    "expiry": expiry
                })
        return pd.DataFrame(records)
    except Exception as e:
        print(f"❌ NSE scrape failed: {e}")
        return pd.DataFrame()
