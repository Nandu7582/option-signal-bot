import matplotlib.pyplot as plt
import numpy as np
import os

def plot_pl(buy_price, sell_price, buy_strike, sell_strike, filename="app/static/pl_graph.png"):
    """
    Plots P&L for a Bull Call Spread:
    - Buy lower strike CE
    - Sell higher strike CE
    """

    spot_prices = np.linspace(buy_strike - 500, sell_strike + 500, 100)
    pnl = []

    for spot in spot_prices:
        if spot < buy_strike:
            profit = -buy_price
        elif spot < sell_strike:
            profit = spot - buy_strike - buy_price
        else:
            profit = sell_strike - buy_strike - buy_price + sell_price
        pnl.append(profit)

    plt.figure(figsize=(10, 5))
    plt.plot(spot_prices, pnl, label="P&L", color="green", linewidth=2)
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(buy_strike, color='blue', linestyle='--', label=f"Buy Strike: {buy_strike}")
    plt.axvline(sell_strike, color='red', linestyle='--', label=f"Sell Strike: {sell_strike}")
    plt.title("Max Profit/Loss Graph")
    plt.xlabel("Spot Price")
    plt.ylabel("Profit / Loss (₹)")
    plt.grid(True)
    plt.legend()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename)
    plt.close()
