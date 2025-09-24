from flask import Flask, request, jsonify, render_template
from joblib import load
import pandas as pd
import os

# The model file should be in the same directory as this script.
MODEL_PATH = 'zero_trust_model.joblib'

# Load the trained model when the app starts
try:
    model = load(MODEL_PATH)
except FileNotFoundError:
    # This will help with debugging in case the file is not found
    print(f"Error: Model file '{MODEL_PATH}' not found. Ensure it's in the same directory.")
    model = None

app = Flask(__name__)

@app.route('/')
def home():
    """
    Renders the main web page for the demo.
    """
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """
    Receives user data from the front end and uses the trained
    model to predict if the activity is legitimate.
    """
    if model is None:
        return jsonify({"status": "Error", "message": "Model not loaded. Please contact the administrator."})

    try:
        data = request.json
        
        # Prepare the data for prediction in a pandas DataFrame
        new_user_data = pd.DataFrame([data])
        
        # Predict the trust score (1 for legitimate, 0 for suspicious)
        prediction = model.predict(new_user_data)
        
        if prediction[0] == 1:
            return jsonify({"status": "Success", "message": "Access Granted: User is legitimate."})
        else:
            return jsonify({"status": "Suspicious", "message": "Access Denied: Suspicious activity detected."})
            
    except Exception as e:
        # Handle potential errors gracefully
        return jsonify({"status": "Error", "message": f"An error occurred: {str(e)}"})
