import { useState } from 'react'
import RecommendationCard from '../components/Recommendations/RecommendationCard'
import { Filter, Lightbulb, TrendingUp } from 'lucide-react'

const Recommendations = () => {
  const [filter, setFilter] = useState('all')

  const recommendations = [
    {
      type: 'add',
      title: 'Add DC Fast Charger - Zone C',
      description: 'High demand detected in Zone C during peak hours with frequent queue buildup',
      location: 'Zone C, Bay 4-5',
      priority: 'high',
      impact: 28,
      cost: '$45,000',
      roi: '18 months',
      insights: [
        'Zone C experiences 35% higher wait times than other zones',
        'Projected 450 additional sessions per month',
        'Expected revenue increase of $2,800/month',
      ],
    },
    {
      type: 'relocate',
      title: 'Relocate Level 2 Charger',
      description: 'Charger B3 shows low utilization (32%) while Zone A is consistently at capacity',
      location: 'From Zone B to Zone A',
      priority: 'medium',
      impact: 18,
      cost: '$3,500',
      roi: '4 months',
      insights: [
        'Zone A utilization averages 89% vs Zone B at 42%',
        'Minimal relocation costs due to existing infrastructure',
        'Estimated 15% overall efficiency improvement',
      ],
    },
    {
      type: 'add',
      title: 'Deploy Mobile Charging Unit',
      description: 'Weekend demand spikes suggest need for flexible capacity',
      location: 'Rotating: Zones A, C, D',
      priority: 'medium',
      impact: 22,
      cost: '$28,000',
      roi: '12 months',
      insights: [
        'Weekend demand 45% higher than weekday average',
        'Mobile unit can serve multiple high-demand periods',
        'Reduces need for permanent infrastructure expansion',
      ],
    },
    {
      type: 'remove',
      title: 'Decommission Underutilized Charger',
      description: 'Charger D2 consistently shows <15% utilization over 3 months',
      location: 'Zone D, Bay 2',
      priority: 'low',
      impact: 5,
      cost: '$1,200',
      roi: '2 months',
      insights: [
        'Only 8 sessions per week average',
        'High maintenance costs relative to usage',
        'Can reallocate resources to higher-demand areas',
      ],
    },
    {
      type: 'add',
      title: 'Upgrade to 350kW Ultra-Fast Charger',
      description: 'Long session times causing queue buildup in Zone A',
      location: 'Zone A, Bay 1 (Replace existing 150kW)',
      priority: 'high',
      impact: 35,
      cost: '$65,000',
      roi: '16 months',
      insights: [
        'Average session time reduced from 45min to 15min',
        'Serves 3x more vehicles per day',
        'Premium pricing opportunity for ultra-fast charging',
      ],
    },
    {
      type: 'relocate',
      title: 'Optimize Charger Spacing',
      description: 'Camera analysis shows inefficient traffic flow in Zone B',
      location: 'Zone B - Reconfigure layout',
      priority: 'low',
      impact: 12,
      cost: '$8,500',
      roi: '8 months',
      insights: [
        'Current layout causes 12% increase in dwell time',
        'Optimization can improve throughput by 15%',
        'Reduces congestion and improves user experience',
      ],
    },
  ]

  const filteredRecommendations = recommendations.filter((rec) => {
    if (filter === 'all') return true
    if (filter === 'priority') return rec.priority === 'high'
    return rec.type === filter
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Recommendations</h1>
          <p className="text-slate-400 mt-1">AI-generated optimization strategies</p>
        </div>
        <div className="flex items-center gap-3">
          <Filter size={18} className="text-slate-400" />
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-primary-500"
          >
            <option value="all">All Recommendations</option>
            <option value="priority">High Priority Only</option>
            <option value="add">Add Chargers</option>
            <option value="remove">Remove Chargers</option>
            <option value="relocate">Relocate/Optimize</option>
          </select>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card bg-gradient-to-br from-danger to-red-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-100">High Priority</p>
              <p className="text-3xl font-bold mt-1">
                {recommendations.filter(r => r.priority === 'high').length}
              </p>
            </div>
            <Lightbulb size={32} className="text-red-200" />
          </div>
        </div>
        <div className="card bg-gradient-to-br from-warning to-orange-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-100">Medium Priority</p>
              <p className="text-3xl font-bold mt-1">
                {recommendations.filter(r => r.priority === 'medium').length}
              </p>
            </div>
            <Lightbulb size={32} className="text-orange-200" />
          </div>
        </div>
        <div className="card bg-gradient-to-br from-success to-emerald-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-emerald-100">Potential Impact</p>
              <p className="text-3xl font-bold mt-1">+24%</p>
            </div>
            <TrendingUp size={32} className="text-emerald-200" />
          </div>
        </div>
        <div className="card bg-gradient-to-br from-primary-600 to-primary-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-primary-100">Est. Revenue Lift</p>
              <p className="text-3xl font-bold mt-1">$8.2K</p>
            </div>
            <div className="text-primary-200 text-xs">per month</div>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">
          Actionable Recommendations ({filteredRecommendations.length})
        </h2>
        <div className="space-y-4">
          {filteredRecommendations.map((recommendation, index) => (
            <RecommendationCard key={index} recommendation={recommendation} />
          ))}
        </div>
      </div>

      {/* Info Card */}
      <div className="card bg-primary-500/10 border-primary-500/30">
        <div className="flex items-start gap-3">
          <Lightbulb className="text-primary-400 mt-1" size={24} />
          <div>
            <h3 className="font-semibold text-primary-300 mb-2">How Recommendations Work</h3>
            <p className="text-sm text-slate-400">
              Our AI analyzes traffic patterns, charger utilization, queue data, and demand forecasts
              to identify optimization opportunities. Recommendations are prioritized by potential impact,
              ROI, and implementation complexity. All suggestions are backed by data-driven insights
              from your DeepStream analytics pipeline.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Recommendations
