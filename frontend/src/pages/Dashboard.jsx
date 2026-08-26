import React, { useEffect, useState } from 'react';
import axios from 'axios';
import KPICard from '../components/KPICard';
import MapView from '../components/MapView';
import RiskPanel from '../components/RiskPanel';
import DetectionModal from '../components/DetectionModal';
import { Eye, Truck, AlertTriangle, Layers, Maximize2 } from 'lucide-react';

const Dashboard = () => {
  const [detections, setDetections] = useState([]);
  const [permits, setPermits] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [selectedRiskData, setSelectedRiskData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [detRes, permitRes, routeRes] = await Promise.all([
        axios.get('/api/detections'),
        axios.get('/api/permits'),
        axios.get('/api/routes')
      ]);

      setDetections(detRes.data || []);
      setPermits(permitRes.data || []);
      setRoutes(routeRes.data || []);

      if (detRes.data && detRes.data.length > 0) {
        handleSelectDetection(detRes.data[0]);
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectDetection = async (det) => {
    setSelectedDetection(det);
    try {
      const riskRes = await axios.get(`/api/risk/${det.detection_id}`);
      setSelectedRiskData(riskRes.data);
    } catch (err) {
      console.error(`Error fetching risk for ${det.detection_id}:`, err);
    }
  };

  // KPI Calculations from backend data
  const totalArea = detections.reduce((acc, curr) => acc + (curr.area_ha || 0), 0);
  const totalVolume = detections.reduce((acc, curr) => acc + (curr.estimated_volume_m3 || 0), 0);
  const highRiskCount = detections.filter(d => d.legal_status !== 'LEGAL_WITHIN_PERMIT').length;

  return (
    <div className="p-6 space-y-6">
      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <KPICard
          title="Monitored Area"
          value={`${totalArea.toFixed(1)} ha`}
          subtitle="Active Satellite Swath"
          icon={Layers}
          color="cyan"
          trend="+1.2 ha / 30d"
        />
        <KPICard
          title="Active Trucks"
          value={`${routes.length} Trucks`}
          subtitle="Monitored Fleet"
          icon={Truck}
          color="emerald"
        />
        <KPICard
          title="Detected Sites"
          value={`${detections.length} Sites`}
          subtitle="Satellite AI Predictions"
          icon={Eye}
          color="cyan"
        />
        <KPICard
          title="High Risk Alerts"
          value={`${highRiskCount} Alerts`}
          subtitle="Requires Field Action"
          icon={AlertTriangle}
          color="red"
          trend="Critical priority"
        />
        <KPICard
          title="Excavation Volume"
          value={`${(totalVolume / 1000).toFixed(1)}k m³`}
          subtitle="Estimated Excavation"
          icon={Maximize2}
          color="amber"
        />
      </div>

      {/* Main Grid: Interactive Map & Risk Fusion Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-270px)] min-h-[500px]">
        <div className="lg:col-span-2 h-full">
          <MapView
            detections={detections}
            permits={permits}
            routes={routes}
            onSelectDetection={handleSelectDetection}
          />
        </div>
        <div className="h-full">
          <RiskPanel
            riskData={selectedRiskData}
            selectedDetection={selectedDetection}
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
