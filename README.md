# Loan_Qualifier

## **Summary**

Hello User,

This program is built to receive user inputs for your:
* path to a list of loans
* path to save filtered list
* credit score
* debt
* montly income
* desired loan amount
* value of home

These prompts are powered by questionary.  You must start by telling the program which loans you have to choose from (through a path to a csvfile).  Make sure your csvfile to be read is formatted with a header and corresponding data like so:

[Lender,Max Loan Amount,Max LTV,Max DTI,Min Credit Score,Interest Rate]
[data]

Once the path is set, the program is designed to filter your submitted list of loans by your entered criteria to determine which loans that you qualify for.

Once your filtered list of loans is created, you can choose to save this filtered list of loans as a csvfile for your review, at a path that you can select.  If you choose not to save your filtered list, the program will terminate.

That's it!  With a properly formatted csvfile and correct inputs, you can now filter through your loan options with ease to find your perfect loan!

## **Requirements**

python 3.7
questionary python library (pip install questionary)
