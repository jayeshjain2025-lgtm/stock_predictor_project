import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os

# =======================
# CONFIG
# =======================
FINNHUB_API_KEY =  "d3tqhlpr01qvr0dk3amgd3tqhlpr01qvr0dk3an0"  # replace with your key
SYMBOL = "MSFT"                   # you can change this to any ticker
OUTPUT_FILE = "finnhub_news_90days.csv"
DAYS_BACK = 90

# =======================
# SCRAPER FUNCTION
# =======================
def get_finnhub_news(symbol, start_date, end_date):
    """Fetch news for a given symbol and date range"""
    url = f"https://finnhub.io/api/v1/company-news"
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
# MAIN SCRAPER LOOP
# =======================
def scrape_finnhub_history(symbol, days_back):
    print(f"Fetching {days_back} days of news for {symbol}...\n")
    all_news = []
    today = datetime.now()

    for i in range(days_back):
        day = today - timedelta(days=i)
        from_date = day.strftime("%Y-%m-%d")
        to_date = (day + timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"→ {from_date}")
        news = get_finnhub_news(symbol, from_date, to_date)

        for item in news:
            all_news.append({
                "title": item.get("headline"),
                "link": item.get("url"),
                "published": item.get("datetime", 0)
            })

        # polite delay to avoid rate-limit (Finnhub free tier = 30 calls/min)
        time.sleep(random.uniform(1.5, 2.5))

    # =======================
    # CLEANUP & SAVE
    # =======================
    df = pd.DataFrame(all_news)
    if df.empty:
        print("✗ No news found!")
        return

    # Convert UNIX timestamps to date format
    df["published"] = pd.to_datetime(df["published"], unit="s", errors="coerce").dt.date

    # Drop duplicates and sort
    df = df.drop_duplicates(subset=["title"]).sort_values("published", ascending=False)

    # Save output
    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✓ Saved {len(df)} articles to {OUTPUT_FILE}")
    print(f"   Date range: {df['published'].min()} → {df['published'].max()}")

# =======================
# RUN
# =======================
if __name__ == "__main__":
    scrape_finnhub_history(SYMBOL, DAYS_BACK)
