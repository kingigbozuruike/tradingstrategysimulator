import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox

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
    
    # stats
    initial_value = initial_cash
    final_value = stock_data['Portfolio Value'].iloc[-1]
    total_profit = final_value - initial_value
    percent_profit = (total_profit / initial_value) * 100
    
    return stock_data, total_profit, percent_profit, final_value

# function to trigger backtest
def run_backtest():
    ticker = entry_ticker.get().upper()
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()
    initial_cash = float(entry_initial_cash.get())

    if not ticker or not start_date or not end_date or not initial_cash:
        tk.messagebox.showerror("Error", "Please fill all fields")
        return

    stock_data = get_stock_data(ticker, start_date, end_date)
    stock_data = generate_signals(stock_data)
    stock_data, total_profit, percent_profit, final_value = backtest_strategy(stock_data, initial_cash)

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

    # display stats on graph
    ax[1].text(0.5, 0.8, f'Total Profit: ${total_profit:.2f}\nPercent Gain: {percent_profit:.2f}%\nFinal Portfolio Value: ${final_value:.2f}',
               horizontalalignment='center', verticalalignment='center', transform=ax[1].transAxes, fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))

    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Trading Strategy Backtester")

# create labels and entry fields for input
tk.Label(root, text="Stock Ticker (e.g., AAPL):").grid(row=0, column=0, padx=10, pady=10)
entry_ticker = tk.Entry(root)
entry_ticker.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
entry_start_date = tk.Entry(root)
entry_start_date.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
entry_end_date = tk.Entry(root)
entry_end_date.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Initial Cash:").grid(row=3, column=0, padx=10, pady=10)
entry_initial_cash = tk.Entry(root)
entry_initial_cash.grid(row=3, column=1, padx=10, pady=10)

# button to trigger backtest
button = tk.Button(root, text="Run Backtest", command=run_backtest)
button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()