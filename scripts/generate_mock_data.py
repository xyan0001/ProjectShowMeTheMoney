import json
import random
from datetime import datetime, timedelta

def generate_mock_data(num_transactions=100, start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    
    transactions = []
    balance = 10000.00  # Starting balance
    
    descriptions = [
        "TRANSFER FROM JJXEDXX - 01",
        "PAYMENT TO SUPPLIER ABC",
        "DIRECT DEBIT UTILITY",
        "POS PURCHASE OFFICE SUPPLIES",
        "CREDIT INTEREST",
        "TRANSFER TO SAVINGS"
    ]

    current_date = start_date

    for i in range(num_transactions):
        # Advance time randomly by 0-3 days
        current_date += timedelta(days=random.randint(0, 3), hours=random.randint(0, 23))
        
        is_credit = random.choice([True, False])
        amount = round(random.uniform(10.0, 5000.0), 2)
        
        debit_amount = 0
        credit_amount = 0
        
        if is_credit:
            credit_amount = amount
            balance += amount
        else:
            debit_amount = amount
            balance -= amount

        transaction = {
            "transactionId": str(i + 1),
            "accountNumber": "9023053068900",
            "transactionDate": current_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "debitAmount": debit_amount,
            "creditAmount": credit_amount,
            "balance": round(balance, 2),
            "description": random.choice(descriptions),
            "transactionCode": str(random.randint(10, 99)),
            "branch": "1",
            "operator": str(random.randint(1000, 9999)),
            "effectiveDate": current_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "cheque": "",
            "thisPayeePart": "",
            "thisPayeeCode": "",
            "thisPayeeRef": "",
            "otherPayeePart": "",
            "otherPayeeCode": "",
            "otherPayeeRef": "",
            "otherPayeeName": "JJXEDXX" if "JJXEDXX" in descriptions else "",
            "otherPayeeAccountNumber": "38-9023-0530689-01",
            "originialTransactionCode": "",
            "sourceCode": "",
            "nonValueTransactionItems": []
        }
        transactions.append(transaction)

    data = {
        "data": {
            "moreTransactions": False,
            "transactionCount": len(transactions),
            "transactionItems": transactions
        }
    }

    return data

if __name__ == "__main__":
    mock_data = generate_mock_data(200)
    with open("mock_transactions.json", "w") as f:
        json.dump(mock_data, f, indent=2)
    print("Mock data generated in mock_transactions.json")
