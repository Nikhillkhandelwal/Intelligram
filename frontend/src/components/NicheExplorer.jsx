/* NicheExplorer.jsx */
import React, { useState } from 'react';
import axios from 'axios';
import { Compass, Loader2, Hash, Lightbulb } from 'lucide-react';

const NICHES = ['fitness', 'choreography', 'real estate', 'personal branding', 'food', 'travel', 'fashion', 'business', 'lifestyle', 'comedy'];

const NicheExplorer = () => {
  const [niche, setNiche]   = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData]     = useState(null);

  const run = async () => {
    if (!niche) return;
    setLoading(true); setData(null);
    try {
      const res = await axios.post('/niche', { niche });
      setData(res.data);
    } catch (e) {
      setData({ error: e.response?.data?.error || 'Niche research failed' });
    } finally { setLoading(false); }
  };

  let aiData = {};
  try { aiData = data?.ai_insights ? JSON.parse(data.ai_insights) : {}; } catch {}

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Compass className="w-5 h-5 text-orange-500" /> Niche Explorer
        </h2>
        <div className="flex flex-wrap gap-2 mb-4">
          {NICHES.map(n => (
            <button key={n} onClick={() => setNiche(n)}
              className={`px-4 py-2 rounded-full text-sm font-semibold capitalize transition-all
                ${niche === n ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-md' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
              {n}
            </button>
          ))}
        </div>
        <button onClick={run} disabled={!niche || loading}
          className="px-6 py-2.5 bg-gradient-to-r from-orange-400 to-pink-500 text-white rounded-full font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-2">
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Researching...</> : '🔍 Research Niche'}
        </button>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* AI Summary */}
          {aiData.summary && (
            <div className="col-span-full bg-gradient-to-r from-orange-500 to-pink-500 text-white rounded-2xl p-5">
              <p className="text-xs font-semibold uppercase tracking-widest opacity-80 mb-1">AI Niche Summary</p>
              <p className="text-base leading-relaxed">{aiData.summary}</p>
            </div>
          )}

          {/* Content Ideas */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-yellow-500" /> Content Ideas
            </h3>
            <ul className="space-y-2">
              {(aiData.content_ideas || data.content_ideas || []).map((idea, i) => (
                <li key={i} className="text-sm text-slate-700 bg-yellow-50 rounded-lg px-3 py-2 border-l-2 border-yellow-400">
                  {idea}
                </li>
              ))}
            </ul>
          </div>

          {/* Caption Frameworks */}
          {aiData.caption_frameworks?.length > 0 && (
            <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
              <h3 className="font-bold text-slate-800 mb-3">✍️ Caption Frameworks</h3>
              <ul className="space-y-2">
                {aiData.caption_frameworks.map((fw, i) => (
                  <li key={i} className="text-sm text-slate-700 bg-slate-50 rounded-lg px-3 py-2">{fw}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Hashtag Clusters */}
          <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Hash className="w-4 h-4 text-blue-500" /> Hashtag Clusters
            </h3>
            <div className="space-y-3">
              <div>
                <p className="text-xs font-semibold text-slate-500 mb-1.5 uppercase">High Reach</p>
                <div className="flex flex-wrap gap-2">
                  {(data.hashtag_clusters?.high_reach || []).map(tag => (
                    <span key={tag} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">{tag}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs font-semibold text-slate-500 mb-1.5 uppercase">Niche Specific</p>
                <div className="flex flex-wrap gap-2">
                  {(data.hashtag_clusters?.niche_specific || []).map(tag => (
                    <span key={tag} className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-xs font-semibold">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Growth Tips */}
          {aiData.growth_tips?.length > 0 && (
            <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
              <h3 className="font-bold text-slate-800 mb-3">🚀 Growth Tips for {data.niche}</h3>
              <ul className="space-y-2">
                {aiData.growth_tips.map((tip, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-700">
                    <span className="text-orange-500 font-bold shrink-0">{i + 1}.</span> {tip}
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

export default NicheExplorer;
