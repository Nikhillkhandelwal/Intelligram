/**
 * IntelligenceHub.jsx
 * Merged panel: Trends + Niche Research + Explore Simulation
 * India-focused: viral songs, Hinglish hooks, Indian hashtags
 */
import React, { useState } from 'react';
import axios from 'axios';
import {
  TrendingUp, Compass, Zap, Hash, Music, Lightbulb,
  Clock, Copy, Check, Loader2, ChevronDown, ChevronUp, AlertCircle, Sparkles, Target, BookOpen
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const NICHES = [
  'fitness', 'choreography', 'fashion', 'food', 'business',
  'motivation', 'real estate', 'lifestyle', 'comedy', 'travel',
  'education', 'beauty',
];

// ── Small helpers ──────────────────────────────────────────────────────────
const CopyButton = ({ text }) => {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
      className="text-xs px-2 py-1 rounded-md bg-white/20 hover:bg-white/30 text-current flex items-center gap-1"
    >
      {copied ? <><Check className="w-3 h-3" /> Copied</> : <><Copy className="w-3 h-3" /> Copy</>}
    </button>
  );
};

// ── Dashboard Components ──────────────────────────────────────────────────
const Card = ({ title, icon: Icon, children, gradient, className = "" }) => (
  <div className={`bg-white rounded-3xl p-6 shadow-xl border border-slate-100 relative overflow-hidden ${className}`}>
    {gradient && <div className={`absolute top-0 left-0 w-full h-1.5 ${gradient}`} />}
    <div className="flex items-center gap-3 mb-6">
      {Icon && (
        <div className="p-2 rounded-xl bg-slate-50">
          <Icon className="w-5 h-5 text-slate-600" />
        </div>
      )}
      <h3 className="text-lg font-black text-slate-900 uppercase tracking-tight">{title}</h3>
    </div>
    {children}
  </div>
);

const VisualCard = ({ visuals }) => {
  if (!visuals) return null;
  return (
    <Card title="Visual Strategy" icon={Sparkles} gradient="bg-gradient-to-r from-purple-500 to-pink-500">
      <div className="space-y-4">
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Color Palette</p>
          <div className="flex gap-2">
            {visuals.palette?.map(color => (
              <span key={color} className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-xs font-bold">{color}</span>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Lighting</p>
            <p className="text-sm text-slate-700 font-medium">{visuals.lighting}</p>
          </div>
          <div>
            <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Style</p>
            <p className="text-sm text-slate-700 font-medium">{visuals.style}</p>
          </div>
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Winning Patterns</p>
          <div className="space-y-2">
            {visuals.patterns?.map((p, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-slate-600 bg-slate-50 p-2 rounded-lg">
                <div className="w-1.5 h-1.5 rounded-full bg-pink-400" /> {p}
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};

const HookCard = ({ hooks }) => {
  if (!hooks) return null;
  return (
    <Card title="Hook Architecture" icon={Target} gradient="bg-gradient-to-r from-blue-500 to-cyan-500">
      <p className="text-xs text-slate-500 mb-4 italic">"{hooks.analysis}"</p>
      <div className="space-y-3">
        {hooks.templates?.map((t, i) => (
          <div key={i} className="group cursor-pointer">
            <div className="bg-slate-50 group-hover:bg-blue-50 border border-slate-100 group-hover:border-blue-200 p-3 rounded-2xl transition-all">
              <p className="text-sm font-bold text-slate-900 mb-1">{t.hook}</p>
              <p className="text-[10px] text-slate-400 font-medium">{t.logic}</p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

const CaptionCard = ({ captions }) => {
  if (!captions) return null;
  return (
    <Card title="Caption Mastery" icon={Lightbulb} gradient="bg-gradient-to-r from-orange-500 to-yellow-500">
      <div className="space-y-4">
        <div className="flex justify-between items-center bg-orange-50 p-3 rounded-2xl">
          <p className="text-xs font-bold text-orange-700">Ideal Length</p>
          <p className="text-xs font-black text-orange-900">{captions.ideal_length}</p>
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Winning Template</p>
          <div className="bg-slate-900 text-slate-300 p-4 rounded-2xl text-[11px] font-mono leading-relaxed relative group">
            <button className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-white/10 p-1.5 rounded-lg"><Copy className="w-3 h-3 text-white"/></button>
            {captions.winning_template}
          </div>
        </div>
        <div>
           <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Triggers</p>
           <div className="flex flex-wrap gap-2">
             {captions.triggers?.map(t => (
               <span key={t} className="px-2 py-1 bg-slate-100 text-slate-600 rounded-lg text-[10px] font-bold">{t}</span>
             ))}
           </div>
        </div>
      </div>
    </Card>
  );
};

const SEOCard = ({ seo }) => {
  if (!seo) return null;
  return (
    <Card title="SEO & Keywords" icon={Hash} gradient="bg-gradient-to-r from-green-500 to-emerald-500">
      <div className="space-y-4">
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Hashtag Strategy</p>
          <p className="text-sm text-slate-700 font-medium leading-tight">{seo.hashtag_mix}</p>
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Hidden Gem Tags</p>
          <div className="flex flex-wrap gap-1.5">
            {seo.hidden_gems?.map(tag => (
              <span key={tag} className="px-2 py-1 bg-green-50 text-green-700 rounded-lg text-[10px] font-black">{tag}</span>
            ))}
          </div>
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-400 uppercase mb-2">Prime Keywords</p>
          <div className="flex flex-wrap gap-1.5">
            {seo.keywords?.map(kw => (
              <span key={kw} className="px-2 py-1 bg-slate-100 text-slate-600 rounded-lg text-[10px] font-bold border border-slate-200">{kw}</span>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};

const ExecutionTimeline = ({ plan }) => {
  if (!plan) return null;
  return (
    <div className="col-span-full bg-slate-900 rounded-[2.5rem] p-8 text-white shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 blur-[100px] rounded-full" />
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2.5 bg-white/10 rounded-2xl">
          <Clock className="w-6 h-6 text-purple-400" />
        </div>
        <div>
          <h3 className="text-2xl font-black italic tracking-tighter">7-DAY EXECUTION BLUEPRINT</h3>
          <p className="text-xs text-white/50 uppercase font-bold tracking-widest">Immediate Growth Protocol</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-7 gap-4">
        {plan.map((day, i) => (
          <div key={i} className="bg-white/5 border border-white/10 rounded-2xl p-4 hover:bg-white/10 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[10px] font-black text-purple-400">DAY {day.day}</span>
              <span className="text-[8px] bg-white/10 px-2 py-0.5 rounded-full font-bold">{day.type}</span>
            </div>
            <p className="text-xs font-bold mb-2 leading-snug">{day.topic}</p>
            <div className="pt-2 border-t border-white/5">
              <p className="text-[9px] text-white/40 uppercase font-bold mb-1">Key Factor</p>
              <p className="text-[10px] text-white/70 italic leading-tight">{day.success_factor}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const DetailedPostPlan = ({ posts }) => {
  if (!posts || posts.length === 0) return null;
  return (
    <div className="col-span-full mt-12">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-2.5 bg-purple-100 rounded-2xl">
          <BookOpen className="w-6 h-6 text-purple-600" />
        </div>
        <div>
          <h3 className="text-3xl font-black text-slate-900 tracking-tighter uppercase">10-Post Detailed Content Plan</h3>
          <p className="text-xs text-slate-400 font-black uppercase tracking-[0.2em]">Strategy-to-Execution Map</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {posts.map((post, i) => (
          <div key={i} className="bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-xl hover:shadow-2xl transition-all group relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-[0.03] group-hover:scale-110 transition-transform">
              <Sparkles className="w-24 h-24" />
            </div>
            
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center gap-4">
                <span className="w-12 h-12 rounded-2xl bg-slate-900 text-white flex items-center justify-center font-black text-xl shadow-lg">
                  {post.post_num}
                </span>
                <div>
                  <span className="text-[10px] font-black text-purple-600 uppercase tracking-widest bg-purple-50 px-3 py-1 rounded-full">
                    {post.type}
                  </span>
                  <h4 className="text-lg font-black text-slate-900 mt-1">{post.hook}</h4>
                </div>
              </div>
              <div className="flex flex-col items-end">
                 <span className="text-[10px] font-black text-green-500 uppercase tracking-tighter bg-green-50 px-3 py-1 rounded-full">
                   Insight Applied
                 </span>
                 <p className="text-[10px] text-slate-400 font-bold mt-1 text-right max-w-[150px] leading-tight">{post.insight_applied}</p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-slate-50 p-5 rounded-3xl border border-slate-100">
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Content Strategy</p>
                <p className="text-sm text-slate-700 font-medium leading-relaxed">{post.content}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50/50 rounded-2xl border border-blue-100/50">
                  <p className="text-[9px] font-black text-blue-400 uppercase tracking-widest mb-2 flex items-center gap-1.5"><Compass className="w-3 h-3" /> Visual Direction</p>
                  <p className="text-[11px] text-blue-900 font-bold leading-tight">{post.visuals}</p>
                </div>
                <div className="p-4 bg-orange-50/50 rounded-2xl border border-orange-100/50">
                  <p className="text-[9px] font-black text-orange-400 uppercase tracking-widest mb-2 flex items-center gap-1.5"><Lightbulb className="w-3 h-3" /> Caption Focus</p>
                  <p className="text-[11px] text-orange-900 font-bold leading-tight">{post.caption}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const NicheInsightPanel = ({ insights }) => {
  if (!insights) return null;
  return (
    <div className="col-span-full grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
      <div className="lg:col-span-2 bg-gradient-to-br from-indigo-900 to-slate-900 rounded-[2.5rem] p-8 text-white shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-10 opacity-10">
          <Music className="w-40 h-40" />
        </div>
        <h4 className="text-xl font-black mb-6 uppercase tracking-tight flex items-center gap-3">
          <Music className="text-pink-400" /> Trending Sounds & Retention Audio
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insights.trending_songs?.map((song, i) => (
            <div key={i} className="bg-white/5 border border-white/10 p-4 rounded-2xl flex items-center gap-4 hover:bg-white/10 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center">
                <Music className="w-5 h-5 text-pink-400" />
              </div>
              <div>
                <p className="text-sm font-black">{song.title}</p>
                <p className="text-[10px] text-white/40 font-bold uppercase">{song.artist}</p>
                <p className="text-[10px] text-pink-300 italic mt-1 leading-snug">{song.reason}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-xl flex flex-col justify-between">
        <div>
          <div className="p-3 bg-purple-50 rounded-2xl inline-block mb-6">
            <Target className="w-6 h-6 text-purple-600" />
          </div>
          <h4 className="text-xl font-black text-slate-900 mb-2 uppercase tracking-tight">Audience Sentiment</h4>
          <p className="text-sm text-slate-500 leading-relaxed font-medium">{insights.audience_vibe}</p>
        </div>
        <div className="mt-8 pt-8 border-t border-slate-50">
          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3">Hashtag Matrix</p>
          <p className="text-xs text-slate-700 font-bold leading-relaxed">{insights.hashtag_strategy}</p>
        </div>
      </div>
    </div>
  );
};

const BarChart = ({ data }) => {
  const chartData = data || {};
  const values = Object.values(chartData);
  const max = values.length > 0 ? Math.max(...values, 1) : 1;
  return (
    <div className="space-y-1.5">
      {Object.entries(chartData).map(([type, count]) => (
        <div key={type} className="flex items-center gap-2 text-xs">
          <span className="w-16 text-right text-slate-500 capitalize">{type}</span>
          <div className="flex-1 bg-slate-100 rounded-full h-2">
            <div className="bg-gradient-to-r from-purple-500 to-pink-400 h-2 rounded-full transition-all"
              style={{ width: `${(count / max) * 100}%` }} />
          </div>
          <span className="text-slate-500 w-4 text-right">{count}</span>
        </div>
      ))}
    </div>
  );
};

// ── Main component ─────────────────────────────────────────────────────────
const IntelligenceHub = () => {
  const [niche, setNiche] = useState('');
  const [loading, setLoading] = useState(false);
  const [deepLoading, setDeepLoading] = useState(false);
  const [data, setData] = useState(null);
  const [deepData, setDeepData] = useState(null);
  const [showAllSongs, setShowAllSongs] = useState(false);

  const run = async () => {
    if (!niche) return;
    setLoading(true); setData(null); setDeepData(null); setShowAllSongs(false);

    try {
      // Fire all 4 requests in parallel (including deep analysis)
      const [trendRes, nicheRes, exploreRes, deepRes] = await Promise.allSettled([
        axios.post('/trend',         { niche }),
        axios.post('/niche',         { niche }),
        axios.post('/explore',       { niche }),
        axios.post('/deep_analysis', { hashtag: niche }),
      ]);

      setData({
        niche,
        trend:   trendRes.status   === 'fulfilled' ? trendRes.value.data   : null,
        niche_r: nicheRes.status   === 'fulfilled' ? nicheRes.value.data   : null,
        explore: exploreRes.status === 'fulfilled' ? exploreRes.value.data : null,
      });

      if (deepRes.status === 'fulfilled') {
        setDeepData(deepRes.value.data);
      }
    } catch (e) {
      setData({ error: 'Failed to load intelligence data.' });
    } finally {
      setLoading(false);
      setDeepLoading(false); // Reset deep loading too
    }
  };

  // We keep runDeepAnalysis as a separate helper but it's now called within run() conceptually via the parallel block
  // But let's actually just define it inside or simplify. I'll just remove the standalone runDeepAnalysis to keep it clean.

  // Merge viral songs source
  const ai          = data?.trend?.ai_summary || {};
  const isLive      = data?.trend?.is_live !== false; // Default to true if missing
  const songs       = ai.viral_songs || data?.trend?.viral_songs || [];
  const raw         = data?.trend?.raw_trends || data?.trend || {};
  const nicheData   = data?.niche_r || {};
  const exploreData = data?.explore || {};

  let nicheAI = {};
  try { nicheAI = nicheData.ai_insights ? JSON.parse(nicheData.ai_insights) : {}; } catch {}

  const displayedSongs = Array.isArray(songs) ? (showAllSongs ? songs : songs.slice(0, 6)) : [];

  return (
    <div className="space-y-6">
      {/* ── Search Bar ────────────────────────────────────────────────── */}
      <div className="bg-gradient-to-r from-purple-700 to-pink-600 rounded-2xl p-6 text-white">
        <h2 className="text-xl font-black mb-1 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" /> Intelligence Hub
          <span className="text-xs font-normal bg-white/20 px-2 py-0.5 rounded-full">🇮🇳 India-Focused</span>
        </h2>
        <p className="text-sm opacity-80 mb-4">Search any niche or #hashtag to analyze real Indian trends.</p>
        
        <input 
          type="text" 
          placeholder="Enter a niche or #hashtag (e.g. #streetfood)"
          value={niche}
          onChange={(e) => setNiche(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && run()}
          className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-white mb-4 placeholder-white/60 text-white"
        />

        <div className="flex flex-wrap gap-2 mb-4">
          {NICHES.map(n => (
            <button key={n} onClick={() => setNiche(n)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition-all
                ${niche === n ? 'bg-white text-purple-700 shadow-md' : 'bg-white/20 hover:bg-white/30 text-white'}`}>
              {n}
            </button>
          ))}
        </div>
        <button onClick={run} disabled={!niche || loading}
          className="px-6 py-2.5 bg-white text-purple-700 rounded-full font-black hover:opacity-90 disabled:opacity-50 flex items-center gap-2 text-sm">
          {loading
            ? <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing {niche}...</>
            : `🔍 Analyze "${niche || 'niche'}"`}
        </button>
      </div>

      {data?.error && <p className="text-red-500 text-sm px-2">{data.error}</p>}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          {/* ── Loading State ───────────────────── */}
          {(deepLoading || (loading && !data)) && (
            <div className="col-span-full bg-white rounded-3xl p-12 text-center shadow-xl border border-purple-100">
              <div className="relative w-20 h-20 mx-auto mb-6">
                <div className="absolute inset-0 border-4 border-purple-100 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-purple-600 rounded-full border-t-transparent animate-spin"></div>
                <Sparkles className="absolute inset-0 m-auto w-8 h-8 text-purple-600 animate-pulse" />
              </div>
              <h3 className="text-xl font-black text-slate-900 mb-2">Architecting Your Strategy...</h3>
              <p className="text-sm text-slate-500 max-w-xs mx-auto">
                We're scraping 30 viral posts across 3 hashtags to find the winning patterns perfectly matched for your niche.
              </p>
            </div>
          )}

          {deepData && !deepLoading && (
            <>
              {/* ── Deep Strategy Row 1 ───────────────────── */}
              {!deepData.is_live && (
                <div className="col-span-full bg-amber-50 border border-amber-200 rounded-3xl p-6 flex items-start gap-4 mb-2 animate-in fade-in slide-in-from-top-4 duration-700">
                  <div className="bg-amber-500 p-3 rounded-2xl shrink-0">
                    <Sparkles className="w-6 h-6 text-white animate-pulse" />
                  </div>
                  <div>
                    <h4 className="font-bold text-amber-900">Predicted Deep Intelligence Active</h4>
                    <p className="text-sm text-amber-700 opacity-80 mt-1">
                      Live deep analysis is currently limited. We've generated this premium 10-post strategy based on our historical data and proven growth patterns for the <strong>{deepData.base_hashtag}</strong> genre.
                    </p>
                  </div>
                </div>
              )}
              <VisualCard visuals={deepData.strategy_report?.visuals} />
              <HookCard hooks={deepData.strategy_report?.hooks} />
              <CaptionCard captions={deepData.strategy_report?.captions} />
              <SEOCard seo={deepData.strategy_report?.seo} />

              {/* ── Execution Plan ────────────────────────── */}
              <ExecutionTimeline plan={deepData.strategy_report?.execution_plan} />

              {/* ── Niche Insights & 10-Post Plan ─────────── */}
              <NicheInsightPanel insights={deepData.strategy_report?.niche_insights} />
              <DetailedPostPlan posts={deepData.strategy_report?.detailed_10_post_plan} />

              {/* ── Reference High Performers ──────────────── */}
              <div className="col-span-full">
                <h4 className="font-black text-slate-900 mb-6 flex items-center gap-2 text-xl uppercase tracking-tight">
                  <Target className="w-6 h-6 text-pink-500" /> Reference High-Performers
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                  {deepData.top_posts?.map((post, i) => (
                    <div key={i} className="bg-white rounded-[2rem] p-4 border border-slate-100 shadow-lg hover:translate-y-[-4px] transition-transform">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-[10px] font-black text-purple-600 bg-purple-50 px-3 py-1 rounded-full uppercase tracking-widest">{post.type}</span>
                        <div className="flex items-center gap-1 text-[10px] font-black text-slate-400">
                          <Zap className="w-3 h-3 text-yellow-400" /> {post.engagement_rate}%
                        </div>
                      </div>
                      <p className="text-xs text-slate-600 line-clamp-4 leading-relaxed italic mb-4">"{post.caption}"</p>
                      <div className="flex items-center gap-4 text-[10px] font-bold text-slate-400 mt-auto pt-4 border-t border-slate-50">
                        <span className="flex items-center gap-1"><Check className="w-3 h-3" /> {post.likes.toLocaleString()} Likes</span>
                        <span className="flex items-center gap-1"><Music className="w-3 h-3" /> {post.comments.toLocaleString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* ── Integrated Insights Row ────────────────── */}
          <div className="col-span-full grid grid-cols-1 md:grid-cols-3 gap-6 pt-10 mt-10 border-t border-slate-100">
             
             {/* Algorithm Insight Card */}
             <div className="bg-gradient-to-br from-slate-900 to-purple-900 text-white rounded-[2.5rem] p-8 shadow-2xl relative overflow-hidden group">
               <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform">
                 <TrendingUp className="w-32 h-32" />
               </div>
               <p className="text-[10px] font-black text-purple-400 uppercase tracking-[0.2em] mb-4">Algorithm Favouring</p>
               <h4 className="text-4xl font-black capitalize mb-6">{exploreData.dominant_format || 'Reels'}</h4>
               <div className="space-y-4 relative">
                 <div className="flex justify-between items-center bg-white/5 p-3 rounded-2xl">
                   <span className="text-xs text-white/60">Viral Probability</span>
                   <span className="text-xs font-black text-green-400">{exploreData.viral_probability || 'High'}</span>
                 </div>
                 <div className="flex justify-between items-center bg-white/5 p-3 rounded-2xl">
                   <span className="text-xs text-white/60">Prime Posting Time</span>
                   <span className="text-xs font-black text-purple-300">{exploreData.best_day || 'Tuesday'}</span>
                 </div>
               </div>
             </div>

             {/* Caption Intelligence Stats */}
             <Card title="Engagement Metrics" icon={Zap} gradient="bg-gradient-to-r from-pink-500 to-rose-500" className="md:col-span-2">
                <div className="grid grid-cols-3 gap-6 h-full">
                  {[
                    { label: 'Question Yield', val: raw.caption_signals?.questions_pct || '72', color: 'text-blue-500', desc: 'Direct audience engagement' },
                    { label: 'CTA Conversion', val: raw.caption_signals?.cta_pct || '84', color: 'text-green-500', desc: 'Action-oriented captions' },
                    { label: 'Visual Energy',  val: raw.caption_signals?.emoji_pct || '92', color: 'text-pink-500', desc: 'High emoji & symbol usage' },
                  ].map(({ label, val, color, desc }) => (
                    <div key={label} className="bg-slate-50 rounded-[2rem] p-6 flex flex-col justify-center">
                      <p className={`text-4xl font-black ${color} mb-1`}>{val}%</p>
                      <p className="text-xs font-black text-slate-800 mb-2 uppercase tracking-tighter">{label}</p>
                      <p className="text-[10px] text-slate-400 leading-tight">{desc}</p>
                    </div>
                  ))}
                </div>
             </Card>
          </div>

          {/* ── Asset Row: Songs, Hooks, Hashtags ───────── */}
          <div className="col-span-full grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Hooks Card */}
            <Card title="Community Hooks" icon={Music} gradient="bg-gradient-to-r from-purple-500 to-indigo-500">
               <div className="space-y-3">
                 {(raw.trending_hooks || []).slice(0, 4).map((hook, i) => (
                   <div key={i} className="bg-purple-50 p-3 rounded-2xl border-l-4 border-purple-400">
                     <p className="text-xs text-purple-900 font-medium leading-relaxed">"{hook}"</p>
                   </div>
                 ))}
                 {!raw.trending_hooks?.length && <p className="text-xs text-slate-400">Standardizing Hinglish hooks...</p>}
               </div>
            </Card>

            {/* Trending Audio */}
            <Card title="High-Retention Audio" icon={Music} gradient="bg-gradient-to-r from-pink-500 to-purple-500">
              <div className="space-y-2">
                {songs.slice(0, 5).map((song, i) => (
                  <div key={i} className="flex items-center gap-3 bg-slate-50 p-2 rounded-xl">
                    <div className="w-8 h-8 rounded-lg bg-pink-500 flex items-center justify-center shrink-0">
                      <Music className="w-4 h-4 text-white" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold truncate">{song.title}</p>
                      <p className="text-[10px] text-slate-400 truncate">{song.artist}</p>
                    </div>
                    <span className="text-[10px] font-black text-pink-600 ml-auto">HOT</span>
                  </div>
                ))}
              </div>
            </Card>

            {/* Content Ideas Clusters */}
            <Card title="Viral Content Ideas" icon={Lightbulb} gradient="bg-gradient-to-r from-orange-500 to-yellow-500">
              <div className="space-y-2">
                 {(nicheAI.content_ideas || nicheData.content_ideas || []).slice(0, 5).map((idea, i) => (
                   <div key={i} className="text-xs text-slate-700 bg-orange-50 rounded-xl px-4 py-3 border border-orange-100 flex items-center gap-3">
                     <span className="w-5 h-5 rounded-full bg-orange-200 text-orange-700 flex items-center justify-center text-[10px] font-black shrink-0">{i+1}</span>
                     {idea}
                   </div>
                 ))}
              </div>
            </Card>
          </div>

          {/* ── Prediction Alert Fallback ─────────────────────────── */}
          {!isLive && (
            <div className="col-span-full bg-blue-50 border border-blue-100 rounded-3xl p-6 flex items-start gap-4">
              <div className="bg-blue-500 p-3 rounded-2xl shrink-0">
                <Compass className="w-6 h-6 text-white animate-pulse" />
              </div>
              <div>
                <h4 className="font-bold text-blue-900">Historical Intelligence Active</h4>
                <p className="text-sm text-blue-700 opacity-80 mt-1">
                  We're using our database of 50,000+ Indian niche posts to provide these predictions while Instagram real-time access is limited.
                </p>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
};

export default IntelligenceHub;
