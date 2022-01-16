import fire
import questionary
from pathlib import Path
from qualifier.utils.fileio import load_csv
from qualifier.utils.calculators import (calculate_loan_to_value_ratio, calculate_monthly_debt_ratio)
from qualifier.filters.max_loan import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# This function loads a CSV file with the list of banks and available loans information
# from the file defined in `file_path`
def load_bank_data(file_path):
    '''Ask for the file path to the latest banking data and load the CSV file
    
    Returns:
        The bank data from the data rate sheet CSV file.'''
    
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    return load_csv(csvpath)
    
def get_applicant_info():
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What is your current debt?").ask()
    income = questionary.text("What is your current monthly income?").ask()
    loan_amount = questionary.text("What is the loan amount you wish to receive?").ask()
    home_value = questionary.text("What is the value of your home?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

# This function implements the following user story:
# As a customer,
# I want to know what are the best loans in the market according to my financial profile
# so that I can choose the best option according to my needs
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

# This function is the main execution point of the application. It triggers all the business logic.
def run():
    # Set the file path of the CVS file with the banks and loans information
    file_path = Path("./data/daily_rate_sheet2.csv")
    # Load the latest Bank data
    bank_data = load_bank_data(file_path)

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()
   
    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )    
    # Print the list of qualifying loans
    print(qualifying_loans)

if __name__ == '__main__':
    fire.Fire(run)
