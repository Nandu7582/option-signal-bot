def fetch_gold_data():
    try:
        price = requests.get(...).json()['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return float(price), False
    except:
        with open("app/static/gold_fallback.json", "r") as f:
            return json.load(f)['price'], True
