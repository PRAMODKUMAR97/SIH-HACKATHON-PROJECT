from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict


# --- Permit Schemas ---
class PermitBase(BaseModel):
    permit_id: str
    owner_name: str
    mineral_type: str
    permitted_volume_m3: float
    max_depth_m: Optional[float] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    status: Optional[str] = "ACTIVE"

class PermitResponse(PermitBase):
    class Config:
        from_attributes = True


# --- Detection Schemas ---
class DetectionBase(BaseModel):
    detection_id: str
    latitude: float
    longitude: float
    area_ha: float
    estimated_depth_m: Optional[float] = 0.0
    estimated_volume_m3: Optional[float] = 0.0
    ndvi_change: Optional[float] = 0.0
    sar_vv_vh_ratio: Optional[float] = 0.0
    texture_variance: Optional[float] = 0.0
    spectral_anomaly_score: Optional[float] = 0.0
    permit_id: Optional[str] = None
    detection_date: Optional[str] = None

class DetectionResponse(DetectionBase):
    mining_probability: float
    confidence_level: str
    legal_status: str
    is_protected_area: bool

    class Config:
        from_attributes = True


# --- Truck & Transport Schemas ---
class TruckBase(BaseModel):
    truck_id: str
    license_plate: str
    driver_name: str
    carrier_company: Optional[str] = None
    assigned_permit_id: Optional[str] = None
    status: Optional[str] = "ACTIVE"

class TruckResponse(TruckBase):
    class Config:
        from_attributes = True


class GPSRecordBase(BaseModel):
    gps_id: str
    truck_id: str
    detection_id: Optional[str] = None
    latitude: float
    longitude: float
    speed_kmh: float
    timestamp: str
    route_deviation_km: float
    unusual_stops_count: int
    checkpoint_name: Optional[str] = None
    rfid_scan_status: str

class GPSRecordResponse(GPSRecordBase):
    class Config:
        from_attributes = True


class ChallanResponse(BaseModel):
    challan_id: str
    truck_id: str
    permit_id: Optional[str] = None
    mineral_type: str
    declared_quantity_kg: float
    issue_timestamp: str
    destination: Optional[str] = None

    class Config:
        from_attributes = True


class WeighbridgeResponse(BaseModel):
    weighbridge_id: str
    challan_id: str
    truck_id: str
    measured_gross_kg: float
    tare_weight_kg: float
    measured_net_kg: float
    timestamp: str

    class Config:
        from_attributes = True


# --- Satellite Analysis Request Schema ---
class SatelliteAnalysisRequest(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate of target site")
    longitude: float = Field(..., description="Longitude coordinate of target site")
    area_ha: Optional[float] = Field(2.5, description="Estimated area in hectares")
    ndvi_change: Optional[float] = Field(-0.45, description="NDVI change value (-1 to 1)")
    sar_vv_vh_ratio: Optional[float] = Field(0.65, description="SAR VV/VH backscatter ratio")
    texture_variance: Optional[float] = Field(0.50, description="Surface texture variance")
    drone_estimated_volume_m3: Optional[float] = Field(None, description="Optional drone 3D volume estimate")


# --- Risk Assessment & Evidence Fusion Schemas ---
class EvidenceBreakdown(BaseModel):
    mining_probability: float
    outside_permit: bool
    protected_area: bool
    legal_status: str
    volume_anomaly: bool
    volume_mismatch_pct: float
    gps_route_anomaly: bool
    route_deviation_km: float
    rfid_mismatch: bool
    weighbridge_discrepancy_pct: float
    historical_change_pct: float

class RiskAssessmentResponse(BaseModel):
    risk_id: str
    detection_id: str
    risk_score: float
    risk_level: str
    evidence_breakdown: EvidenceBreakdown
    reasons: List[str]
    recommended_action: str
    created_at: str

    class Config:
        from_attributes = True
