Cat News & Cat Food Finder — Jane's Collection

<<<<<<< HEAD
Meet Jane — the cat-loving agent. She loves cats and helps you discover random cute cat images,
recent cat-related news from around the world, find the cheapest best cat food for your adult feline,
AND find the top-rated cat toys to keep your furry friend entertained!
=======
Meet Jane — the cat-loving agent . She loves cats and helps you discover random cute cat images,
recent cat-related news from around the world, AND find the cheapest best cat food for your adult feline.
>>>>>>> 1d1dfe7404989588786877559ad3381b1ed1d1b0

### FOR THE LOVE OF CATS

This repository provides a collection of Jane's cat-loving CLI tools:
- **catnews**: Fetches random "cute cat" images paired with recent cat-related news
- **catfood**: Finds the cheapest top cat foods for adult cats with ratings and price comparisons
<<<<<<< HEAD
- **cattoys**: Gets top-rated cat toys with descriptions, prices, and where to buy them
=======
>>>>>>> 1d1dfe7404989588786877559ad3381b1ed1d1b0
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

   **cattoys** (find top-rated cat toys):
   - Using Python directly:
       python cat_toys.py
       python cat_toys.py --category interactive --count 5
       python cat_toys.py --max-price 20 --min-rating 4.5
    
   - On Windows:
       .\cattoys.bat
       .\cattoys.bat --category interactive --max-price 25

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

**cattoys** — Get top-rated cat toys

- Shows the top-rated cat toys available online with full details
- Includes toy description, benefits, prices, ratings, and shopping links
- Perfect for finding entertainment and enrichment options for your cat
- Filters available for category, max price, and minimum rating

- Common flags:
  - --count N         Number of top toys to show (default: 3)
  - --category CAT    Filter by category (e.g., 'interactive', 'plush', 'ball', 'tunnel')
  - --max-price PRICE Filter by maximum price (e.g., 25.00)
  - --min-rating RATE Filter by minimum rating (0-5, default: 0)
  - --sort FIELD      Sort by 'rating', 'price', or 'name' (default: rating)
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

**cattoys examples:**
- Show the top 3 highest-rated cat toys (default):
    python cat_toys.py

- Find interactive toys under $15:
    python cat_toys.py --category interactive --max-price 15

- Get top plush toys with 4.5+ rating:
    python cat_toys.py --category plush --min-rating 4.5

- Get 5 top-rated toys as JSON:
    python cat_toys.py --count 5 --json

Project components (what's included)
- cat_news.py       — Primary catnews CLI agent. Implements subcommands: cute, news, both.
- cat_food.py       — catfood CLI agent. Finds and compares cat food prices.
- cat_toys.py       — cattoys CLI agent. Gets top-rated cat toys with details and links.
- catnews.bat       — Windows launcher for catnews (run from repo root).
- catfood.bat       — Windows launcher for catfood (run from repo root).
- cattoys.bat       — Windows launcher for cattoys (run from repo root).
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

**cattoys (cat_toys.py):**
- get_top_cat_toys()        — Filters cat toys by category, price, rating (sorted by rating)
- print_results()           — Displays cat toys with descriptions and benefits

Data sources used:
- catnews images: Wikimedia Commons via MediaWiki API (public/freely-licensed)
- catnews news: Google News RSS search for "cats" and "kittens"
- catfood: Curated database of popular adult cat foods with pricing from Amazon, Chewy, Walmart, Petco
- cattoys: Curated database of popular cat toys with ratings, prices, and retailer links

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

**cattoys:**
- Toy ratings and prices are based on a curated database and are approximate/indicative.
- For real-time pricing and ratings, integrate with retailer APIs.
- Always verify current prices, availability, and safety reviews on retailer websites.
- Check toy reviews and ensure toys are appropriate for your cat's age and play style.

Possible next steps / enhancements

- **catnews**: 
  - Add alternate image providers (Unsplash, Bing)
  - Package as installable pip package with global console entry

- **catfood**:
  - Integrate live price scraping from major retailers
  - Add vet/nutritional recommendations
  - Support for kittens, senior cats, or diet-specific foods
  - Price alerts and tracking

<<<<<<< HEAD
- **cattoys**:
  - Integrate live toy ratings from major retailers
  - Add toy safety ratings and age recommendations
  - Implement "Deal of the Day" for discounted toys
  - Add personalized recommendations based on cat type/age

If you'd like, I can implement any of the above next.
=======

>>>>>>> 1d1dfe7404989588786877559ad3381b1ed1d1b0

License
Provided as-is for learning and prototyping. Use responsibly and always consult your vet for pet health decisions.
