Cat News — Cute Cat Images + Recent Cat News (CLI)

Meet Jane — the cat-loving agent. She loves cats and curates random cute cat images
paired with recent cat-related news from around the world. Use the "catnews" CLI to
ask Jane for a cute cat picture, a cat news update, or both.

This repository provides a small command-line tool named "catnews" that:
- Fetches random "cute cat" images from Wikimedia Commons (no API key required)
- Fetches recent cat-related news from Google News RSS
- Pairs one news item with each picture and prints the results

Quick start

1. Clone or fork this repository.
2. (Optional) Create and activate a virtual environment.

   python -m venv .venv
   .\.venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the CLI

   - Using Python directly:
       python cat_news.py both --count 4 --since-hours 48 --download-dir images
       python cat_news.py cute --count 3 --download-dir images
       python cat_news.py news --since-hours 24

   - On Windows you can use the included launcher (from the repo root):
       .\catnews.bat cute --count 3

Usage overview
- Actions (subcommands):
  - cute   : Fetch and show random cute cat images (optionally download)
  - news   : Show recent cat-related news
  - both   : Fetch images and pair each with a recent news item (default)

Common flags
- --count N        Number of images to fetch (default: 3 for cute/both)
- --download-dir D Directory to download images into (optional)
- --no-download    Do not download images; only print URLs and news
- --since-hours H  How recent the news should be in hours (default: 48)

Examples
- Show 5 cute cat images and download them into an images folder:
    python cat_news.py cute --count 5 --download-dir images

- Show recent cat news from the last 24 hours:
    python cat_news.py news --since-hours 24

- Default (both): 3 random cute cat images paired with recent news (48 hours):
    python cat_news.py
    python cat_news.py both

Project components (what's included)
- cat_news.py       — Primary CLI agent (recommended). Implements subcommands: cute, news, both.
- catnews.bat       — Windows launcher that forwards arguments to cat_news.py (run from repo root).
- cat_agent.py      — Earlier/simpler CLI script (kept for reference).
- requirements.txt  — Python dependencies (requests, feedparser).
- README.md         — This file with usage and details.

Key functions inside cat_news.py
- fetch_wikimedia_images(query_terms, count, fetch_limit)
  - Searches Wikimedia Commons (primary search restricts to File namespace) and returns image title + URL pairs. Has a fallback search when no results are found.
- fetch_news_entries(query, max_items)
  - Fetches Google News RSS for the specified query and returns parsed entries (title, link, published timestamp).
- filter_recent_entries(entries, since_hours)
  - Filters news entries to those within the specified recent time window (in hours).
- download_image(url, out_path)
  - Downloads image bytes to disk.
- print_pairings(images, news_entries, download_dir, no_download)
  - Pairs images with news entries and prints info; downloads files when requested.

Dependencies
- Python 3.8+ recommended
- See requirements.txt; install with:

    pip install -r requirements.txt

Data sources used
- Images: Wikimedia Commons via the MediaWiki API (https://commons.wikimedia.org/w/api.php). Public and freely-licensed images; verify individual image licenses for reuse.
- News: Google News RSS search (https://news.google.com/rss/search?q=...). RSS content and timestamps are provided by publishers.

Limitations & notes
- Image results depend on Wikimedia search results and may vary by query or over time.
- RSS timestamps may be missing or inconsistent across publishers; the script normalizes timestamps to UTC when available.
- The tool does no caching or deduplication across runs. It performs synchronous network calls and downloads, which is simple but not optimized for speed.
- No API keys are required for current sources. Using other providers (Unsplash, Bing, Flickr) may require API keys and different request code.

Possible next steps / enhancements
- Package as an installable Python package (setup.cfg/pyproject.toml) with a console_scripts entry named "catnews" so users can run it globally.
- Add alternate image providers (Unsplash, Bing) for higher-quality photos (requires API keys).
- Add language/location filters for news queries and better date handling.
- Add caching, retries, parallel downloads, and simple logging for robustness.

If you'd like, I can implement any of the above next (packaging, alternate sources, or robustness improvements).

License
Provided as-is for learning and prototyping.
