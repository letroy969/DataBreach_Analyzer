import React, { createContext, useContext, useState, useEffect } from 'react'
import { processBreachData } from '../utils/dataProcessor'

const DataContext = createContext()

export const useData = () => {
  const context = useContext(DataContext)
  if (!context) {
    throw new Error('useData must be used within a DataProvider')
  }
  return context
}

const DataProvider = ({ children }) => {
  const [rawData, setRawData] = useState([])
  const [processedData, setProcessedData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Load data on component mount
  useEffect(() => {
    loadData()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Try to load from local CSV file first
      const response = await fetch('/data/sample_breaches.csv')
      if (response.ok) {
        const csvText = await response.text()
        const data = parseCSV(csvText)
        setRawData(data)
        setProcessedData(processBreachData(data))
      } else {
        // Fallback to sample data
        const sampleData = generateSampleData()
        setRawData(sampleData)
        setProcessedData(processBreachData(sampleData))
      }
    } catch (err) {
      console.error('Error loading data:', err)
      setError('Failed to load data. Using sample data.')

      // Use sample data as fallback
      const sampleData = generateSampleData()
      setRawData(sampleData)
      setProcessedData(processBreachData(sampleData))
    } finally {
      setLoading(false)
    }
  }

  const parseCSV = csvText => {
    const lines = csvText.split('\n')
    const headers = lines[0].split(',').map(h => h.trim())
    const data = []

    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        const values = lines[i].split(',').map(v => v.trim())
        const record = {}
        headers.forEach((header, index) => {
          record[header] = values[index] || ''
        })
        data.push(record)
      }
    }

    return data
  }

  const generateSampleData = () => {
    // Generate sample data if CSV is not available
    const industries = [
      'Healthcare',
      'Financial',
      'Technology',
      'Retail',
      'Government',
      'Education',
      'Energy',
      'Manufacturing',
      'Transportation',
      'Media',
    ]
    const countries = [
      'US',
      'GB',
      'CA',
      'AU',
      'DE',
      'FR',
      'JP',
      'IN',
      'BR',
      'CN',
      'IT',
      'ES',
      'NL',
      'SE',
      'NO',
      'DK',
      'FI',
      'CH',
      'AT',
      'BE',
    ]
    const breachTypes = [
      'Hacking',
      'Insider',
      'Physical',
      'Social Engineering',
      'System Error',
      'Unknown',
    ]

    const data = []
    const startDate = new Date('2020-01-01')
    const endDate = new Date('2024-12-31')

    for (let i = 1; i <= 500; i++) {
      const industry = industries[Math.floor(Math.random() * industries.length)]
      const country = countries[Math.floor(Math.random() * countries.length)]
      const breachType =
        breachTypes[Math.floor(Math.random() * breachTypes.length)]

      // Generate random date
      const randomTime =
        startDate.getTime() +
        Math.random() * (endDate.getTime() - startDate.getTime())
      const breachDate = new Date(randomTime)

      // Generate realistic company name
      const companyPrefixes = [
        'Health',
        'Medical',
        'Care',
        'Hospital',
        'Bank',
        'Credit',
        'Finance',
        'Tech',
        'Cloud',
        'Data',
        'Retail',
        'Store',
        'Market',
        'Gov',
        'Federal',
        'Agency',
      ]
      const companySuffixes = [
        'Corp',
        'Inc',
        'LLC',
        'Ltd',
        'Group',
        'Systems',
        'Solutions',
        'Services',
      ]
      const companyName = `${
        companyPrefixes[Math.floor(Math.random() * companyPrefixes.length)]
      } ${companySuffixes[Math.floor(Math.random() * companySuffixes.length)]}`

      // Generate realistic records exposed (log-normal distribution)
      const recordsExposed = Math.floor(Math.random() * 1000000) + 1000

      data.push({
        id: i,
        breach_date: breachDate.toISOString().split('T')[0],
        name: companyName,
        industry: industry,
        country: country,
        records_exposed: recordsExposed,
        breach_type: breachType,
        source_url: `https://example.com/breach-${i
          .toString()
          .padStart(4, '0')}`,
      })
    }

    return data
  }

  const refreshData = () => {
    loadData()
  }

  const value = {
    rawData,
    processedData,
    loading,
    error,
    refreshData,
  }

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>
}

export default DataProvider
