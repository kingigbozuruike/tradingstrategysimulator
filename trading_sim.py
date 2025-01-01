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


def backtest_strategy(stock_data, initial_cash=100000):
    cash = initial_cash
    shares = 0
    portfolio_value = []
    
    # Loop through each row of stock data
    for date, row in stock_data.iterrows():
        # If Buy signal and enough cash to buy shares
        if row['Buy Signal'].item():  # Convert Buy Signal to a scalar
            if cash >= row['Close'].item():  # Ensure Close is a scalar value
                shares_to_buy = cash // row['Close'].item()
                cash -= shares_to_buy * row['Close'].item()
                shares += shares_to_buy
        
        # If Sell signal and have shares to sell
        if row['Sell Signal'].item():  # Convert Sell Signal to a scalar
            if shares > 0:
                cash += shares * row['Close'].item()
                shares = 0
        
        # Track portfolio value (cash + value of shares held)
        portfolio_value.append(cash + shares * row['Close'].item())
    
    # Add the portfolio value to the stock_data dataframe
    stock_data['Portfolio Value'] = portfolio_value
    stock_data['Cash'] = cash
    stock_data['Shares'] = shares
    return stock_data


# Define the stock ticker, start and end dates
ticker = input("Enter the stock ticker (e.g., 'AAPL', 'GOOG'): ").upper()
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
initial_cash = float(input("Enter the initial cash amount for backtest: "))

# fetch and generate signals
stock_data = get_stock_data(ticker, start_date, end_date)
stock_data = generate_signals(stock_data)

# backtest strategy
stock_data = backtest_strategy(stock_data)

# Plotting the results in two subplots
fig, ax = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Plot 1: Stock price with SMAs and buy/sell signals
ax[0].plot(stock_data['Close'], label='Close Price', alpha=0.7)
ax[0].plot(stock_data['SMA_50'], label='SMA 50', linestyle='--')
ax[0].plot(stock_data['SMA_200'], label='SMA 200', linestyle='--')

buy_signals = stock_data[stock_data['Buy Signal']]
sell_signals = stock_data[stock_data['Sell Signal']]

ax[0].scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', alpha=1)
ax[0].scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', alpha=1)

ax[0].set_title(f"{ticker} Trading Strategy")
ax[0].set_ylabel('Price')
ax[0].legend()

# Plot 2: Portfolio value over time
ax[1].plot(stock_data['Portfolio Value'], label='Portfolio Value', color='purple')
ax[1].set_title('Portfolio Value Over Time')
ax[1].set_ylabel('Portfolio Value')
ax[1].legend()

plt.xlabel('Date')
plt.tight_layout()
plt.show()