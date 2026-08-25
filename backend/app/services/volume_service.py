def analyze_volume(
    permitted_volume_m3: float,
    estimated_excavation_m3: float,
    transported_quantity_m3: float = 0.0,
    drone_estimated_volume_m3: float = None
) -> dict:
    """
    Compares excavation volume against permit volume and transported volume.
    Integrates drone 3D volume estimate if available.
    """
    effective_excavation = drone_estimated_volume_m3 if drone_estimated_volume_m3 is not None else estimated_excavation_m3

    volume_mismatch_pct = 0.0
    volume_anomaly = False

    if permitted_volume_m3 > 0:
        if effective_excavation > permitted_volume_m3:
            volume_mismatch_pct = ((effective_excavation - permitted_volume_m3) / permitted_volume_m3) * 100.0
            volume_anomaly = True
    else:
        # Mining occurring outside permit (0 permitted volume)
        if effective_excavation > 0:
            volume_mismatch_pct = 100.0
            volume_anomaly = True

    return {
        "permitted_volume_m3": permitted_volume_m3,
        "estimated_excavation_m3": effective_excavation,
        "transported_quantity_m3": transported_quantity_m3,
        "volume_mismatch_pct": round(volume_mismatch_pct, 2),
        "volume_anomaly": volume_anomaly,
        "used_drone_estimate": drone_estimated_volume_m3 is not None
    }
