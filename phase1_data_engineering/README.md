# Phase 1: Data Engineering

## 📊 Overview

This phase focuses on **data collection and visualization** for the Stock Predictor project. It includes modules for fetching real-time stock data, creating interactive visualizations, and managing the complete data pipeline workflow.

## 🚀 Quick Start

### Local Installation

```bash
# Navigate to phase1_data_engineering directory
cd phase1_data_engineering

# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit demo app
streamlit run streamlit_app.py
```

### Online Demos

Experience the interactive demos directly in your browser:

🌐 **Live Demos:**
- **Streamlit Cloud:** [Deploy to Streamlit](https://streamlit.io/cloud) - Deploy your own instance using this repository
- **HuggingFace Spaces:** [Create Space](https://huggingface.co/spaces) - Deploy using the HuggingFace Spaces platform
- **Local Demo:** Run `streamlit run streamlit_app.py` for full-featured local experience

> **Note:** To deploy on Streamlit Cloud or HuggingFace Spaces:
> 1. Fork this repository
> 2. Connect your GitHub account to the platform
> 3. Select `streamlit_app.py` as the main file
> 4. Deploy!

---

## 📁 Project Structure

```
phase1_data_engineering/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── fetch_data.py             # Data fetching module
├── plot_data.py              # Visualization module
├── main.py                   # Main workflow orchestrator
├── streamlit_app.py          # Interactive demo application
└── sample_outputs/           # Demo materials and sample outputs
    └── DEMO_GUIDE.md         # Comprehensive demo documentation
```

---

## 🔍 Features

### 1. Data Fetching (`fetch_data.py`)
- ✅ Real-time stock data retrieval using **Yahoo Finance API**
- ✅ Support for multiple stock symbols (AAPL, GOOGL, MSFT, TSLA, etc.)
- ✅ Flexible time periods (1mo, 3mo, 6mo, 1y, 2y, 5y)
- ✅ Automatic data validation and error handling
- ✅ Historical OHLCV data (Open, High, Low, Close, Volume)

### 2. Data Visualization (`plot_data.py`)
- ✅ **Interactive Price Charts** with Plotly
- ✅ **Moving Averages** (20-day and 50-day MA)
- ✅ **Volume Analysis** with bar charts
- ✅ **Statistical Summaries** (mean, std, quartiles)
- ✅ **Responsive Design** for various screen sizes
- ✅ **Export Functionality** (CSV download)

### 3. Interactive Demo (`streamlit_app.py`)
- ✅ User-friendly web interface
- ✅ Real-time data fetching and visualization
- ✅ Multiple tabs for different views:
  - 📊 **Overview:** Key metrics and statistics
  - 📈 **Price Chart:** Interactive line chart with MAs
  - 📉 **Volume Analysis:** Trading volume visualization
  - 📋 **Data Table:** Raw data with download option
- ✅ Customizable inputs (stock symbol, time period)
- ✅ Error handling and user feedback

---

## 📊 Sample Outputs & Demos

The `sample_outputs/` directory contains:

📄 **[DEMO_GUIDE.md](sample_outputs/DEMO_GUIDE.md)** - Comprehensive documentation including:
- Sample visualizations (price charts, volume analysis)
- Screenshot descriptions of the demo interface
- Technical implementation details
- Sample data points from real stocks (AAPL, GOOGL)
- Step-by-step workflow demonstrations
- GIF demonstrations (concept)
- Best practices and usage notes

### Key Demo Features:

1. **Stock Price Chart with Moving Averages**
   - Interactive line chart showing closing prices
   - 20-day and 50-day moving averages overlay
   - Hover details for precise data points
   - Zoom and pan capabilities

2. **Trading Volume Analysis**
   - Bar chart of daily trading volumes
   - Volume statistics (avg, max, min)
   - Correlation with price movements

3. **Statistical Dashboard**
   - Comprehensive OHLCV statistics
   - Price volatility measures
   - Percentage changes and trends

4. **Data Export**
   - One-click CSV download
   - Complete historical data
   - Ready for further analysis

---

## 🛠️ Requirements

### Python Dependencies

```txt
streamlit==1.28.0      # Web app framework
pandas==2.1.3          # Data manipulation
yfinance==0.2.32       # Stock data API
plotly==5.18.0         # Interactive visualizations
numpy==1.26.2          # Numerical computing
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

### System Requirements
- Python 3.9 or higher
- Internet connection (for data fetching)
- Modern web browser (Chrome, Firefox, Edge)

---

## 💻 Usage

### Command Line Interface

```bash
# Fetch data for a specific stock
python fetch_data.py --symbol AAPL --period 1y

# Generate visualizations
python plot_data.py --symbol AAPL --period 1y

# Run complete workflow
python main.py
```

### Interactive Web Interface

```bash
# Launch Streamlit app
streamlit run streamlit_app.py

# Open browser and navigate to:
# Local: http://localhost:8501
```

**Using the Streamlit App:**
1. Enter a valid stock symbol (e.g., AAPL, GOOGL, MSFT)
2. Select desired time period from dropdown
3. Click "Fetch Data" button
4. Explore visualizations in different tabs
5. Download data as CSV if needed

---

## 🎥 Demo Deployment

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with GitHub
4. Click "New app"
5. Select your forked repository
6. Set main file path: `phase1_data_engineering/streamlit_app.py`
7. Click "Deploy"
8. Share your app URL!

### HuggingFace Spaces Deployment

1. **Create a new Space** on [HuggingFace](https://huggingface.co/new-space)
2. Select "Streamlit" as the SDK
3. Clone the Space repository locally:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
4. Copy files from `phase1_data_engineering/` to the Space directory:
   - `streamlit_app.py`
   - `requirements.txt`
5. Rename `streamlit_app.py` to `app.py` (HuggingFace convention)
6. Commit and push:
   ```bash
   git add .
   git commit -m "Add stock predictor demo"
   git push
   ```
7. Your Space will automatically deploy!

### Docker Deployment (Advanced)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

```bash
docker build -t stock-predictor-demo .
docker run -p 8501:8501 stock-predictor-demo
```

---

## 📝 Module Documentation

### `fetch_data.py`
**Purpose:** Fetches historical stock data from Yahoo Finance API

**Key Functions:**
- `fetch_stock_data(symbol, period)`: Retrieves stock data
- `validate_symbol(symbol)`: Validates stock ticker symbol
- `get_available_periods()`: Returns supported time periods

### `plot_data.py`
**Purpose:** Creates interactive visualizations of stock data

**Key Functions:**
- `plot_price_chart(df, symbol)`: Generates price chart with MAs
- `plot_volume_chart(df, symbol)`: Creates volume bar chart
- `calculate_moving_averages(df)`: Computes MA20 and MA50

### `main.py`
**Purpose:** Orchestrates the complete data pipeline workflow

**Workflow:**
1. User inputs stock symbol and period
2. Fetches data using `fetch_data.py`
3. Generates visualizations using `plot_data.py`
4. Displays results and saves outputs

### `streamlit_app.py`
**Purpose:** Interactive web-based demo application

**Features:**
- Sidebar configuration panel
- Real-time data fetching
- Multi-tab interface
- Interactive Plotly charts
- CSV export functionality

---

## 📖 Examples

### Example 1: Fetch Apple Stock Data

```python
import yfinance as yf
import pandas as pd

# Fetch 1 year of AAPL data
stock = yf.Ticker("AAPL")
df = stock.history(period="1y")

print(f"Fetched {len(df)} data points")
print(df.head())
```

### Example 2: Calculate Moving Averages

```python
# Calculate 20-day and 50-day moving averages
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

print(df[['Close', 'MA20', 'MA50']].tail())
```

### Example 3: Create Interactive Chart

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price'))
fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20'))
fig.update_layout(title='Stock Price Chart', xaxis_title='Date', yaxis_title='Price')
fig.show()
```

---

## ⚠️ Important Notes

1. **API Limitations:** Yahoo Finance API has rate limits. Avoid excessive requests.
2. **Data Accuracy:** Stock data is provided "as-is" from Yahoo Finance.
3. **Market Hours:** Real-time data updates only during market hours (9:30 AM - 4:00 PM ET).
4. **Symbol Validation:** Always verify stock symbols before fetching data.
5. **Internet Required:** Active internet connection needed for data fetching.

---

## 🔗 Useful Links

- **Yahoo Finance API Documentation:** [yfinance on PyPI](https://pypi.org/project/yfinance/)
- **Streamlit Documentation:** [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Documentation:** [plotly.com/python](https://plotly.com/python/)
- **Sample Outputs & Demo Guide:** [sample_outputs/DEMO_GUIDE.md](sample_outputs/DEMO_GUIDE.md)

---

## 📞 Support & Contribution

### Report Issues
Found a bug or have a suggestion? [Open an issue](https://github.com/jayeshjain2025-lgtm/stock_predictor_project/issues)

### Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🎯 Next Steps: Phase 2

Phase 2 will introduce:
- Machine learning models for price prediction
- Sentiment analysis from news and social media
- Portfolio optimization algorithms
- Risk assessment tools
- Real-time alerts and notifications

Stay tuned! 🚀

---

## 📜 License

This project is part of the Stock Predictor Project educational initiative.

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0  
**Author:** jayeshjain2025-lgtm
