"""Feature definitions shared by the baseline Random Forest scripts."""
from __future__ import annotations

FEATURE_COLUMNS = ["blue", "green", "red", "nir", "swir1", "ndvi", "ndwi", "bare_soil", "temporal_difference", "sar_change", "slope"]


def feature_vector(row: dict) -> list[float]:
    """Return ordered numeric features; reject incomplete training records."""
    missing = [column for column in FEATURE_COLUMNS if row.get(column) in (None, "")]
    if missing:
        raise ValueError(f"Training sample is missing required features: {', '.join(missing)}")
    return [float(row[column]) for column in FEATURE_COLUMNS]
