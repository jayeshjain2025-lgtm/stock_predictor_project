from plotting import StockPlotter

valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

while True:
    try:
        period = input("Enter period: ").strip() or "1mo"
        interval = input("Enter interval: ").strip() or "1h"
        symbol = input("Enter stock ticker symbol (e.g. AAPL, MSFT, RELIANCE.NS): ").strip().upper()
        
        # Validate
        if interval not in valid_intervals or period not in valid_periods:
            print(f"Invalid input. Valid intervals: {valid_intervals}, valid periods: {valid_periods}")
            continue
        
        # Fetch and plot
        plotter = StockPlotter(symbol, period, interval)
        df = plotter.plotting()
        
        print(f"Fetched {len(df)} rows for {symbol}")
        break  # exit loop if successful
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please try again.\n")
