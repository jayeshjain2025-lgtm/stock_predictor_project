import feedparser
import os
import pandas as pd
import datetime
import json
import boto3
import requests
import time

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(script_dir), 'config.json')

# Load config
with open(config_path, 'r') as f:
    config = json.load(f)

rss_urls = config["rss_feeds"]
project_root = os.path.dirname(script_dir)
data_raw_dir = os.path.join(project_root, "Data", "Raw")
os.makedirs(data_raw_dir, exist_ok=True)
output_path = os.path.join(script_dir, config["output_path"])

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)
base_fname = config.get("output_filename", f"scraped_news.csv")
base_fname = os.path.basename(base_fname)

# Scrape headlines
all_entries = []
for url in rss_urls:
    print(f"Fetching feed: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        print(f"Fetched {len(feed.entries)} entries from {url}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        continue
    time.sleep(5)
    for entry in feed.entries:
        all_entries.append({
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, "published", "N/A")
        })

# Create DataFrame
df = pd.DataFrame(all_entries)
df['published'] = pd.to_datetime(df['published'], errors = 'coerce', utc=True)
df["published"] = df["published"].dt.date
df["published"].fillna(datetime.date.today(), inplace=True)


# Add timestamped filename
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
file_name = os.path.join(data_raw_dir, base_fname.replace(".csv", f"_{date_str}.csv"))

# Save locally
df.to_csv(file_name, index=False)

# Upload to S3
s3 = boto3.client("s3")
s3.upload_file(file_name, "phase-3-bucket", f"Raw/{date_str}_headlines.csv")

print(f"Saved and uploaded headlines: {file_name}")