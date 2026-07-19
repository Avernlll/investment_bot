import yfinance as yf
import pandas as pd
import time

tickers = ["AAPL", "AMZN", "GOOGL", "META", "MSFT"]
print("📊 Fetching fundamental data (one by one)...")

fundamental_data = []

for ticker in tickers:
    try:
        print(f"⏳ Fetching {ticker}...", end=" ", flush=True)
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info:
            print("⚠️ No data")
            continue
        
        fundamental_data.append({
            "Ticker": ticker,
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A"),
            "Forward EPS": info.get("forwardEps", "N/A"),
            "Market Cap (B)": info.get("marketCap", 0) / 1e9,
            "Revenue (B)": info.get("totalRevenue", 0) / 1e9,
            "Profit Margin (%)": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else "N/A",
            "Dividend Yield (%)": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else "N/A"
        })
        print("✅")
        
    except Exception as e:
        print(f"❌ Skipped: {e}")
        continue
    
    time.sleep(0.5)

df = pd.DataFrame(fundamental_data)

if df.empty:
    print("❌ No data fetched.")
    exit()

df_sorted = df.sort_values("P/E Ratio")
print("\n" + "="*80)
print("📋 FUNDAMENTAL COMPARISON (Cheapest to Most Expensive by P/E)")
print("="*80)
print(df_sorted.to_string(index=False))

df.to_csv("fundamental_data.csv", index=False)
print("\n💾 Saved to fundamental_data.csv")