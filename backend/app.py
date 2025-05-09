from flask import Flask, request, jsonify
import pandas as pd
from model import predict_flare

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    prediction = predict_flare(df)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)


