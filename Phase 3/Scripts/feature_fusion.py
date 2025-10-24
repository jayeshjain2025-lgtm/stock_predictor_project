import pandas as pd
import os, datetime, json, boto3

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
mini_projects = os.path.dirname(project_root)

# Load config
config_path = os.path.join(project_root, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Directories
data_processed_dir = os.path.join(project_root, "Data", "Processed")
data_fused_dir = os.path.join(project_root, "Data", "Fused")
os.makedirs(data_fused_dir, exist_ok=True)
data_analysed_dir = os.path.join(mini_projects, 'Phase 2', 'data', 'phase2_datasets')

# File names
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
indicators_path = os.path.join(data_analysed_dir, f"MSFT_analysis_data.csv")  # Phase 2 output
sentiment_path = os.path.join(data_processed_dir, f"{date_str}_sentiment.csv")               # Phase 3 output

# Load data
indicators_df = pd.read_csv(indicators_path)
sentiment_df = pd.read_csv(sentiment_path)

# Convert date columns
indicators_df["Date"] = pd.to_datetime(indicators_df["Date"], errors='coerce').dt.date
sentiment_df["published"] = pd.to_datetime(sentiment_df["published"], errors='coerce').dt.date

# Aggregate sentiment by date
sentiment_agg = sentiment_df.groupby("published").agg(
    mean_sentiment=("sentiment", "mean"),
    sentiment_count=("sentiment", "count")
).reset_index().rename(columns={"published": "Date"})

# Merge
merged_df = pd.merge(indicators_df, sentiment_agg, on="Date", how="left")

# Fill missing sentiment with neutral (0)
merged_df["mean_sentiment"].fillna(0, inplace=True)
merged_df["sentiment_count"].fillna(0, inplace=True)

# Save final fused dataset
fused_path = os.path.join(data_fused_dir, f"{date_str}.csv")
merged_df.to_csv(fused_path, index=False)

#S3 Upload
s3 = boto3.client("s3")
s3.upload_file(fused_path, "phase-3-bucket", f"Fused/{date_str}_fused_features.csv")

print(f"Feature fusion complete. File saved at: {fused_path}")
