import requests
url = 'http://localhost:5005/webhooks/rest/webhook'
payload = {"sender":"mee","message": "what is codincub?"}

import json
r = requests.post(url, data=json.dumps(payload))

# Response, status etc
print(r.text)
print(r.status_code)

data = r.json()
print(data[0].get("text"))

# using curl command in terminal
# curl -XPOST -d '{"message":"hello","sender":"me"}' 'http://localhost:5005/webhooks/rest/webhook'

# run rasa project 
# rasa run --enable-api --debug --cors "*"
