import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [historyRange, setHistoryRange] = useState(6); // Default 6 months
  const [predictRange, setPredictRange] = useState(3); // Default 3 months
  const [hasPredicted, setHasPredicted] = useState(false);

  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/transactions');
      const data = await response.json();
      // Sort transactions by date
      const sortedTransactions = data.data.transactionItems.sort((a, b) => 
        new Date(a.transactionDate) - new Date(b.transactionDate)
      );
      setTransactions(sortedTransactions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setLoading(false);
    }
  };

  const filterTransactions = () => {
    if (transactions.length === 0) {
      setFilteredTransactions([]);
      return;
    }

    if (historyRange === 'all') {
      setFilteredTransactions(transactions);
      return;
    }

    // Use the latest transaction date as the anchor (current date)
    const dates = transactions.map(t => new Date(t.transactionDate).getTime());
    const latestDate = new Date(Math.max(...dates));
    
    const cutoffDate = new Date(latestDate);
    cutoffDate.setMonth(cutoffDate.getMonth() - parseInt(historyRange));

    const filtered = transactions.filter(t => new Date(t.transactionDate) >= cutoffDate);
    setFilteredTransactions(filtered);
  };

  const fetchPrediction = async () => {
    setHasPredicted(true);
    try {
      const response = await fetch('http://localhost:5000/api/prediction', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ months: parseInt(predictRange) }),
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

  useEffect(() => {
    fetchTransactions();
  }, []);

  useEffect(() => {
    filterTransactions();
  }, [transactions, historyRange]);

  useEffect(() => {
    if (hasPredicted) {
      fetchPrediction();
    }
  }, [predictRange]);

  const chartData = {
    datasets: [
      {
        label: 'Historical Balance',
        data: filteredTransactions.map(t => ({ x: t.transactionDate, y: t.balance })),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'Predicted Balance',
        data: [
            ...(filteredTransactions.length > 0 ? [{
                x: filteredTransactions[filteredTransactions.length - 1].transactionDate,
                y: filteredTransactions[filteredTransactions.length - 1].balance
            }] : []),
            ...predictions
            .filter(p => {
                if (filteredTransactions.length === 0) return true;
                const lastHistoryDate = new Date(filteredTransactions[filteredTransactions.length - 1].transactionDate);
                return new Date(p.date) > lastHistoryDate;
            })
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .map(p => ({ x: p.date, y: p.predictedBalance }))
        ],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderDash: [5, 5],
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'month'
        }
      }
    },
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
      
      <div style={{ marginBottom: '20px', display: 'flex', gap: '20px', alignItems: 'center' }}>
        <div>
          <label style={{ marginRight: '10px' }}>History Range:</label>
          <select 
            value={historyRange} 
            onChange={(e) => setHistoryRange(e.target.value)}
            style={{ padding: '5px' }}
          >
            <option value="3">Last 3 Months</option>
            <option value="6">Last 6 Months</option>
            <option value="12">Last 12 Months</option>
            <option value="all">All Time</option>
          </select>
        </div>

        <div>
          <label style={{ marginRight: '10px' }}>Prediction Range:</label>
          <select 
            value={predictRange} 
            onChange={(e) => setPredictRange(e.target.value)}
            style={{ padding: '5px' }}
          >
            <option value="3">Next 3 Months</option>
            <option value="6">Next 6 Months</option>
            <option value="9">Next 9 Months</option>
            <option value="12">Next 12 Months</option>
          </select>
        </div>

        <button onClick={fetchPrediction} style={{ padding: '5px 15px' }}>
          Predict Future Balance
        </button>
      </div>

      {loading ? (
        <p>Loading data...</p>
      ) : (
        <div style={{ height: '500px', width: '100%' }}>
            <Line key={`${historyRange}-${predictRange}-${filteredTransactions.length}`} options={options} data={chartData} />
        </div>
      )}
      
      <h2>Recent Transactions</h2>
      <ul style={{ maxHeight: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
        {filteredTransactions.map((t) => (
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
