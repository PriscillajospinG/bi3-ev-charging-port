import { useEffect, useState } from 'react'
import { Activity, Zap, TrendingUp, AlertCircle } from 'lucide-react'
import TrafficStats from '../components/Monitoring/TrafficStats'
import ChargerCard from '../components/Monitoring/ChargerCard'
import UtilizationChart from '../components/Analytics/UtilizationChart'
import OccupancyPieChart from '../components/Analytics/OccupancyPieChart'
import { api } from '../services/api'
import useAppStore from '../store/useAppStore'
import websocket from '../services/websocket'

const Dashboard = () => {
  const [timeRange, setTimeRange] = useState('24h')
  const { 
    currentMetrics, 
    chargers, 
    utilizationData,
    occupancyData,
    setCurrentMetrics,
    setChargers,
    setUtilizationData,
    setOccupancyData
  } = useAppStore()

  useEffect(() => {
    // Fetch initial data
    fetchDashboardData()

    // Setup WebSocket listeners
    websocket.on('metrics_update', handleMetricsUpdate)
    websocket.on('charger_update', handleChargerUpdate)

    return () => {
      websocket.off('metrics_update', handleMetricsUpdate)
      websocket.off('charger_update', handleChargerUpdate)
    }
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [metricsRes, chargersRes, utilizationRes, occupancyRes] = await Promise.all([
        api.getCurrentMetrics(),
        api.getChargers(),
        api.getUtilizationData({ range: '24h' }),
        api.getOccupancyStats(),
      ])

      setCurrentMetrics(metricsRes.data)
      setChargers(chargersRes.data)
      setUtilizationData(utilizationRes.data)
      setOccupancyData(occupancyRes.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      // Use mock data for demo
      setMockData()
    }
  }

  const setMockData = () => {
    setCurrentMetrics({
      currentQueue: 8,
      queueChange: 2,
      vehiclesDetected: 142,
      avgDwellTime: '23 min',
      dwellChange: 5,
      peakPrediction: '4:30 PM',
      peakTime: '4:30 PM',
    })

    setChargers([
      {
        id: 1,
        name: 'Charger A1',
        location: 'Zone A - Bay 1',
        status: 'occupied',
        power: 150,
        type: 'DC Fast',
        sessionTime: '45 min',
        energyDelivered: 38.5,
        utilization: 85,
      },
      {
        id: 2,
        name: 'Charger A2',
        location: 'Zone A - Bay 2',
        status: 'available',
        power: 150,
        type: 'DC Fast',
        utilization: 62,
      },
      {
        id: 3,
        name: 'Charger B1',
        location: 'Zone B - Bay 1',
        status: 'occupied',
        power: 50,
        type: 'Level 2',
        sessionTime: '1h 20m',
        energyDelivered: 22.3,
        utilization: 78,
      },
      {
        id: 4,
        name: 'Charger B2',
        location: 'Zone B - Bay 2',
        status: 'maintenance',
        power: 50,
        type: 'Level 2',
        maintenanceNote: 'Scheduled maintenance',
        utilization: 45,
      },
    ])

    setUtilizationData(
      Array.from({ length: 24 }, (_, i) => ({
        time: `${i}:00`,
        utilization: Math.floor(Math.random() * 40) + 30,
      }))
    )

    setOccupancyData([
      { name: 'Available', value: 12 },
      { name: 'Occupied', value: 8 },
      { name: 'Maintenance', value: 2 },
      { name: 'Offline', value: 1 },
    ])
  }

  const handleMetricsUpdate = (data) => {
    setCurrentMetrics(data)
  }

  const handleChargerUpdate = (data) => {
    useAppStore.getState().updateCharger(data.chargerId, data.updates)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-slate-400 mt-1">Real-time overview of EV charging operations</p>
        </div>
        <div className="flex items-center gap-2">
          {['24h', '7d', '30d'].map((range) => (
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

      {/* Traffic Stats */}
      <TrafficStats stats={currentMetrics || {}} />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Utilization Trend</h3>
          <UtilizationChart data={utilizationData} type="area" />
        </div>
        <OccupancyPieChart data={occupancyData} />
      </div>

      {/* Chargers Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Active Chargers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {chargers.map((charger) => (
            <ChargerCard key={charger.id} charger={charger} />
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card bg-gradient-to-r from-primary-600 to-primary-700">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold mb-2">Need Insights?</h3>
            <p className="text-primary-100">
              Check predictions and recommendations to optimize your charging infrastructure
            </p>
          </div>
          <div className="flex gap-3">
            <a href="/predictions" className="btn-secondary">
              View Predictions
            </a>
            <a href="/recommendations" className="bg-white text-primary-700 font-semibold py-2 px-4 rounded-lg hover:bg-primary-50 transition-colors">
              Get Recommendations
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
