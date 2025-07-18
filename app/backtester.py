import pandas as pd

def run_backtest(strategy_name):
    # Dummy historical data
    data = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
        "buy_strike": [18200, 18300, 18400, 18500, 18600],
        "sell_strike": [18400, 18500, 18600, 18700, 18800],
        "profit": [1200, -500, 800, 1500, -300]
    })

    total_profit = data["profit"].sum()
    win_rate = (data["profit"] > 0).mean() * 100

    summary = f"""
📈 Backtest Summary for Strategy: {strategy_name}
--------------------------------------------------
Total Trades: {len(data)}
Winning Trades: {(data["profit"] > 0).sum()}
Win Rate: {win_rate:.2f}%
Total Profit: ₹{total_profit}
Average Profit per Trade: ₹{data["profit"].mean():.2f}
"""

    return summary
