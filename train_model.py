import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load dataset
data = pd.read_csv("dataset/logs.csv")

# Train Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

model.fit(data)

# Create model folder if it doesn't exist
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/anomaly_model.pkl")

print("✅ Model trained successfully!")
print("✅ Saved as model/anomaly_model.pkl")