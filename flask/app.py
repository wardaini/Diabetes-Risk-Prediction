from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / 'diabetes_rf_model.pkl'

# Load model
model = None
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded: {MODEL_PATH}")
    print(f"   Features: {list(model.feature_names_in_)}")
except Exception as e:
    print(f"❌ Error loading model: {e}")

THRESHOLD = 0.5

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'success': False, 'error': 'Model tidak tersedia'}), 500

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Data tidak ditemukan'}), 400

        # Ambil fitur sesuai urutan model
        features = list(model.feature_names_in_)
        print(f"Features model: {features}")
        print(f"Data diterima : {data}")

        input_values = [float(data.get(f, 0)) for f in features]
        input_df = pd.DataFrame([input_values], columns=features)

        probability = float(model.predict_proba(input_df)[0][1])

        # Level risiko
        if probability < 0.30:
            risk_level = 'Rendah'
        elif probability < 0.50:
            risk_level = 'Sedang'
        else:
            risk_level = 'Tinggi'

        print(f"Probabilitas: {probability:.4f} → {risk_level}")

        return jsonify({
            'success'    : True,
            'probability': probability,
            'risk_level' : risk_level,
            'threshold'  : THRESHOLD
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status'      : 'healthy',
        'model_loaded': model is not None,
        'features'    : list(model.feature_names_in_) if model else [],
        'threshold'   : THRESHOLD
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Diabetes Prediction System")
    print("http://localhost:5000")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=5000)