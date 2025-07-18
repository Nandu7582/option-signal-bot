import plotly.graph_objects as go
import numpy as np

def plot_payoff(strategy, spot, strikes, premiums=None):
    x = np.linspace(spot - 500, spot + 500, 100)
    y = np.zeros_like(x)

    if strategy == "Bull Call Spread":
        buy_strike, sell_strike = strikes
        buy_premium = premiums[0] if premiums else 100
        sell_premium = premiums[1] if premiums else 50

        y = np.where(x < buy_strike, -buy_premium,
            np.where(x < sell_strike, x - buy_strike - buy_premium,
                     sell_strike - buy_strike - buy_premium + sell_premium))

    elif strategy == "Iron Condor":
        sell_pe, buy_pe, sell_ce, buy_ce = strikes
        pe_premium = premiums[0] if premiums else 50
        ce_premium = premiums[1] if premiums else 50

        y = np.where(x < buy_pe, -100,
            np.where(x < sell_pe, x - sell_pe + pe_premium,
            np.where(x < sell_ce, pe_premium + ce_premium,
            np.where(x < buy_ce, sell_ce - x + ce_premium, -100))))

    elif strategy == "Straddle":
        strike = strikes[0]
        premium = premiums[0] if premiums else 200
        y = np.abs(x - strike) - premium

    elif strategy == "Covered Call":
        sell_strike = strikes[0]
        premium = premiums[0] if premiums else 50
        y = np.where(x < sell_strike, x - spot + premium,
                     sell_strike - spot + premium)

    elif strategy == "Protective Put":
        buy_strike = strikes[0]
        premium = premiums[0] if premiums else 50
        y = np.where(x > buy_strike, x - spot - premium,
                     buy_strike - spot - premium)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Payoff', line=dict(color='green')))
    fig.update_layout(
        title=f"{strategy} Payoff",
        xaxis_title="Spot Price",
        yaxis_title="Profit / Loss",
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def strategy_summary(strategy, strikes, premiums=None):
    if strategy == "Bull Call Spread":
        buy, sell = strikes
        buy_premium = premiums[0] if premiums else 100
        sell_premium = premiums[1] if premiums else 50
        max_profit = (sell - buy - buy_premium + sell_premium) * 100
        max_loss = buy_premium * 100
        breakeven = buy + buy_premium
        return {
            "Max Profit": f"₹{max_profit}",
            "Max Loss": f"₹{-max_loss}",
            "Breakeven": f"₹{breakeven}"
        }

    elif strategy == "Straddle":
        strike = strikes[0]
        premium = premiums[0] if premiums else 200
        return {
            "Max Profit": "Unlimited",
            "Max Loss": f"₹{-premium * 100}",
            "Breakeven": f"₹{strike - premium} / ₹{strike + premium}"
        }

    elif strategy == "Iron Condor":
        return {
            "Max Profit": "Net credit",
            "Max Loss": "Spread width - credit",
            "Breakeven": "Between short strikes ± credit"
        }

    elif strategy == "Covered Call":
        strike = strikes[0]
        premium = premiums[0] if premiums else 50
        return {
            "Max Profit": f"₹{(strike - spot + premium) * 100}",
            "Max Loss": "Unlimited downside",
            "Breakeven": f"₹{spot - premium}"
        }

    elif strategy == "Protective Put":
        strike = strikes[0]
        premium = premiums[0] if premiums else 50
        return {
            "Max Profit": "Unlimited upside",
            "Max Loss": f"₹{(spot - strike + premium) * 100}",
            "Breakeven": f"₹{spot + premium}"
        }

    return {}
