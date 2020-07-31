function sendChartbotScheduledMailReport() {
  
  // Read Sheets
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ws = ss.getSheetByName("Day_wise_summery");
  const ws2 = ss.getSheetByName("Date_wise_persion_list");
  
  // get header columns of different tables from diff workspace sheets
  const theader1 = ws.getRange("B1:E1").getValues();
  const theader2 = ws2.getRange("B1:H1").getValues();
  
  // for Day_wise_summery table headers columns
  const Date1 = theader1[0][0];
  const Number_of_Persons_Interacted = theader1[0][1];
  const Max_Num_of_queries_from_one_person = theader1[0][2];
  const Max_Time_spent_by_a_person = theader1[0][3];
  
  // for Date_wise_persion_list table headers columns
  const Date2 = theader2[0][0];
  const Email_Id = theader2[0][1];
  const Name = theader2[0][2];
  const No_of_querries = theader2[0][3];
  const Start_time = theader2[0][4];
  const End_Time = theader2[0][5];
  const Duration = theader2[0][6];
  
  // Get Last row index from diff workspace sheets
  const last_row1 = ws.getLastRow();
  const last_row2 = ws2.getLastRow();
  
  // Get actual table data from diff workspace sheets
  const TableRangeValue1 = ws.getRange(2,2,last_row1-2,4).getDisplayValues();
  const TableRangeValue2 = ws2.getRange(2,2,last_row2-2,7).getDisplayValues();
  
  // connect HTML file with script
  const htmltemplet = HtmlService.createTemplateFromFile("mail_templet");
  
  // send Day_wise_summery table data to HTML file
  htmltemplet.Date1 = Date1;
  htmltemplet.Number_of_Persons_Interacted = Number_of_Persons_Interacted;
  htmltemplet.Max_Num_of_queries_from_one_person = Max_Num_of_queries_from_one_person;
  htmltemplet.Max_Time_spent_by_a_person = Max_Time_spent_by_a_person;
  htmltemplet.TableRangeValue1 = TableRangeValue1;
  
  // send Date_wise_persion_list table data to HTML file
  htmltemplet.Date2 = Date2;
  htmltemplet.Email_Id = Email_Id;
  htmltemplet.Name = Name;
  htmltemplet.No_of_querries = No_of_querries;
  htmltemplet.Start_time = Start_time;
  htmltemplet.End_Time = End_Time;
  htmltemplet.Duration = Duration;
  htmltemplet.TableRangeValue2 = TableRangeValue2;
  
  // Get yesterday date
  var yesterday = Utilities.formatDate(new Date(Date.now() - 864e5), "GMT", "MMM dd, yyyy");
  console.log(yesterday);
  
  //send yesterday date to HTML file
  htmltemplet.yesterday = yesterday;
  
  // Got final HTML table output 
  const final_html = htmltemplet.evaluate().getContent();
  //console.log(final_html); 
  
  // List of recipient to send daily update Mail
  var recipient = ["santoshi.kalaskar@bridgelabz.com","kalaskars1996@gmail.com"];
  Logger.log("Recipient Mail list length: " +recipient.length);
  
  // check Quota of Remaining available Mails
  var emailQuotaRemaining = MailApp.getRemainingDailyQuota(); 
  Logger.log("Remaining email quota: " + emailQuotaRemaining);
  
  // check condition & then send Mail
  if (emailQuotaRemaining > recipient.length) 
  {
   GmailApp.sendEmail(recipient, "Chatbot Report Daily Mail Update...!", "please open this mail with client that support HTML",
                     {htmlBody:final_html} );
   Logger.log("Daily Chatbot Update mail send successfully....! ");
  
  }
  else {
      Logger.log("Sorry unable to send mail because of  Remaining email Quota available is " + emailQuotaRemaining + " is less than Receipient mail list");
  }
  
}

