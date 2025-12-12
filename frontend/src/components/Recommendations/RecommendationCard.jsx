import { Plus, Minus, MapPin, AlertTriangle, CheckCircle } from 'lucide-react'

const RecommendationCard = ({ recommendation }) => {
  const getIcon = (type) => {
    switch (type) {
      case 'add':
        return <Plus className="text-success" size={24} />
      case 'remove':
        return <Minus className="text-danger" size={24} />
      case 'relocate':
        return <MapPin className="text-warning" size={24} />
      default:
        return <CheckCircle className="text-primary-400" size={24} />
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-danger/20 text-danger border-danger/30'
      case 'medium':
        return 'bg-warning/20 text-warning border-warning/30'
      case 'low':
        return 'bg-primary-500/20 text-primary-400 border-primary-500/30'
      default:
        return 'bg-slate-700/20 text-slate-400 border-slate-700/30'
    }
  }

  return (
    <div className="card hover:border-primary-500 transition-all">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-slate-700/50 rounded-lg">
          {getIcon(recommendation.type)}
        </div>

        <div className="flex-1">
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-lg font-semibold">{recommendation.title}</h3>
            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getPriorityColor(recommendation.priority)}`}>
              {recommendation.priority.toUpperCase()}
            </span>
          </div>

          <p className="text-sm text-slate-400 mb-4">{recommendation.description}</p>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-xs text-slate-500">Location</p>
              <p className="text-sm font-medium">{recommendation.location}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Expected Impact</p>
              <p className="text-sm font-medium text-success">+{recommendation.impact}%</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-xs text-slate-500">Estimated Cost</p>
              <p className="text-sm font-medium">{recommendation.cost}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">ROI Timeline</p>
              <p className="text-sm font-medium">{recommendation.roi}</p>
            </div>
          </div>

          {recommendation.insights && (
            <div className="bg-primary-500/10 border border-primary-500/30 rounded-lg p-3 mb-3">
              <p className="text-xs font-medium text-primary-300 mb-1">Key Insights:</p>
              <ul className="text-xs text-slate-400 space-y-1">
                {recommendation.insights.map((insight, index) => (
                  <li key={index}>• {insight}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex gap-2">
            <button className="btn-primary flex-1 text-sm">
              Implement
            </button>
            <button className="btn-secondary text-sm">
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RecommendationCard
