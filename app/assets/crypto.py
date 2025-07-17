def fetch_bitcoin_data():
    try:
        price = requests.get(...).json()['bitcoin']['inr']
        return price, False
    except:
        with open("app/static/btc_fallback.json", "r") as f:
            return json.load(f)['price'], True
