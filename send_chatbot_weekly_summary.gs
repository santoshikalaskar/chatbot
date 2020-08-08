function send_weekly_summary() {
  // Read Sheets
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ws = ss.getSheetByName("Day_Wise_Summary");
  
  // get header columns of different tables from diff workspace sheets
  const theader1 = ws.getRange("B1:E1").getValues();
  
  // for Day_wise_summery table headers columns
  const Date1 = theader1[0][0];
  const Number_of_Persons_Interacted = theader1[0][1];
  const Max_Num_of_queries_from_one_person = theader1[0][2];
  const Max_Time_spent_by_a_person = theader1[0][3];
  
  // Get Last row index from diff workspace sheets
  const last_row1 = ws.getLastRow();
  
  // Get actual table data from diff workspace sheets
  const TableRangeValue1 = ws.getRange(2,2,last_row1-2,4).getDisplayValues();
  
  // connect HTML file with script
  const htmltemplet = HtmlService.createTemplateFromFile("send_chatbot_weekly_summary_template");
  
  // send Day_wise_summery table data to HTML file
  htmltemplet.Date1 = Date1;
  htmltemplet.Number_of_Persons_Interacted = Number_of_Persons_Interacted;
  htmltemplet.Max_Num_of_queries_from_one_person = Max_Num_of_queries_from_one_person;
  htmltemplet.Max_Time_spent_by_a_person = Max_Time_spent_by_a_person;
  htmltemplet.TableRangeValue1 = TableRangeValue1;
  
  // Get yesterday date
  var yesterday = Utilities.formatDate(new Date(Date.now() - 864e5), "GMT", "MMM dd, yyyy");
  
  var week_days = getLastweek_days()
  for (var j = 0; j < week_days.length; j++){
  Logger.log(week_days[j])
  }
  
  //send yesterday date to HTML file
  htmltemplet.week_days = week_days;
  
  // Got final HTML table output 
  const final_html = htmltemplet.evaluate().getContent();
  console.log(final_html); 
  
  // List of recipient to send daily update Mail
  //var recipient_to = ["anindo@bridgelabz.com","manoj@bridgelabz.com","gauri@bridgelabz.com"];
  var recipient_to = ["anindo@bridgelabz.com"]
  var recipient_cc = "santoshi.kalaskar@bridgelabz.com"+","+"akanksha.kaple@bridgelabz.com";
  //var recipient_cc = "santoshi.kalaskar@bridgelabz.com"
  Logger.log("Recipient Mail list length: " +recipient_to.length);
  
  // check Quota of Remaining available Mails
  var emailQuotaRemaining = MailApp.getRemainingDailyQuota(); 
  Logger.log("Remaining email quota: " + emailQuotaRemaining);
  
  // check condition & then send Mail
  if (emailQuotaRemaining > (recipient_to.length+2)) 
  {
   
   GmailApp.sendEmail(recipient_to, "Chatbot Report Weekly Update Mail...!", "please open this mail with client that support HTML",
                     {htmlBody:final_html,
                     cc: recipient_cc});
                     
   Logger.log("Weekly Chatbot Update mail send successfully....! ");
  
  }
  else {
      Logger.log("Sorry unable to send mail because of  Remaining email Quota available is " + emailQuotaRemaining + " is less than Receipient mail list");
  } 

}

function getLastweek_days()
{
  var week_days = [];
  var today = new Date();
  for(var i = 6; i >= 0; i--) 
  {
  var lastWeek = Utilities.formatDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - i), "GMT", "MMM dd, yyyy");
    week_days.push(lastWeek)
  }
  Logger.log(week_days); 
  return week_days;
}

