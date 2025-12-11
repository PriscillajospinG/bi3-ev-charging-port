import { AlertTriangle, Bell, CheckCircle, XCircle, Clock, Zap } from 'lucide-react'
import { formatDate } from '../../utils/helpers'

const AlertCard = ({ alert }) => {
  const getAlertIcon = (type) => {
    switch (type) {
      case 'critical':
        return <XCircle className="text-danger" size={24} />
      case 'warning':
        return <AlertTriangle className="text-warning" size={24} />
      case 'info':
        return <Bell className="text-primary-400" size={24} />
      case 'success':
        return <CheckCircle className="text-success" size={24} />
      default:
        return <Bell className="text-slate-400" size={24} />
    }
  }

  const getAlertBg = (type) => {
    switch (type) {
      case 'critical':
        return 'bg-danger/10 border-danger/30'
      case 'warning':
        return 'bg-warning/10 border-warning/30'
      case 'info':
        return 'bg-primary-500/10 border-primary-500/30'
      case 'success':
        return 'bg-success/10 border-success/30'
      default:
        return 'bg-slate-700/10 border-slate-700/30'
    }
  }

  return (
    <div className={`p-4 rounded-lg border ${getAlertBg(alert.type)} hover:shadow-lg transition-all`}>
      <div className="flex items-start gap-3">
        <div className="mt-0.5">{getAlertIcon(alert.type)}</div>
        <div className="flex-1">
          <div className="flex items-start justify-between mb-1">
            <h4 className="font-semibold">{alert.title}</h4>
            <span className="text-xs text-slate-500">{formatDate(alert.timestamp, 'short')}</span>
          </div>
          <p className="text-sm text-slate-400 mb-2">{alert.message}</p>
          {alert.location && (
            <p className="text-xs text-slate-500">📍 {alert.location}</p>
          )}
          {alert.action && (
            <button className="mt-3 text-xs font-semibold text-primary-400 hover:text-primary-300">
              {alert.action} →
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

const AlertsPanel = ({ alerts }) => {
  const criticalAlerts = alerts.filter(a => a.type === 'critical').length
  const warningAlerts = alerts.filter(a => a.type === 'warning').length

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Active Alerts</h3>
        <div className="flex items-center gap-3">
          {criticalAlerts > 0 && (
            <div className="flex items-center gap-1 text-danger">
              <XCircle size={16} />
              <span className="text-sm font-semibold">{criticalAlerts}</span>
            </div>
          )}
          {warningAlerts > 0 && (
            <div className="flex items-center gap-1 text-warning">
              <AlertTriangle size={16} />
              <span className="text-sm font-semibold">{warningAlerts}</span>
            </div>
          )}
        </div>
      </div>
      
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {alerts.length === 0 ? (
          <div className="text-center py-8 text-slate-500">
            <CheckCircle size={48} className="mx-auto mb-3 text-success" />
            <p>All systems operational</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))
        )}
      </div>
    </div>
  )
}

export default AlertsPanel
