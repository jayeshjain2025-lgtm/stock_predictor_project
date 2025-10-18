# Phase 2: Finance Basics

This phase focuses on implementing fundamental financial analysis tools and technical indicators for stock market analysis. It provides essential building blocks for understanding stock performance, market metrics, and trading strategies.

## Overview

Phase 2 introduces core financial concepts and technical analysis tools that are crucial for stock trend prediction. The modules in this phase enable users to:
- Fetch and analyze basic stock information
- Calculate technical indicators (RSI, SMA, EMA)
- Implement trading strategies
- Understand financial metrics and market data

## Files Description

### 1. `stock info.py`
**Purpose**: Core module for retrieving basic stock information and financial metrics.

**Key Features**:
- `Stock` class that encapsulates stock data using `yfinance` library
- Retrieves essential stock information including:
  - Current price
  - P/E ratio (Price-to-Earnings ratio)
  - Market capitalization
  - 52-week high and low prices
  - Trading volume
  - Dividend yield
  - Earnings per share (EPS)

**Usage Example**:
```python
from stock_info import Stock

# Create a stock object
stock = Stock('AAPL')

# Get stock information
info = stock.get_stock_info()
print(f"Current Price: ${info['currentPrice']}")
print(f"Market Cap: ${info['marketCap']:,}")
print(f"P/E Ratio: {info['trailingPE']}")
```

**Output Format**:
Returns a dictionary containing:
- `currentPrice`: Current trading price
- `marketCap`: Total market capitalization
- `trailingPE`: Price-to-Earnings ratio
- `fiftyTwoWeekHigh`: Highest price in last 52 weeks
- `fiftyTwoWeekLow`: Lowest price in last 52 weeks
- `volume`: Trading volume
- `dividendYield`: Dividend yield percentage
- `trailingEps`: Earnings per share

---

### 2. `financial_statements.py`
**Purpose**: Implements technical indicators for financial analysis, specifically the Relative Strength Index (RSI).

**Key Features**:
- `Technical_Indicators` class for calculating RSI
- Measures momentum and identifies overbought/oversold conditions
- Uses 14-day period as default (industry standard)
- Provides signal interpretation:
  - RSI > 70: Overbought (potential sell signal)
  - RSI < 30: Oversold (potential buy signal)

**RSI Calculation**:
1. Calculate average gains and losses over period
2. Compute Relative Strength (RS) = Average Gain / Average Loss
3. RSI = 100 - (100 / (1 + RS))

**Usage Example**:
```python
from financial_statements import Technical_Indicators

# Initialize with stock ticker
ti = Technical_Indicators('TSLA')

# Calculate RSI
rsi_value = ti.calculate_rsi()
print(f"Current RSI: {rsi_value:.2f}")

if rsi_value > 70:
    print("Signal: Overbought - Consider selling")
elif rsi_value < 30:
    print("Signal: Oversold - Consider buying")
else:
    print("Signal: Neutral")
```

---

### 3. `market_info.py`
**Purpose**: Implements trading strategies using moving average crossovers.

**Key Features**:
- `crossover_strategy` function for SMA-based trading signals
- Compares short-term (50-day) and long-term (200-day) moving averages
- Generates buy/sell signals based on crossover patterns
- Classic "Golden Cross" and "Death Cross" detection

**Strategy Logic**:
- **Buy Signal (Golden Cross)**: Short-term SMA crosses above long-term SMA
  - Indicates upward momentum and potential bullish trend
- **Sell Signal (Death Cross)**: Short-term SMA crosses below long-term SMA
  - Indicates downward momentum and potential bearish trend
- **Hold**: No crossover detected, maintain current position

**Usage Example**:
```python
from market_info import crossover_strategy

# Get trading signal
signal = crossover_strategy('GOOGL')
print(f"Trading Signal: {signal}")

if signal == 'Buy':
    print("Action: Enter long position")
elif signal == 'Sell':
    print("Action: Exit position or short")
else:
    print("Action: Hold current position")
```

**Technical Details**:
- Short-term SMA: 50-day moving average
- Long-term SMA: 200-day moving average
- Requires sufficient historical data (minimum 200 days)

---

### 4. `technical_indicators.py`
**Purpose**: Calculates and analyzes moving averages for trend identification.

**Key Features**:
- `moving_averages` function for computing SMA and EMA
- Supports multiple timeframes (20, 50, 200 days)
- Calculates both Simple Moving Average (SMA) and Exponential Moving Average (EMA)
- Returns comprehensive trend analysis

**Moving Averages Explained**:
- **Simple Moving Average (SMA)**: Arithmetic mean of prices over period
  - Equal weight to all prices
  - Smoother but slower to react to changes
  
- **Exponential Moving Average (EMA)**: Weighted average favoring recent prices
  - More responsive to recent price changes
  - Better for short-term trading signals

**Usage Example**:
```python
from technical_indicators import moving_averages

# Get moving averages
result = moving_averages('MSFT')

print(f"20-day SMA: ${result['SMA_20']:.2f}")
print(f"50-day SMA: ${result['SMA_50']:.2f}")
print(f"200-day SMA: ${result['SMA_200']:.2f}")
print(f"\n20-day EMA: ${result['EMA_20']:.2f}")
print(f"50-day EMA: ${result['EMA_50']:.2f}")
print(f"200-day EMA: ${result['EMA_200']:.2f}")
```

**Interpretation Guide**:
- **Current Price vs SMA/EMA**:
  - Price > MA: Bullish signal, uptrend
  - Price < MA: Bearish signal, downtrend
- **Short-term vs Long-term MA**:
  - Short MA > Long MA: Bullish momentum
  - Short MA < Long MA: Bearish momentum

---

## Dependencies

All modules require the following Python packages:

```bash
pip install yfinance pandas numpy
```

- **yfinance**: Yahoo Finance API for fetching stock data
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations

---

## Installation & Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd stock_trend_predictor_project/phase2_finance_basics
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
# Or install individually:
pip install yfinance pandas numpy
```

3. **Run individual modules**:
```bash
python "stock info.py"
python financial_statements.py
python market_info.py
python technical_indicators.py
```

---

## Common Use Cases

### 1. Quick Stock Analysis
```python
from stock_info import Stock
from financial_statements import Technical_Indicators
from technical_indicators import moving_averages

ticker = 'AAPL'

# Get basic info
stock = Stock(ticker)
info = stock.get_stock_info()

# Calculate RSI
ti = Technical_Indicators(ticker)
rsi = ti.calculate_rsi()

# Get moving averages
ma = moving_averages(ticker)

print(f"Stock: {ticker}")
print(f"Price: ${info['currentPrice']}")
print(f"RSI: {rsi:.2f}")
print(f"50-day SMA: ${ma['SMA_50']:.2f}")
```

### 2. Trading Signal Generator
```python
from market_info import crossover_strategy
from financial_statements import Technical_Indicators

ticker = 'TSLA'

# Get crossover signal
signal = crossover_strategy(ticker)

# Get RSI for confirmation
ti = Technical_Indicators(ticker)
rsi = ti.calculate_rsi()

print(f"Crossover Signal: {signal}")
print(f"RSI: {rsi:.2f}")

# Combined analysis
if signal == 'Buy' and rsi < 30:
    print("Strong Buy Signal!")
elif signal == 'Sell' and rsi > 70:
    print("Strong Sell Signal!")
```

### 3. Trend Analysis
```python
from technical_indicators import moving_averages

ticker = 'NVDA'
ma = moving_averages(ticker)

# Analyze trend
if ma['SMA_20'] > ma['SMA_50'] > ma['SMA_200']:
    print("Strong Uptrend")
elif ma['SMA_20'] < ma['SMA_50'] < ma['SMA_200']:
    print("Strong Downtrend")
else:
    print("Mixed/Ranging Market")
```

---

## Key Financial Concepts

### Technical Indicators
- **RSI (Relative Strength Index)**: Momentum oscillator measuring speed and magnitude of price changes
- **SMA (Simple Moving Average)**: Average price over specified period
- **EMA (Exponential Moving Average)**: Weighted average emphasizing recent prices

### Trading Signals
- **Golden Cross**: Bullish signal when 50-day MA crosses above 200-day MA
- **Death Cross**: Bearish signal when 50-day MA crosses below 200-day MA
- **Overbought/Oversold**: RSI-based signals for potential reversals

### Financial Metrics
- **P/E Ratio**: Valuation metric (price per share / earnings per share)
- **Market Cap**: Total value of company's outstanding shares
- **EPS (Earnings Per Share)**: Company's profit divided by outstanding shares
- **Dividend Yield**: Annual dividend payment as percentage of stock price

---

## Next Steps

This phase provides the foundation for more advanced analysis. Future phases will build upon these basics to:
- Implement machine learning models for prediction
- Develop portfolio optimization strategies
- Create automated trading systems
- Integrate sentiment analysis from news and social media

---

## Contributing

For improvements or bug fixes:
1. Test changes with multiple stock tickers
2. Ensure backward compatibility
3. Document new features thoroughly
4. Handle edge cases (delisted stocks, insufficient data, etc.)

---

## Notes & Limitations

- **Data Dependency**: All modules rely on Yahoo Finance API availability
- **Historical Data**: Some indicators require minimum data periods (e.g., 200 days for 200-day SMA)
- **Market Hours**: Real-time data only available during market hours
- **Accuracy**: Technical indicators are tools, not guarantees - always combine with fundamental analysis
- **API Rate Limits**: Be mindful of yfinance rate limits when analyzing many stocks

---

## License

Part of the Stock Trend Predictor Project

---

## Contact & Support

For questions or issues related to Phase 2:
- Check the main project README
- Review yfinance documentation: https://pypi.org/project/yfinance/
- Ensure all dependencies are installed correctly

---

**Phase 2 Status**: ✅ Complete - Foundation for financial analysis established
