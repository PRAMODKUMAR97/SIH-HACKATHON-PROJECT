import React from 'react';
import { Plane, ArrowRight, Layers, ShieldCheck, Box, Maximize2, Cpu } from 'lucide-react';

const DroneVerificationPage = () => {
  const steps = [
    {
      number: '01',
      title: 'Satellite Detection',
      desc: 'Sentinel-1 SAR & Sentinel-2 Optical sensors detect surface anomalies and spectral changes across wide mining regions.',
      icon: Layers,
    },
    {
      number: '02',
      title: 'Drone Request Dispatch',
      desc: 'High-risk suspicious locations automatically trigger targeted autonomous drone mission dispatch requests.',
      icon: Plane,
    },
    {
      number: '03',
      title: '3D Photogrammetry & Mesh',
      desc: 'Structure-from-Motion (SfM) creates geo-referenced point clouds, DSM/DTM surface models, and 3D meshes.',
      icon: Box,
    },
    {
      number: '04',
      title: 'Excavation Volume Calculation',
      desc: 'Precise depth and pit volume measurements compare estimated excavation against legal mining lease limits.',
      icon: Maximize2,
    },
    {
      number: '05',
      title: 'AI Evidence Fusion',
      desc: '3D drone volume metrics cross-check against e-Challan transportation logs to generate final risk score.',
      icon: Cpu,
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Module Status Header */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#111827] via-[#162035] to-[#111827] border border-cyan-500/30 space-y-3 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Plane className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-white font-mono">Drone 3D Photogrammetry Module</h2>
              <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                FUTURE INTEGRATION PIPELINE
              </span>
            </div>
            <p className="text-xs text-gray-400 mt-0.5">
              High-resolution local 3D mine reconstruction and volumetric excavation verification workflow.
            </p>
          </div>
        </div>
      </div>

      {/* Intended Workflow Stepper */}
      <div className="p-6 rounded-xl bg-[#111827] border border-[#1e293b] space-y-6">
        <h3 className="text-xs font-bold text-gray-300 font-mono uppercase tracking-wider">
          Intended Drone 3D Verification Workflow
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {steps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <div key={idx} className="relative p-4 rounded-xl bg-[#0b0f19] border border-gray-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold font-mono text-cyan-400">{step.number}</span>
                  <div className="p-2 rounded-lg bg-gray-800 text-cyan-400">
                    <Icon className="w-4 h-4" />
                  </div>
                </div>
                <h4 className="text-xs font-bold text-white font-mono">{step.title}</h4>
                <p className="text-[11px] text-gray-400 leading-relaxed">{step.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Hardware Interface Specs Note */}
      <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] flex items-center justify-between text-xs font-mono">
        <span className="text-gray-400">Supported Formats: OpenDroneMap / WebODM, DSM/DTM GeoTIFF, Point Cloud (.LAS/.OBJ)</span>
        <span className="text-cyan-400">Backend Open ODM Endpoint Integration Point Ready</span>
      </div>
    </div>
  );
};

export default DroneVerificationPage;
