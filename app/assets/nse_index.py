from nsepython import *

def fetch_index_options(symbol="BANKNIFTY"):
    data = nse_optionchain_scrapper(symbol)
    df = pd.DataFrame(data['records']['data'])
    return df
