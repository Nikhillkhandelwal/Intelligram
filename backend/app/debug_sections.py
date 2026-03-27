"""
Dump all section inner_text from a real post to identify correct metrics sections.
"""
from playwright.sync_api import sync_playwright
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

TEST_USERNAME = "bicepssandbanter"

with sync_playwright() as p:
    user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "playwright_profile")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()
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
        print("No posts found!")
        context.close()
        exit()

    post_url = f"https://www.instagram.com{first_href}"
    print(f"\n=== Post: {post_url} ===\n")
    page.goto(post_url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    print("--- All <section> inner texts ---")
    for i, sec in enumerate(page.locator('section').all()):
        try:
            txt = sec.inner_text().strip()
            if txt:
                print(f"  Section[{i}]: {txt!r}")
        except: pass

    print("\n--- All <span> texts with aria-label ---")
    for el in page.locator('span[aria-label]').all():
        try:
            label = el.get_attribute('aria-label') or ''
            txt = el.inner_text().strip()
            print(f"  aria-label={label!r} => {txt!r}")
        except: pass

    print("\n--- Buttons with like/comment in aria-label ---")
    for el in page.locator('button, div[role=button]').all():
        try:
            label = (el.get_attribute('aria-label') or '').lower()
            if 'like' in label or 'comment' in label:
                txt = el.inner_text().strip()
                print(f"  aria-label={label!r} => text={txt!r}")
        except: pass

    context.close()
