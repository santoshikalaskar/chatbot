import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests
import json
import pandas as pd

class Rasa_Test:
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.url = 'http://localhost:5005/webhooks/rest/webhook'

    # Sample Method
    def call_sheet(self,sheet_name,worksheet_name):
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
        self.sheet = self.client.open(self.sheet_name).worksheet(self.worksheet_name)
        return self.sheet

    def fetch_data(self, sheet):
        self.google_sheet = sheet
        list_of_records = self.google_sheet.get_all_records()
        Question_list = []
        self.todays_date = datetime.today().strftime('%b %d, %Y')
        print(self.todays_date)
        self.todays_date = "Aug 20, 2020"
        for records in list_of_records:
            if records.get('Date') == self.todays_date:
                question = records.get('question')
                Question_list.append(question)
        return Question_list

    def call_rasa_api(self,question_list):
        Response_list = []
        print(self.url)
        for ques in question_list:
            payload = {"sender": "mee", "message": ques}
            r = requests.post(self.url, data=json.dumps(payload))
            response_return = r.json()
            Response_list.append(response_return[0].get("text"))
        print(Response_list)
        return Response_list

rasa_obj = Rasa_Test()
sheet = rasa_obj.call_sheet("Chatbot_Daily_Report","Chatbot_Daily_Report")
question_list = rasa_obj.fetch_data(sheet)
try:
    if len(question_list) != 0:
        Response_list = rasa_obj.call_rasa_api(question_list)
        d = {'Questions': question_list, 'Rasa_response': Response_list}
        Rasa_dataframe = pd.DataFrame(d)
        print(Rasa_dataframe)

except:
    print("No interaction happened in today's date.")

# Append Rows Example
# report_line = ['ok', 'ok', 'ok', 'ok','ok','ok','ok']
# sheet.append_row(report_line)