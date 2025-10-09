# Phase 1: Data Engineering

## Purpose

This phase establishes the foundation of the Stock Predictor project by:
- Collecting historical stock market data from reliable sources
- Processing and cleaning raw financial data for analysis
- Creating insightful visualizations to understand stock price trends and patterns
- Building a reusable data pipeline for future phases

## Data Sources

- **Yahoo Finance API** via the `yfinance` Python library
  - Provides historical stock prices (Open, High, Low, Close, Volume)
  - Supports multiple ticker symbols and date ranges
  - Free and reliable data source for financial information

## Pipeline Overview

The Phase 1 data pipeline follows three key steps:

### 1. **Fetch** (`fetch_data.py`)
- Downloads historical stock data from Yahoo Finance
- Supports customizable date ranges and ticker symbols
- Returns structured pandas DataFrame with OHLCV data

### 2. **Clean** (within `main.py`)
- Handles missing values and data inconsistencies
- Validates data integrity
- Prepares data for visualization and analysis

### 3. **Visualize** (`plotting.py`)
- Generates comprehensive stock price charts
- Creates technical analysis visualizations
- Saves charts as image files for reporting

## Example Output Charts

The pipeline generates various visualizations including:

```python
# Example: Stock Price Visualization
import matplotlib.pyplot as plt
import pandas as pd

# Sample output showing closing prices over time
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Closing Price')
plt.title('Stock Price History')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)
plt.savefig('stock_price_chart.png')
```

**Sample Chart Output:**

![Stock Price Visualization](./demo/sample_chart.png)

*Note: Actual charts will be saved in the current directory after running the scripts.*

## Instructions to Run

### Prerequisites
Ensure you have Python 3.x installed on your system.

### Step 1: Install Dependencies
```bash
pip install yfinance pandas matplotlib seaborn
```

### Step 2: Run Individual Scripts

**To fetch data only:**
```bash
python fetch_data.py
```

**To generate visualizations:**
```bash
python plotting.py
```

### Step 3: Run Complete Pipeline
**Execute the main script to run the entire pipeline:**
```bash
python main.py
```

This will:
1. Fetch stock data using `fetch_data.py`
2. Clean and process the data
3. Generate visualizations using `plotting.py`
4. Save output files (charts and data) to the current directory

### Optional: Run Interactive Demo
```bash
cd demo
python app.py
```

## Dependencies (Phase 1 Specific)

### Core Libraries
- **yfinance** (>=0.2.0) - Yahoo Finance API wrapper for data fetching
- **pandas** (>=1.5.0) - Data manipulation and analysis
- **matplotlib** (>=3.6.0) - Basic plotting and visualization
- **seaborn** (>=0.12.0) - Enhanced statistical visualizations

### Standard Libraries
- **datetime** - Date and time handling
- **os** - File system operations

### Installation Command
```bash
pip install yfinance pandas matplotlib seaborn
```

## Project Structure

```
phase1_data_engineering/
├── README.md           # This file
├── fetch_data.py       # Data fetching module
├── plotting.py         # Visualization module
├── main.py            # Main pipeline orchestrator
└── demo/              # Interactive demo application
```

## Output Files

After running the pipeline, you'll find:
- Stock price charts (`.png` files)
- Processed data files (optional `.csv` exports)
- Log files (if logging is enabled)

## Next Steps

Once Phase 1 is complete, proceed to **Phase 2: Finance Basics** to implement financial metrics and technical indicators.
