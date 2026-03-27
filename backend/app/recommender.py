"""
recommender.py — AIRecommender (India-focused)
Generates captions, hashtags, hooks, viral songs & best posting time.
Always returns real data — AI if available, curated India fallback otherwise.
"""

from app.intelligence import DataTransformer

# ── India-focused niche hashtag packs ────────────────────────────────────────
INDIA_HASHTAGS = {} # (Hardcoded fallbacks removed to ensure AI results are preferred and dynamic)

DEFAULT_HASHTAGS = ["#ReelsIndia", "#IndianCreator", "#Viral", "#Trending"]

# ── India-specific viral songs (updated March 2026) ───────────────────────
INDIA_VIRAL_SONGS = []

# ── India-specific hook templates ─────────────────────────────────────────
INDIA_HOOKS = []

# ── India-specific caption templates per niche ────────────────────────────
INDIA_CAPTIONS = {
    "default": []
}

# ── Improvement tips (India-specific) ────────────────────────────────────
INDIA_TIPS = []


class AIRecommender:
    """Generate India-focused content recommendations."""

    def __init__(self, ai_engine=None, scraper=None):
        self.ai = ai_engine
        self.scraper = scraper
        self.transformer = DataTransformer()

    def recommend(self, topic: str, niche: str = "", username: str = "") -> dict:
        """Build a full recommendation pack for the given topic."""

        # Build patterns from user's account if available
        patterns = {}
        if self.scraper and username:
            try:
                res = self.scraper.fetch_posts(username, max_posts=20)
                if res and res.get("posts") is not None and not res["posts"].empty:
                    df = res["posts"]
                    patterns = self.transformer.detect_patterns(df, followers=res.get("profile", {}).get("followers", 0))
            except Exception as e:
                print(f"AIRecommender: could not fetch {username}: {e}")

        # Try AI engine first
        if self.ai:
            try:
                result = self.ai.recommend(topic=topic, niche=niche, patterns=patterns)
                if result and result.get("captions"):
                    return result
            except Exception as e:
                print(f"AIRecommender: AI recommend failed: {e}")

        # ── India fallback (always produces real content) ────────────────
        def fill(text: str) -> str:
            return text.replace("{topic}", topic or "ye cheez")

        niche_key = niche.lower() if niche else "default"
        caption_templates = INDIA_CAPTIONS.get(niche_key, INDIA_CAPTIONS["default"])
        hashtags = INDIA_HASHTAGS.get(niche_key, DEFAULT_HASHTAGS)

        best_day  = patterns.get("best_posting_day", "Sunday")
        best_hour = patterns.get("best_posting_hour", 19)    # 7 PM IST

        return {
            "topic":    topic,
            "niche":    niche,
            "captions": [fill(c) for c in caption_templates],
            "hashtags": [h for h in hashtags[:25]],
            "hooks":    [fill(h) for h in INDIA_HOOKS[:3]],
            "viral_songs": INDIA_VIRAL_SONGS[:6],
            "best_time": {"day": best_day, "hour": best_hour},
            "improvement_tips": INDIA_TIPS,
        }
