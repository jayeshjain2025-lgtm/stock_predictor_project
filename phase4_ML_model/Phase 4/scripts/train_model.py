import pandas as pd
import os, datetime, pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error, r2_score

# Paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mini_project_dir = os.path.dirname(project_root)
data_fused_dir = os.path.join(mini_project_dir, 'Phase 3', "Data", "Fused")

# Load the latest fused dataset
fused_files = [f for f in os.listdir(data_fused_dir) if f.endswith('.csv')]
latest_fused = max(fused_files, key=lambda x: os.path.getctime(os.path.join(data_fused_dir, x)))
fused_path = os.path.join(data_fused_dir, latest_fused)

print(f"Loading data from: {fused_path}")
data = pd.read_csv(fused_path)

# Target (Close price)
if "Close" not in data.columns:
    raise ValueError("No 'Close' column found in the dataset.")
y = data["Close"]

# Features and target
# Drop columns that aren't numeric or useful as predictors
drop_cols = ["Date", "symbol", "Name", "Company", "Ticker", "Unnamed: 0", 'Close']
data = data.drop(columns=[c for c in drop_cols if c in data.columns])

# Convert everything possible to numeric and fill NaNs
data = data.apply(pd.to_numeric, errors='coerce').fillna(0)
y = pd.to_numeric(y, errors='coerce')
y = y.ffill().bfill()

if y.isna().sum() > 0:
    raise ValueError("Target variable still contains NaN values after filling.")

X = data  # all numeric features

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")
print(f"Model trained successfully. MSE: {mse:.4f}")

model_path = "model/final_model.pkl"
with open(model_path, "rb") as f:
    data = pickle.load(f)

# Save model + feature order (correct)
model_dir = os.path.join(project_root, "model")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "final_model.pkl")

model_metadata = {
    "model": model,
    "features": X.columns.tolist()  # all numeric feature names in order
}

with open(model_path, "wb") as f:
    pickle.dump(model_metadata, f)

print("Model and feature order saved successfully!")
print(f"Features expected by the model ({len(X.columns.tolist())}):")
print(X.columns.tolist())


print(f"Model saved at: {model_path}")
