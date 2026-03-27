import React from 'react';

const ContentTable = ({ posts }) => {
  return (
    <div className="card mt-12 overflow-hidden">
      <h3 className="text-lg font-bold mb-4">Detailed Content Audit</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 text-slate-500 text-sm uppercase font-bold tracking-wider">
              <th className="px-6 py-4">Type</th>
              <th className="px-6 py-4">Likes</th>
              <th className="px-6 py-4">Comments</th>
              <th className="px-6 py-4">Date/Time</th>
              <th className="px-6 py-4">Has Question?</th>
              <th className="px-6 py-4">Has CTA?</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {(posts || []).map((post, i) => (
              <tr key={i} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-md text-xs font-bold uppercase ${
                    post.type === 'video' ? 'bg-purple-100 text-purple-700' :
                    post.type === 'carousel' ? 'bg-blue-100 text-blue-700' :
                    'bg-slate-100 text-slate-700'
                  }`}>
                    {post.type}
                  </span>
                </td>
                <td className="px-6 py-4 font-semibold">{post.likes.toLocaleString()}</td>
                <td className="px-6 py-4 text-slate-600">{post.comments.toLocaleString()}</td>
                <td className="px-6 py-4 text-slate-500 text-sm">
                  {post.date} @ {post.hour}:00
                </td>
                <td className="px-6 py-4 text-center">
                  {post.has_question ? '✅' : '❌'}
                </td>
                <td className="px-6 py-4 text-center">
                  {post.has_cta ? '✅' : '❌'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ContentTable;
