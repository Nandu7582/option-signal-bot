import httpx

def get_banknifty_option_oi():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nseindia.com/option-chain"
    }

    with httpx.Client(headers=headers, follow_redirects=True, timeout=20) as client:
        client.get("https://www.nseindia.com")  # to set cookies
        res = client.get(url)
        data = res.json()

    results = []
    for row in data['records']['data']:
        if 'CE' in row and 'PE' in row:
            results.append({
                "strike": row["strikePrice"],
                "call_oi": row["CE"]["openInterest"],
                "put_oi": row["PE"]["openInterest"]
            })

    return results[:5]
