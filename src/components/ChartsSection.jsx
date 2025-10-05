import React from 'react'
import { motion } from 'framer-motion'
import BreachesByYearChart from './charts/BreachesByYearChart'
import IndustryDistributionChart from './charts/IndustryDistributionChart'
import RegionalDistributionChart from './charts/RegionalDistributionChart'
import RecordsVsCostChart from './charts/RecordsVsCostChart'

const ChartsSection = ({ data }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Breaches by Year */}
      <motion.div
        initial={{ opacity: 0, x: -30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="chart-container"
      >
        <h3 className="text-lg font-semibold mb-4 text-base-content">
          Breaches by Year
        </h3>
        <BreachesByYearChart data={data.stats.trendAnalysis.yearlyData} />
      </motion.div>

      {/* Industry Distribution */}
      <motion.div
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="chart-container"
      >
        <h3 className="text-lg font-semibold mb-4 text-base-content">
          Top Industries by Frequency
        </h3>
        <IndustryDistributionChart
          data={data.stats.industryStats.byCount.slice(0, 10)}
        />
      </motion.div>

      {/* Regional Distribution */}
      <motion.div
        initial={{ opacity: 0, x: -30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="chart-container"
      >
        <h3 className="text-lg font-semibold mb-4 text-base-content">
          Breaches by Region
        </h3>
        <RegionalDistributionChart
          data={data.stats.regionalStats.byCount.slice(0, 8)}
        />
      </motion.div>

      {/* Records vs Cost Scatter */}
      <motion.div
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="chart-container"
      >
        <h3 className="text-lg font-semibold mb-4 text-base-content">
          Records vs Estimated Cost
        </h3>
        <RecordsVsCostChart data={data.records.slice(0, 100)} />
      </motion.div>
    </div>
  )
}

export default ChartsSection

