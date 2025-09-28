# **🛡️ AI-Powered Zero Trust Access Control**

## **Next-Generation Behavioral Anomaly Detection**

### **🔗 Live Application & Code**

| Component | Link |
| :---- | :---- |
| **Live App** | https://9908maahi.pythonanywhere.com/ |
| **Code Repository** | https://github.com/9908mahesh/zero-trust-project.git |

## **💡 Overview**

This project is a full-stack prototype demonstrating a **Zero Trust** security model powered by a custom-trained Machine Learning model. The system continuously verifies every access request by analyzing behavioral features, moving past static passwords to provide **real-time risk assessment** and **dynamic access decisions.**

**Goal:** Proactively mitigate threats from compromised accounts and insider activity by challenging or denying access to suspicious users.

### **Core Features**

* **Dynamic Challenge:** Suspicious access attempts are met with a requirement for **2-Factor Authentication \+ CAPTCHA**, enforcing the "Never Trust, Always Verify" principle.  
* **Real-time Prediction:** Uses an Isolation Forest model (an Unsupervised ML algorithm) to classify attempts as LEGITIMATE or SUSPICIOUS instantly.  
* **Interactive Scenarios:** Allows users to easily switch between low-risk and randomized high-risk input profiles for direct testing.

## **💻 Technical Stack**

| Component | Technology | Role |
| :---- | :---- | :---- |
| **Backend/API** | Python / **Flask** | Routes, API endpoint (/predict), and model serving. |
| **Machine Learning** | **Scikit-learn** (Isolation Forest) | The core anomaly detection algorithm. |
| **Data/Model** | **Pandas** / **Joblib** | Data preprocessing, synthetic data generation, and model persistence. |
| **Frontend/UI** | HTML, **JavaScript**, **Tailwind CSS** | Interactive interface for input, status, and result visualization. |
| **Deployment** | **PythonAnywhere** | Hosting environment for the full-stack application. |

## **📸 Application Screenshots**

These screenshots demonstrate the two distinct states of the AI-powered Zero Trust system in action:

| ACCESS GRANTED (Legitimate) | ACCESS DENIED (Suspicious) |
| :---- | :---- |
|  |  |

## **🧪 Usage Guide**

The application accepts four primary features to generate a prediction. You can control these features using the interface buttons and editable inputs.

### **Input Features & Impact**

| Feature Name | Description | Example of Legitimate Input | Example of Suspicious Input |
| :---- | :---- | :---- | :---- |
| **Geolocation Deviation (km)** | Distance (in km) from the user's typical login location. | 0.5 km | 8,000 km (International jump) |
| **Historical Risk Score (0.0 \- 1.0)** | A composite score based on past user behavior (1.0 is highest trust). | 0.98 | 0.12 (Indicates compromised credentials) |
| **Login Time (Is Abnormal)** | Binary flag: Is the login outside typical working hours? | Normal (Payload: 0\) | Abnormal (Payload: 1\) |
| **Device Fingerprint (Consistent)** | Binary flag: Is the session ID/device hash recognized? | Consistent (Payload: 1\) | New Session ID (Payload: 0\) |

### **Scenario Testing Flow**

1. Click **"Set Legitimate Defaults"** to load typical low-risk data.  
2. Click **"Randomize Suspicious Inputs"** to load a randomized, high-risk profile (e.g., high KM, low risk score).  
3. Click **"Run AI Prediction"** to send the current data to the Flask model for real-time scoring.

## **🛠️ Setup and Installation**

### **1\. Project Structure**

Ensure all files are arranged correctly for Flask deployment:

zero-trust-project/  
├── app.py                      \# (Flask server logic)  
├── train\_model.py              \# (Model training script)  
├── requirements.txt            \# (Dependency list)  
├── isolation\_forest\_model.joblib \# (The trained model)  
└── templates/  
    └── index.html              \# (The frontend UI)

### **2\. Dependencies**

Install the required Python packages (e.g., on PythonAnywhere or locally):

pip install \-r requirements.txt

### **3\. Training the Model**

Run this script once to generate the machine learning model file (isolation\_forest\_model.joblib):

python train\_model.py

### **4\. Running Locally**

Start the Flask server from the root directory:

python app.py

Access the application at http://127.0.0.1:5000/.