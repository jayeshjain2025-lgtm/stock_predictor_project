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

base_fname = config.get("output_filename", "scraped_news.csv")
master_path = os.path.join(data_raw_dir, base_fname)

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
            "published": getattr(entry, "published", "N/A"),
            "source": url
        })

# Create DataFrame
df_new = pd.DataFrame(all_entries)
df_new['published'] = pd.to_datetime(df_new['published'], errors='coerce', utc=True)
df_new['published'] = df_new['published'].dt.date
df_new["published"].fillna(datetime.date.today(), inplace=True)
df_new["scraped_on"] = datetime.date.today()

# Load existing master file (if exists)
if os.path.exists(master_path):
    df_master = pd.read_csv(master_path)
    print(f"Loaded existing master dataset with {len(df_master)} rows.")
else:
    df_master = pd.DataFrame(columns=df_new.columns)
    print("No existing master dataset found. Creating a new one.")

# Combine and drop duplicates
df_combined = pd.concat([df_master, df_new], ignore_index=True)
df_combined.drop_duplicates(subset=["title", "link", "published"], inplace=True)
df_combined.reset_index(drop=True, inplace=True)

# Save updated master file
df_combined.to_csv(master_path, index=False)

# Log update time
log_path = os.path.join(data_raw_dir, "update_log.txt")
with open(log_path, "a") as log:
    log.write(f"Updated on {datetime.datetime.now().isoformat()} | Rows: {len(df_combined)}\n")

print(f"Appended and uploaded master dataset with {len(df_combined)} total entries.")
