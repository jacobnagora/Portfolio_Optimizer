# Portfolio Optimizer

This Python application performs historical stock analysis and visualization using data retrieved from Yahoo Finance. It is designed to help investors and analysts evaluate stock performance over time through statistical measures and interactive plots.

## Overview

The script supports the following features:

- Fetches historical price data for a specified stock ticker
- Calculates:
  - Daily return percentages
  - Maximum and minimum daily returns
  - Mean and standard deviation of daily returns
- Produces interactive time series charts for:
  - Daily returns (%)
  - Daily high prices
  - Daily low prices

## Usage

1. Clone the repository or download the source code.

2. Open the `Portfolio_Optimizer.py` file and modify the ticker symbol:

```python
history, stock_name = analyze_stock('**_AMZN_**')
```

3. Run the script:

```bash
python Portfolio_Optimizer.py
```

4. Three interactive HTML charts will open in your default web browser:
   - Daily return chart
   - Daily high price chart
   - Daily low price chart

## Dependencies

The project uses the following Python libraries:
- [`yfinance`](https://pypi.org/project/yfinance/) – for retrieving financial data from Yahoo Finance  
- [`plotly`](https://pypi.org/project/plotly/) – for interactive visualizations using `graph_objects`  
- [`datetime`](https://docs.python.org/3/library/datetime.html) – standard Python library for handling date and time  
- [`sys`](https://docs.python.org/3/library/sys.html) – standard Python library for interacting with the system (e.g., exiting on error)

## Notes
- This script requires an internet connection to fetch data from Yahoo Finance.
- If an invalid ticker is entered, the script will terminate with an error message.
- Charts will automatically open in your browser once generated.
- The script uses a start date of "1900-01-01" to capture the full available history of the security.
  
## License

This project is licensed under the MIT License. 
