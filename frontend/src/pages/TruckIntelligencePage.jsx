import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Truck, MapPin, AlertTriangle, ShieldCheck, CheckCircle, Navigation } from 'lucide-react';

const TruckIntelligencePage = () => {
  const [trucks, setTrucks] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedTruck, setSelectedTruck] = useState(null);

  useEffect(() => {
    fetchTruckData();
  }, []);

  const fetchTruckData = async () => {
    try {
      const [truckRes, routeRes] = await Promise.all([
        axios.get('/api/trucks'),
        axios.get('/api/routes')
      ]);
      setTrucks(truckRes.data || []);
      setRoutes(routeRes.data || []);
    } catch (err) {
      console.error('Error fetching truck data:', err);
    }
  };

  const getRFIDBadge = (status) => {
    switch (status) {
      case 'CHECKPOINT_VERIFIED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">VERIFIED</span>;
      case 'CHECKPOINT_MISSED':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">CHECKPOINT MISSED</span>;
      case 'GPS_RFID_MISMATCH':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30">GPS/RFID MISMATCH</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-500/10 text-gray-400 border border-gray-500/30">{status}</span>;
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl bg-[#111827] border border-[#1e293b] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <Truck className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white font-mono">Truck Transportation & Fleet Intelligence</h2>
            <p className="text-xs text-gray-400">GPS route deviation tracking, RFID checkpoint matching, and weighbridge cross-checks.</p>
          </div>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="text-gray-400">Total Monitored Fleet: <strong className="text-white">{trucks.length}</strong></span>
          <span className="text-gray-400">Active GPS Logs: <strong className="text-cyan-400">{routes.length}</strong></span>
        </div>
      </div>

      {/* Fleet Table */}
      <div className="rounded-xl bg-[#111827] border border-[#1e293b] overflow-hidden shadow-xl">
        <div className="px-6 py-4 border-b border-[#1e293b] flex items-center justify-between">
          <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider">
            Active Mineral Transport Fleet Logs
          </h3>
          <span className="text-xs text-gray-400 font-mono">Realtime GPS Signals</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-gray-300 font-mono">
            <thead className="bg-[#0b0f19] text-gray-400 uppercase tracking-wider text-[10px] border-b border-[#1e293b]">
              <tr>
                <th className="px-6 py-3.5">Truck ID</th>
                <th className="px-6 py-3.5">License Plate</th>
                <th className="px-6 py-3.5">Carrier Company</th>
                <th className="px-6 py-3.5">Assigned Permit</th>
                <th className="px-6 py-3.5">Route Deviation</th>
                <th className="px-6 py-3.5">Unusual Stops</th>
                <th className="px-6 py-3.5">RFID Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {routes.map((r) => {
                const truck = trucks.find(t => t.truck_id === r.truck_id) || {};
                return (
                  <tr key={r.gps_id} className="hover:bg-[#1f2937]/50 transition-colors">
                    <td className="px-6 py-4 font-bold text-white flex items-center gap-2">
                      <Truck className="w-4 h-4 text-cyan-400" />
                      {r.truck_id}
                    </td>
                    <td className="px-6 py-4 text-gray-300 font-bold">{truck.license_plate || 'JH-10-XX-XXXX'}</td>
                    <td className="px-6 py-4 text-gray-400">{truck.carrier_company || 'Mining Logistics Co'}</td>
                    <td className="px-6 py-4 text-cyan-400">{truck.assigned_permit_id || 'PERMIT-101'}</td>
                    <td className={`px-6 py-4 font-bold ${r.route_deviation_km > 1.0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                      {r.route_deviation_km} km
                    </td>
                    <td className="px-6 py-4 text-white">{r.unusual_stops_count} stops</td>
                    <td className="px-6 py-4">{getRFIDBadge(r.rfid_scan_status)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TruckIntelligencePage;
