import streamlit as st
from plotting import StockPlotter       # Make sure this module is accessible

st.title("📈 Stock Analyzer with Yahoo Finance")

# --- Inputs ---
symbol = st.text_input("Enter stock ticker symbol", "AAPL").strip().upper()

with st.sidebar:
    st.header("Configuration")
    
    period = st.selectbox(
        "Select period",
        ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
        index=2
    )

    interval = st.selectbox(
        "Select interval",
        ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
        index=7
    )

# --- Button ---
if st.button("Fetch and Plot"):
    with st.spinner("Fetching data..."):
        try:
            # Use the user inputs
            plotter = StockPlotter(symbol, period, interval)
            df = plotter.plotting()  # this will save CSV and plot
            
            # Optional Streamlit line chart
            st.line_chart(df["Close"])
            st.success(f"Fetched {len(df)} rows for {symbol}")
        except Exception as e:
            st.error(f"Error: {e}")
