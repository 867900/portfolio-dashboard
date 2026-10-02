# Portfolio Risk & Optimization Dashboard

A Streamlit web app that simulates thousands of random stock portfolios, finds the one with the best risk-adjusted return (highest Sharpe ratio), and compares it to the S&P 500.

**Live app:** https://portfolio-risk-dashboard01.streamlit.app

## What it does

1. Takes a list of stock tickers from the user (e.g. `AAPL, MSFT, GOOGL`)
2. Pulls 5 years of historical price data from Yahoo Finance
3. Calculates each stock's daily returns, volatility, and the covariance between them
4. Runs a Monte Carlo simulation: generates 5,000 random portfolio weightings, and calculates the annualized return and volatility of each
5. Identifies the portfolio with the highest Sharpe ratio (best return per unit of risk)
6. Plots all simulated portfolios on a risk/return scatter chart (the efficient frontier), highlighting the optimal one
7. Compares the optimal portfolio's return, volatility, and Sharpe ratio against simply holding the S&P 500 over the same period

## Tech stack

- **Python**
- **pandas / numpy** — data handling and the Monte Carlo / portfolio math
- **yfinance** — fetching real market data
- **matplotlib** — the risk/return scatter chart
- **Streamlit** — the web interface and deployment

## Why this project

Built to learn Python from the ground up (loops, functions, pandas, numpy) while applying concepts from Modern Portfolio Theory (Markowitz efficient frontier, Sharpe ratio) studied in my finance coursework at WU Vienna.

## Limitations (known, and worth knowing)

- **Sharpe ratio assumes a 0% risk-free rate.** A more complete version would subtract the current risk-free rate (e.g. T-bill yield) from returns before dividing by volatility.
- **The comparison to the S&P 500 is in-sample.** The optimal portfolio is chosen using the same 5-year window it's then compared against, so it has a built-in advantage — this isn't a predictive backtest.
- **No transaction costs, taxes, or rebalancing** are modeled.
- Past performance shown here does not indicate future results. This is a learning project, not investment advice.

## Possible future improvements

- Out-of-sample backtesting: pick weights using one period, test them on a later, unseen period
- Add a risk-free rate input for a more accurate Sharpe ratio
- Track the chosen portfolio's real performance going forward (paper trading)

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```