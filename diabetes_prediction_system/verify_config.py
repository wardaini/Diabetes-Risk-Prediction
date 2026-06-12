#!/usr/bin/env python3
"""
Verify configuration and sync with model features
"""

import json
import joblib
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
MODEL_PATH = BASE_DIR / "random_forest_tuned_model.pkl"

print("=" * 60)
print("Configuration Verification")
print("=" * 60)

# Load model to get actual features
print("\nLoading model...")
model = joblib.load(MODEL_PATH)
model_features = list(model.feature_names_in_)
print(f"Model features: {model_features}")

# Load current config
print("\nLoading current config...")
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
    config_features = config.get('features', [])
    print(f"Config features: {config_features}")

# Check if they match
if model_features == config_features:
    print("\n✓ Features match! Config is correct.")
else:
    print("\n✗ Features DON'T match! Updating config...")
    config['features'] = model_features
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print(f"✓ Updated config with model features: {model_features}")

# Test prediction with sample data
print("\n" + "=" * 60)
print("Testing prediction...")
print("=" * 60)

sample_input = np.array([[0, 0, 1, 25.5, 1, 2]])
print(f"Sample input shape: {sample_input.shape}")
print(f"Sample input: {sample_input}")

try:
    probability = model.predict_proba(sample_input)[0][1]
    print(f"✓ Prediction successful! Probability: {probability:.4f}")
except Exception as e:
    print(f"✗ Prediction failed: {e}")

print("\n" + "=" * 60)
