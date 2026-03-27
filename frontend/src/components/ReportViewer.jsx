import React, { useState, useRef } from 'react';
import { 
  Download, Share2, FileText, Sparkles, Zap, 
  BarChart3, TrendingUp, CheckCircle2, Instagram,
  Users, Search, Loader2
} from 'lucide-react';
import jsPDF from 'jspdf';
import domToImage from 'dom-to-image-more';

const ReportViewer = ({ report, username }) => {
  const reportRef = useRef(null);
  const [isExporting, setIsExporting] = useState(false);

  const exportPDF = async () => {
    if (!reportRef.current) return;
    setIsExporting(true);

    try {
      const element = reportRef.current;
      
      // 1. Capture full quality PNG from DOM
      // dom-to-image-more handles modern CSS (oklch, grid, etc.) much better than html2canvas
      const imgData = await domToImage.toPng(element, {
        bgcolor: '#f8fafc',
        width: element.scrollWidth,
        height: element.scrollHeight,
        style: {
          transform: 'scale(1)',
          // Hide elements with 'no-print' class during export
          '.no-print': 'display: none !important;'
        },
        // Quality settings
        cacheBust: true,
        copyStyles: true
      });

      // 2. Map to PDF
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      
      // Create a temporary Image to get dimensions
      const img = new Image();
      img.src = imgData;
      
      await new Promise((resolve) => {
        img.onload = resolve;
      });

      const imgWidth = img.width;
      const imgHeight = img.height;
      const ratio = pdfWidth / imgWidth;
      const contentHeight = imgHeight * ratio;
      
      let heightLeft = contentHeight;
      let position = 0;

      // Add first page
      pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, contentHeight, undefined, 'FAST');
      heightLeft -= pdfHeight;

      // Add more pages if content is taller than A4
      while (heightLeft > 0) {
        position = heightLeft - contentHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, contentHeight, undefined, 'FAST');
        heightLeft -= pdfHeight;
      }

      pdf.save(`Intelligence-Audit-${username}.pdf`);
    } catch (error) {
      console.error("PDF Export failed:", error);
      alert("PDF Generation failed: " + (error.message || "Unknown error") + ". Please use Ctrl+P (Print to PDF) as fallback.");
    } finally {
      setIsExporting(false);
    }
  };

  if (!report) return null;

  // 1. Extract JSON Strategy Block
  let strategy = null;
  const jsonMatch = report.match(/```json\n([\s\S]*?)\n```/);
  if (jsonMatch) {
    try {
      strategy = JSON.parse(jsonMatch[1]);
    } catch (e) {
      console.error("Failed to parse strategy JSON", e);
    }
  }

  // 2. Enhanced Robust Parser for Modules
  // We look for [MODULE_START: Name] or fallback to legacy numbering
  let rawSections = [];
  const delimiterRegex = /\[MODULE_START:\s*(.*?)\]/g;
  const sections = report.split(/\[MODULE_START:\s*.*?\]/);
  
  // Extract module names from the delimiters
  const foundNames = [...report.matchAll(delimiterRegex)].map(m => m[1]);
  
  if (foundNames.length > 0) {
    // Delimiter mode
    rawSections = sections.slice(1).map((content, i) => ({
      name: foundNames[i],
      content: content.trim()
    }));
  } else {
    // Legacy fallback split
    const splitData = report.split(/\n\d+\.\s+[A-Z\s]+|###\s+/).filter(s => s.trim().length > 10);
    const legacyNames = [
      "Performance Intelligence", "Hook & Content Analysis", "Trend Intelligence", 
      "Audience Intelligence", "Competitor Benchmarking", "Conversion & CTA",
      "Posting Optimization", "Virality Prediction", "Actionable Strategy", "Final Verdict"
    ];
    rawSections = splitData.map((content, i) => ({
      name: legacyNames[i] || `Module ${i+1}`,
      content: content.trim()
    }));
  }

  const getIcon = (name) => {
    const n = name.toLowerCase();
    if (n.includes('performance')) return <BarChart3 className="w-5 h-5" />;
    if (n.includes('hook')) return <Zap className="w-5 h-5" />;
    if (n.includes('trend')) return <TrendingUp className="w-5 h-5" />;
    if (n.includes('audience')) return <Users className="w-5 h-5" />;
    if (n.includes('competitor')) return <Search className="w-5 h-5" />;
    if (n.includes('conversion') || n.includes('cta')) return <Instagram className="w-5 h-5" />;
    if (n.includes('optimization') || n.includes('posting')) return <CheckCircle2 className="w-5 h-5" />;
    if (n.includes('virality')) return <Zap className="w-5 h-5" />;
    if (n.includes('strategy')) return <FileText className="w-5 h-5" />;
    return <Sparkles className="w-5 h-5" />;
  };

  return (
    <div ref={reportRef} className="mt-16 space-y-16 animate-in fade-in slide-in-from-bottom-10 duration-1000 p-8 pt-1">
      
      {/* ── Hero Presentation Case ── */}
      <div className="bg-slate-900 rounded-[3.5rem] p-12 lg:p-16 text-white shadow-[0_40px_100px_-20px_rgba(15,23,42,0.3)] relative overflow-hidden border border-white/5 group">
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-purple-600/20 blur-[120px] rounded-full animate-pulse" />
        <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-pink-600/10 blur-[120px] rounded-full" />
        
        <div className="relative z-10 flex flex-col lg:flex-row justify-between items-center gap-12">
          <div className="text-center lg:text-left">
            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 px-5 py-2 rounded-full text-[10px] font-black uppercase tracking-[0.3em] mb-8 text-purple-300">
              Marketing Intelligence Suite 4.0
            </div>
            <h2 className="text-6xl xl:text-7xl font-black tracking-tighter mb-6 leading-none">
              Strategic Audit<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-amber-300 animate-gradient-x">@{username}</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-lg leading-relaxed font-medium">
              We've processed <span className="text-white">real-time behavioral data</span> through our 10-module proprietary engine to map your growth trajectory.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="glass-dark rounded-[2.5rem] p-8 text-center min-w-[180px] hover:scale-105 transition-transform">
              <p className="text-[10px] uppercase font-black tracking-[0.2em] text-slate-500 mb-2">Agency Confidence</p>
              <div className="text-5xl font-black tracking-tighter text-white">98<span className="text-xl opacity-20">%</span></div>
            </div>
            <div className="bg-gradient-to-br from-indigo-600 via-purple-700 to-pink-600 rounded-[2.5rem] p-8 text-center min-w-[180px] shadow-2xl shadow-purple-900/50 hover:scale-105 transition-transform border border-white/10">
              <p className="text-[10px] uppercase font-black tracking-[0.2em] text-purple-200 mb-2">Velocity Score</p>
              <div className="text-5xl font-black text-white">A<span className="text-xl opacity-40">+</span></div>
            </div>
          </div>
        </div>
      </div>

      {/* ── 10 Module Intelligence Engine ── */}
      <div>
        <div className="flex items-center justify-between mb-10">
          <div>
            <h3 className="text-3xl font-black text-slate-900 tracking-tight">Intelligence Modules</h3>
            <p className="text-slate-500 font-medium">Core pillars of your performance audit</p>
          </div>
          <div className="hidden lg:flex gap-2">
            {[1,2,3,4,5].map(i => <div key={i} className="w-1.5 h-1.5 rounded-full bg-slate-200" />)}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
          {rawSections.map((section, idx) => {
            const { name, content } = section;
            
            // Try to extract a score if present like (Score: 85)
            const scoreMatch = content.match(/Score:?\s*(\d+)/i);
            const score = scoreMatch ? parseInt(scoreMatch[1]) : null;

            return (
              <div 
                key={idx} 
                className="bg-white rounded-[2.5rem] p-10 shadow-sm border border-slate-100 hover:shadow-2xl hover:border-purple-200 transition-all duration-500 group flex flex-col h-full fade-in-up"
                style={{ animationDelay: `${idx * 150}ms` }}
              >
                <div className="flex items-start justify-between mb-8">
                  <div className="p-4 bg-slate-50 rounded-2xl text-slate-900 group-hover:bg-slate-900 group-hover:text-white transition-all duration-300 transform group-hover:rotate-6">
                    {getIcon(name)}
                  </div>
                  <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest border border-slate-100 px-3 py-1 rounded-full">MDL-{idx + 1}</span>
                </div>

                <h3 className="text-xl font-black text-slate-900 mb-6 tracking-tight uppercase group-hover:text-purple-600 transition-colors">{name}</h3>
                
                {score !== null && (
                  <div className="mb-6 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-[10px] font-black uppercase text-slate-400">Section Score</span>
                      <span className="text-xs font-black text-slate-900">{score}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-1000 delay-500" style={{ width: `${score}%` }} />
                    </div>
                  </div>
                )}

                <div className="text-slate-600 text-sm leading-relaxed space-y-4 flex-grow">
                  {(() => {
                    const cleaned = content.replace(/```json[\s\S]*?```/g, '').trim();
                    if (!cleaned && name.toLowerCase().includes('strategy')) {
                      return <p className="italic text-slate-400">Interactive execution Roadmap generated below. View the "Execution Roadmap" section for your detailed 7-day plan.</p>
                    }
                    if (!cleaned) {
                      return <p className="italic text-slate-400">Insight gathering in progress... View related modules for parallel data points.</p>
                    }
                    
                    return cleaned.split('\n').map((line, i) => {
                      let t = line.trim();
                      if (!t || t.toLowerCase().includes("score:")) return null;

                      // Inline bold parser for **text**
                      const parts = t.split(/(\*\*.*?\*\*)/g);
                      const renderLine = (p) => p.map((part, pi) => {
                        if (part.startsWith('**') && part.endsWith('**')) {
                          return <strong key={pi} className="text-slate-900 font-black">{part.slice(2, -2)}</strong>;
                        }
                        return part;
                      });

                      if (t.startsWith('-') || t.startsWith('*') || t.startsWith('•')) {
                         return <div key={i} className="flex gap-3 items-start text-slate-700 font-medium">
                            <div className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-2 shrink-0 shadow-lg shadow-purple-500/40" />
                            <span>{renderLine(parts)}</span>
                         </div>
                      }
                      return <p key={i}>{renderLine(parts)}</p>
                    });
                  })()}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* ── Visualized Strategy Dashboard ── */}
      {strategy && (
        <div className="bg-slate-50 rounded-[4rem] p-4 lg:p-8">
          <div className="bg-white rounded-[3.5rem] p-12 lg:p-20 shadow-[0_50px_100px_-20px_rgba(0,0,0,0.05)] border border-slate-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-16 text-slate-100 pointer-events-none -mr-10 -mt-10">
              <Sparkles className="w-64 h-64" />
            </div>
            
            <div className="relative z-10">
              <div className="text-center mb-16">
                <span className="text-purple-600 font-black text-[10px] uppercase tracking-[0.4em]">Proprietary Growth Map</span>
                <h3 className="text-5xl font-black text-slate-900 mt-2 tracking-tighter">Execution Roadmap</h3>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* Weekly Timeline */}
                <div className="lg:col-span-7 bg-slate-50 rounded-[3rem] p-10 border border-slate-100">
                  <h4 className="font-black text-xs uppercase tracking-[0.2em] text-slate-400 mb-10 flex items-center gap-3">
                    <div className="w-10 h-[1px] bg-slate-300" /> 7-Day Performance Cycle
                  </h4>
                  <div className="space-y-8">
                    {strategy.weekly_plan?.map((item, i) => {
                      const [title, ...descParts] = item.split(' - ');
                      const description = descParts.join(' - ');
                      return (
                        <div key={i} className="flex gap-6 items-start group">
                          <div className="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center text-sm font-black text-slate-900 group-hover:bg-slate-900 group-hover:text-white group-hover:scale-110 transition-all duration-300 border border-slate-100 shrink-0 mt-1">0{i+1}</div>
                          <div className="flex-grow pb-6 border-b border-slate-200/60">
                             <p className="text-slate-800 text-base font-bold group-hover:text-purple-600 transition-colors uppercase tracking-tight mb-2">{title}</p>
                             {description && (
                               <p className="text-slate-500 text-sm font-medium leading-relaxed italic border-l-2 border-slate-200 pl-4">
                                 {description}
                               </p>
                             )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Ideas & Captions */}
                <div className="lg:col-span-5 space-y-8">
                  <div className="bg-slate-900 rounded-[3rem] p-10 text-white shadow-2xl relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                      <Zap className="w-16 h-16" />
                    </div>
                    <h4 className="font-black text-xs uppercase tracking-[0.2em] text-pink-400 mb-8">Viral Concepts</h4>
                    <div className="space-y-5">
                      {strategy.content_ideas?.map((idea, i) => (
                        <div key={i} className="text-base font-bold flex gap-4 items-start leading-tight">
                          <span className="text-pink-500 shrink-0">⚡</span> 
                          <span>{idea}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-[3rem] p-10 shadow-xl border border-slate-100 h-full">
                    <h4 className="font-black text-xs uppercase tracking-[0.2em] text-indigo-600 mb-8">Caption Frameworks</h4>
                    <div className="space-y-4">
                      {strategy.caption_strategy?.map((s, i) => {
                        const [label, ...valParts] = s.split(': ');
                        const value = valParts.join(': ');
                        return (
                          <div key={i} className="flex flex-col gap-1 bg-slate-50 p-4 rounded-2xl border border-slate-100 hover:border-indigo-200 transition-all">
                             <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">{label}</span>
                             <span className="text-sm font-bold text-slate-800">{value || label}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              {/* Strategy Footer */}
                <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-8 bg-slate-900 rounded-[2.5rem] p-12 text-white shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-purple-600/10 blur-[80px] rounded-full" />
                  
                  <div className="relative z-10">
                    <p className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 mb-4">Optimized Cluster</p>
                    <div className="flex flex-wrap gap-3">
                      {strategy.hashtags?.map((t, i) => (
                        <span key={i} className="text-purple-400 text-xs font-black font-mono tracking-widest bg-white/5 px-3 py-1 rounded-lg border border-purple-500/10 hover:border-purple-500/30 transition-colors">#{t.replace('#', '')}</span>
                      ))}
                    </div>
                  </div>

                  <div className="relative z-10 lg:text-right flex flex-col justify-center border-t lg:border-t-0 lg:border-l border-white/10 pt-8 lg:pt-0 lg:pl-12">
                    <p className="text-[10px] font-black uppercase tracking-[0.3em] text-pink-500 mb-2">Prime Posting Frequency</p>
                    <p className="text-3xl font-black tracking-tighter mb-4">
                      {strategy.posting_schedule?.best_time} <span className="text-slate-600 text-sm mx-2">on</span> {strategy.posting_schedule?.best_days?.join(', ')}
                    </p>
                    {strategy.posting_schedule?.frequency_insight && (
                      <p className="text-slate-400 text-xs font-medium leading-relaxed italic max-w-sm lg:ml-auto">
                        "{strategy.posting_schedule.frequency_insight}"
                      </p>
                    )}
                  </div>
                </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Master CTA ── */}
      <div className="flex flex-col items-center gap-6 pb-20 mt-16 no-print">
        <button 
          onClick={exportPDF} 
          disabled={isExporting}
          className="group relative bg-slate-900 text-white px-16 py-6 rounded-3xl font-black text-base transition-all hover:scale-105 active:scale-95 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.3)] flex items-center gap-4 overflow-hidden disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <div className="relative flex items-center gap-4">
            {isExporting ? (
              <Loader2 className="w-6 h-6 animate-spin" />
            ) : (
              <Download className="w-6 h-6 animate-bounce" /> 
            )}
            <span>{isExporting ? 'Generating Intelligence PDF...' : 'Export Enterprise Audit PDF'}</span>
          </div>
        </button>
        <p className="text-slate-400 text-xs font-bold uppercase tracking-[0.2em]">Ready for Client Presentation</p>
      </div>
    </div>
  );
};

export default ReportViewer;
