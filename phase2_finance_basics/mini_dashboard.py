from financial_statements import Technical_Indicators
import yfinance as yf
from stock_info import Stock
from market_info import BuySell
from technical_indicators import SMA_EMA

def analyze_stock(symbol):
    data = yf.download(symbol, period = '6mo', interval = '1d')
    BuySell(symbol, data)

    print("\n============================")
    print(f"📊 Analyzing {symbol} ...")
    print("============================")

    # ---------- Fundamentals ----------
    print("\n🔹 Fundamental Indicators:")
    stock = Stock(symbol)
    print(stock.market_cap())
    print(stock.dividend_info())
    print(stock.eps_info())
    print(stock.pe_ratio())
    print(stock.pb_ratio())
    print(stock.roe_ratio())
    print(stock.de_ratio())

    # ---------- Technicals ----------
    print("\n🔹 SMA / EMA Crossover:")
    bs = BuySell(symbol)
    bs.crossover_strategy(data)

    print("\n🔹 RSI Indicator:")
    ti = Technical_Indicators(symbol)
    ti.rsi(data)
    ti.macd(data)

    print("\n🔹 SMA, EMA Plotting:")
    se = SMA_EMA()
    se.moving_averages(symbol,data)

if __name__ == '__main__':
    symbols = input('Enter the ticker symbol of the stock:').upper().split()
    for symbol in symbols:
        analyze_stock(symbol)