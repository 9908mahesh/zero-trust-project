import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump

def generate_data():
    """
    Generates a synthetic dataset for training the zero trust model.
    The data includes features like typing speed, mouse movement, and
    whether the user's location has changed.
    """
    data = {
        # Normal distribution for typing speed, average 50 wpm
        'typing_speed': np.random.normal(50, 10, 2000),  
        # Normal distribution for mouse movement, lower value means smoother movement
        'mouse_movement': np.random.normal(0.5, 0.2, 2000), 
        # Uniform distribution for time between logins
        'login_time_diff': np.random.uniform(1, 5, 2000), 
        # 5% chance of a location change (simulates an attacker)
        'location_change': np.random.choice([0, 1], 2000, p=[0.95, 0.05]),
        # 90% legitimate users, 10% suspicious
        'is_legitimate': np.random.choice([0, 1], 2000, p=[0.1, 0.9]) 
    }
    df = pd.DataFrame(data)
    
    # Introduce anomalies for the "suspicious" users (is_legitimate == 0)
    # Give them slower, more erratic typing and erratic mouse movement
    df.loc[df['is_legitimate'] == 0, 'typing_speed'] = np.random.uniform(5, 20, sum(df['is_legitimate'] == 0))
    df.loc[df['is_legitimate'] == 0, 'mouse_movement'] = np.random.uniform(0.8, 1.2, sum(df['is_legitimate'] == 0))
    
    return df

def train_and_save_model():
    """
    Trains a Random Forest Classifier on the synthetic data and saves the model.
    """
    df = generate_data()

    # Separate features (X) and target (y)
    X = df.drop('is_legitimate', axis=1)
    y = df['is_legitimate']

    # Split the data into a training set and a testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model to a file using joblib
    dump(model, 'zero_trust_model.joblib')
    print("Model trained and saved as 'zero_trust_model.joblib'")

if __name__ == '__main__':
    train_and_save_model()
