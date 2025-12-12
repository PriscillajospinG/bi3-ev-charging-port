import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'

const PredictionCard = ({ prediction }) => {
  const getTrendIcon = (trend) => {
    if (trend === 'up') return <TrendingUp className="text-danger" size={24} />
    if (trend === 'down') return <TrendingDown className="text-success" size={24} />
    return <AlertCircle className="text-warning" size={24} />
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return 'text-success'
    if (confidence >= 60) return 'text-warning'
    return 'text-danger'
  }

  return (
    <div className="card hover:border-primary-500 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{prediction.title}</h3>
          <p className="text-sm text-slate-400 mt-1">{prediction.timeframe}</p>
        </div>
        {getTrendIcon(prediction.trend)}
      </div>

      <div className="space-y-3">
        <div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-primary-400">
              {prediction.value}
            </span>
            <span className="text-sm text-slate-400">{prediction.unit}</span>
          </div>
          <p className="text-xs text-slate-500 mt-1">{prediction.description}</p>
        </div>

        <div className="pt-3 border-t border-slate-700">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Confidence</span>
            <span className={`text-sm font-semibold ${getConfidenceColor(prediction.confidence)}`}>
              {prediction.confidence}%
            </span>
          </div>
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${
                prediction.confidence >= 80 ? 'bg-success' :
                prediction.confidence >= 60 ? 'bg-warning' : 'bg-danger'
              }`}
              style={{ width: `${prediction.confidence}%` }}
            />
          </div>
        </div>

        {prediction.recommendation && (
          <div className="bg-primary-500/10 border border-primary-500/30 rounded-lg p-3">
            <p className="text-xs text-primary-300">{prediction.recommendation}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default PredictionCard
