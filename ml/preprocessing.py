"""Load labelled, raster-derived training samples from a portable CSV file."""
from __future__ import annotations

import csv
from pathlib import Path

from features import feature_vector


def load_samples(path: str | Path) -> tuple[list[list[float]], list[int]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("Training CSV has no rows.")
    if "label" not in rows[0]:
        raise ValueError("Training CSV must include label (1=mining, 0=non-mining).")
    features = [feature_vector(row) for row in rows]
    labels = [int(row["label"]) for row in rows]
    if set(labels) != {0, 1}:
        raise ValueError("Training CSV must include both mining (1) and non-mining (0) samples.")
    return features, labels
