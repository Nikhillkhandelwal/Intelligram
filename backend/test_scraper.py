import sys
import os
sys.path.append(os.path.join(os.getcwd(), "app"))
from scraper import InstagramScraper
from dotenv import load_dotenv

load_dotenv()

def test():
    print("Initializing test scraper...")
    scraper = InstagramScraper()
    print("Fetching posts for 'instagram'...")
    df = scraper.fetch_posts("instagram", max_posts=1)
    if df is not None and not df.empty:
        print("SUCCESS: Fetched data.")
        print(df.iloc[0])
    else:
        print("FAILURE: No data fetched.")

if __name__ == "__main__":
    test()
