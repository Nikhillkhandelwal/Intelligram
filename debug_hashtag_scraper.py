import sys
import os

# Add the backend/app directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.scraper import InstagramScraper
import json
import pandas as pd

def test_hashtag_scraping():
    print("Testing Hashtag Scraping for #StartupIndia...")
    scraper = InstagramScraper()
    
    # Test standard hashtag fetch
    res = scraper.fetch_hashtag_posts("StartupIndia", max_posts=5)
    
    if res and res.get("posts") is not None and not res["posts"].empty:
        print(f"✅ SUCCESS: Scraped {len(res['posts'])} posts")
        print(res["posts"][["post_id", "likes", "comments"]].head())
    else:
        print("❌ FAILED: Scraper returned 0 posts or None")
        
    # Check session status
    try:
        print("\nChecking Instaloader Context...")
        print(f"Logged in as: {scraper.L.context.username}")
        # Try a simple profile lookup to see if session is valid
        profile = scraper.L.context.get_json("instagram/")
        print("✅ Session appears valid (can hit generic IG endpoints)")
    except Exception as e:
        print(f"❌ Session Check Failed: {e}")

if __name__ == "__main__":
    test_hashtag_scraping()
