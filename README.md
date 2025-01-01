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
