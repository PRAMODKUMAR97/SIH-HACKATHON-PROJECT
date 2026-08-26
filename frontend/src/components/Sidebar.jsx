import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Eye, 
  TrendingUp, 
  AlertTriangle, 
  FileText, 
  Plane, 
  Truck, 
  ShieldAlert,
  Activity
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Detections', path: '/detections', icon: Eye },
    { name: 'Historical Trends', path: '/historical-trends', icon: TrendingUp },
    { name: 'Alerts', path: '/alerts', icon: AlertTriangle, badge: '4' },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'Drone Verification', path: '/drone-verification', icon: Plane, tag: 'SOON' },
    { name: 'Truck Intelligence', path: '/truck-intelligence', icon: Truck },
  ];

  return (
    <aside className="w-64 bg-[#0b0f19] border-r border-[#1e293b] flex flex-col justify-between h-screen sticky top-0 z-30 select-none">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-5 border-b border-[#1e293b] bg-[#111827]/60">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <ShieldAlert className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400">
              KHANAN-NETRA
            </h1>
            <p className="text-[10px] text-gray-400 font-mono tracking-widest uppercase">Mining Intelligence</p>
          </div>
        </div>

        {/* Navigation Section */}
        <div className="px-3 py-6">
          <div className="px-3 mb-2 text-[11px] font-mono text-gray-400 tracking-wider uppercase">
            Core Modules
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-cyan-500/20 to-teal-500/10 text-cyan-400 border-l-4 border-cyan-400 shadow-sm'
                        : 'text-gray-400 hover:text-gray-200 hover:bg-[#111827]'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-5 h-5 shrink-0" />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span className="px-2 py-0.5 text-xs font-bold rounded-full bg-red-500/20 text-red-400 border border-red-500/30">
                      {item.badge}
                    </span>
                  )}
                  {item.tag && (
                    <span className="px-1.5 py-0.5 text-[10px] font-mono rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                      {item.tag}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* System Status Footer */}
      <div className="p-4 m-3 rounded-xl bg-[#111827] border border-[#1e293b]">
        <div className="flex items-center gap-2 mb-2">
          <Activity className="w-4 h-4 text-emerald-400 animate-spin" style={{ animationDuration: '4s' }} />
          <span className="text-xs font-semibold text-gray-200">System Status</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-mono text-emerald-400 font-medium">AI Monitoring Active</span>
        </div>
        <div className="mt-2 pt-2 border-t border-gray-800 text-[10px] text-gray-400 font-mono flex justify-between">
          <span>Engine v1.0</span>
          <span>FastAPI Online</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
