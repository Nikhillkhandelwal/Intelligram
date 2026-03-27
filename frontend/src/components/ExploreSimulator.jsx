/* ExploreSimulator.jsx */
import React, { useState } from 'react';
import axios from 'axios';
import { Zap, Loader2 } from 'lucide-react';

const NICHES = ['fitness', 'choreography', 'real estate', 'personal branding', 'food', 'travel', 'fashion', 'business', 'lifestyle', 'comedy'];

const ViralGauge = ({ level }) => {
  const pct = level === 'High' ? 85 : level === 'Moderate' ? 55 : 25;
  const color = level === 'High' ? '#22c55e' : level === 'Moderate' ? '#f59e0b' : '#ef4444';
  return (
    <div className="flex flex-col items-center py-4">
      <div className="relative w-32 h-32">
        <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
          <path d="M18 2 a16 16 0 0 1 0 32 a16 16 0 0 1 0-32"
            fill="none" stroke="#e2e8f0" strokeWidth="3" />
          <path d="M18 2 a16 16 0 0 1 0 32 a16 16 0 0 1 0-32"
            fill="none" stroke={color} strokeWidth="3"
            strokeDasharray={`${pct} 100`} strokeLinecap="round" />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <p className="text-2xl font-black" style={{ color }}>{pct}%</p>
          <p className="text-xs text-slate-500">{level}</p>
        </div>
      </div>
      <p className="text-sm font-semibold text-slate-600 mt-2">Viral Probability</p>
    </div>
  );
};

const ExploreSimulator = () => {
  const [niche, setNiche]   = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData]     = useState(null);

  const run = async () => {
    if (!niche) return;
    setLoading(true); setData(null);
    try {
      const res = await axios.post('/explore', { niche });
      setData(res.data);
    } catch (e) {
      setData({ error: e.response?.data?.error || 'Simulation failed' });
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-yellow-500" /> Explore Page Simulator
        </h2>
        <p className="text-sm text-slate-500 mb-4">Predict what type of content is likely to reach the Explore page in your niche right now.</p>
        <div className="flex flex-wrap gap-2 mb-4">
          {NICHES.map(n => (
            <button key={n} onClick={() => setNiche(n)}
              className={`px-4 py-2 rounded-full text-sm font-semibold capitalize transition-all
                ${niche === n ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-md' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
              {n}
            </button>
          ))}
        </div>
        <button onClick={run} disabled={!niche || loading}
          className="px-6 py-2.5 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-full font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-2">
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Simulating...</> : '⚡ Run Simulation'}
        </button>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Viral Gauge */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col items-center">
            <ViralGauge level={data.viral_probability} />
          </div>

          {/* Dominant Format */}
          <div className="bg-gradient-to-br from-yellow-400 to-orange-500 text-white rounded-2xl p-5 flex flex-col justify-center items-center text-center">
            <p className="text-xs font-semibold uppercase tracking-widest opacity-80 mb-2">Algorithm-Favored Format</p>
            <p className="text-3xl font-black capitalize">{data.dominant_format || 'Reels'}</p>
            <p className="text-sm opacity-80 mt-1">Post this format for best reach</p>
          </div>

          {/* Best Day */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 flex flex-col justify-center items-center text-center">
            <p className="text-xs font-semibold uppercase text-slate-500 tracking-widest mb-2">Best Day to Post</p>
            <p className="text-3xl font-black text-purple-600">{data.best_day || 'Tuesday'}</p>
            <p className="text-sm text-slate-500 mt-1">Caption style: {data.caption_style}</p>
          </div>

          {/* Recommendations */}
          <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">🎯 Actionable Predictions</h3>
            <ul className="space-y-2">
              {(data.recommendations || []).map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                  <span className="text-yellow-500 font-black shrink-0">{i + 1}.</span>
                  <span dangerouslySetInnerHTML={{ __html: r.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                </li>
              ))}
            </ul>
          </div>

          {/* Trending Hooks */}
          {data.trending_hooks?.length > 0 && (
            <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
              <h3 className="font-bold text-slate-800 mb-3">🔥 Trending Hook Examples</h3>
              <div className="space-y-2">
                {data.trending_hooks.map((h, i) => (
                  <div key={i} className="text-sm text-slate-700 bg-yellow-50 rounded-lg px-3 py-2 border-l-2 border-yellow-400">
                    "{h}"
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Hashtags */}
          {data.top_hashtags?.length > 0 && (
            <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
              <h3 className="font-bold text-slate-800 mb-3">Top Hashtags for Explore</h3>
              <div className="flex flex-wrap gap-2">
                {data.top_hashtags.map(({ hashtag }) => (
                  <span key={hashtag} className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-xs font-semibold">{hashtag}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ExploreSimulator;
