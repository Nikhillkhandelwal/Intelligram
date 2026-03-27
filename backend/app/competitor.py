"""
competitor.py — CompetitorAnalyser
Given a username, scrapes their posts and returns:
  - Top 5 performing posts (by engagement rate)
  - Average and median engagement rate
  - Content type breakdown
  - Caption analysis (length, hooks, CTAs)
  - Hashtag strategy
  - Posting schedule patterns
"""

import pandas as pd
from app.intelligence import DataTransformer


class CompetitorAnalyser:
    """Analyse a competitor's Instagram presence."""

    def __init__(self, scraper=None):
        self.scraper = scraper
        self.transformer = DataTransformer()

    def analyse(self, username: str, max_posts: int = 30) -> dict:
        """Scrape and analyse the given account."""
        res = None
        if self.scraper:
            try:
                res = self.scraper.fetch_posts(username, max_posts=max_posts)
            except Exception as e:
                print(f"CompetitorAnalyser: scrape error for {username}: {e}")

        if not res or res.get("posts") is None or res["posts"].empty:
            return self._empty_result(username)

        df = res["posts"]
        profile = res.get("profile", {})
        
        df = self.transformer.add_engagement_rate(df)
        df = self.transformer.categorize_posts(df)

        # Top posts
        top_posts = self.transformer.top_posts(df, n=5)

        # Engagement stats
        avg_er = round(float(df["engagement_rate"].mean()), 2)
        med_er = round(float(df["engagement_rate"].median()), 2)
        top_er = round(float(df["engagement_rate"].max()), 2)

        # Content breakdown
        type_breakdown = df.get("type", pd.Series([])).value_counts().to_dict()
        cat_breakdown  = df["category"].value_counts().to_dict()

        # Caption patterns
        captions = df.get("caption", pd.Series([""] * len(df))).fillna("")
        avg_cap_len = int(captions.apply(len).mean())
        caption_style = (
            "Short & punchy" if avg_cap_len < 100
            else "Medium storytelling" if avg_cap_len < 300
            else "Long-form"
        )

        # Hook usage
        hook_count = sum(1 for c in captions if self.transformer._has_hook(c))
        hook_pct   = int(hook_count / max(len(captions), 1) * 100)
        top_hooks  = list(set([self.transformer._extract_hook(c) for c in captions if self.transformer._has_hook(c)]))[:5]

        # Hashtags
        top_hashtags = self.transformer.extract_hashtags(df)

        # Posting schedule
        by_day  = df.groupby("day")["engagement_rate"].mean() if "day" in df.columns else pd.Series()
        by_hour = df.groupby("hour")["engagement_rate"].mean() if "hour" in df.columns else pd.Series()
        best_day  = str(by_day.idxmax())  if not by_day.empty  else "Unknown"
        best_hour = int(by_hour.idxmax()) if not by_hour.empty else 12

        # Strategy summary (text)
        strategy = self._build_strategy_summary(
            type_breakdown, cat_breakdown, avg_er, caption_style, hook_pct, best_day, best_hour
        )

        return {
            "username": username,
            "total_posts_analyzed": len(df),
            "engagement": {
                "avg": avg_er,
                "median": med_er,
                "peak": top_er,
            },
            "top_posts": top_posts,
            "content_breakdown": {
                "by_type": type_breakdown,
                "by_category": cat_breakdown,
            },
            "caption_analysis": {
                "avg_length": avg_cap_len,
                "style": caption_style,
                "hook_usage_pct": hook_pct,
                "top_hooks": top_hooks,
            },
            "top_hashtags": top_hashtags[:15],
            "best_posting_time": {
                "day": best_day,
                "hour": best_hour,
            },
            "strategy_summary": strategy,
        }

    def _build_strategy_summary(self, type_bd, cat_bd, avg_er, cap_style, hook_pct,
                                  best_day, best_hour) -> list[str]:
        notes = []
        # Dominant content type
        if type_bd:
            dominant = max(type_bd, key=type_bd.get)
            notes.append(f"Primarily posts **{dominant}** content ({type_bd[dominant]} posts).")
        # Engagement health
        if avg_er >= 5:
            notes.append(f"Strong engagement rate of **{avg_er}%** — content resonates well.")
        elif avg_er >= 2:
            notes.append(f"Moderate engagement rate of **{avg_er}%** — room to improve.")
        else:
            notes.append(f"Low engagement rate of **{avg_er}%** — audience may not be engaged.")
        # Hooks
        if hook_pct >= 60:
            notes.append(f"Uses strong hooks in **{hook_pct}%** of posts — very hook-driven strategy.")
        elif hook_pct >= 30:
            notes.append(f"Moderate hook usage (**{hook_pct}%** of posts).")
        else:
            notes.append(f"Low hook usage (**{hook_pct}%**) — captions are descriptive rather than hook-driven.")
        # Caption style
        notes.append(f"Caption style is **{cap_style}**.")
        # Best time
        ampm = "AM" if best_hour < 12 else "PM"
        h12 = best_hour % 12 or 12
        notes.append(f"Posts perform best on **{best_day}s at {h12}{ampm}**.")
        return notes

    def _empty_result(self, username: str) -> dict:
        return {
            "username": username,
            "total_posts_analyzed": 0,
            "engagement": {"avg": 0, "median": 0, "peak": 0},
            "top_posts": [],
            "content_breakdown": {"by_type": {}, "by_category": {}},
            "caption_analysis": {"avg_length": 0, "style": "unknown", "hook_usage_pct": 0},
            "top_hashtags": [],
            "best_posting_time": {"day": "unknown", "hour": 0},
            "strategy_summary": ["Could not fetch data for this account."],
        }
