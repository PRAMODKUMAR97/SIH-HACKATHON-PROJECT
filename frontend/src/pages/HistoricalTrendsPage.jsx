import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';
import { TrendingUp, Calendar, Layers, Activity } from 'lucide-react';

const HistoricalTrendsPage = () => {
  const [timeRange, setTimeRange] = useState('6M');

  // Realistic historical trend dataset for target mining regions
  const trendData = [
    { period: 'Jan 2026', legalArea: 1.1, suspiciousArea: 0.2, volume: 15400, riskScore: 22 },
    { period: 'Feb 2026', legalArea: 1.3, suspiciousArea: 0.5, volume: 22000, riskScore: 35 },
    { period: 'Mar 2026', legalArea: 1.5, suspiciousArea: 0.9, volume: 38500, riskScore: 48 },
    { period: 'Apr 2026', legalArea: 1.8, suspiciousArea: 1.4, volume: 54000, riskScore: 65 },
    { period: 'May 2026', legalArea: 2.1, suspiciousArea: 2.3, volume: 72000, riskScore: 78 },
    { period: 'Jun 2026', legalArea: 2.4, suspiciousArea: 3.1, volume: 89000, riskScore: 84 },
    { period: 'Jul 2026', legalArea: 2.8, suspiciousArea: 4.2, volume: 100800, riskScore: 92 },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-xl bg-[#111827] border border-[#1e293b]">
        <div>
          <h2 className="text-base font-bold text-white font-mono flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-cyan-400" /> Historical Mining Activity Trends
          </h2>
          <p className="text-xs text-gray-400">Temporal change analysis of excavation area, volume overruns, and risk trends.</p>
        </div>

        {/* Time Filter Buttons */}
        <div className="flex items-center gap-1.5 p-1 rounded-lg bg-[#0b0f19] border border-gray-800 font-mono text-xs">
          {['7D', '30D', '6M', '1Y'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-3 py-1.5 rounded-md font-semibold transition ${
                timeRange === range
                  ? 'bg-cyan-500 text-black shadow-md'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Mining Area Growth (Legal vs Suspicious) */}
        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
            <h3 className="text-xs font-bold text-gray-200 font-mono uppercase tracking-wider">
              Mining Area Expansion (Hectares)
            </h3>
            <span className="text-[10px] text-cyan-400 font-mono">Area Trend (ha)</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorLegal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorSuspicious" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="period" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0b0f19', borderColor: '#1e293b', borderRadius: '8px', fontSize: '12px' }} />
                <Legend />
                <Area type="monotone" dataKey="legalArea" name="Legal Lease Area" stroke="#10b981" fillOpacity={1} fill="url(#colorLegal)" />
                <Area type="monotone" dataKey="suspiciousArea" name="Suspicious Area" stroke="#ef4444" fillOpacity={1} fill="url(#colorSuspicious)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Cumulative Excavation Volume Growth */}
        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
            <h3 className="text-xs font-bold text-gray-200 font-mono uppercase tracking-wider">
              Excavation Volume Trajectory (m³)
            </h3>
            <span className="text-[10px] text-amber-400 font-mono">Volume (m³)</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="period" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0b0f19', borderColor: '#1e293b', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="volume" name="Excavated Volume (m³)" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoricalTrendsPage;
