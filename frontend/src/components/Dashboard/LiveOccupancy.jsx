import { Activity, Zap, Battery, TrendingUp } from 'lucide-react'

const LiveOccupancy = ({ occupancy }) => {
  const totalChargers = occupancy.total
  const occupiedChargers = occupancy.occupied
  const availableChargers = occupancy.available
  const occupancyRate = Math.round((occupiedChargers / totalChargers) * 100)

  const getOccupancyStatus = (rate) => {
    if (rate >= 90) return { color: 'danger', label: 'Critical', action: 'Deploy backup charger' }
    if (rate >= 75) return { color: 'warning', label: 'High', action: 'Monitor closely' }
    if (rate >= 50) return { color: 'primary-400', label: 'Moderate', action: 'Normal operation' }
    return { color: 'success', label: 'Low', action: 'Good availability' }
  }

  const status = getOccupancyStatus(occupancyRate)

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Live Occupancy Status</h3>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-danger rounded-full animate-pulse" />
          <span className="text-xs text-slate-400">LIVE</span>
        </div>
      </div>

      {/* Main occupancy display */}
      <div className="text-center mb-6">
        <div className="relative inline-block">
          <svg className="w-48 h-48 transform -rotate-90">
            {/* Background circle */}
            <circle
              cx="96"
              cy="96"
              r="88"
              fill="none"
              stroke="#1e293b"
              strokeWidth="16"
            />
            {/* Progress circle */}
            <circle
              cx="96"
              cy="96"
              r="88"
              fill="none"
              stroke={`var(--color-${status.color})`}
              strokeWidth="16"
              strokeLinecap="round"
              strokeDasharray={`${occupancyRate * 5.53} 553`}
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="text-5xl font-bold">{occupancyRate}%</p>
            <p className="text-sm text-slate-400 mt-1">{status.label} Load</p>
          </div>
        </div>
      </div>

      {/* Charger counts */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center p-3 bg-slate-700/30 rounded-lg">
          <Zap size={20} className="mx-auto mb-2 text-slate-400" />
          <p className="text-2xl font-bold">{totalChargers}</p>
          <p className="text-xs text-slate-400">Total</p>
        </div>
        <div className="text-center p-3 bg-danger/20 rounded-lg border border-danger/30">
          <Battery size={20} className="mx-auto mb-2 text-danger" />
          <p className="text-2xl font-bold text-danger">{occupiedChargers}</p>
          <p className="text-xs text-slate-400">In Use</p>
        </div>
        <div className="text-center p-3 bg-success/20 rounded-lg border border-success/30">
          <Activity size={20} className="mx-auto mb-2 text-success" />
          <p className="text-2xl font-bold text-success">{availableChargers}</p>
          <p className="text-xs text-slate-400">Available</p>
        </div>
      </div>

      {/* Status message */}
      <div className={`p-3 rounded-lg bg-${status.color}/10 border border-${status.color}/30`}>
        <div className="flex items-center gap-2">
          <TrendingUp size={16} className={`text-${status.color}`} />
          <p className="text-sm font-medium">{status.action}</p>
        </div>
      </div>

      {/* Queue info */}
      {occupancy.queueLength > 0 && (
        <div className="mt-4 p-3 bg-warning/10 border border-warning/30 rounded-lg">
          <p className="text-sm font-semibold text-warning">
            ⚠️ {occupancy.queueLength} vehicles waiting
          </p>
          <p className="text-xs text-slate-400 mt-1">
            Avg wait time: {occupancy.avgWaitTime} min
          </p>
        </div>
      )}
    </div>
  )
}

export default LiveOccupancy
