import React from 'react'
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts'

const RegionalDistributionChart = ({ data }) => {
  const COLORS = [
    '#1fb6b6',
    '#ffb86b',
    '#0b2948',
    '#10b981',
    '#ef4444',
    '#3b82f6',
    '#8b5cf6',
    '#f59e0b',
    '#06b6d4',
    '#84cc16',
  ]

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0]
      return (
        <div className="chart-tooltip">
          <p className="font-semibold">{`Country: ${data.name}`}</p>
          <p className="text-primary">{`Breaches: ${data.value}`}</p>
          <p className="text-secondary">{`Percentage: ${data.percent.toFixed(
            1
          )}%`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) =>
              `${name} (${(percent * 100).toFixed(0)}%)`
            }
            outerRadius={80}
            fill="#8884d8"
            dataKey="count"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export default RegionalDistributionChart

