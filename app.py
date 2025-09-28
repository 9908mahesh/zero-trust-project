from flask import Flask, request, jsonify, render_template
from joblib import load
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# --- Model Loading ---
MODEL_PATH = 'isolation_forest_model.joblib'

# Check if the model file exists
if not os.path.exists(MODEL_PATH):
    print(f"--- WARNING: Model file not found at {MODEL_PATH} ---")
    print("Please run 'python train_model.py' first to generate the model.")
    # Use a placeholder (None) and handle errors later
    model = None
else:
    try:
        # Load the trained Isolation Forest model
        model = load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

# Define the expected feature order for the model
FEATURES = [
    'geo_deviation_km',
    'historical_risk_score',
    'login_time_is_abnormal',
    'device_is_consistent'
]

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main HTML interface."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives input data via POST request, runs it through the model,
    and returns a prediction (LEGITIMATE or SUSPICIOUS) and a confidence score.
    """
    if not model:
        return jsonify({
            'prediction': 'ERROR', 
            'confidence': 0.0, 
            'error_message': 'Model not loaded on the server.'
        }), 500

    try:
        data = request.get_json()
        
        # 1. Prepare data for the model
        # Create a DataFrame in the exact order the model expects
        input_data = pd.DataFrame({k: [data.get(k)] for k in FEATURES})
        
        # Simple input validation
        if input_data.isnull().values.any():
             return jsonify({
                'prediction': 'ERROR',
                'confidence': 0.0,
                'error_message': 'Missing data fields in payload.'
            }), 400

        # 2. Make Prediction
        # Isolation Forest uses a decision_function to get a score:
        # Higher score (closer to 0 for Isolation Forest) means more 'normal'.
        # Lower score (more negative) means more 'anomalous'.
        
        # Predict: returns 1 (inlier/legitimate) or -1 (outlier/suspicious)
        prediction_result = model.predict(input_data)[0]
        
        # Decision function: raw anomaly score
        anomaly_score = model.decision_function(input_data)[0]
        
        # 3. Process Result and Calculate Confidence
        
        if prediction_result == 1:
            # LEGITIMATE
            prediction_label = 'LEGITIMATE'
            
            # Confidence: 1 minus the scaled anomaly score (closer to 1.0 is better)
            # Scaling score for a more intuitive confidence display (e.g., clamp between 0.5 and 0.99)
            confidence = 1.0 - np.clip(-anomaly_score * 0.5, 0.01, 0.5)
            
        else:
            # SUSPICIOUS (Anomaly Detected)
            prediction_label = 'SUSPICIOUS'
            
            # Confidence: Scaled anomaly score (closer to 1.0 is better)
            confidence = np.clip(-anomaly_score * 0.5, 0.5, 0.99)

        # 4. Return JSON response
        return jsonify({
            'prediction': prediction_label,
            'confidence': round(confidence, 2)
        })

    except Exception as e:
        app.logger.error(f"Prediction failed: {e}")
        return jsonify({
            'prediction': 'ERROR', 
            'confidence': 0.0, 
            'error_message': str(e)
        }), 500

if __name__ == '__main__':
    # In a production environment, you would use a proper WSGI server (like Gunicorn)
    # The debug flag is useful for development but should be False in production.
    app.run(debug=True, host='0.0.0.0', port=5000)
