from datetime import date
from datetime import timedelta
import pandas as pd
from google_sheet_handler import Google_sheet_handler
import logger_hander

class ReTrain_bot:

    # initialize RASA API
    def __init__(self):
        pass

    def fetch_data(self, google_sheet, yesterday):
        """
            This function will Fetch data of specific date from google sheet & return converted list.
            :param google_sheet: Original google_sheet, yesterday: date
            :return: data columns in list
        """
        list_of_records = google_sheet.get_all_records()

        Question_list = []
        Email_id_list = []
        Bot1_intent_list = []
        bot2_intent_list = []
        Actual_intent_must_be = []
        Bot1_Result_List = []
        Bot2_Result_List = []

        for records in list_of_records:
            if ( records.get('Date') == yesterday and records.get('Question_is_proper_or_not') == "Right" and records.get('Bot1_Result') == "Wrong" ):
                question = records.get('Question')
                email_id = records.get('Email')
                Bot1_intent = records.get('BOT1_Intent')
                Bot2_intent = records.get('BOT2_Intent')
                Actual_intent = records.get('Actual_intent_must_be')
                Bot1_Result = records.get('Bot1_Result')
                Bot2_Result = records.get('Bot2_Result')

                Question_list.append(question)
                Email_id_list.append(email_id)
                Bot1_intent_list.append(Bot1_intent)
                bot2_intent_list.append(Bot2_intent)
                Actual_intent_must_be.append(Actual_intent)
                Bot1_Result_List.append(Bot1_Result)
                Bot2_Result_List.append(Bot2_Result)

        logger.info("Data fetched from existing sheet Successfully..!")
        return Email_id_list, Question_list, Bot1_intent_list, bot2_intent_list, Actual_intent_must_be, Bot1_Result_List, Bot2_Result_List

    def find_yesterday_date(self):
        """
            This function will find yesterday date
            :param null
            :return: yesterday date in specific format
        """
        today = date.today()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime('%b %d, %Y')
        return yesterday

    def check_cell_name_valid_or_not(self, sheet, List_cell_name):
        return Google_sheet_handler.find_cell(self, sheet, List_cell_name)

if __name__ == "__main__":

    # create instances
    retrain_obj = ReTrain_bot()
    sheet_handler = Google_sheet_handler()
    logger = logger_hander.set_logger()

    # get google sheet
    sheet = sheet_handler.call_sheet("Chatbot_Daily_Report","BL_BOT_Compare")
    if sheet != 'WorksheetNotFound':
        yesterday = retrain_obj.find_yesterday_date()
        yesterday = "Sep 13, 2020"
        print(yesterday)
        List_of_cell_name = ['Date','Email','Question','BOT1_Intent','BOT2_Intent','Question_is_proper_or_not', 'Actual_intent_must_be', 'Bot1_Result', 'Bot2_Result']

        # check cell name is valid or not
        flag = retrain_obj.check_cell_name_valid_or_not(sheet,List_of_cell_name)
        if flag:
            Email_id_list, Question_list, Bot1_intent_list, bot2_intent_list, Actual_intent_must_be, Bot1_Result_List, Bot2_Result_List = retrain_obj.fetch_data(sheet,yesterday)
            if len(Question_list) == 0:
                logger.info("No interaction happened in yesterday.")
            else:
                dict = {'Date': yesterday, 'Email': Email_id_list, 'Questions': Question_list, 'bot1_intent': Bot1_intent_list,
                     'bot2_intent': bot2_intent_list, 'Actual_intent_must_be': Actual_intent_must_be, 'Bot1_Result_List': Bot1_Result_List, 'Bot2_Result_List': Bot2_Result_List }
                dataframe = pd.DataFrame(dict)
                print(dataframe)
                df_list_value = dataframe.values.tolist()

                # get google sheet to store result
                created_sheet = sheet_handler.call_sheet("Chatbot_Daily_Report", "Sheet12")
                if created_sheet != 'WorksheetNotFound':
                    output = sheet_handler.save_output_into_sheet(created_sheet, df_list_value)
                    if output == True:
                        logger.info(" Sheet Updated Successfully...!!!")
                    else:
                        logger.error(" Something went wrong while Updating sheet ")
