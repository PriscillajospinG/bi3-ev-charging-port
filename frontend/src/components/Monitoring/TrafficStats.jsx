import { Users, Car, TrendingUp, Activity } from 'lucide-react'

const TrafficStats = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="card bg-gradient-to-br from-primary-600 to-primary-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-primary-100">Current Queue</p>
            <p className="text-3xl font-bold mt-2">{stats.currentQueue}</p>
            <p className="text-xs text-primary-200 mt-1">
              {stats.queueChange > 0 ? '↑' : '↓'} {Math.abs(stats.queueChange)} from avg
            </p>
          </div>
          <Users size={40} className="text-primary-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-success to-emerald-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-emerald-100">Vehicles Detected</p>
            <p className="text-3xl font-bold mt-2">{stats.vehiclesDetected}</p>
            <p className="text-xs text-emerald-200 mt-1">Last hour</p>
          </div>
          <Car size={40} className="text-emerald-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-warning to-orange-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-orange-100">Avg Dwell Time</p>
            <p className="text-3xl font-bold mt-2">{stats.avgDwellTime}</p>
            <p className="text-xs text-orange-200 mt-1">
              {stats.dwellChange > 0 ? '↑' : '↓'} {Math.abs(stats.dwellChange)} min
            </p>
          </div>
          <Activity size={40} className="text-orange-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-purple-600 to-purple-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-purple-100">Peak Prediction</p>
            <p className="text-3xl font-bold mt-2">{stats.peakPrediction}</p>
            <p className="text-xs text-purple-200 mt-1">Expected at {stats.peakTime}</p>
          </div>
          <TrendingUp size={40} className="text-purple-200" />
        </div>
      </div>
    </div>
  )
}

export default TrafficStats
