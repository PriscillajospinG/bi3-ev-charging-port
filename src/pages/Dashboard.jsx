import { useEffect, useState } from 'react'
import { Activity, Zap, TrendingUp, AlertCircle } from 'lucide-react'
import TrafficStats from '../components/Monitoring/TrafficStats'
import ChargerCard from '../components/Monitoring/ChargerCard'
import UtilizationChart from '../components/Analytics/UtilizationChart'
import OccupancyPieChart from '../components/Analytics/OccupancyPieChart'
import LiveOccupancy from '../components/Dashboard/LiveOccupancy'
import TrafficFlowMap from '../components/Dashboard/TrafficFlowMap'
import RevenueMetrics from '../components/Dashboard/RevenueMetrics'
import ChargerPerformanceTable from '../components/Dashboard/ChargerPerformanceTable'
import AlertsPanel from '../components/Dashboard/AlertsPanel'
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

  const [occupancy, setOccupancy] = useState({
    total: 23,
    occupied: 18,
    available: 5,
    queueLength: 4,
    avgWaitTime: 12,
  })

  const [traffic, setTraffic] = useState({
    approaching: 12,
    eta: 8,
    routes: 3,
    vehicles: [
      { id: 1, type: 'Tesla Model 3', eta: 5, route: 'Highway 101' },
      { id: 2, type: 'Nissan Leaf', eta: 8, route: 'Main St' },
      { id: 3, type: 'Chevy Bolt', eta: 12, route: 'Oak Ave' },
      { id: 4, type: 'Ford Mach-E', eta: 6, route: 'Highway 101' },
    ],
    routeDetails: [
      { name: 'Highway 101 North', vehicles: 7 },
      { name: 'Main Street', vehicles: 3 },
      { name: 'Oak Avenue', vehicles: 2 },
    ],
  })

  const [revenueMetrics, setRevenueMetrics] = useState({
    todayRevenue: 1247.50,
    todayChange: 8.3,
    weekRevenue: 7832.20,
    avgDailyRevenue: 1118.89,
    monthRevenue: 28456.80,
    monthProgress: 72,
    projectedRevenue: 39500,
  })

  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'critical',
      title: 'High Queue Detected',
      message: '4 vehicles waiting, 18/23 chargers occupied. Consider deploying mobile unit.',
      location: 'Zone A',
      timestamp: new Date(),
      action: 'Deploy Mobile Charger',
    },
    {
      id: 2,
      type: 'warning',
      title: 'Charger B2 Downtime',
      message: 'Charger has been offline for 3 hours. Maintenance required.',
      location: 'Zone B - Bay 2',
      timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
      action: 'Schedule Maintenance',
    },
    {
      id: 3,
      type: 'warning',
      title: 'Prolonged Session - Possible Misuse',
      message: 'Vehicle at Charger A3 has been connected for 4.5 hours with charging complete.',
      location: 'Zone A - Bay 3',
      timestamp: new Date(Date.now() - 30 * 60 * 1000),
      action: 'Send Notification',
    },
    {
      id: 4,
      type: 'info',
      title: 'Peak Hour Approaching',
      message: 'High demand predicted at 4:30 PM. Ensure all chargers operational.',
      timestamp: new Date(Date.now() - 15 * 60 * 1000),
    },
  ])

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
        sessions: 28,
        revenue: 324.50,
        avgSession: 42,
        performance: 92,
      },
      {
        id: 2,
        name: 'Charger A2',
        location: 'Zone A - Bay 2',
      {/* Revenue Metrics - Owner's Primary KPI */}
      <RevenueMetrics metrics={revenueMetrics} />

      {/* Critical Info Row - Occupancy & Traffic */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LiveOccupancy occupancy={occupancy} />
        <TrafficFlowMap traffic={traffic} />
      </div>

      {/* Alerts - Misuse, Queues, Downtime */}
      <AlertsPanel alerts={alerts} />

      {/* Charger Performance & Utilization */}
      <ChargerPerformanceTable chargers={chargers} />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Utilization Trend (24h)</h3>
          <UtilizationChart data={utilizationData} type="area" />
        </div>
        <OccupancyPieChart data={occupancyData} />
      </div>nue: 189.60,
        avgSession: 52,
        performance: 85,
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
        sessions: 18,
        revenue: 98.40,
        avgSession: 48,
        performance: 65,
      },
      {
        id: 5,
        name: 'Charger C1',
        location: 'Zone C - Bay 1',
        status: 'occupied',
        power: 150,
        type: 'DC Fast',
        sessionTime: '32 min',
        energyDelivered: 28.2,
        utilization: 91,
        sessions: 31,
        revenue: 358.90,
        avgSession: 35,
        performance: 94,
      },
      {
        id: 6,
        name: 'Charger C2',
        location: 'Zone C - Bay 2',
        status: 'available',
        power: 50,
        type: 'Level 2',
        utilization: 58,
        sessions: 25,
        revenue: 145.20,
        avgSession: 45,
        performance: 82,
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
