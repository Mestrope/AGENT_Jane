#!/usr/bin/env python3
"""
cat_news.py

Jane — the cat-loving agent. She loves cats and curates random cute cat images
paired with recent cat-related news from around the web.

"catnews" CLI: show random cute cat images and recent cat-related news.

Usage examples:
  python cat_news.py cute --count 3 --download-dir images
  python cat_news.py news --since-hours 24
  python cat_news.py both --count 4 --since-hours 48 --download-dir images

Or on Windows after cloning/forking, run:
  .\\catnews.bat cute --count 3

Notes:
- Images are sourced from Wikimedia Commons (no API key required).
- News are fetched from Google News RSS (search for "cats"/"kittens").
"""
import argparse
import os
import sys
import time
import random
from datetime import datetime, timezone, timedelta, date
from urllib.parse import urlencode

import requests
import feedparser

USER_AGENT = "Jane/CatNewsAgent/1.0 (https://example.com)"
WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


def fetch_wikimedia_images(query_terms=("cute cat", "kitten"), count=5, fetch_limit=50):
    """Search Wikimedia Commons for images matching query_terms and return randomly selected image dicts.

    Uses the File namespace (gsrnamespace=6) to ensure results are image files.
    If the primary search returns no items, a fallback search without the extra
    filters is attempted.

    Returns list of dicts: {title, url}
    """
    q = " OR ".join(query_terms)
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": q,
        "gsrlimit": str(min(fetch_limit, 50)),
        # Restrict to File namespace so results are actual files (images)
        "gsrnamespace": "6",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
    }
    headers = {"User-Agent": USER_AGENT}

    def _extract_items(data):
        pages = data.get("query", {}).get("pages", {})
        items = []
        for pid, page in pages.items():
            title = page.get("title")
            imageinfo = page.get("imageinfo")
            if imageinfo and isinstance(imageinfo, list):
                url = imageinfo[0].get("url")
                if url and url.lower().startswith("http"):
                    items.append({"title": title, "url": url})
        return items

    try:
        resp = requests.get(WIKIMEDIA_API, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        items = _extract_items(data)
    except Exception:
        items = []

    # Fallback: try a more permissive search if nothing found
    if not items:
        try:
            fallback_params = params.copy()
            # remove namespace restriction for broader results
            fallback_params.pop("gsrnamespace", None)
            # add a simple 'file:' prefix to bias toward file pages
            fallback_params["gsrsearch"] = "file:" + q
            resp = requests.get(WIKIMEDIA_API, params=fallback_params, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            items = _extract_items(data)
        except Exception:
            items = []

    if not items:
        return []

    # pick random unique items up to count
    random.shuffle(items)
    return items[:min(count, len(items))]


def fetch_news_entries(query="cats OR kittens", max_items=50):
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
    # sort by published desc
    entries.sort(key=lambda x: x["published"] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
    return entries


def filter_recent_entries(entries, since_hours=48):
    if since_hours <= 0:
        return entries
    cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
    recent = [e for e in entries if e.get("published") and e.get("published") >= cutoff]
    return recent or entries


def download_image(url, out_path):
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, stream=True, timeout=30)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def print_pairings(images, news_entries, download_dir=None, no_download=False):
    if download_dir and not no_download:
        os.makedirs(download_dir, exist_ok=True)

    for idx, img in enumerate(images, start=1):
        print(f"\n[{idx}] Title: {img.get('title')}")
        print(f"    Image URL: {img.get('url')}")
        news_item = None
        if news_entries:
            news_item = news_entries[(idx - 1) % len(news_entries)]
        if news_item:
            published = news_item.get("published")
            published_str = published.isoformat() if published else "(unknown)"
            print(f"    News: {news_item.get('title')}")
            print(f"    Link: {news_item.get('link')}")
            print(f"    Published (UTC): {published_str}")
        else:
            print("    News: (no recent news found)")

        if download_dir and not no_download:
            ext = os.path.splitext(img.get("url"))[1]
            if not ext:
                ext = ".jpg"
            filename = f"cat_{idx}{ext}"
            out_path = os.path.join(download_dir, filename)
            try:
                print(f"    Downloading to: {out_path} ...")
                download_image(img.get("url"), out_path)
                print("    Download complete.")
            except Exception as e:
                print("    Download failed:", e)


def main():
    parser = argparse.ArgumentParser(prog="catnews", description="Show random cute cat images and recent cat news.")
    sub = parser.add_subparsers(dest="action", help="Action to perform: cute, news, both")

    p_cute = sub.add_parser("cute", help="Show cute cat images (optionally download)")
    p_cute.add_argument("--count", type=int, default=3, help="Number of images to fetch (default:3)")
    p_cute.add_argument("--download-dir", type=str, default=None, help="Directory to download images into (optional)")
    p_cute.add_argument("--no-download", action="store_true", help="Do not download images; only print URLs and news")

    p_news = sub.add_parser("news", help="Show recent cat-related news")
    p_news.add_argument("--since-hours", type=int, default=48, help="How recent news should be (hours, default 48)")
    p_news.add_argument("--max-items", type=int, default=10, help="Max news items to fetch/display")

    p_both = sub.add_parser("both", help="Show images paired with news (default)")
    p_both.add_argument("--count", type=int, default=3, help="Number of images to fetch (default:3)")
    p_both.add_argument("--download-dir", type=str, default=None, help="Directory to download images into (optional)")
    p_both.add_argument("--no-download", action="store_true", help="Do not download images; only print URLs and news")
    p_both.add_argument("--since-hours", type=int, default=48, help="How recent news should be (hours, default 48)")

    # If no subcommand is provided, default to "both"
    if len(sys.argv) == 1:
        args = parser.parse_args(["both"])
    else:
        args = parser.parse_args()

    try:
        if args.action == "cute":
            images = fetch_wikimedia_images(count=args.count)
            print_pairings(images, [], download_dir=getattr(args, "download_dir", None), no_download=getattr(args, "no_download", False))
        elif args.action == "news":
            entries = fetch_news_entries(max_items=getattr(args, "max_items", 10))
            recent = filter_recent_entries(entries, since_hours=getattr(args, "since_hours", 48))
            print("\nRecent cat-related news:")
            for i, e in enumerate(recent[:getattr(args, "max_items", 10)], start=1):
                published = e.get("published")
                pub_str = published.isoformat() if published else "(unknown)"
                print(f"\n[{i}] {e.get('title')}")
                print(f"    Link: {e.get('link')}")
                print(f"    Published (UTC): {pub_str}")
        else:  # both
            images = fetch_wikimedia_images(count=args.count)
            entries = fetch_news_entries(max_items=50)
            recent = filter_recent_entries(entries, since_hours=getattr(args, "since_hours", 48))
            print_pairings(images, recent, download_dir=getattr(args, "download_dir", None), no_download=getattr(args, "no_download", False))
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
