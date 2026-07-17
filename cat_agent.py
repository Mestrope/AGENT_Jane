#!/usr/bin/env python3
"""
cat_agent.py

Simple CLI agent that searches for cat images on Wikimedia Commons and
prints one recent news item about cats for each image.

Usage:
  python cat_agent.py --count 5 --download-dir images

Requirements:
  pip install -r requirements.txt

This script is intentionally simple so users can fork and extend it.
"""
import argparse
import os
import sys
import requests
import time
from datetime import datetime, timezone, date
from urllib.parse import urlencode

try:
    import feedparser
except Exception:
    print("Missing dependency 'feedparser'. Install with: pip install -r requirements.txt")
    sys.exit(1)

USER_AGENT = "CatImageNewsAgent/1.0 (https://example.com)"
WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


def fetch_wikimedia_images(count=5, extra_limit=10):
    """Fetch image URLs from Wikimedia Commons using the search generator.

    Returns a list of dicts: {title, url, pageid}
    """
    # generator search may return some non-file pages; request extra and filter
    limit = min(max(count, 1) + extra_limit, 50)
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": "cat filetype:bitmap",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(WIKIMEDIA_API, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    results = []
    pages = data.get("query", {}).get("pages", {})
    for pid, page in pages.items():
        title = page.get("title")
        imageinfo = page.get("imageinfo")
        if imageinfo and isinstance(imageinfo, list):
            url = imageinfo[0].get("url")
            if url and url.lower().startswith("http"):
                results.append({"title": title, "url": url, "pageid": pid})
    # sort results by title for deterministic output, then take requested count
    results = sorted(results, key=lambda r: r.get("title"))[:count]
    return results


def fetch_news_entries(query="cats", max_items=20):
    """Fetch news entries from Google News RSS for the given query.

    Returns a list of dicts: {title, link, published: datetime}
    """
    params = {"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"}
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(GOOGLE_NEWS_RSS, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    entries = []
    for e in feed.entries[:max_items]:
        published = None
        if hasattr(e, "published_parsed") and e.published_parsed:
            published = datetime.fromtimestamp(time.mktime(e.published_parsed), tz=timezone.utc)
        entries.append({"title": e.get("title"), "link": e.get("link"), "published": published})
    # sort by published desc (None goes last)
    entries.sort(key=lambda x: x["published"] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
    return entries


def filter_today_entries(entries):
    """Return entries whose published date is today (UTC). If none found, return full list."""
    today_utc = date.today()
    today_items = []
    for e in entries:
        p = e.get("published")
        if p and p.date() == today_utc:
            today_items.append(e)
    return today_items or entries


def download_image(url, out_path):
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, stream=True, timeout=30)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def main():
    parser = argparse.ArgumentParser(description="CLI agent: fetch cat images and pair each with a news item about cats today.")
    parser.add_argument("--count", type=int, default=5, help="Number of cat images to fetch (default: 5)")
    parser.add_argument("--download-dir", type=str, default=None, help="Directory to download images into (optional)")
    parser.add_argument("--no-download", action="store_true", help="Do not download images; only print URLs and news")
    args = parser.parse_args()

    try:
        print(f"Searching for {args.count} cat images on Wikimedia Commons...")
        images = fetch_wikimedia_images(count=args.count)
    except Exception as e:
        print("Failed to fetch images:", e)
        sys.exit(1)

    if not images:
        print("No images found. Try increasing count or check your network connection.")
        sys.exit(1)

    try:
        print("Fetching recent news about cats...")
        news_entries = fetch_news_entries(query="cats", max_items=50)
        news_today = filter_today_entries(news_entries)
    except Exception as e:
        print("Failed to fetch news:", e)
        news_today = []

    # Ensure download directory exists
    if args.download_dir and not args.no_download:
        os.makedirs(args.download_dir, exist_ok=True)

    if not news_today:
        print("No news entries found. Proceeding without news items.")

    print("\nResults:")
    for idx, img in enumerate(images, start=1):
        print(f"\n[{idx}] Title: {img.get('title')}")
        print(f"    Image URL: {img.get('url')}")

        # select a news item for this image (rotate through available news)
        news_item = None
        if news_today:
            news_item = news_today[(idx - 1) % len(news_today)]

        if news_item:
            published = news_item.get("published")
            published_str = published.isoformat() if published else "(unknown)"
            print(f"    News: {news_item.get('title')}")
            print(f"    Link: {news_item.get('link')}")
            print(f"    Published (UTC): {published_str}")
        else:
            print("    News: (no recent news found)")

        if args.download_dir and not args.no_download:
            # create a safe filename
            ext = os.path.splitext(img.get("url"))[1]
            if not ext:
                ext = ".jpg"
            filename = f"cat_{idx}{ext}"
            out_path = os.path.join(args.download_dir, filename)
            try:
                print(f"    Downloading to: {out_path} ...")
                download_image(img.get("url"), out_path)
                print("    Download complete.")
            except Exception as e:
                print("    Download failed:", e)

    print("\nDone.")


if __name__ == "__main__":
    main()
