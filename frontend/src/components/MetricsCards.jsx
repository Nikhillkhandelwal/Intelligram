import React from 'react';
import { Users, Heart, MessageCircle, BarChart3, Sparkles } from 'lucide-react';

const MetricsCards = ({ metrics }) => {
  if (!metrics) return null;
  const cards = [
    { label: 'Followers', value: (metrics.followers || 0).toLocaleString(), icon: Users, color: 'from-emerald-500 to-teal-600', shadow: 'shadow-emerald-500/20' },
    { label: 'Avg Likes', value: Math.round(metrics.avg_likes).toLocaleString(), icon: Heart, color: 'from-pink-500 to-rose-600', shadow: 'shadow-pink-500/20' },
    { label: 'Avg Comments', value: Math.round(metrics.avg_comments).toLocaleString(), icon: MessageCircle, color: 'from-blue-500 to-cyan-600', shadow: 'shadow-blue-500/20' },
    { label: 'Engagement Rate', value: `${((metrics.avg_engagement_rate || 0) * 1).toFixed(2)}%`, icon: BarChart3, color: 'from-purple-500 to-indigo-600', shadow: 'shadow-purple-500/20' },
    { label: 'Reach Health', value: `${(metrics.active_follower_rate || 0).toFixed(1)}%`, sub: metrics.reach_status || 'Healthy', icon: BarChart3, color: 'from-orange-500 to-red-600', shadow: 'shadow-orange-500/20' },
    { label: 'Content Score', value: `${metrics.content_score || 0}`, sub: '/100', icon: Sparkles, color: 'from-amber-400 to-orange-500', shadow: 'shadow-amber-500/20' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      {cards.map((card, i) => (
        <div key={i} className={`relative group overflow-hidden bg-white rounded-[2rem] p-8 shadow-sm border border-slate-100 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2`}>
          <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${card.color} opacity-0 group-hover:opacity-5 -mr-16 -mt-16 rounded-full blur-3xl transition-opacity animate-pulse`} />
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-2xl bg-gradient-to-br ${card.color} text-white shadow-lg ${card.shadow} transform group-hover:rotate-12 transition-transform`}>
              <card.icon className="w-6 h-6" />
            </div>
            {card.sub && (
              <span className="text-[10px] font-black text-slate-300 uppercase tracking-widest">Premium Score</span>
            )}
          </div>
          <div>
            <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1">{card.label}</p>
            <div className="flex items-baseline gap-1">
              <span className="text-4xl font-black text-slate-900 tracking-tighter tabular-nums">{card.value}</span>
              {card.sub && <span className="text-sm font-bold text-slate-300">{card.sub}</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MetricsCards;
