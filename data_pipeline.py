import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# ---------- 1. Download data for multiple stocks ----------
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA"]
print(f"📥 Downloading data for: {', '.join(tickers)}")

data = yf.download(tickers, start="2022-01-01", end="2025-01-01")["Close"]

# Check for missing data and drop empty columns
data = data.dropna(axis=1, how='all')

print(f"✅ Loaded data for {data.shape[1]} stocks, {data.shape[0]} days")

# ---------- 2. Show basic statistics ----------
print("\n📊 Latest Prices (MNT equivalent if you want):")
print(data.tail(3))

# ---------- 3. Calculate daily returns ----------
returns = data.pct_change().dropna()
print(f"\n📈 Average Daily Return (%):")
print((returns.mean() * 100).round(2))

print(f"\n📉 Volatility (Std Dev of Daily Returns %):")
print((returns.std() * 100).round(2))

# ---------- 4. Calculate correlation between stocks ----------
print("\n🔗 Correlation Matrix (Top 5 stocks):")
print(returns.corr().round(2).head())

# ---------- 5. Save data to CSV ----------
data.to_csv("stock_prices.csv")
print("\n💾 Saved data to stock_prices.csv")

# ---------- 6. Quick plot ----------
plt.figure(figsize=(12, 6))
for ticker in data.columns:
    # Normalize to 100% for comparison
    normalized = data[ticker] / data[ticker].iloc[0] * 100
    plt.plot(normalized, label=ticker)

plt.title("Stock Performance Comparison (2022-2025)")
plt.xlabel("Date")
plt.ylabel("Normalized Price (Start = 100)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("stock_performance.png")
print("📊 Saved plot to stock_performance.png")
plt.show()

print("\n✅ Pipeline complete! Check stock_prices.csv and stock_performance.png")