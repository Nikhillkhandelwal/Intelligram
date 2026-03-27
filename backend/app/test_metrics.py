import sys
sys.stdout = open("result.txt", "w", encoding="utf-8")
from playwright.sync_api import sync_playwright
import os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
sys.path.insert(0, os.path.dirname(__file__))
from scraper import InstagramScraper

scraper = InstagramScraper()
df = scraper._fetch_from_ig_playwright("bicepssandbanter", max_posts=3)
if df is not None:
    for _, row in df.iterrows():
        print(f"POST {row['post_id']} -> Likes: {row['likes']}, Comments: {row['comments']}")
else:
    print("FAILED - returned None")
sys.stdout.close()
