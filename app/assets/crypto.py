import requests

def fetch_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
    data = requests.get(url).json()
    return data['bitcoin']['inr']
