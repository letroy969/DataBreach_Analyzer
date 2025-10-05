import React from 'react'
import { motion } from 'framer-motion'
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Target,
  AlertTriangle,
  DollarSign,
  Users,
  Building,
} from 'lucide-react'
import {
  formatNumber,
  formatCurrency,
  formatPercentage,
} from '../utils/dataProcessor'

const AnalyticsInsights = ({ data }) => {
  const { stats } = data

  const insights = [
    {
      title: 'Top 5 Companies by Records Exposed',
      icon: Building,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20',
      content: (
        <div className="space-y-2">
          {stats.topCompanies.map((company, index) => (
            <div
              key={company.company}
              className="flex justify-between items-center p-2 bg-base-200 rounded"
            >
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-base-content/70">
                  #{index + 1}
                </span>
                <span className="font-medium">{company.company}</span>
                <span className="badge badge-sm badge-outline">
                  {company.industry}
                </span>
              </div>
              <div className="text-right">
                <div className="font-mono text-sm">
                  {formatNumber(company.recordsExposed)}
                </div>
                <div className="text-xs text-base-content/70">
                  {company.year}
                </div>
              </div>
            </div>
          ))}
        </div>
      ),
    },
    {
      title: 'Industry Risk Analysis',
      icon: Target,
      color: 'text-secondary',
      bgColor: 'bg-secondary/10',
      borderColor: 'border-secondary/20',
      content: (
        <div className="space-y-3">
          <div className="text-center">
            <div className="text-2xl font-bold text-secondary">
              {stats.industryStats.topIndustry}
            </div>
            <div className="text-sm text-base-content/70">
              Highest Risk Industry
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold">
                {stats.industryStats.totalIndustries}
              </div>
              <div className="text-xs text-base-content/70">
                Industries Affected
              </div>
            </div>
            <div>
              <div className="text-lg font-semibold">
                {formatPercentage(
                  stats.breachTypeStats.insiderThreatPercentage
                )}
              </div>
              <div className="text-xs text-base-content/70">
                Insider Threats
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: 'Trend Analysis',
      icon:
        stats.trendAnalysis.trend === 'increasing'
          ? TrendingUp
          : stats.trendAnalysis.trend === 'decreasing'
          ? TrendingDown
          : Minus,
      color:
        stats.trendAnalysis.trend === 'increasing'
          ? 'text-error'
          : stats.trendAnalysis.trend === 'decreasing'
          ? 'text-success'
          : 'text-info',
      bgColor:
        stats.trendAnalysis.trend === 'increasing'
          ? 'bg-error/10'
          : stats.trendAnalysis.trend === 'decreasing'
          ? 'bg-success/10'
          : 'bg-info/10',
      borderColor:
        stats.trendAnalysis.trend === 'increasing'
          ? 'border-error/20'
          : stats.trendAnalysis.trend === 'decreasing'
          ? 'border-success/20'
          : 'border-info/20',
      content: (
        <div className="space-y-3">
          <div className="text-center">
            <div
              className={`text-lg font-semibold ${
                stats.trendAnalysis.trend === 'increasing'
                  ? 'text-error'
                  : stats.trendAnalysis.trend === 'decreasing'
                  ? 'text-success'
                  : 'text-info'
              }`}
            >
              {stats.trendAnalysis.description}
            </div>
          </div>
          {stats.trendAnalysis.countChange !== undefined && (
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-lg font-semibold">
                  {formatPercentage(Math.abs(stats.trendAnalysis.countChange))}
                </div>
                <div className="text-xs text-base-content/70">Count Change</div>
              </div>
              <div>
                <div className="text-lg font-semibold">
                  {formatPercentage(
                    Math.abs(stats.trendAnalysis.recordsChange)
                  )}
                </div>
                <div className="text-xs text-base-content/70">
                  Records Change
                </div>
              </div>
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Correlation Analysis',
      icon: AlertTriangle,
      color: 'text-accent',
      bgColor: 'bg-accent/10',
      borderColor: 'border-accent/20',
      content: (
        <div className="space-y-3">
          <div className="text-center">
            <div className="text-2xl font-bold text-accent">
              {stats.correlation.correlation > 0 ? '+' : ''}
              {stats.correlation.correlation}
            </div>
            <div className="text-sm text-base-content/70">
              Correlation Coefficient
            </div>
          </div>
          <div className="text-sm text-center text-base-content/70">
            {stats.correlation.description}
          </div>
        </div>
      ),
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {insights.map((insight, index) => (
        <motion.div
          key={insight.title}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: index * 0.1 }}
          className={`insight-card ${insight.bgColor} ${insight.borderColor} border`}
        >
          <div className="flex items-center gap-3 mb-4">
            <div className={`p-2 rounded-lg ${insight.bgColor}`}>
              <insight.icon className={`w-5 h-5 ${insight.color}`} />
            </div>
            <h3 className="font-semibold text-base-content">{insight.title}</h3>
          </div>
          {insight.content}
        </motion.div>
      ))}
    </div>
  )
}

export default AnalyticsInsights

