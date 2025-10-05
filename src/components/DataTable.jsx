import React, { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { Search, Download, Filter, ChevronUp, ChevronDown } from 'lucide-react'
import { formatNumber, formatCurrency } from '../utils/dataProcessor'

const DataTable = ({ records }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [industryFilter, setIndustryFilter] = useState('')
  const [yearFilter, setYearFilter] = useState('')
  const [sortField, setSortField] = useState('recordsExposed')
  const [sortDirection, setSortDirection] = useState('desc')

  // Get unique values for filters
  const industries = useMemo(() => {
    const unique = [...new Set(records.map(r => r.industry))].sort()
    return unique
  }, [records])

  const years = useMemo(() => {
    const unique = [...new Set(records.map(r => r.year))].sort((a, b) => b - a)
    return unique
  }, [records])

  // Filter and sort data
  const filteredRecords = useMemo(() => {
    let filtered = records.filter(record => {
      const matchesSearch =
        record.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.industry.toLowerCase().includes(searchTerm.toLowerCase()) ||
        record.country.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesIndustry =
        !industryFilter || record.industry === industryFilter
      const matchesYear = !yearFilter || record.year === parseInt(yearFilter)

      return matchesSearch && matchesIndustry && matchesYear
    })

    // Sort data
    filtered.sort((a, b) => {
      let aValue = a[sortField]
      let bValue = b[sortField]

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase()
        bValue = bValue.toLowerCase()
      }

      if (sortDirection === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return filtered
  }, [
    records,
    searchTerm,
    industryFilter,
    yearFilter,
    sortField,
    sortDirection,
  ])

  const handleSort = field => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const handleExportCSV = () => {
    const headers = [
      'Company',
      'Year',
      'Industry',
      'Country',
      'Records Exposed',
      'Breach Type',
      'Estimated Cost',
    ]
    const csvContent = [
      headers.join(','),
      ...filteredRecords.map(record =>
        [
          `"${record.company}"`,
          record.year,
          `"${record.industry}"`,
          record.country,
          record.recordsExposed,
          `"${record.breachType}"`,
          record.recordsExposed * 200,
        ].join(',')
      ),
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `breach_data_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
    window.URL.revokeObjectURL(url)
  }

  const SortIcon = ({ field }) => {
    if (sortField !== field) return null
    return sortDirection === 'asc' ? (
      <ChevronUp className="w-4 h-4" />
    ) : (
      <ChevronDown className="w-4 h-4" />
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-6"
    >
      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex-1 min-w-64">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-base-content/50" />
            <input
              type="text"
              placeholder="Search companies, industries, or countries..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="search-input pl-10 w-full"
            />
          </div>
        </div>

        <select
          value={industryFilter}
          onChange={e => setIndustryFilter(e.target.value)}
          className="filter-select"
        >
          <option value="">All Industries</option>
          {industries.map(industry => (
            <option key={industry} value={industry}>
              {industry}
            </option>
          ))}
        </select>

        <select
          value={yearFilter}
          onChange={e => setYearFilter(e.target.value)}
          className="filter-select"
        >
          <option value="">All Years</option>
          {years.map(year => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>

        <button onClick={handleExportCSV} className="btn btn-primary btn-sm">
          <Download className="w-4 h-4 mr-2" />
          Export CSV
        </button>
      </div>

      {/* Results count */}
      <div className="text-sm text-base-content/70">
        Showing {filteredRecords.length} of {records.length} records
      </div>

      {/* Table */}
      <div className="data-table overflow-x-auto">
        <table className="table w-full">
          <thead>
            <tr>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('company')}
              >
                <div className="flex items-center gap-2">
                  Company
                  <SortIcon field="company" />
                </div>
              </th>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('year')}
              >
                <div className="flex items-center gap-2">
                  Year
                  <SortIcon field="year" />
                </div>
              </th>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('industry')}
              >
                <div className="flex items-center gap-2">
                  Industry
                  <SortIcon field="industry" />
                </div>
              </th>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('country')}
              >
                <div className="flex items-center gap-2">
                  Country
                  <SortIcon field="country" />
                </div>
              </th>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('recordsExposed')}
              >
                <div className="flex items-center gap-2">
                  Records Exposed
                  <SortIcon field="recordsExposed" />
                </div>
              </th>
              <th
                className="cursor-pointer hover:bg-base-300/50"
                onClick={() => handleSort('breachType')}
              >
                <div className="flex items-center gap-2">
                  Breach Type
                  <SortIcon field="breachType" />
                </div>
              </th>
              <th>Estimated Cost</th>
            </tr>
          </thead>
          <tbody>
            {filteredRecords.slice(0, 100).map((record, index) => (
              <motion.tr
                key={record.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.01 }}
                className="hover:bg-base-300/30"
              >
                <td className="font-medium">{record.company}</td>
                <td>{record.year}</td>
                <td>
                  <span className="badge badge-outline badge-sm">
                    {record.industry}
                  </span>
                </td>
                <td>{record.country}</td>
                <td className="font-mono text-sm">
                  {formatNumber(record.recordsExposed)}
                </td>
                <td>
                  <span
                    className={`badge badge-sm ${
                      record.breachType === 'Hacking'
                        ? 'badge-error'
                        : record.breachType === 'Insider'
                        ? 'badge-warning'
                        : record.breachType === 'System Error'
                        ? 'badge-info'
                        : 'badge-neutral'
                    }`}
                  >
                    {record.breachType}
                  </span>
                </td>
                <td className="font-mono text-sm text-success">
                  {formatCurrency(record.recordsExposed * 200)}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredRecords.length > 100 && (
        <div className="text-center text-sm text-base-content/70">
          Showing first 100 results. Use filters to narrow down your search.
        </div>
      )}
    </motion.div>
  )
}

export default DataTable

