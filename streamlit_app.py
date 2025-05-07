import streamlit as st
import pandas as pd
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
            "flare": None  # Placeholder until ML model is used
        }
        new_df = pd.DataFrame([new_entry])
        new_df.to_csv(DATA_PATH, mode='a', header=False, index=False)
        st.success("Entry logged! Refresh the page to see it update.")

