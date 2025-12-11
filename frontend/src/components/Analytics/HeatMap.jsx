const HeatMap = ({ data, title }) => {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  const hours = Array.from({ length: 24 }, (_, i) => i)

  const getColor = (value) => {
    if (value >= 80) return 'bg-danger'
    if (value >= 60) return 'bg-warning'
    if (value >= 40) return 'bg-primary-500'
    if (value >= 20) return 'bg-primary-700'
    return 'bg-slate-700'
  }

  const getOpacity = (value) => {
    return Math.min(value / 100, 1)
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      
      <div className="overflow-x-auto">
        <div className="inline-block min-w-full">
          {/* Hours header */}
          <div className="flex mb-2">
            <div className="w-12" />
            {hours.map(hour => (
              <div key={hour} className="w-8 text-center text-xs text-slate-400">
                {hour % 3 === 0 ? hour : ''}
              </div>
            ))}
          </div>

          {/* Heatmap grid */}
          {days.map((day, dayIndex) => (
            <div key={day} className="flex items-center mb-1">
              <div className="w-12 text-xs text-slate-400 font-medium">{day}</div>
              {hours.map(hour => {
                const value = data?.[dayIndex]?.[hour] || Math.floor(Math.random() * 100)
                return (
                  <div
                    key={`${day}-${hour}`}
                    className={`w-8 h-8 m-0.5 rounded ${getColor(value)} transition-all hover:scale-110 cursor-pointer`}
                    style={{ opacity: getOpacity(value) }}
                    title={`${day} ${hour}:00 - ${value}% utilization`}
                  />
                )
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 mt-6 text-xs">
        <span className="text-slate-400">Low</span>
        <div className="flex gap-1">
          <div className="w-6 h-6 rounded bg-slate-700" />
          <div className="w-6 h-6 rounded bg-primary-700" />
          <div className="w-6 h-6 rounded bg-primary-500" />
          <div className="w-6 h-6 rounded bg-warning" />
          <div className="w-6 h-6 rounded bg-danger" />
        </div>
        <span className="text-slate-400">High</span>
      </div>
    </div>
  )
}

export default HeatMap
