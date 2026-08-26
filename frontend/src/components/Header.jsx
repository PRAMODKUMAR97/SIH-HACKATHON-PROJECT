import React from 'react';
import { Download, FileText, Calendar, Database, Sparkles } from 'lucide-react';

const Header = ({ title, subtitle }) => {
  const handleExportKML = () => {
    window.open('/api/export/kml', '_blank');
  };

  const handleExportGPX = () => {
    window.open('/api/export/gpx', '_blank');
  };

  const handleGenerateReport = () => {
    window.open('/api/report', '_blank');
  };

  return (
    <header className="h-20 bg-[#111827]/80 backdrop-blur-md border-b border-[#1e293b] px-8 flex items-center justify-between sticky top-0 z-20">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold text-gray-100 tracking-tight">
            {title || 'KHANAN-NETRA Command Center'}
          </h1>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
            <Database className="w-3.5 h-3.5" />
            DEMO DATA
          </span>
        </div>
        <p className="text-xs text-gray-400 mt-0.5 flex items-center gap-2">
          <span>{subtitle || 'AI-Powered Satellite Mining Intelligence & Surveillance'}</span>
          <span className="text-gray-600">•</span>
          <span className="flex items-center gap-1 font-mono text-cyan-400">
            <Calendar className="w-3 h-3" /> Period: 2026-08-01 — Present
          </span>
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-3">
        <button
          onClick={handleExportKML}
          className="flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold bg-[#1e293b] text-gray-200 hover:text-white hover:bg-gray-700 border border-gray-700 transition-all duration-150 active:scale-95 shadow-sm"
          title="Export detection placemarks and permit boundaries in KML format"
        >
          <Download className="w-4 h-4 text-cyan-400" />
          Export KML
        </button>

        <button
          onClick={handleExportGPX}
          className="flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold bg-[#1e293b] text-gray-200 hover:text-white hover:bg-gray-700 border border-gray-700 transition-all duration-150 active:scale-95 shadow-sm"
          title="Export truck GPS waypoints in GPX format"
        >
          <Download className="w-4 h-4 text-teal-400" />
          Export GPX
        </button>

        <button
          onClick={handleGenerateReport}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold bg-gradient-to-r from-cyan-500 to-teal-500 text-black hover:brightness-110 transition-all duration-150 active:scale-95 shadow-lg shadow-cyan-500/20 font-medium"
        >
          <FileText className="w-4 h-4 text-black" />
          Generate Report
        </button>
      </div>
    </header>
  );
};

export default Header;
