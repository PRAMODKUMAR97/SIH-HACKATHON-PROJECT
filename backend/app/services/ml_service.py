import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Synthetic baseline training dataset for Mining Detection ML model
# Features: [ndvi_change, sar_vv_vh_ratio, texture_variance, spectral_anomaly_score]
# Target: 0 (No Mining), 1 (Active Mining)
X_TRAIN = np.array([
    [-0.05, 0.10, 0.05, 0.10],  # No mining
    [-0.10, 0.20, 0.10, 0.15],  # No mining
    [-0.02, 0.12, 0.08, 0.08],  # No mining
    [-0.15, 0.25, 0.12, 0.20],  # Low probability
    [-0.35, 0.50, 0.40, 0.55],  # Mining
    [-0.55, 0.70, 0.65, 0.75],  # Mining
    [-0.80, 0.90, 0.85, 0.90],  # Heavy Mining
    [-0.92, 0.95, 0.92, 0.95],  # Heavy Mining
    [-0.45, 0.65, 0.58, 0.62],  # Mining
    [-0.70, 0.82, 0.78, 0.85],  # Mining
])

Y_TRAIN = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

# Initialize baseline Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=20, random_state=42)
rf_model.fit(X_TRAIN, Y_TRAIN)


def train_and_predict_detection(
    ndvi_change: float,
    sar_vv_vh_ratio: float,
    texture_variance: float,
    spectral_anomaly_score: float
) -> dict:
    """
    Predicts mining probability and confidence using Random Forest model.
    """
    features = np.array([[ndvi_change, sar_vv_vh_ratio, texture_variance, spectral_anomaly_score]])
    probabilities = rf_model.predict_proba(features)[0]
    
    # Mining probability corresponds to class 1
    mining_prob = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])

    # Assign confidence level based on probability distance from 0.5
    confidence_margin = abs(mining_prob - 0.5)
    if confidence_margin > 0.35:
        confidence_level = "HIGH"
    elif confidence_margin > 0.15:
        confidence_level = "MEDIUM"
    else:
        confidence_level = "LOW"

    return {
        "mining_probability": round(mining_prob, 4),
        "confidence_level": confidence_level
    }
