# sentiment_analysis.py
import os
import json
import datetime
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import boto3

# ---- config / paths (adapt to your project layout) ----
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_raw_dir = os.path.join(project_root, "Data", "Raw")
data_processed_dir = os.path.join(project_root, "Data", "Processed")
os.makedirs(data_processed_dir, exist_ok=True)

date_str = datetime.datetime.now().strftime("%Y-%m-%d")
raw_path = os.path.join(data_raw_dir, f"{date_str}.csv")
if not os.path.exists(raw_path):
    raise FileNotFoundError(f"Raw file not found: {raw_path}")

# ---- simple text cleaning ----
def clean_text(s):
    if not isinstance(s, str):
        return ""
    s = s.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # remove some junk chars that confuse sentiment tools
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    return s

# ---- finance lexicon (small, extend later) ----
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

# small helper to check multi-word phrases first
def lexicon_adjust(text_lower):
    adjust = 0.0
    # check multi-word first
    for phrase in ["strong earnings", "record high", "cut forecast", "turnaround"]:
        if phrase in text_lower:
            if phrase in FIN_POS:
                adjust += 0.18
            elif phrase in FIN_NEG:
                adjust -= 0.18
    # single words
    for w in FIN_POS:
        if w in text_lower:
            adjust += 0.08
    for w in FIN_NEG:
        if w in text_lower:
            adjust -= 0.10
    return adjust

# ---- analyzer init ----
analyzer = SentimentIntensityAnalyzer()

# ---- read data ----
df = pd.read_csv(raw_path, dtype=str)  # read as strings to avoid surprises
df.fillna("", inplace=True)
if "title" not in df.columns:
    raise ValueError("Expected 'title' column in raw CSV")

# ensure published exists and is consistent
if "published" in df.columns:
    try:
        df["published"] = pd.to_datetime(df["published"], errors="coerce").dt.date
    except Exception:
        pass
else:
    df["published"] = date_str

# ---- scoring loop ----
scores = []
labels = []
subjectivities = []

for i, row in df.iterrows():
    raw_title = row.get("title", "")
    title = clean_text(raw_title)
    title_lower = title.lower()

    # VADER compound (-1..1)
    vader_scores = analyzer.polarity_scores(title)
    vader_compound = vader_scores.get("compound", 0.0)

    # TextBlob polarity (-1..1) + subjectivity
    tb = TextBlob(title)
    tb_polarity = tb.sentiment.polarity
    subjectivity = tb.sentiment.subjectivity

    # ensemble: weight VADER more for short headlines
    combined = 0.65 * vader_compound + 0.35 * tb_polarity

    # lexicon adjustment (finance-specific)
    adjust = lexicon_adjust(title_lower)
    combined += adjust

    # clamp
    combined = max(-1.0, min(1.0, combined))

    # label with a narrow neutral band
    if combined > 0.05:
        label = "Positive"
    elif combined < -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    scores.append(combined)
    labels.append(label)
    subjectivities.append(subjectivity)

# ---- attach to dataframe ----
df["sentiment"] = scores
df["sentiment_label"] = labels
df["subjectivity"] = subjectivities

# ---- small post-processing: drop exact duplicates by title (keep first) ----
df.drop_duplicates(subset=["title"], keep="first", inplace=True)

# ---- save processed ----
processed_path = os.path.join(data_processed_dir, f"{date_str}_sentiment.csv")
df.to_csv(processed_path, index=False)

# ---- summary (per-source or overall) ----
summary = {
    "date": date_str,
    "num_articles": int(len(df)),
    "avg_sentiment": float(df["sentiment"].mean()),
    "num_positive": int((df["sentiment_label"] == "Positive").sum()),
    "num_neutral": int((df["sentiment_label"] == "Neutral").sum()),
    "num_negative": int((df["sentiment_label"] == "Negative").sum()),
}
summary_path = os.path.join(data_processed_dir, f"{date_str}_sentiment_summary.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)

s3 = boto3.client("s3")
s3.upload_file(processed_path, "phase-3-bucket", f"Processed/{date_str}_sentiment.csv")

print(f"Saved processed sentiment to: {processed_path}")
print(f"Saved summary to: {summary_path}")
print("Summary:", summary)