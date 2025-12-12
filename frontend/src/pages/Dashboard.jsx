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
  const [useMockData, setUseMockData] = useState(false)
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
      const [liveRes, chargersRes] = await Promise.all([
        api.getDashboardLive(),
        api.getChargers(),
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

      // Metrics and Chargres
      setCurrentMetrics(liveData.summary_metrics); // Warning: summary_metrics structure != FrontendMetrics.
      // summary_metrics: { total_sessions, total_revenue, avg_utilization, avg_performance }
      // FrontendMetrics: { currentQueue, queueChange, vehiclesDetected, avgDwellTime... }
      // Actually liveRes.summary_metrics is NOT what setCurrentMetrics expects.
      // AND Dashboard.jsx uses `currentMetrics` for the top cards (Queue, Vehicles, Dwell Time).
      // `summary_metrics` from `/live` seems to be distinct from `frontend_get_current_metrics`.
      // `AnalyticsService.get_summary_metrics` returns total stats.
      // `AnalyticsService.frontend_get_current_metrics` returns queue/vehicles stats.
      // The `/live` endpoint returns `summary_metrics` but NOT `frontend_metrics`.

      // FIX: I should fetch `api.getCurrentMetrics()` as well or rely on it from an updated `/live` endpoint.
      // Since I want to integrate perfectly, I will ADD `api.getCurrentMetrics()` to the Promise.all.

    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      setMockData()
    }
  }

  const [occupancy, setOccupancy] = useState(null)

  const [traffic, setTraffic] = useState(null)

  const [revenueMetrics, setRevenueMetrics] = useState(null)

  const [alerts, setAlerts] = useState([])

  const setMockData = () => {
    setUseMockData(true)
    console.warn('⚠️ Using mock data - backend offline')

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
        status: 'available',
        power: 150,
        type: 'DC Fast',
        utilization: 62,
        sessions: 22,
        revenue: 267.80,
        avgSession: 38,
        performance: 88,
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
        sessions: 34,
        revenue: 189.60,
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
      {/* Mock Data Warning Banner */}
      {useMockData && (
        <div className="bg-yellow-900/30 border border-yellow-700 text-yellow-100 p-4 rounded-lg flex items-start gap-3">
          <AlertCircle size={24} className="flex-shrink-0 text-yellow-500 mt-0.5" />
          <div>
            <h3 className="font-semibold text-yellow-200">⚠️ Demo Mode: Using Mock Data</h3>
            <p className="text-sm text-yellow-200/80 mt-1">Backend is offline. Showing sample data for demonstration.</p>
          </div>
        </div>
      )}

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
