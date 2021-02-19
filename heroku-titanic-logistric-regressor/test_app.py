# sample data
import json, requests

data = {'Pclass': 3
      , 'Age': 2
      , 'SibSp': 1
      , 'Fare': 50}
data = json.dumps(data)

send_requests = requests.post('http://127.0.0.1:5342/', data)

print(send_requests.json())
