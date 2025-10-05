/**
 * Data processing utilities for breach insights analysis
 * Handles data cleaning, transformation, and calculation of KPIs
 */

/**
 * Clean and process raw breach data
 * @param {Array} rawData - Array of breach records
 * @returns {Object} Processed data with statistics and cleaned records
 */
export function processBreachData(rawData) {
  if (!rawData || rawData.length === 0) {
    return {
      records: [],
      stats: getEmptyStats(),
      lastUpdated: new Date().toISOString(),
    }
  }

  // Clean and validate data
  const cleanedRecords = rawData
    .map((record, index) => ({
      id: record.id || index + 1,
      breachDate: record.breach_date || record.breachDate,
      company: record.name || record.company || 'Unknown Company',
      industry: record.industry || 'Unknown',
      country: record.country || 'Unknown',
      recordsExposed: parseInt(
        record.records_exposed || record.recordsExposed || 0
      ),
      breachType: record.breach_type || record.breachType || 'Unknown',
      sourceUrl: record.source_url || record.sourceUrl || '',
      year:
        new Date(record.breach_date || record.breachDate).getFullYear() ||
        new Date().getFullYear(),
    }))
    .filter(
      record =>
        record.recordsExposed > 0 &&
        record.company !== 'Unknown Company' &&
        record.industry !== 'Unknown'
    )

  // Calculate statistics
  const stats = calculateStatistics(cleanedRecords)

  return {
    records: cleanedRecords,
    stats,
    lastUpdated: new Date().toISOString(),
  }
}

/**
 * Calculate comprehensive statistics from breach records
 * @param {Array} records - Cleaned breach records
 * @returns {Object} Statistics object
 */
function calculateStatistics(records) {
  if (records.length === 0) return getEmptyStats()

  const totalBreaches = records.length
  const totalRecordsExposed = records.reduce(
    (sum, record) => sum + record.recordsExposed,
    0
  )
  const avgBreachSize = Math.round(totalRecordsExposed / totalBreaches)

  // Year-over-year calculation
  const currentYear = new Date().getFullYear()
  const previousYear = currentYear - 1

  const currentYearBreaches = records.filter(r => r.year === currentYear).length
  const previousYearBreaches = records.filter(
    r => r.year === previousYear
  ).length

  const yoyChange =
    previousYearBreaches > 0
      ? ((currentYearBreaches - previousYearBreaches) / previousYearBreaches) *
        100
      : 0

  // Industry analysis
  const industryStats = getIndustryStats(records)

  // Regional analysis
  const regionalStats = getRegionalStats(records)

  // Breach type analysis
  const breachTypeStats = getBreachTypeStats(records)

  // Cost estimation ($200 per record)
  const estimatedCost = totalRecordsExposed * 200

  // Top companies by records exposed
  const topCompanies = getTopCompanies(records, 5)

  // Trend analysis
  const trendAnalysis = getTrendAnalysis(records)

  // Correlation analysis
  const correlation = getCorrelationAnalysis(records)

  return {
    totalBreaches,
    totalRecordsExposed,
    avgBreachSize,
    yoyChange,
    estimatedCost,
    industryStats,
    regionalStats,
    breachTypeStats,
    topCompanies,
    trendAnalysis,
    correlation,
    dateRange: {
      start: Math.min(...records.map(r => r.year)),
      end: Math.max(...records.map(r => r.year)),
    },
  }
}

/**
 * Get industry statistics
 * @param {Array} records - Breach records
 * @returns {Object} Industry statistics
 */
function getIndustryStats(records) {
  const industryMap = {}

  records.forEach(record => {
    const industry = record.industry
    if (!industryMap[industry]) {
      industryMap[industry] = {
        count: 0,
        totalRecords: 0,
        avgRecords: 0,
      }
    }
    industryMap[industry].count++
    industryMap[industry].totalRecords += record.recordsExposed
  })

  // Calculate averages
  Object.keys(industryMap).forEach(industry => {
    industryMap[industry].avgRecords = Math.round(
      industryMap[industry].totalRecords / industryMap[industry].count
    )
  })

  // Sort by count
  const sortedIndustries = Object.entries(industryMap)
    .map(([industry, stats]) => ({ industry, ...stats }))
    .sort((a, b) => b.count - a.count)

  return {
    byCount: sortedIndustries,
    topIndustry: sortedIndustries[0]?.industry || 'Unknown',
    totalIndustries: sortedIndustries.length,
  }
}

/**
 * Get regional statistics
 * @param {Array} records - Breach records
 * @returns {Object} Regional statistics
 */
function getRegionalStats(records) {
  const regionMap = {}

  records.forEach(record => {
    const country = record.country
    if (!regionMap[country]) {
      regionMap[country] = {
        count: 0,
        totalRecords: 0,
      }
    }
    regionMap[country].count++
    regionMap[country].totalRecords += record.recordsExposed
  })

  const sortedRegions = Object.entries(regionMap)
    .map(([country, stats]) => ({ country, ...stats }))
    .sort((a, b) => b.count - a.count)

  return {
    byCount: sortedRegions,
    topCountry: sortedRegions[0]?.country || 'Unknown',
    totalCountries: sortedRegions.length,
  }
}

/**
 * Get breach type statistics
 * @param {Array} records - Breach records
 * @returns {Object} Breach type statistics
 */
function getBreachTypeStats(records) {
  const typeMap = {}

  records.forEach(record => {
    const type = record.breachType
    if (!typeMap[type]) {
      typeMap[type] = { count: 0, percentage: 0 }
    }
    typeMap[type].count++
  })

  const total = records.length
  Object.keys(typeMap).forEach(type => {
    typeMap[type].percentage = Math.round((typeMap[type].count / total) * 100)
  })

  const sortedTypes = Object.entries(typeMap)
    .map(([type, stats]) => ({ type, ...stats }))
    .sort((a, b) => b.count - a.count)

  return {
    byCount: sortedTypes,
    topType: sortedTypes[0]?.type || 'Unknown',
    insiderThreatPercentage: typeMap['Insider']?.percentage || 0,
  }
}

/**
 * Get top companies by records exposed
 * @param {Array} records - Breach records
 * @param {number} limit - Number of top companies to return
 * @returns {Array} Top companies
 */
function getTopCompanies(records, limit = 5) {
  return records
    .sort((a, b) => b.recordsExposed - a.recordsExposed)
    .slice(0, limit)
    .map(record => ({
      company: record.company,
      recordsExposed: record.recordsExposed,
      industry: record.industry,
      year: record.year,
    }))
}

/**
 * Get trend analysis
 * @param {Array} records - Breach records
 * @returns {Object} Trend analysis
 */
function getTrendAnalysis(records) {
  const yearlyData = {}

  records.forEach(record => {
    const year = record.year
    if (!yearlyData[year]) {
      yearlyData[year] = { count: 0, totalRecords: 0 }
    }
    yearlyData[year].count++
    yearlyData[year].totalRecords += record.recordsExposed
  })

  const sortedYears = Object.entries(yearlyData)
    .map(([year, data]) => ({ year: parseInt(year), ...data }))
    .sort((a, b) => a.year - b.year)

  if (sortedYears.length < 2) {
    return {
      trend: 'insufficient_data',
      description: 'Insufficient data for trend analysis',
      yearlyData: sortedYears,
    }
  }

  const recent = sortedYears[sortedYears.length - 1]
  const previous = sortedYears[sortedYears.length - 2]

  const countChange = ((recent.count - previous.count) / previous.count) * 100
  const recordsChange =
    ((recent.totalRecords - previous.totalRecords) / previous.totalRecords) *
    100

  let trend = 'stable'
  let description = 'Breach activity has remained relatively stable'

  if (countChange > 20) {
    trend = 'increasing'
    description = `Breach frequency increased by ${Math.round(
      countChange
    )}% from ${previous.year} to ${recent.year}`
  } else if (countChange < -20) {
    trend = 'decreasing'
    description = `Breach frequency decreased by ${Math.round(
      Math.abs(countChange)
    )}% from ${previous.year} to ${recent.year}`
  }

  return {
    trend,
    description,
    yearlyData: sortedYears,
    countChange: Math.round(countChange),
    recordsChange: Math.round(recordsChange),
  }
}

/**
 * Get correlation analysis between records exposed and other factors
 * @param {Array} records - Breach records
 * @returns {Object} Correlation analysis
 */
function getCorrelationAnalysis(records) {
  if (records.length < 10) {
    return {
      correlation: 0,
      description: 'Insufficient data for correlation analysis',
    }
  }

  // Simple correlation between records exposed and year
  const years = records.map(r => r.year)
  const recordsExposed = records.map(r => r.recordsExposed)

  const correlation = calculateCorrelation(years, recordsExposed)

  let description = 'No significant correlation found'
  if (Math.abs(correlation) > 0.3) {
    const direction = correlation > 0 ? 'positive' : 'negative'
    const strength = Math.abs(correlation) > 0.7 ? 'strong' : 'moderate'
    description = `${strength} ${direction} correlation between year and records exposed`
  }

  return {
    correlation: Math.round(correlation * 100) / 100,
    description,
  }
}

/**
 * Calculate Pearson correlation coefficient
 * @param {Array} x - First variable
 * @param {Array} y - Second variable
 * @returns {number} Correlation coefficient
 */
function calculateCorrelation(x, y) {
  const n = x.length
  const sumX = x.reduce((a, b) => a + b, 0)
  const sumY = y.reduce((a, b) => a + b, 0)
  const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0)
  const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0)
  const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0)

  const numerator = n * sumXY - sumX * sumY
  const denominator = Math.sqrt(
    (n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY)
  )

  return denominator === 0 ? 0 : numerator / denominator
}

/**
 * Get empty statistics object
 * @returns {Object} Empty statistics
 */
function getEmptyStats() {
  return {
    totalBreaches: 0,
    totalRecordsExposed: 0,
    avgBreachSize: 0,
    yoyChange: 0,
    estimatedCost: 0,
    industryStats: { byCount: [], topIndustry: 'Unknown', totalIndustries: 0 },
    regionalStats: { byCount: [], topCountry: 'Unknown', totalCountries: 0 },
    breachTypeStats: {
      byCount: [],
      topType: 'Unknown',
      insiderThreatPercentage: 0,
    },
    topCompanies: [],
    trendAnalysis: {
      trend: 'unknown',
      description: 'No data available',
      yearlyData: [],
    },
    correlation: { correlation: 0, description: 'No data available' },
    dateRange: {
      start: new Date().getFullYear(),
      end: new Date().getFullYear(),
    },
  }
}

/**
 * Format number with commas
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
export function formatNumber(num) {
  return new Intl.NumberFormat().format(num)
}

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency
 */
export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

/**
 * Format percentage
 * @param {number} value - Value to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage
 */
export function formatPercentage(value, decimals = 1) {
  return `${value.toFixed(decimals)}%`
}

/**
 * Get year-over-year change indicator
 * @param {number} change - YoY change percentage
 * @returns {Object} Indicator object with emoji and color
 */
export function getYoYIndicator(change) {
  if (change > 0) {
    return { emoji: '🔼', color: 'text-error', label: 'Increase' }
  } else if (change < 0) {
    return { emoji: '🔽', color: 'text-success', label: 'Decrease' }
  } else {
    return { emoji: '➡️', color: 'text-info', label: 'No Change' }
  }
}

