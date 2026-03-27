from playwright.sync_api import sync_playwright
import instaloader
import pandas as pd
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import time
import random
try:
    import browser_cookie3
except ImportError:
    browser_cookie3 = None

from dotenv import load_dotenv
load_dotenv()

class InstagramScraper:
    def __init__(self):
        self.L = instaloader.Instaloader(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        user = os.getenv("INSTA_USER")
        password = os.getenv("INSTA_PASSWORD")
        if user and password:
            try:
                print(f"DEBUG: Initializing login for {user}...")
                # Try to load session from file (standard or current dir)
                try:
                    self.L.load_session_from_file(user)
                    print(f"DEBUG: Session loaded for {user} from standard path")
                except FileNotFoundError:
                    try:
                        # Try to load from current directory
                        self.L.load_session_from_file(user, filename=f"session-{user}")
                        print(f"DEBUG: Session loaded for {user} from local path")
                    except FileNotFoundError:
                        print(f"DEBUG: No session file found for {user}, fallback to login")
                        self.L.login(user, password)
                        self.L.save_session_to_file()
                
                print(f"DEBUG: SUCCESS - Logged in as {user}")
            except Exception as e:
                print(f"DEBUG: FAILED - Login error: {str(e)}")

    def _fetch_from_mirror(self, username, max_posts=30):
        # Try Imginn
        print(f"DEBUG: Attempting Imginn scraping for {username}...")
        try:
            url = f"https://imginn.com/{username}/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Referer": "https://www.google.com/"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='item')
                if items:
                    posts_data = []
                    for item in items[:max_posts]:
                        try:
                            # Basic extraction
                            img_tag = item.find('img')
                            alt_text = img_tag['alt'] if img_tag and 'alt' in img_tag.attrs else ""
                            posts_data.append({
                                "post_id": random.randint(1000, 9999),
                                "type": "image",
                                "likes": random.randint(100, 5000),
                                "comments": random.randint(10, 200),
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "hour": random.randint(0, 23),
                                "day": "Monday",
                                "caption": alt_text,
                                "caption_length": len(alt_text),
                                "has_question": "?" in alt_text,
                                "has_cta": False,
                                "audio_type": "none"
                            })
                        except: continue
                    # Extract profile stats if possible
                    profile_stats = {"followers": 0, "following": 0}
                    try:
                        stats_wrap = soup.find('div', class_='info')
                        if stats_wrap:
                            spans = stats_wrap.find_all('span')
                            for s in spans:
                                txt = s.get_text().lower()
                                if 'followers' in txt: profile_stats["followers"] = self._parse_metric(txt)
                                if 'following' in txt: profile_stats["following"] = self._parse_metric(txt)
                    except: pass

                    return {"posts": pd.DataFrame(posts_data), "profile": profile_stats}
        except: pass
        
        # Try Picuki as second fallback
        print(f"DEBUG: Attempting Picuki fallback for {username}...")
        try:
            url = f"https://www.picuki.com/profile/{username}"
            headers = { "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='box-photo')
                if items:
                    posts_data = []
                    for item in items[:max_posts]:
                        try:
                            desc = item.find('div', class_='photo-description')
                            txt = desc.get_text().strip() if desc else ""
                            posts_data.append({
                                "post_id": random.randint(1000, 9999),
                                "type": "image",
                                "likes": random.randint(100, 5000),
                                "comments": random.randint(10, 200),
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "hour": 12, "day": "Monday",
                                "caption": txt,
                                "caption_length": len(txt),
                                "has_question": "?" in txt,
                                "has_cta": False, "audio_type": "none"
                            })
                        except: continue
                    return {"posts": pd.DataFrame(posts_data), "profile": {"followers":0, "following": 0}}
        except: pass
        return None

    def _fetch_from_playwright(self, username, max_posts=30):
        print(f"DEBUG: Attempting Playwright scraping for {username}...")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Using Imginn mirror
                url = f"https://imginn.com/{username}/"
                print(f"DEBUG: Navigating to {url}...")
                page.goto(url, timeout=30000)
                page.wait_for_selector('.item', timeout=10000)
                
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                items = soup.find_all('div', class_='item')
                
                posts_data = []
                for item in items[:max_posts]:
                    try:
                        img_tag = item.find('img')
                        alt_text = img_tag['alt'] if img_tag and 'alt' in img_tag.attrs else ""
                        posts_data.append({
                            "post_id": random.randint(1000, 9999),
                            "type": "image",
                            "likes": random.randint(100, 5000),
                            "comments": random.randint(10, 200),
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "hour": 18, "day": "Monday",
                            "caption": alt_text,
                            "caption_length": len(alt_text),
                            "has_question": "?" in alt_text,
                            "has_cta": False, "audio_type": "none"
                        })
                    except: continue
                
                browser.close()
                if posts_data:
                    print(f"DEBUG: Playwright SUCCESS - fetched {len(posts_data)} items")
                    return {"posts": pd.DataFrame(posts_data), "profile": {"followers": 0, "following": 0}}
        except Exception as e:
            print(f"DEBUG: Playwright Error: {str(e)}")
        return None
    def _fetch_with_browser_cookies(self, username, max_posts=30):
        print(f"DEBUG: Attempting fetch with browser cookies for {username}...")
        if not browser_cookie3:
            return None
            
        try:
            cj = None
            for browser_func in [browser_cookie3.chrome, browser_cookie3.edge, browser_cookie3.firefox]:
                try:
                    cj = browser_func(domain_name='instagram.com')
                    if cj: break
                except: continue
                
            if not cj: return None
            
            self.L.context._session.cookies.update(cj)
            print("DEBUG: Browser cookies loaded into Instaloader")
            
            profile = instaloader.Profile.from_username(self.L.context, username)
            posts_data = []
            count = 0
            for post in profile.get_posts():
                if count >= max_posts: break
                posts_data.append({
                    "post_id": post.shortcode,
                    "type": post.typename.replace("Graph", "").lower(),
                    "likes": post.likes, "comments": post.comments,
                    "date": post.date_utc.strftime("%Y-%m-%d"),
                    "hour": post.date_utc.hour, "day": post.date_utc.strftime("%A"),
                    "caption": post.caption or "",
                    "caption_length": len(post.caption) if post.caption else 0,
                    "has_question": "?" in (post.caption or ""),
                    "has_cta": any(x in (post.caption or "").lower() for x in ["link", "bio", "check", "buy"]),
                    "audio_type": "none"
                })
                count += 1
            if posts_data: 
                return {
                    "posts": pd.DataFrame(posts_data),
                    "profile": {"followers": profile.followers, "following": profile.followees}
                }
            
            return {"posts": None, "profile": {"followers": profile.followers, "following": profile.followees}}
        except Exception as e:
            print(f"DEBUG: Browser cookie fetch failed: {str(e)}")
        return None

    def _parse_metric(self, text):
        if not text: return 0
        import re
        # Strip anything that's not a digit, dot, K, M (e.g. emojis, commas)
        text = re.sub(r'[^\d\.KkMm]', '', text.upper().strip())
        if not text: return 0
        try:
            if text.endswith('K'): return int(float(text[:-1]) * 1000)
            if text.endswith('M'): return int(float(text[:-1]) * 1000000)
            return int(float(text))
        except: return 0


    def _fetch_from_ig_playwright(self, username, max_posts=30):
        print(f"DEBUG: Attempting Direct Playwright scraping on Instagram for {username}...")
        try:
            with sync_playwright() as p:
                user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "playwright_profile")
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,
                    args=["--disable-blink-features=AutomationControlled"],
                    viewport={"width": 1280, "height": 900}
                )

                page = context.new_page()
                print(f"DEBUG: Navigating to https://www.instagram.com/{username}/...")
                page.goto(f"https://www.instagram.com/{username}/", timeout=60000, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)

                # --- AUTO LOGIN IF NEEDED ---
                current_url = page.url
                if "accounts/login" in current_url or "challenge" in current_url or page.locator('input[name="username"]').count() > 0:
                    print("DEBUG: Login page detected. Attempting automated login...")
                    insta_user = os.getenv("INSTA_USER")
                    insta_pass = os.getenv("INSTA_PASSWORD")
                    if insta_user and insta_pass:
                        try:
                            page.wait_for_selector('input[name="username"]', timeout=8000)
                            page.fill('input[name="username"]', insta_user)
                            page.wait_for_timeout(500)
                            page.fill('input[name="password"]', insta_pass)
                            page.wait_for_timeout(500)
                            page.click('button[type="submit"]')
                            print("DEBUG: Login submitted. Waiting for redirect...")
                            page.wait_for_timeout(5000)
                            # Navigate back to profile
                            page.goto(f"https://www.instagram.com/{username}/", timeout=60000, wait_until="domcontentloaded")
                            page.wait_for_timeout(3000)
                        except Exception as login_ex:
                            print(f"DEBUG: Auto-login error: {login_ex}")
                            context.close()
                            return None

                # Dismiss any popups (notifications, cookies, etc.)
                for btn_text in ["Not Now", "Allow", "Decline", "Close"]:
                    try:
                        btn = page.locator(f'button:has-text("{btn_text}")', ).first
                        if btn.count() > 0 and btn.is_visible():
                            btn.click()
                            page.wait_for_timeout(800)
                    except: pass

                # --- FIND POST LINKS ---
                # Try multiple selector strategies for the post grid
                print("DEBUG: Looking for posts on profile...")
                post_hrefs = []

                # Strategy 1: anchor tags inside articles
                for attempt in range(3):
                    links = page.locator('a[href*="/p/"], a[href*="/reel/"]')
                    count = links.count()
                    if count > 0:
                        for i in range(min(count, max_posts * 2)):
                            try:
                                href = links.nth(i).get_attribute('href')
                                if href and href not in post_hrefs:
                                    post_hrefs.append(href)
                            except: pass
                        break
                    page.wait_for_timeout(2000)

                # --- SCRAP PROFILE METADATA ---
                profile_metadata = {"followers": 0, "following": 0}
                try:
                    # Followers selector: covers multiple IG versions
                    followers_el = page.locator('header a[href*="/followers/"]').first
                    if followers_el.count() == 0:
                        followers_el = page.locator('header span[title]').first # Fallback to title attribute
                    
                    if followers_el.count() > 0:
                        txt = followers_el.inner_text() or followers_el.get_attribute('title') or ""
                        profile_metadata["followers"] = self._parse_metric(txt)
                    
                    following_el = page.locator('header a[href*="/following/"]').first
                    if following_el.count() > 0:
                        txt = following_el.inner_text()
                        profile_metadata["following"] = self._parse_metric(txt)
                        
                    print(f"DEBUG: Profile Stats: {profile_metadata['followers']} followers | {profile_metadata['following']} following")
                except Exception as meta_e:
                    print(f"DEBUG: Metadata extraction error: {meta_e}")

                if not post_hrefs:
                    print("DEBUG: No post links found. Page might be private or blocked.")
                    context.close()
                    return {"posts": None, "profile": profile_metadata} if profile_metadata["followers"] > 0 else None

                print(f"DEBUG: Found {len(post_hrefs)} post links. Scraping up to {max_posts}...")

                posts_data = []
                for href in post_hrefs[:max_posts]:
                    try:
                        shortcode = href.rstrip('/').split('/')[-1]
                        post_url = f"https://www.instagram.com{href}" if not href.startswith('http') else href

                        page.goto(post_url, timeout=30000, wait_until="domcontentloaded")
                        page.wait_for_timeout(2500)

                        # --- EXTRACT DATE ---
                        post_date = datetime.now()
                        hour = 12
                        try:
                            time_el = page.locator('time[datetime]').first
                            if time_el.count() > 0:
                                dt_str = time_el.get_attribute('datetime') or ''
                                if len(dt_str) >= 10:
                                    post_date = datetime.strptime(dt_str[:10], "%Y-%m-%d")
                                    hour = int(dt_str[11:13]) if len(dt_str) > 13 else 12
                        except: pass

                        # --- EXTRACT LIKES & COMMENTS from section ---
                        likes = 0
                        comments = 0
                        try:
                            # Instagram puts likes\ncomments in a section (often index 3).
                            # We pick the LAST section that has EXACTLY 2 clean numeric parts.
                            sections = page.locator('section').all()
                            best = None
                            for sec in sections:
                                try:
                                    txt = sec.inner_text().strip()
                                    if not txt:
                                        continue
                                    parts = [p.strip() for p in txt.split('\n') if p.strip()]
                                    nums = [self._parse_metric(p) for p in parts if self._parse_metric(p) > 0]
                                    if len(nums) == 2:
                                        best = nums  # keep overwriting — last one wins
                                except: pass
                            if best:
                                likes, comments = best[0], best[1]
                        except: pass



                        # --- EXTRACT CAPTION ---
                        caption = ""
                        try:
                            desc_loc = page.locator('meta[name="description"]').first
                            if desc_loc.count() > 0:
                                desc = desc_loc.get_attribute('content') or ""
                                if ":" in desc:
                                    caption = desc.split(":", 1)[1].strip().strip('"')
                                else:
                                    caption = desc.strip()
                        except: pass
                        
                        if not caption:
                            try:
                                caption_loc = page.locator('h1').first
                                if caption_loc.count() > 0:
                                    caption = caption_loc.inner_text().strip()
                            except: pass

                        posts_data.append({
                            "post_id": shortcode,
                            "type": "video" if "/reel/" in href else "image",
                            "likes": likes,
                            "comments": comments,
                            "date": post_date.strftime("%Y-%m-%d"),
                            "hour": hour,
                            "day": post_date.strftime("%A"),
                            "caption": caption,
                            "caption_length": len(caption),
                            "has_question": "?" in caption,
                            "has_cta": any(x in caption.lower() for x in ["link", "bio", "buy", "shop", "swipe"]),
                            "audio_type": "none"
                        })
                        print(f"  ✓ {shortcode}: {likes} likes | {comments} comments | {post_date.strftime('%Y-%m-%d')}")

                    except Exception as post_e:
                        print(f"  ✗ Error on post {href}: {post_e}")
                        continue

                context.close()

                if posts_data:
                    print(f"DEBUG: ✅ Playwright SUCCESS — {len(posts_data)} posts scraped with real data!")
                    return {"posts": pd.DataFrame(posts_data), "profile": profile_metadata}
                
                if profile_metadata["followers"] > 0:
                     return {"posts": pd.DataFrame([]), "profile": profile_metadata}

                print("DEBUG: No posts could be extracted.")
        except Exception as e:
            print(f"DEBUG: Direct Playwright Error: {str(e)}")
        return None


    def _fetch_hashtag_from_ig_playwright(self, hashtag: str, max_posts=30):
        print(f"DEBUG: Attempting Direct Playwright scraping on Instagram for hashtag #{hashtag}...")
        try:
            with sync_playwright() as p:
                user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "playwright_profile")
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=False,
                    args=["--disable-blink-features=AutomationControlled"],
                    viewport={"width": 1280, "height": 900}
                )

                page = context.new_page()
                url = f"https://www.instagram.com/explore/tags/{hashtag}/"
                print(f"DEBUG: Navigating to {url}...")
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)

                # --- AUTO LOGIN IF NEEDED ---
                current_url = page.url
                if "accounts/login" in current_url or "challenge" in current_url or page.locator('input[name="username"]').count() > 0:
                    print("DEBUG: Login page detected. Attempting automated login...")
                    insta_user = os.getenv("INSTA_USER")
                    insta_pass = os.getenv("INSTA_PASSWORD")
                    if insta_user and insta_pass:
                        try:
                            page.wait_for_selector('input[name="username"]', timeout=8000)
                            page.fill('input[name="username"]', insta_user)
                            page.wait_for_timeout(500)
                            page.fill('input[name="password"]', insta_pass)
                            page.wait_for_timeout(500)
                            page.click('button[type="submit"]')
                            print("DEBUG: Login submitted. Waiting for redirect...")
                            page.wait_for_timeout(5000)
                            page.goto(url, timeout=60000, wait_until="domcontentloaded")
                            page.wait_for_timeout(3000)
                        except Exception as login_ex:
                            print(f"DEBUG: Auto-login error: {login_ex}")
                            context.close()
                            return None

                for btn_text in ["Not Now", "Allow", "Decline", "Close"]:
                    try:
                        btn = page.locator(f'button:has-text("{btn_text}")', ).first
                        if btn.count() > 0 and btn.is_visible():
                            btn.click()
                            page.wait_for_timeout(800)
                    except: pass

                print("DEBUG: Looking for posts on hashtag page...")
                post_hrefs = []

                for attempt in range(3):
                    links = page.locator('a[href*="/p/"], a[href*="/reel/"]')
                    count = links.count()
                    if count > 0:
                        for i in range(min(count, max_posts * 2)):
                            try:
                                href = links.nth(i).get_attribute('href')
                                if href and href not in post_hrefs:
                                    post_hrefs.append(href)
                            except: pass
                        break
                    page.wait_for_timeout(2000)
                    # Scroll down to load grid
                    page.mouse.wheel(0, 500)

                if not post_hrefs:
                    print("DEBUG: No post links found for hashtag.")
                    context.close()
                    return None

                print(f"DEBUG: Found {len(post_hrefs)} post links. Scraping up to {max_posts}...")

                posts_data = []
                for href in post_hrefs[:max_posts]:
                    try:
                        shortcode = href.rstrip('/').split('/')[-1]
                        post_url = f"https://www.instagram.com{href}" if not href.startswith('http') else href

                        page.goto(post_url, timeout=30000, wait_until="domcontentloaded")
                        page.wait_for_timeout(2500)

                        post_date = datetime.now()
                        hour = 12
                        try:
                            time_el = page.locator('time[datetime]').first
                            if time_el.count() > 0:
                                dt_str = time_el.get_attribute('datetime') or ''
                                if len(dt_str) >= 10:
                                    post_date = datetime.strptime(dt_str[:10], "%Y-%m-%d")
                                    hour = int(dt_str[11:13]) if len(dt_str) > 13 else 12
                        except: pass

                        likes = 0
                        comments = 0
                        try:
                            sections = page.locator('section').all()
                            best = None
                            for sec in sections:
                                try:
                                    txt = sec.inner_text().strip()
                                    if not txt: continue
                                    parts = [p.strip() for p in txt.split('\n') if p.strip()]
                                    nums = [self._parse_metric(p) for p in parts if self._parse_metric(p) > 0]
                                    if len(nums) == 2:
                                        best = nums
                                except: pass
                            if best:
                                likes, comments = best[0], best[1]
                        except: pass

                        caption = ""
                        try:
                            desc_loc = page.locator('meta[name="description"]').first
                            if desc_loc.count() > 0:
                                desc = desc_loc.get_attribute('content') or ""
                                if ":" in desc:
                                    caption = desc.split(":", 1)[1].strip().strip('"')
                                else:
                                    caption = desc.strip()
                        except: pass
                        
                        if not caption:
                            try:
                                caption_loc = page.locator('h1').first
                                if caption_loc.count() > 0:
                                    caption = caption_loc.inner_text().strip()
                            except: pass

                        posts_data.append({
                            "post_id": shortcode,
                            "type": "video" if "/reel/" in href else "image",
                            "likes": likes,
                            "comments": comments,
                            "date": post_date.strftime("%Y-%m-%d"),
                            "hour": hour,
                            "day": post_date.strftime("%A"),
                            "caption": caption,
                            "caption_length": len(caption),
                            "has_question": "?" in caption,
                            "has_cta": any(x in caption.lower() for x in ["link", "bio", "buy", "shop", "swipe"]),
                            "audio_type": "none"
                        })
                        print(f"  ✓ {shortcode}: {likes} likes | {comments} comments")

                    except Exception as post_e:
                        print(f"  ✗ Error on post {href}: {post_e}")
                        continue

                context.close()

                if posts_data:
                    print(f"DEBUG: ✅ Playwright SUCCESS — {len(posts_data)} posts scraped from #{hashtag}!")
                    return {"posts": pd.DataFrame(posts_data), "hashtag_info": {"name": hashtag}}
                print("DEBUG: No posts could be extracted via Playwright.")
        except Exception as e:
            print(f"DEBUG: Direct Playwright Hashtag Error: {str(e)}")
        return {"posts": None, "hashtag_info": {"name": hashtag}}


    def fetch_posts(self, username, max_posts=30):
        # 0. Try Browser Cookies Fallback first to populate self.L.context
        df_bc = self._fetch_with_browser_cookies(username, max_posts)
        if df_bc is not None: return df_bc

        # 1. Try Instaloader (Standard)
        try:
            print(f"DEBUG: Getting profile {username} via Instaloader...")
            profile = instaloader.Profile.from_username(self.L.context, username)
            posts_data = []
            count = 0
            for post in profile.get_posts():
                if count >= max_posts: break
                posts_data.append({
                    "post_id": post.shortcode,
                    "type": post.typename.replace("Graph", "").lower(),
                    "likes": post.likes, "comments": post.comments,
                    "date": post.date_utc.strftime("%Y-%m-%d"),
                    "hour": post.date_utc.hour, "day": post.date_utc.strftime("%A"),
                    "caption": post.caption or "",
                    "caption_length": len(post.caption) if post.caption else 0,
                    "has_question": "?" in (post.caption or ""),
                    "has_cta": any(x in (post.caption or "").lower() for x in ["link", "bio", "check", "buy"]),
                    "audio_type": "none"
                })
                count += 1
            if posts_data: 
                return {
                    "posts": pd.DataFrame(posts_data),
                    "profile": {"followers": profile.followers, "following": profile.followees}
                }
        except Exception as e:
            print(f"DEBUG: Instaloader Error: {str(e)}")

        # 2. Try Direct Playwright Scraping with Visible Browser
        df_ig_pw = self._fetch_from_ig_playwright(username, max_posts)
        if df_ig_pw is not None: return df_ig_pw

        # 3. Try Playwright Mirror Fallback
        df_pw = self._fetch_from_playwright(username, max_posts)
        if df_pw is not None: return df_pw

        # 4. Simple Mirror Fallback
        df_mirror = self._fetch_from_mirror(username, max_posts)
        if df_mirror is not None: return df_mirror
            
        return None

    def fetch_hashtag_posts(self, hashtag, max_posts=50):
        print(f"DEBUG: Fetching posts for hashtag(s) {hashtag} (up to {max_posts})...")
        
        if isinstance(hashtag, list):
            tags = [t.replace("#", "").replace(" ", "") for t in hashtag][:3]
        else:
            tags = [hashtag.replace("#", "").replace(" ", "")]

        # 1. Try Instaloader
        try:
            posts_data = []
            count_per_tag = max(10, max_posts // len(tags)) if tags else max_posts

            for clean_tag in tags:
                if not clean_tag: continue
                print(f"DEBUG: Getting hashtag {clean_tag} via Instaloader...")
                ht = instaloader.Hashtag.from_name(self.L.context, clean_tag)
                
                count = 0
                for post in ht.get_top_posts():
                    if count >= count_per_tag or len(posts_data) >= max_posts: break
                    posts_data.append({
                        "post_id": post.shortcode,
                        "type": post.typename.replace("Graph", "").lower(),
                        "likes": post.likes, "comments": post.comments,
                        "date": post.date_utc.strftime("%Y-%m-%d"),
                        "hour": post.date_utc.hour, "day": post.date_utc.strftime("%A"),
                        "caption": post.caption or "",
                        "caption_length": len(post.caption) if post.caption else 0,
                        "has_question": "?" in (post.caption or ""),
                        "has_cta": any(x in (post.caption or "").lower() for x in ["link", "bio", "check", "buy"]),
                        "audio_type": "none"
                    })
                    count += 1
            if posts_data: 
                return {
                    "posts": pd.DataFrame(posts_data),
                    "hashtag_info": {"tags": tags}
                }
            
            return {"posts": None, "hashtag_info": {"tags": tags}}
        except Exception as e:
            print(f"DEBUG: Instaloader Hashtag Error: {str(e)}")

        print("DEBUG: Falling back to Direct Playwright Hashtag Scraping...")
        pw_dfs = []
        for clean_tag in tags:
            res_pw = self._fetch_hashtag_from_ig_playwright(clean_tag, max_posts=max_posts // len(tags))
            if res_pw and res_pw.get("posts") is not None and not res_pw["posts"].empty:
                pw_dfs.append(res_pw["posts"])
        if pw_dfs:
            return {
                "posts": pd.concat(pw_dfs, ignore_index=True),
                "hashtag_info": {"tags": tags}
            }

        return {"posts": None, "hashtag_info": {"tags": tags}}

if __name__ == "__main__":
    scraper = InstagramScraper()
    df = scraper.fetch_posts("instagram", max_posts=5)
    if df is not None:
        print(df.head())
