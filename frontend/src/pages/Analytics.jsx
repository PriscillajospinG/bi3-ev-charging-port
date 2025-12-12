import { useState, useEffect } from 'react'
import { Download, Calendar } from 'lucide-react'
import UtilizationChart from '../components/Analytics/UtilizationChart'
import HeatMap from '../components/Analytics/HeatMap'
import OccupancyPieChart from '../components/Analytics/OccupancyPieChart'
import { api } from '../services/api'

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d')
  const [utilizationData, setUtilizationData] = useState([])
  const [occupancyData, setOccupancyData] = useState([
    { name: 'Available', value: 0 },
    { name: 'Occupied', value: 0 },
    { name: 'Maintenance', value: 0 },
    { name: 'Offline', value: 0 },
  ])
  const [weeklyTrend, setWeeklyTrend] = useState([])
  const [metrics, setMetrics] = useState({
    avgUtilization: '0%',
    totalSessions: 0,
    energy: 0,
    revenue: '$0'
  })
  const [chargers, setChargers] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, utilRes, chargersRes] = await Promise.all([
          api.getAnalyticsSummary(),
          api.getUtilizationTrend(),
          api.getChargers()
        ])

        // Map Metrics
        const s = summaryRes.data;
        setMetrics({
          avgUtilization: s.avg_utilization || '0%',
          totalSessions: s.total_sessions || 0,
          energy: s.energy_delivered || 0,
          revenue: s.revenue || '$0'
        })

        // Map Util Data (using same trend for now as backend provides 24h profile)
        const trend = utilRes.data.map(item => ({
          time: item.hour,
          utilization: item.utilization
        }));
        setUtilizationData(trend);
        // Simulate weekly by repeating/shifting for now as backend 'daily' mock endpoint reuses this
        setWeeklyTrend(trend.slice(0, 7).map((t, i) => ({
          time: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i],
          utilization: t.utilization
        })));

        // Map Chargers & Occupancy
        const cList = chargersRes.data;
        setChargers(cList);

        const occCounts = { Available: 0, Occupied: 0, Maintenance: 0, Offline: 0 };
        cList.forEach(c => {
          let status = c.status === 'In Use' ? 'Occupied' : c.status;
          if (!occCounts[status] && status !== 'Occupied') status = 'Available'; // fallback
          if (occCounts[status] !== undefined) occCounts[status]++;
        });
        setOccupancyData([
          { name: 'Available', value: occCounts.Available },
          { name: 'Occupied', value: occCounts.Occupied },
          { name: 'Maintenance', value: occCounts.Maintenance },
          { name: 'Offline', value: occCounts.Offline },
        ]);

      } catch (e) {
        console.error("Failed to fetch analytics", e);
      }
    }
    fetchData();
  }, [timeRange])

  const exportReport = () => {
    console.log('Exporting analytics report...')
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
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Avg Utilization</p>
          <p className="text-3xl font-bold text-primary-400">{metrics.avgUtilization}</p>
          <p className="text-xs text-success mt-1">↑ 5.3% from last period</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Total Sessions</p>
          <p className="text-3xl font-bold text-primary-400">{metrics.totalSessions.toLocaleString()}</p>
          <p className="text-xs text-success mt-1">↑ 12.4% from last period</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Energy Delivered</p>
          <p className="text-3xl font-bold text-primary-400">{metrics.energy.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">kWh</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-400 mb-1">Revenue</p>
          <p className="text-3xl font-bold text-success">{metrics.revenue}</p>
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
              {chargers.map((c, i) => (
                <tr key={c.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                  <td className="py-3 px-4 font-medium">{c.name}</td>
                  <td className="py-3 px-4">{c.sessions}</td>
                  <td className="py-3 px-4">
                    <span className="text-primary-400 font-semibold">
                      {c.utilization}%
                    </span>
                  </td>
                  <td className="py-3 px-4">{c.energyDelivered || '-'}</td>
                  <td className="py-3 px-4 text-success">${c.revenue || '0.00'}</td>
                  <td className="py-3 px-4">{c.avgSession || 0} min</td>
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
