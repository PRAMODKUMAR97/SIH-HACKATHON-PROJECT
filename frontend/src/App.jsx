import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import DetectionsPage from './pages/DetectionsPage';
import HistoricalTrendsPage from './pages/HistoricalTrendsPage';
import AlertsPage from './pages/AlertsPage';
import ReportsPage from './pages/ReportsPage';
import DroneVerificationPage from './pages/DroneVerificationPage';
import TruckIntelligencePage from './pages/TruckIntelligencePage';

function App() {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0b0f19] text-gray-100 selection:bg-cyan-500 selection:text-black">
      {/* Persistent Left Command Sidebar */}
      <Sidebar />

      {/* Main View Area */}
      <div className="flex-1 flex flex-col h-screen overflow-y-auto">
        <Header />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/detections" element={<DetectionsPage />} />
            <Route path="/historical-trends" element={<HistoricalTrendsPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/drone-verification" element={<DroneVerificationPage />} />
            <Route path="/truck-intelligence" element={<TruckIntelligencePage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
