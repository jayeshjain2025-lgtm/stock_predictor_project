from plot_data import StockPlotter

if __name__ == "__main__":
    period = input("Enter period: ").strip() or "1mo"
    interval = input("Enter interval: ").strip() or "1h"
    symbol = input("Enter stock ticker symbol (e.g. AAPL, MSFT, RELIANCE.NS): ").strip().upper()
    
    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    
    if interval not in valid_intervals or period not in valid_periods:
        raise SystemExit(f"Invalid interval or period.\nValid intervals: {valid_intervals}\nValid periods: {valid_periods}")
    
    plotter = StockPlotter(symbol, period, interval)
    df = plotter.plot_data()
