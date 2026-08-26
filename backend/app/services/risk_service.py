"""Explainable, configurable evidence-fusion scoring."""
from __future__ import annotations

WEIGHTS = {"mining_probability": 30, "change_magnitude": 20, "outside_permit": 25, "protected_overlap": 12, "affected_area": 5, "history": 4, "drone": 8, "transport": 10}


def _level(score: int) -> str:
    return "CRITICAL" if score >= 85 else "HIGH" if score >= 65 else "MEDIUM" if score >= 35 else "LOW"


def calculate_risk(*, probability: float, change_percentage: float, outside_percentage: float, protected_percentage: float, affected_area_ha: float, history_score: float = 0.8, drone_mismatch: bool = False, transport_anomalies: int = 0) -> dict:
    """Fuse observed/modelled indicators into an auditable 0–100 score."""
    contributions = {
        "Mining probability": round(max(0, min(1, probability)) * WEIGHTS["mining_probability"]),
        "Rapid area increase": round(min(100, max(0, change_percentage)) / 100 * WEIGHTS["change_magnitude"]),
        "Outside permit": round(min(100, max(0, outside_percentage)) / 100 * WEIGHTS["outside_permit"]),
        "Protected-area overlap": round(min(100, max(0, protected_percentage)) / 100 * WEIGHTS["protected_overlap"]),
        "Affected area": round(min(1, max(0, affected_area_ha) / 8) * WEIGHTS["affected_area"]),
        "Historical trend": round(max(0, min(1, history_score)) * WEIGHTS["history"]),
        "Drone volume mismatch": WEIGHTS["drone"] if drone_mismatch else 0,
        "Transport anomalies": min(WEIGHTS["transport"], max(0, transport_anomalies) * 5),
    }
    score = min(100, sum(contributions.values()))
    return {"score": score, "level": _level(score), "weights": WEIGHTS, "breakdown": contributions, "interpretation": "AI-generated evidence score for prioritisation. It does not determine legal liability."}
