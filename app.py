import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Portfolio Risk & Optimization Dashboard")
st.write("This app simulates 5,000 random portfolios from the stocks you enter, "
         "finds the mix with the best return per unit of risk (the highest Sharpe ratio), "
         "and compares it to the S&P 500.")
st.caption("Based on 5 years of daily data from Yahoo Finance. Past performance does not guarantee future results. Not financial advice.")
tickers_input = st.text_input("Enter stock tickers, separated by commas (e.g., AAPL, MSFT, GOOGL):")
tickers = tickers_input.split(",")
tickers = [t.strip().upper() for t in tickers]
if len(tickers) < 2:
    st.warning("Please enter at least 2 tickers to build a portfolio.")
    st.stop()
if st.button("Run Analysis"):
    data = yf.download(tickers, period="5y")["Close"]
    if data.empty:
        st.error("No data could be retrieved. Check your ticker symbols.")
        st.stop()

    invalid = [t for t in data.columns if data[t].isna().all()]
    if invalid:
        st.error(f"No data found for: {', '.join(invalid)}. Check the spelling.")
        st.stop()
    returns = data.pct_change()
    mean_returns = returns.mean()
    covariance = returns.cov()

    num_portfolios = 5000
    results = []
    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights = weights / np.sum(weights)
        portfolio_return = np.sum(mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(weights @ covariance @ weights) * np.sqrt(252)
        results.append([portfolio_return, portfolio_volatility]+list(weights))
    columns = ["Return", "Volatility"] + [f"{t} Weight" for t in tickers]
    results_df = pd.DataFrame(results, columns=columns)
    results_df["Sharpe"] = results_df["Return"] / results_df["Volatility"]

    max_sharpe_portfolio = results_df.loc[results_df["Sharpe"].idxmax()]

    st.subheader("Optimal Portfolio (Max Sharpe Ratio)")
    st.write(f"Expected annual return: {max_sharpe_portfolio['Return']:.2%}")
    st.write(f"Annual volatility: {max_sharpe_portfolio['Volatility']:.2%}")
    st.write(f"Sharpe ratio: {max_sharpe_portfolio['Sharpe']:.2f}")

    st.write("Recommended weights:")
    for t in tickers:
        st.write(f"{t}: {max_sharpe_portfolio[t + ' Weight']:.1%}")

    fig, ax = plt.subplots()
    scatter = ax.scatter(results_df["Volatility"], results_df["Return"], c=results_df["Sharpe"], cmap="viridis")
    ax.scatter(max_sharpe_portfolio["Volatility"], max_sharpe_portfolio["Return"], c="red", marker="*", s=200, label= "Max Sharpe Ratio")
    ax.set_xlabel("Volatility (Risk)")
    ax.set_ylabel("Return")
    ax.set_title("Monte Carlo Simulated Portfolios")
    fig.colorbar(scatter, label="Sharpe Ratio")
    st.pyplot(fig)
    sp500_data = yf.download("^GSPC", period="5y")["Close"]
    sp500_returns = sp500_data.pct_change()
    sp500_return = sp500_returns.mean().iloc[0] * 252
    sp500_volatility = sp500_returns.std().iloc[0] * np.sqrt(252)
    sp500_sharpe = sp500_return / sp500_volatility

    comparison = pd.DataFrame({
        "Return": [max_sharpe_portfolio["Return"], sp500_return],
        "Volatility": [max_sharpe_portfolio["Volatility"], sp500_volatility],
        "Sharpe": [max_sharpe_portfolio["Sharpe"], sp500_sharpe],
    }, index=["Optimal portfolio", "S&P 500"])

    st.write("Optimal portfolio vs. S&P 500")
    st.write(comparison)

                                   

