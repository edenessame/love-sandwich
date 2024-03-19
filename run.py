# library of code used to access and update data in the spreadsheet
# have to install them into the project using:"pip3 install gspread google-auth" in the terminal
# imports the whole gspread library and can access any funtion, method or class within it
import gspread

# imports just the credentials class which is part of the service funtion, from the google auth library 
# as we only need this class no need to import the whole library
from google.oauth2.service_account import Credentials

# imports pprint method that prints data that is easier to read
from pprint import pprint

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


# def update_sales_worksheet(data):
    """
    Update sales worksheet in google sheets.
    adding a new row with the list data provided
    code commented out, replaced by the update_worksheet function
    """
#    print("Updating sales worksheet...\n")
    # acesses google sheets using the constant variable SHEETS and then just the "sales" worksheet in
    # there using the gspread worksheet() method and puts it in a variable sales_worksheet
#    sales_worksheet = SHEET.worksheet("sales")
    # now the sheet is accessed, another gspread method- append_row() is used to add a new row
    # to the spread sheet, pass it the variable "data" in the () to add the data in that variable to
    # the spread sheet
#    sales_worksheet.append_row(data)
#    print("Sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
    """
    Update surplus worksheet in google sheets.
    adding a new row with the list data provided
    code commented out, replaced by the update_worksheet function
    """
#    print("Updating surplus worksheet...\n")
    # acesses google sheets using the constant variable SHEETS and then just the "sales" worksheet in
    # there using the gspread worksheet() method and puts it in a variable surplus_worksheet
#    surplus_worksheet = SHEET.worksheet("surplus")
    # now the sheet is accessed, another gspread method- append_row() is used to add a new row
    # to the spread sheet, pass it the variable "data" in the () to add the data in that variable to
    # the spread sheet
#   surplus_worksheet.append_row(data)
#    print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Refactored function to do the jub of multiple similar functions
    Recieves a list of integers to be inserted into a work sheet
    Update the relevant worksheet with the data provided when the function is called
    in the main function area
    the parameters "data" and "worksheet "become what is put in their place when the function is called
    eg. update_worksheet(sales_data, "sales") this accesses the "sales" worksheet and 
    appends the sales_data to the bottom of the spreadsheet
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type
    the surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates extras made when stock ran out
    """
    print("Calculating surplus data...\n")
    
    # gets the data from the stock worksheet in google sheets and puts it in a variable "stock"
    # .get_all_values gets all the data from the worksheet and returns it in multiple arrays of the different rows
    stock = SHEET.worksheet("stock").get_all_values() 
    # gets the last array from what is returned above
    stock_row = stock[-1]
    
    # empty array to store the surplus data retrieved from the for loop bellow
    surplus_data = []
    # for loop to iterate through 2 lists using the zip method
    # reterns each item in the stock_row/sales_row arrays and adds them to the stock or sales variables 
    for stock, sales in zip(stock_row, sales_row):
        # then subtract one from the other to get the surplus amount in a variable: "surplus" 
        # but first use int() to turn the items returned from the stock variable, which will be strings
        # into integers so one can be subtracted from the other
        # and using .append() update the empty surplus_data array with the values retrieved 
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    # return the suplus_data array created in the function and store it in a variable in the main function
    return surplus_data   

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the last 5 
    entries for each sandwich and returns a list of lists
    """
    sales = SHEET.worksheet("sales")
    # col_values() method provided by gspread allows access to a single column in the worksheet, with
    # a number in the (), but to access all you have to use a for loop
    # column = sales.col_values(3)

    # creates an empty array, then loops through the columns in range 1-7 
    # then adds them seperatly to the array columns with append, then "[-5:]" slices 
    # the last 5 items, we need the ":" because we want to slice multiple values from the list
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns   

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type adding 10%
    """
    print("Calculating stock data...\n")
    # empty array to add averages to from for loop bellow
    new_stock_data = []

    # loops through each column in "data" which is the worksheet thats passed when the function is called 
    # getting each number as a string, have to add int() to turn the strings into integers so can do calculations with them
    # then work out the average, using the sum() method adds all items in the () so all the columns in (int_column)
    # this is then divided by the length of the column using len(int_column) to give the average 
    # then add 10%, then round them to whole numbers, then add them to the empty array
    for column in data:
        int_column = [int(num) for num in column]
        # sum() adds all items in the variable written in () together, len() gets the amount of items in the (variable) 
        average = sum(int_column) / len(int_column)
        # * 1.1 adds 10%
        stock_num = average * 1.1
        # round() rounds the items in the () to whole numbers rather than decimals
        new_stock_data.append(round(stock_num))

    return new_stock_data




def main():
    """
    runs all the main functions
    Common practice to wrap the main function calls in a function called "main"
    functions have to be called bellow themselves to work 
    """
    # gets the sales_data input into the get_sales_data function and puts it into the variable data so it can be used
    data = get_sales_data()  
    # loops through the data array and turns the strings in to integers and assigns it to sales_data variable
    # so it can be used mathematically. different to the previously used sales_data variable
    sales_data = [int(num) for num in data]
    # calls upate_worksheet function and passes it the sales_data variable with the in put sales for the day to be
    # assigned to the data parameter and the string "sales" to be assigned to the worksheet parameter
    # they then replace those words in the update_worksheet function, so it can access the variable and
    # worksheet that they are assigned to
    update_worksheet(sales_data, "sales")
    # calls calculate_surplus_data function, passing it the sales_data list to use in the calculation
    # subtracting it from the stock to get the new surplus data
    new_surplus_data = calculate_surplus_data(sales_data)
    # calls upate_worksheet function and passes it the new_surplus_data variable with the calculated surplus to be
    # assigned to the data parameter and the string "surplus" to be assigned to the worksheet parameter
    # they then replace those words in the update_worksheet function, so it can access the variable and
    # worksheet that they are assigned to
    update_worksheet(new_surplus_data, "surplus")
    # gets last 5 days sales from the sales worksheet
    sales_columns = get_last_5_entries_sales()
    # passes the data recieved from get last 5 entries sales function thats saved in sales_columns variable
    # into calculate_stock_data function. this adds the entries together in each column and divides by the number of 
    # entries in the column to give an average + 10%
    stock_data = calculate_stock_data(sales_columns)
    # calls update_worksheet function again, same as before, passing it the stock_data and thelling it to update
    # the "stock" worksheet
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation")

# calls the main function and all the other functions within it
main()

