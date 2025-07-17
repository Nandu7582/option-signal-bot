import pandas as pd

def simulate_bull_call(df, buy_strike, sell_strike, buy_premium=100, sell_premium=50):
    df = df.copy()
    df['spot'] = df['underlyingValue']
    df['payoff'] = df['spot'].apply(lambda x:
        -buy_premium if x < buy_strike else
        x - buy_strike - buy_premium if x < sell_strike else
        sell_strike - buy_strike - buy_premium + sell_premium
    )
    return df[['spot', 'payoff']]

def simulate_iron_condor(df, sell_pe, buy_pe, sell_ce, buy_ce, credit=100):
    df = df.copy()
    df['spot'] = df['underlyingValue']
    df['payoff'] = df['spot'].apply(lambda x:
        -100 if x < buy_pe else
        x - sell_pe + credit if x < sell_pe else
        credit if x < sell_ce else
        sell_ce - x + credit if x < buy_ce else
        -100
    )
    return df[['spot', 'payoff']]

def simulate_straddle(df, strike, premium=200):
    df = df.copy()
    df['spot'] = df['underlyingValue']
    df['payoff'] = df['spot'].apply(lambda x: abs(x - strike) - premium)
    return df[['spot', 'payoff']]

def calculate_metrics(df):
    profits = df['payoff']
    win_rate = (profits > 0).mean() * 100
    avg_return = profits.mean()
    max_drawdown = profits.max() - profits.min()
    profit_factor = profits[profits > 0].sum() / abs(profits[profits < 0].sum()) if profits[profits < 0].sum() != 0 else float('inf')

    return {
        "Win Rate (%)": round(win_rate, 2),
        "Average Return": round(avg_return, 2),
        "Max Drawdown": round(max_drawdown, 2),
        "Profit Factor": round(profit_factor, 2)
    }
