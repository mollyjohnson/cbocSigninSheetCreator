#!/usr/bin/python3 

# Author: Molly Johnson
# Date: 3/24/21
# Description: Creates cboc signin excel file for
# checking in clinics for one month. Will adjust 
# for the days of the month, weekends, and federal holidays

####################################################################
### Function Title:
### Arguments:
### Returns:
### Description: 
####################################################################

# import openpyxl, datetime, and calendar
import openpyxl
from openpyxl import Workbook
from datetime import datetime
import calendar
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

# create constants
JB = "Jesse Brown"
CP = "Crown Point"
HE = "Hoffman Est."
LA = "LaSalle"
AU = "Aurora"
JO = "Joliet"
KA = "Kankakee"
OL = "Oak Lawn"
FZ = "Frozen"
TCH = "Tech"
TOA = "Time of Arrival"
MID_DATE = 15
CBOC_COL_WIDTH = 10.86
HEADER_ROW_HEIGHT = 45
CBOC_ROW_HEIGHT = 20
TECH_TOA_HEIGHT = 27
CBOC_NAME_AND_FROZEN_HEIGHT = 21
SPACER_HEIGHT = 10
NUM_ROWS = 27
HEADER_ROW = 1
CBOC_ROW = 2
DATE_ROW = 3
TECH_TOA_ROW = 4
CBOC_NAME_AND_FROZEN_ROW_START = 5
CBOC_NAME_AND_FROZEN_ROWS = [5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27]
SPACER_ROWS = [7,10,13,16,19,22,15]

# set cell border values
thin = Side(border_style = "thin", color = "000000")
double = Side(border_style = "double", color = "000000")
thick = Side(border_style = "thick", color = "001C54")

####################################################################
### Function Title: setRowHeights()
### Arguments:
### Returns:
### Description: 
####################################################################
def setRowHeights(ws):
    ws.row_dimensions[HEADER_ROW].width = HEADER_ROW_HEIGHT
    

####################################################################
### Function Title: validUserInput()
### Arguments:
### Returns:
### Description: 
####################################################################
def validUserInput(userInput):
    # check that length of user input string is correct
    if(len(userInput) != 5):
        return False
    
    # check that first two chars are digits, mid char
    # is / or -, and last 2 chars are digits.
    j = 0
    while(j < len(userInput)):
        if(j != 2):
            if(userInput[j].isdigit() == False):
                return False
        else:
            if(userInput[j] != '-' and userInput[j] != '/'):
                return False
        j += 1
    
    # if the month and year chars were digits, make sure they make sense
    monthInput = ""
    yearInput = ""
    monthInput += userInput[0]
    monthInput += userInput[1]
    yearInput += userInput[3]
    yearInput += userInput[4]

    # check that month is between 1 and 12
    if(int(monthInput) < 1 or int(monthInput) > 12):
        return False
    # check that year is between 2021 and 2099
    if (int(yearInput) < 21 or int(yearInput) > 99):
        return False
    
    # otherwise met all requirements, return true
    return True

####################################################################
### Function Title: getStartDate()
### Arguments:
### Returns:
### Description: 
####################################################################
def getStartDate():
    # get start date of the month from user
    i = 0
    while(i == 0):
        userInput = input("\nEnter month and year in the format mm/yy: ")
        if(validUserInput(userInput) == True):
            i = 1
        else:
            print("Your entry was invalid. Enter month and year in the format mm/yy or mm-yy:")

    # reformat start date input into string for datetime in format mm-01-20yy
    i = 0
    startDate = "" 
    while(i < len(userInput)):
        if(i >= 0 and i <= 1):
            startDate += userInput[i]
        elif(i == 2):
            startDate += "-01-20"
        elif(i >= 3):
            startDate += userInput[i]
        i += 1
    return startDate

####################################################################
### Function Title: createHeader()
### Arguments:
### Returns:
### Description: 
####################################################################
def createHeader(ws, startCell, endCell, startDateObj):
    # create header border formatting
    headerBorderLeft = Border(top = thick , left = thick, right = None, bottom = thick) 
    headerBorderRight = Border(top = thick , left = None, right = thick, bottom = thick)  
    headerBorderMid = Border(top = thick, left = None, right = None, bottom = thick)
    
    # font values
    headerFont = Font(name = 'Times New Roman', size = 28, bold = True)    
    
    ###################NEED TO USE NUMBERS NOT LETTERS FOR CELLS HERE
    #set header alignment to center, font to Times New Roman and size to 28
    ws['A1'].alignment = Alignment(horizontal = 'center')
    ws['A1'].font = headerFont
    
    # set border at far left and far right of header merged cells
    ws['A1'].border = headerBorderLeft
    ws['AE1'].border = headerBorderRight
    
    # set border at middle header merged cells
    for row in ws.iter_rows(min_row = 1, max_row = 1, min_col = (startCell + 1), max_col = (endCell - 1)):
        for cell in row:
            cell.border = headerBorderMid 
            
    # create header and merge cells A1 through AE1
    ws['A1'] = ("Month/Year: " + (str(calendar.month_name[startDateObj.month]) + " " + 
        str(startDateObj.year)).upper())
    data = ws['A1'].value 
    ws.merge_cells('A1:AE1')
    ws['A1'] = data 

####################################################################
### Function Title: getDateTimeObj()
### Arguments:
### Returns:
### Description: 
####################################################################   
def getDatetimeObj(startDate):
    dateTimeObj = datetime.strptime(startDate, "%m-%d-%Y")
    #print start date string
    print(startDate)
    #get day number from date
    print('Day of Month: ', dateTimeObj.day)
    #get year from date
    print('Year: ', dateTimeObj.year)
    #to get name of day (in number) from date
    print('Day of Week (number): ', dateTimeObj.weekday())
    # to get name of day from date
    print('Day of Week (name): ', calendar.day_abbr[dateTimeObj.weekday()])
    # to get name of month from date
    print('Month name: ', calendar.month_name[dateTimeObj.month])
    return dateTimeObj
    
####################################################################
### Function Title: main()
### Arguments:
### Returns:
### Description: 
####################################################################
def main():
    # create workbook (1st sheet at pos 0 created automatically)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "1-15"

    # create 2nd sheet at pos 1
    ws2 = wb.create_sheet("16-End", 1)
    
    # get start date string from user
    startDate = getStartDate()

    # Create date object in format mm-dd-yyyy from start date string
    startDateObj = getDatetimeObj(startDate)
    
    # get end date for the month
    endDate = calendar.monthrange(startDateObj.year, startDateObj.month)[1]
    print("End of month date: " + str(endDate))

    #to iterate to next date/day name
    #print('Next date (num) of week: ', (startDateObj.day + 1))
    #print('Next day of week (name): ', calendar.day_abbr[(startDateObj.weekday()) + 1])

    # set row height for all rows
    setRowHeights(ws1)
    setRowHeights(ws2)
    
    cbocNameBorder = Border(top = thick , left = thick, right = thick, bottom = thick) 
    cbocNameFont = Font(name = 'Times New Roman', size = 10, bold = True)

    # create cboc cell font/border/value

    ws1.cell(row=2, column=1).font = cbocNameFont
    ws1.cell(row=2, column=1).border = cbocNameBorder
    ws1.cell(row=2, column=1).value = 'test'
    #ws1['A2'].font = cbocNameFont
    #ws1['A2'].border = cbocNameBorder
    ws1.column_dimensions['A'].width = CBOC_COL_WIDTH
    
    # create header for both sheets
    createHeader(ws1, 1, MID_DATE, startDateObj)
    createHeader(ws2, 1, (endDate - MID_DATE), startDateObj)
    
    # save workbook to excel file and exit
    wb.save('cboc_signin_sheet.xlsx')   

if __name__ == "__main__":
    main()