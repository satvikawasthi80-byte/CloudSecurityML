import pandas as pd
import joblib

# Load trained model
model = joblib.load("model/anomaly_model.pkl")

# Load dataset
data = pd.read_csv("dataset/logs.csv")

# Predict anomalies
predictions = model.predict(data)

# Add prediction column
data["Prediction"] = predictions

# Convert values
data["Prediction"] = data["Prediction"].replace({
    1: "Normal",
    -1: "Anomaly"
})

print(data)