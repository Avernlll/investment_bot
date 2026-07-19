import yfinance as yf
import time

# ---------- Test with a single stock ----------
ticker = "AAPL"
print(f"O Fetching data for {ticker}...")

try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # Print just the key metrics
    print(f"✅ Ticker: {ticker}")
    print(f"   P/E Ratio: {info.get('trailingPE', 'N/A')}")
    print(f"   PEG Ratio: {info.get('pegRatio', 'N/A')}")
    print(f"   EPS (TTM): {info.get('trailingEps', 'N/A')}")
    print(f"   Market Cap (B): {info.get('marketCap', 0) / 1e9:.2f} B")
    print(f"   Profit Margin: {info.get('profitMargins', 0) * 100:.2f}%")

except Exception as e:
    print(f"❌ Error: {e}") 