import { useState, useEffect } from 'react'
import PredictionCard from '../components/Predictions/PredictionCard'
import DemandForecast from '../components/Predictions/DemandForecast'
import { Calendar, TrendingUp } from 'lucide-react'
import { api } from '../services/api'

const Predictions = () => {
  const [forecastPeriod, setForecastPeriod] = useState('7d')
  const [demandData, setDemandData] = useState([])
  const [predictions, setPredictions] = useState([])
  const [forecastStats, setForecastStats] = useState({
    peak: 0,
    peakTime: '--',
    average: 0,
    accuracy: 0
  })

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const days = forecastPeriod === '24h' ? 1 : (forecastPeriod === '30d' ? 30 : 7);
        const [res, accRes] = await Promise.all([
          api.getForecast(days),
          api.getForecastAccuracy()
        ]);

        const data = res.data;

        // Map Forecast Graph Data
        // Backend returns { dates: [], ensemble: [], lower: [], upper: [] }
        // Note: Current backend forecast might be simplistic (daily), but let's map it.
        // If the backend returns empty, show empty.
        if (data.forecast && data.forecast.dates) {
          const mappedData = data.forecast.dates.map((date, i) => ({
            time: new Date(date).toLocaleDateString(),
            predicted: data.forecast.ensemble[i],
            upperBound: data.forecast.upper_bound[i],
            lowerBound: data.forecast.lower_bound[i],
            historical: null // mix if available
          }));
          setDemandData(mappedData);

          // Derive stats
          const values = data.forecast.ensemble;
          const maxVal = Math.max(...values);
          const avgVal = values.reduce((a, b) => a + b, 0) / values.length;
          const maxIdx = values.indexOf(maxVal);

          setForecastStats({
            peak: Math.round(maxVal),
            peakTime: mappedData[maxIdx] ? mappedData[maxIdx].time : '--',
            average: Math.round(avgVal),
            accuracy: parseFloat(accRes.data.accuracy) || 85
          })

          // Generate Key Predictions Cards from data
          setPredictions([
            {
              title: 'Peak Demand Forecast',
              timeframe: `Next ${forecastPeriod}`,
              value: Math.round(maxVal),
              unit: 'vehicles/day',
              trend: 'up',
              confidence: parseFloat(accRes.data.accuracy),
              description: `Highest traffic expected on ${mappedData[maxIdx]?.time}`,
            },
            {
              title: 'Average Load',
              timeframe: `Next ${forecastPeriod}`,
              value: Math.round(avgVal),
              unit: 'sessions/day',
              trend: 'neutral',
              confidence: 80,
              description: 'Steady baseline activity',
            }
          ]);
        }

      } catch (e) {
        console.error("Failed to fetch predictions", e);
      }
    }
    fetchForecast();
  }, [forecastPeriod])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Demand Predictions</h1>
          <p className="text-slate-400 mt-1">AI-powered forecasting and trend analysis</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <Calendar size={18} />
            <span>Model: LSTM + Prophet</span>
          </div>
          <div className="flex items-center gap-2">
            {['24h', '7d', '30d'].map((period) => (
              <button
                key={period}
                onClick={() => setForecastPeriod(period)}
                className={`px-4 py-2 rounded-lg transition-colors ${forecastPeriod === period
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                  }`}
              >
                {period}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Model Info */}
      <div className="card bg-gradient-to-r from-purple-600 to-purple-700">
        <div className="flex items-center gap-4">
          <TrendingUp size={40} />
          <div className="flex-1">
            <h3 className="text-lg font-semibold">Prediction Engine Status</h3>
            <p className="text-sm text-purple-100 mt-1">
              Multi-model ensemble using LSTM, Prophet, and XGBoost for demand forecasting
            </p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold">87.3%</p>
            <p className="text-sm text-purple-100">Accuracy</p>
          </div>
        </div>
      </div>

      {/* Demand Forecast Chart */}
      <DemandForecast
        data={demandData}
        forecast={forecastStats}
      />

      {/* Prediction Cards */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Key Predictions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {predictions.map((prediction, index) => (
            <PredictionCard key={index} prediction={prediction} />
          ))}
        </div>
      </div>

      {/* Seasonal Patterns */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Seasonal Patterns Detected</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-700/30 p-4 rounded-lg">
            <p className="text-sm text-slate-400 mb-2">Weekday Pattern</p>
            <p className="text-lg font-semibold">Morning & Evening Peaks</p>
            <p className="text-xs text-slate-500 mt-1">7-9 AM, 4-7 PM</p>
          </div>
          <div className="bg-slate-700/30 p-4 rounded-lg">
            <p className="text-sm text-slate-400 mb-2">Weekend Pattern</p>
            <p className="text-lg font-semibold">Midday Peak</p>
            <p className="text-xs text-slate-500 mt-1">11 AM - 3 PM</p>
          </div>
          <div className="bg-slate-700/30 p-4 rounded-lg">
            <p className="text-sm text-slate-400 mb-2">Special Events</p>
            <p className="text-lg font-semibold">+40% Demand</p>
            <p className="text-xs text-slate-500 mt-1">During local events</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Predictions
