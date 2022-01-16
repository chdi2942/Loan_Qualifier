# @TODO Define a function that implements the following user story:
# As a lender,
# I want to filter the bank list by checking the customer's desired loan against the bank's maximum loan size
# so that we can know which banks offer the loan amount requested by the customer
def filter_max_loan_size(loan_amount, bank_list):

    loan_size_approval_list = []
    for bank in bank_list:
        if loan_amount <= int(bank[1]):
            loan_size_approval_list.append(bank)
    return loan_size_approval_list