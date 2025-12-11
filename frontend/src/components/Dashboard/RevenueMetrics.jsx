import { DollarSign, TrendingUp, Receipt, CreditCard } from 'lucide-react'
import { formatCurrency } from '../../utils/helpers'

const RevenueMetrics = ({ metrics }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="card bg-gradient-to-br from-success to-emerald-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-emerald-100">Today's Revenue</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(metrics.todayRevenue)}</p>
            <p className="text-xs text-emerald-200 mt-1">
              {metrics.todayChange > 0 ? '↑' : '↓'} {Math.abs(metrics.todayChange)}% vs yesterday
            </p>
          </div>
          <DollarSign size={40} className="text-emerald-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-primary-600 to-primary-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-primary-100">This Week</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(metrics.weekRevenue)}</p>
            <p className="text-xs text-primary-200 mt-1">
              Avg: {formatCurrency(metrics.avgDailyRevenue)}/day
            </p>
          </div>
          <Receipt size={40} className="text-primary-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-purple-600 to-purple-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-purple-100">This Month</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(metrics.monthRevenue)}</p>
            <p className="text-xs text-purple-200 mt-1">
              Target: {metrics.monthProgress}% achieved
            </p>
          </div>
          <CreditCard size={40} className="text-purple-200" />
        </div>
      </div>

      <div className="card bg-gradient-to-br from-warning to-orange-700">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-orange-100">Projected (30d)</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(metrics.projectedRevenue)}</p>
            <p className="text-xs text-orange-200 mt-1">
              Based on current trends
            </p>
          </div>
          <TrendingUp size={40} className="text-orange-200" />
        </div>
      </div>
    </div>
  )
}

export default RevenueMetrics
