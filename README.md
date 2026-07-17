Cat News & Cat Food Finder — Jane's Collection

Meet Jane — the cat-loving agent . She loves cats and helps you discover random cute cat images,
recent cat-related news from around the world, AND find the cheapest best cat food for your adult feline.

This repository provides a collection of Jane's cat-loving CLI tools:
- **catnews**: Fetches random "cute cat" images paired with recent cat-related news
- **catfood**: Finds the cheapest top cat foods for adult cats with ratings and price comparisons
- **jane**: Always happy to help you find the best kitty content and deals.

Quick start

1. Clone or fork this repository.
2. (Optional) Create and activate a virtual environment.

   python -m venv .venv
   .\.venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run Jane's tools

   **catnews** (images + news):
   - Using Python directly:
       python cat_news.py both --count 4 --since-hours 48 --download-dir images
       python cat_news.py cute --count 3 --download-dir images
       python cat_news.py news --since-hours 24
   
   - On Windows you can use the included launcher (from the repo root):
       .\catnews.bat cute --count 3

   **catfood** (find affordable cat food):
   - Using Python directly:
       python cat_food.py
       python cat_food.py --count 5 --brand "Purina"
       python cat_food.py --max-price 20 --min-rating 4.0
   
   - On Windows:
       .\catfood.bat
       .\catfood.bat --count 5 --brand "Royal Canin"

Tools overview

**catnews** — Cute cat images + recent news

- Actions (subcommands):
  - cute   : Fetch and show random cute cat images (optionally download)
  - news   : Show recent cat-related news
  - both   : Fetch images and pair each with a recent news item (default)

- Common flags:
  - --count N        Number of images to fetch (default: 3 for cute/both)
  - --download-dir D Directory to download images into (optional)
  - --no-download    Do not download images; only print URLs and news
  - --since-hours H  How recent the news should be in hours (default: 48)

**catfood** — Find affordable cat food

- Shows the cheapest top 3 adult cat foods available online (from popular retailers like Amazon, Chewy, Walmart, Petco)
- Displays prices, ratings, weight, and price per ounce for easy comparison
- Filters available for brand, max price, and minimum rating

- Common flags:
  - --count N         Number of cheapest foods to show (default: 3)
  - --brand BRAND     Filter by brand (e.g., 'Purina', 'Royal Canin')
  - --max-price PRICE Filter by maximum price (e.g., 25.00)
  - --min-rating RATE Filter by minimum rating (0-5, default: 0)
  - --sort FIELD      Sort by 'price', 'rating', or 'name' (default: price)
  - --json            Output results as JSON

Examples

**catnews examples:**
- Show 5 cute cat images and download them into an images folder:
    python cat_news.py cute --count 5 --download-dir images

- Show recent cat news from the last 24 hours:
    python cat_news.py news --since-hours 24

**catfood examples:**
- Show the top 3 cheapest cat foods (default):
    python cat_food.py

- Find the cheapest Purina cat foods:
    python cat_food.py --brand "Purina"

- Show cat foods under $20 with at least 4.0 rating:
    python cat_food.py --max-price 20 --min-rating 4.0

- Get 5 cheapest options as JSON:
    python cat_food.py --count 5 --json

Project components (what's included)
- cat_news.py       — Primary catnews CLI agent. Implements subcommands: cute, news, both.
- cat_food.py       — catfood CLI agent. Finds and compares cat food prices.
- catnews.bat       — Windows launcher for catnews (run from repo root).
- catfood.bat       — Windows launcher for catfood (run from repo root).
- cat_agent.py      — Earlier/simpler catnews script (kept for reference).
- requirements.txt  — Python dependencies (requests, feedparser).
- README.md         — This file with usage and details.

Key functions and data sources

**catnews (cat_news.py):**
- fetch_wikimedia_images()  — Searches Wikimedia Commons for cat images
- fetch_news_entries()      — Fetches Google News RSS for cat-related news
- filter_recent_entries()   — Filters news by time window
- print_pairings()          — Pairs images with news and prints results

**catfood (cat_food.py):**
- get_cat_foods()           — Filters cat food list by brand, price, rating
- calculate_price_per_oz()  — Calculates cost efficiency
- print_results()           — Displays cat food options in formatted table

Data sources used:
- catnews images: Wikimedia Commons via MediaWiki API (public/freely-licensed)
- catnews news: Google News RSS search for "cats" and "kittens"
- catfood: Curated database of popular adult cat foods with pricing from Amazon, Chewy, Walmart, Petco

Dependencies
- Python 3.8+ recommended
- See requirements.txt; install with:

    pip install -r requirements.txt

Notes and caveats

**catnews:**
- Image results depend on Wikimedia search and may vary over time.
- RSS timestamps are provided by publishers and may be inconsistent.
- No API keys required; simple local operation.

**catfood:**
- Prices are based on a curated database of popular cat foods and are approximate/indicative.
- For real-time pricing, integrate with retailer APIs (Amazon Product Ads, Chewy API, etc.).
- Always verify current prices and availability on retailer websites.
- Consult your veterinarian before switching your cat's diet.

Possible next steps / enhancements

- **catnews**: 
  - Add alternate image providers (Unsplash, Bing)
  - Package as installable pip package with global console entry

- **catfood**:
  - Integrate live price scraping from major retailers
  - Add vet/nutritional recommendations
  - Support for kittens, senior cats, or diet-specific foods
  - Price alerts and tracking

If you'd like, I can implement any of the above next.

License
Provided as-is for learning and prototyping. Use responsibly and always consult your vet for pet health decisions.
