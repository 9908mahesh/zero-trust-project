🛡️ AI-Powered Zero Trust Access Control (Behavioral Anomaly Detection)
Project Overview
This is a full-stack web application prototype demonstrating a Zero Trust security model powered by Machine Learning. Instead of relying solely on static credentials, this system continuously verifies user identity by analyzing real-time behavioral features (such as geolocation deviation, login time anomaly, and device consistency).

The core function is Anomaly Detection. The system determines if a login attempt is LEGITIMATE or SUSPICIOUS in real-time, proactively mitigating risks from compromised accounts and insider threats.

Key Features
Real-time Prediction: Uses a trained Isolation Forest model to classify access requests instantly.

Scenario Testing: Allows users to input both "Legitimate" and "Suspicious" data points to see the model's decision.

Zero Trust Decision: Access is dynamically granted or denied/challenged based on the behavioral risk score.

💻 Technology Stack
Component

Technology

Role

Backend Framework

Python / Flask

Routes, API endpoint (/predict), Model serving.

Machine Learning

Scikit-learn (Isolation Forest)

Anomaly detection model for classifying behaviors.

Data Handling

Pandas / NumPy / Joblib

Data preprocessing, synthetic data generation, and model persistence.

Frontend

HTML, JavaScript, Tailwind CSS

Interactive UI for feature input, visualization, and API communication.

Deployment

PythonAnywhere

Hosting the Flask web application and serving the model.

🚀 Setup and Deployment
Prerequisites
A Python 3 environment.

A PythonAnywhere account (for deployment).

1. File Structure
Ensure your project directory has the following structure:

zero-trust-project/
├── app.py                      # Flask server application
├── train_model.py              # Script to train and save the ML model
├── requirements.txt            # Python dependencies
├── isolation_forest_model.joblib # **Trained model file (must be present)**
└── templates/
    └── index.html              # Frontend user interface


2. Model Training (Local or PythonAnywhere Console)
You must run the training script first to create the necessary model file (isolation_forest_model.joblib).

# Install dependencies first (or let PythonAnywhere handle this)
pip install -r requirements.txt

# Run the training script
python train_model.py


This script generates the synthetic dataset, trains the Isolation Forest model, and saves it as isolation_forest_model.joblib.

3. Deployment on PythonAnywhere
Upload Files: Upload all files (.py, .txt, .joblib) and the templates/ folder to your PythonAnywhere project directory.

Virtual Environment: Set up a virtual environment and install dependencies:

pip install -r requirements.txt


Web App Setup:

Navigate to the Web tab in PythonAnywhere.

Create a new web app using the Flask framework.

Configure the WSGI file to point to your app.py logic.

The Flask application (app.py) will automatically load the saved isolation_forest_model.joblib file when it starts, making the /predict endpoint available to the frontend.

🌐 Live Demo and Screenshots
The application is hosted on PythonAnywhere and available to test in real-time.

Live Application Link: https://9908maahi.pythonanywhere.com/

Below are screenshots demonstrating the two main states of the Zero Trust system:

State

Decision

Screenshot

Legitimate User

ACCESS GRANTED



Suspicious User

ACCESS DENIED - ANOMALY DETECTED



💡 How to Use the Application
The application allows you to simulate user behavior by adjusting the key input features.

Scenario Buttons:

Set Legitimate Defaults: Populates the inputs with low-risk values (e.g., small geolocation deviation, high historical risk score), resulting in an ACCESS GRANTED prediction.

Randomize Suspicious Inputs: Populates the inputs with high-risk, randomized values (e.g., massive geolocation deviation, low historical risk score), resulting in an ACCESS DENIED - ANOMALY DETECTED prediction.

Editable Inputs: You can manually adjust the values for Geolocation Deviation (km) and Historical Risk Score (0.0 - 1.0) to test nuanced scenarios.

Run AI Prediction: Click this button to send the current feature set to the Flask backend, where the Isolation Forest model returns an access decision and a confidence score.

Example Scenarios:
Scenario

Geo Deviation (km)

Risk Score (0-1)

Login Time (Abnormal)

Expected Result

Legitimate User

0.5

0.98

No (0)

ACCESS GRANTED

Compromised Account

8000.0

0.12

Yes (1)

ACCESS DENIED

Insider Threat

10.0

0.05

No (0)

ACCESS DENIED (Due to low historical score)

🧠 Model & Concept
Isolation Forest (Model)
The Isolation Forest is an unsupervised machine learning algorithm designed specifically for anomaly detection. It works by "isolating" observations rather than building profiles of normal points. Anomalies are data points that are few and different, making them easier to isolate using random partitioning. This makes it highly effective for cybersecurity threat detection, where suspicious logins are rare compared to legitimate ones.

Zero Trust (Concept)
The core security principle here is Never Trust, Always Verify. Access is not granted based on network location or initial authentication; instead, every access attempt is treated as suspicious until the user's current behavioral profile passes the AI verification.
