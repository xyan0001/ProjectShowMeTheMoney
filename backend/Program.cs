using Microsoft.SemanticKernel;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Semantic Kernel Configuration
var openAiEndpoint = builder.Configuration["AzureOpenAI:Endpoint"];
var openAiApiKey = builder.Configuration["AzureOpenAI:ApiKey"];
var openAiDeploymentName = builder.Configuration["AzureOpenAI:DeploymentName"];

if (!string.IsNullOrEmpty(openAiEndpoint) && !string.IsNullOrEmpty(openAiApiKey) && !string.IsNullOrEmpty(openAiDeploymentName))
{
    var kernel = Kernel.CreateBuilder()
        .AddAzureOpenAIChatCompletion(openAiDeploymentName, openAiEndpoint, openAiApiKey)
        .Build();
    builder.Services.AddSingleton(kernel);
}

// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        builder =>
        {
            builder.AllowAnyOrigin()
                   .AllowAnyMethod()
                   .AllowAnyHeader();
        });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseCors("AllowAll");
app.UseAuthorization();

app.MapControllers();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
