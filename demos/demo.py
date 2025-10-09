#!/usr/bin/env python3
"""
Stock Predictor Demo
A demonstration of the stock prediction system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_sample_data():
    """
    Load sample stock data for demonstration
    """
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    prices = 100 + np.cumsum(np.random.randn(100) * 2)
    
    data = pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, 100)
    })
    
    return data

def calculate_moving_average(data, window=20):
    """
    Calculate moving average for the stock data
    """
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data

def predict_trend(data):
    """
    Simple trend prediction based on moving average
    """
    current_price = data['Close'].iloc[-1]
    ma_value = data['MA'].iloc[-1]
    
    if current_price > ma_value:
        return "Bullish"
    else:
        return "Bearish"

def main():
    """
    Main demo function
    """
    print("Stock Predictor Demo")
    print("=" * 50)
    
    # Load sample data
    data = load_sample_data()
    print(f"\nLoaded {len(data)} days of stock data")
    
    # Calculate moving average
    data = calculate_moving_average(data)
    print(f"Calculated 20-day moving average")
    
    # Predict trend
    trend = predict_trend(data)
    print(f"\nCurrent Trend: {trend}")
    print(f"Current Price: ${data['Close'].iloc[-1]:.2f}")
    print(f"20-day MA: ${data['MA'].iloc[-1]:.2f}")
    
    print("\nDemo completed successfully!")

if __name__ == "__main__":
    main()
