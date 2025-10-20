import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

class BuySell:
    def __init__(self, symbol, period = '2yr'):
        self.symbol = symbol
        self.period = period
    def crossover_strategy(self, data, period = 'period', short_window = 20, long_window = 50):

        #data = yf.download(self.symbol, period = period, interval = '1d')

        data['SMA_short'] = data['Close'].rolling(window = short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window = long_window).mean()

        data['Signal'] = 0

        for i in range(short_window, len(data)):
            if data['SMA_short'].iloc[i] > data['SMA_long'].iloc[i] and data['SMA_short'].iloc[i-1] <= data['SMA_long'].iloc[i-1]:
                data.loc[data.index[i], 'Signal'] = 1  # Buy signal
            elif data['SMA_short'].iloc[i] < data['SMA_long'].iloc[i] and data['SMA_short'].iloc[i-1] >= data['SMA_long'].iloc[i-1]:
                data.loc[data.index[i], 'Signal'] = -1  # Sell signal

        buy_dates = data[data['Signal'] == 1].index.date.tolist()
        sell_dates = data[data['Signal'] == -1].index.date.tolist()
        print("Buy Dates:", buy_dates)
        print("Sell Dates:", sell_dates)


        #Plotting
        plt.figure(figsize=(14,7))
        plt.plot(data['Close'], label='Close', color='black')
        plt.plot(data['SMA_short'], label=f'{short_window}-Day SMA', color='blue')
        plt.plot(data['SMA_long'], label=f'{long_window}-Day SMA', color='yellow')

        # Plot buy/sell signals
        plt.scatter(data[data['Signal']==1].index, 
                    data['SMA_short'][data['Signal']==1], marker='^', color='green', s=100, label='Buy Signal')
        plt.scatter(data[data['Signal']==-1].index, 
                    data['SMA_short'][data['Signal']==-1], marker='v', color='red', s=100, label='Sell Signal')

        plt.title(f"{self.symbol} — SMA Crossover Strategy")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
