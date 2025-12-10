import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [transactions, setTransactions] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/transactions');
      const data = await response.json();
      setTransactions(data.data.transactionItems);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setLoading(false);
    }
  };

  const fetchPrediction = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/prediction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ months: 6 }),
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        alert(`Prediction failed: ${errorText}`);
        return;
      }

      const data = await response.json();
      setPredictions(data);
    } catch (error) {
      console.error('Error fetching prediction:', error);
      alert('Error fetching prediction. Check console for details.');
    }
  };

  const chartData = {
    labels: [
        ...transactions.map(t => new Date(t.transactionDate).toLocaleDateString()),
        ...predictions.map(p => new Date(p.date).toLocaleDateString())
    ],
    datasets: [
      {
        label: 'Historical Balance',
        data: transactions.map(t => t.balance),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'Predicted Balance',
        data: [
            ...Array(transactions.length).fill(null), // Pad with nulls for historical period
            ...predictions.map(p => p.predictedBalance)
        ],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderDash: [5, 5],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Cash Flow Trend & Prediction',
      },
    },
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Show Me The Money</h1>
      <button onClick={fetchPrediction} style={{ marginBottom: '20px', padding: '10px 20px' }}>
        Predict Future Cash Flow
      </button>
      
      {loading ? (
        <p>Loading data...</p>
      ) : (
        <div style={{ height: '500px', width: '100%' }}>
            <Line options={options} data={chartData} />
        </div>
      )}
      
      <h2>Recent Transactions</h2>
      <ul style={{ maxHeight: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
        {transactions.map((t) => (
          <li key={t.transactionId} style={{ listStyle: 'none', borderBottom: '1px solid #eee', padding: '5px 0' }}>
            <strong>{new Date(t.transactionDate).toLocaleDateString()}</strong>: {t.description} - 
            <span style={{ color: t.creditAmount > 0 ? 'green' : 'red', marginLeft: '10px' }}>
              ${t.creditAmount > 0 ? t.creditAmount : -t.debitAmount}
            </span>
            <span style={{ float: 'right' }}>Bal: ${t.balance}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
