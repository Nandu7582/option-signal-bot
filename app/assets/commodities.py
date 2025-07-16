def fetch_gold_data():
    url = "https://www.alphavantage.co/query?function=COMMODITY_EXCHANGE_RATE&from_symbol=XAU&to_symbol=INR&apikey=YOUR_API_KEY"
    data = requests.get(url).json()
    return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
