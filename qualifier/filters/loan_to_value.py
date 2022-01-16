# @TODO Define a function that implements the following user story:
# As a lender,
# I want to filter the bank list by checking if the customer's loan-to-value is equal to or less than the maximum loan-to-value ratio allowed by the bank
# so that we assess if the customer's home value is worth as an asset to secure the loan
def filter_loan_to_value(loan_to_value_ratio, bank_list):

    ltv_approval_list = []
    for bank in bank_list:
        if loan_to_value_ratio <= float(bank[2]):
            ltv_approval_list.append(bank)
    return ltv_approval_list