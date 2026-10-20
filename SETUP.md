# Data Collection Setup Guide

This guide walks through configuring the reference data-collection scripts used to build the Assamese Movie Reviews dataset.

> **Note:** These are reference implementations demonstrating the collection methodology described in the dataset card — not the exact original scripts (which were not preserved from the original collection process). Adapt movie IDs, subreddit names, and search queries to your target sources.

## Prerequisites

- Python 3.8+
- pip

## Step 1: Clone and enter the repository

```bash
git clone https://github.com/AvinabhDutta-Dev/assamese-dataset-collection.git
cd assamese-dataset-collection
```

## Step 2: Run the setup script

```bash
chmod +x setup.sh
./setup.sh
```

This creates a virtual environment, installs dependencies, and generates a `.env` file from the template.

## Step 3a: Get Reddit API credentials (required for the Reddit scraper)

1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
2. Click **create another app...** at the bottom.
3. Select **script** as the app type.
4. Fill in a name (e.g., "AssameseSentimentScraper") and redirect URI (`http://localhost:8080` works for script apps).
5. After creation, copy the **client ID** (under the app name) and **client secret**.

## Step 3b: Get a YouTube Data API key (required for the YouTube scraper)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services → Library**, search for **YouTube Data API v3**, and enable it.
4. Go to **APIs & Services → Credentials → Create Credentials → API Key**.
5. Copy the generated key into `.env` as `YOUTUBE_API_KEY`.

## Step 4: Configure `.env`

Open `.env` and fill in:
```
REDDIT_CLIENT_ID=<your client id>
REDDIT_CLIENT_SECRET=<your client secret>
REDDIT_USER_AGENT=AssameseSentimentAnalysisScraper/1.0 by /u/<your reddit username>
```

## Step 5: Run the scrapers

**IMDb scraper** (no credentials needed — just a target movie ID, found in the movie's IMDb URL, e.g., `tt1234567`):
```bash
python scripts/imdb_scraper.py
```

**Reddit scraper** (requires `.env` configured):
```bash
python scripts/reddit_scraper.py
```

**YouTube scraper** (requires `YOUTUBE_API_KEY` in `.env`):
```bash
python scripts/youtube_scraper.py
```

Both scripts output CSVs matching the project's baseline schema (`ID`, `Reviews`, `Sentiment`), with `Sentiment` left blank for subsequent manual annotation — consistent with the two-annotator labeling process described in the dataset card.

## Notes

- IMDb's page structure changes periodically — the scraper's CSS selectors may need updates if scraping breaks.
- Respect each platform's Terms of Service and rate limits when collecting data. The included `time.sleep()` delays are a minimum courtesy, not a guarantee of compliance.
- `scripts/youtube_scraper.py` is included as a reference template and requires a `YOUTUBE_API_KEY` in `.env`. It uses the YouTube Data API v3 API key flow; OAuth setup is not required by this script. API availability, quota limits, video settings, and comment availability can affect results.
