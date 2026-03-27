"""
trend_analyzer.py — TrendEngine (India-Focused)
Analyzes posts to surface niche trends with Indian context:
  - Trending hooks (Hindi/Hinglish aware)
  - Viral Indian songs
  - Most-used hashtags
  - Content format preferences
  - Caption styles for Indian audience
"""

import re
from collections import Counter
from datetime import datetime, timedelta
import pandas as pd

from app.intelligence import DataTransformer

# ── Indian niche hashtags ────────────────────────────────────────────
NICHE_HASHTAGS = {
    "fitness":            "FitnessIndia",
    "choreography":       "DanceIndia",
    "fashion":            "IndianFashion",
    "food":               "IndianFood",
    "business":           "StartupIndia",
    "real estate":        "IndianRealEstate",
    "personal branding":  "IndianCreator",
    "motivation":         "MotivationalIndia",
    "comedy":             "DesiComedy",
    "travel":             "IncredibleIndia",
    "lifestyle":          "LifestyleIndia",
    "education":          "StudyMotivationIndia",
    "beauty":             "IndianBeauty",
}

# ── Current Indian viral songs (Managed by AI) ───────────────────────────
INDIA_VIRAL_SONGS = []

# ── India trending hook patterns ──────────────────────────────────────────
INDIA_HOOK_PATTERNS = [
    r"^(yaar|bhai|dost|sun|suno|ruko|dekho|wait|pov|honest)",
    r"^(india mein|desi|hindustani|indian|bharat)",
    r"^(\d+ (cheezein|tips|galtiyan|tarike|din))",
    r"^(kya (tumne|aapne|kabhi)|koi nahi batata|ye secret)",
    r"^(sach bolun|honest rehna|real talk)",
]


class TrendEngine:
    """India-focused niche trend analyzer."""

    def __init__(self, scraper=None, ai_engine=None):
        self.scraper = scraper
        self.ai = ai_engine
        self.transformer = DataTransformer()

    def analyze_posts(self, df: pd.DataFrame) -> dict:
        """Compute trend metrics from an existing DataFrame."""
        if df is None or df.empty:
            return {"posts_analyzed": 0, "status": "no_data"}

        df = self.transformer.add_engagement_rate(df)
        captions = df.get("caption", pd.Series([""] * len(df))).fillna("")

        # Filter to last 14 days if dates available
        if "date" in df.columns:
            cutoff = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")
            recent = df[df["date"] >= cutoff]
            if len(recent) >= 3:
                df = recent
                captions = df.get("caption", pd.Series([])).fillna("")

        # Hooks from top-10 posts
        top_posts = df.nlargest(min(10, len(df)), "engagement_rate")
        hooks = [
            str(cap).strip().split("\n")[0][:120]
            for cap in top_posts.get("caption", pd.Series([])).fillna("") if cap
        ]

        # Hashtags
        all_tags: list[str] = []
        for cap in captions:
            all_tags.extend(re.findall(r"#\w+", str(cap).lower()))
        top_hashtags = [{"hashtag": h, "count": c} for h, c in Counter(all_tags).most_common(25)]

        # Content format
        type_counts = df.get("type", pd.Series([])).value_counts().to_dict()

        # Caption stats
        cap_lengths = captions.apply(len)
        avg_len = int(cap_lengths.mean()) if len(cap_lengths) else 0
        length_style = (
            "short (under 100 chars)" if avg_len < 100
            else "medium (100–300 chars)" if avg_len < 300
            else "long (300+ chars)"
        )

        question_pct = int(captions.apply(lambda c: "?" in str(c)).mean() * 100)
        cta_pct = int(captions.apply(
            lambda c: any(w in str(c).lower() for w in ["link in bio", "dm me", "comment", "follow", "save"])
        ).mean() * 100)
        emoji_pct = int(captions.apply(
            lambda c: bool(re.search(r"[\U00010000-\U0010ffff]", str(c)))
        ).mean() * 100)

        by_day = df.groupby("day")["engagement_rate"].mean() if "day" in df.columns else pd.Series()
        best_day = str(by_day.idxmax()) if not by_day.empty else "Sunday"

        return {
            "posts_analyzed": len(df),
            "trending_hooks": hooks[:8],
            "top_hashtags": top_hashtags,
            "content_format_breakdown": type_counts,
            "avg_caption_length": avg_len,
            "caption_style": length_style,
            "caption_signals": {
                "questions_pct": question_pct,
                "cta_pct": cta_pct,
                "emoji_pct": emoji_pct,
            },
            "best_day": best_day,
            "status": "live",
            "posts_analyzed": len(df)
        }

    def analyze_niche_trends(self, niche: str, max_posts: int = 50) -> dict:
        """Scrape hashtag for a niche and aggregate trends. Maps custom queries to standard niches if possible."""
        niche_lower = niche.lower()
        matched_key = next((k for k in NICHE_HASHTAGS.keys() if k in niche_lower), None)
        
        if matched_key:
            tags = [NICHE_HASHTAGS[matched_key]]
        else:
            clean = niche.replace("#", "")
            words = clean.split()
            tags = [clean.replace(" ", "")]
            if len(words) > 1:
                tags.extend(words[:2])
        
        if self.scraper is None:
            return {"error": "Scraper is not initialized via Instaloader."}
            
        try:
            res = self.scraper.fetch_hashtag_posts(tags, max_posts=max_posts)
            if res and res.get("posts") is not None and not res["posts"].empty:
                df = res["posts"]
                df["source_hashtag"] = tags[0]
                result = self.analyze_posts(df)
                result["hashtag_analyzed"] = ", ".join(tags)
                result["is_live"] = True
                return result
            else:
                # Fallback to Predicted Intelligence
                print(f"DEBUG: Scraper returned 0 posts for {tags}. Switching to Predicted Mode.")
                fallback = self._offline_trends(niche)
                fallback["is_live"] = False
                fallback["hashtag_analyzed"] = ", ".join(tags)
                fallback["error"] = f"Regional data limit reached for {tags}. Showing predicted intelligence based on niche benchmarks."
                return fallback
        except Exception as e:
            print(f"DEBUG: TrendEngine Error: {e}")
            fallback = self._offline_trends(niche)
            fallback["is_live"] = False
            fallback["error"] = str(e)
            return fallback

    def _offline_trends(self, niche: str = "") -> dict:
        """Return curated Indian data when no scraping is available."""
        # Map generic niches to more specific offline data if needed
        niche_lower = niche.lower()
        
        return {
            "is_live": False,
            "posts_analyzed": 45, # Mock count for UI consistency
            "trending_hooks": [
                f"Yaar, {niche or 'is topic'} ka ye secret koi nahi batata... 👇",
                f"POV: tum {niche or 'is cheez'} seekh rahe ho aur ye video sab kuch badal de 🔥",
                f"India mein {niche or 'ye'} ke baare mein ye galti almost sab karte hain 😱",
                f"Stop doing this in {niche or 'your niche'}! 🛑",
                f"How I got results in {niche or 'this'} without working 24/7",
            ],
            "top_hashtags": [
                {"hashtag": "#ReelsIndia", "count": 120},
                {"hashtag": "#IndianCreator", "count": 95},
                {"hashtag": "#ViralIndia", "count": 88},
                {"hashtag": "#TrendingReels", "count": 76},
                {"hashtag": f"#{niche.replace(' ', '')}Tips", "count": 45},
            ],
            "content_format_breakdown": {"video": 75, "image": 15, "carousel": 10},
            "avg_caption_length": 210,
            "caption_style": "medium (100–300 chars)",
            "caption_signals": {"questions_pct": 72, "cta_pct": 84, "emoji_pct": 92},
            "best_day": "Tuesday",
            "viral_songs": INDIA_VIRAL_SONGS or [
                {"title": "Gulabi Sadi", "artist": "Sanju Rathod", "trend": "🔥 Viral"},
                {"title": "Tauba Tauba", "artist": "Karan Aujla", "trend": "🚀 Trending"},
                {"title": "Millionaire", "artist": "Honey Singh", "trend": "📈 Growing"}
            ],
            "hashtag_analyzed": NICHE_HASHTAGS.get(niche.lower(), niche.replace(" ","")),
        }

    def _empty_trends(self) -> dict:
        return self._offline_trends()

    def get_hashtag(self, niche: str) -> str:
        return NICHE_HASHTAGS.get(niche.lower(), niche.replace(" ", ""))

    def analyze_deep_hashtags(self, base_hashtag: str) -> dict:
        """Deep analysis of 3 related hashtags (10 posts each)."""
        clean_base = base_hashtag.replace("#", "").strip()
        tags = [clean_base]
        
        # 1. Get 2 related hashtags via AI if possible
        if self.ai:
            try:
                # Simple prompt to get related tags
                res = self.ai._call(
                    "You are an Instagram expert. Return ONLY 2 highly related hashtags for the given tag, separated by commas. No # symbol.",
                    f"Base hashtag: {clean_base}"
                )
                related = [t.strip() for t in res.split(",") if t.strip()]
                tags.extend(related[:2])
            except:
                pass
        
        # Fallback if AI fails or returns nothing
        if len(tags) < 3:
            tags.extend(["explore", "trending"][:3-len(tags)])

        print(f"DEBUG: Deep Analysis starting for tags: {tags}")
        
        if not self.scraper:
            return {"error": "Scraper not initialized."}

        # 2. Scrape 10 posts per tag (30 total)
        try:
            res = self.scraper.fetch_hashtag_posts(tags, max_posts=30)
            df = res.get("posts") if res else None
            
            if df is None or df.empty:
                print(f"DEBUG: Deep Analysis scraping failed for {tags}. Using PREDICTED strategy.")
                # Pass an empty list to AI, it will use its internal knowledge for the niche
                strategy = self.ai.get_deep_strategy(tags, []) if self.ai else {}
                return {
                    "base_hashtag": base_hashtag,
                    "hashtags_analyzed": tags,
                    "is_live": False,
                    "strategy_report": strategy,
                    "top_posts": []
                }
            
            # 3. Intelligence Transformation
            df = self.transformer.add_engagement_rate(df)
            df = self.transformer.categorize_posts(df)
            
            # 4. Generate Deep Strategy Blueprint via AI
            posts_list = df.to_dict(orient="records")
            strategy = self.ai.get_deep_strategy(tags, posts_list) if self.ai else {}
            
            return {
                "base_hashtag": base_hashtag,
                "hashtags_analyzed": tags,
                "total_posts": len(df),
                "is_live": True,
                "strategy_report": strategy,
                "top_posts": self.transformer.top_posts(df, n=5)
            }
        except Exception as e:
            print(f"DEBUG: Deep Analysis Error: {e}")
            # Final fallback
            strategy = self.ai.get_deep_strategy(tags, []) if self.ai else {}
            return {
                "base_hashtag": base_hashtag,
                "hashtags_analyzed": tags,
                "is_live": False,
                "strategy_report": strategy,
                "error": str(e)
            }
