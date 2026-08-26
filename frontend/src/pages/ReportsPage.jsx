import React, { useState } from 'react';
import axios from 'axios';
import { FileText, Download, CheckCircle, ShieldAlert, Sparkles } from 'lucide-react';

const ReportsPage = () => {
  const [reportJSON, setReportJSON] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummaryReport = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/report');
      setReportJSON(res.data);
    } catch (err) {
      console.error('Error fetching report:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] flex items-center justify-between">
        <div>
          <h2 className="text-base font-bold text-white font-mono flex items-center gap-2">
            <FileText className="w-5 h-5 text-cyan-400" /> Evidence Report Generation Suite
          </h2>
          <p className="text-xs text-gray-400">Generate field inspection packages, GIS KML placemarks, and truck route GPX files.</p>
        </div>

        <button
          onClick={fetchSummaryReport}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold bg-cyan-500 text-black hover:bg-cyan-400 transition shadow-lg shadow-cyan-500/20 active:scale-95 font-mono"
        >
          <Sparkles className="w-4 h-4 text-black" />
          {loading ? 'Generating Report...' : 'Compile Surveillance Summary'}
        </button>
      </div>

      {/* Report Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-3 shadow-md">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 w-fit">
            <FileText className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">Surveillance Summary JSON/PDF</h3>
          <p className="text-xs text-gray-400">Comprehensive report payload listing all high-risk detections, reasons, and recommended field actions.</p>
          <button
            onClick={() => window.open('/api/report', '_blank')}
            className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-cyan-400 text-xs font-semibold rounded-lg border border-gray-700 transition flex items-center justify-center gap-2 font-mono"
          >
            <Download className="w-4 h-4" /> Download Report
          </button>
        </div>

        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-3 shadow-md">
          <div className="p-2.5 rounded-lg bg-teal-500/10 border border-teal-500/30 text-teal-400 w-fit">
            <Download className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">GIS Placemarks (KML)</h3>
          <p className="text-xs text-gray-400">Google Earth and GIS compatible KML placemark dataset for field navigation.</p>
          <button
            onClick={() => window.open('/api/export/kml', '_blank')}
            className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-teal-400 text-xs font-semibold rounded-lg border border-gray-700 transition flex items-center justify-center gap-2 font-mono"
          >
            <Download className="w-4 h-4" /> Export KML
          </button>
        </div>

        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-3 shadow-md">
          <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 w-fit">
            <Download className="w-5 h-5" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">Truck GPS Routes (GPX)</h3>
          <p className="text-xs text-gray-400">GPS route waypoints and RFID checkpoint scan logs in standard GPX format.</p>
          <button
            onClick={() => window.open('/api/export/gpx', '_blank')}
            className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-emerald-400 text-xs font-semibold rounded-lg border border-gray-700 transition flex items-center justify-center gap-2 font-mono"
          >
            <Download className="w-4 h-4" /> Export GPX
          </button>
        </div>
      </div>

      {/* Compiled Report JSON Previewer */}
      {reportJSON && (
        <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] space-y-3 shadow-xl">
          <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
            <span className="text-xs font-bold text-white font-mono uppercase">Compiled Report Payload</span>
            <span className="text-xs text-emerald-400 font-mono flex items-center gap-1">
              <CheckCircle className="w-3.5 h-3.5" /> Generated Successfully
            </span>
          </div>
          <pre className="p-4 rounded-lg bg-[#0b0f19] text-xs font-mono text-cyan-300 overflow-x-auto border border-gray-800 max-h-96">
            {JSON.stringify(reportJSON, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ReportsPage;
