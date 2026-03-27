from playwright.sync_api import sync_playwright
import time
import json

def test_hover():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # NOTE: Without cookies, this will redirect to login.
        # But for test purposes, let's load cookies from our session-instagram file
        import browser_cookie3
        try:
            cj = browser_cookie3.chrome(domain_name='instagram.com')
            context.add_cookies([{"name": c.name, "value": c.value, "domain": c.domain, "path": c.path} for c in cj])
        except: pass

        page.goto('https://www.instagram.com/garyvee/', timeout=60000)
        page.wait_for_selector('article a', timeout=15000)
        
        links = page.locator('article a')
        count = links.count()
        print(f"Found {count} posts.")
        
        posts = []
        for i in range(min(3, count)):
            el = links.nth(i)
            # Hover to reveal likes/comments
            el.hover()
            page.wait_for_timeout(500)
            
            # The ul appears inside the link when hovered
            # It usually has class like "x1qjc9v5" etc.
            # We can extract all numbers from inside the <a> tag
            text = el.inner_text()
            print(f"Post {i}: {text}")

if __name__ == '__main__':
    test_hover()
