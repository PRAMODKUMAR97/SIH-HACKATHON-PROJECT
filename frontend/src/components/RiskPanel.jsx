import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle, Info, ChevronRight, Layers, ArrowRight } from 'lucide-react';

const RiskPanel = ({ riskData, selectedDetection }) => {
  if (!riskData) {
    return (
      <div className="h-full rounded-xl bg-[#111827] border border-[#1e293b] p-6 flex flex-col items-center justify-center text-center text-gray-400">
        <ShieldAlert className="w-12 h-12 text-gray-600 mb-3 animate-pulse" />
        <h3 className="text-sm font-semibold text-gray-300">No Detection Selected</h3>
        <p className="text-xs text-gray-500 mt-1 max-w-xs">
          Click on any mining detection site on the map or in the table to inspect explainable AI risk evidence.
        </p>
      </div>
    );
  }

  const { risk_score, risk_level, evidence_breakdown = {}, reasons = [], recommended_action } = riskData;

  const getRiskColor = (level) => {
    switch (level) {
      case 'CRITICAL':
        return { text: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', bar: 'bg-red-500' };
      case 'HIGH':
        return { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/30', bar: 'bg-amber-500' };
      case 'MEDIUM':
        return { text: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', bar: 'bg-yellow-500' };
      default:
        return { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', bar: 'bg-emerald-500' };
    }
  };

  const style = getRiskColor(risk_level);

  return (
    <div className="h-full rounded-xl bg-[#111827] border border-[#1e293b] p-5 flex flex-col justify-between overflow-y-auto space-y-4 shadow-xl">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between border-b border-[#1e293b] pb-3">
          <div>
            <span className="text-[10px] font-mono text-cyan-400 tracking-wider uppercase">AI Evidence Fusion</span>
            <h2 className="text-base font-extrabold text-white font-mono">
              Site {selectedDetection?.detection_id || riskData.detection_id}
            </h2>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-black tracking-wide border ${style.bg} ${style.text} ${style.border}`}>
            {risk_level} RISK
          </span>
        </div>

        {/* Risk Score Gauge */}
        <div className="mt-4 p-4 rounded-xl bg-[#0b0f19] border border-[#1e293b] text-center">
          <div className="text-xs text-gray-400 font-mono">EXPLAINABLE RISK SCORE</div>
          <div className="flex items-baseline justify-center gap-1 mt-1">
            <span className={`text-4xl font-extrabold font-mono ${style.text}`}>
              {risk_score}
            </span>
            <span className="text-sm font-mono text-gray-500">/ 100</span>
          </div>

          {/* Progress Bar */}
          <div className="w-full h-2 bg-gray-800 rounded-full mt-3 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${style.bar}`}
              style={{ width: `${Math.min(100, Math.max(5, risk_score))}%` }}
            ></div>
          </div>
        </div>

        {/* Evidence Breakdown Metrics */}
        <div className="mt-4 space-y-2">
          <div className="text-xs font-semibold text-gray-300 font-mono tracking-wider uppercase mb-2">
            Multi-Source Signals
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2.5 rounded-lg bg-[#0b0f19] border border-gray-800">
              <span className="text-gray-400 block text-[10px]">Mining Prob</span>
              <span className="font-bold text-white font-mono">
                {Math.round((evidence_breakdown.mining_probability || 0) * 100)}%
              </span>
            </div>

            <div className="p-2.5 rounded-lg bg-[#0b0f19] border border-gray-800">
              <span className="text-gray-400 block text-[10px]">Spatial Boundary</span>
              <span className={`font-bold font-mono ${evidence_breakdown.outside_permit ? 'text-red-400' : 'text-emerald-400'}`}>
                {evidence_breakdown.outside_permit ? 'Violation' : 'Legal Lease'}
              </span>
            </div>

            <div className="p-2.5 rounded-lg bg-[#0b0f19] border border-gray-800">
              <span className="text-gray-400 block text-[10px]">Volume Overrun</span>
              <span className={`font-bold font-mono ${evidence_breakdown.volume_anomaly ? 'text-amber-400' : 'text-emerald-400'}`}>
                +{evidence_breakdown.volume_mismatch_pct || 0}%
              </span>
            </div>

            <div className="p-2.5 rounded-lg bg-[#0b0f19] border border-gray-800">
              <span className="text-gray-400 block text-[10px]">GPS Route Dev</span>
              <span className={`font-bold font-mono ${evidence_breakdown.gps_route_anomaly ? 'text-amber-400' : 'text-emerald-400'}`}>
                {evidence_breakdown.route_deviation_km || 0} km
              </span>
            </div>
          </div>
        </div>

        {/* Reasons & Explanations */}
        <div className="mt-4">
          <div className="text-xs font-semibold text-gray-300 font-mono tracking-wider uppercase mb-2">
            Evidence Reasons
          </div>
          <ul className="space-y-1.5 text-xs text-gray-300">
            {reasons.map((reason, idx) => (
              <li key={idx} className="flex items-start gap-2 p-2 rounded-lg bg-[#0b0f19] border border-gray-800/60">
                <ChevronRight className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommended Action & Decision Support Disclaimer */}
      <div>
        <div className="p-3.5 rounded-xl bg-cyan-950/30 border border-cyan-500/30">
          <div className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider font-semibold">
            Recommended Action
          </div>
          <div className="text-xs font-bold text-white mt-1 flex items-center justify-between">
            <span>{recommended_action}</span>
            <ArrowRight className="w-4 h-4 text-cyan-400" />
          </div>
        </div>

        <div className="mt-3 text-[10px] text-gray-500 text-center flex items-center justify-center gap-1">
          <Info className="w-3 h-3 text-amber-500 shrink-0" />
          <span>Decision-support prototype. Requires human field verification.</span>
        </div>
      </div>
    </div>
  );
};

export default RiskPanel;
