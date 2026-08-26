import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, Polyline, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import { AlertCircle, ShieldCheck, ShieldAlert, Truck, Layers, MapPin } from 'lucide-react';

// Fix Leaflet Default Icon Path issues
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom Icon Generator
const createCustomMarker = (color) => {
  return L.divIcon({
    className: 'custom-map-pin',
    html: `
      <div style="
        background-color: ${color};
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 0 10px ${color};
      "></div>
    `,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
};

const MapView = ({ detections = [], permits = [], routes = [], onSelectDetection }) => {
  const center = [23.6900, 86.4800]; // Dhanbad mining surveillance region center

  // Permit polygon geometry mappings
  const permitPolygons = [
    {
      id: 'PERMIT-101',
      name: 'Bharat Mining Corp (Coal)',
      coords: [
        [23.670, 86.440],
        [23.670, 86.460],
        [23.690, 86.460],
        [23.690, 86.440]
      ],
      color: '#10b981' // Green
    },
    {
      id: 'PERMIT-102',
      name: 'Deccan Minerals Ltd (Iron Ore)',
      coords: [
        [23.710, 86.490],
        [23.710, 86.510],
        [23.730, 86.510],
        [23.730, 86.490]
      ],
      color: '#10b981'
    }
  ];

  // Protected forest area polygon
  const protectedPolygon = {
    id: 'PROT-ZONE-01',
    name: 'Damodar Reserve Forest (Eco-Sensitive Zone)',
    coords: [
      [23.640, 86.520],
      [23.640, 86.560],
      [23.680, 86.560],
      [23.680, 86.520]
    ],
    color: '#ef4444' // Red
  };

  const getMarkerColor = (status) => {
    switch (status) {
      case 'LEGAL_WITHIN_PERMIT':
        return '#10b981'; // Green
      case 'SUSPICIOUS_OUTSIDE_PERMIT':
        return '#f59e0b'; // Amber
      case 'ILLEGAL_PROTECTED_AREA':
        return '#ef4444'; // Red
      default:
        return '#06b6d4'; // Cyan
    }
  };

  return (
    <div className="relative w-full h-full rounded-xl overflow-hidden border border-[#1e293b] shadow-2xl bg-[#0b0f19]">
      <MapContainer
        center={center}
        zoom={12}
        scrollWheelZoom={true}
        className="w-full h-full z-10"
        style={{ background: '#0b0f19' }}
      >
        {/* Dark Matter GIS Tiles */}
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {/* Permit Boundary Polygons */}
        {permitPolygons.map((p) => (
          <Polygon
            key={p.id}
            positions={p.coords}
            pathOptions={{ color: p.color, fillColor: p.color, fillOpacity: 0.15, weight: 2, dashArray: '4, 4' }}
          >
            <Tooltip sticky className="custom-tooltip">
              <div className="text-xs font-sans">
                <strong className="text-emerald-400">Legal Lease: {p.id}</strong>
                <div>{p.name}</div>
              </div>
            </Tooltip>
          </Polygon>
        ))}

        {/* Protected Eco Zone Polygon */}
        <Polygon
          positions={protectedPolygon.coords}
          pathOptions={{ color: protectedPolygon.color, fillColor: protectedPolygon.color, fillOpacity: 0.25, weight: 2 }}
        >
          <Tooltip sticky>
            <div className="text-xs font-sans text-red-400">
              <strong>PROTECTED FOREST ZONE</strong>
              <div>{protectedPolygon.name}</div>
            </div>
          </Tooltip>
        </Polygon>

        {/* Truck GPS Route Polylines */}
        {routes.map((r, idx) => (
          <Marker
            key={`truck-g-${idx}`}
            position={[r.latitude, r.longitude]}
            icon={createCustomMarker('#06b6d4')}
          >
            <Popup>
              <div className="text-xs font-sans p-1 text-gray-900">
                <strong className="flex items-center gap-1"><Truck className="w-3.5 h-3.5 text-cyan-600"/> Truck {r.truck_id}</strong>
                <div>Checkpoint: {r.checkpoint_name || 'En route'}</div>
                <div>Status: {r.rfid_scan_status}</div>
                <div>Deviation: {r.route_deviation_km} km</div>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Mining Detection Markers */}
        {detections.map((det) => {
          const color = getMarkerColor(det.legal_status);
          return (
            <Marker
              key={det.detection_id}
              position={[det.latitude, det.longitude]}
              icon={createCustomMarker(color)}
              eventHandlers={{
                click: () => onSelectDetection && onSelectDetection(det)
              }}
            >
              <Popup className="custom-popup">
                <div className="p-2 text-xs font-sans text-gray-900 space-y-1">
                  <div className="flex items-center justify-between border-b pb-1 font-mono font-bold">
                    <span>Site {det.detection_id}</span>
                    <span style={{ color }}>{det.legal_status}</span>
                  </div>
                  <div>Area: <strong>{det.area_ha} ha</strong></div>
                  <div>Est Volume: <strong>{det.estimated_volume_m3.toLocaleString()} m³</strong></div>
                  <div>Mining Prob: <strong>{Math.round(det.mining_probability * 100)}%</strong></div>
                  <button
                    onClick={() => onSelectDetection && onSelectDetection(det)}
                    className="mt-2 w-full py-1 bg-cyan-600 text-white rounded text-[11px] font-medium hover:bg-cyan-700"
                  >
                    View Risk Analysis
                  </button>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      {/* Map Legend Overlay */}
      <div className="absolute bottom-4 left-4 z-20 p-3 rounded-lg bg-[#111827]/90 backdrop-blur-md border border-[#1e293b] text-xs space-y-1.5 shadow-xl select-none">
        <div className="font-semibold text-gray-300 text-[11px] uppercase tracking-wider mb-1">Map Layers & Status</div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block border border-white"></span>
          <span className="text-gray-300">Legal Mining Lease</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-amber-500 inline-block border border-white"></span>
          <span className="text-gray-300">Suspicious Outside Lease</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-500 inline-block border border-white"></span>
          <span className="text-gray-300">Illegal Protected Zone</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-cyan-400 inline-block border border-white"></span>
          <span className="text-gray-300">Monitored Truck GPS</span>
        </div>
      </div>
    </div>
  );
};

export default MapView;
