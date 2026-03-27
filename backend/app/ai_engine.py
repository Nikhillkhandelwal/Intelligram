"""
ai_engine.py — Multi-purpose AI Engine
Handles all GPT-4o-mini interactions for:
  - Account audit (original)
  - Content recommendations
  - Trend summarization
  - Competitor strategy
  - Niche research
"""

import os
import json
import openai
from dotenv import load_dotenv
import pandas as pd
import re

load_dotenv()

# ── System Prompts ───────────────────────────────────────────────────────────

AUDIT_PROMPT = """
You are the world's leading Instagram Growth Strategist, specifically elite in the Indian Creator Economy (Hinglish context, tier-1/2/3 audience behavior).
Provide a deep-dive "Instagram Marketing Intelligence Audit" for the provided account data.

IMPORTANT: Start your response EXACTLY with these two lines:
GLOBAL SCORE: [Number]/100
GROWTH GRADE: [Letter A-F]

Then structure your audit into these 4 PREMIUM MODULES using the EXACT headers below:

### MODULE 1: BRAND IDENTITY & BIO CONVERSION
- Critique the current Bio, Profile Image, and Name.
- Provide 3 "Power Bio" options with clear CTAs and Hinglish touchpoints if applicable.
- Suggest "Link-in-Bio" optimization.

### MODULE 2: CONTENT PILLARS & VIRAL HOOK ANALYSIS
- Identify the 3 most successful content formats from the data (e.g., POV Reels, Educational Carousels).
- Analyze the "Hook" effectiveness. Give 5 specific "Viral Hook" ideas based on their niche.
- Critique the Caption Style and Hashtag strategy.

### MODULE 3: PERFORMANCE METRICS & ALGORITHM ALIGNMENT
- Interpret the Engagement Rate (ER). Categorize it as (Low, Good, Elite).
- Identify "Peak Engagement Windows" (Best time/day to post).
- Content Format Recommendation: Should they do more Reels, Images, or Carousels?

### MODULE 4: THE 30-DAY "INDIA-FIRST" GROWTH ROADMAP
- A structured 4-week plan.
- 5 Concrete Action Items to implement IMMEDIATELY.
- Final Verdict: The #1 thing that will 10x their growth.

Use vibrant Markdown, bold text, and clear bullet points.
"""

AGENCY_AUDIT_PROMPT = """
You are the world's most elite Instagram Growth Agency Partner. You are performing a high-stakes "Marketing Intelligence Audit" for a premium client.
Your goal is to provide deep, actionable intelligence, not just data.

### DATA CONTEXT PROVIDED:
- Account Metrics: {patterns}
- Top Posts: {top_posts}
- Competitor Benchmarks: {benchmarks}

### YOUR ANALYSIS MUST COVER THESE 10 MODULES. 
CRITICAL: Start EACH module with exactly "[MODULE_START: Name of Module]" on a new line.

[MODULE_START: PERFORMANCE INTELLIGENCE]
- Interpret the Content Score ({content_score}/100).
- Analyze the {trend_status} trend ({trend_pct}% change).
- Content Format Insight: Explain WHY {format_insight}.

[MODULE_START: HOOK & CONTENT ANALYSIS (CRITICAL)]
- Categorize hooks into: [Curiosity, Storytelling, Emotional, Relatable, Trend-based].
- Identify the #1 best-performing hook pattern from the top posts.
- Evaluate the "Hook Effectiveness Score" (0-100).

[MODULE_START: TREND INTELLIGENCE ENGINE]
- Based on the {niche} niche, analyze if the client is "Trend-Aligned".
- Generate a "Trend Alignment Score" (0-100).

[MODULE_START: AUDIENCE INTELLIGENCE & REACH]
- Reach Assessment: The Active Follower Rate is **{af_rate}%** ({reach_status}).
- Insight: {reach_insight}
- Perform "Virtual Sentiment Analysis": based on engagement ratios and categories, infer if the audience is [Learning, Buying, or Entertained].
- Predict which Content Pillar will drive the most "Save" and "Share" actions.

[MODULE_START: COMPETITOR BENCHMARKING]
- Compare the client to {competitor_list}. 
- Highlight the "Competitive Gap" (e.g., "Competitor X posts 3x more Reels").

[MODULE_START: CONVERSION & CTA ANALYSIS]
- Evaluate CTA effectiveness. Are they using "Hard CTAs" (Buy/Link) or "Soft CTAs" (Share/Tag)?
- Suggest a high-conversion CTA for their next post.

[MODULE_START: POSTING OPTIMIZATION]
- Confirm best time ({best_time}) and day ({best_day}).
- Recommend a "Frequency Shift" (e.g., "Move from 3 posts to 5 posts/week").

[MODULE_START: VIRALITY PREDICTION]
- Select the most recent post and assign a "Viral Potential Score" [High/Medium/Low] with a 1-sentence reason.

[MODULE_START: ACTIONABLE STRATEGY ENGINE]
First, provide a 3-sentence high-level strategic summary of the recommended execution path.
Then, provide a valid JSON block inside triple backticks for the interactive dashboard.
CRITICAL: Each item in `weekly_plan` MUST be descriptive (e.g., "Day 1: [Post Type] - [Topic] - [Brief Execution Tip]").
The `caption_strategy` should use descriptive keys like "Hook Pattern: [Type]", "Structure Type: [Style]", "Emoji Goal: [Count] per caption".
The `posting_schedule` MUST include a `frequency_insight` explaining WHY this frequency works.

```json
{{
  "weekly_plan": ["Day 1: ...", "Day 2: ...", "Day 3: ...", "Day 4: ...", "Day 5: ...", "Day 6: ...", "Day 7: ..."],
  "content_ideas": ["Concept 1: [Strategic Tip]", "Concept 2: [Strategic Tip]", "Concept 3: [Strategic Tip]"],
  "caption_strategy": ["Hook Pattern: [Value]", "Structure Type: [Value]", "Emoji Goal: [Value]"],
  "hashtags": ["tag1", "tag2", "tag3"],
  "posting_schedule": {{
    "best_time": "7-9 PM", 
    "best_days": ["Sunday", "Wednesday"],
    "frequency_insight": "Detailed explanation of why this frequency is optimal for the current account health."
  }}
}}
```

[MODULE_START: FINAL VERDICT]
- The one "North Star" metric or action that will 10x this account in 90 days.

STRICT INSTRUCTIONS: 
- Use markdown bold (e.g., **text**) SELECTIVELY for critical data points and insights to improve readability.
- Use a professional agency tone: clinical, sharp, and data-driven.
- Ensure the JSON block in Module 9 is the ONLY place structured technical data appears.
- Each module should be 4-5 sentences of deep, unique insight.
"""

RECOMMEND_PROMPT = """
You are an Instagram content strategist. Given a topic: "{topic}" and niche: "{niche}", 
generate a comprehensive content recommendation package.
Your response MUST be an EXACT JSON object with these keys: 
{{
  "captions": ["List of 20 platform-optimized, high-converting captions..."],
  "scripts": [
    {{
      "title": "A short catchy title for this reel",
      "hook": "The first 3 seconds: strong, curiosity-driven or problem-solving hook",
      "body": "The core message: concise, fast-paced educational or entertaining content",
      "cta": "Strong Call-to-Action based on the goal (e.g., Follow, Comment a keyword, DM for info)"
    }}
  ],
  "hashtags": ["30 relevant, high-performance hashtags..."],
  "hooks": ["3-5 separate, standalone hook ideas to test..."],
  "best_time": {{"day": "DayName", "hour": 18}},
  "improvement_tips": ["5 actionable tips to improve reach/engagement..."],
  "viral_songs": [
    {{"title": "Song Name", "artist": "Artist", "trend": "🔥 Indian/Global trending audio"}}
  ]
}}

Requirements:
1. Generate EXACTLY 20 captions.
2. Generate EXACTLY 5 to 7 scripts, each reflecting a unique strategic angle.
3. Ensure viral_songs reflect current Indian and global trends relevant to the niche.
4. Return ONLY valid JSON. No markdown, no pre-amble, no explanation.
"""

TREND_PROMPT = """
You are an Instagram trend analyst. Given raw trend data from a niche,
summarize the key trends in a JSON object:
{
  "headline": "One-line summary of what's working right now",
  "trend_signals": ["signal1", "signal2", ...],
  "viral_formats": ["format1", "format2"],
  "caption_insight": "Insight about caption style that's winning",
  "hook_insight": "Insight about hooks that grab attention",
  "hashtag_strategy": "Recommended hashtag approach",
  "action_items": ["action1", "action2", "action3"],
  "viral_songs": [{"title": "Song Title", "artist": "Artist Name", "trend": "Trending 🔥"}, {"title": "Trending Track", "artist": "Viral Artist", "trend": "High Growth"}]
}
Return ONLY valid JSON.
"""

NICHE_PROMPT = """
You are a niche marketing expert. Given hashtags and top captions from a niche,
generate actionable intelligence as JSON:
{
  "summary": "2-3 sentence overview of what's working in this niche",
  "content_ideas": ["idea1", "idea2", "idea3", "idea4", "idea5"],
  "caption_frameworks": ["framework1", "framework2", "framework3"],
  "hashtag_strategy": "Brief hashtag strategy for this niche",
  "growth_tips": ["tip1", "tip2", "tip3"]
}
Return ONLY valid JSON.
"""

DEEP_STRATEGY_PROMPT = """
You are the world's most elite Instagram Growth Strategist. You are analyzing top-performing posts across 3 related hashtags: {hashtags}.
Your goal is to provide a "Descriptive Strategy Blueprint" in JSON format that another creator in this genre can use to IMMEDIATELY start creating high-performing content.

Return ONLY a JSON object with this structure:
{{
  "visuals": {{
    "palette": ["color1", "color2"],
    "lighting": "description of lighting",
    "framing": "description of framing",
    "style": "Minimalist/Vibrant/etc",
    "patterns": ["pattern1", "pattern2"]
  }},
  "hooks": {{
    "analysis": "psychology of the hooks",
    "templates": [
      {{"hook": "exact template 1", "logic": "why it works"}},
      {{"hook": "exact template 2", "logic": "why it works"}},
      {{"hook": "exact template 3", "logic": "why it works"}},
      {{"hook": "exact template 4", "logic": "why it works"}},
      {{"hook": "exact template 5", "logic": "why it works"}}
    ]
  }},
  "captions": {{
    "ideal_length": "e.g. 150-200 chars",
    "formatting": "description",
    "triggers": ["trigger1", "trigger2"],
    "winning_template": "a complete template with placeholders"
  }},
  "seo": {{
    "hashtag_mix": "ratio description",
    "hidden_gems": ["tag1", "tag2"],
    "keywords": ["keyword1", "keyword2", "keyword3"]
  }},
  "execution_plan": [
    {{"day": 1, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 2, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 3, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 4, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 5, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 6, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}},
    {{"day": 7, "type": "Content Type", "topic": "Topic Idea", "success_factor": "Key Factor"}}
  ],
  "detailed_10_post_plan": [
    {{
      "post_num": 1,
      "type": "Reel/Carousel/Static",
      "hook": "Specific viral hook text",
      "content": "Detailed content strategy & value prop",
      "visuals": "Specific visual/B-roll idea (India context)",
      "caption": "Caption focus & CTA",
      "insight_applied": "Which specific competitor pattern this uses"
    }}
  ],
  "niche_insights": {{
    "trending_songs": [{{"title": "Song", "artist": "Artist", "reason": "Why it's viral"}}],
    "hashtag_strategy": "Detailed cluster strategy",
    "audience_vibe": "What the Indian audience is feeling/craving in this niche"
  }}
}}

STRICT INSTRUCTIONS:
- Generate EXACTLY 10 posts in the detailed_10_post_plan.
- Be extremely SPECIFIC and DESCRIPTIVE in the strings.
- Return ONLY valid JSON. No other text.
"""


class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        # Configure OpenAI SDK to wrap Groq's high-speed endpoint
        openai.api_key = self.api_key
        openai.base_url = "https://api.groq.com/openai/v1/"

    def _call(self, system: str, user: str, json_mode: bool = False) -> str | dict:
        """Core API call using Groq via OpenAI SDK wrapper."""
        kwargs = dict(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
        )
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        response = openai.chat.completions.create(**kwargs)
        text = response.choices[0].message.content
        print(f"DEBUG: AI Response Text: {text[:500]}...") # Log first 500 chars
        if json_mode:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # If Llama returns extra text around JSON, strip it safely
                import re
                match = re.search(r'\{.*\}', text.replace('\n', ' '), re.DOTALL)
                if match:
                    return json.loads(match.group(0))
                return {}
        return text

    # ── Audit (existing) ─────────────────────────────────────────────────
    def analyze_data(self, data_input: str | dict, competitors_data=None) -> str:
        """Process data and generate a deep-dive audit using either legacy or agency prompts."""
        try:
            # Check if this is the new structured intelligence dict
            if isinstance(data_input, dict) and "patterns" in data_input:
                patterns = data_input["patterns"]
                top_posts = data_input.get("top_posts", [])
                
                # Reach Health Data
                reach_info = patterns.get("reach_analysis", {})
                
                # Format variables for AGENCY_AUDIT_PROMPT
                prompt_vars = {
                    "patterns": json.dumps(patterns, indent=2),
                    "top_posts": json.dumps(top_posts, indent=2),
                    "benchmarks": json.dumps(competitors_data or [], indent=2),
                    "content_score": patterns.get("content_score", "N/A"),
                    "trend_status": patterns.get("performance_trends", {}).get("status", "stable"),
                    "trend_pct": patterns.get("performance_trends", {}).get("change_pct", 0),
                    "format_insight": (patterns.get("format_analysis", {}).get("insights") or ["No format insights available."])[0],
                    "niche": "General Instagram",
                    "competitor_list": ", ".join([c["username"] for c in (competitors_data or [])]) or "Industry Averages",
                    "best_time": f"{patterns.get('best_posting_hour', 18)}:00",
                    "best_day": patterns.get("best_posting_day", "Sunday"),
                    # New Reach Metrics
                    "af_rate": reach_info.get("active_follower_rate", 0),
                    "reach_status": reach_info.get("status", "Unknown"),
                    "reach_insight": reach_info.get("insight", "Data pending.")
                }
                
                user_msg = "Please generate the Agency-Level 10-Module Audit based on the provided intelligence."
                return self._call(AGENCY_AUDIT_PROMPT.format(**prompt_vars), user_msg)

            # Legacy fallback for raw JSON string
            import io
            df = pd.read_json(io.StringIO(str(data_input)))
            
            summary = f"""
            Account: {(df['username'].iloc[0] if not df.empty and 'username' in df.columns else 'Unknown')}
            Total Posts analyzed: {len(df)}
            Avg Likes: {df['likes'].mean():.1f} if 'likes' in df.columns else 0
            Avg Comments: {df['comments'].mean():.1f} if 'comments' in df.columns else 0
            Top 5 Post Types: {df['type'].value_counts().head(5).to_dict() if 'type' in df.columns else {}}
            Best Posting Times (Raw): {df.groupby('hour')['likes'].mean().idxmax() if 'hour' in df.columns and 'likes' in df.columns else '18'}:00
            """

            user_msg = f"ACCOUNT DATA SUMMARY:\n{summary}\n\nCOMPETITOR DATA:\n{competitors_data}\n\nGenerate the Audit Report now."
            return self._call(AUDIT_PROMPT, user_msg)
            
        except Exception as e:
            print(f"AIEngine audit error: {e}")
            import traceback
            traceback.print_exc()
            return self._audit_fallback()

    # ── Recommendations ───────────────────────────────────────────────────
    def recommend(self, topic: str, niche: str = "", patterns: dict = None) -> dict:
        try:
            prompt = (
                f"Topic: {topic}\nNiche: {niche or 'general'}\n"
                f"Account patterns: {json.dumps(patterns or {}, indent=2)}\n\n"
                "Generate optimized content recommendations."
            )
            # Ensure RECOMMEND_PROMPT is formatted with topic and niche
            formatted_system = RECOMMEND_PROMPT.format(topic=topic, niche=niche)
            return self._call(formatted_system, prompt, json_mode=True)
        except Exception as e:
            print(f"AIEngine recommend error: {e}")
            return {
                "captions": ["Are you making this mistake? 👇", "Here is my secret formula. 🤫", "Save this for later! 📌"],
                "hashtags": ["#explore", "#trending", "#viral", "#growthtips", "#india", "#tipsandtricks"],
                "hooks": ["Watch this before you post", "3 hidden secrets to", "The biggest lie you've been told"],
                "best_time": {"day": "Wednesday", "hour": 18},
                "improvement_tips": ["Post 4 reels a week consistently", "Use trending audio tracks", "Ask questions in the first 3 seconds", "Keep videos under 15s", "Add clean text-on-screen"]
            }

    # ── Trend Summary ─────────────────────────────────────────────────────
    def summarize_trends(self, raw_data: dict) -> dict:
        try:
            prompt = f"Raw trend data:\n{json.dumps(raw_data, indent=2)}"
            return self._call(TREND_PROMPT, prompt, json_mode=True)
        except Exception as e:
            print(f"AIEngine trend error: {e}")
            return {
                "headline": "Analyzing live niche data...",
                "trend_signals": [],
                "viral_formats": [],
                "caption_insight": "Scraping fresh captions...",
                "hook_insight": "Extracting viral hooks...",
                "hashtag_strategy": "Calculating hashtag clusters...",
                "action_items": [],
                "viral_songs": []
            }

    # ── Niche Research ────────────────────────────────────────────────────
    def research_niche(self, data: dict) -> str:
        try:
            prompt = f"Niche data:\n{json.dumps(data, indent=2)}"
            result = self._call(NICHE_PROMPT, prompt, json_mode=True)
            return json.dumps(result)
        except Exception as e:
            print(f"AIEngine niche error: {e}")
            return json.dumps({
                "summary": "This niche thrives on high-energy authenticity and quick value delivery.",
                "content_ideas": ["A Day in the life behind the scenes", "Top 3 common myths busted", "Step-by-step visual guide"],
                "caption_frameworks": ["Hook + Personal Story + CTA", "Problem + Agitation + Solution"],
                "hashtag_strategy": "Mix 2 broad hashtags with 8 hyper-local or micro-niche ones.",
                "growth_tips": ["Engage 15 mins before posting", "Collaborate with similar sized creators"]
            })

    # ── Competitor Summary ────────────────────────────────────────────────
    def analyse_competitor(self, data: dict) -> str:
        try:
            prompt = (
                f"Competitor data:\n{json.dumps(data, indent=2)}\n\n"
                "Provide a 3-4 sentence strategic summary of what this account is doing well "
                "and where their weaknesses are. Be specific and data-driven."
            )
            return self._call(
                "You are a top Instagram marketing analyst. Provide brief, sharp competitor insights.",
                prompt
            )
        except Exception as e:
            print(f"AIEngine competitor error: {e}")
            return "This account has strong overall engagement driven by consistent posting and clear visual branding. However, their comment interaction rate could be significantly improved by asking more direct, polarizing questions in their captions."

    # ── Deep Strategy Analysis ────────────────────────────────────────────
    def get_deep_strategy(self, hashtags: list, posts_data: list) -> dict:
        """Generate a descriptive strategy blueprint based on 30 posts from 3 hashtags."""
        try:
            summary_data = []
            for p in posts_data:
                summary_data.append({
                    "caption": p.get("caption", "")[:150],
                    "type": p.get("type"),
                    "likes": p.get("likes", 0),
                    "comments": p.get("comments", 0),
                    "hashtags": re.findall(r"#\w+", str(p.get("caption", "")))
                })

            # Format system prompt with hashtags
            system_msg = DEEP_STRATEGY_PROMPT.format(hashtags=", ".join(hashtags))
            
            data_summary = json.dumps(summary_data, indent=2) if summary_data else "No live post data available. Please provide a PREDICTED high-performance strategy based on general niche benchmarks."
            user_msg = f"Target Hashtags: {hashtags}\n\nTop Post Data:\n{data_summary}\n\nGenerate the structured JSON strategy."
            
            res = self._call(system_msg, user_msg)
            
            # Extract JSON from response if there's any Markdown wrapping
            json_match = re.search(r"\{.*\}", res, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(res)
        except Exception as e:
            print(f"AIEngine deep strategy error: {e}")
            return {
                "visuals": {"palette": ["Warm Neutrals", "Gold"], "lighting": "Soft warm lighting", "framing": "Mix of close-ups and wide shots", "style": "Elegant", "patterns": ["Aesthetic B-roll"]},
                "hooks": {"analysis": "Emotional hooks perform best.", "templates": [{"hook": "You won't believe...", "logic": "Curiosity"}]},
                "captions": {"ideal_length": "150-300 chars", "formatting": "Bullet points", "triggers": ["Questions"], "winning_template": "Hook + Value + CTA"},
                "seo": {"hashtag_mix": "5 niche, 5 broad", "hidden_gems": ["#trending"], "keywords": ["instagram"]},
                "execution_plan": [{"day": 1, "type": "Reel", "topic": "Introduction", "success_factor": "Hook"}]
            }

    # ── Fallback ──────────────────────────────────────────────────────────
    def _audit_fallback(self) -> str:
        return """
### MODULE 1: PROFILE & BIO OPTIMIZATION
**Brand Identity:** Profile lacks a clear value proposition.
- **Bio:** Change to action-oriented: "Helping you [Achieve X] without [Pain Y]".
- **Link-in-bio:** Add a direct CTA pointing to your main product or newsletter.

### MODULE 2: CONTENT STRATEGY & HOOK AUDIT
**Top Performers:** Reels significantly outperform static images, especially under 15 seconds.
- **Hooks:** Put the most surprising fact in the first 3 seconds.
- **Captions:** Break long paragraphs into 1-2 sentence lines for readability.

### MODULE 3: ENGAGEMENT & COMMUNITY INSIGHTS
- High like-to-comment ratio: people enjoy content but don't feel compelled to converse.
- **Action:** Ask polarizing or open-ended questions in pinned comments.
- **Frequency:** Commit to 4x per week — algorithm rewards consistency.

### MODULE 4: THE 30-DAY GROWTH ROADMAP
**Status: Growth Ready ✅**
1. **Week 1:** Overhaul bio, pin top 3 best-performing Reels.
2. **Week 2:** Test 3 new hook formats (Negative, "How I...", Contrarian).
3. **Week 3:** Engage 15 min/day with competitors' active commenters.
4. **Week 4:** Launch 3-part mini-series to drive profile visits.

**Content Pillars:** Behind The Scenes | Step-by-Step Tutorials | Myth-Busting
"""


if __name__ == "__main__":
    engine = AIEngine()
    print(engine.analyze_data('{"username": "test_user", "posts": []}', "[]"))
