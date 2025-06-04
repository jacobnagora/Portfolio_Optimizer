# Portfolio Optimizer

This Python application performs historical stock analysis and visualization using data retrieved from Yahoo Finance. It is designed to help investors and analysts evaluate stock performance over time through statistical measures and interactive plots.

## Overview

The script supports the following features:

- Accepts multiple stock tickers in one run
- Allows users to assign asset classes to each ticker (Equity, Fixed Income, Alternative)
- Classifies assets by risk level (High, Low to Medium, Unknown)
- Fetches historical price data for each stock ticker
- Calculates:
  - Daily return percentages
  - Maximum and minimum daily returns
  - Mean and standard deviation of daily returns
  - Expected annual return
  - Annualized standard deviation
  - Beta relative to the S&P 500

## Usage

1. Clone the repository or download the source code.

2. Open the `Portfolio_Optimizer.py` file and run it:

3. Run the script using:

   `python Portfolio_Optimizer.py`

4. When prompted, enter one or more stock tickers, in any format if necessary)

5. For each ticker you enter, the script will ask you to specify the asset class. For example, for Apple stock:

   **What is the asset class for AAPL? [Equity / Fixed Income / Alternative]:**  
   `Equity`

   If you enter an invalid response, it will ask you again until a valid input is given.

6. After all tickers and asset classes are entered, the script will calculate and print the following for each stock:

   - The highest daily return to date
   - The worst daily return to date
   - The mean daily return
   - The standard deviation of daily returns
   - The expected annual return
   - The annualized standard deviation
   - The beta relative to the S&P 500
   - The assigned risk level based on asset class

## Dependencies

The project uses the following Python libraries:

- [`yfinance`](https://pypi.org/project/yfinance/) - for retrieving financial data from Yahoo Finance  
- [`numpy`](https://pypi.org/project/numpy/) - for numerical calculations  
- [`pandas`](https://pypi.org/project/pandas/) - for data manipulation and time series analysis  
- [`re`](https://docs.python.org/3/library/re.html) - for parsing user input

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
