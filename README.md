# SympFlaura

## Link:
https://sympflaura.streamlit.app/

## Project Overview
Symptom tracker &amp; flare prediction applet(?) for users with chronic illnesses
* Uses machine learning to track and forecast risk of chronic illness flare (low, medium, or high) based off of the severity of different symptoms
* Model based off of whether or not user experienced a flareup that day given symptoms
* Allows users to login, input new entries, then get instant feedback on results

## Motivation
* Symptom tracking for chronic illnesses to predict illness flareups often are not tailored towards patients who experience a wide variety of potentially relevant vs. not relevant symptoms
* Pre-existing flaretracking/forecasting is often simple, with pre-existing symptoms to select from, which are predicted independently of one another
* The goal of this tool is to fill in the gaps by both providing tracking of historic symptoms, predicting flareups so that a patient can prepare, and a providing a more in-depth analysis of the relationships between different symptoms to improve accuracy of predictions

## Features
* Deployable streamlit link with an easy to use UI
* Analytics dashboard: daily averages, flare risk analytics, symptoms over time, symptom correlation heatmap, etc
* User input section (rating symptom severity on a scale of 1 to 10) with instant prediction feedback
* User authentication and login

## Technical Details
* Languages: Python
* Libraries: scikit-learn, pandas
* APIs: Streamlit, Flask
* Environment: VS Code
* Key concepts: Machine learning, classification, user interface, data persistence (user accounts)







