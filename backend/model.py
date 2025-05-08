import pandas as pd
import joblib

# Load the trained model once
model = joblib.load("flare_model.pkl")

def predict_flare(df):
    features = df[["fatigue", "pain", "brain_fog"]]
    prediction = model.predict(features)[0]
    return "high risk" if prediction == 1 else "low risk"