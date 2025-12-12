import { MapPin, Navigation, Car, Clock, Zap } from 'lucide-react'

const TrafficFlowMap = ({ traffic }) => {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Incoming Traffic Analysis</h3>
      
      {/* Traffic summary */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-3 bg-slate-700/30 rounded-lg">
          <Car size={24} className="mx-auto mb-2 text-primary-400" />
          <p className="text-2xl font-bold">{traffic.approaching}</p>
          <p className="text-xs text-slate-400">Approaching</p>
        </div>
        <div className="text-center p-3 bg-slate-700/30 rounded-lg">
          <Clock size={24} className="mx-auto mb-2 text-warning" />
          <p className="text-2xl font-bold">{traffic.eta}</p>
          <p className="text-xs text-slate-400">Avg ETA (min)</p>
        </div>
        <div className="text-center p-3 bg-slate-700/30 rounded-lg">
          <Navigation size={24} className="mx-auto mb-2 text-success" />
          <p className="text-2xl font-bold">{traffic.routes}</p>
          <p className="text-xs text-slate-400">Active Routes</p>
        </div>
      </div>

      {/* Simplified map visualization */}
      <div className="relative bg-slate-900 rounded-lg p-6 h-64 border border-slate-700">
        {/* Station location */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="relative">
            <div className="w-16 h-16 bg-success rounded-full flex items-center justify-center animate-pulse">
              <Zap size={32} className="text-white" />
            </div>
            <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
              <span className="text-xs font-semibold bg-slate-800 px-2 py-1 rounded">Your Station</span>
            </div>
          </div>
        </div>

        {/* Incoming vehicles indicators */}
        {traffic.vehicles?.map((vehicle, index) => {
          const positions = [
            { top: '20%', left: '20%' },
            { top: '30%', right: '25%' },
            { bottom: '25%', left: '30%' },
            { bottom: '20%', right: '20%' },
          ]
          const pos = positions[index % 4]
          
          return (
            <div
              key={vehicle.id}
              className="absolute"
              style={pos}
            >
              <div className="relative group">
                <Car size={20} className="text-primary-400" />
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block">
                  <div className="bg-slate-800 border border-slate-700 px-2 py-1 rounded text-xs whitespace-nowrap">
                    <p className="font-semibold">{vehicle.type}</p>
                    <p className="text-slate-400">ETA: {vehicle.eta} min</p>
                    <p className="text-slate-400">Route: {vehicle.route}</p>
                  </div>
                </div>
                {/* Direction arrow */}
                <div className="absolute top-1/2 left-1/2">
                  <div className="w-px h-8 bg-primary-400/50" 
                       style={{ 
                         transform: `rotate(${45 * index}deg) translateY(-100%)`
                       }} 
                  />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Traffic routes list */}
      <div className="mt-4 space-y-2">
        <p className="text-sm font-semibold text-slate-400">Detected Routes:</p>
        {traffic.routeDetails?.map((route, index) => (
          <div key={index} className="flex items-center justify-between text-sm bg-slate-800/50 p-2 rounded">
            <span className="flex items-center gap-2">
              <Navigation size={14} className="text-primary-400" />
              {route.name}
            </span>
            <span className="text-slate-400">{route.vehicles} vehicles</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TrafficFlowMap
