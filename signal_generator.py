import pandas as pd
import numpy as np

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_signal(ticker, prices_df, fundamentals_df):
    """
    Returns: signal (BUY/HOLD/SELL), score (int), reasoning (list of strings)
    """
    # 1. Extract price data
    if ticker not in prices_df.columns:
        return "HOLD", 0, ["No price data"]
    
    close_prices = prices_df[ticker].dropna()
    if len(close_prices) < 50:
        return "HOLD", 0, ["Insufficient data (need 50 days)"]
    
    # 2. Technical Indicators
    sma_50 = close_prices.rolling(50).mean().iloc[-1]
    current_price = close_prices.iloc[-1]
    rsi = calculate_rsi(close_prices).iloc[-1]
    
    # 3. Fundamentals
    fund = fundamentals_df[fundamentals_df['Ticker'] == ticker]
    if not fund.empty:
        pe = fund.iloc[0]['P/E Ratio']
        if isinstance(pe, str):
            pe = float(pe) if pe != 'N/A' else 30.0
        profit_margin = fund.iloc[0]['Profit Margin (%)']
        if isinstance(profit_margin, str):
            profit_margin = float(profit_margin) if profit_margin != 'N/A' else 10.0
    else:
        pe = 30.0
        profit_margin = 10.0
    
    # 4. Scoring System (0 to 4)
    score = 0
    reasoning = []
    
    # Price above 50-day SMA (trend is up)
    if current_price > sma_50:
        score += 1
        reasoning.append(f"Price (${current_price:.2f}) > 50-day SMA (${sma_50:.2f})")
    else:
        reasoning.append(f"Price (${current_price:.2f}) < 50-day SMA (${sma_50:.2f})")
    
    # RSI (momentum)
    if rsi < 30:
        score += 1
        reasoning.append(f"Oversold (RSI = {rsi:.1f})")
    elif rsi > 70:
        score -= 1
        reasoning.append(f"Overbought (RSI = {rsi:.1f})")
    else:
        reasoning.append(f"Neutral RSI ({rsi:.1f})")
    
    # P/E Ratio (value)
    if pe < 25:
        score += 1
        reasoning.append(f"P/E ({pe:.1f}) < 25 (cheap)")
    else:
        reasoning.append(f"P/E ({pe:.1f}) >= 25 (expensive)")
    
    # Profit Margin (quality)
    if profit_margin > 20:
        score += 1
        reasoning.append(f"Profit Margin ({profit_margin:.1f}%) > 20% (good)")
    else:
        reasoning.append(f"Profit Margin ({profit_margin:.1f}%) < 20% (okay)")
    
    # 5. Final Decision
    if score >= 3:
        signal = "BUY"
    elif score <= 0:
        signal = "SELL"
    else:
        signal = "HOLD"
    
    return signal, score, reasoning