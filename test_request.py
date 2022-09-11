import requests

object = {
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

url = 'http://localhost:9696/predict'
response = requests.post(url, json=object)
print(response.json())