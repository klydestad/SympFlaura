import pandas as pd

# Placeholder prediction logic
def predict_flare(df):
    score = (df['fatigue'][0] + df['pain'][0]) / 2
    return "high risk" if score > 5 else "low risk"
