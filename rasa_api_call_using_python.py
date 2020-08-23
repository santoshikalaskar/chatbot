# import requests
# url = 'http://localhost:5005/webhooks/rest/webhook'
# payload = {"sender":"mee","message": "what is codincub?"}

# import json
# r = requests.post(url, data=json.dumps(payload))

# Response, status etc
# print(r.text)
# print(r.status_code)

# data = r.json()
# print(data[0].get("text"))

# using curl command in terminal
# curl -XPOST -d '{"message":"hello","sender":"me"}' 'http://localhost:5005/webhooks/rest/webhook'

# run rasa project 
# rasa run --enable-api --debug --cors "*"

import requests
import json
import pandas as pd

url = 'http://localhost:5005/webhooks/rest/webhook'
# reading csv file
dataframe = pd.read_csv("Chatbot_Daily_Report.csv")
print("<---- Dataframe Columns ---->")
print(dataframe.columns)

questions = dataframe['question']
Response_list = []
Question_list= []
for ques in questions:
    payload = {"sender":"mee","message": ques}
    r = requests.post(url, data=json.dumps(payload))
    response_return = r.json()
    Question_list.append(ques)
    Response_list.append(response_return[0].get("text"))
    #print("\n")

d = {'Questions':Question_list,'Rasa_response':Response_list}
Rasa_dataframe = pd.DataFrame(d)

Rasa_dataframe.to_csv('Rasa_output_dataframe.csv')

