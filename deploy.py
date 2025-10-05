#!/usr/bin/env python3
"""
Deployment helper script for Data Breach Insights Dashboard
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git_status():
    """Check if we're in a git repository and if there are uncommitted changes."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not in a git repository. Please initialize git first:")
            print("   git init")
            print("   git add .")
            print("   git commit -m 'Initial commit'")
            return False
        
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes:")
            print(result.stdout)
            return False
        else:
            print("✅ Git repository is clean")
            return True
    except FileNotFoundError:
        print("❌ Git is not installed. Please install git first.")
        return False

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'app/app.py',
        'app/data_loader.py', 
        'app/visuals.py',
        'app/ai_insights.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files exist")
        return True

def check_streamlit_app():
    """Check if the Streamlit app can be imported without errors."""
    try:
        # Add app directory to path
        sys.path.insert(0, str(Path('app')))
        
        # Try to import the main modules
        import app
        import data_loader
        import visuals
        import ai_insights
        
        print("✅ Streamlit app imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking app: {e}")
        return False

def main():
    """Main deployment check function."""
    print("🚀 Data Breach Insights Dashboard - Deployment Check")
    print("=" * 50)
    
    checks = [
        ("Git Repository", check_git_status),
        ("Required Files", check_requirements),
        ("Streamlit App", check_streamlit_app)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Go to https://share.streamlit.io")
        print("3. Create new app from your repository")
        print("4. Set main file path to: app/app.py")
        print("5. Deploy!")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
