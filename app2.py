import questionary
import csv
from pathlib import Path
from qualifier.utils.fileio import load_csv
from qualifier.utils.calculators import (calculate_loan_to_value_ratio, calculate_monthly_debt_ratio)
from qualifier.filters.max_loan import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# This function loads a CSV file with the list of banks and available loans information from user input
def load_bank_data(file_path):
    '''Ask for the file path to the latest banking data and load the CSV file
    
    Returns:
        The bank data from the data rate sheet CSV file.'''
    
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    return load_csv(csvpath)

#Function to get user information via questionary
def get_applicant_info():
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What is your current debt?").ask()
    income = questionary.text("What is your current monthly income?").ask()
    loan_amount = questionary.text("What is the loan amount you wish to receive?").ask()
    home_value = questionary.text("What is the value of your home?").ask()

    #converts user inputs to correct data types
    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

#Gives MDR and LTV for user and filters loans according to user's needs
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

#Function is called if they select "Yes" in save_qualifying_list function
def save_csv():

    header = ["Lender", "Max Loan", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]

    #asks user what path to save filtered loan list
    user_path = questionary.text("What output path would you like to use for your filtered loan list csv file?").ask()

    #creates new csv file for filtered loan list
    with open(user_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(header)
        
        for row in qualifying_loans:
            csvwriter.writerow(row)

#Asks user if they would like to save their filtered loan list
def save_qualifying_loans():
    user_input = questionary.confirm("Would you like to save your filtered loan list?").ask()
    if user_input:
        # If they select yes, move them to save_csv function
        save_csv()
    else:
        # If they select no, tell them their list will not be saved
        print("Ok, we will not save your filtered loan list.")

'''This is where the program starts'''

file_path = Path("./data/daily_rate_sheet.csv")
   
# Load the latest Bank data
bank_data = load_bank_data(file_path)
    
# Get the applicant's information
credit_score, debt, income, loan_amount, home_value = get_applicant_info()

#Find qualifying loans based on user input   
qualifying_loans = find_qualifying_loans(
    bank_data, credit_score, debt, income, loan_amount, home_value
)
#Call the save_qualifying_loan function to ask user if they would like to save
save_qualifying_loans()