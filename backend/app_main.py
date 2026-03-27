"""
app.py — Flask API
Endpoints:
  POST /analyze    — Full account audit (existing)
  POST /trend      — Niche trend analysis
  POST /recommend  — AI content recommendations
  POST /competitor — Competitor breakdown
  POST /niche      — Niche intelligence
  POST /explore    — Explore page simulation
"""

import os
import json
from dotenv import load_dotenv
import logging
load_dotenv()

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from app.scraper import InstagramScraper
from app.ai_engine import AIEngine
from app.intelligence import DataTransformer
from app.trend_analyzer import TrendEngine
from app.recommender import AIRecommender
from app.competitor import CompetitorAnalyser
from app.niche_engine import NicheEngine
import pandas as pd

# ── Flask Setup ───────────────────────────────────────────────────────────────
_base_path = os.path.dirname(os.path.abspath(__file__))
_dist_path = os.path.join(_base_path, '..', 'frontend', 'dist')

app = Flask(__name__, static_folder=_dist_path, static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})

# ── Singletons ───────────────────────────────────────────────────────────────
scraper     = InstagramScraper()
ai_engine   = AIEngine()
transformer = DataTransformer()
trend_eng   = TrendEngine(scraper=scraper, ai_engine=ai_engine)
recommender = AIRecommender(ai_engine=ai_engine, scraper=scraper)
competitor  = CompetitorAnalyser(scraper=scraper)
niche_eng   = NicheEngine(scraper=scraper, ai_engine=ai_engine)

# ── Utility ──────────────────────────────────────────────────────────────────
def _get_json():
    data = request.get_json(silent=True) or {}
    if not data and request.data:
        try:
            data = json.loads(request.data.decode("utf-8"))
        except Exception:
            data = {}
    return data

def _mock_df(username="creator"):
    return pd.DataFrame([
        {"post_id": "v1", "type": "video",    "likes": 2400, "comments": 85,  "date": "2026-03-20",
         "hour": 18, "day": "Friday",   "caption": f"How I grew my {username} community 10x in 90 days #growth #india",
         "has_question": True,  "has_cta": True,  "audio_type": "trending"},
        {"post_id": "i1", "type": "image",    "likes": 1200, "comments": 30,  "date": "2026-03-21",
         "hour": 10, "day": "Saturday", "caption": "3 mistakes I made starting out. Don't do this! #tips #learn",
         "has_question": False, "has_cta": True,  "audio_type": "none"},
        {"post_id": "c1", "type": "carousel", "likes": 3500, "comments": 120, "date": "2026-03-22",
         "hour": 20, "day": "Sunday",   "caption": "My honest journey and the lessons learned. #motivation #india",
         "has_question": True,  "has_cta": False, "audio_type": "none"},
        {"post_id": "v2", "type": "video",    "likes": 5100, "comments": 290, "date": "2026-03-19",
         "hour": 19, "day": "Thursday", "caption": "POV: You finally stopped scrolling and saw this 🔥 #viral #trends",
         "has_question": False, "has_cta": True,  "audio_type": "trending"},
        {"post_id": "i2", "type": "image",    "likes": 900,  "comments": 15,  "date": "2026-03-18",
         "hour":  9, "day": "Wednesday","caption": "Grateful for the support. New updates soon! #community",
         "has_question": False, "has_cta": False, "audio_type": "none"},
    ])

# ── Routes ───────────────────────────────────────────────────────────────────

# ── SPA Routing ──────────────────────────────────────────────────────────────

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "Instagram Marketing Intelligence Engine v2.0"})

@app.route("/deep_analysis", methods=["POST"])
def deep_analysis():
    data = _get_json()
    hashtag = data.get("hashtag", "")
    if not hashtag:
        return jsonify({"error": "hashtag is required"}), 400

    logging.info(f"[/deep_analysis] hashtag={hashtag!r}")
    print(f"[/deep_analysis] hashtag={hashtag!r}")
    try:
        result = trend_eng.analyze_deep_hashtags(hashtag)
        logging.info(f"[/deep_analysis] Success for {hashtag}")
        return jsonify(result)
    except Exception as e:
        logging.error(f"[/deep_analysis] Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ── 1. ACCOUNT AUDIT ─────────────────────────────────────────────────────────
@app.route("/analyze", methods=["POST"])
def analyze():
    data     = _get_json()
    username = data.get("username")
    competitor_usernames = data.get("competitors", [])
    if not username:
        return jsonify({"error": "username is required"}), 400

    print(f"[/analyze] {username} (competitors: {competitor_usernames})")

    # 1. Scrape Primary Account
    if res_primary and res_primary.get("posts") is not None and not res_primary["posts"].empty:
        df_primary = res_primary["posts"]
        profile_primary = res_primary["profile"]
        is_live = True
    else:
        print(f"[/analyze] primary scrape failed — using mock data")
        df_primary = _mock_df(username)
        profile_primary = {"followers": 12500, "following": 450}
        is_live = False

    # 2. Scrape Competitors (limit to 3 for performance)
    competitor_insights = []
    for c_user in competitor_usernames[:3]:
        try:
            print(f"[/analyze] Benchmarking competitor: {c_user}")
            res_c = scraper.fetch_posts(c_user, max_posts=15)
            if res_c and res_c.get("posts") is not None and not res_c["posts"].empty:
                df_c = res_c["posts"]
                df_c = transformer.add_engagement_rate(df_c)
                c_patterns = transformer.detect_patterns(df_c, followers=res_c["profile"].get("followers", 0))
                competitor_insights.append({
                    "username": c_user,
                    "followers": res_c["profile"].get("followers", 0),
                    "avg_er": c_patterns.get("avg_engagement_rate", 0),
                    "post_frequency": c_patterns.get("total_posts_analyzed", 0),
                    "best_format": max(c_patterns.get("content_type_breakdown", {"none":0}), key=c_patterns.get("content_type_breakdown", {"none":0}).get)
                })
        except Exception as e:
            print(f"[/analyze] Competitor {c_user} benchmarking failed: {e}")

    # 3. Intelligence Layer
    df_primary = transformer.add_engagement_rate(df_primary)
    df_primary = transformer.categorize_posts(df_primary)
    patterns = transformer.detect_patterns(df_primary, followers=profile_primary.get("followers", 0))
    top_posts = transformer.top_posts(df_primary, n=5)

    metrics = {
        "avg_likes":        round(float(df_primary["likes"].mean()), 1),
        "avg_comments":     round(float(df_primary["comments"].mean()), 1),
        "avg_engagement_rate": round(float(df_primary["engagement_rate"].mean()), 2),
        "followers":        profile_primary.get("followers", 0),
        "following":        profile_primary.get("following", 0),
        "active_follower_rate": patterns.get("reach_analysis", {}).get("active_follower_rate", 0),
        "reach_status":     patterns.get("reach_analysis", {}).get("status", "Healthy"),
        "content_score":    patterns.get("content_score", 0),
        "total_posts":      len(df_primary),
        "best_day":         patterns["best_posting_day"],
        "best_hour":        patterns["best_posting_hour"],
        "top_hashtags":     patterns["top_hashtags"][:10],
        "category_breakdown": patterns["category_breakdown"],
    }

    # 4. Agency-Level AI Audit
    audit_report = ai_engine.analyze_data(
        {"patterns": patterns, "top_posts": top_posts},
        competitor_insights
    )

    return jsonify({
        "username":     str(username),
        "metrics":      metrics,
        "patterns":     patterns,
        "top_posts":    top_posts,
        "posts":        df_primary.to_dict(orient="records"),
        "benchmarks":   competitor_insights,
        "audit_report": audit_report,
        "is_live":      is_live
    })


# ── 2. TREND ANALYSIS ────────────────────────────────────────────────────────
@app.route("/trend", methods=["POST"])
def trend():
    data  = _get_json()
    niche = data.get("niche", "")
    username = data.get("username", "")

    print(f"[/trend] niche={niche!r} username={username!r}")

    # Pull live trends from niche OR the user's own account
    if niche:
        raw_trends = trend_eng.analyze_niche_trends(niche)
        if "error" in raw_trends:
            return jsonify(raw_trends)
    elif username:
        res = scraper.fetch_posts(username, max_posts=20)
        df = res["posts"] if res and res.get("posts") is not None else None
        raw_trends = trend_eng.analyze_posts(df) if df is not None else trend_eng._empty_trends()
    else:
        return jsonify({"error": "niche or username required"}), 400

    # AI summary
    ai_summary = ai_engine.summarize_trends(raw_trends)

    return jsonify({
        "niche":       niche or username,
        "raw_trends":  raw_trends,
        "ai_summary":  ai_summary,
    })


# ── 3. AI RECOMMENDATIONS ────────────────────────────────────────────────────
@app.route("/recommend", methods=["POST"])
def recommend():
    data     = _get_json()
    topic    = data.get("topic", "")
    niche    = data.get("niche", "")
    username = data.get("username", "")

    if not topic:
        return jsonify({"error": "topic is required"}), 400

    print(f"[/recommend] topic={topic!r} niche={niche!r}")
    result = recommender.recommend(topic=topic, niche=niche, username=username)
    return jsonify(result)


# ── 4. COMPETITOR ANALYSIS ───────────────────────────────────────────────────
@app.route("/competitor", methods=["POST"])
def competitor_route():
    data     = _get_json()
    username = data.get("username", "")
    if not username:
        return jsonify({"error": "username is required"}), 400

    print(f"[/competitor] {username}")
    result = competitor.analyse(username, max_posts=20)

    # AI commentary
    if result["total_posts_analyzed"] > 0:
        result["ai_commentary"] = ai_engine.analyse_competitor(result)

    return jsonify(result)


# ── 5. NICHE INTELLIGENCE ────────────────────────────────────────────────────
@app.route("/niche", methods=["POST"])
def niche_route():
    data  = _get_json()
    niche = data.get("niche", "")
    if not niche:
        return jsonify({"error": "niche is required"}), 400

    print(f"[/niche] {niche}")
    result = niche_eng.research(niche)
    return jsonify(result)


# ── 6. EXPLORE SIMULATION ────────────────────────────────────────────────────
@app.route("/explore", methods=["POST"])
def explore():
    data  = _get_json()
    niche = data.get("niche", "general")

    print(f"[/explore] {niche}")

    # Get niche trends for prediction base
    raw = trend_eng._empty_trends()
    try:
        raw = trend_eng.analyze_niche_trends(niche, max_posts=8)
    except Exception:
        pass

    # Determine best format
    formats = raw.get("content_format_breakdown", {})
    top_format = max(formats, key=formats.get) if formats else "reels"

    # Build prediction logic
    er_signal = "High" if raw.get("posts_analyzed", 0) > 20 else "Moderate"
    signals = raw.get("trending_hooks", [])[:3]

    recommendations = [
        f"Prioritize **{top_format}** — it's the dominant format in this niche right now.",
        f"Caption style: **{raw.get('caption_style', 'medium')}** performs best.",
        f"Post on **{raw.get('best_day', 'Tuesday')}** for maximum engagement.",
    ]
    if signals:
        recommendations.append(f"Use hooks that start like: \"{signals[0][:60]}...\"")

    return jsonify({
        "niche": niche,
        "viral_probability": er_signal,
        "dominant_format": top_format,
        "trending_hooks": signals,
        "recommendations": recommendations,
        "top_hashtags": raw.get("top_hashtags", [])[:10],
        "caption_style": raw.get("caption_style", "medium"),
        "best_day": raw.get("best_day", "Tuesday"),
    })



if __name__ == "__main__":
    app.run(debug=True, port=5000)
