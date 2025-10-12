# Phase 1: Data Engineering

## Purpose
This phase establishes the foundation of the Stock Trend Predictor project by:
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
df.plot(y='Close', title='Stock Price History')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()
```

## Running the Phase 1 Pipeline

### Prerequisites
- Python 3.8 or higher
- Internet connection for data fetching

### Steps to Execute
1. Navigate to the phase1_data_engineering directory
2. Run the main pipeline script:
```bash
python main.py
```
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
