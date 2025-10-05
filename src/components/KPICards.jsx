import React from 'react'
import { motion } from 'framer-motion'
import { Shield, Database, TrendingUp, DollarSign } from 'lucide-react'
import {
  formatNumber,
  formatCurrency,
  formatPercentage,
  getYoYIndicator,
} from '../utils/dataProcessor'

const KPICards = ({ stats }) => {
  const kpiData = [
    {
      title: 'Total Breaches',
      value: formatNumber(stats.totalBreaches),
      icon: Shield,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20',
    },
    {
      title: 'Total Records Exposed',
      value: formatNumber(stats.totalRecordsExposed),
      icon: Database,
      color: 'text-secondary',
      bgColor: 'bg-secondary/10',
      borderColor: 'border-secondary/20',
    },
    {
      title: 'Average Breach Size',
      value: formatNumber(stats.avgBreachSize),
      icon: TrendingUp,
      color: 'text-accent',
      bgColor: 'bg-accent/10',
      borderColor: 'border-accent/20',
    },
    {
      title: 'Estimated Cost',
      value: formatCurrency(stats.estimatedCost),
      icon: DollarSign,
      color: 'text-success',
      bgColor: 'bg-success/10',
      borderColor: 'border-success/20',
    },
  ]

  const yoyIndicator = getYoYIndicator(stats.yoyChange)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {kpiData.map((kpi, index) => (
        <motion.div
          key={kpi.title}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: index * 0.1 }}
          className={`metric-card ${kpi.bgColor} ${kpi.borderColor} border`}
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`p-3 rounded-lg ${kpi.bgColor}`}>
              <kpi.icon className={`w-6 h-6 ${kpi.color}`} />
            </div>
            {kpi.title === 'Total Breaches' && (
              <div className="text-right">
                <div className={`text-sm font-medium ${yoyIndicator.color}`}>
                  {yoyIndicator.emoji}{' '}
                  {formatPercentage(Math.abs(stats.yoyChange))}
                </div>
                <div className="text-xs text-base-content/70">YoY Change</div>
              </div>
            )}
          </div>

          <div className="space-y-2">
            <div className={`text-3xl font-bold ${kpi.color}`}>{kpi.value}</div>
            <div className="text-sm text-base-content/70 font-medium">
              {kpi.title}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  )
}

export default KPICards

