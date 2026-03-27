"""
Debug script: opens a real Instagram post and prints all text that contains
numbers, so we can identify the correct selectors for likes and comments.
"""
from playwright.sync_api import sync_playwright
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Use an account you want to inspect
TEST_USERNAME = "instagram"

with sync_playwright() as p:
    user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "playwright_profile")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    # 1. Go to profile to get first post link
    page.goto(f"https://www.instagram.com/{TEST_USERNAME}/", timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    links = page.locator('a[href*="/p/"], a[href*="/reel/"]')
    first_href = None
    for i in range(min(links.count(), 20)):
        href = links.nth(i).get_attribute('href')
        if href:
            first_href = href
            break

    if not first_href:
        print("No posts found. Might need login.")
        context.close()
        exit()

    post_url = f"https://www.instagram.com{first_href}"
    print(f"\n=== Inspecting: {post_url} ===\n")
    page.goto(post_url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    # 2. Dump all text nodes that look like numbers (for likes/comments)
    texts = page.locator('span, a, div[role="button"]').all()
    number_re = re.compile(r'^[\d,\.]+[KkMm]?$')
    print("--- Number-like visible text and selectors ---")
    count = 0
    for el in texts:
        try:
            txt = el.inner_text().strip()
            if txt and number_re.match(txt):
                # Try to get aria-label
                label = el.get_attribute('aria-label') or ''
                print(f"  TEXT: {txt!r:20}  aria-label: {label!r}")
                count += 1
        except: pass
    print(f"\nTotal number-like texts: {count}")

    # 3. Dump all aria-labels containing "like" or "comment"
    print("\n--- aria-labels containing 'like' or 'comment' ---")
    for el in page.locator('[aria-label]').all():
        try:
            label = (el.get_attribute('aria-label') or '').lower()
            if 'like' in label or 'comment' in label:
                print(f"  aria-label: {label!r}  text: {el.inner_text().strip()!r}")
        except: pass

    # 4. Dump section inner text (where likes usually appear)
    print("\n--- section inner texts ---")
    for s in page.locator('section').all():
        try:
            txt = s.inner_text().strip()
            if txt and len(txt) < 200:
                print(f"  {txt!r}")
        except: pass

    context.close()
