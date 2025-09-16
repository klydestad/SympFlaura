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

from app import pred_result

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


if not st.session_state.get('authentication_status'):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)
    
    with col2:
        st.markdown("**Demo Account Credentials:**")
        st.markdown("*Copy and paste into login!*")
        st.info("user")
        st.info("sympflaura123")
else:
    # Just do login attempt if already authenticated
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
        #st.stop()

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
                result = pred_result(fatigue, pain, brain_fog)
                new_entry["flare"] = result
                st.success(f"Entry logged! Flare-up risk: **{result.upper()}**")
            except Exception as e:
                st.warning(f"Could not get prediction. Error: {e}")
                new_entry["flare"] = "unknown"

            pd.DataFrame([new_entry]).to_csv(user_data_path, mode='a', header=False, index=False, lineterminator='\n')
            
             # Store the prediction in session state to show until next entry
            st.session_state['last_prediction'] = result
            st.session_state['show_prediction'] = True
            st.rerun()

    # Show prediction message if exists
    if st.session_state.get('show_prediction', False):
        result = st.session_state.get('last_prediction', 'unknown')
        st.info(f"🔮 **Last Prediction:** Flare-up risk is **{result.upper()}**")
        
    

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
        # with col4:
        #     flare_risk = today_row['flare'] if pd.notna(today_row['flare']) else "unknown"
        #     st.metric("⚡ Flare Risk Level", flare_risk.title())
        
      # ------------------- FLARE RISK PREDICTIONS -------------------
    st.subheader("🔮 Flare Risk Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Today's Risk**")
        
        # Get today's data for averaging
        today_entries = df[df['date'].dt.date == today]
        
        if not today_entries.empty:
            # Average of today's symptoms
            avg_fatigue = today_entries['fatigue'].mean()
            avg_pain = today_entries['pain'].mean()
            avg_brain_fog = today_entries['brain_fog'].mean()
            
            # Get ML prediction based on today's averages
            try:
                avg_prediction = pred_result(avg_fatigue, avg_pain, avg_brain_fog)
                st.info(f"Based on today's avg symptoms: **{avg_prediction.upper()}**")
            except:
                st.info("Based on today's avg symptoms: **UNKNOWN**")
        else:
            st.info("No entries for today yet")
            
        # Show last individual prediction if available
        if st.session_state.get('show_prediction', False):
            last_pred = st.session_state.get('last_prediction', 'unknown')
            st.info(f"Last individual entry: **{last_pred.upper()}**")
    
    with col2:
        st.write("**Next 7 Days Risk**")
        
        if len(df) >= 3:  # Need some historical data
            # Use recent symptom trends to predict 7-day risk
            recent_data = df.tail(7)  # Last 7 entries
            
            # Calculate trend in symptoms
            recent_avg_fatigue = recent_data['fatigue'].mean()
            recent_avg_pain = recent_data['pain'].mean()
            recent_avg_brain_fog = recent_data['brain_fog'].mean()
            
            # Simulate slight symptom progression for 7-day forecast
            future_fatigue = min(10, recent_avg_fatigue * 1.1)  # Slight increase
            future_pain = min(10, recent_avg_pain * 1.05)
            future_brain_fog = min(10, recent_avg_brain_fog * 1.08)
            
            try:
                seven_day_prediction = pred_result(future_fatigue, future_pain, future_brain_fog)
                
                # Additional context based on recent flare history
                recent_flares = recent_data['flare'].dropna()
                high_risk_count = sum(1 for flare in recent_flares if 'high' in str(flare).lower())
                
                if high_risk_count >= 2:
                    risk_context = "⚠️ Recent high-risk pattern detected"
                elif high_risk_count >= 1:
                    risk_context = "⚡ Some recent elevated risk"
                else:
                    risk_context = "✅ Recent patterns look stable"
                
                st.info(f"Trend-based forecast: **{seven_day_prediction.upper()}**")
                st.caption(risk_context)
                
            except:
                st.info("Unable to generate 7-day forecast")
        else:
            st.info("Need more data for 7-day forecast")
            
            
  # ------------------- 7-DAY ROLLING SYMPTOM AVERAGES ------------------- 
    st.subheader("📈 7-Day Rolling Symptom Averages")
    if len(df) >= 7:  # Need some historical data
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
    else:
            st.info("Need more data for 7-day forecast")
            
    # ------------------- SYMPTOM TIMELINE -------------------          
    st.subheader("\U0001F4C8 Symptom Timeline")
    fig = px.line(df, x="date", y=["fatigue", "pain", "brain_fog"], markers=True)
    st.plotly_chart(fig)   
        
    # # ------------------- WEEKLY FLARE COUNT -------------------
    # st.subheader("Weekly Flare Count")
    # weekly_flares = df.groupby("week")["flare"].count().reset_index() 
    # fig3 = px.bar(weekly_flares, x="week", y="flare", labels={"flare": "Flare Count", "week": "Week"},
    #                 title="Number of Entries per Week")
    # st.plotly_chart(fig3)

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