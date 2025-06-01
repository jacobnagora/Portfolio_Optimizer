# Import key libraries and modules

import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime as dt
import cufflinks as cf

# Define a function that analyzes the given stock
def analyze_stock(ticker_symbol):
    # Configuration
    ticker_symbol = ticker_symbol # Select your stock to evaluate

    # Fetch stock data
    stock = yf.Ticker(ticker_symbol)
    stock_name = stock.info.get('longName', ticker_symbol)
    # history = stock.history(start="1997-05-15", end=dt.datetime.today().strftime('%Y-%m-%d'))
    history = stock.history(start="2017-07-14", end="2022-12-16")
    
    # Round for user readability
    history_reset = history.reset_index()
    cols_to_round = ['Open', 'High', 'Low', 'Close', 'Volume']
    history_reset[cols_to_round] = history_reset[cols_to_round].round(2)

    # Calculate performance metrics and statistics
    # Calculate percentage daily returns since inception
    history['% Daily Return'] = history['Close'].pct_change(1) * 100
    history['% Daily Return'] = history['% Daily Return'].fillna(0)
    # Calculate the highest percentage daily return
    print(f'The highest daily return of {stock_name} to date was {history["% Daily Return"].max().round(2)}%.')
    # Calculate the lowest percentage daily return 
    print(f'The worst daily return of {stock_name} to date was {history["% Daily Return"].min().round(2)}%.')
    # Calculate the stock mean return
    stock_mean = history['% Daily Return'].mean().round(2)
    print(f"The mean return of {stock_name} is {stock_mean}%.")
    # Calculate the stock standard deviation
    stock_std_dev = history['% Daily Return'].std().round(2)
    print(f'The current standard deviation of {stock_name} is {stock_std_dev}%.')
    return history.reset_index(), stock_name

# Define a function that plots the daily stock price return % 
def plot_daily_return(df, stock_name):

    # Initialize the figure
    fig = go.Figure()

    # Add line trace for % Daily Return
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['% Daily Return'],
        mode='lines',
        name='% Daily Return'
    ))

    # Update layout styling
    fig.update_layout(
        title=f"{stock_name} - Daily Return (%) Over Time",
        xaxis_title='Date',
        yaxis_title='Daily Return (%)',
        plot_bgcolor='white',
        title_font=dict(size=22),
        font=dict(size=14),
        hovermode='x unified'
    )

    # Show the chart (opens in browser)
    fig.write_html("daily_return_chart.html", auto_open=True)

# Define a function that plots the daily high price
def plot_daily_high(df, stock_name):
    # Initialize the figure
    fig = go.Figure()

    # Add line trace for Daily High
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['High'],
        mode='lines',
        name='High'
    ))

    # Update layout styling
    fig.update_layout(
        title=f"{stock_name} - Daily High Over Time",
        xaxis_title='Date',
        yaxis_title='High',
        plot_bgcolor='white',
        title_font=dict(size=22),
        font=dict(size=14),
        hovermode='x unified'
    )

    # Show the chart (opens in browser)
    fig.write_html("daily_high_chart.html", auto_open=True)

# Define a function that plots the daily low price
def plot_daily_low(df, stock_name):
    # Initialize the figure
    fig = go.Figure()

    # Add line trace for Daily High
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Low'],
        mode='lines',
        name='High'
    ))

    # Update layout styling
    fig.update_layout(
        title=f"{stock_name} - Daily Low Over Time",
        xaxis_title='Date',
        yaxis_title='Low',
        plot_bgcolor='white',
        title_font=dict(size=22),
        font=dict(size=14),
        hovermode='x unified'
    )

    # Show the chart (opens in browser)
    fig.write_html("daily_low_chart.html", auto_open=True)


history, stock_name = analyze_stock('AMZN')
plot_daily_return(history, stock_name)
plot_daily_high(history, stock_name)
plot_daily_low(history, stock_name)
