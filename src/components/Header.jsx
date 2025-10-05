import React from 'react'
import { Shield, Sun, Moon, RefreshCw } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'
import { useData } from '../contexts/DataContext'

const Header = () => {
  const { theme, toggleTheme, isDark } = useTheme()
  const { loading, refreshData, processedData } = useData()

  return (
    <header className="navbar bg-base-200 shadow-lg border-b border-base-300">
      <div className="navbar-start">
        <div className="flex items-center gap-2">
          <Shield className="w-8 h-8 text-primary" />
          <div>
            <h1 className="text-xl font-bold text-gradient">
              Data Breach Insights Report
            </h1>
            <p className="text-sm text-base-content/70">
              A Data Analyst Case Study — 2004–2023
            </p>
          </div>
        </div>
      </div>

      <div className="navbar-center">
        {processedData && (
          <div className="text-sm text-base-content/70">
            Last updated: {new Date(processedData.lastUpdated).toLocaleString()}
          </div>
        )}
      </div>

      <div className="navbar-end">
        <div className="flex items-center gap-2">
          <button
            onClick={refreshData}
            disabled={loading}
            className="btn btn-ghost btn-sm"
            title="Refresh Data"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>

          <button
            onClick={toggleTheme}
            className="btn btn-ghost btn-sm"
            title={`Switch to ${isDark ? 'light' : 'dark'} theme`}
          >
            {isDark ? (
              <Sun className="w-4 h-4" />
            ) : (
              <Moon className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header

