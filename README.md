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
history, stock_name = analyze_stock('AMZN')
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
- [`pandas`](https://pypi.org/project/pandas/) – for data manipulation and time series analysis  
- [`numpy`](https://pypi.org/project/numpy/) – for numerical calculations  
- [`matplotlib`](https://pypi.org/project/matplotlib/) – optional static plotting  
- [`plotly`](https://pypi.org/project/plotly/) – for interactive visualizations  
- [`cufflinks`](https://pypi.org/project/cufflinks/) – connects Plotly with pandas  
- `datetime` – standard Python library for handling time ranges

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
