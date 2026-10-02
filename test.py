print("Hello, portfolio dashboard!")
import yfinance as yf
data = yf.download("AAPL", period="5d")
import yfinance as yf
tickers = ["AAPL", "MSFT", "GOOGL"]
data = yf.download(tickers, period="1y")["Close"]
returns = data.pct_change()
mean_returns = returns.mean()
volatility = returns.std()
correlation = returns.corr()
covariance = returns.cov()
import numpy as np
weights = np.random.random(3)
weights = weights / np.sum(weights)
portfolio_return = np.sum(mean_returns * weights)*252
portfolio_volatility = np.sqrt(weights @ covariance @ weights)*np.sqrt(252)
num_portfolios = 5000
results = []
for i in range (num_portfolios):
    weights = np.random.random(3)
    weights = weights / np.sum(weights)
    portfolio_return = np.sum(mean_returns * weights)*252
    portfolio_volatility = np.sqrt(weights @ covariance @ weights)*np.sqrt(252)
    results.append([portfolio_return, portfolio_volatility, weights[0], weights[1], weights[2]])
print(results[:5])
import pandas as pd
results_df = pd.DataFrame(results, columns=["Return", "Volatility", "Weight_AAPL", "Weight_MSFT", "Weight_GOOGL"])
print(results_df.head())
results_df["Sharpe"]= results_df["Return"] / results_df["Volatility"]
max_sharpe_portfolio = results_df.loc[results_df["Sharpe"].idxmax()]
print("max_sharpe_portfolio:", max_sharpe_portfolio)
import matplotlib.pyplot as plt
plt.scatter(results_df["Volatility"], results_df["Return"], c=results_df["Sharpe"], cmap="viridis")
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Volatility")
plt.ylabel("Return")
plt.title("Monte Carlo Simulation of Portfolio Optimization")
plt.scatter(max_sharpe_portfolio["Volatility"], max_sharpe_portfolio["Return"], color="red", marker="*", s=200)
plt.show()
