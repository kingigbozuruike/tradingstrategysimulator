import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    return stock_data

def generate_signals(stock_data):
    stock_data['Signal'] = 0
    stock_data.loc[stock_data['SMA_50'] > stock_data['SMA_200'], 'Signal'] = 1
    stock_data.loc[stock_data['SMA_50'] <= stock_data['SMA_200'], 'Signal'] = -1
    stock_data['Position'] = stock_data['Signal'].diff()

    stock_data['Buy Signal'] = (stock_data['Position'] == 2)
    stock_data['Sell Signal'] = (stock_data['Position'] == -2)
    
    return stock_data

ticker = 'AAPL'
start_date = '2010-01-01'
end_date = '2020-01-01'

stock_data = get_stock_data(ticker, start_date, end_date)
stock_data = generate_signals(stock_data)



plt.figure(figsize=(14, 7))
plt.plot(stock_data['Close'], label='Close Price', alpha=0.7)
plt.plot(stock_data['SMA_50'], label='SMA 50', linestyle='--')
plt.plot(stock_data['SMA_200'], label='SMA 200', linestyle='--')


buy_signals = stock_data[stock_data['Buy Signal']]
sell_signals = stock_data[stock_data['Sell Signal']]

# debug buy/sell signals
print(f"Buy Signals: {len(buy_signals)}")
print(f"Sell Signals: {len(sell_signals)}")


plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', alpha=1)
plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', alpha=1)


plt.title(f"{ticker} Trading Strategy")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
