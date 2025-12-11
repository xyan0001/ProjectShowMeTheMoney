import json
import random
from datetime import datetime, timedelta

def generate_nz_bank_account():
    banks = [
        {"prefixes": ["01", "04", "06", "11"], "branch_range": (1, 5699)}, # ANZ
        {"prefixes": ["02"], "branch_range": (1, 1299)}, # BNZ
        {"prefixes": ["03"], "branch_range": (1, 1999)}, # Westpac
        {"prefixes": ["12"], "branch_range": (3000, 3499)}, # ASB (Common)
        {"prefixes": ["38"], "branch_range": (9000, 9499)}, # Kiwibank (Common)
    ]
    
    bank = random.choice(banks)
    prefix = random.choice(bank["prefixes"])
    branch = random.randint(bank["branch_range"][0], bank["branch_range"][1])
    account = random.randint(1, 9999999)
    suffix = random.randint(0, 99)
    
    return f"{prefix}-{branch:04d}-{account:07d}-{suffix:02d}"

def generate_mock_data(num_transactions=200, end_date_str="2025-12-11"):
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    # Estimate start date to fit transactions (avg 1.5 days per transaction)
    start_date = end_date - timedelta(days=int(num_transactions * 1.5) + 30)
    
    transactions = []
    balance = 5000.00  # Starting balance
    
    descriptions = [
        "TRANSFER FROM JJXEDXX - 01",
        "PAYMENT TO SUPPLIER ABC",
        "DIRECT DEBIT UTILITY",
        "POS PURCHASE OFFICE SUPPLIES",
        "CREDIT INTEREST",
        "TRANSFER TO SAVINGS",
        "COUNTDOWN SUPERMARKET",
        "NEW WORLD GROCERY",
        "UBER TRIP",
        "UBER EATS",
        "NETFLIX SUBSCRIPTION",
        "SPOTIFY PREMIUM",
        "Z ENERGY PETROL",
        "BP CONNECT",
        "CAFE LUNCH",
        "RESTAURANT DINNER",
        "SALARY PAYMENT",
        "RENT PAYMENT",
        "POWER BILL",
        "INTERNET BILL",
        "MOBILE PLAN",
        "GYM MEMBERSHIP",
        "PHARMACY PURCHASE",
        "HARDWARE STORE",
        "ONLINE SHOPPING AMAZON",
        "THE WAREHOUSE",
        "KMART PURCHASE"
    ]

    current_date = start_date

    for i in range(num_transactions):
        # Advance time randomly by 0-3 days
        current_date += timedelta(days=random.randint(0, 3), hours=random.randint(0, 23))
        
        # Ensure we don't go past the end date
        if current_date > end_date:
            current_date = end_date
        
        is_credit = random.choice([True, False])
        # Make salary more likely to be credit and larger
        if random.random() < 0.1:
             description = "SALARY PAYMENT"
             is_credit = True
             amount = round(random.uniform(2000.0, 4000.0), 2)
        else:
             description = random.choice([d for d in descriptions if d != "SALARY PAYMENT"])
             amount = round(random.uniform(10.0, 300.0), 2)
        
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
            "description": description,
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
            "otherPayeeName": "JJXEDXX" if "JJXEDXX" in description else "",
            "otherPayeeAccountNumber": generate_nz_bank_account(),
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
