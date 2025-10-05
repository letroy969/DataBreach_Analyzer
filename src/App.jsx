import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Header from './components/Header'
import ThemeProvider from './contexts/ThemeContext'
import DataProvider from './contexts/DataContext'
import './App.css'

function App() {
  return (
    <ThemeProvider>
      <DataProvider>
        <Router>
          <div className="min-h-screen bg-base-100">
            <Header />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
              </Routes>
            </main>
          </div>
        </Router>
      </DataProvider>
    </ThemeProvider>
  )
}

export default App

