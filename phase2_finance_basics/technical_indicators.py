import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def moving_averages(symbol, period = '6mo', short_window = 20, long_window = 50):
    #Fetch historical data
    data = yf.download(symbol, period = period)

    # Calculate moving averages
    data['SMA_short'] = data['Close'].rolling(window = short_window).mean()
    data['SMA_long'] = data ['Close'].rolling(window = long_window).mean()
    data['EMA_short'] = data['Close'].ewm(span = short_window, adjust = False).mean()
    data['EMA_long'] = data ['Close'].ewm(span = long_window, adjust = False).mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close', linewidth=1)
    plt.plot(data['SMA_short'], label=f'{short_window}-Day SMA')
    plt.plot(data['SMA_long'], label=f'{long_window}-Day SMA')
    plt.plot(data['EMA_short'], label=f'{short_window}-Day EMA', linestyle='--')
    plt.plot(data['EMA_long'], label=f'{long_window}-Day EMA', linestyle='--')
    plt.title(f"{symbol} — SMA & EMA Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

# Example usage:
moving_averages('MSFT')