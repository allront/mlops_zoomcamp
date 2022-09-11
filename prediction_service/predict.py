import pickle
import pandas as pd
from flask import Flask, request, jsonify

# load model score code with picke
with open('modelv2.pkl', 'rb') as f_in:
    (model) = pickle.load(f_in)

# define prediction function
def predict(model, object):
    y_pred = model.predict(object)
    return int(y_pred[0])

app = Flask("prediction")

#defining endpoint
@app.route('/predict', methods=['POST'])
def response_prediction():
    object = request.get_json()

    pred = predict(model, pd.json_normalize(object))

    result = {
        'responce-prediction': pred
    }

    return jsonify(result)

#run the web service
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
