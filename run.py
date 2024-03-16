# library of code used to access and update data in the spreadsheet
# have to install them into the project using:"pip3 install gspread google-auth" in the terminal
# imports the whole gspread library and can access any funtion, method or class within it
import gspread
# imports just the credentials class which is part of the service funtion, from the google auth library 
# as we only need this class no need to import the whole library
from google.oauth2.service_account import Credentials

# constant variables in capitals, to tell others they shouldn't be changed
# lists the APIs the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# calls the credentials class from google auth service_account
# pass it the creds.json file (the spreadsheet) to access
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')    

# uses the worksheet method from gspread to access the spreadsheet data in a variable we call 'sales'
sales = SHEET.worksheet('sales')

# uses a method from gspread to pull all the values from the sales worksheet using the sales variable we made
data = sales.get_all_values()

print(data)