import pandas as pd

def simplify_settlements(file_path="Team_Expense_Split_Complete.xlsx", direct_expenses=[]):
    # Read net balances from the Balances sheet
    df = pd.read_excel(file_path, sheet_name='Balances')
    balances = dict(zip(df['Member'], df['Net Balance'].round(2)))

    # Adjust balances using the manually provided direct expenses
    for payer, receiver, amount in direct_expenses:
        balances[payer] -= amount
        balances[receiver] += amount

    debtors = [(m, -amt) for m, amt in balances.items() if amt < 0]
    creditors = [(m, amt) for m, amt in balances.items() if amt > 0]

    transactions = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amt = debtors[i]
        creditor, credit_amt = creditors[j]

        payment = min(debt_amt, credit_amt)
        transactions.append((debtor, creditor, round(payment, 2)))

        debtors[i] = (debtor, debt_amt - payment)
        creditors[j] = (creditor, credit_amt - payment)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    df_transactions = pd.DataFrame(transactions, columns=["From (Debtor)", "To (Creditor)", "Amount"])
    print("\nSimplified Settlement Recommendations (with Manual Direct Expenses):")
    print(df_transactions.to_string(index=False))

    with open("simplified_settlements_from_list.txt", "w") as f:
        f.write("Simplified Settlement Recommendations (with Manual Direct Expenses):\n")
        f.write(df_transactions.to_string(index=False))

# Example usage:
if __name__ == "__main__":
    direct_expenses = [
    ]
    simplify_settlements("Team_Expense_Split_Complete.xlsx", direct_expenses)
