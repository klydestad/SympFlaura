# Sympflaura
Symptom tracker &amp; prediction

Technologies: 
(Python, Streamlit API, Flask API)


Process (Delete later):

1. Setup
- (Created folders, files, intial framework)


2.  Run & Install
- Python environment setup
    python3 -m venv venv
    source venv/bin/activate


- INSTALL:
    pip install flask pandas

- RUN: 
    cd backend
    python app.py

- create gitignore for venv


3.  Testing connection works
- NEW TERMINAL TO TEST API:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"fatigue": 7, "pain": 6, "brain_fog": 5}'

- should yield 
  {"prediction":"high risk"}


4. Streamlit API add
- Install necessary stuff: 
    pip install streamlit plotly pandas
- Run: 
    streamlit run streamlit_app.py

- Add an entry to the streamlit, refresh page, see graphs update/see sample_symptoms.csv update too

5. Flask API add
- Install
    pip install requests
- Update streamlit file: 
    import requests
    then include flask stuff


- Run:   
    - Terminal 1:
        cd backend
        python3 app.py

    - Terminal 2:
        streamlit run streamlit_app.py


