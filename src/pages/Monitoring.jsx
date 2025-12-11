import { useState } from 'react'
import CameraFeed from '../components/Monitoring/CameraFeed'
import TrafficStats from '../components/Monitoring/TrafficStats'
import ChargerCard from '../components/Monitoring/ChargerCard'

const Monitoring = () => {
  const [cameras] = useState([
    { id: 1, title: 'Main Entrance', rtspUrl: 'rtsp://camera1/stream', type: 'road' },
    { id: 2, title: 'Zone A - Chargers', rtspUrl: 'rtsp://camera2/stream', type: 'charger' },
    { id: 3, title: 'Zone B - Chargers', rtspUrl: 'rtsp://camera3/stream', type: 'charger' },
    { id: 4, title: 'Exit Lane', rtspUrl: 'rtsp://camera4/stream', type: 'road' },
  ])

  const [stats] = useState({
    currentQueue: 8,
    queueChange: 2,
    vehiclesDetected: 142,
    avgDwellTime: '23 min',
    dwellChange: 5,
    peakPrediction: '4:30 PM',
    peakTime: '4:30 PM',
  })

  const [chargers] = useState([
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
  ])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Live Monitoring</h1>
        <p className="text-slate-400 mt-1">Real-time camera feeds and detection analytics</p>
      </div>

      {/* Traffic Stats */}
      <TrafficStats stats={stats} />

      {/* Camera Feeds */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Camera Feeds</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {cameras.map((camera) => (
            <CameraFeed
              key={camera.id}
              cameraId={camera.id}
              title={camera.title}
              rtspUrl={camera.rtspUrl}
              type={camera.type}
            />
          ))}
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
