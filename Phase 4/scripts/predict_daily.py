import os
import pandas as pd
import pickle
import datetime

# Paths – adjust according to your project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FUSED_DIR = os.path.join(PROJECT_ROOT, '..', 'Phase 3', 'Data', 'Fused')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'model', 'final_model.pkl')

def get_latest_fused_csv(stock_symbol=None):
    # List all CSVs
    files = [f for f in os.listdir(DATA_FUSED_DIR) if f.endswith('.csv')]
    if stock_symbol:
        files = [f for f in files if stock_symbol in f]
    if not files:
        raise FileNotFoundError("No fused CSV files found.")
    # Return the latest one by creation time
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(DATA_FUSED_DIR, x)))
    return os.path.join(DATA_FUSED_DIR, latest_file)

def load_model(model_path=MODEL_PATH):
    with open(model_path, 'rb') as f:
        model_metadata = pickle.load(f)
    return model_metadata['model'], model_metadata['features']

def predict_today(stock_symbol=None):
    fused_csv = get_latest_fused_csv(stock_symbol)
    print(f"Loading fused data: {fused_csv}")
    data = pd.read_csv(fused_csv)
    
    # Drop irrelevant columns
    drop_cols = ["Date", "Name", "Company", "Ticker", "Unnamed: 0", 'Close']
    data = data.drop(columns=[c for c in drop_cols if c in data.columns])
    
    # Convert all features to numeric (non-numeric → NaN → fill 0)
    data = data.apply(pd.to_numeric, errors='coerce').fillna(0)

    latest_row = data.iloc[-1:]  # last row = today's features

    model, feature_order = load_model()
    
    # Ensure all features are present
    missing_features = set(feature_order) - set(latest_row.columns)
    if missing_features:
        raise ValueError(f"Missing features in fused data: {missing_features}")
    
    # Reorder features to match training
    X = latest_row[feature_order]
    prediction = model.predict(X)[0]
    
    # Log result
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"[{date_str}] Prediction for stock {stock_symbol or 'single-stock'}: {prediction:.2f}")
    return prediction

if __name__ == "__main__":
    predict_today()  # Add stock_symbol='MSFT' if needed
