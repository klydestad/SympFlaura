import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


# auth code
# Temporary login users (replace with Firebase or hashed creds later)
names = ['Kiersten']
usernames = ['kiki']
passwords = ['sympflaura123']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'sympflaura_cookie',
    'sympflaura_key',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
if authentication_status == None:
    st.warning('Please enter your username and password')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f"Logged in as {name}")

    user_data_path = f"data/{username}_symptoms.csv"
    st.set_page_config(page_title="SympFlaura", layout="centered")
    st.title("SympFlaura: Symptom Tracker")

    # Load existing data (create if doesn't exist)
    try:
        df = pd.read_csv(user_data_path, parse_dates=["date"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "fatigue", "pain", "brain_fog", "flare"])
        df.to_csv(user_data_path, index=False)
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.to_period("W").astype(str)

    # Plot symptom history
    st.subheader("📈 Symptom Timeline")
    fig = px.line(df, x="date", y=["fatigue", "pain", "brain_fog"], markers=True)
    st.plotly_chart(fig)

    # Log new entry
    st.subheader("📝 Log Today's Symptoms")

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
            new_df.to_csv(user_data_path, mode='a', header=False, index=False, lineterminator='\n')


    st.subheader("7-Day Rolling Symptom Averages")

    rolling_df = df.copy()
    rolling_df["rolling_fatigue"] = rolling_df["fatigue"].rolling(7).mean()
    rolling_df["rolling_pain"] = rolling_df["pain"].rolling(7).mean()
    rolling_df["rolling_brain_fog"] = rolling_df["brain_fog"].rolling(7).mean()

    fig2 = px.line(
        rolling_df,
        x="date",
        y=["rolling_fatigue", "rolling_pain", "rolling_brain_fog"],
        labels={"value": "Symptom Score"},
        title="7-Day Rolling Averages"
    )
    st.plotly_chart(fig2)






    st.subheader("Weekly Flare Count")

    df["week"] = df["date"].dt.to_period("W").astype(str)
    weekly_flares = df.groupby("week")["flare"].sum().reset_index()

    fig3 = px.bar(
        weekly_flares,
        x="week",
        y="flare",
        labels={"flare": "Flare Count", "week": "Week"},
        title="Number of Flares per Week"
    )
    st.plotly_chart(fig3)





    st.subheader("Symptom Correlation Heatmap")

    corr = df[["fatigue", "pain", "brain_fog"]].corr()

    fig4, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig4)