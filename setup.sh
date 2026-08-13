#!/bin/bash
# Assamese Dataset Collection — Environment Setup Script

echo "Setting up data collection environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template — please fill in your Reddit API credentials before running the Reddit scraper."
else
    echo ".env already exists — skipping."
fi

echo ""
echo "Setup complete."
echo "Next steps:"
echo "  1. Edit .env with your Reddit API credentials (get them at https://www.reddit.com/prefs/apps)"
echo "  2. Run: python scripts/imdb_scraper.py"
echo "  3. Run: python scripts/youtube_scraper.py"
echo "  4. Run: python scripts/reddit_scraper.py"