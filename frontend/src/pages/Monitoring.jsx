import { useState, useEffect } from 'react'

import VideoUpload from '../components/Monitoring/VideoUpload'
import TrafficStats from '../components/Monitoring/TrafficStats'
import ChargerCard from '../components/Monitoring/ChargerCard'
import { api } from '../services/api'

const Monitoring = () => {


  const [stats, setStats] = useState({
    currentQueue: 0,
    queueChange: 0,
    vehiclesDetected: 0,
    avgDwellTime: '0 min',
    dwellChange: 0,
    peakPrediction: '--',
    peakTime: '--',
  })

  const [chargers, setChargers] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsRes, chargersRes] = await Promise.all([
          api.getCurrentMetrics(),
          api.getChargers()
        ])
        setStats(metricsRes.data)
        setChargers(chargersRes.data)
      } catch (e) {
        console.error("Failed to fetch monitoring data", e)
      }
    }
    fetchData()
    // Poll every 10s for monitoring
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Live Monitoring</h1>
        <p className="text-slate-400 mt-1">Upload and process videos with YOLOv11 detection</p>
      </div>

      {/* Video Upload Section */}
      <VideoUpload />

      {/* Current Detection Stats */}
      <div className="card bg-slate-800/50 border border-slate-700">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-4 h-4 bg-slate-400 rounded"></div>
          <h2 className="text-xl font-semibold">Current Detection Stats</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-slate-400 mb-2">Queue Length</p>
            <p className="text-4xl font-bold">{stats.currentQueue}</p>
            <p className="text-xs text-success mt-1">+{stats.queueChange} from last reading</p>
          </div>
          <div>
            <p className="text-sm text-slate-400 mb-2">Avg Dwell Time</p>
            <p className="text-4xl font-bold">{stats.avgDwellTime}</p>
            <p className="text-xs text-success mt-1">+{stats.dwellChange} min</p>
          </div>
        </div>
      </div>



      {/* Live Charger Status */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Charger Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {chargers.map((charger) => (
            <ChargerCard key={charger.id} charger={charger} />
          ))}
        </div>
      </div>

      {/* Detection Pipeline Info */}
      <div className="card bg-slate-800/50 border-primary-500/30">
        <h3 className="text-lg font-semibold mb-3">Detection Pipeline Status</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">Model</p>
            <p className="font-semibold text-primary-400">YOLOv11</p>
          </div>
          <div className="text-center p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">FPS</p>
            <p className="font-semibold text-success">28.4</p>
          </div>
          <div className="text-center p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">Inference Time</p>
            <p className="font-semibold text-warning">35ms</p>
          </div>
          <div className="text-center p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">GPU Usage</p>
            <p className="font-semibold text-primary-400">68%</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Monitoring
