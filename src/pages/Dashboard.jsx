import React from 'react'
import { motion } from 'framer-motion'
import KPICards from '../components/KPICards'
import ChartsSection from '../components/ChartsSection'
import DataTable from '../components/DataTable'
import AnalyticsInsights from '../components/AnalyticsInsights'
import { useData } from '../contexts/DataContext'

const Dashboard = () => {
  const { processedData, loading, error } = useData()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="loading loading-spinner loading-lg text-primary"></div>
        <span className="ml-4 text-lg">Loading breach data...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="alert alert-warning">
        <span>{error}</span>
      </div>
    )
  }

  if (!processedData) {
    return (
      <div className="alert alert-error">
        <span>No data available</span>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      {/* KPI Cards Section */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        <h2 className="text-2xl font-bold mb-6 text-gradient">
          Key Performance Indicators
        </h2>
        <KPICards stats={processedData.stats} />
      </motion.section>

      {/* Charts Section */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <h2 className="text-2xl font-bold mb-6 text-gradient">
          Interactive Analytics
        </h2>
        <ChartsSection data={processedData} />
      </motion.section>

      {/* Analytics Insights */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <h2 className="text-2xl font-bold mb-6 text-gradient">
          Analytics Insights
        </h2>
        <AnalyticsInsights data={processedData} />
      </motion.section>

      {/* Data Table */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <h2 className="text-2xl font-bold mb-6 text-gradient">
          Breach Records
        </h2>
        <DataTable records={processedData.records} />
      </motion.section>
    </motion.div>
  )
}

export default Dashboard

