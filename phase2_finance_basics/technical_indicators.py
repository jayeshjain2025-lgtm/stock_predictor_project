import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class SMA_EMA:
    def moving_averages(self,symbol, data, period = '6mo', short_window = 20, long_window = 50):
        
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
