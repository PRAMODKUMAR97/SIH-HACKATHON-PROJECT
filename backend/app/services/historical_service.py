def analyze_historical_change(activity_growth_pct: float) -> dict:
    """
    Evaluates activity growth percentage over historical periods.
    """
    historical_anomaly = activity_growth_pct > 0.50  # More than 50% growth is flagged
    return {
        "activity_growth_pct": round(activity_growth_pct * 100.0, 2) if activity_growth_pct <= 1.0 else round(activity_growth_pct, 2),
        "historical_anomaly": historical_anomaly
    }
