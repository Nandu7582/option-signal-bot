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
    win_rate = round((profits > 0).mean() * 100, 2)
    avg_return = round(profits.mean(), 2)
    max_drawdown = round(profits.max() - profits.min(), 2)

    total_gain = profits[profits > 0].sum()
    total_loss = abs(profits[profits < 0].sum())
    profit_factor = round(total_gain / total_loss, 2) if total_loss != 0 else float('inf')

    return {
        "Win Rate (%)": win_rate,
        "Average Return": avg_return,
        "Max Drawdown": max_drawdown,
        "Profit Factor": profit_factor
    }
