import React, { useState } from 'react';
import { Search, Plus, X } from 'lucide-react';

const InputForm = ({ onAnalyze, loading }) => {
  const [username, setUsername] = useState('');
  const [competitors, setCompetitors] = useState(['']);

  const addCompetitor = () => setCompetitors([...competitors, '']);
  const removeCompetitor = (index) => {
    const newCompetitors = competitors.filter((_, i) => i !== index);
    setCompetitors(newCompetitors);
  };

  const updateCompetitor = (index, value) => {
    const newCompetitors = [...competitors];
    newCompetitors[index] = value;
    setCompetitors(newCompetitors);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze({ username, competitors: competitors.filter(c => c.trim() !== '') });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-10">
      <div className="space-y-4">
        <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.3em] block ml-1">Primary Instagram Handle</label>
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 group-focus-within:opacity-5 blur-xl transition-opacity pointer-events-none" />
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="e.g. garyvee"
            className="w-full px-8 py-5 pl-16 rounded-[2rem] border-2 border-slate-100 bg-slate-50/50 focus:bg-white focus:border-purple-500 focus:ring-4 focus:ring-purple-500/10 outline-none transition-all text-lg font-bold tracking-tight text-slate-900"
            required
          />
          <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-300 w-6 h-6 group-focus-within:text-purple-500 transition-colors pointer-events-none" />
        </div>
      </div>

      <div className="space-y-4">
        <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.3em] block ml-1">Competitive Benchmarking (Up to 3)</label>
        <div className="grid grid-cols-1 gap-3">
          {competitors.map((comp, index) => (
            <div key={index} className="flex gap-3 group animate-in slide-in-from-left-4 duration-300">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={comp}
                  onChange={(e) => updateCompetitor(index, e.target.value)}
                  placeholder="Competitor handle"
                  className="w-full px-6 py-3.5 rounded-2xl border-2 border-slate-100 bg-slate-50/50 focus:bg-white focus:border-indigo-500 outline-none transition-all text-sm font-bold text-slate-700"
                />
              </div>
              {competitors.length > 1 && (
                <button 
                  type="button" 
                  onClick={() => removeCompetitor(index)}
                  className="p-3 text-slate-300 hover:text-rose-500 transition-colors bg-slate-50 rounded-2xl hover:bg-rose-50"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>
          ))}
        </div>
        
        {competitors.length < 3 && (
          <button
            type="button"
            onClick={addCompetitor}
            className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-purple-600 transition-colors py-2 px-1"
          >
            <Plus className="w-4 h-4" /> Add Benchmark Target
          </button>
        )}
      </div>

      <div className="pt-8 border-t border-slate-100">
        <button
          type="submit"
          disabled={loading}
          className="w-full relative group overflow-hidden bg-slate-900 text-white rounded-[2rem] py-6 font-black text-sm uppercase tracking-[0.4em] transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 via-pink-600 to-amber-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <span className="relative">Execute intelligence Audit</span>
        </button>
      </div>
    </form>
  );
};

export default InputForm;
