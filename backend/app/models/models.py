from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Permit(Base):
    __tablename__ = "permits"

    permit_id = Column(String, primary_key=True, index=True)
    owner_name = Column(String, nullable=False)
    mineral_type = Column(String, nullable=False)
    permitted_volume_m3 = Column(Float, nullable=False, default=0.0)
    max_depth_m = Column(Float, nullable=True)
    issue_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    status = Column(String, default="ACTIVE")

    detections = relationship("Detection", back_populates="permit")
    trucks = relationship("Truck", back_populates="permit")


class Detection(Base):
    __tablename__ = "detections"

    detection_id = Column(String, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    area_ha = Column(Float, nullable=False, default=0.0)
    estimated_depth_m = Column(Float, default=0.0)
    estimated_volume_m3 = Column(Float, default=0.0)
    
    # Remote Sensing & Spectral Features
    ndvi_change = Column(Float, default=0.0)
    sar_vv_vh_ratio = Column(Float, default=0.0)
    texture_variance = Column(Float, default=0.0)
    spectral_anomaly_score = Column(Float, default=0.0)
    
    # Mining ML Prediction & Status
    mining_probability = Column(Float, default=0.0)
    confidence_level = Column(String, default="LOW")  # LOW, MEDIUM, HIGH
    legal_status = Column(String, default="PENDING_VERIFICATION")  # LEGAL_WITHIN_PERMIT, SUSPICIOUS_OUTSIDE_PERMIT, ILLEGAL_PROTECTED_AREA
    is_protected_area = Column(Boolean, default=False)
    
    permit_id = Column(String, ForeignKey("permits.permit_id"), nullable=True)
    detection_date = Column(String, default=datetime.utcnow().strftime("%Y-%m-%d"))

    permit = relationship("Permit", back_populates="detections")
    gps_records = relationship("GPSRecord", back_populates="detection")
    historical_activities = relationship("HistoricalActivity", back_populates="detection")
    risk_assessment = relationship("RiskAssessment", back_populates="detection", uselist=False)
    alerts = relationship("Alert", back_populates="detection")


class Truck(Base):
    __tablename__ = "trucks"

    truck_id = Column(String, primary_key=True, index=True)
    license_plate = Column(String, nullable=False)
    driver_name = Column(String, nullable=False)
    carrier_company = Column(String, nullable=True)
    assigned_permit_id = Column(String, ForeignKey("permits.permit_id"), nullable=True)
    status = Column(String, default="ACTIVE")

    permit = relationship("Permit", back_populates="trucks")
    gps_records = relationship("GPSRecord", back_populates="truck")
    challans = relationship("Challan", back_populates="truck")
    weighbridge_records = relationship("WeighbridgeRecord", back_populates="truck")


class GPSRecord(Base):
    __tablename__ = "gps_records"

    gps_id = Column(String, primary_key=True, index=True)
    truck_id = Column(String, ForeignKey("trucks.truck_id"), nullable=False)
    detection_id = Column(String, ForeignKey("detections.detection_id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed_kmh = Column(Float, default=0.0)
    timestamp = Column(String, nullable=False)
    route_deviation_km = Column(Float, default=0.0)
    unusual_stops_count = Column(Integer, default=0)
    checkpoint_name = Column(String, nullable=True)
    rfid_scan_status = Column(String, default="CHECKPOINT_VERIFIED")  # CHECKPOINT_VERIFIED, CHECKPOINT_MISSED, GPS_RFID_MISMATCH

    truck = relationship("Truck", back_populates="gps_records")
    detection = relationship("Detection", back_populates="gps_records")


class Checkpoint(Base):
    __tablename__ = "checkpoints"

    checkpoint_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rfid_reader_active = Column(Boolean, default=True)


class Challan(Base):
    __tablename__ = "challans"

    challan_id = Column(String, primary_key=True, index=True)
    truck_id = Column(String, ForeignKey("trucks.truck_id"), nullable=False)
    permit_id = Column(String, ForeignKey("permits.permit_id"), nullable=True)
    mineral_type = Column(String, nullable=False)
    declared_quantity_kg = Column(Float, nullable=False)
    issue_timestamp = Column(String, nullable=False)
    destination = Column(String, nullable=True)

    truck = relationship("Truck", back_populates="challans")
    weighbridge_record = relationship("WeighbridgeRecord", back_populates="challan", uselist=False)


class WeighbridgeRecord(Base):
    __tablename__ = "weighbridge_records"

    weighbridge_id = Column(String, primary_key=True, index=True)
    challan_id = Column(String, ForeignKey("challans.challan_id"), nullable=False)
    truck_id = Column(String, ForeignKey("trucks.truck_id"), nullable=False)
    measured_gross_kg = Column(Float, nullable=False)
    tare_weight_kg = Column(Float, nullable=False)
    measured_net_kg = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
    operator_id = Column(String, nullable=True)

    challan = relationship("Challan", back_populates="weighbridge_record")
    truck = relationship("Truck", back_populates="weighbridge_records")


class HistoricalActivity(Base):
    __tablename__ = "historical_activities"

    history_id = Column(String, primary_key=True, index=True)
    detection_id = Column(String, ForeignKey("detections.detection_id"), nullable=False)
    period = Column(String, nullable=False)
    historical_area_ha = Column(Float, default=0.0)
    historical_volume_m3 = Column(Float, default=0.0)
    activity_growth_pct = Column(Float, default=0.0)

    detection = relationship("Detection", back_populates="historical_activities")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    risk_id = Column(String, primary_key=True, index=True)
    detection_id = Column(String, ForeignKey("detections.detection_id"), unique=True, nullable=False)
    risk_score = Column(Float, nullable=False)  # 0 to 100
    risk_level = Column(String, nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    
    # Individual evidence components
    mining_prob_score = Column(Float, default=0.0)
    boundary_violation_score = Column(Float, default=0.0)
    volume_anomaly_score = Column(Float, default=0.0)
    gps_anomaly_score = Column(Float, default=0.0)
    rfid_anomaly_score = Column(Float, default=0.0)
    historical_change_score = Column(Float, default=0.0)

    reasons = Column(Text, nullable=False)  # JSON string or bullet points
    recommended_action = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    detection = relationship("Detection", back_populates="risk_assessment")


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String, primary_key=True, index=True)
    detection_id = Column(String, ForeignKey("detections.detection_id"), nullable=False)
    severity = Column(String, nullable=False)  # INFO, WARNING, CRITICAL
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(String, default=datetime.utcnow().isoformat())

    detection = relationship("Detection", back_populates="alerts")
