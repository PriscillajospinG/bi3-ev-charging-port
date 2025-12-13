import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts'

const DemandForecast = ({ data, historical, forecast }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-700 p-3 rounded-lg shadow-lg">
          <p className="text-sm font-semibold mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-xs" style={{ color: entry.color }}>
              {entry.name}: {entry.value} vehicles
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Demand Forecast</h3>
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-primary-500 rounded" />
            <span className="text-slate-400">Historical</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-warning rounded" />
            <span className="text-slate-400">Predicted</span>
          </div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="time" stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '12px' }} />
          
          {/* Current time reference line */}
          <ReferenceLine x="Now" stroke="#ef4444" strokeDasharray="3 3" label={{ value: 'Now', fill: '#ef4444', fontSize: 12 }} />
          
          <Line
            type="monotone"
            dataKey="historical"
            stroke="#0ea5e9"
            strokeWidth={2}
            dot={false}
            name="Historical Data"
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#f59e0b"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={false}
            name="Predicted Demand"
          />
          <Line
            type="monotone"
            dataKey="upperBound"
            stroke="#f59e0b"
            strokeWidth={1}
            strokeOpacity={0.3}
            dot={false}
            name="Upper Bound"
          />
          <Line
            type="monotone"
            dataKey="lowerBound"
            stroke="#f59e0b"
            strokeWidth={1}
            strokeOpacity={0.3}
            dot={false}
            name="Lower Bound"
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 grid grid-cols-3 gap-4 pt-4 border-t border-slate-700">
        <div className="text-center">
          <p className="text-xs text-slate-400">Peak Predicted</p>
          <p className="text-xl font-bold text-danger mt-1">{forecast?.peak || 'N/A'}</p>
          <p className="text-xs text-slate-500">{forecast?.peakTime || 'N/A'}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-400">Avg Demand</p>
          <p className="text-xl font-bold text-primary-400 mt-1">{forecast?.average || 'N/A'}</p>
          <p className="text-xs text-slate-500">vehicles/hour</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-slate-400">Model Accuracy</p>
          <p className="text-xl font-bold text-success mt-1">{forecast?.accuracy || 'N/A'}%</p>
          <p className="text-xs text-slate-500">LSTM Model</p>
        </div>
      </div>
    </div>
  )
}

export default DemandForecast
