def generate_option_signals(df, strategy):
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

    elif strategy == "Bear Call Spread":
        ce_df = df[df['optionType'] == 'CE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if len(ce_df) >= 2:
            otm = ce_df.iloc[0]
            further_otm = ce_df.iloc[1]
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Bear Call Spread",
                "sell_strike": otm['strikePrice'],
                "buy_strike": further_otm['strikePrice'],
                "confidence": otm['confidence'] + further_otm['confidence'],
                "logic": "OTM CE credit spread"
            })

    elif strategy == "Bull Put Spread":
        pe_df = df[df['optionType'] == 'PE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if len(pe_df) >= 2:
            otm = pe_df.iloc[0]
            further_otm = pe_df.iloc[1]
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Bull Put Spread",
                "sell_strike": otm['strikePrice'],
                "buy_strike": further_otm['strikePrice'],
                "confidence": otm['confidence'] + further_otm['confidence'],
                "logic": "OTM PE credit spread"
            })

    elif strategy == "Iron Condor":
        ce_df = df[df['optionType'] == 'CE'].sort_values('strikePrice')
        pe_df = df[df['optionType'] == 'PE'].sort_values('strikePrice', ascending=False)
        if len(ce_df) >= 2 and len(pe_df) >= 2:
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

    elif strategy == "Long Straddle":
        atm_df = df.sort_values('distance').head(1)
        if not atm_df.empty:
            strike = atm_df.iloc[0]['strikePrice']
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Long Straddle",
                "strike": strike,
                "confidence": atm_df.iloc[0]['confidence'],
                "logic": "ATM CE + PE with high OI"
            })

    elif strategy == "Long Strangle":
        ce_df = df[df['optionType'] == 'CE'].sort_values('strikePrice')
        pe_df = df[df['optionType'] == 'PE'].sort_values('strikePrice', ascending=False)
        if not ce_df.empty and not pe_df.empty:
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Long Strangle",
                "ce_strike": ce_df.iloc[-1]['strikePrice'],
                "pe_strike": pe_df.iloc[-1]['strikePrice'],
                "confidence": ce_df.iloc[-1]['confidence'] + pe_df.iloc[-1]['confidence'],
                "logic": "OTM CE + OTM PE for breakout"
            })

    elif strategy == "Covered Call":
        ce_df = df[df['optionType'] == 'CE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if not ce_df.empty:
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Covered Call",
                "sell_strike": ce_df.iloc[0]['strikePrice'],
                "confidence": ce_df.iloc[0]['confidence'],
                "logic": "Hold stock + sell CE"
            })

    elif strategy == "Protective Put":
        pe_df = df[df['optionType'] == 'PE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if not pe_df.empty:
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Protective Put",
                "buy_strike": pe_df.iloc[0]['strikePrice'],
                "confidence": pe_df.iloc[0]['confidence'],
                "logic": "Hold stock + buy PE"
            })

    elif strategy == "Call":
        ce_df = df[df['optionType'] == 'CE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if not ce_df.empty:
            best_ce = ce_df.iloc[0]
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Call",
                "strike": best_ce['strikePrice'],
                "confidence": best_ce['confidence'],
                "logic": "High OI CE near spot"
            })

    elif strategy == "Put":
        pe_df = df[df['optionType'] == 'PE'].sort_values(['distance', 'confidence'], ascending=[True, False])
        if not pe_df.empty:
            best_pe = pe_df.iloc[0]
            signals.append({
                "symbol": df['symbol'].iloc[0],
                "type": "Put",
                "strike": best_pe['strikePrice'],
                "confidence": best_pe['confidence'],
                "logic": "High OI PE near spot"
            })

    return signals
