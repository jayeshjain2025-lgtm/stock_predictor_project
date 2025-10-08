import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Stock Predictor - Phase 1 Demo",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Stock Predictor - Phase 1: Data Engineering")
st.markdown("""
This interactive demo showcases the **Phase 1 Data Engineering** features of the Stock Predictor project:
- **Data Fetching**: Retrieve real-time stock data using Yahoo Finance API
- **Data Visualization**: Interactive charts and graphs
- **Workflow**: End-to-end data pipeline demonstration
""")

# Sidebar for user inputs
st.sidebar.header("Configuration")
stock_symbol = st.sidebar.text_input("Stock Symbol", value="AAPL", help="Enter a valid stock ticker symbol")
period = st.sidebar.selectbox(
    "Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

# Add a demo button
if st.sidebar.button("Fetch Data", type="primary"):
    st.session_state.fetch_data = True

if 'fetch_data' not in st.session_state:
    st.session_state.fetch_data = False

# Main content area
if st.session_state.fetch_data:
    try:
        # Fetch data
        with st.spinner(f"Fetching data for {stock_symbol}..."):
            stock = yf.Ticker(stock_symbol)
            df = stock.history(period=period)
            
        if df.empty:
            st.error("No data found for the given symbol. Please try another.")
        else:
            # Display basic info
            st.success(f"Successfully fetched {len(df)} data points for {stock_symbol}")
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Price Chart", "📉 Volume Analysis", "📋 Data Table"])
            
            with tab1:
                st.subheader("Stock Overview")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Latest Close", f"${df['Close'].iloc[-1]:.2f}")
                with col2:
                    change = df['Close'].iloc[-1] - df['Close'].iloc[0]
                    st.metric("Change", f"${change:.2f}", f"{(change/df['Close'].iloc[0]*100):.2f}%")
                with col3:
                    st.metric("Highest", f"${df['High'].max():.2f}")
                with col4:
                    st.metric("Lowest", f"${df['Low'].min():.2f}")
                
                # Statistical summary
                st.subheader("Statistical Summary")
                st.dataframe(df[['Open', 'High', 'Low', 'Close', 'Volume']].describe())
            
            with tab2:
                st.subheader("Price Chart with Moving Averages")
                
                # Calculate moving averages
                df['MA20'] = df['Close'].rolling(window=20).mean()
                df['MA50'] = df['Close'].rolling(window=50).mean()
                
                # Create interactive plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price', line=dict(color='blue', width=2)))
                fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='20-Day MA', line=dict(color='orange', width=1.5)))
                fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='50-Day MA', line=dict(color='red', width=1.5)))
                
                fig.update_layout(
                    title=f"{stock_symbol} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    hovermode='x unified',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Volume Analysis")
                
                fig_volume = go.Figure()
                fig_volume.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue'))
                fig_volume.update_layout(
                    title=f"{stock_symbol} Trading Volume",
                    xaxis_title="Date",
                    yaxis_title="Volume",
                    height=400
                )
                st.plotly_chart(fig_volume, use_container_width=True)
                
                # Volume statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Volume", f"{df['Volume'].mean():,.0f}")
                with col2:
                    st.metric("Max Volume", f"{df['Volume'].max():,.0f}")
                with col3:
                    st.metric("Min Volume", f"{df['Volume'].min():,.0f}")
            
            with tab4:
                st.subheader("Raw Data")
                st.dataframe(df, use_container_width=True)
                
                # Download button
                csv = df.to_csv()
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{stock_symbol}_data.csv",
                    mime="text/csv"
                )
    
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        st.info("Please check the stock symbol and try again.")

else:
    # Welcome screen
    st.info("👈 Configure your settings in the sidebar and click 'Fetch Data' to begin!")
    
    # Feature highlights
    st.subheader("Features Demonstrated:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 Data Fetching
        - Real-time stock data retrieval
        - Multiple timeframe support
        - Yahoo Finance API integration
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Visualization
        - Interactive price charts
        - Moving averages (MA20, MA50)
        - Volume analysis
        - Candlestick patterns
        """)
    
    with col3:
        st.markdown("""
        ### ⚙️ Workflow
        - Data validation
        - Statistical analysis
        - CSV export functionality
        - Responsive UI
        """)

# Footer
st.markdown("---")
st.markdown("""
**Phase 1: Data Engineering** | Built with Streamlit, yfinance, and Plotly  
🔗 [GitHub Repository](https://github.com/jayeshjain2025-lgtm/stock_predictor_project)
""")
