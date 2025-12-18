#!/usr/bin/env python3
"""
Data Breach Insights Report - Streamlit Runner

Simple script to run the Streamlit application with proper configuration.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r app/requirements.txt")
        return False

def run_streamlit():
    """Run the Streamlit application."""
    app_path = Path(__file__).parent / "app" / "app.py"
    
    if not app_path.exists():
        print(f"❌ App file not found: {app_path}")
        return False
    
    print("🚀 Starting Data Breach Insights Report Dashboard...")
    print("📍 App location:", app_path)
    print("🌐 Open your browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run streamlit with proper configuration
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.headless", "false",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thank you for using Data Breach Insights Report!")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print("💻 Data Breach Insights Report - Streamlit Dashboard")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the project root directory")
        print("   The 'app' folder should be in the current directory")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Run the application
    return run_streamlit()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




