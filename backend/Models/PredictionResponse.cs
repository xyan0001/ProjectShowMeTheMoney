using System.Text.Json.Serialization;

namespace ShowMeTheMoney.API.Models;

public class PredictionResponse
{
    [JsonPropertyName("predictions")]
    public List<PredictionItem> Predictions { get; set; }
}

public class PredictionItem
{
    [JsonPropertyName("date")]
    public string Date { get; set; }

    [JsonPropertyName("predictedBalance")]
    public decimal PredictedBalance { get; set; }
}
