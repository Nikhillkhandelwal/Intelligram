from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://imginn.com/instagram/")
    page.wait_for_selector('.item')
    html = page.locator('.item').first.inner_html()
    print("ITEM HTML:")
    print(html)
    browser.close()
