import { Activity, Zap, Clock, TrendingUp, AlertCircle } from 'lucide-react'

const ChargerPerformanceTable = ({ chargers }) => {
  const getPerformanceColor = (score) => {
    if (score >= 85) return 'text-success'
    if (score >= 70) return 'text-primary-400'
    if (score >= 50) return 'text-warning'
    return 'text-danger'
  }

  const getStatusIndicator = (status) => {
    const indicators = {
      occupied: { color: 'bg-primary-400', text: 'In Use' },
      available: { color: 'bg-success', text: 'Available' },
      maintenance: { color: 'bg-warning', text: 'Maintenance' },
      offline: { color: 'bg-danger', text: 'Offline' },
    }
    return indicators[status] || indicators.offline
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Charger Performance Overview</h3>
        <button className="text-xs text-primary-400 hover:text-primary-300 font-semibold">
          View Detailed Report →
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700 text-left">
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Charger</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Status</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Utilization</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Sessions (24h)</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Revenue (24h)</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Avg Session</th>
              <th className="py-3 px-4 text-xs font-semibold text-slate-400">Performance</th>
            </tr>
          </thead>
          <tbody>
            {chargers.map((charger) => {
              const indicator = getStatusIndicator(charger.status)
              return (
                <tr key={charger.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                  <td className="py-3 px-4">
                    <div>
                      <p className="font-medium">{charger.name}</p>
                      <p className="text-xs text-slate-500">{charger.type}</p>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${indicator.color}`} />
                      <span className="text-sm">{indicator.text}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${
                            charger.utilization >= 80 ? 'bg-danger' :
                            charger.utilization >= 60 ? 'bg-warning' : 'bg-success'
                          }`}
                          style={{ width: `${charger.utilization}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold w-12">{charger.utilization}%</span>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-sm font-medium">{charger.sessions}</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-sm font-semibold text-success">${charger.revenue}</span>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className="text-sm">{charger.avgSession} min</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-semibold ${getPerformanceColor(charger.performance)}`}>
                        {charger.performance}
                      </span>
                      {charger.performance < 70 && (
                        <AlertCircle size={14} className="text-warning" />
                      )}
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Summary stats */}
      <div className="mt-4 pt-4 border-t border-slate-700 grid grid-cols-4 gap-4">
        <div className="text-center">
          <p className="text-xs text-slate-400">Total Sessions</p>
          <p className="text-xl font-bold text-primary-400">
            {chargers.reduce((sum, c) => sum + c.sessions, 0)}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-400">Total Revenue</p>
          <p className="text-xl font-bold text-success">
            ${chargers.reduce((sum, c) => sum + c.revenue, 0).toFixed(2)}
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-400">Avg Utilization</p>
          <p className="text-xl font-bold text-primary-400">
            {Math.round(chargers.reduce((sum, c) => sum + c.utilization, 0) / chargers.length)}%
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-400">Avg Performance</p>
          <p className="text-xl font-bold text-success">
            {Math.round(chargers.reduce((sum, c) => sum + c.performance, 0) / chargers.length)}
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChargerPerformanceTable
