function sendEmailsFromCell() {
  
  // Read Sheets
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const app = ss.getSheetByName("send_mail_to_many");
  
  // get Mail body static mail body template text
  var messageBody = app.getRange(1, 7).getValue();
  
  // get Last row of the workspace sheet
  var last_row = app.getLastRow();
  
  // check Quota of Remaining available Mails
  var emailQuotaRemaining = MailApp.getRemainingDailyQuota(); 
  Logger.log("Remaining email quota: " + emailQuotaRemaining);
  
  // check condition
  if (emailQuotaRemaining >= (last_row-1)) 
    {
      // iterate each row to fetch id & name
    for( var i=2;i<=last_row;i++)
      {
      var currentEmail = app.getRange(i, 1).getValue();
      var currentName = app.getRange(i, 2).getValue();
    
      // replace body template dynamically
      var newMessageBody = messageBody.replace("{name}",currentName);
      
      // send mail
      GmailApp.sendEmail(currentEmail, "Send mail to multiple people demo...!", newMessageBody );
      
      } // close for loop
      
      Logger.log("Sent mail to "+(last_row-1)+" people successfully....! ");
      
      }// close if 
    else 
      {
        Logger.log("You have " + emailQuotaRemaining + " left and you're trying to send "+(last_row-1)+ " Emails. Email were not sent.");
      }
  
 }

