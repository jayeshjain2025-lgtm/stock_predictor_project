import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os

# =======================
# CONFIG
# =======================
FINNHUB_API_KEY = "d3tqhlpr01qvr0dk3amgd3tqhlpr01qvr0dk3an0"  # replace with your own
SYMBOL = "MSFT"                     # e.g., AAPL, TSLA, AMZN
DAYS_BACK = 7
OUTPUT_DIR = "Data/Raw"
MASTER_FILE = "scraped_news.csv"
LOG_FILE = "update_log.txt"

# =======================
# HELPER FUNCTIONS
# =======================
def get_finnhub_news(symbol, start_date, end_date):
    """Fetch news for a given symbol and date range from Finnhub"""
    url = "https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": symbol,
        "from": start_date,
        "to": end_date,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"✗ Error fetching {start_date} → {end_date}: {e}")
        return []

# =======================
# MAIN SCRAPER
# =======================
def scrape_finnhub_history(symbol, days_back):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    master_path = os.path.join(OUTPUT_DIR, MASTER_FILE)
    log_path = os.path.join(OUTPUT_DIR, LOG_FILE)

    # Load existing data if available
    if os.path.exists(master_path):
        df_master = pd.read_csv(master_path)
        print(f"Loaded existing master dataset with {len(df_master)} rows.")
    else:
        df_master = pd.DataFrame(columns=["title", "link", "published", "symbol"])
        print("No existing master dataset found. Creating a new one.")

    print(f"\nFetching last {days_back} days of news for {symbol}...\n")
    all_news = []
    today = datetime.now()

    for i in range(days_back):
        day = today - timedelta(days=i)
        from_date = day.strftime("%Y-%m-%d")
        to_date = (day + timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"→ Fetching {from_date}")
        news = get_finnhub_news(symbol, from_date, to_date)

        for item in news:
            all_news.append({
                "title": item.get("headline"),
                "link": item.get("url"),
                "published": item.get("datetime", 0),
                "symbol": symbol
            })

        # polite delay for free tier rate-limit (30 calls/min)
        time.sleep(random.uniform(1.5, 2.5))

    # Process new data
    df_new = pd.DataFrame(all_news)
    if df_new.empty:
        print("✗ No news found!")
        return

    df_new["published"] = pd.to_datetime(df_new["published"], unit="s", errors="coerce").dt.date
    df_new.dropna(subset=["title"], inplace=True)

    # Combine and deduplicate
    df_combined = pd.concat([df_master, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["title", "link", "published"], inplace=True)

    # ✅ Normalize all date formats before sorting
    df_combined["published"] = pd.to_datetime(df_combined["published"], errors="coerce").dt.date

    df_combined.sort_values("published", ascending=False, inplace=True)
    df_combined.reset_index(drop=True, inplace=True)

    # Save updated master file
    df_combined.to_csv(master_path, index=False)

    # Log update
    with open(log_path, "a") as log:
        log.write(f"Updated {symbol} | {datetime.now().isoformat()} | Total: {len(df_combined)}\n")

    print(f"\n✓ Master dataset updated — {len(df_combined)} total entries")
    print(f"   Date range: {df_combined['published'].min()} → {df_combined['published'].max()}")
    print(f"   Saved at: {master_path}")

# =======================
# RUN
# =======================
if __name__ == "__main__":
    scrape_finnhub_history(SYMBOL, DAYS_BACK)
