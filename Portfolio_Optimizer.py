# Import key libraries and modules
import yfinance as yf
import numpy as np
import pandas as pd
import re

raw_input = input(f'What stock(s) would you like to evaluate? ').strip().upper()

ticker_symbols = re.findall(r'[A-Z\.]+', raw_input)

print(f'You entered tickers {ticker_symbols}.')

# Initialize dictionary to store user-defined asset classes
asset_classes = {}

# Define risk levels by asset class
risk_by_class = {
    'Equity': 'High',
    'Fixed Income': 'Low to Medium',
    'Alternative': 'High',
    'Unknown': 'Unknown'
}


# Define a function that analyzes the given stock(s)
def analyze_stocks(ticker_symbols):
    results = []
    # Fetch stock data and asset class
    for ticker in ticker_symbols:
        valid_classes = ['Equity', 'Fixed Income', 'Alternative']

        # Get asset class from user with validation
        while True:
            asset_class = asset_classes.get(ticker)
            if asset_class:
                break

            print(f"\nAsset class for {ticker} is not known.")
            user_input = input(f"What is the asset class for {ticker}? [Equity / Fixed Income / Alternative]: ").strip().title()

            if user_input in valid_classes:
                asset_class = user_input
                print(f'Confirming that the asset class for {ticker} is {asset_class}')
                break
            else:
                print(f"Invalid input: '{user_input}' is not a valid asset class. Please enter 'Equity', 'Fixed Income', or 'Alternative'.")

        # Save the validated asset class
        asset_classes[ticker] = asset_class
        risk_level = risk_by_class[asset_class]
    
        try:
            stock = yf.Ticker(ticker)
            info = stock.info  # This will fail if the ticker is invalid
            if 'longName' not in info or info.get('regularMarketPrice') is None:
                print(f"{ticker} is invalid or inactive.")
                continue
            history = stock.history(period="max")
            if history.empty:
                print(f"{ticker} has no historical data.")
                continue

            stock_name = info.get('longName') or ticker

            # Round for user readability
            history_reset = history.reset_index()
            cols_to_round = ['Open', 'High', 'Low', 'Close', 'Volume']
            history_reset[cols_to_round] = history_reset[cols_to_round].round(2)

            # Calculate and print summary info
            history['% Daily Return'] = history['Close'].pct_change(1) * 100
            history['% Daily Return'] = history['% Daily Return'].fillna(0)
            print(f'The highest daily return of {stock_name} to date was {round(history["% Daily Return"].max(), 2)}%.')
            print(f'The worst daily return of {stock_name} to date was {round(history["% Daily Return"].min(), 2)}%.')
            stock_mean = history['% Daily Return'].mean().round(2)
            print(f"The mean return of {stock_name} is {stock_mean}%.")
            stock_std_dev = round(history['% Daily Return'].std(), 2)
            print(f'The current standard deviation of {stock_name} is {stock_std_dev}%.')
            
            # Save this stock's result
            history_reset['% Daily Return'] = history['% Daily Return'].values
            results.append((history_reset, stock_name))


        except Exception as e:
            print(f"Error with {ticker}: {e}")
            continue
    return results

results = analyze_stocks(ticker_symbols)


# Define a function that identifies the best possible combination of a portfolio of random stocks
# 	1.	Gather data: Collect historical returns, calculate expected returns, standard deviations, and betas for each of the ten stocks.

# Define a function to calculate expected return, standard deviation, and beta for each stock
def gather_portfolio_metrics(results):
    portfolio_data = []

    # Define the market index for beta calculation
    market_ticker = '^GSPC'
    market = yf.Ticker(market_ticker)
    market_hist = market.history(period="max")['Close'].pct_change().dropna()

    for history_df, stock_name in results:
        try:
            # Ensure 'Date' is in datetime format and set as index
            history_df['Date'] = pd.to_datetime(history_df['Date'])
            history_df.set_index('Date', inplace=True)

            # Convert daily return from % to decimal
            stock_returns = history_df['% Daily Return'] / 100

            # Align with market data
            aligned_returns = pd.concat([stock_returns, market_hist], axis=1, join='inner')
            aligned_returns.columns = ['stock_return', 'market_return']

            # Calculate beta using covariance / variance
            covariance = np.cov(aligned_returns['stock_return'], aligned_returns['market_return'])[0, 1]
            market_variance = np.var(aligned_returns['market_return'])
            beta = covariance / market_variance

            # Calculate expected return (annualized) and standard deviation (annualized)
            expected_return = stock_returns.mean() * 252
            std_dev = stock_returns.std() * np.sqrt(252)

            # Store the results in a dictionary
            stock_metrics = {
                'Name': stock_name,
                'Expected Return (%)': round(expected_return * 100, 2),
                'Standard Deviation (%)': round(std_dev * 100, 2),
                'Beta': round(beta, 3)
            }

            portfolio_data.append(stock_metrics)

        except Exception as e:
            print(f"Error calculating metrics for {stock_name}: {e}")
            continue

    return portfolio_data

# Analyze the tickers and calculate metrics
results = analyze_stocks(ticker_symbols)
portfolio_metrics = gather_portfolio_metrics(results)

# Display the results
for metric in portfolio_metrics:
    print(f"\nStock: {metric['Name']}")
    print(f"Expected Return: {metric['Expected Return (%)']}%")
    print(f"Standard Deviation: {metric['Standard Deviation (%)']}%")
    print(f"Beta: {metric['Beta']}")

#	2.	Construct portfolios: Generate all possible combinations of these stocks. Focus on combinations with different weights rather than every single combination, since the number of combinations grows exponentially.
#	3.	Evaluate: For each combination, calculate the portfolio’s expected return and standard deviation, and use betas to understand the systematic risk.
#	4.	Identify the efficient frontier.
#	5.	Select the superior combination: Depending on criteria—like the highest Sharpe ratio, the minimum variance, or a target beta.
