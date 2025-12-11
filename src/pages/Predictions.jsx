import { useState } from 'react'
import PredictionCard from '../components/Predictions/PredictionCard'
import DemandForecast from '../components/Predictions/DemandForecast'
import { Calendar, TrendingUp } from 'lucide-react'

const Predictions = () => {
  const [forecastPeriod, setForecastPeriod] = useState('7d')

  const predictions = [
    {
      title: 'Peak Demand Today',
      timeframe: 'Next 8 hours',
      value: 18,
      unit: 'vehicles',
      trend: 'up',
      confidence: 87,
      description: 'Expected peak at 4:30 PM based on historical patterns',
      recommendation: 'Ensure all chargers in Zone A are operational',
    },
    {
      title: 'Weekend Forecast',
      timeframe: 'Sat-Sun',
      value: 245,
      unit: 'total sessions',
      trend: 'up',
      confidence: 73,
      description: 'Higher than usual weekend activity expected',
      recommendation: 'Consider deploying mobile charger to Zone C',
    },
    {
      title: 'Next Week Demand',
      timeframe: 'Dec 12-18',
      value: 892,
      unit: 'sessions',
      trend: 'up',
      confidence: 81,
      description: 'Steady increase due to holiday travel',
    },
    {
      title: 'Seasonal Trend',
      timeframe: 'Q1 2024',
      value: 15,
      unit: '% growth',
      trend: 'up',
      confidence: 69,
      description: 'Quarterly growth projection',
    },
  ]

  const demandData = [
    ...Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      historical: Math.floor(Math.random() * 15) + 5,
      predicted: null,
      upperBound: null,
      lowerBound: null,
    })),
    { time: 'Now', historical: null, predicted: null },
    ...Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      historical: null,
      predicted: Math.floor(Math.random() * 20) + 8,
      upperBound: Math.floor(Math.random() * 25) + 12,
      lowerBound: Math.floor(Math.random() * 10) + 3,
    })),
  ]

  const forecastStats = {
    peak: 18,
    peakTime: '4:30 PM',
    average: 12,
    accuracy: 87,
  }

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
                className={`px-4 py-2 rounded-lg transition-colors ${
                  forecastPeriod === period
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
