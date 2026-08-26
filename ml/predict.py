"""Run the saved Random Forest model for one raster-derived feature record."""
from __future__ import annotations

import argparse
import json

from joblib import load

from features import feature_vector


def predict(model_path: str, feature_json: str) -> dict:
    bundle = load(model_path); vector = feature_vector(json.loads(feature_json)); probability = float(bundle["model"].predict_proba([vector])[0][1])
    return {"mining_probability": round(probability, 4), "non_mining_probability": round(1 - probability, 4), "confidence": "VERY HIGH" if probability >= .8 else "HIGH" if probability >= .6 else "MEDIUM" if probability >= .3 else "LOW", "warning": bundle.get("limitations")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict mining probability from a JSON feature record.")
    parser.add_argument("--model", default="ml/model/model.joblib")
    parser.add_argument("--features", required=True, help="JSON object containing the documented feature columns")
    print(json.dumps(predict(parser.parse_args().model, parser.parse_args().features), indent=2))
