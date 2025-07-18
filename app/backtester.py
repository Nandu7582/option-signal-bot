import pandas as pd

def calculate_metrics(profits):
    total_trades = len(profits)
    wins = profits[profits > 0]
    losses = profits[profits < 0]

    win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0
    avg_win = wins.mean() if not wins.empty else 0
    avg_loss = losses.mean() if not losses.empty else 0
    total_profit = profits.sum()
    avg_profit = profits.mean() if total_trades > 0 else 0

    return {
        "Total Trades": total_trades,
        "Win Rate (%)": round(win_rate, 2),
        "Average Win": round(avg_win, 2),
        "Average Loss": round(avg_loss, 2),
        "Total Profit": round(total_profit, 2),
        "Average Profit": round(avg_profit, 2)
    }

def simulate_iron_condor(df):
    # Example logic: payoff based on strike spread and volatility
    profits = []
    for _, row in df.iterrows():
        spread = abs(row["sell_strike"] - row["buy_strike"])
        volatility = row.get("impliedVolatility", 20)
        premium = spread * 0.3  # Assume 30% of spread as premium
        risk = spread - premium

        # Simulate outcome
        if volatility < 25:
            profits.append(premium)  # Favorable
        else:
            profits.append(-risk)    # Unfavorable

    return pd.Series(profits)

def run_backtest(strategy_name):
    df = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
        "buy_strike": [18200, 18300, 18400, 18500, 18600],
        "sell_strike": [18400, 18500, 18600, 18700, 18800],
        "impliedVolatility": [22, 28, 24, 30, 19]
    })

    if strategy_name == "Iron Condor":
        profits = simulate_iron_condor(df)
    else:
        profits = pd.Series([1200, -500, 800, 1500, -300])  # Dummy fallback

    metrics = calculate_metrics(profits)

    summary = f"""
📈 Backtest Summary for Strategy: {strategy_name}
--------------------------------------------------
Total Trades: {metrics['Total Trades']}
Win Rate: {metrics['Win Rate (%)']}%
Average Win: ₹{metrics['Average Win']}
Average Loss: ₹{metrics['Average Loss']}
Total Profit: ₹{metrics['Total Profit']}
Average Profit per Trade: ₹{metrics['Average Profit']}
"""

    return summary
