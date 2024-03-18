# library of code used to access and update data in the spreadsheet
# have to install them into the project using:"pip3 install gspread google-auth" in the terminal
# imports the whole gspread library and can access any funtion, method or class within it
import gspread
# imports just the credentials class which is part of the service funtion, from the google auth library 
# as we only need this class no need to import the whole library
from google.oauth2.service_account import Credentials

# constant variables in all uppercase, to tell others they shouldn't be changed
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


def get_sales_data():
    """
    Get sales figures input from the user
    run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers seperated by commas. 
    The loop will repeatedly request data, until it is valid
    """
    # while loop to keep requesting data after an invalid responce until we get a valid response
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        # split function converts one full string at the commas into a seperate list of items so each item can be seperatly accessed
        # eg not "1,2,3,4", but ["1", "2", "3", "4"] they are still strings though and have to be turned into integers to work on mathematically
        sales_data = data_str.split(",")
        
        # call validate_data function and get its returned function: true/false if true it ends the while loop, if false it continues
        # just need "if" that means if true, otherwise its false, "break" keyword ends the loop
        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    # gets the values from the variable sales_data when a valid input has been recieved
    return sales_data        

def validate_data(values):  
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int
    or if there aren't exactly 6 values 
    if the data contains anything else it will break the program
    """
    try:
        # loops through the values (sales_data) array and turns the strings in to integers
        [int(value) for value in values]
        # len() method reterns the length of the list. if the length (amount) of values is not equal to 6
        # raise error message saying how many values were input
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    # using the "as" keyword assign ValueError object to "e" variable, which is  standard python shorthand for "error" 
    # then can insert the e variable into an f string instead of writing ValueError        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        # if an error is thrown return false to continue while loop asking for valid input
        return False

    # return true ending while loop
    return True  


def update_sales_worksheet(data):
    """
    Update sales worksheet in google sheets.
    adding a new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    # acesses google sheets using the constant variable SHEETS and then just the "sales" worksheet in
    # there using the gspread worksheet() method and puts it in a variable sales_worksheet
    sales_worksheet = SHEET.worksheet("sales")
    # now the sheet is accessed, another gspread method- append_row() is used to add a new row
    # to the spread sheet, pass it the variable "data" in the () to add the data in that variable to
    # the spread sheet
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")



# gets the sales_data input into the get_sales_data function and puts it into the variable data so it can be used
data = get_sales_data()  
# loops through the data array and turns the strings in to integers and assigns it to sales_data variable
# so it can be used mathematically. different to the previously used sales_data variable
sales_data = [int(num) for num in data]
# calls upate_sales_worksheet functionand passes it the sales_data variable with all the data
update_sales_worksheet(sales_data)