import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import MetricsCards from './components/MetricsCards';
import Charts from './components/Charts';
import ContentTable from './components/ContentTable';
import ReportViewer from './components/ReportViewer';
import RecommenderPanel from './components/RecommenderPanel';
import CompetitorCard from './components/CompetitorCard';
import IntelligenceHub from './components/IntelligenceHub';
import {
  Instagram, AlertCircle, CheckCircle2,
  TrendingUp, Sparkles, Search, BarChart2
} from 'lucide-react';

const TABS = [
  { id: 'audit',        label: 'Audit',       icon: BarChart2  },
  { id: 'intelligence', label: '🇮🇳 Intel Hub', icon: TrendingUp },
  { id: 'recommend',    label: 'AI Recs',      icon: Sparkles   },
  { id: 'competitor',   label: 'Competitor',   icon: Search     },
];

const App = () => {
  const [activeTab, setActiveTab] = useState('audit');
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);
  const [data, setData]           = useState(null);
  const [step, setStep]           = useState('Scraping...');

  const runAudit = async ({ username, competitors }) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      setStep('Scraping Instagram...');
      const response = await axios.post('/analyze', { username, competitors });
      setStep('AI Analysis in progress...');
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Check backend status.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafafa] pb-24 text-slate-900 font-sans selection:bg-purple-100 selection:text-purple-600">
      {/* ── Enterprise Header ── */}
      <header className="glass sticky top-0 z-50 py-5">
        <div className="container mx-auto px-6 flex justify-between items-center">
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="bg-slate-900 p-2 rounded-2xl group-hover:bg-purple-600 transition-colors shadow-xl shadow-slate-200">
              <Instagram className="text-white w-5 h-5" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-lg font-black tracking-tighter leading-none">
                INTELLIGRAM <span className="text-purple-600">.</span>
              </h1>
              <span className="text-[9px] text-slate-400 font-black uppercase tracking-[0.3em] mt-0.5">Agency OS</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-2 bg-slate-100 p-1.5 rounded-2xl border border-slate-200">
            {TABS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex items-center gap-2 px-6 py-2 rounded-xl text-[11px] font-black uppercase tracking-widest transition-all
                  ${activeTab === id
                    ? 'bg-white text-slate-900 shadow-sm'
                    : 'text-slate-400 hover:text-slate-600'}`}
              >
                <Icon className="w-3.5 h-3.5" />
                {label}
              </button>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-[10px] font-black uppercase text-slate-400 tracking-widest">System Status</span>
              <span className="text-[11px] font-bold text-green-500 flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" /> Operational</span>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 mt-16 max-w-7xl">

        {/* ── AUDIT TAB ── */}
        {activeTab === 'audit' && (
          <div className="animate-in fade-in duration-1000">
            {!data && !loading && (
              <div className="max-w-4xl mx-auto">
                <div className="text-center space-y-10 mb-20">
                  <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-50 text-purple-600 rounded-full text-[10px] font-black uppercase tracking-[0.3em] mb-4">
                    Enterprise Marketing Engine
                  </div>
                  <h1 className="text-7xl xl:text-8xl font-black text-slate-900 tracking-tighter leading-[0.9]">
                    Instagram <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-br from-slate-900 via-slate-700 to-slate-500">Intelligence.</span>
                  </h1>
                  <p className="text-xl text-slate-500 max-w-2xl mx-auto leading-relaxed font-medium">
                    The world's most advanced audit engine for agencies. 
                    Deep metrics, competitor benchmarking, and AI roadmap.
                  </p>
                </div>
                
                <div className="premium-card relative group hover:shadow-[0_80px_100px_-20px_rgba(0,0,0,0.08)] transition-all duration-700">
                  <div className="absolute top-0 right-0 p-10 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity pointer-events-none">
                     <TrendingUp className="w-64 h-64 -rotate-12" />
                  </div>
                  <InputForm onAnalyze={runAudit} loading={loading} />
                </div>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center py-40 space-y-10">
                <div className="relative">
                  <div className="w-32 h-32 border-[6px] border-slate-100 border-t-purple-600 rounded-full animate-spin shadow-2xl" />
                  <div className="absolute inset-2 border-[6px] border-transparent border-t-pink-500 rounded-full animate-spin-slow opacity-50" />
                  <Instagram className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-slate-900 w-10 h-10 animate-float" />
                </div>
                <div className="text-center space-y-2">
                  <h2 className="text-3xl font-black text-slate-900 tracking-tighter uppercase">Initializing Engine</h2>
                  <div className="flex items-center gap-2 justify-center">
                    <span className="text-purple-600 font-black text-xs uppercase tracking-[0.3em] animate-pulse">{step}</span>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="bg-white border border-red-100 p-10 rounded-[2.5rem] shadow-2xl flex flex-col items-center text-center gap-6 max-w-2xl mx-auto mt-8 group animate-in zoom-in-95 duration-500">
                <div className="p-5 bg-red-50 rounded-3xl text-red-500 group-hover:scale-110 transition-transform">
                  <AlertCircle className="w-10 h-10" />
                </div>
                <div>
                  <h3 className="text-xl font-black text-slate-900 uppercase tracking-tight mb-2">Analysis Stalled</h3>
                  <p className="text-slate-500 font-medium">{error}</p>
                </div>
                <button onClick={() => setError(null)} className="px-8 py-3 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-black transition-colors">
                  Reset System
                </button>
              </div>
            )}

            {data && (
              <div className="space-y-16 animate-in fade-in slide-in-from-bottom-10 duration-1000">
                <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-8 border-b border-slate-200 pb-12">
                  <div>
                    <div className="flex items-center gap-3 text-purple-600 text-[10px] font-black uppercase tracking-[0.4em] mb-4">
                      <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" /> Audit Executed Successfully
                    </div>
                    <h2 className="text-7xl font-black text-slate-900 tracking-tighter lowercase leading-none">@{data.username}</h2>
                    {data.is_live === false && (
                      <div className="mt-4 flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-blue-100">
                        <Sparkles className="w-3 h-3 animate-pulse" /> Predicted Intelligence Active (Live Scraping Limited)
                      </div>
                    )}
                    <p className="text-slate-400 font-bold mt-4 text-sm uppercase tracking-widest flex items-center gap-2">
                       <BarChart2 className="w-4 h-4" /> Comprehensive Data Set ({data.posts?.length} Points)
                    </p>
                  </div>
                  <button onClick={() => setData(null)} className="px-10 py-4 bg-slate-100 text-slate-900 font-black text-[11px] uppercase tracking-widest rounded-2xl hover:bg-slate-900 hover:text-white transition-all shadow-sm">
                    Generate New Report
                  </button>
                </div>
                
                <MetricsCards metrics={data.metrics} />
                <Charts posts={data.posts} />
                <ReportViewer report={data.audit_report} username={data.username} />
                <ContentTable posts={data.posts} />
              </div>
            )}
          </div>
        )}

        {/* ── OTHER TABS ── */}
        {activeTab === 'intelligence' && <IntelligenceHub />}
        {activeTab === 'recommend'    && <RecommenderPanel />}
        {activeTab === 'competitor'   && <CompetitorCard />}
      </main>

      <footer className="mt-20 py-10 border-t border-slate-100 text-center text-slate-400 text-xs">
        <p>© 2026 IntelliGram — AI Marketing Intelligence Engine. Not affiliated with Meta Inc.</p>
      </footer>
    </div>
  );
};

export default App;
