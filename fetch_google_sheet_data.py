import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests
import json
import pandas as pd
import gspread_dataframe as gd

class Rasa_Test:
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.url = 'http://localhost:5005/webhooks/rest/webhook'

    def call_sheet(self,sheet_name,worksheet_name):
        self.sheet = self.client.open(sheet_name).worksheet(worksheet_name)
        return self.sheet

    def fetch_data(self, google_sheet, todays_date):
        list_of_records = google_sheet.get_all_records()
        Question_list = []
        for records in list_of_records:
            if records.get('Date') == todays_date:
                question = records.get('question')
                Question_list.append(question)
        return Question_list

    def call_rasa_api(self,question_list):
        Response_list = []
        try:
            print(self.url)
            for ques in question_list:
                payload = {"sender": "mee", "message": ques}
                r = requests.post(self.url, data=json.dumps(payload))
                response_return = r.json()
                Response_list.append(response_return[0].get("text"))
            return Response_list
        except:
            print("Rasa API connection issue...!")

    def save_output_into_sheet(self,worksheet,df_list):
        existing_df = gd.get_as_dataframe(worksheet)
        #print("Existing DF"+ existing_df)
        try:
            for row in df_list:
                worksheet.append_row(row)
            return True
        except:
            print("something went wrong while updating google sheet..!")

rasa_obj = Rasa_Test()
sheet = rasa_obj.call_sheet("Chatbot_Daily_Report","Chatbot_Daily_Report")
todays_date = datetime.today().strftime('%b %d, %Y')
todays_date = "Aug 20, 2020"
question_list = rasa_obj.fetch_data(sheet,todays_date)
try:
    if len(question_list) != 0:
        Response_list = rasa_obj.call_rasa_api(question_list)
        d = {'Date':todays_date,'Questions': question_list, 'Rasa_output': Response_list}
        Rasa_dataframe = pd.DataFrame(d)
        df_list_value = Rasa_dataframe.values.tolist()
        created_sheet = rasa_obj.call_sheet("Chatbot_Daily_Report","Rasa_chatbot_output")
        output = rasa_obj.save_output_into_sheet(created_sheet,df_list_value)
        if output == True:
            print("Added today's data successfully...!!!")
except:
    print("No interaction happened in today's date.")
