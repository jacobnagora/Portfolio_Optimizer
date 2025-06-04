# Import key libraries and modules
import yfinance as yf
import numpy as np
import pandas as pd
import re
import plotly.express as px
import os

# User input for stock ticker(s) and initial investment outlay
raw_input = input("Enter stock ticker(s) (in any format, if necessary): ").strip().upper()
ticker_symbols = re.findall(r'[A-Z\.]+', raw_input)

print("\nInitial Investment:")
while True:
    try:
        initial_investment = float(input("  What is your initial investment outlay? (e.g., 100000): ").replace(',', ''))
        break
    except ValueError:
        print("  Please enter a valid number.")

# Define a function that analyzes the given stock(s)
def analyze_stocks(ticker_symbols):
    results = []
    for ticker in ticker_symbols:
        ticker = ticker.upper()
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="max")
            if history.empty or history.shape[0] < 100:  # Require at least ~100 days of data to run
                print(f"{ticker} is invalid or lacks sufficient data.")
                continue

            stock_name = ticker
            try:
                info = stock.info
                stock_name = info.get('longName', ticker)
            except:
                pass

            # Round for user readability
            history_reset = history.reset_index()
            cols_to_round = ['Open', 'High', 'Low', 'Close', 'Volume']
            history_reset[cols_to_round] = history_reset[cols_to_round].round(2)

            # Add % Daily Return
            history_reset['% Daily Return'] = history['Close'].pct_change() * 100

            results.append((history_reset, stock_name, ticker))

        except Exception as e:
            print(f"\n{ticker} is invalid or inactive and was skipped.")
            continue

    return results

results = analyze_stocks(ticker_symbols)

# Define price_scaling()
def price_scaling(df):
    scaled_df = df.copy()
    for col in scaled_df.columns[1:]:
        scaled_df[col] = pd.to_numeric(scaled_df[col], errors='coerce')
        scaled_df[col] = scaled_df[col] / scaled_df[col].iloc[0]
    return scaled_df

# Merge all historical returns into one DataFrame
merged_df = pd.DataFrame()
for df, name, ticker in results:
    df = df[['Date', 'Close']].copy()
    df.rename(columns={'Close': name}, inplace=True)
    if merged_df.empty:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on='Date', how='inner')

# Optimize portfolio using Sharpe ratio
def optimize_portfolio(df, num_portfolios=10_000, risk_free_rate=0.02):
    returns = df.iloc[:, 1:].pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252

    results = []
    for _ in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        expected_return = np.dot(weights, mean_returns)
        std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (expected_return - risk_free_rate) / std_dev
        results.append((weights, expected_return, std_dev, sharpe_ratio))

    best = max(results, key=lambda x: x[3])
    weights, ret, std, sharpe = best
    return [float(w) for w in weights], ret, std, sharpe

# Asset allocation function
def asset_allocation(df, weights, initial_investment):
    portfolio_df = df.copy()
    scaled_df = price_scaling(df)
    for i, stock in enumerate(scaled_df.columns[1:]):
        portfolio_df[stock] = scaled_df[stock] * weights[i] * initial_investment
    portfolio_df['Portfolio Value'] = portfolio_df.iloc[:, 1:].sum(axis=1)
    portfolio_df['Portfolio Daily Return'] = portfolio_df['Portfolio Value'].pct_change() * 100
    portfolio_df.fillna(0, inplace=True)
    return portfolio_df

# Gather stock metrics
def gather_portfolio_metrics(results, expected_market_return, risk_free_rate):
    portfolio_data = []

    # Define the market index for beta calculation
    market_ticker = '^GSPC'
    market = yf.Ticker(market_ticker)
    market_hist = market.history(period="max")['Close'].pct_change().dropna()
    market_hist.index = pd.to_datetime(market_hist.index)

    for history_df, stock_name, ticker in results:
        try:
            history_df['Date'] = pd.to_datetime(history_df['Date'])
            history_df.set_index('Date', inplace=True)

            stock_returns = history_df['Close'].pct_change().dropna()
            stock_returns = pd.to_numeric(stock_returns, errors='coerce').dropna()
            stock_returns.index = stock_returns.index.tz_localize(None)

            aligned_returns = pd.concat([stock_returns, market_hist], axis=1, join='inner')
            aligned_returns.columns = ['stock_return', 'market_return']
            aligned_returns.dropna(inplace=True)

            if aligned_returns.shape[0] >= 50:
                covariance = np.cov(aligned_returns['stock_return'], aligned_returns['market_return'])[0, 1]
                market_variance = np.var(aligned_returns['market_return'])
                beta = covariance / market_variance
            else:
                info = yf.Ticker(ticker).info
                beta = info.get('beta', np.nan)

            if beta is None or np.isnan(beta):
                raise ValueError("Beta unavailable for CAPM calculation")

            expected_return = risk_free_rate + beta * (expected_market_return - risk_free_rate)
            std_dev = stock_returns.std() * np.sqrt(252)
            sharpe_ratio = (expected_return - risk_free_rate) / std_dev

            stock_metrics = {
                'Name': stock_name,
                'Expected Return (%)': round(expected_return * 100, 2),
                'Standard Deviation (%)': round(std_dev * 100, 2),
                'Sharpe Ratio': round(sharpe_ratio, 3)
            }

        except Exception as e:
            print(f"Skipped {stock_name} due to error: {e}")
            stock_metrics = {
                'Name': stock_name,
                'Expected Return (%)': float('nan'),
                'Standard Deviation (%)': float('nan'),
                'Sharpe Ratio': float('nan')
            }

        portfolio_data.append(stock_metrics)

    return portfolio_data

# Run the optimizer
best_weights, best_return, best_std, best_sharpe = optimize_portfolio(merged_df)

# Prompt user for CAPM inputs
expected_market_return = float(input("Enter the expected market return (e.g., 0.08 for 8%): "))
risk_free_rate = float(input("Enter the risk-free rate (e.g., 0.02 for 2%): "))

portfolio_metrics = gather_portfolio_metrics(results, expected_market_return, risk_free_rate)
for i, metric in enumerate(portfolio_metrics):
    metric['Optimal Weight (%)'] = round(best_weights[i] * 100, 2)

# Build DataFrame for plotting
risk_return_df = pd.DataFrame(portfolio_metrics)
risk_return_df['Expected Return'] = risk_return_df['Expected Return (%)'] / 100
risk_return_df['Std Dev'] = risk_return_df['Standard Deviation (%)'] / 100
risk_return_df['Weight'] = risk_return_df['Optimal Weight (%)'] / 100

# Drop rows with missing values
risk_return_df.dropna(subset=['Expected Return', 'Std Dev'], inplace=True)

# Compute each stock’s individual Sharpe Ratio = (E[R] - R_f) / σ
risk_return_df['Sharpe Ratio'] = (
    (risk_return_df['Expected Return'] - risk_free_rate) / risk_return_df['Std Dev']
).round(3)

# Add the optimized-portfolio “point” at the bottom of the same DF
portfolio_point = {
    'Name': 'Optimized Portfolio',
    'Expected Return': best_return,
    'Std Dev': best_std,
    'Weight': 1.0,  # full portfolio
    'Expected Return (%)': best_return * 100,
    'Standard Deviation (%)': best_std * 100,
    'Optimal Weight (%)': 100.0,
    'Sharpe Ratio': round((best_return - risk_free_rate) / best_std, 3)
}
risk_return_df = pd.concat([risk_return_df, pd.DataFrame([portfolio_point])], ignore_index=True)

# Construct a dynamic title that includes assumptions
title_str = (
    f"Risk vs. Return (Portfolio Size: ${initial_investment:,.0f}, "
    f"Risk‐Free Rate: {risk_free_rate * 100:.2f}%, "
    f"Market Return: {expected_market_return * 100:.2f}%)"
)

fig1 = px.scatter(
    risk_return_df,
    x='Std Dev',
    y='Expected Return',
    size='Weight',
    color='Name',
    hover_name='Name',
    hover_data={
        'Sharpe Ratio': True,
        'Weight': ':.2%',
        'Expected Return': ':.2%',
        'Std Dev': ':.2%'
    },
    title=title_str,
    labels={
        'Std Dev': 'Volatility (Std Dev)',
        'Expected Return': 'Expected Return'
    },
    width=900,
    height=600
)

# Make the “Optimized Portfolio” marker stand out with a black outline
fig1.update_traces(
    marker=dict(line=dict(width=2, color='black')),
    selector=dict(name='Optimized Portfolio')
)

# Save & launch the risk vs. return HTML
report1 = "risk_return_report.html"
fig1.write_html(report1, include_plotlyjs="cdn", full_html=True)
os.system(f"open {report1}")


# Simulate portfolio overt time compared to SPY

# (a) We already have `merged_df` containing daily closes for each stock
# (b) Compute the daily portfolio value (scaled_i * weight_i * initial_investment)
def asset_allocation(df, weights, initial_investment):
    portfolio_df = df.copy()
    scaled_df = price_scaling(df)
    for i, stock in enumerate(scaled_df.columns[1:]):
        portfolio_df[stock] = scaled_df[stock] * weights[i] * initial_investment
    portfolio_df['Portfolio Value'] = portfolio_df.iloc[:, 1:].sum(axis=1)
    portfolio_df.fillna(method='ffill', inplace=True)
    return portfolio_df

optimal_df = asset_allocation(merged_df, best_weights, initial_investment) 
# `optimal_df` now has a column 'Portfolio Value' for each date

# (c) Download SPY for the same date range
spy = yf.Ticker("SPY").history(period="max")['Close']
spy = spy.loc[optimal_df['Date'].min(): optimal_df['Date'].max()]
spy = spy.to_frame(name='SPY Close')
spy['SPY Value'] = (spy['SPY Close'] / spy['SPY Close'].iloc[0]) * initial_investment

# (d) Combine portfolio & SPY into one plotting DataFrame
compare_df = pd.DataFrame({
    'Date': optimal_df['Date'],
    'Portfolio Value': optimal_df['Portfolio Value']
})
compare_df = compare_df.set_index('Date').join(spy['SPY Value'], how='inner').reset_index()

# (e) Plot Engine
fig2 = px.line(
    compare_df,
    x='Date',
    y=['Portfolio Value', 'SPY Value'],
    labels={'value':'Portfolio Value', 'variable':'Asset'},
    title="Optimized Portfolio vs. SPY Over Time",
    width=900,
    height=500
)

# Save & launch the portfolio vs. SPY HTML
report2 = "portfolio_vs_spy_report.html"
fig2.write_html(report2, include_plotlyjs="cdn", full_html=True)
os.system(f"open {report2}")

# Print outputs with Sharpes

print("\n------------------------------------------------------------")
print("Optimal Portfolio Allocation (Max Sharpe Ratio):\n")
for name, weight in zip(merged_df.columns[1:], best_weights):
    print(f"   {name:<25} → {round(weight * 100, 2)}%")

print(f"\n   Expected Annual Return  : {round(best_return * 100, 2)}%")
print(f"   Portfolio Std Dev       : {round(best_std * 100, 2)}%")
print(f"   Sharpe Ratio            : {round(best_sharpe, 3)}")
print("------------------------------------------------------------\n")

print("Detailed Metrics by Stock:\n")
for metric in portfolio_metrics:
    # compute each stock’s Sharpe ratio again (just for printing)
    er = metric['Expected Return (%)'] / 100
    sd = metric['Standard Deviation (%)'] / 100
    sr = ((er - risk_free_rate) / sd) if not np.isnan(er) and not np.isnan(sd) else float('nan')
    print(f"Stock: {metric['Name']}")
    print(f"   - Expected Return   : {metric['Expected Return (%)']}%")
    print(f"   - Std Deviation     : {metric['Standard Deviation (%)']}%")
    print(f"   - Sharpe Ratio      : {sr:.3f}")
    print(f"   - Optimal Weight    : {metric['Optimal Weight (%)']}%")
    allocation = (metric['Optimal Weight (%)'] / 100) * initial_investment
    print(f"   - Dollar Allocation : ${allocation:,.2f}\n")