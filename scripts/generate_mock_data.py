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
    # Calculate start date based on desired density (e.g., ~1 transaction every 2 days)
    # This ensures transactions are spread out over a realistic period
    days_back = int(num_transactions * 2)
    start_date = end_date - timedelta(days=days_back)
    
    # Generate random timestamps within the range and sort them
    timestamps = []
    total_seconds = int((end_date - start_date).total_seconds())
    
    for _ in range(num_transactions):
        random_seconds = random.randint(0, total_seconds)
        timestamps.append(start_date + timedelta(seconds=random_seconds))
    
    timestamps.sort()
    
    transactions = []
    balance = 15000.00  # Starting balance for business
    
    # Business related descriptions
    income_descriptions = [
        "INVOICE PAYMENT - CLIENT A",
        "INVOICE PAYMENT - CLIENT B", 
        "INVOICE PAYMENT - CLIENT C",
        "STRIPE PAYOUT",
        "SHOPIFY SETTLEMENT",
        "GST REFUND",
        "INTEREST RECEIVED"
    ]

    expense_descriptions = [
        "OFFICE RENT",
        "XERO SUBSCRIPTION",
        "AWS WEB SERVICES",
        "OFFICE SUPPLIES - WAREHOUSE STATIONERY",
        "BUSINESS INSURANCE",
        "ACC LEVY",
        "PAYE TAX PAYMENT",
        "CONTRACTOR PAYMENT - DEV",
        "CONTRACTOR PAYMENT - DESIGN",
        "SOFTWARE LICENSE - ADOBE",
        "SOFTWARE LICENSE - MICROSOFT",
        "INTERNET - BUSINESS FIBRE",
        "MOBILE - FLEET PLAN",
        "TRAVEL EXPENSES - FLIGHTS",
        "CLIENT LUNCH",
        "COFFEE FOR OFFICE",
        "CLEANING SERVICES",
        "COURIER POST",
        "PRINTING SERVICES",
        "BANK FEES"
    ]

    for i in range(num_transactions):
        current_date = timestamps[i]
        
        # 30% chance of income (invoices etc), 70% chance of expense
        if random.random() < 0.3:
             is_credit = True
             description = random.choice(income_descriptions)
             # Income tends to be larger chunks
             amount = round(random.uniform(500.0, 5000.0), 2)
        else:
             is_credit = False
             description = random.choice(expense_descriptions)
             # Expenses vary widely
             if "RENT" in description or "TAX" in description:
                 amount = round(random.uniform(1000.0, 3000.0), 2)
             elif "CONTRACTOR" in description:
                 amount = round(random.uniform(500.0, 2000.0), 2)
             else:
                 amount = round(random.uniform(20.0, 500.0), 2)
        
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
