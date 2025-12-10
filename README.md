# Show Me The Money

This is a full-stack web application designed to visualize transaction history and predict future cash flow using LLM integration.

## Prerequisites

- .NET 9.0 SDK
- Node.js (v20+)
- Python 3 (for generating mock data)

## Project Structure

- `backend/`: ASP.NET Core Web API (.NET 9)
- `frontend/`: React + Vite application
- `scripts/`: Python scripts for data generation

## Setup & Run

### 1. Generate Mock Data

First, generate the mock transaction data that serves as the "database" for this demo.

```bash
python scripts/generate_mock_data.py
```

This will create a `mock_transactions.json` file in the project root.

### 2. Backend (.NET Web API)

Navigate to the backend directory and run the API.

```bash
cd backend
dotnet run
```

The API will start at `http://localhost:5000`.
- Swagger UI: `http://localhost:5000/swagger`
- Transactions Endpoint: `http://localhost:5000/api/transactions`

**Configuration:**
To use real Azure OpenAI for predictions, configure your credentials using .NET User Secrets (recommended for security):

```bash
dotnet user-secrets init
dotnet user-secrets set "AzureOpenAI:Endpoint" "https://YOUR_RESOURCE_NAME.openai.azure.com/"
dotnet user-secrets set "AzureOpenAI:ApiKey" "YOUR_API_KEY"
dotnet user-secrets set "AzureOpenAI:DeploymentName" "YOUR_DEPLOYMENT_NAME"
```

If not configured, the app will use a mock random-walk prediction algorithm.

### 3. Frontend (React)

Open a new terminal, navigate to the frontend directory, install dependencies, and start the dev server.

```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:5173`.

## Features

- **Cash Trend Diagram**: Visualizes historical account balance using Chart.js.
- **Transaction List**: Displays a scrollable list of recent transactions.
- **AI Prediction**: "Predict Future Cash Flow" button calls the backend to generate a 3-month cash flow forecast (simulated or via Azure OpenAI).
