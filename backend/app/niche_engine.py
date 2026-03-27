"""
niche_engine.py — NicheEngine
Scrapes top accounts in a given niche, extracts 50-100 posts,
and generates:
  - Best hashtag clusters
  - Common caption structures
  - Trending content ideas
  - Audience engagement patterns
"""

import pandas as pd
import re
from collections import Counter

from app.intelligence import DataTransformer
from app.trend_analyzer import NICHE_HASHTAGS

# India-specific content idea templates per niche (Fallbacks removed to ensure AI results are dynamic)
NICHE_CONTENT_IDEAS = {}
DEFAULT_CONTENT_IDEAS = []

DEFAULT_CONTENT_IDEAS = [
    "{niche} mein top Indian creators kya kar rahe hain?",
    "India mein {niche} ka future — kya sochte ho?",
    "Meri {niche} journey — honest story 🇮🇳",
    "Indian audience ke liye {niche} tips jo kaam karti hain",
    "{niche} challenge — 30 din, kya change hoga?",
]



class NicheEngine:
    """Research a niche and generate intelligence reports."""

    def __init__(self, scraper=None, ai_engine=None):
        self.scraper = scraper
        self.ai = ai_engine
        self.transformer = DataTransformer()

    def research(self, niche: str, max_posts: int = 50) -> dict:
        """Aggregate niche intelligence from hashtag search."""
        niche_lower = niche.lower()
        matched_key = next((k for k in NICHE_HASHTAGS.keys() if k in niche_lower), None)
        
        if matched_key:
            tags = [NICHE_HASHTAGS[matched_key]]
        else:
            clean = niche.replace("#", "")
            words = clean.split()
            tags = [clean.replace(" ", "")]
            if len(words) > 1:
                tags.extend([w for w in words if w][:2])

        if self.scraper is None:
            return {"error": "Scraper is not initialized via Instaloader."}
            
        try:
            res = self.scraper.fetch_hashtag_posts(tags, max_posts=max_posts)
            if not res or res.get("posts") is None or res["posts"].empty:
                print(f"DEBUG: NicheEngine scraper failed for {tags}. Using offline fallback.")
                return self._offline_result(niche)
            combined = res["posts"]
            combined["source_hashtag"] = tags[0]
            is_live = True
        except Exception as e:
            print(f"DEBUG: NicheEngine research error: {e}")
            return self._offline_result(niche)

        combined = self.transformer.add_engagement_rate(combined)

        # Top posts
        top_posts = self.transformer.top_posts(combined, n=10)

        # Hashtag clusters
        all_tags: list[str] = []
        captions = combined.get("caption", pd.Series([])).fillna("")
        for cap in captions:
            all_tags.extend(re.findall(r"#\w+", str(cap).lower()))
        hashtag_counts = Counter(all_tags)
        hashtags_high  = [h for h, c in hashtag_counts.most_common(10)]
        hashtags_niche = [h for h, c in hashtag_counts.most_common(50) if c == 1][:10]

        # Caption structure examples (top 5 captions)
        top_by_er = combined.nlargest(5, "engagement_rate")
        caption_examples = [str(c)[:200] for c in top_by_er.get("caption", pd.Series([])).fillna("")]

        # Content ideas
        ideas = NICHE_CONTENT_IDEAS.get(niche.lower(), [
            t.replace("{niche}", niche) for t in DEFAULT_CONTENT_IDEAS
        ])

        # AI enhancement
        ai_insights = ""
        if self.ai:
            try:
                ai_insights = self.ai.research_niche({
                    "niche": niche,
                    "top_hashtags": hashtags_high,
                    "top_captions": caption_examples,
                    "avg_engagement": round(float(combined["engagement_rate"].mean()), 2),
                })
            except Exception as e:
                print(f"NicheEngine: AI insight failed: {e}")

        return {
            "niche": niche,
            "hashtag_analyzed": ", ".join(tags),
            "total_posts": len(combined),
            "top_posts": top_posts,
            "hashtag_clusters": {
                "high_reach": hashtags_high,
                "niche_specific": hashtags_niche,
                "all": [{"hashtag": h, "count": c} for h, c in hashtag_counts.most_common(25)],
            },
            "caption_examples": caption_examples,
            "content_ideas": ideas,
            "ai_insights": ai_insights,
        }

    def _offline_result(self, niche: str) -> dict:
        ideas = NICHE_CONTENT_IDEAS.get(niche.lower(), [
            t.replace("{niche}", niche) for t in DEFAULT_CONTENT_IDEAS
        ])
        return {
            "is_live": False,
            "niche": niche,
            "hashtag_analyzed": NICHE_HASHTAGS.get(niche.lower(), niche.replace(" ", "")),
            "total_posts": 0,
            "top_posts": [],
            "hashtag_clusters": {"high_reach": [], "niche_specific": [], "all": []},
            "caption_examples": [],
            "content_ideas": ideas,
            "ai_insights": f"No live data available for '{niche}'. These content ideas are based on proven strategies for this niche.",
        }
