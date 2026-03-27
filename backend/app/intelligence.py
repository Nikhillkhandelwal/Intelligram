"""
intelligence.py — DataTransformer
Converts raw scraped post DataFrames into structured insights:
  - Top-performing posts by engagement rate
  - Content categorization (educational, entertainment, promotional, storytelling)
  - Pattern detection (hooks, caption length, hashtags)
"""

import re
import pandas as pd
from collections import Counter
from datetime import datetime


# ── Keyword dictionaries for content categorization ────────────────────────
CATEGORY_KEYWORDS = {
    "educational": [
        "how to", "tips", "learn", "guide", "step", "tutorial", "trick",
        "secret", "why", "what is", "explained", "understand", "fact",
        "did you know", "strategy", "method", "technique", "insight"
    ],
    "entertainment": [
        "funny", "lol", "haha", "vibe", "mood", "challenge", "trend",
        "dance", "prank", "reaction", "skit", "comedy", "fun", "enjoy",
        "watch this", "unbelievable", "crazy", "omg", "wow"
    ],
    "promotional": [
        "buy", "shop", "sale", "discount", "offer", "link in bio", "promo",
        "limited", "deal", "click", "order", "available now", "dm me",
        "collab", "sponsor", "ad", "paid", "product", "service"
    ],
    "storytelling": [
        "story", "journey", "i was", "i remember", "it all started", "my life",
        "last year", "when i", "looking back", "never forget", "this is me",
        "honest", "real talk", "vulnerable", "confess", "truth", "struggle"
    ],
}

HOOK_PATTERNS = [
    r"^(stop|wait|warning|pov|plot twist|nobody talks about|you need to|this is why|the truth about)",
    r"^(how (i|to|we)|i (went|did|tried|made)|what happens when)",
    r"^(#\d+ (reason|mistake|thing|tip|hack|way))",
    r"^(\d+ (reasons|mistakes|things|tips|hacks|ways))",
]


class DataTransformer:
    """Transform raw post DataFrame into actionable intelligence."""

    # ── Engagement Rate ──────────────────────────────────────────────────
    def add_engagement_rate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add an `engagement_rate` column. Uses views if available, else max likes as denominator."""
        df = df.copy()
        views = df.get("views", df["likes"].clip(lower=1))
        df["engagement_rate"] = ((df["likes"] + df["comments"]) / views.clip(lower=1) * 100).fillna(0).round(2)
        return df

    def top_posts(self, df: pd.DataFrame, n: int = 10) -> list[dict]:
        """Return top N posts ranked by engagement rate."""
        df = self.add_engagement_rate(df)
        top = df.nlargest(n, "engagement_rate")
        return top.to_dict(orient="records")

    # ── Content Categorization ───────────────────────────────────────────
    def _categorize_caption(self, caption: str) -> str:
        if not caption:
            return "uncategorized"
        caption_lower = caption.lower()
        scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in caption_lower:
                    scores[cat] += 1
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "uncategorized"

    def categorize_posts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add a `category` column to the DataFrame."""
        df = df.copy()
        captions = df.get("caption", pd.Series([""] * len(df)))
        df["category"] = captions.apply(self._categorize_caption)
        return df

    # ── Hook Detection ───────────────────────────────────────────────────
    def _has_hook(self, caption: str) -> bool:
        if not caption:
            return False
        first_line = caption.strip().split("\n")[0].lower()
        return any(re.match(pat, first_line, re.IGNORECASE) for pat in HOOK_PATTERNS)

    def _extract_hook(self, caption: str) -> str:
        if not caption:
            return ""
        return caption.strip().split("\n")[0][:120]

    # ── Hashtag Extraction ───────────────────────────────────────────────
    def extract_hashtags(self, df: pd.DataFrame) -> list[dict]:
        """Return sorted list of (hashtag, count) from all captions."""
        all_tags = []
        captions = df.get("caption", pd.Series([]))
        for cap in captions.dropna():
            all_tags.extend(re.findall(r"#\w+", str(cap).lower()))
        counted = Counter(all_tags).most_common(30)
        return [{"hashtag": tag, "count": cnt} for tag, cnt in counted]

    # ── Reach & Audience Intelligence ──────────────────────────────────
    def calculate_reach_intelligence(self, df: pd.DataFrame, followers: int) -> dict:
        """Analyze audience reach vs content performance."""
        if followers <= 0 or df.empty:
            return {"active_follower_rate": 0, "status": "no_data", "insight": "Awaiting follower data for reach analysis."}

        avg_engagement = (df["likes"] + df["comments"]).mean()
        # Active Follower Rate (AFR)
        afr = (avg_engagement / followers) * 100
        
        # Benchmarks
        status = "Elite" if afr >= 5 else "Healthy" if afr >= 1.5 else "Low Resonance"
        insight = "Excellent audience resonance." if status == "Elite" else \
                  "Steady audience engagement." if status == "Healthy" else \
                  "Content is failing to reach existing followers (ghost audience or poor retention)."
            
        return {
            "active_follower_rate": round(afr, 2),
            "status": status,
            "insight": insight,
            "followers": followers
        }

    # ── Performance Intelligence (Agency-Level) ──────────────────────────
    def calculate_content_score(self, df: pd.DataFrame) -> int:
        """Calculate a 0-100 Content Score."""
        if df.empty: return 0
        
        # 1. Engagement Score (50%)
        # Benchmarking against a "Good" ER of 5%
        avg_er = float(df["engagement_rate"].mean())
        er_score = min(100.0, (avg_er / 5.0) * 100) * 0.5
        
        # 2. Consistency Score (25%)
        # Based on post frequency (assuming data is recent)
        if "date" in df.columns:
            days_span = (pd.to_datetime(df["date"].max()) - pd.to_datetime(df["date"].min())).days
            posts_per_day = len(df) / max(days_span, 1)
            # Optimal frequency: 0.5 to 1 post/day
            consistency_score = min(100, (posts_per_day / 0.7) * 100) * 0.25
        else:
            consistency_score = 15 # Placeholder
            
        # 3. Quality Signal Score (25%)
        # Hooks, CTAs, Caption Length
        hook_pct = (df["caption"].apply(self._has_hook).sum() / len(df)) * 100 if "caption" in df.columns else 0
        cta_pct = (df.get("has_cta", pd.Series([0]*len(df))).sum() / len(df)) * 100
        quality_score = (min(100, hook_pct) * 0.1) + (min(100, cta_pct) * 0.15)
        
        return int(er_score + consistency_score + quality_score)

    def compare_formats(self, df: pd.DataFrame) -> dict:
        """Compare performance across content formats."""
        if "type" not in df.columns: return {}
        formats = df.groupby("type")["engagement_rate"].mean().to_dict()
        
        insights = []
        if len(formats) > 1:
            best = max(formats, key=formats.get)
            worst = min(formats, key=formats.get)
            if formats[worst] > 0:
                multiplier = round(formats[best] / formats[worst], 1)
                insights.append(f"{best.capitalize()} posts perform {multiplier}x better than {worst} posts on this account.")
        
        return {
            "avg_er_by_format": {k: round(float(v), 2) for k, v in formats.items()},
            "insights": insights
        }

    def detect_trends(self, df: pd.DataFrame) -> dict:
        """Detect growth or decline trends over the analyzed period."""
        if len(df) < 4: return {"status": "stable", "change_pct": 0}
        
        # Compare first half vs second half (chronologically)
        df_sorted = df.sort_values("date") if "date" in df.columns else df
        mid = len(df_sorted) // 2
        recent_er = df_sorted.tail(mid)["engagement_rate"].mean()
        older_er = df_sorted.head(mid)["engagement_rate"].mean()
        
        if older_er == 0: return {"status": "growing", "change_pct": 100}
        
        diff_pct = round(((recent_er - older_er) / older_er) * 100, 1)
        status = "growing" if diff_pct > 5 else "declining" if diff_pct < -5 else "stable"
        
        return {
            "status": status,
            "change_pct": diff_pct,
            "insight": f"Engagement is {status} by {abs(diff_pct)}% recently."
        }

    # ── Pattern Detection ────────────────────────────────────────────────
    def detect_patterns(self, df: pd.DataFrame, followers: int = 0) -> dict:
        """Detect high-level patterns across all posts."""
        df = self.add_engagement_rate(df)
        df = self.categorize_posts(df)

        captions = df.get("caption", pd.Series([""] * len(df))).fillna("")
        df["caption_length"] = captions.apply(len)
        
        # Advanced Intelligence
        content_score = self.calculate_content_score(df)
        format_analysis = self.compare_formats(df)
        trend_analysis = self.detect_trends(df)
        reach_analysis = self.calculate_reach_intelligence(df, followers)
        
        avg_cap_len = int(df["caption_length"].mean())
        hooks = [self._extract_hook(c) for c in captions if self._has_hook(c)]
        type_counts = df.get("type", pd.Series([])).value_counts().to_dict()
        cat_counts = df["category"].value_counts().to_dict()

        # Best time
        by_hour = df.groupby("hour")["engagement_rate"].mean() if "hour" in df.columns else pd.Series()
        best_hour = int(by_hour.idxmax()) if not by_hour.empty else 18
        by_day = df.groupby("day")["engagement_rate"].mean() if "day" in df.columns else pd.Series()
        best_day = str(by_day.idxmax()) if not by_day.empty else "Friday"

        return {
            "content_score": content_score,
            "performance_trends": trend_analysis,
            "format_analysis": format_analysis,
            "reach_analysis": reach_analysis,
            "avg_engagement_rate": round(float(df["engagement_rate"].mean()), 2),
            "avg_caption_length": avg_cap_len,
            "hook_count": len(hooks),
            "top_hooks": hooks[:5],
            "content_type_breakdown": type_counts,
            "category_breakdown": cat_counts,
            "best_posting_hour": best_hour,
            "best_posting_day": best_day,
            "top_hashtags": self.extract_hashtags(df)[:20],
            "total_posts_analyzed": len(df),
        }

    # ── Summary for AI prompt ────────────────────────────────────────────
    def summary_for_ai(self, df: pd.DataFrame) -> dict:
        patterns = self.detect_patterns(df)
        top = self.top_posts(df, n=5)
        return {
            "patterns": patterns,
            "top_posts": top,
        }
