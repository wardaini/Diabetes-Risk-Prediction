"""
Test Flask server - fresh implementation
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model
model = joblib.load('random_forest_tuned_model.pkl')
print(f"Model features: {list(model.feature_names_in_)}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Use model's actual features
        features = list(model.feature_names_in_)
        print(f"Using features: {features}")
        
        # Create DataFrame
        input_features = [float(data.get(f, 0)) for f in features]
        input_df = pd.DataFrame([input_features], columns=features)
        
        print(f"DataFrame:\n{input_df}")
        
        # Predict
        prob = model.predict_proba(input_df)[0][1]
        print(f"Prediction probability: {prob}")
        
        return jsonify({
            'success': True,
            'probability': float(prob),
            'features_used': features
        })
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)
