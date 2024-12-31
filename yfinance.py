import yfinance from yf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    return stock_data

ticker = 'AAPL'
start_date = '2010-01-01'
end_date = '2020-01-01'

stock_data = get_stock_data(ticker, start_date, end_date)
print(stock_data.head())

plt.figure(figsize=(12, 6))
plt.plot(stock_data['Close'], label='Close Price')
plt.plot(stock_data['SMA_50'], label='SMA 50')
plt.plot(stock_data['SMA_200'], label='SMA 200')
plt.title('Stock Data')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
