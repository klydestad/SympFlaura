import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

DATA_PATH = "data/sample_symptoms.csv"

st.set_page_config(page_title="SympFlaura", layout="centered")

st.title("SympFlaura: Symptom Tracker")

# Load existing data
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

# Plot symptom history
st.subheader("📈 Symptom Timeline")
fig = px.line(df, x="date", y=["fatigue", "pain", "brain_fog"], markers=True)
st.plotly_chart(fig)

# Log new entry
st.subheader("📝 Log Today’s Symptoms")

with st.form("log_form"):
    fatigue = st.slider("Fatigue", 0, 10, 5)
    pain = st.slider("Pain", 0, 10, 5)
    brain_fog = st.slider("Brain Fog", 0, 10, 5)
    submitted = st.form_submit_button("Submit")

    if submitted:
        new_entry = {
            "date": datetime.now().date(),
            "fatigue": fatigue,
            "pain": pain,
            "brain_fog": brain_fog,
            "flare": None
        }

    # Send to Flask API for prediction
        try:
            response = requests.post(
                "http://127.0.0.1:5000/predict",
                json={
                    "fatigue": fatigue,
                    "pain": pain,
                    "brain_fog": brain_fog
                }
            )
            result = response.json().get("prediction", "unknown")
            new_entry["flare"] = result
            st.success(f"Entry logged! Flare-up risk: **{result.upper()}**")

        except Exception as e:
            result = "unknown"
            st.warning(f"Could not get prediction. Error: {e}")
            st.info("The entry was saved, but no risk level was added.")

        # Append to CSV
        new_df = pd.DataFrame([new_entry])
        new_df.to_csv(DATA_PATH, mode='a', header=False, index=False, lineterminator='\n')

