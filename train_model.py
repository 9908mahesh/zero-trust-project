import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from joblib import dump
import os

# Define feature columns
FEATURES = [
    'geo_deviation_km',
    'historical_risk_score',
    'login_time_is_abnormal', # 1=Abnormal (e.g., 3am), 0=Normal
    'device_is_consistent'    # 0=Inconsistent (New Device), 1=Consistent
]

def generate_synthetic_data(n_samples=1000, contamination=0.1):
    """Generates synthetic behavioral login data for model training."""
    
    # 1. Generate normal (low-risk) data points
    n_normal = int(n_samples * (1 - contamination))
    normal_data = pd.DataFrame({
        'geo_deviation_km': np.random.normal(loc=10, scale=20, size=n_normal), # Low deviation (10km avg)
        'historical_risk_score': np.random.uniform(low=0.7, high=1.0, size=n_normal), # High risk score (low risk)
        'login_time_is_abnormal': np.random.choice([0, 0, 0, 1], size=n_normal), # Mostly normal time
        'device_is_consistent': np.random.choice([1, 1, 1, 0], size=n_normal) # Mostly consistent device
    })
    
    # Ensure geo deviation is not negative
    normal_data['geo_deviation_km'] = normal_data['geo_deviation_km'].apply(lambda x: max(0, x))

    # 2. Generate anomalous (high-risk) data points
    n_anomaly = int(n_samples * contamination)
    anomaly_data = pd.DataFrame({
        'geo_deviation_km': np.random.uniform(low=1000, high=15000, size=n_anomaly), # High deviation (long distance)
        'historical_risk_score': np.random.uniform(low=0.01, high=0.4, size=n_anomaly), # Low risk score (high risk)
        'login_time_is_abnormal': np.random.choice([1, 1, 1, 0], size=n_anomaly), # Mostly abnormal time
        'device_is_consistent': np.random.choice([0, 0, 1], size=n_anomaly) # Mostly inconsistent device
    })
    
    # Combine data
    data = pd.concat([normal_data, anomaly_data], ignore_index=True)
    return data[FEATURES]

def train_and_save_model(data, model_path='isolation_forest_model.joblib'):
    """Trains the Isolation Forest model and saves it."""
    
    print("Starting model training...")
    
    # Isolation Forest is an unsupervised anomaly detection model.
    # It attempts to "isolate" outliers based on random sub-sampling.
    # The 'contamination' parameter estimates the proportion of outliers in the data.
    model = IsolationForest(
        contamination=0.1, 
        random_state=42, 
        n_estimators=100
    )
    
    # Train the model
    model.fit(data)
    
    # Save the model to disk
    dump(model, model_path)
    
    print(f"Model trained successfully and saved to: {model_path}")
    
    # Quick check for model functionality
    # Prediction: -1 for anomalies (suspicious), 1 for inliers (legitimate)
    sample_legit = data.iloc[[0]] 
    sample_suspicious = pd.DataFrame({
        'geo_deviation_km': [10000.0],
        'historical_risk_score': [0.1],
        'login_time_is_abnormal': [1],
        'device_is_consistent': [0]
    })
    
    print("\nModel Test:")
    print(f"Legitimate Sample Prediction (-1=Suspicious, 1=Legitimate): {model.predict(sample_legit)}")
    print(f"Suspicious Sample Prediction (-1=Suspicious, 1=Legitimate): {model.predict(sample_suspicious)}")


if __name__ == '__main__':
    # Ensure the model directory exists if needed, though typically it's saved in the root/app directory
    
    synthetic_data = generate_synthetic_data(n_samples=5000, contamination=0.05)
    train_and_save_model(synthetic_data)
