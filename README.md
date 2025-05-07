# Sympflaura
Symptom tracker &amp; prediction


Process:

1. Setup
- Created folders, files, intial framework


2.  Run & Install
NOTES: 
python3 -m venv venv
source venv/bin/activate

INSTALL:
pip install flask pandas

RUN: 
cd backend
python app.py


3.  Testing connection works
NEW TERMINAL TO TEST API:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"fatigue": 7, "pain": 6, "brain_fog": 5}'

  should yield 
  
  {"prediction":"high risk"}
