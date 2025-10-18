import yfinance as yf
import matplotlib.pyplot as plt

class Technical_Indicators:
    def __init__(self, symbol, period = '6mo', window = 20):
        self.symbol = symbol
        self.period = period
        self.window = window

    def rsi(self):
        #Fetch historical data
        data = yf.download(self.symbol, period = self.period, interval = '1d')
        # Calculate moving averages
        data['Change'] = data['Close'].diff()  # yfinance actually returns 'Close' with capital C
        data['Gain'] = data['Change'].where(data['Change'] > 0, 0)
        data['Loss'] = -data['Change'].where(data['Change'] < 0, 0)
        #Finding Avg
        data['Avg_Gain'] = data['Gain'].ewm(span = self.window, adjust = False).mean()
        data['Avg_Loss'] = data['Loss'].ewm(span = self.window, adjust = False).mean()
        #Calculate RSI
        data['RS'] = data['Avg_Gain'] / data['Avg_Loss'].replace(0, 1e-10)
        data['RSI'] = 100 - (100 / (1 + data['RS']))
        
        # Extract first and last dates safely

        data['Prev_RSI'] = data['RSI'].shift(1)
        overbought_cross = data[(data['Prev_RSI'] < 70) & (data['RSI'] >= 70)]
        oversold_cross = data[(data['Prev_RSI'] > 30) & (data['RSI'] <= 30)]

        overbought_dates = overbought_cross.index.date.tolist()
        oversold_dates = oversold_cross.index.date.tolist()

        print(f"\n--- {self.symbol} RSI Crossovers ---")
        if overbought_dates:
            print("Overbought (RSI crossed above 70):", overbought_dates)
        else:
            print("No overbought crossover found in this period.")

        if oversold_dates:
            print("Oversold (RSI crossed below 30):", oversold_dates)
        else:
            print("No oversold crossover found in this period.")

        # Plot RSI
        plt.figure(figsize=(14,7))
        plt.plot(data['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
        plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')

        plt.scatter(overbought_cross.index, overbought_cross['RSI'], color='red', label='Overbought Cross', marker='^', s=100)
        plt.scatter(oversold_cross.index, oversold_cross['RSI'], color='green', label='Oversold Cross', marker='v', s=100)


        plt.title(f"{self.symbol} - Relative Strength Index (RSI)")
        plt.xlabel("Date")
        plt.ylabel("RSI Value")
        plt.legend()
        plt.show()

        return data['RSI']

if __name__ == '__main__':
    # Example usage
    ti = Technical_Indicators('NVDA')
    print(ti.rsi())