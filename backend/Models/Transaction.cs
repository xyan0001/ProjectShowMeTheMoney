namespace ShowMeTheMoney.API.Models;

public class TransactionResponse
{
    public TransactionData Data { get; set; }
}

public class TransactionData
{
    public bool MoreTransactions { get; set; }
    public int TransactionCount { get; set; }
    public List<TransactionItem> TransactionItems { get; set; }
}

public class TransactionItem
{
    public string TransactionId { get; set; }
    public string AccountNumber { get; set; }
    public DateTime TransactionDate { get; set; }
    public decimal DebitAmount { get; set; }
    public decimal CreditAmount { get; set; }
    public decimal Balance { get; set; }
    public string Description { get; set; }
    public string TransactionCode { get; set; }
    public string Branch { get; set; }
    public string Operator { get; set; }
    public DateTime EffectiveDate { get; set; }
    public string Cheque { get; set; }
    public string ThisPayeePart { get; set; }
    public string ThisPayeeCode { get; set; }
    public string ThisPayeeRef { get; set; }
    public string OtherPayeePart { get; set; }
    public string OtherPayeeCode { get; set; }
    public string OtherPayeeRef { get; set; }
    public string OtherPayeeName { get; set; }
    public string OtherPayeeAccountNumber { get; set; }
    public string OriginialTransactionCode { get; set; }
    public string SourceCode { get; set; }
    public List<NonValueTransactionItem> NonValueTransactionItems { get; set; }
}

public class NonValueTransactionItem
{
    public string NonValueTransactionId { get; set; }
    public string NonValueTransactionDescription { get; set; }
    public string NonValueTransactionCode { get; set; }
}
