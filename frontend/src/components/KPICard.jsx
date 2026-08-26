import React from 'react';

const KPICard = ({ title, value, subtitle, icon: Icon, color = 'cyan', onClick, trend }) => {
  const colorStyles = {
    cyan: {
      bg: 'bg-cyan-500/10',
      border: 'border-cyan-500/30',
      text: 'text-cyan-400',
      glow: 'group-hover:shadow-cyan-500/10',
    },
    emerald: {
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-500/30',
      text: 'text-emerald-400',
      glow: 'group-hover:shadow-emerald-500/10',
    },
    red: {
      bg: 'bg-red-500/10',
      border: 'border-red-500/30',
      text: 'text-red-400',
      glow: 'group-hover:shadow-red-500/10',
    },
    amber: {
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/30',
      text: 'text-amber-400',
      glow: 'group-hover:shadow-amber-500/10',
    },
  };

  const style = colorStyles[color] || colorStyles.cyan;

  return (
    <div
      onClick={onClick}
      className={`group relative p-5 rounded-xl bg-[#111827] border border-[#1e293b] hover:border-gray-700 transition-all duration-200 cursor-pointer shadow-md ${style.glow} hover:-translate-y-0.5`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-gray-400 tracking-wide uppercase">{title}</span>
        <div className={`p-2.5 rounded-lg ${style.bg} border ${style.border} ${style.text}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3">
        <div className="text-2xl font-extrabold text-white tracking-tight font-mono">{value}</div>
        {subtitle && (
          <div className="mt-1 flex items-center justify-between text-xs text-gray-400">
            <span>{subtitle}</span>
            {trend && <span className="font-mono text-emerald-400">{trend}</span>}
          </div>
        )}
      </div>
    </div>
  );
};

export default KPICard;
