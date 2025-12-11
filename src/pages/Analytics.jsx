import { useState } from 'react'
import { Download, Calendar } from 'lucide-react'
import UtilizationChart from '../components/Analytics/UtilizationChart'
import HeatMap from '../components/Analytics/HeatMap'
import OccupancyPieChart from '../components/Analytics/OccupancyPieChart'

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d')
  
  const utilizationData = Array.from({ length: 24 }, (_, i) => ({
    time: `${i}:00`,
    utilization: Math.floor(Math.random() * 40) + 30,
  }))

  const occupancyData = [
    { name: 'Available', value: 12 },
    { name: 'Occupied', value: 8 },
    { name: 'Maintenance', value: 2 },
    { name: 'Offline', value: 1 },
  ]

  const weeklyTrend = Array.from({ length: 7 }, (_, i) => ({
    time: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i],
    utilization: Math.floor(Math.random() * 30) + 50,
  }))

  const exportReport = () => {
    console.log('Exporting analytics report...')
    // In production, this would generate and download a PDF/CSV report
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Analytics</h1>
          <p className="text-slate-400 mt-1">Detailed insights and performance metrics</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={exportReport}
            className="btn-secondary flex items-center gap-2"
          >
            <Download size={18} />
            Export Report
          </button>
          <div className="flex items-center gap-2">
            {['24h', '7d', '30d', '90d'].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  timeRange === range
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Avg Utilization</p>
          <p className="text-3xl font-bold text-primary-400">74.2%</p>
          <p className="text-xs text-success mt-1">↑ 5.3% from last period</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Total Sessions</p>
          <p className="text-3xl font-bold text-primary-400">1,284</p>
          <p className="text-xs text-success mt-1">↑ 12.4% from last period</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Energy Delivered</p>
          <p className="text-3xl font-bold text-primary-400">8,432</p>
          <p className="text-xs text-slate-400 mt-1">kWh</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Revenue</p>
          <p className="text-3xl font-bold text-success">$3,847</p>
          <p className="text-xs text-success mt-1">↑ 8.7% from last period</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Daily Utilization Trend</h3>
          <UtilizationChart data={utilizationData} type="line" />
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Weekly Performance</h3>
          <UtilizationChart data={weeklyTrend} type="bar" />
        </div>
      </div>

      {/* Heatmap and Occupancy */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <HeatMap title="Weekly Utilization Heatmap" />
        </div>
        <div className="lg:col-span-1">
          <OccupancyPieChart data={occupancyData} />
        </div>
      </div>

      {/* Detailed Stats Table */}
      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Charger Performance Details</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Charger</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Sessions</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Utilization</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Energy (kWh)</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Revenue</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-slate-400">Avg Session</th>
              </tr>
            </thead>
            <tbody>
              {['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].map((charger, i) => (
                <tr key={charger} className="border-b border-slate-800 hover:bg-slate-800/50">
                  <td className="py-3 px-4 font-medium">Charger {charger}</td>
                  <td className="py-3 px-4">{Math.floor(Math.random() * 100) + 50}</td>
                  <td className="py-3 px-4">
                    <span className="text-primary-400 font-semibold">
                      {Math.floor(Math.random() * 40) + 50}%
                    </span>
                  </td>
                  <td className="py-3 px-4">{(Math.random() * 2000 + 500).toFixed(0)}</td>
                  <td className="py-3 px-4 text-success">${(Math.random() * 1000 + 200).toFixed(2)}</td>
                  <td className="py-3 px-4">{Math.floor(Math.random() * 40) + 20} min</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Analytics
