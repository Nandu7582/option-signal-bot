def generate_option_signals(df, strategy="Bull Call Spread"):
    signals = []
    df = df[df['optionType'].isin(['CE', 'PE'])].copy()

    spot_price = df['underlyingValue'].iloc[0]
    df['distance'] = abs(df['strikePrice'] - spot_price)

    def score(row):
        score = 0
        if row['openInterest'] > 100000: score += 1
        if row['impliedVolatility'] > 20: score += 1
        if abs(row['strikePrice'] - spot_price) < 100: score += 1
        return score

    df['confidence'] = df.apply(score, axis=1)

    if strategy == "Bull Call Spread":
        ce_df = df[df['optionType'] == 'CE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if not ce_df.empty:
            atm = ce_df.iloc[0]
            otm = ce_df[ce_df['strikePrice'] > atm['strikePrice']].sort_values('confidence', ascending=False).head(1)
            if not otm.empty:
                signals.append({
                    "symbol": df['symbol'].iloc[0],
                    "type": "Bull Call Spread",
                    "buy_strike": atm['strikePrice'],
                    "sell_strike": otm.iloc[0]['strikePrice'],
                    "confidence": atm['confidence'] + otm.iloc[0]['confidence'],
                    "logic": "ATM CE + OTM CE with high OI/IV"
                })

    elif strategy == "Iron Condor":
        ce_df = df[df['optionType'] == 'CE'].sort_values('strikePrice')
        pe_df = df[df['optionType'] == 'PE'].sort_values('strikePrice', ascending=False)
        if not ce_df.empty and not pe_df.empty:
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Iron Condor",
                "sell_ce": ce_df.iloc[-2]['strikePrice'],
                "buy_ce": ce_df.iloc[-1]['strikePrice'],
                "sell_pe": pe_df.iloc[-2]['strikePrice'],
                "buy_pe": pe_df.iloc[-1]['strikePrice'],
                "confidence": ce_df.iloc[-2]['confidence'] + pe_df.iloc[-2]['confidence'],
                "logic": "Volatility range + OI filter"
            })

    elif strategy == "Straddle":
        atm_df = df.sort_values('distance').head(1)
        if not atm_df.empty:
            strike = atm_df.iloc[0]['strikePrice']
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Straddle",
                "strike": strike,
                "confidence": atm_df.iloc[0]['confidence'],
                "logic": "ATM CE + PE with high OI"
            })

    return signals

def suggest_hedge(signal):
    if signal['type'] == "Bull Call Spread":
        return {
            "hedge_type": "Put Buy",
            "strike": signal['buy_strike'] - 200,
            "logic": "Protect downside below long CE strike"
        }
    elif signal['type'] == "Iron Condor":
        return {
            "hedge_type": "Calendar Spread",
            "logic": "Use different expiry to hedge range risk"
        }
    elif signal['type'] == "Straddle":
        return {
            "hedge_type": "Strangle",
            "strike_low": signal['strike'] - 100,
            "strike_high": signal['strike'] + 100,
            "logic": "Reduce premium cost by widening strikes"
        }
    return {}
