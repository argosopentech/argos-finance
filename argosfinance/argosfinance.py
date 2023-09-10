import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def graph_market_data(ticker_symbol, start_date, end_date):
    # Fetch historical price data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Plot the closing price
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['Close'], label=f'{ticker_symbol} Closing Price')
    plt.title(f'{ticker_symbol} Closing Price History ({start_date} to {end_date})')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)

    # Show the plot in the Jupyter notebook
    plt.show()