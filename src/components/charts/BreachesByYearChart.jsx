import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const BreachesByYearChart = ({ data }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="chart-tooltip">
          <p className="font-semibold">{`Year: ${label}`}</p>
          <p className="text-primary">{`Breaches: ${payload[0].value}`}</p>
          <p className="text-secondary">{`Records: ${
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
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="currentColor"
            opacity={0.3}
          />
          <XAxis dataKey="year" stroke="currentColor" fontSize={12} />
          <YAxis stroke="currentColor" fontSize={12} />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="count"
            stroke="#1fb6b6"
            strokeWidth={3}
            dot={{ fill: '#1fb6b6', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: '#1fb6b6', strokeWidth: 2 }}
          />
          <Line
            type="monotone"
            dataKey="totalRecords"
            stroke="#ffb86b"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#ffb86b', strokeWidth: 2, r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default BreachesByYearChart

