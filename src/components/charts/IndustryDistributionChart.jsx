import React from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const IndustryDistributionChart = ({ data }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="chart-tooltip">
          <p className="font-semibold">{`Industry: ${label}`}</p>
          <p className="text-primary">{`Breaches: ${payload[0].value}`}</p>
          <p className="text-secondary">{`Avg Records: ${
            payload[1]?.value?.toLocaleString() || 'N/A'
          }`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="currentColor"
            opacity={0.3}
          />
          <XAxis
            dataKey="industry"
            stroke="currentColor"
            fontSize={12}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis stroke="currentColor" fontSize={12} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" fill="#1fb6b6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default IndustryDistributionChart

