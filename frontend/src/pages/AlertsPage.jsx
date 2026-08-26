import React, { useEffect, useState } from 'react';
import axios from 'axios';
import DetectionModal from '../components/DetectionModal';
import { AlertTriangle, ShieldAlert, CheckCircle, ChevronRight, Info } from 'lucide-react';

const AlertsPage = () => {
  const [riskAssessments, setRiskAssessments] = useState([]);
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [selectedRiskData, setSelectedRiskData] = useState(null);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get('/api/risk');
      setRiskAssessments(res.data || []);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    }
  };

  const handleOpenDetails = async (riskItem) => {
    try {
      const detRes = await axios.get(`/api/detections/${riskItem.detection_id}`);
      setSelectedDetection(detRes.data);
      setSelectedRiskData(riskItem);
    } catch (err) {
      console.error(`Error loading detection ${riskItem.detection_id}:`, err);
    }
  };

  const getSeverityStyle = (level) => {
    switch (level) {
      case 'CRITICAL':
        return { text: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30' };
      case 'HIGH':
        return { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/30' };
      case 'MEDIUM':
        return { text: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30' };
      default:
        return { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30' };
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400">
            <AlertTriangle className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white font-mono">Surveillance Alert Center</h2>
            <p className="text-xs text-gray-400">Categorized risk warnings requiring desk review or priority field inspection.</p>
          </div>
        </div>
        <span className="px-3 py-1 text-xs font-mono font-bold rounded-full bg-red-500/20 text-red-400 border border-red-500/30">
          {riskAssessments.length} Active System Alerts
        </span>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {riskAssessments.map((item) => {
          const style = getSeverityStyle(item.risk_level);
          return (
            <div
              key={item.risk_id}
              className={`p-5 rounded-xl bg-[#111827] border ${style.border} transition hover:bg-[#161f33] shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4`}
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-black border ${style.bg} ${style.text} ${style.border}`}>
                    {item.risk_level} SEVERITY
                  </span>
                  <span className="text-sm font-bold text-white font-mono">
                    Detection Site {item.detection_id}
                  </span>
                  <span className="text-xs font-mono text-gray-400">
                    Risk Score: <strong className={style.text}>{item.risk_score} / 100</strong>
                  </span>
                </div>

                {/* Evidence Reasons Bullet List */}
                <ul className="space-y-1 text-xs text-gray-300">
                  {item.reasons.map((r, idx) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Action Button */}
              <div className="shrink-0">
                <button
                  onClick={() => handleOpenDetails(item)}
                  className="px-4 py-2 text-xs font-semibold rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/20 transition active:scale-95"
                >
                  Inspect Site Evidence
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detection Detail Modal */}
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

export default AlertsPage;
