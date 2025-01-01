# Trading Strategy Simulator

This project is a **Trading Strategy Simulator** that allows users to backtest a stock trading strategy using historical stock data. The strategy uses **Simple Moving Averages (SMA)** to generate buy and sell signals. The user can visualize the stock price, moving averages, and portfolio value over time.

## Features

- Fetches historical stock data using **Yahoo Finance** (`yfinance`).
- Computes **50-day** and **200-day Simple Moving Averages (SMA)** for the selected stock.
- Simulates a trading strategy with buy and sell signals based on the crossover of the 50-day and 200-day SMAs.
- Backtests the strategy, calculating portfolio value over time.
- Visualizes the stock price, moving averages, and portfolio value on separate graphs.
- Allows user to specify stock ticker and initial cash through a simple **Graphical User Interface (GUI)**.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kingigbozuruike/trading-strategy-simulator.git
cd trading-strategy-simulator
```

### 2. Install dependencies
You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Run the simulator
To run the simulator, execute the Python script:

```bash
python trading_sim.py
```
The GUI will appear, and you can input the stock ticker and initial cash to begin the simulation.

## How It Works

### 1. User Input:
The user is prompted to enter a stock ticker symbol (e.g., AAPL for Apple) and an initial cash amount for the portfolio.

### 2. Stock Data Retrieval:
The project fetches historical stock data from Yahoo Finance using the yfinance library.

### 3. Signal Generation:
The 50-day SMA and 200-day SMA are calculated for the given stock.
Buy and sell signals are generated based on the crossover of the SMAs.

### 4. Backtesting:
The backtest simulates buying and selling actions using the strategy, tracking the portfolio value at each step.

### 5. Visualization:
A graph of the stock price, SMAs, and portfolio value is displayed for visual analysis.

## Example
<img width="1440" alt="Screenshot 2024-12-31 at 8 05 03 PM" src="https://github.com/user-attachments/assets/1e299dd7-7de5-43c4-b518-19b0f923a9a3" />

## Future Enhancements
Additional Strategy Options: Implement other technical indicators (e.g., RSI, MACD) for signal generation.
Real-Time Trading: Integrate the simulator with real-time stock data for live trading.
Performance Metrics: Add more detailed metrics like Sharpe ratio, maximum drawdown, etc.
User Customization: Allow the user to specify different strategy parameters, such as SMA window size.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
yfinance: Used for retrieving historical stock data from Yahoo Finance.
matplotlib: Used for generating visualizations of stock prices and portfolio performance.


