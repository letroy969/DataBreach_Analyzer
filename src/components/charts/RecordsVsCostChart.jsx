import React from 'react'
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const RecordsVsCostChart = ({ data }) => {
  const chartData = data.map(record => ({
    records: record.recordsExposed,
    cost: record.recordsExposed * 200, // $200 per record
    company: record.company,
    industry: record.industry,
    year: record.year,
  }))

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="chart-tooltip">
          <p className="font-semibold">{`Company: ${data.company}`}</p>
          <p className="text-primary">{`Records: ${data.records.toLocaleString()}`}</p>
          <p className="text-secondary">{`Cost: $${data.cost.toLocaleString()}`}</p>
          <p className="text-accent">{`Industry: ${data.industry}`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="currentColor"
            opacity={0.3}
          />
          <XAxis
            type="number"
            dataKey="records"
            name="Records Exposed"
            stroke="currentColor"
            fontSize={12}
            scale="log"
          />
          <YAxis
            type="number"
            dataKey="cost"
            name="Estimated Cost"
            stroke="currentColor"
            fontSize={12}
            scale="log"
          />
          <Tooltip content={<CustomTooltip />} />
          <Scatter dataKey="cost" fill="#1fb6b6" r={4} />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}

export default RecordsVsCostChart

