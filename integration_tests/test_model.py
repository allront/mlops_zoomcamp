import json
import requests


def integration_test():
    '''
    Test a model.pkl from src/prediction_service/predict.py
    raise an AssertionError if the prediction isn't correct
    Hint: it starts by a different dockerfile located in current directory
    ''' 

    row = {
            "age":41,
            "job":"services",
            "marital":"married",
            "education":"unknown",
            "default":"no",
            "balance":88,
            "housing":"yes",
            "loan":"no",
            "contact":"cellular",
            "day":11,
            "month":"may",
            "campaign":1,
            "pdays":336,
            "previous":2,
            "poutcome":"failure"
            }
            
    URL = "http://localhost:9696/predict"
    response = requests.post(URL, json=row)

    actual_response = response.json()
    print(actual_response, "integration test has been past")

    expected_response = {'response-prediction': 0.0}
    assert expected_response == actual_response

if __name__=='__main__':
    integration_test()
