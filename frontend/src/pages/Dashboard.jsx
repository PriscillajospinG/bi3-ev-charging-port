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
      const [liveRes, chargersRes, metricsRes] = await Promise.all([
        api.getDashboardLive(),
        api.getChargers(),
        api.getCurrentMetrics(),
      ])

      const liveData = liveRes.data;

      // Map Revenue Metrics
      // Helper to parse currency string "$1,234.50" -> 1234.50
      const parseCurrency = (str) => {
        if (typeof str === 'number') return str;
        if (!str) return 0;
        return parseFloat(str.replace(/[^0-9.-]+/g, ''));
      }

      // Helper to parse percent string "+5.2%" -> 5.2
      const parsePercent = (str) => {
        if (typeof str === 'number') return str;
        if (!str) return 0;
        return parseFloat(str.replace(/[^0-9.-]+/g, ''));
      }

      setRevenueMetrics({
        todayRevenue: parseCurrency(liveData.revenue_panel.today.actual),
        todayChange: parsePercent(liveData.revenue_panel.today.percent_change),
        weekRevenue: parseCurrency(liveData.revenue_panel.week.total),
        avgDailyRevenue: parseCurrency(liveData.revenue_panel.week.avg_per_day),
        monthRevenue: parseCurrency(liveData.revenue_panel.month.total),
        monthProgress: liveData.revenue_panel.month.target_percent,
        projectedRevenue: parseCurrency(liveData.revenue_panel.month.projected_30d),
      })

      // Map Live Occupancy
      setOccupancy({
        total: liveData.live_occupancy.total_chargers,
        occupied: liveData.live_occupancy.in_use,
        available: liveData.live_occupancy.available,
        queueLength: liveData.live_occupancy.waiting,
        avgWaitTime: parseInt(liveData.live_occupancy.avg_wait_time) || 0,
      })

      // Map Traffic
      setTraffic({
        approaching: liveData.traffic_analysis.approaching,
        eta: liveData.traffic_analysis.eta_avg,
        routes: liveData.traffic_analysis.routes.length,
        vehicles: [], // Backend doesn't provide these yet
        routeDetails: liveData.traffic_analysis.routes.map(r => ({
          name: r.route,
          vehicles: r.count
        })),
      })

      // Map Alerts
      const mappedAlerts = liveData.alerts.map((alert, idx) => ({
        id: idx + 1,
        type: 'warning', // Default to warning as backend doesn't specify
        title: alert.title,
        message: alert.details,
        location: alert.location,
        timestamp: new Date(alert.timestamp === 'Just now' ? Date.now() : alert.timestamp),
        action: 'View Details'
      }));
      setAlerts(mappedAlerts.length > 0 ? mappedAlerts : []);

      // Map Utilization Trend
      setUtilizationData(liveData.utilization_trend.map(item => ({
        time: item.hour,
        utilization: item.utilization
      })));

      // Map Status Distribution to Occupancy Pie Chart
      const dist = liveData.status_distribution;
      setOccupancyData([
        { name: 'Available', value: dist.available.units },
        { name: 'Occupied', value: dist.occupied.units },
        { name: 'Maintenance', value: dist.maintenance.units },
        { name: 'Offline', value: dist.offline.units },
      ]);

      // Metrics & Chargers
      setCurrentMetrics(metricsRes.data)
      setChargers(chargersRes.data)

    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  }

  const [occupancy, setOccupancy] = useState({
    total: 0,
    occupied: 0,
    available: 0,
    queueLength: 0,
    avgWaitTime: 0,
  })

  const [traffic, setTraffic] = useState({
    approaching: 0,
    eta: 0,
    routes: 0,
    vehicles: [],
    routeDetails: [],
  })

  const [revenueMetrics, setRevenueMetrics] = useState({
    todayRevenue: 0,
    todayChange: 0,
    weekRevenue: 0,
    avgDailyRevenue: 0,
    monthRevenue: 0,
    monthProgress: 0,
    projectedRevenue: 0,
  })

  const [alerts, setAlerts] = useState([])

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
              className={`px-4 py-2 rounded-lg transition-colors ${timeRange === range
                ? 'bg-primary-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

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
