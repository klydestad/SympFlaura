
# Process
This document serves to 
- Capture step by step the initial setup & improvements (minus commit comments).
- Keep track of next steps, minor improvements, order of adding features
- Instructions on setup (e.g. commands to run backend etc)


## NEXT STEPS:
- Branding/UX
- Add auth (user accounts)
- Web scraping investigation as step
    - (Replace sample data with ...)

# Misc. Todo
- Construct proper readme format when done

# Table of Contents
1. Initial Setup Process
2. ML Component
3. Analytics Dashboards


## 1. Initial Setup Process

### 1. Setup
- (Created folders, files, intial framework)


### 2.  Run & Install
- Python environment setup: 
    - python3 -m venv venv 
    - source venv/bin/activate

- Install: 
    - pip install flask pandas

- Run: 
    - cd backend
    - python app.py

- create gitignore for venv


### 3.  Testing connection works
- NEW TERMINAL TO TEST API:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"fatigue": 7, "pain": 6, "brain_fog": 5}'

- Should yield: 
    - {"prediction":"high risk"}


#### 4. Streamlit API add
- Install necessary stuff: pip install streamlit plotly pandas
- Run: streamlit run streamlit_app.py

- Add an entry to the streamlit, refresh page, see graphs update/see sample_symptoms.csv update too

### 5. Flask API add
- Install: pip install requests
- Update streamlit file: import requests 

- Run:   
    - Terminal 1: cd backend python3 app.py
    - Terminal 2: streamlit run streamlit_app.py


### Recap so far

| Tool         | Running Command                  | Purpose                       |
| ------------ | -------------------------------- | ----------------------------- |
| Flask API | `cd backend && python3 app.py`   | Runs your `/predict` endpoint |
| Streamlit | `streamlit run streamlit_app.py` | Opens the SympFlaura frontend |



## 2. ML Component: Sample data
### 1. Setup
    - create folder/notebook
    - pip install scikit-learn joblib
    - sample data added

## 3. Analytics Dashboards
### 1. Setup
    - pip install seaborn



## 4. Deploy Streamlit App Online
### 1. Setup
    - added requirements.txt: pip freeze > requirements.txt, ensure necessary packages there
    - Link: https://sympflaura.streamlit.app/ 

