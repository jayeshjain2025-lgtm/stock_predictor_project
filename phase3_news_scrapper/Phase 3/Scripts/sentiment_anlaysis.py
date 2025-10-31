# sentiment_analysis.py
import os
import json
import datetime
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import boto3

# ---- config / paths ----
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_raw_dir = os.path.join(project_root, "Data", "Raw")
data_processed_dir = os.path.join(project_root, "Data", "Processed")
os.makedirs(data_processed_dir, exist_ok=True)

date_str = datetime.datetime.now().strftime("%Y-%m-%d")
raw_path = os.path.join(data_raw_dir, f"scraped_news.csv")
if not os.path.exists(raw_path):
    raise FileNotFoundError(f"Raw file not found: {raw_path}")

master_path = os.path.join(data_processed_dir, "master_sentiment.csv")

# ---- text cleaning ----
def clean_text(s):
    if not isinstance(s, str):
        return ""
    s = s.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    return s

# ---- finance lexicon ----
FIN_POS = [
    "rally", "rallies", "gain", "gains", "surge", "soar", "beat", "beats",
    "upgraded", "upgrade", "record high", "record-high", "strong earnings",
    "outperform", "bullish", "bounce", "turnaround", "recovery"
]
FIN_NEG = [
    "plunge", "plunges", "drop", "drops", "decline", "declines", "miss",
    "misses", "downgrade", "downgrades", "weak", "weakness", "warns",
    "selloff", "sell-off", "cut forecast", "loss", "fall", "fallen"
]

def lexicon_adjust(text_lower):
    adjust = 0.0
    for phrase in ["strong earnings", "record high", "cut forecast", "turnaround"]:
        if phrase in text_lower:
            if phrase in FIN_POS:
                adjust += 0.18
            elif phrase in FIN_NEG:
                adjust -= 0.18
    for w in FIN_POS:
        if w in text_lower:
            adjust += 0.08
    for w in FIN_NEG:
        if w in text_lower:
            adjust -= 0.10
    return adjust

# ---- analyzer ----
analyzer = SentimentIntensityAnalyzer()

# ---- read raw data ----
df = pd.read_csv(raw_path, dtype=str)
df.fillna("", inplace=True)
if "title" not in df.columns:
    raise ValueError("Expected 'title' column in raw CSV")

if "published" in df.columns:
    try:
        df["published"] = pd.to_datetime(df["published"], errors="coerce").dt.date
    except Exception:
        df["published"] = datetime.date.today()
else:
    df["published"] = datetime.date.today()

# ---- sentiment scoring ----
scores, labels, subjectivities = [], [], []

for _, row in df.iterrows():
    title = clean_text(row.get("title", ""))
    lower = title.lower()

    vader = analyzer.polarity_scores(title)["compound"]
    tb = TextBlob(title).sentiment
    combined = 0.65 * vader + 0.35 * tb.polarity + lexicon_adjust(lower)
    combined = max(-1.0, min(1.0, combined))

    if combined > 0.05:
        label = "Positive"
    elif combined < -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    scores.append(combined)
    labels.append(label)
    subjectivities.append(tb.subjectivity)

df["sentiment"] = scores
df["sentiment_label"] = labels
df["subjectivity"] = subjectivities
df.drop_duplicates(subset=["title"], keep="first", inplace=True)

# ---- append to master ----
if os.path.exists(master_path):
    df_master = pd.read_csv(master_path, dtype=str)
    df_master["published"] = pd.to_datetime(df_master["published"], errors="coerce").dt.date
    df_master["sentiment"] = pd.to_numeric(df_master["sentiment"], errors="coerce")
else:
    df_master = pd.DataFrame()

df_combined = pd.concat([df_master, df], ignore_index=True)
df_combined.drop_duplicates(subset=["title"], keep="first", inplace=True)
df_combined.sort_values("published", ascending=False, inplace=True)
df_combined.to_csv(master_path, index=False)

# ---- summary ----
summary = {
    "date": date_str,
    "num_articles": int(len(df)),
    "avg_sentiment": float(df["sentiment"].mean()),
    "num_positive": int((df["sentiment_label"] == "Positive").sum()),
    "num_neutral": int((df["sentiment_label"] == "Neutral").sum()),
    "num_negative": int((df["sentiment_label"] == "Negative").sum()),
}

# ---- upload to S3 ----
s3 = boto3.client("s3")
bucket = "phase-3-bucket"
s3.upload_file(master_path, bucket, "Processed/master_sentiment.csv")

print(f"✓ Updated master file: {master_path}")
print(f"✓ Uploaded to S3 bucket: {bucket}")
print("Summary:", json.dumps(summary, indent=2))