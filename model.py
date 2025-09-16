import pandas as pd
import joblib
import os

# Load the trained model once
model_path = os.path.join(os.path.dirname(__file__), "flare_model.pkl")
model = joblib.load(model_path)

def predict_flare(df):
    features = df[["fatigue", "pain", "brain_fog"]]
    prediction = model.predict(features)[0]
    mapping = {0: "low risk", 1: "medium risk", 2: "high risk"}
    return mapping.get(prediction, "unknown")