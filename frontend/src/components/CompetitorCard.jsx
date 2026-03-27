/* CompetitorCard.jsx */
import React, { useState } from 'react';
import axios from 'axios';
import { Search, Loader2, TrendingUp, Star } from 'lucide-react';

const EngagementBadge = ({ value }) => {
  const color = value >= 5 ? 'text-green-600 bg-green-50' : value >= 2 ? 'text-yellow-600 bg-yellow-50' : 'text-red-600 bg-red-50';
  const label = value >= 5 ? 'Strong' : value >= 2 ? 'Moderate' : 'Low';
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-bold ${color}`}>
      {value}% — {label}
    </span>
  );
};

const CompetitorCard = () => {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const run = async () => {
    if (!username) return;
    setLoading(true); setData(null);
    try {
      const res = await axios.post('/competitor', { username });
      setData(res.data);
    } catch (e) {
      setData({ error: e.response?.data?.error || 'Analysis failed' });
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Search className="w-5 h-5 text-purple-500" /> Competitor Analysis
        </h2>
        <div className="flex gap-3">
          <div className="relative flex-1">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">@</span>
            <input type="text" placeholder="competitor_username"
              value={username} onChange={e => setUsername(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && run()}
              className="w-full border border-slate-200 rounded-xl pl-7 pr-4 py-3 text-sm outline-none focus:ring-2 focus:ring-purple-400" />
          </div>
          <button onClick={run} disabled={!username || loading}
            className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-xl font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-2">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Stats row */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
            <p className="text-xs text-slate-500 uppercase font-semibold mb-1">Avg Engagement</p>
            <EngagementBadge value={data.engagement?.avg || 0} />
          </div>
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
            <p className="text-xs text-slate-500 uppercase font-semibold mb-1">Peak Engagement</p>
            <p className="text-2xl font-black text-orange-500">{data.engagement?.peak || 0}%</p>
          </div>
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
            <p className="text-xs text-slate-500 uppercase font-semibold mb-1">Posts Analyzed</p>
            <p className="text-2xl font-black text-purple-600">{data.total_posts_analyzed}</p>
          </div>

          {/* Strategy Summary */}
          <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">📋 Content Strategy</h3>
            <ul className="space-y-2">
              {(data.strategy_summary || []).map((s, i) => (
                <li key={i} className="text-sm text-slate-700 flex gap-2 items-start">
                  <span className="text-purple-500 shrink-0 mt-0.5">•</span>
                  <span dangerouslySetInnerHTML={{ __html: s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                </li>
              ))}
            </ul>
          </div>

          {data.ai_commentary && (
            <div className="col-span-full bg-gradient-to-br from-slate-900 to-purple-900 text-white rounded-2xl p-5">
              <p className="text-xs font-semibold uppercase tracking-widest text-purple-300 mb-2">🤖 AI Commentary</p>
              <p className="text-sm leading-relaxed">{data.ai_commentary}</p>
            </div>
          )}

          {/* Top Posts */}
          <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Star className="w-4 h-4 text-yellow-500" /> Top Performing Posts
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs text-slate-500 border-b border-slate-100">
                    <th className="pb-2 pr-4">Post ID</th>
                    <th className="pb-2 pr-4">Type</th>
                    <th className="pb-2 pr-4">Likes</th>
                    <th className="pb-2 pr-4">Comments</th>
                    <th className="pb-2">Eng. Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {(data.top_posts || []).map(p => (
                    <tr key={p.post_id} className="border-b border-slate-50 hover:bg-slate-50">
                      <td className="py-2 pr-4 font-mono text-xs text-slate-500">{p.post_id?.slice(0, 10)}</td>
                      <td className="py-2 pr-4 capitalize">{p.type}</td>
                      <td className="py-2 pr-4 font-semibold">{p.likes?.toLocaleString()}</td>
                      <td className="py-2 pr-4 text-slate-600">{p.comments?.toLocaleString()}</td>
                      <td className="py-2">
                        <span className="px-2 py-0.5 bg-purple-50 text-purple-700 rounded-full text-xs font-bold">
                          {p.engagement_rate}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Caption + Hashtags */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">Caption Style</h3>
            <p className="text-sm"><strong>{data.caption_analysis?.style}</strong></p>
            <p className="text-sm text-slate-600 mt-1">Avg length: {data.caption_analysis?.avg_length} chars</p>
            <p className="text-sm text-slate-600">Hook usage: <strong>{data.caption_analysis?.hook_usage_pct}%</strong> of posts</p>
            
            {data.caption_analysis?.top_hooks?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-100">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Used Hooks</p>
                <div className="flex flex-col gap-1.5">
                  {data.caption_analysis.top_hooks.map((hook, i) => (
                    <div key={i} className="text-sm text-slate-700 bg-slate-50 p-2 rounded-lg border border-slate-100">
                      "{hook}"
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="md:col-span-2 bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">Top Hashtags Used</h3>
            <div className="flex flex-wrap gap-2">
              {(data.top_hashtags || []).map(({ hashtag, count }) => (
                <span key={hashtag} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">
                  {hashtag} <span className="opacity-60">×{count}</span>
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompetitorCard;
