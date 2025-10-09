from fetch_data import StockFetcher
import matplotlib.pyplot as plt

class StockPlotter:
    def __init__(self, symbol, period='1mo', interval='1h'):
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def plotting(self):
        fetcher = StockFetcher(self.symbol, self.period, self.interval)
        df = fetcher.get_data()
        
        plt.figure(figsize=(10,5))
        plt.plot(df.index, df['Close'], linewidth=1.5)
        plt.title(f"{self.symbol} Closing Prices ({self.period}, {self.interval})", fontsize=12)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
        
        return df
