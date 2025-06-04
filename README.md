# Portfolio Optimizer

A Python-based portfolio analytics tool that applies Modern Portfolio Theory to construct and visualize optimal portfolios using real-time data from Yahoo Finance. It calculates risk-adjusted metrics like the Sharpe ratio and compares your optimized portfolio to SPY.

## Overview

This application allows users to:

* Input multiple stock tickers
* Calculate performance metrics for each asset:

  * Daily returns
  * Annualized return and standard deviation
  * Beta (vs. S\&P 500)
  * Sharpe ratio (based on a user-defined risk-free rate)
* Simulate thousands of random portfolio weight combinations to:

  * Maximize the Sharpe ratio
  * Identify optimal weights
  * Compare portfolio performance against SPY
* Visualize results via interactive Plotly charts:

  * **Risk vs. Return plot** — highlighting each asset and the optimized portfolio
  * **Portfolio vs. SPY performance** — showing relative growth over time
* Export results to auto-generated HTML reports

## Usage

1. Clone the repository or download the source code.

2. Open the `Portfolio_Optimizer.py` file and run the script:

   ```bash
   python Portfolio_Optimizer.py
   ```

3. When prompted:

   * Enter one or more stock tickers (e.g., `AMZN MSFT TSLA`)
   * Specify your total initial investment (e.g., `100000`)
   * Enter your expected market return (e.g., `0.08` for 8%)
   * Enter your risk-free rate (e.g., `0.03` for 3%)

4. After collecting inputs, the script will:

   * Fetch historical data for each ticker from Yahoo Finance
   * Calculate daily returns, annualized return and volatility, beta, and Sharpe ratio
   * Run thousands of portfolio simulations to maximize the Sharpe ratio
   * Identify the optimal weights and allocations for your portfolio
   * Compare its performance to SPY
   * Display a terminal summary with expected return, risk, Sharpe ratio, weights, and dollar allocations
   * Generate and automatically open two interactive HTML charts in your default browser:

     * `risk_return_report.html`
     * `portfolio_vs_spy_report.html`

## Output Example

* **Risk vs. Return Plot**
  Bubble chart showing each asset’s volatility, expected return, and Sharpe ratio — plus a highlighted point for the optimized portfolio.

* **Performance vs. SPY**
  Line chart comparing the optimized portfolio’s growth over time to the S\&P 500.

* **Console Output**
  Sharpe ratios, expected returns, volatilities, optimal weights, and dollar allocations are neatly displayed for quick analysis.

## Dependencies

This project uses the following Python libraries:

* [`yfinance`](https://pypi.org/project/yfinance/) – for retrieving stock and ETF data
* [`pandas`](https://pypi.org/project/pandas/) – for data handling and manipulation
* [`numpy`](https://pypi.org/project/numpy/) – for numerical operations and portfolio math
* [`plotly`](https://pypi.org/project/plotly/) – for interactive data visualizations
* [`re`](https://docs.python.org/3/library/re.html) – for parsing ticker symbols from user input
* [`os`](https://docs.python.org/3/library/os.html) – for launching HTML reports in the browser

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.