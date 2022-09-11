import json
from datetime import datetime
from time import sleep
import pyarrow as pa


import pandas as pd
import requests

table = pd.read_csv("./evidently_service/datasets/test.csv")
table.drop(['request_id'], inplace=True, axis=1)
table = pa.Table.from_pandas(table, preserve_index=False)
data  = table.to_pylist()

# sends the data to the prediction service with 1 second pause and write responce to csv file

with open("predictions.csv", 'w') as f_target:
    f_target.write(f"age,job,marital,education,default,balance,housing,loan,contact,day,month,campaign,pdays,previous,poutcome,predicion\n")
    for row in data:
        resp = requests.post("http://127.0.0.1:9696/predict", json=row)
        print(f"prediction: {resp.json()['responce-prediction']}")
        f_target.write(f"{row['age']},{row['job']},{row['marital']},{row['education']},{row['default']},{row['balance']},{row['housing']},{row['loan']},{row['contact']},{row['day']},{row['month']},{row['campaign']},{row['pdays']},{row['previous']},{row['poutcome']},{resp.json()['responce-prediction']}\n")
        sleep(1)