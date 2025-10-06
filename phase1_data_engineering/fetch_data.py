import time

import yfinance as yf

class StockFetcher:

    def __init__(self, symbol, period='1mo', interval='1h'):
        self.symbol = symbol
        self.period = period
        self.interval = interval

    def get_data(self):
        for attempt in range(3):
            try:
                df = yf.download(
                    self.symbol,
                    period=self.period,
                    interval=self.interval,
                    progress=False
                )
                if not df.empty:
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)
        else:
            raise SystemExit("No data returned. Check ticker/symbol and network.")
        
        # Save to CSV
        csv_name = f"{self.symbol}_yfinance.csv"
        df.to_csv(csv_name)
        print(f"Saved {len(df)} rows to {csv_name}")
        
        return df
