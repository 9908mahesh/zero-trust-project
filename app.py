import os
from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__)

# Correctly load the model using an absolute path relative to the app's directory
MODEL_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zero_trust_model.joblib')

try:
    model = joblib.load(MODEL_FILE_PATH)
    model_loaded = True
except Exception as e:
    model_loaded = False
    print(f"Error loading the model: {e}")

@app.route('/')
def home():
    return render_template('index.html', model_loaded=model_loaded)

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'prediction': 'Model not loaded. Please contact the administrator.'})

    try:
        data = request.json
        user_id = data.get('userId')
        session_id = data.get('sessionId')
        ip_address = data.get('ipAddress')
        typing_speed = data.get('typingSpeed')
        mouse_movement = data.get('mouseMovement')
        login_time = data.get('loginTime')

        # Convert ip_address to a numerical feature (e.g., using a hash)
        # For simplicity in this example, we'll use a placeholder.
        ip_address_feature = hash(ip_address) % 1000  # Simple hash to integer

        # Prepare the features for the model
        features = [
            typing_speed,
            mouse_movement,
            login_time,
            ip_address_feature
        ]
        
        # Reshape the data for prediction. The model expects a 2D array.
        features_np = np.array(features).reshape(1, -1)

        # Make a prediction
        prediction_proba = model.predict_proba(features_np)[0]
        prediction_class = model.predict(features_np)[0]

        # The model returns a probability of belonging to each class.
        # We assume 0 is "legitimate" and 1 is "suspicious".
        result = "Legitimate" if prediction_class == 0 else "Suspicious"

        response = {
            'prediction': result,
            'probability_legitimate': float(prediction_proba[0]),
            'probability_suspicious': float(prediction_proba[1])
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
