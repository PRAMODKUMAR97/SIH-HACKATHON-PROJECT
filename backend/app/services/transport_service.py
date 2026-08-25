def analyze_transport_and_rfid(
    route_deviation_km: float,
    unusual_stops_count: int,
    rfid_scan_status: str,
    declared_quantity_kg: float = 0.0,
    measured_net_kg: float = 0.0
) -> dict:
    """
    Evaluates truck GPS route deviations, RFID checkpoints, and weighbridge discrepancies.
    """
    # 1. GPS Route Anomaly Evaluation
    gps_anomaly = route_deviation_km > 1.0 or unusual_stops_count >= 2

    # 2. RFID Checkpoint Anomaly Evaluation
    rfid_anomaly = rfid_scan_status in ["CHECKPOINT_MISSED", "GPS_RFID_MISMATCH"]

    # 3. Weighbridge vs e-Challan Discrepancy Evaluation
    weighbridge_discrepancy_pct = 0.0
    weighbridge_anomaly = False

    if declared_quantity_kg > 0 and measured_net_kg > 0:
        diff_kg = abs(measured_net_kg - declared_quantity_kg)
        weighbridge_discrepancy_pct = (diff_kg / declared_quantity_kg) * 100.0
        # Tolerable variance is 5%; beyond 5% is an anomaly
        if weighbridge_discrepancy_pct > 5.0:
            weighbridge_anomaly = True

    return {
        "gps_anomaly": gps_anomaly,
        "route_deviation_km": route_deviation_km,
        "unusual_stops_count": unusual_stops_count,
        "rfid_scan_status": rfid_scan_status,
        "rfid_anomaly": rfid_anomaly,
        "declared_quantity_kg": declared_quantity_kg,
        "measured_net_kg": measured_net_kg,
        "weighbridge_discrepancy_pct": round(weighbridge_discrepancy_pct, 2),
        "weighbridge_anomaly": weighbridge_anomaly
    }
