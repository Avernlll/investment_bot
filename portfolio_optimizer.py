import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

# ---------- 1. Load data ----------
tickers = ["AAPL", "AMZN", "GOOGL", "META", "MSFT"]
data = yf.download(tickers, start="2022-01-01", end="2025-01-01")["Close"]
data = data.dropna(axis=1, how='all')

# ---------- 2. Calculate returns and covariance ----------
returns = data.pct_change().dropna()
mean_returns = returns.mean()
cov_matrix = returns.cov()

# ---------- 3. Define optimization functions ----------
def portfolio_annualized_performance(weights, mean_returns, cov_matrix, trading_days=252):
    returns = np.sum(mean_returns * weights) * trading_days
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(trading_days)
    return returns, std

def negative_sharpe(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
    p_returns, p_std = portfolio_annualized_performance(weights, mean_returns, cov_matrix)
    return -(p_returns - risk_free_rate) / p_std

# ---------- 4. Find optimal weights (Max Sharpe) ----------
num_assets = len(tickers)
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for _ in range(num_assets))
initial_guess = num_assets * [1. / num_assets]

result = minimize(
    negative_sharpe,
    initial_guess,
    args=(mean_returns, cov_matrix),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights = result.x

# ---------- 5. Display results ----------
print("\n" + "="*60)
print("🎯 OPTIMAL PORTFOLIO (Maximum Sharpe Ratio)")
print("="*60)

for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight*100:.2f}%")

annual_return, annual_volatility = portfolio_annualized_performance(optimal_weights, mean_returns, cov_matrix)
sharpe_ratio = (annual_return - 0.02) / annual_volatility

print("\n📊 Portfolio Performance:")
print(f"Expected Annual Return: {annual_return*100:.2f}%")
print(f"Expected Annual Volatility: {annual_volatility*100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# ---------- 6. Save allocation to CSV ----------
pd.DataFrame({
    'Stock': tickers,
    'Allocation (%)': optimal_weights * 100
}).to_csv("optimal_allocation.csv", index=False)
print("\n💾 Saved allocation to optimal_allocation.csv")