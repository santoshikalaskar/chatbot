function generate_formulae() {
  
  // Read Sheets
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ws1 = ss.getSheetByName("generate_formulae");
  const ws2 = ss.getSheetByName("Date_Wise_PersonList2");
  const ws3 = ss.getSheetByName("Day_Wise_Summary2");
 
  // generate_formulae sheet : set formula
  ws1.getRange("F1").setValue("Time");
  ws1.getRange("G1").setValue("Date");
  
  ws1.getRange("F2").setFormula('=IFERROR(INDEX(split(E2," "),0,2),"")');
  var fillDownRange = ws1.getRange(2,6,998,1);
  ws1.getRange("F2").copyTo(fillDownRange);
  
  ws1.getRange("G2").setFormula('=INT(E2)');
  var fillDownRange = ws1.getRange(2,7,998,1);
  ws1.getRange("G2").copyTo(fillDownRange);
  
  // Date_Wise_PersonList2 sheet : set formula
  ws2.getRange("A1").setFormula('=unique(QUERY(generate_formulae!A1:G,"SELECT G, C"))');
  var fillDownRange2 = ws2.getRange(2,1);
  ws2.getRange("A2").copyTo(fillDownRange2);
  
  ws2.getRange("C1").setValue("Name");
  ws2.getRange("D1").setValue("No of querries");
  ws2.getRange("E1").setValue("Start time");
  ws2.getRange("F1").setValue("End Time");
  ws2.getRange("G1").setValue("Duration");
  
  ws2.getRange("C2").setFormula('=IFNA(INDEX(vlookup(B2,generate_formulae!$C$2:$D,2,FALSE),0,1)," ")');
  var fillDownRange = ws2.getRange(2,3,998,1);
  ws2.getRange("C2").copyTo(fillDownRange);
  
  ws2.getRange("D2").setFormula('=if(countif(filter(generate_formulae!C$2:C,generate_formulae!C$2:C=B2,generate_formulae!G$2:G=A2),B2)=0,"",countif(filter(generate_formulae!C$2:C,generate_formulae!C$2:C=B2,generate_formulae!G$2:G=A2),B2))');
  var fillDownRange = ws2.getRange(2,4,998,1);
  ws2.getRange("D2").copyTo(fillDownRange);
  
  ws2.getRange("E2").setFormula('=min(filter(generate_formulae!$F$2:$F,generate_formulae!$C$2:$C=$B2))');
  var fillDownRange = ws2.getRange(2,5,998,1);
  ws2.getRange("E2").copyTo(fillDownRange);
  
  ws2.getRange("F2").setFormula('=MAX(filter(generate_formulae!$F$2:$F,generate_formulae!$C$2:$C=$B2))');
  var fillDownRange = ws2.getRange(2,6,998,1);
  ws2.getRange("F2").copyTo(fillDownRange);
  
  ws2.getRange("G2").setFormula('=F2-E2');
  var fillDownRange = ws2.getRange(2,7,998,1);
  ws2.getRange("G2").copyTo(fillDownRange);
  
  //Day_Wise_Summary2 sheet : set Formula
  ws3.getRange("B1").setValue("Date");
  ws3.getRange("C1").setValue("Number of Persons Interacted");
  ws3.getRange("D1").setValue("Max Num of queries from one person");
  ws3.getRange("E1").setValue("Max Time spent by a person");
  
  ws3.getRange("B2").setFormula('=QUERY(Date_Wise_PersonList2!A2,"SELECT A")');
  ws3.getRange("B3").setFormula('= B2+1');
  var fillDownRange = ws3.getRange(3,2,997,1);
  ws3.getRange("B3").copyTo(fillDownRange);
  
  ws3.getRange("C2").setFormula('=if(countif(Date_Wise_PersonList2!A$2:A,B2)=0,"No Entry Found",countif(Date_Wise_PersonList2!A$2:A,B2))');
  var fillDownRange = ws3.getRange(2,3,998,1);
  ws3.getRange("c2").copyTo(fillDownRange);
  
  ws3.getRange("D2").setFormula('=IFNA(max(filter(Date_Wise_PersonList2!D$2:D,Date_Wise_PersonList2!A$2:A=B2)),"No Entry Found")');
  var fillDownRange = ws3.getRange(2,4,998,1);
  ws3.getRange("D2").copyTo(fillDownRange);
  
  ws3.getRange("E2").setFormula('=IFNA(max(filter(Date_Wise_PersonList2!G$2:G,Date_Wise_PersonList2!A$2:A=B2)),"No Entry Found")');
  var fillDownRange = ws3.getRange(2,5,998,1);
  ws3.getRange("E2").copyTo(fillDownRange);
  
}

