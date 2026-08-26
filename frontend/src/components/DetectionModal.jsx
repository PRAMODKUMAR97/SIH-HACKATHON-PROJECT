import React from 'react';
import { X, ShieldAlert, MapPin, Database, Layers, Truck, FileText } from 'lucide-react';

const DetectionModal = ({ detection, riskData, onClose }) => {
  if (!detection) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn select-none">
      <div className="relative w-full max-w-2xl bg-[#111827] border border-[#1e293b] rounded-2xl shadow-2xl overflow-hidden text-gray-200">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#1e293b] bg-[#0b0f19]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white font-mono">Site Detection Details: {detection.detection_id}</h2>
              <p className="text-xs text-gray-400">Recorded Date: {detection.detection_date || '2026-08-25'}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
          {/* Top Status Badges */}
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-[#0b0f19] border border-gray-800">
              <span className="text-[10px] text-gray-400 font-mono block">LEGAL STATUS</span>
              <span className="text-xs font-bold text-cyan-400 font-mono">{detection.legal_status}</span>
            </div>
            <div className="p-3 rounded-xl bg-[#0b0f19] border border-gray-800">
              <span className="text-[10px] text-gray-400 font-mono block">MINING PROBABILITY</span>
              <span className="text-xs font-bold text-emerald-400 font-mono">
                {Math.round((detection.mining_probability || 0) * 100)}% ({detection.confidence_level})
              </span>
            </div>
            <div className="p-3 rounded-xl bg-[#0b0f19] border border-gray-800">
              <span className="text-[10px] text-gray-400 font-mono block">EXPLAINABLE RISK SCORE</span>
              <span className="text-xs font-bold text-red-400 font-mono">
                {riskData?.risk_score || 0} / 100 ({riskData?.risk_level || 'EVALUATING'})
              </span>
            </div>
          </div>

          {/* Coordinates & Area Details */}
          <div className="p-4 rounded-xl bg-[#0b0f19] border border-gray-800 space-y-2">
            <h4 className="text-xs font-bold text-gray-300 font-mono uppercase flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-cyan-400" /> Geographic & Volume Specs
            </h4>
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>Latitude: <strong className="text-white font-mono">{detection.latitude}</strong></div>
              <div>Longitude: <strong className="text-white font-mono">{detection.longitude}</strong></div>
              <div>Detected Area: <strong className="text-white font-mono">{detection.area_ha} hectares</strong></div>
              <div>Est Excavation Volume: <strong className="text-white font-mono">{detection.estimated_volume_m3?.toLocaleString()} m³</strong></div>
              <div>Assigned Permit: <strong className="text-cyan-400 font-mono">{detection.permit_id || 'None (Outside Boundary)'}</strong></div>
              <div>Protected Zone Overlap: <strong className={detection.is_protected_area ? 'text-red-400' : 'text-emerald-400'}>{detection.is_protected_area ? 'YES (Illegal Overlap)' : 'NO'}</strong></div>
            </div>
          </div>

          {/* Spectral Remote Sensing Indicators */}
          <div className="p-4 rounded-xl bg-[#0b0f19] border border-gray-800 space-y-2">
            <h4 className="text-xs font-bold text-gray-300 font-mono uppercase flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-teal-400" /> Remote Sensing Feature Vectors
            </h4>
            <div className="grid grid-cols-2 gap-4 text-xs font-mono">
              <div>NDVI Change: <span className="text-gray-200">{detection.ndvi_change}</span></div>
              <div>SAR VV/VH Ratio: <span className="text-gray-200">{detection.sar_vv_vh_ratio}</span></div>
              <div>Texture Variance: <span className="text-gray-200">{detection.texture_variance}</span></div>
              <div>Spectral Anomaly: <span className="text-gray-200">{detection.spectral_anomaly_score}</span></div>
            </div>
          </div>

          {/* Risk Reasons List */}
          {riskData?.reasons && (
            <div className="p-4 rounded-xl bg-red-950/20 border border-red-500/30 space-y-2">
              <h4 className="text-xs font-bold text-red-400 font-mono uppercase">Risk Evidence Explanations</h4>
              <ul className="text-xs text-gray-300 space-y-1 list-disc list-inside">
                {riskData.reasons.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-[#1e293b] bg-[#0b0f19]">
          <span className="text-[11px] text-gray-500 font-mono">DEMO DATA MODE</span>
          <button
            onClick={onClose}
            className="px-5 py-2 text-xs font-semibold bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition"
          >
            Close Details
          </button>
        </div>
      </div>
    </div>
  );
};

export default DetectionModal;
