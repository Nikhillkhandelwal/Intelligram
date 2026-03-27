import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, LineChart, Line
} from 'recharts';

const Charts = ({ posts = [] }) => {
  const safePosts = posts || [];
  const typeData = [
    { name: 'Images', value: safePosts.filter(p => p.type === 'image' || p.type === 'GraphImage').length },
    { name: 'Videos/Reels', value: safePosts.filter(p => p.type === 'video' || p.type === 'GraphVideo').length },
    { name: 'Carousels', value: safePosts.filter(p => p.type === 'carousel' || p.type === 'GraphSidecar').length },
  ];

  const engagementTrend = [...safePosts]
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .map(p => ({
      date: p.date.split('-').slice(1).join('/'),
      engagement: (Number(p.likes) || 0) + (Number(p.comments) || 0)
    }));

  const COLORS = ['#833AB4', '#E1306C', '#F56040'];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12">
      <div className="card h-[400px]">
        <h3 className="text-lg font-bold mb-4">Content Type Breakdown</h3>
        <ResponsiveContainer width="100%" height="85%">
          <PieChart>
            <Pie
              data={typeData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {typeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="card h-[400px]">
        <h3 className="text-lg font-bold mb-4">Engagement Trend (Last {posts.length} Posts)</h3>
        <ResponsiveContainer width="100%" height="85%">
          <LineChart data={engagementTrend}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="engagement" stroke="#833AB4" strokeWidth={3} dot={{ fill: '#833AB4' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;
