import pandas as pd
import joblib

# Load the trained model once
model = joblib.load("flare_model.pkl")

def predict_flare(df):
    features = df[["fatigue", "pain", "brain_fog"]]
    prediction = model.predict(features)[0]
    mapping = {0: "low risk", 1: "medium risk", 2: "high risk"}
    return mapping.get(prediction, "unknown")