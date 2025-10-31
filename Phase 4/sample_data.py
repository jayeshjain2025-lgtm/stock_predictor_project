import requests

# URL of your running Flask API
url = "http://127.0.0.1:5000/predict"

# --------------------------
# 1️⃣ Dictionary input
# --------------------------
sample_features_dict = {
    'High': 305.0,
    'Low': 300.5,
    'Open': 302.3,
    'Volume': 3500000,
    'SMA_short': 303.2,
    'SMA_long': 299.8,
    'EMA_short': 303.0,
    'EMA_long': 300.0,
    'Change': 1.5,
    'Gain': 1.5,
    'Loss': 0.0,
    'Avg_Gain': 1.2,
    'Avg_Loss': 0.3,
    'RS': 4.0,
    'RSI': 80.0,
    'MACD_Line': 2.0,
    'Signal_Line': 1.5,
    'MACD_Hist': 0.5,
    'PE_Ratio': 25.0,
    'PB_Ratio': 4.0,
    'ROE': 15.0,
    'DE_Ratio': 0.5,
    'EPS': 12.0,
    'Dividend_Yield': 1.2,
    'Market_Cap': 2000000000,
    'Symbol': 1,  # numeric encoding for symbol
    'mean_sentiment': 0.05,
    'sentiment_count': 10
}

response = requests.post(url, json={"features": sample_features_dict})
print("Dictionary input prediction:")
print(response.json())

# --------------------------
# 2️⃣ List input (must match feature order)
# --------------------------
sample_features_list = [
    305.0, 300.5, 302.3, 3500000, 303.2, 299.8, 303.0, 300.0,
    1.5, 1.5, 0.0, 1.2, 0.3, 4.0, 80.0, 2.0, 1.5, 0.5, 25.0,
    4.0, 15.0, 0.5, 12.0, 1.2, 2000000000, 1, 0.05, 10
]

response = requests.post(url, json={"features": sample_features_list})
print("\nList input prediction:")
print(response.json())
