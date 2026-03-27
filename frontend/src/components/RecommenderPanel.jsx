/* RecommenderPanel.jsx */
import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Copy, Check, Loader2, Clock, Hash, Music, Play, Video, ChevronRight, FileText } from 'lucide-react';

// Helper: convert 24h hour to 12h IST string
const toIST = (hour) => {
  const h12 = hour % 12 || 12;
  const ampm = hour < 12 ? 'AM' : 'PM';
  return `${h12}:00 ${ampm} IST`;
};

const NICHES = ['fitness', 'choreography', 'real estate', 'personal branding', 'food', 'travel', 'fashion', 'business', 'comedy'];

const CopyButton = ({ text, label }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button onClick={copy} className="text-[10px] font-black uppercase tracking-widest px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center gap-1.5 transition-all active:scale-95 shadow-sm border border-slate-200/50">
      {copied ? <><Check className="w-3 h-3 text-green-500" /> Copied</> : <><Copy className="w-3 h-3" /> {label || 'Copy'}</>}
    </button>
  );
};

const RecommenderPanel = () => {
  const [topic, setTopic] = useState('');
  const [niche, setNiche] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const run = async () => {
    if (!topic) return;
    setLoading(true); setData(null);
    try {
      const res = await axios.post('/recommend', { topic, niche });
      setData(res.data);
    } catch (e) {
      setData({ error: e.response?.data?.error || 'Recommendation failed' });
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-6">
      {/* Input */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
        <h2 className="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-yellow-500" /> AI Content Recommender
        </h2>
        <input
          type="text"
          placeholder="Enter your reel topic (e.g. morning routine for productivity)"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && run()}
          className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-purple-400 mb-3"
        />
        <div className="flex flex-wrap gap-2 mb-4">
          {NICHES.map(n => (
            <button key={n} onClick={() => setNiche(n)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition-all
                ${niche === n ? 'bg-purple-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
              {n}
            </button>
          ))}
        </div>
        <button onClick={run} disabled={!topic || loading}
          className="px-6 py-2.5 bg-gradient-to-r from-yellow-400 to-orange-500 text-white rounded-full font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-2">
          {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Generating...</> : '✨ Generate Recommendations'}
        </button>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          
          {/* 🎬 5-7 Reels Scripts (New Section) */}
          <div className="bg-white rounded-3xl p-8 shadow-[0_20px_50px_-15px_rgba(0,0,0,0.05)] border border-slate-100 flex flex-col">
            <h3 className="text-xl font-black text-slate-900 mb-6 flex items-center gap-3">
              <div className="p-2 bg-pink-100 rounded-xl text-pink-600">
                <Video className="w-5 h-5" />
              </div>
              5-7 Viral Reel Scripts
            </h3>
            <div className="space-y-6 flex-1 overflow-y-auto pr-2 max-h-[1000px] scrollbar-thin scrollbar-thumb-slate-200">
              {(data.scripts || []).map((script, i) => (
                <div key={i} className="bg-slate-50 rounded-2xl p-6 border border-slate-100 group hover:border-pink-200 transition-colors">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] font-black text-pink-600 uppercase tracking-widest bg-pink-50 px-3 py-1 rounded-full">Script {i + 1}: {script.title}</span>
                    <CopyButton text={`Hook: ${script.hook}\nBody: ${script.body}\nCTA: ${script.cta}`} />
                  </div>
                  <div className="space-y-4">
                    <div>
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mb-1">🪝 THE HOOK</p>
                      <p className="text-sm font-black text-slate-900 leading-tight">"{script.hook}"</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mb-1">📝 THE BODY</p>
                      <p className="text-xs text-slate-600 leading-relaxed font-medium">{script.body}</p>
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter mb-1">🎯 THE CTA</p>
                      <p className="text-xs font-bold text-purple-600">"{script.cta}"</p>
                    </div>
                  </div>
                </div>
              ))}
              {(!data.scripts || data.scripts.length === 0) && (
                <div className="text-center py-20 bg-slate-50/50 rounded-3xl border border-dashed border-slate-200">
                   <p className="text-slate-400 text-sm font-medium italic">Generating unique script structures...</p>
                </div>
              )}
            </div>
          </div>

          {/* ✍️ 20 Optimized Captions */}
          <div className="bg-white rounded-3xl p-8 shadow-[0_20px_50px_-15px_rgba(0,0,0,0.05)] border border-slate-100">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-black text-slate-900 flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-xl text-purple-600">
                  <FileText className="w-5 h-5" />
                </div>
                20 Optimized Captions
              </h3>
              <div className="flex items-center gap-4">
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{data.captions?.length || 0} Ready</span>
                <CopyButton text={(data.captions || []).join('\n\n')} label="Copy All" />
              </div>
            </div>
            <div className="space-y-3 max-h-[1000px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-slate-200">
              {(data.captions || []).map((cap, i) => (
                <div key={i} className="bg-slate-50 rounded-xl p-4 border border-slate-100 hover:bg-white hover:border-purple-100 transition-all cursor-default group">
                  <div className="flex justify-between items-start mb-2 opacity-40 group-hover:opacity-100 transition-opacity">
                    <span className="text-[10px] font-black text-purple-600 uppercase">#{i + 1}</span>
                    <CopyButton text={cap} />
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed font-medium line-clamp-3 group-hover:line-clamp-none transition-all">{cap}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Hooks */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3">🎣 Hook Suggestions (First 3s)</h3>
            <ul className="space-y-2">
              {(data.hooks || []).map((hook, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-yellow-500 font-black text-sm shrink-0">→</span>
                  <span className="text-sm text-slate-700">{hook}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Best Time */}
          <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <h3 className="font-bold text-slate-800 mb-3 flex items-center gap-2">
              <Clock className="w-4 h-4 text-green-500" /> Best Posting Time
            </h3>
            {data.best_time && (
              <div className="text-center py-4">
                <p className="text-4xl font-black text-purple-600">{data.best_time.day}</p>
                <p className="text-slate-500 text-sm mt-1">{toIST(data.best_time.hour ?? 19)}</p>
                <span className="inline-block mt-2 px-3 py-1 bg-green-50 text-green-700 text-xs font-bold rounded-full">🇮🇳 Indian Standard Time</span>
              </div>
            )}
            <div className="mt-3 space-y-1">
              {(data.improvement_tips || []).slice(0, 3).map((tip, i) => (
                <p key={i} className="text-xs text-slate-600 flex gap-1.5">
                  <span className="text-orange-400">•</span> {tip}
                </p>
              ))}
            </div>
          </div>

          {/* Hashtags */}
          <div className="col-span-full bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-slate-800 flex items-center gap-2">
                <Hash className="w-4 h-4 text-blue-500" /> {(data.hashtags || []).length} Hashtags
              </h3>
              <CopyButton text={(data.hashtags || []).join(' ')} />
            </div>
            <div className="flex flex-wrap gap-2">
              {(data.hashtags || []).map(tag => (
                <span key={tag} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold">{tag}</span>
              ))}
            </div>
          </div>
          {/* Viral Songs */}
          {(data.viral_songs || []).length > 0 && (
            <div className="col-span-full bg-gradient-to-br from-slate-900 to-purple-900 text-white rounded-2xl p-5">
              <h3 className="font-bold mb-3 flex items-center gap-2">
                <Music className="w-4 h-4 text-pink-400" /> 🎵 Indian Viral Songs for Your Reel
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                {(data.viral_songs || []).slice(0, 6).map((s, i) => (
                  <div key={i} className="flex items-center gap-2 bg-white/10 rounded-xl px-3 py-2">
                    <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center shrink-0">
                      <Music className="w-3.5 h-3.5 text-white" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold truncate">{s.title}</p>
                      <p className="text-xs opacity-60 truncate">{s.artist}</p>
                    </div>
                    <span className="text-xs shrink-0 ml-auto">{s.trend}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RecommenderPanel;
