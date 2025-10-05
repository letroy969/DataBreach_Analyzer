@echo off
echo 💻 Data Breach Insights Report - Streamlit Dashboard
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if app directory exists
if not exist "app" (
    echo ❌ App directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 🔧 Checking dependencies...
pip install -r app/requirements.txt >nul 2>&1

REM Run the Streamlit application
echo 🚀 Starting Data Breach Insights Report Dashboard...
echo 🌐 Open your browser to: http://localhost:8501
echo ⏹️  Press Ctrl+C to stop the server
echo ------------------------------------------------------------

streamlit run app/app.py --server.headless false --server.port 8501

echo.
echo 👋 Dashboard stopped. Thank you for using Data Breach Insights Report!
pause

