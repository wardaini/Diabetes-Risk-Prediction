#!/usr/bin/env python3
"""
Debug script to check model features and order
"""

import joblib
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "random_forest_tuned_model.pkl"

print("=" * 60)
print("Model Feature Debugging")
print("=" * 60)

try:
    model = joblib.load(MODEL_PATH)
    print(f"\nModel type: {type(model)}")
    print(f"Model: {model}")
    
    # Check if model has feature names stored
    if hasattr(model, 'feature_names_in_'):
        print(f"\nFeature names in model: {model.feature_names_in_}")
        print(f"Feature order: {list(model.feature_names_in_)}")
        print(f"Number of features: {len(model.feature_names_in_)}")
    else:
        print("\nModel does NOT have feature_names_in_ attribute")
        print(f"Model n_features_in_: {model.n_features_in_ if hasattr(model, 'n_features_in_') else 'N/A'}")
        
    # Try to get other info
    if hasattr(model, 'n_features_in_'):
        print(f"Expected number of features: {model.n_features_in_}")
    
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
