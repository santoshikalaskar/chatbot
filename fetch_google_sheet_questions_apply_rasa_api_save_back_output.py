import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import timedelta
import requests
import json
import pandas as pd
import gspread_dataframe as gd

class Rasa_Test:

    # initialize gspread details & RASA API
    def __init__(self):
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.url = 'http://localhost:5005/webhooks/rest/webhook'

    # Fetch Worksheet Object
    def call_sheet(self,sheet_name,worksheet_name):
        self.sheet = self.client.open(sheet_name).worksheet(worksheet_name)
        return self.sheet

    # Fetch required data(Questions) from that Sheet & return with Column_List
    def fetch_data(self, google_sheet, todays_date):
        print("data fetching from existing sheet.....")
        list_of_records = google_sheet.get_all_records()
        Question_list = []
        email_id_list = []
        Name_list = []
        intent_list = []
        for records in list_of_records:
            if records.get('Date') == todays_date:
                question = records.get('question')
                email_id = records.get('email_id')
                name = records.get('name')
                Question_list.append(question)
                email_id_list.append(email_id)
                Name_list.append(name)
                intent_list.append("")
        print("data fetched from existing sheet successfully..!")
        return Question_list, email_id_list, Name_list, intent_list

    # Pass question list to RASA api & get Response
    def call_rasa_api(self,question_list):
        Response_list = []
        try:
            print("Pass questions list to API.....")
            print(self.url)
            for ques in question_list:
                payload = {"sender": "mee", "message": ques}
                r = requests.post(self.url, data=json.dumps(payload))
                response_return = r.json()
                Response_list.append(response_return[0].get("text"))
            print("response of rasa for each question has done successfully..!")
            return Response_list
        except:
            print("Rasa API connection issue...!")

    # Save & Append output into Google sheet
    def save_output_into_sheet(self,worksheet,df_list):
        existing_df = gd.get_as_dataframe(worksheet)
        #print("Existing DF"+ existing_df)
        try:
            print("Output of rasa appending to the new sheet...!")
            for row in df_list:
                worksheet.append_row(row)
            print("Output response of Rasa has been appended to new sheet successfully..!")
            return True
        except:
            print("something went wrong while updating google sheet..!")

rasa_obj = Rasa_Test()
sheet = rasa_obj.call_sheet("Chatbot_Daily_Report","Chatbot_Daily_Report")
today = date.today()
yesterday = today - timedelta(days=1)
yesterday = yesterday.strftime('%b %d, %Y')
print(yesterday)
# yesterday = "Sep 01, 2020"
question_list, email_id, Name, intent_list = rasa_obj.fetch_data(sheet,yesterday)
# email_id = [item for item in sheet.col_values(3) if item]
# Name = [item for item in sheet.col_values(4) if item]
try:
    if len(question_list) != 0:
        Response_list = rasa_obj.call_rasa_api(question_list)
        d = {'Date':yesterday,'Email':email_id,'Questions': question_list,'Rasa_intent':intent_list,'Rasa_output': Response_list}
        Rasa_dataframe = pd.DataFrame(d)
        # print(Rasa_dataframe)
        df_list_value = Rasa_dataframe.values.tolist()
        created_sheet = rasa_obj.call_sheet("Chatbot_Daily_Report","BL_BOT_Compare")
        output = rasa_obj.save_output_into_sheet(created_sheet,df_list_value)
        if output == True:
            print("Added today's data successfully...!!!")
    else:
        print("Something Issue at Rasa API backend")
except:
    print("No interaction happened in today's date.")

