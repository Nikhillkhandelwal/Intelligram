/* TrendDashboard.jsx */
import React, { useState } from 'react';
import axios from 'axios';
import { TrendingUp, Hash, Clock, Lightbulb, Loader2 } from 'lucide-react';

const NICHES = ['fitness', 'choreography', 'real estate', 'personal branding', 'food', 'travel', 'fashion', 'business', 'lifestyle', 'comedy'];

const TrendDashboard = () => {
  const [niche, setNiche] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const run = async () => {
    if (!niche) return;
    setLoading(true);
    setData(null);
    try {
      const res = await axios.post('/trend', { niche });
      setData(res.data);
    } catch (e) {
      setData({ error: e.response?.data?.error || 'Failed to fetch trends' });
    } finally {
      setLoading(false);
    }
  };

  const raw = data?.raw_trends || {};
  const ai  = data?.ai_summary  || {};

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-pink-500" /> Niche Trend Analysis
        </h2>
        {data && data.is_live === false && (
          <div className="mb-4 flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-blue-100 italic">
            <Sparkles className="w-3 h-3 animate-pulse" /> Predicted Trend Intelligence Active
          </div>
        )}
        <div className="flex gap-3 flex-wrap">
          {NICHES.map(n => (
            <button
              key={n}
              onClick={() => setNiche(n)}
              className={`px-4 py-2 rounded-full text-sm font-semibold capitalize transition-all
                ${niche === n
                  ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white shadow-md'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
            >
              {n}
            </button>
          ))}
        </div>
        <button
          onClick={run}
          disabled={!niche || loading}
          className="mt-4 px-6 py-2.5 bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-full font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-2"
        >
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing...</> : 'Analyze Trends'}
        </button>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* AI Headline */}
          {ai.headline && (
            <div className="col-span-full bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-2xl p-5">
              <p className="text-xs font-semibold uppercase tracking-widest opacity-80 mb-1">AI Insight</p>
              <p className="text-xl font-bold">{ai.headline}</p>
            </div>
          )}

          {/* Trending Hooks */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-yellow-500" /> Trending Hooks
            </h3>
            <ul className="space-y-2">
              {(raw.trending_hooks || []).slice(0, 5).map((h, i) => (
                <li key={i} className="text-sm text-slate-700 bg-slate-50 rounded-lg p-2.5 border-l-2 border-yellow-400">
                  {h}
                </li>
              ))}
              {(!raw.trending_hooks || raw.trending_hooks.length === 0) && (
                <li className="text-sm text-slate-400">No data available yet</li>
              )}
            </ul>
          </div>

          {/* Top Hashtags */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Hash className="w-4 h-4 text-blue-500" /> Top Hashtags
            </h3>
            <div className="flex flex-wrap gap-2">
              {(raw.top_hashtags || []).slice(0, 16).map(({ hashtag, count }) => (
                <span key={hashtag} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">
                  {hashtag} <span className="opacity-60">×{count}</span>
                </span>
              ))}
            </div>
          </div>

          {/* Caption Signals */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">Caption Intelligence</h3>
            <div className="space-y-2 text-sm">
              <p className="text-slate-600">Style: <span className="font-semibold text-slate-800">{raw.caption_style || '—'}</span></p>
              <p className="text-slate-600">Avg length: <span className="font-semibold text-slate-800">{raw.avg_caption_length || 0} chars</span></p>
              <div className="grid grid-cols-3 gap-2 mt-3">
                {[
                  { label: 'Questions', val: raw.caption_signals?.questions_pct },
                  { label: 'CTA',       val: raw.caption_signals?.cta_pct },
                  { label: 'Emoji',     val: raw.caption_signals?.emoji_pct },
                ].map(({ label, val }) => (
                  <div key={label} className="text-center bg-slate-50 rounded-lg p-2">
                    <p className="text-lg font-black text-purple-600">{val ?? 0}%</p>
                    <p className="text-xs text-slate-500">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Best Day + Format */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Clock className="w-4 h-4 text-green-500" /> Performance Patterns
            </h3>
            <p className="text-sm text-slate-600 mb-2">Best day: <strong>{raw.best_day || '—'}</strong></p>
            <div className="space-y-1">
              {Object.entries(raw.content_format_breakdown || {}).map(([type, count]) => (
                <div key={type} className="flex items-center gap-2 text-sm">
                  <div className="w-20 text-right text-slate-500 capitalize">{type}</div>
                  <div className="flex-1 bg-slate-100 rounded-full h-2">
                    <div className="bg-gradient-to-r from-purple-500 to-pink-400 h-2 rounded-full"
                      style={{ width: `${Math.min((count / Math.max(...Object.values(raw.content_format_breakdown))) * 100, 100)}%` }} />
                  </div>
                  <span className="text-slate-600 w-4">{count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* AI action items */}
          {ai.action_items?.length > 0 && (
            <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
              <h3 className="font-bold text-slate-800 mb-3">🎯 Action Items</h3>
              <ul className="space-y-2">
                {ai.action_items.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                    <span className="text-purple-500 font-bold shrink-0">{i + 1}.</span> {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TrendDashboard;
