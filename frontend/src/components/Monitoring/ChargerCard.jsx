import { Battery, Zap, Clock, AlertTriangle } from 'lucide-react'

const ChargerCard = ({ charger }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'text-success'
      case 'occupied':
        return 'text-primary-400'
      case 'offline':
        return 'text-slate-500'
      case 'maintenance':
        return 'text-warning'
      default:
        return 'text-slate-400'
    }
  }

  const getStatusBg = (status) => {
    switch (status) {
      case 'available':
        return 'bg-success/20'
      case 'occupied':
        return 'bg-primary-500/20'
      case 'offline':
        return 'bg-slate-500/20'
      case 'maintenance':
        return 'bg-warning/20'
      default:
        return 'bg-slate-400/20'
    }
  }

  return (
    <div className={`card border-l-4 ${
      charger.status === 'available' ? 'border-success' :
      charger.status === 'occupied' ? 'border-primary-400' :
      charger.status === 'maintenance' ? 'border-warning' : 'border-slate-600'
    }`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold">{charger.name}</h3>
          <p className="text-sm text-slate-400">{charger.location}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusBg(charger.status)} ${getStatusColor(charger.status)}`}>
          {charger.status.toUpperCase()}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="flex items-center gap-2">
          <Zap size={18} className="text-primary-400" />
          <div>
            <p className="text-xs text-slate-400">Power</p>
            <p className="font-semibold">{charger.power} kW</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Battery size={18} className="text-success" />
          <div>
            <p className="text-xs text-slate-400">Type</p>
            <p className="font-semibold">{charger.type}</p>
          </div>
        </div>

        {charger.status === 'occupied' && (
          <>
            <div className="flex items-center gap-2">
              <Clock size={18} className="text-warning" />
              <div>
                <p className="text-xs text-slate-400">Session Time</p>
                <p className="font-semibold">{charger.sessionTime}</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Battery size={18} className="text-primary-400" />
              <div>
                <p className="text-xs text-slate-400">Energy</p>
                <p className="font-semibold">{charger.energyDelivered} kWh</p>
              </div>
            </div>
          </>
        )}

        {charger.status === 'maintenance' && (
          <div className="col-span-2 flex items-center gap-2 bg-warning/10 p-2 rounded">
            <AlertTriangle size={18} className="text-warning" />
            <p className="text-sm text-warning">{charger.maintenanceNote}</p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-slate-700">
        <div className="flex items-center justify-between text-sm">
          <span className="text-slate-400">Utilization (24h)</span>
          <span className="font-semibold text-primary-400">{charger.utilization}%</span>
        </div>
        <div className="mt-2 h-2 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-primary-600 to-primary-400"
            style={{ width: `${charger.utilization}%` }}
          />
        </div>
      </div>
    </div>
  )
}

export default ChargerCard
