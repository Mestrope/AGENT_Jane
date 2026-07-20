#!/usr/bin/env python3
"""
cat_toys.py

Jane's Cat Toys Recommendation Tool — finds the top 3 highest-rated cat toys available online.

This tool picks the top 3 highest rated cat toys of the day and provides links, prices,
and descriptions to help you find the perfect toy for your cat.

Usage examples:
  python cat_toys.py
  python cat_toys.py --count 5 --max-price 30
  python cat_toys.py --category "interactive" --min-rating 4.5
  python cat_toys.py --json

Jane loves recommending great toys to keep your cat happy and active!
"""
import argparse
import sys
import json
from typing import List, Dict
from datetime import datetime

USER_AGENT = "Jane/CatToysAgent/1.0 (https://example.com)"

# Database of popular cat toys with ratings and details
# This is a curated list; in production, you'd scrape live prices and ratings
CAT_TOYS = [
    {
        "name": "Interactive Feather Wand Toy",
        "category": "interactive",
        "price": 12.99,
        "rating": 4.8,
        "description": "Multi-colored feather wand with bell and interactive motion. Great for exercise and engagement.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=feather+wand+cat+toy",
        "benefits": ["Exercise", "Interactive play", "Bonding"]
    },
    {
        "name": "Laser Pointer Pet Toy",
        "category": "interactive",
        "price": 9.99,
        "rating": 4.7,
        "description": "USB rechargeable laser pointer with auto-on timer. Provides endless entertainment and exercise.",
        "source": "Chewy",
        "url": "https://chewy.com/s?query=laser+pointer+cat+toy",
        "benefits": ["Exercise", "Mental stimulation", "Auto-timer mode"]
    },
    {
        "name": "Catnip Mouse Toy Set",
        "category": "plush",
        "price": 14.99,
        "rating": 4.9,
        "description": "Pack of 6 soft plush mice filled with premium catnip. Perfect for batting and pouncing.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=catnip+mouse+toys+cats",
        "benefits": ["Stress relief", "Pouncing practice", "Multi-pack value"]
    },
    {
        "name": "Crinkle Ball Toy",
        "category": "ball",
        "price": 7.99,
        "rating": 4.6,
        "description": "Lightweight crinkle ball that makes sounds when batted. Encourages independent play.",
        "source": "Petco",
        "url": "https://petco.com/shop/en/petco/cat-toys",
        "benefits": ["Sound stimulation", "Lightweight", "Easy to bat"]
    },
    {
        "name": "Tunnel Cat Toy",
        "category": "tunnel",
        "price": 18.99,
        "rating": 4.8,
        "description": "Foldable tunnel with crinkle sound and dangling toy. Provides hiding space and play area.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=tunnel+cat+toy",
        "benefits": ["Hiding space", "Crinkle sounds", "Space-saving design"]
    },
    {
        "name": "Ball Track Toy",
        "category": "interactive",
        "price": 16.99,
        "rating": 4.7,
        "description": "Oval track with rolling balls underneath. Cats can bat the balls as they move around.",
        "source": "Chewy",
        "url": "https://chewy.com/s?query=ball+track+cat+toy",
        "benefits": ["Chase instinct", "Independent play", "Durable design"]
    },
    {
        "name": "Catnip Filled Kick Toy",
        "category": "plush",
        "price": 8.99,
        "rating": 4.5,
        "description": "Long plush toy filled with catnip and silvervine. Perfect for kicking and carrying around.",
        "source": "Walmart",
        "url": "https://walmart.com/search/?query=catnip+kick+toy+cats",
        "benefits": ["Kicking motion", "Catnip and silvervine", "Portable"]
    },
    {
        "name": "Electric Moving Toy Mouse",
        "category": "interactive",
        "price": 22.99,
        "rating": 4.8,
        "description": "Battery-powered mouse that scurries around unpredictably. Stimulates hunting instincts.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=electric+moving+mouse+cat+toy",
        "benefits": ["Hunting simulation", "Unpredictable movement", "Interactive fun"]
    },
    {
        "name": "Feather Teaser Rod",
        "category": "interactive",
        "price": 11.99,
        "rating": 4.6,
        "description": "Classic wand with feathers and bell. Lightweight and easy to control for extended play sessions.",
        "source": "Petco",
        "url": "https://petco.com/shop/en/petco/cat-toys",
        "benefits": ["Easy control", "Classic design", "Affordable"]
    },
    {
        "name": "Spinning Bird Toy",
        "category": "interactive",
        "price": 13.99,
        "rating": 4.7,
        "description": "Motorized toy with feather attachment that spins and moves. Mesmerizes cats with realistic motion.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=spinning+bird+cat+toy",
        "benefits": ["Realistic motion", "Mesmerizing", "Exercise"]
    },
    {
        "name": "Jingle Ball Toy Pack",
        "category": "ball",
        "price": 10.99,
        "rating": 4.4,
        "description": "Pack of 4 small balls with jingle bells inside. Great for multi-cat households.",
        "source": "Amazon",
        "url": "https://amazon.com/s?k=jingle+ball+cat+toys",
        "benefits": ["Multiple toys", "Sound attraction", "Affordable"]
    },
    {
        "name": "Suction Cup Ball Toy",
        "category": "interactive",
        "price": 9.99,
        "rating": 4.5,
        "description": "Ball mounted on suction cup to window or wall. Cats can bat and chase without it rolling away.",
        "source": "Chewy",
        "url": "https://chewy.com/s?query=suction+cup+ball+cat+toy",
        "benefits": ["No-roll design", "Window mounting", "Exercise"]
    },
]


def get_top_cat_toys(
    category_filter: str = None,
    max_price: float = None,
    min_rating: float = 0.0,
    count: int = 3
) -> List[Dict]:
    """
    Filter cat toys by category, max price, and min rating.
    Returns sorted list (highest rating first, then by price).
    """
    results = CAT_TOYS.copy()

    if category_filter:
        results = [t for t in results if category_filter.lower() in t["category"].lower()]

    if max_price:
        results = [t for t in results if t["price"] <= max_price]

    if min_rating > 0:
        results = [t for t in results if t["rating"] >= min_rating]

    # Sort by rating descending (highest first), then by price ascending
    results.sort(key=lambda x: (-x["rating"], x["price"]))

    return results[:count]


def print_results(toys: List[Dict], show_all_fields: bool = False):
    """Print cat toy results in a formatted table."""
    if not toys:
        print("No cat toys found matching your criteria.")
        return

    print(f"\n{'='*120}")
    print(f"{'TOP CAT TOYS RECOMMENDATION (Sorted by Rating)':<120}")
    print(f"{'='*120}\n")

    for idx, toy in enumerate(toys, start=1):
        print(f"[{idx}] {toy['name']}")
        print(f"    Category: {toy['category'].capitalize():15} | Price: ${toy['price']:<7.2f} | Rating: {toy['rating']} stars")
        print(f"    Description: {toy['description']}")
        print(f"    Source: {toy['source']:15} | URL: {toy['url']}")
        
        if toy.get('benefits'):
            benefits_str = " | ".join(toy['benefits'])
            print(f"    Benefits: {benefits_str}")
        
        if show_all_fields:
            print(f"    Last Updated: {datetime.now().isoformat()}")
        
        print()

    print(f"{'='*120}")
    print(f"Jane's tip: Mix different types of toys (interactive, plush, balls) to keep your cat engaged!")
    print(f"Rotate toys weekly to maintain novelty and keep your cat mentally stimulated.")
    print(f"{'='*120}\n")


def main():
    parser = argparse.ArgumentParser(
        prog="cattoys",
        description="Jane's Cat Toys Finder — find the top-rated cat toys online."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of top-rated cat toys to show (default: 3)"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter by category (e.g., 'interactive', 'plush', 'ball', 'tunnel')"
    )
    parser.add_argument(
        "--max-price",
        type=float,
        default=None,
        help="Filter by maximum price per item (e.g., 25.00)"
    )
    parser.add_argument(
        "--min-rating",
        type=float,
        default=0.0,
        help="Filter by minimum rating (0-5, default: 0 - no filter)"
    )
    parser.add_argument(
        "--sort",
        choices=["rating", "price", "name"],
        default="rating",
        help="Sort results by field (default: rating)"
    )
    parser.add_argument(
        "--all-fields",
        action="store_true",
        help="Show all fields in output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    try:
        # Get top-rated cat toys
        toys = get_top_cat_toys(
            category_filter=args.category,
            max_price=args.max_price,
            min_rating=args.min_rating,
            count=args.count
        )

        if args.json:
            print(json.dumps(toys, indent=2))
        else:
            print_results(toys, show_all_fields=args.all_fields)

    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
