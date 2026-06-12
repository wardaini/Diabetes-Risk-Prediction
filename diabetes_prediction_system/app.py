"""
Diabetes Prediction System - Flask API
Main application file that serves the prediction API
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Configuration
BASE_DIR = Path(__file__).parent
MODEL_PATH = Path(r"D:\diabetes_prediction_system-main\diabetes_prediction_system/random_forest_tuned_model.pkl")
THRESHOLD_PATH = Path(r"D:\diabetes_prediction_system-main\diabetes_prediction_system\optimal_threshold.pkl")
CONFIG_PATH = BASE_DIR / 'config.json'

# Load model and configuration
model = None
optimal_threshold = None
config = None

def load_model_and_config():
    """Load the trained model and configuration"""
    global model, optimal_threshold, config

    try:
        # Load model using joblib (better for sklearn models)
        if MODEL_PATH.exists():
            try:
                model = joblib.load(MODEL_PATH)
                print(f"Model loaded from: {MODEL_PATH}")
                print(f"Model feature names: {list(model.feature_names_in_)}")
            except Exception as e:
                print(f"Error loading model with joblib: {e}")
                model = None
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}")
            model = None

        # Load configuration
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                print(f"Configuration loaded from file")
        else:
            # Default configuration
            config = {
                'threshold': {
                    'low': 0.18,
                    'medium': 0.36
                },
                'model_type': 'random_forest',
                'features': [
                    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'PhysActivity', 'GenHlth'
                ]
            }
            print("Using default configuration")

        # CRITICAL: Override features with model's actual feature order if model loaded
        if model is not None and hasattr(model, 'feature_names_in_'):
            model_features = list(model.feature_names_in_)
            config['features'] = model_features
            print(f"CRITICAL: Using model's feature order: {model_features}")
        else:
            print(f"WARNING: Model feature names not available, using config features")

        # Load optimal threshold
        if THRESHOLD_PATH.exists():
            with open(THRESHOLD_PATH, 'rb') as f:
                optimal_threshold = pickle.load(f)
                print(f"Optimal threshold loaded: {optimal_threshold}")
                # Update config with loaded threshold
                if isinstance(optimal_threshold, dict):
                    config['threshold'] = optimal_threshold
                else:
                    # If threshold is a single value, use it as medium threshold
                    config['threshold'] = {
                        'low': optimal_threshold * 0.5,
                        'medium': optimal_threshold
                    }
        else:
            print(f"Warning: Threshold file not found at {THRESHOLD_PATH}")
            print("Using default threshold")

    except Exception as e:
        import traceback
        print(f"Error loading model: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        config = {
            'threshold': {'low': 0.25, 'medium': 0.5},
            'model_type': 'unknown',
            'features': []
        }
        model = None
        optimal_threshold = None

# Initialize on startup
load_model_and_config()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/styles.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/script.js')
def serve_js():
    """Serve JavaScript file"""
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # CRITICAL: Use model's actual feature order, NOT config
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded'}), 500
            
        if not hasattr(model, 'feature_names_in_'):
            return jsonify({'success': False, 'error': 'Model has no feature_names_in_'}), 500
        
        features = list(model.feature_names_in_)
        print(f"DEBUG PREDICT: Model features from model.feature_names_in_: {features}")
        print(f"DEBUG PREDICT: Received data: {data}")
        
        input_features = [float(data.get(f, 0)) for f in features]
        print(f"DEBUG PREDICT: Input features (as floats): {input_features}")

        # Create DataFrame with proper feature names to avoid scikit-learn warning
        input_df = pd.DataFrame([input_features], columns=features)
        print(f"DEBUG PREDICT: Input DataFrame:\n{input_df}")
        print(f"DEBUG PREDICT: DataFrame dtypes:\n{input_df.dtypes}")

        # Get probability
        probability = model.predict_proba(input_df)[0][1]
        model_status = "Model berhasil digunakan"

        # Threshold - get from model's attributes or use config as fallback
        threshold = config.get('threshold', {'low': 0.18, 'medium': 0.36}) if config else {'low': 0.18, 'medium': 0.36}

        # Tentukan level risiko
        if probability < threshold['low']:
            risk_level = 'Rendah'
        elif probability < threshold['medium']:
            risk_level = 'Sedang'
        else:
            risk_level = 'Tinggi'

        return jsonify({
            'success': True,
            'probability': float(probability),
            'risk_level': risk_level,
            'threshold': threshold,
            'display_threshold': config.get('display_threshold', threshold) if config else threshold,
            'model_status': model_status,
            'message': f'Risiko diabetes: {risk_level}'
        })

    except Exception as e:
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"Error in predict: {error_msg}")
        print(f"Traceback: {error_trace}")
        return jsonify({'success': False, 'error': error_msg, 'traceback': error_trace}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_path': str(MODEL_PATH),
        'threshold_path': str(THRESHOLD_PATH),
        'optimal_threshold': optimal_threshold,
        'config': config,
        'debug_config_features': config.get('features', []) if config else 'config is None'
    })

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'model_type': config.get('model_type', 'unknown'),
        'threshold': config.get('threshold', {}),
        'features': config.get('features', [])
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Diabetes Prediction System - Flask API")
    print("=" * 50)
    print(f"Server running on http://localhost:5000")
    print("API Endpoint: http://localhost:5000/predict")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)