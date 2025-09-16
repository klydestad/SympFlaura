import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
from yaml.loader import SafeLoader


import sys
import os
sys.path.append('backend')
from app import predict

# Page config
st.set_page_config(page_title="SympFlaura", layout="centered")


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


# hashed_passwords = stauth.Hasher(['sympflaura123'])
# print(hashed_passwords)


# authenticator = stauth.Authenticate(
#     credentials=credentials,
#     cookie_name='sympflaura_cookie',
#     key='sympflaura_key',
#     cookie_expiry_days=1
# )


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status'):
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{st.session_state.get("name")}*')
    
    username = st.session_state["username"]
    st.write(f"You are logged in as: {username}")
    user_data_path = f"data/{username}_symptoms.csv"
    
    
# with open('./config.yaml', 'w') as file:
#     yaml.dump(config, file, default_flow_style=False, allow_unicode=True)    


# username = st.session_state["username"]
# st.write(f"You are logged in as: {username}")
# user_data_path = f"data/{username}_symptoms.csv"
  
# auth_status = authenticator.login(location='main')

# if auth_status is False:
#     st.error("Username/password is incorrect")
# elif auth_status is None:
#     st.warning("Please enter your username and password")
# elif auth_status:
#     authenticator.logout("Logout", "sidebar")
#     st.sidebar.success(f"Logged in as {authenticator.name}")

#     username = authenticator.username
#     user_data_path = f"data/{username}_symptoms.csv"
#     st.title("SympFlaura: Symptom Tracker")
    
    
    
    

    # ------------------- LOAD DATA -------------------
    try:
        df = pd.read_csv(user_data_path, parse_dates=["date"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "fatigue", "pain", "brain_fog", "flare"])
        df.to_csv(user_data_path, index=False)

    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.to_period("W").astype(str)
    
    if df.empty:
        st.info("No symptoms logged yet. Use the form below to get started!")
        st.stop()

    # ------------------- NEW ENTRY FORM -------------------
    st.subheader("\U0001F4DD Log Today's Symptoms")
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

            try:
                result = predict(fatigue, pain, brain_fog)
                new_entry["flare"] = result
                st.success(f"Entry logged! Flare-up risk: **{result.upper()}**")
            except Exception as e:
                st.warning(f"Could not get prediction. Error: {e}")
                new_entry["flare"] = "unknown"

            pd.DataFrame([new_entry]).to_csv(user_data_path, mode='a', header=False, index=False, lineterminator='\n')
            st.rerun()

    # ------------------- DAILY SYMPTOMS AVERAGES -------------------
    st.subheader("Daily Symptoms Average")
    daily_symptoms = df.groupby(df['date'].dt.date).agg({
    'fatigue': 'mean',
    'pain': 'mean', 
    'brain_fog': 'mean',
    'flare': 'first'
    }).reset_index()
    daily_symptoms.columns = ['date', 'fatigue', 'pain', 'brain_fog', 'flare']
    
    today = datetime.now().date()
    today_data = daily_symptoms[daily_symptoms['date'] == today]
    # Today's Summary
    if not today_data.empty:
        st.subheader(f"Today's Summary ({today})")
        today_row = today_data.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Fatigue", f"{today_row['fatigue']:.1f}/10")
        with col2:
            st.metric("Pain", f"{today_row['pain']:.1f}/10")
        with col3:
            st.metric("Brain Fog", f"{today_row['brain_fog']:.1f}/10")
        with col4:
            import pandas as pd
            flare_risk = today_row['flare'] if pd.notna(today_row['flare']) else "unknown"
            st.metric("⚡ Flare Risk Level", flare_risk.title())

    st.subheader("📈 7-Day Rolling Symptom Averages")
    rolling_df = df.copy()
    rolling_df["rolling_fatigue"] = rolling_df["fatigue"].rolling(7, min_periods=1).mean()
    rolling_df["rolling_pain"] = rolling_df["pain"].rolling(7, min_periods=1).mean()
    rolling_df["rolling_brain_fog"] = rolling_df["brain_fog"].rolling(7, min_periods=1).mean()

    # Get current 7-day averages (most recent values)
    current_fatigue = rolling_df["rolling_fatigue"].iloc[-1]
    current_pain = rolling_df["rolling_pain"].iloc[-1]
    current_brain_fog = rolling_df["rolling_brain_fog"].iloc[-1]

    # Display current averages
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current 7-Day Avg Fatigue", f"{current_fatigue:.1f}")
    with col2:
        st.metric("Current 7-Day Avg Pain", f"{current_pain:.1f}")
    with col3:
        st.metric("Current 7-Day Avg Brain Fog", f"{current_brain_fog:.1f}")        
        
    # ------------------- SYMPTOM TIMELINE -------------------          
    st.subheader("\U0001F4C8 Symptom Timeline")
    fig = px.line(df, x="date", y=["fatigue", "pain", "brain_fog"], markers=True)
    st.plotly_chart(fig)   
        
    # ------------------- WEEKLY FLARE COUNT -------------------
    st.subheader("Weekly Flare Count")
    weekly_flares = df.groupby("week")["flare"].count().reset_index() 
    fig3 = px.bar(weekly_flares, x="week", y="flare", labels={"flare": "Flare Count", "week": "Week"},
                    title="Number of Entries per Week")
    st.plotly_chart(fig3)

    # ------------------- SYMPTOM CORRELATION HEATMAP -------------------
    st.subheader("Symptom Correlation Heatmap")
    corr = df[["fatigue", "pain", "brain_fog"]].corr()
    fig4, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig4)


elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')