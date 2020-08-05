function sendIndividualsEmails() {
  
  // Read Sheets
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const app = ss.getSheetByName("Date_Wise_PersonList");
  
  // connect HTML file with script
  const htmltemplet = HtmlService.createTemplateFromFile("send_individual_mail");
  
  // get Last row of the workspace sheet
  var last_row = app.getLastRow();
  Logger.log("Last row: "+ last_row)
  
  // Get yesterday date
  
  var UserEnteredDate = app.getRange(2, 11).getDisplayValues()[0][0];
  Logger.log(UserEnteredDate)
  
  
  //var yesterday = Utilities.formatDate(new Date(Date.now() - 864e5), "GMT", "MMM dd, yyyy");
  //Logger.log("Yesterday date: " + yesterday);
  
  // check Quota of Remaining available Mails
  var emailQuotaRemaining = MailApp.getRemainingDailyQuota(); 
  Logger.log("Remaining email quota: " + emailQuotaRemaining);
  
  var no_of_rows_found = find_no_of_rows(app,UserEnteredDate,last_row)
  
  // check condition
  if (emailQuotaRemaining >= no_of_rows_found) 
    {
       var counter = 0;
      
       // iterate each row to fetch id & name
       for( var i=2;i<=last_row;i++)
       {
          var currentDate = app.getRange(i, 1).getDisplayValues();
         
          if (currentDate == UserEnteredDate) 
          {
            
            var currentEmail = app.getRange(i, 2).getValue();
            var currentName = app.getRange(i, 3).getValue();
            
            // send dynamic name to html template
            htmltemplet.currentName = currentName;
        
            // get & evaluate all html code 
            const final_html = htmltemplet.evaluate().getContent();
            
            // send mail
            GmailApp.sendEmail(currentEmail, "Reminder Mail that you have interacted with our BridgeLabz Chatbot.", "please open this mail with client that support HTML",
                        {htmlBody:final_html});
            counter = counter + 1; 
            
            var status = app.getRange(i,8);
            status.setValue("Mail Sent");
            
          }// close if 
      
        } // close for loop
      
        Logger.log("Sent mail to "+(counter)+" people successfully....! ");
      
      }// close if 
    else 
      {
        Logger.log("You have " + emailQuotaRemaining + " left and you're trying to send "+(last_row-1)+ " Emails. Email were not sent.");
      }
 }

function find_no_of_rows(app,UserEnteredDate,last_row)
{ 
  var counter = 0;
  for( var i=2;i<=last_row;i++)
  {
    var currentDate = app.getRange(i, 1).getDisplayValues();
    if (currentDate == UserEnteredDate)
    {
      counter = counter + 1;
    }  
  }
  Logger.log("Matched Rows: "+ counter); 
  return counter;
}

