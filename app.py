from flask import Flask, request, jsonify
import pandas as pd
from model import predict_flare

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_route():  # Changed name to avoid conflict
    data = request.json
    df = pd.DataFrame([data])
    prediction = predict_flare(df)
    return jsonify({'prediction': prediction})

def pred_result(fatigue, pain, brain_fog):
    """Direct prediction function for Streamlit"""
    data_df = pd.DataFrame([{"fatigue": fatigue, "pain": pain, "brain_fog": brain_fog}])
    return predict_flare(data_df)

if __name__ == '__main__':
    app.run(debug=True)