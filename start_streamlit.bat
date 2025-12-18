@echo off
echo 💻 Data Breach Insights Report - Streamlit Dashboard
echo ============================================================

REM Kill any existing Streamlit processes
taskkill /f /im python.exe >nul 2>&1

REM Start Streamlit with proper configuration
echo 🚀 Starting Streamlit Dashboard...
echo 🌐 Opening http://localhost:8501 in your browser...
echo ⏹️  Press Ctrl+C to stop the server
echo ------------------------------------------------------------

streamlit run app/app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false

echo.
echo 👋 Dashboard stopped. Thank you for using Data Breach Insights Report!
pause




