import React, { useEffect, useState } from 'react';
import axios from 'axios';
import DetectionModal from '../components/DetectionModal';
import { Search, Filter, Eye, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';

const DetectionsPage = () => {
  const [detections, setDetections] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [selectedRiskData, setSelectedRiskData] = useState(null);

  useEffect(() => {
    fetchDetections();
  }, []);

  const fetchDetections = async () => {
    try {
      const res = await axios.get('/api/detections');
      setDetections(res.data || []);
    } catch (err) {
      console.error('Error fetching detections:', err);
    }
  };

  const handleOpenDetails = async (det) => {
    setSelectedDetection(det);
    try {
      const riskRes = await axios.get(`/api/risk/${det.detection_id}`);
      setSelectedRiskData(riskRes.data);
    } catch (err) {
      console.error(`Error fetching risk for ${det.detection_id}:`, err);
    }
  };

  const filteredDetections = detections.filter(d => {
    const matchesSearch = d.detection_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (d.permit_id && d.permit_id.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'ALL' || d.legal_status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case 'LEGAL_WITHIN_PERMIT':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">LEGAL LEASE</span>;
      case 'SUSPICIOUS_OUTSIDE_PERMIT':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">SUSPICIOUS OUTSIDE LEASE</span>;
      case 'ILLEGAL_PROTECTED_AREA':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30">ILLEGAL PROTECTED ZONE</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-500/10 text-gray-400 border border-gray-500/30">{status}</span>;
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Search & Filter Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl bg-[#111827] border border-[#1e293b]">
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search by Detection ID or Permit ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 text-xs rounded-lg bg-[#0b0f19] border border-gray-800 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-3">
          <Filter className="w-4 h-4 text-gray-400" />
          <span className="text-xs text-gray-400 font-mono">Status:</span>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 text-xs rounded-lg bg-[#0b0f19] border border-gray-800 text-white focus:outline-none focus:border-cyan-500 font-mono"
          >
            <option value="ALL">All Statuses</option>
            <option value="LEGAL_WITHIN_PERMIT">Legal Within Permit</option>
            <option value="SUSPICIOUS_OUTSIDE_PERMIT">Suspicious Outside Permit</option>
            <option value="ILLEGAL_PROTECTED_AREA">Illegal Protected Area</option>
          </select>
        </div>
      </div>

      {/* Detections Data Table */}
      <div className="rounded-xl bg-[#111827] border border-[#1e293b] overflow-hidden shadow-xl">
        <div className="px-6 py-4 border-b border-[#1e293b] flex items-center justify-between">
          <h2 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
            Satellite Detection Registry ({filteredDetections.length})
          </h2>
          <span className="text-xs text-gray-400 font-mono">Realtime AI Predictions</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-gray-300">
            <thead className="bg-[#0b0f19] text-gray-400 font-mono uppercase tracking-wider text-[10px] border-b border-[#1e293b]">
              <tr>
                <th className="px-6 py-3.5">Detection ID</th>
                <th className="px-6 py-3.5">Coordinates</th>
                <th className="px-6 py-3.5">Status</th>
                <th className="px-6 py-3.5">Area (ha)</th>
                <th className="px-6 py-3.5">Est Volume (m³)</th>
                <th className="px-6 py-3.5">Mining Prob</th>
                <th className="px-6 py-3.5">Confidence</th>
                <th className="px-6 py-3.5">Date</th>
                <th className="px-6 py-3.5 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60 font-mono">
              {filteredDetections.map((det) => (
                <tr key={det.detection_id} className="hover:bg-[#1f2937]/50 transition-colors">
                  <td className="px-6 py-4 font-bold text-white">{det.detection_id}</td>
                  <td className="px-6 py-4 text-gray-400">{det.latitude}, {det.longitude}</td>
                  <td className="px-6 py-4">{getStatusBadge(det.legal_status)}</td>
                  <td className="px-6 py-4 text-white font-bold">{det.area_ha} ha</td>
                  <td className="px-6 py-4 text-cyan-400 font-bold">{det.estimated_volume_m3?.toLocaleString()} m³</td>
                  <td className="px-6 py-4 text-emerald-400 font-bold">{Math.round((det.mining_probability || 0) * 100)}%</td>
                  <td className="px-6 py-4">{det.confidence_level}</td>
                  <td className="px-6 py-4 text-gray-400">{det.detection_date}</td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => handleOpenDetails(det)}
                      className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/20 transition active:scale-95"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detail Modal */}
      {selectedDetection && (
        <DetectionModal
          detection={selectedDetection}
          riskData={selectedRiskData}
          onClose={() => setSelectedDetection(null)}
        />
      )}
    </div>
  );
};

export default DetectionsPage;
