using Microsoft.AspNetCore.Mvc;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using ShowMeTheMoney.API.Models;
using System.Text.Json;

namespace ShowMeTheMoney.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionController : ControllerBase
{
    private readonly Kernel? _kernel;
    private readonly IWebHostEnvironment _env;

    public PredictionController(IWebHostEnvironment env, Kernel? kernel = null)
    {
        _env = env;
        _kernel = kernel;
    }

    [HttpPost]
    public async Task<IActionResult> PredictCashFlow([FromBody] PredictionRequest request)
    {
        // 1. Get historical data (mock)
        string filePath = Path.Combine(_env.ContentRootPath, "..", "mock_transactions.json");
        if (!System.IO.File.Exists(filePath))
        {
            return NotFound("Mock data file not found.");
        }

        string jsonString = await System.IO.File.ReadAllTextAsync(filePath);
        var transactionData = JsonSerializer.Deserialize<TransactionResponse>(jsonString, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

        if (transactionData?.Data?.TransactionItems == null)
        {
            return BadRequest("Invalid transaction data.");
        }

        // 2. Prepare prompt for LLM
        var transactions = transactionData.Data.TransactionItems
            .OrderBy(t => t.TransactionDate)
            .Select(t => new { t.TransactionDate, t.DebitAmount, t.CreditAmount, t.Balance, t.Description })
            .ToList();

        string transactionsJson = JsonSerializer.Serialize(transactions);

        // Fallback if Kernel is not configured (e.g. missing secrets)
        if (_kernel == null)
        {
             return Ok(GenerateMockPrediction(transactions.Last().Balance, request.Months));
        }

        try
        {
            var executionSettings = new OpenAIPromptExecutionSettings
            {
                ResponseFormat = typeof(PredictionResponse),
                MaxTokens = 4000,
                Temperature = 0.5,
                TopP = 0,
            };

            var skPrompt = $@"
## Role
You are a financial analyst AI. 

## Task
Based on the following transaction history, predict the cash flow for the next {request.Months} months.

## Requirements
- Analyze the spending and income patterns.
- Project the balance for the end of each future month.
- Output ONLY valid JSON matching the specified structure.
- Do not include any markdown formatting or explanation.

## Transaction History:
{transactionsJson}
";

            var predictFunction = _kernel.CreateFunctionFromPrompt(skPrompt, executionSettings);
            var result = await _kernel.InvokeAsync(predictFunction);
            
            var responseString = result.ToString();
            var predictionResponse = JsonSerializer.Deserialize<PredictionResponse>(responseString);

            if (predictionResponse == null)
            {
                return StatusCode(500, "Failed to deserialize LLM response.");
            }

            // Flatten the structure to match what the frontend expects (List of objects)
            return Ok(predictionResponse.Predictions);
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Error calling LLM: {ex.Message}");
        }
    }

    private List<object> GenerateMockPrediction(decimal currentBalance, int months)
    {
        var predictions = new List<object>();
        var date = DateTime.Now;
        var balance = currentBalance;
        var random = new Random();

        for (int i = 1; i <= months; i++)
        {
            // Simple random walk for mock prediction
            balance += random.Next(-1000, 2000); 
            predictions.Add(new 
            { 
                date = date.AddMonths(i).ToString("yyyy-MM-dd"), 
                predictedBalance = balance 
            });
        }
        return predictions;
    }
}

public class PredictionRequest
{
    public int Months { get; set; } = 3;
}
