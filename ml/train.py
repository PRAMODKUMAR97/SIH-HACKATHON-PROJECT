"""Train and save the documented local Random Forest baseline.

Example:
  python ml/train.py --input data/demo/training_samples.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

from joblib import dump
from sklearn.ensemble import RandomForestClassifier

from features import FEATURE_COLUMNS
from preprocessing import load_samples


def train(input_path: str, output_path: str) -> dict:
    features, labels = load_samples(input_path)
    model = RandomForestClassifier(n_estimators=160, max_depth=8, min_samples_leaf=2, class_weight="balanced", random_state=20260826, n_jobs=-1)
    model.fit(features, labels)
    output = Path(output_path); output.parent.mkdir(parents=True, exist_ok=True)
    dump({"model": model, "feature_columns": FEATURE_COLUMNS, "training_source": str(input_path), "limitations": "Small demo training dataset only. Do not use for operational or legal conclusions."}, output)
    return {"samples": len(labels), "mining_samples": sum(labels), "non_mining_samples": len(labels) - sum(labels), "model": str(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train KHANAN-NETRA's local Random Forest baseline.")
    parser.add_argument("--input", default="data/demo/training_samples.csv")
    parser.add_argument("--output", default="ml/model/model.joblib")
    print(train(**vars(parser.parse_args())))
