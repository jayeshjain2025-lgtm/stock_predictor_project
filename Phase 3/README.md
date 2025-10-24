# Phase 3: Sentiment Analysis & News Aggregation

## Purpose

This phase combines news scraping with sentiment analysis to predict stock market trends based on news sentiment:

- Scraping financial news from multiple RSS feeds
- Extracting sentiment scores from news articles
- Analyzing historical sentiment patterns
- Correlating sentiment with stock price movements
- Building feature fusion for predictive modeling

## Overview

Phase 3 implements a comprehensive news sentiment analysis pipeline that integrates real-time financial news data with sentiment scoring techniques. This phase bridges the gap between financial analysis (Phase 2) and raw market data (Phase 1) by introducing the psychological and market sentiment aspects of stock prediction.

## Key Components

### Scripts

- **scraper.py** - RSS feed scraper that collects financial news from multiple sources
- **sentiment_analysis.py** - Sentiment scoring using VADER and TextBlob
- **feature_fusion.py** - Combines sentiment data with technical and fundamental indicators
- **old_news.py** - Processes historical news archives

### Configuration

- **config.json** - Stores RSS feed URLs and data paths (sensitive credentials stored in .env)

## Setup

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then configure your AWS credentials and bucket name.

## Running the Pipeline

```bash
python Scripts/scraper.py
python Scripts/sentiment_analysis.py
python Scripts/feature_fusion.py
```

## Data Flow

1. **Data Collection** - scraper.py fetches latest news from RSS feeds
2. **Sentiment Analysis** - sentiment_analysis.py scores article sentiment
3. **Feature Engineering** - feature_fusion.py creates composite features
4. **Output** - Results stored in Data/Raw for modeling

## Dependencies

See `requirements.txt` for all Python package dependencies.
