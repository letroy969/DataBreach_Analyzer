#!/usr/bin/env python3
"""
Test script for Data Breach Insights Report project.

This script verifies that all components are working correctly
and provides a comprehensive test suite for the project.
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path
import subprocess
import json

def test_data_files():
    """Test that all data files exist and are valid."""
    print("🧪 Testing data files...")
    
    # Check sample CSV
    csv_file = "data/sample_breaches.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Missing: {csv_file}")
        return False
    
    df = pd.read_csv(csv_file)
    if len(df) < 400:  # Should have at least 400 records
        print(f"❌ Insufficient data: {len(df)} records")
        return False
    
    print(f"✅ Sample CSV: {len(df)} records")
    
    # Check Power BI data files
    powerbi_files = [
        "powerbi/breaches_for_powerbi.csv",
        "powerbi/industry_lookup.csv",
        "powerbi/country_lookup.csv",
        "powerbi/breach_severity.csv"
    ]
    
    for file in powerbi_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            return False
        print(f"✅ {file}")
    
    return True

def test_database_functionality():
    """Test database creation and queries."""
    print("\n🧪 Testing database functionality...")
    
    try:
        # Test data ingestion
        result = subprocess.run([
            sys.executable, "scripts/ingest_csv_to_postgres.py",
            "--csv", "data/sample_breaches.csv",
            "--db", "sqlite:///test.db"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Data ingestion failed: {result.stderr}")
            return False
        
        print("✅ Data ingestion successful")
        
        # Test database queries
        conn = sqlite3.connect("test.db")
        
        # Test basic query
        df = pd.read_sql_query("SELECT COUNT(*) as count FROM breaches", conn)
        if df.iloc[0]['count'] < 400:
            print(f"❌ Insufficient data in database: {df.iloc[0]['count']} records")
            return False
        
        print(f"✅ Database queries: {df.iloc[0]['count']} records")
        
        # Test analytical queries
        analytical_queries = [
            "SELECT COUNT(*) FROM breaches WHERE records_exposed > 1000000",
            "SELECT industry, COUNT(*) FROM breaches GROUP BY industry",
            "SELECT strftime('%Y', breach_date) as year, COUNT(*) FROM breaches GROUP BY year"
        ]
        
        for query in analytical_queries:
            try:
                pd.read_sql_query(query, conn)
            except Exception as e:
                print(f"❌ Query failed: {query} - {e}")
                return False
        
        print("✅ Analytical queries working")
        
        conn.close()
        os.remove("test.db")  # Clean up
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_excel_workbook():
    """Test Excel workbook creation."""
    print("\n🧪 Testing Excel workbook...")
    
    try:
        # Test workbook creation
        result = subprocess.run([
            sys.executable, "scripts/create_excel_workbook.py",
            "--csv", "data/sample_breaches.csv",
            "--output", "test_workbook.xlsx"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Excel workbook creation failed: {result.stderr}")
            return False
        
        if not os.path.exists("test_workbook.xlsx"):
            print("❌ Excel workbook file not created")
            return False
        
        # Test workbook content
        excel_file = pd.ExcelFile("test_workbook.xlsx")
        expected_sheets = ['RAW', 'CLEAN', 'industry_map', 'PIVOT_BreachesByYear', 
                          'PIVOT_IndustryRecords', 'PIVOT_Geography', 'PIVOT_BreachTypes',
                          'Summary_Stats', 'Top_Breaches', 'Executive_Summary']
        
        for sheet in expected_sheets:
            if sheet not in excel_file.sheet_names:
                print(f"❌ Missing sheet: {sheet}")
                return False
        
        print(f"✅ Excel workbook: {len(excel_file.sheet_names)} sheets")
        
        # Clean up
        os.remove("test_workbook.xlsx")
        return True
        
    except Exception as e:
        print(f"❌ Excel test failed: {e}")
        return False

def test_powerbi_data():
    """Test Power BI data preparation."""
    print("\n🧪 Testing Power BI data...")
    
    try:
        # Test Power BI data preparation
        result = subprocess.run([
            sys.executable, "scripts/prepare_powerbi_data.py",
            "--csv", "data/sample_breaches.csv",
            "--output", "test_powerbi"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Power BI data preparation failed: {result.stderr}")
            return False
        
        # Check output files
        powerbi_files = [
            "test_powerbi/breaches_for_powerbi.csv",
            "test_powerbi/industry_lookup.csv",
            "test_powerbi/country_lookup.csv",
            "test_powerbi/breach_severity.csv",
            "test_powerbi/CONNECTION_INSTRUCTIONS.md"
        ]
        
        for file in powerbi_files:
            if not os.path.exists(file):
                print(f"❌ Missing: {file}")
                return False
        
        print("✅ Power BI data preparation successful")
        
        # Clean up
        import shutil
        shutil.rmtree("test_powerbi")
        return True
        
    except Exception as e:
        print(f"❌ Power BI test failed: {e}")
        return False

def test_documentation():
    """Test that all documentation files exist."""
    print("\n🧪 Testing documentation...")
    
    required_files = [
        "README.md",
        "data/README.md",
        "excel/README.md",
        "powerbi/README.md",
        "docs/case_study.md",
        "docs/architecture.md",
        "docs/demo_script.md",
        "docs/executive_report.md",
        "recruiter_pitches.md",
        "LICENSE"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            return False
        
        # Check file size (should not be empty)
        if os.path.getsize(file) < 100:
            print(f"❌ File too small: {file}")
            return False
        
        print(f"✅ {file}")
    
    return True

def test_scripts():
    """Test that all scripts are executable."""
    print("\n🧪 Testing scripts...")
    
    scripts = [
        "scripts/produce_sample_csv.py",
        "scripts/ingest_csv_to_postgres.py",
        "scripts/create_excel_workbook.py",
        "scripts/prepare_powerbi_data.py",
        "scripts/test_queries.py"
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"❌ Missing: {script}")
            return False
        
        # Test script syntax
        try:
            with open(script, 'r') as f:
                compile(f.read(), script, 'exec')
        except SyntaxError as e:
            print(f"❌ Syntax error in {script}: {e}")
            return False
        
        print(f"✅ {script}")
    
    return True

def test_requirements():
    """Test that requirements.txt is valid."""
    print("\n🧪 Testing requirements...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ Missing: requirements.txt")
        return False
    
    try:
        with open("requirements.txt", 'r') as f:
            requirements = f.read()
        
        # Check for key packages
        key_packages = ['pandas', 'sqlalchemy', 'openpyxl', 'matplotlib', 'plotly']
        for package in key_packages:
            if package not in requirements:
                print(f"❌ Missing package: {package}")
                return False
        
        print("✅ requirements.txt valid")
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🚀 Starting comprehensive project test...")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("Database Functionality", test_database_functionality),
        ("Excel Workbook", test_excel_workbook),
        ("Power BI Data", test_powerbi_data),
        ("Documentation", test_documentation),
        ("Scripts", test_scripts),
        ("Requirements", test_requirements)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Project is ready for presentation.")
        return True
    else:
        print(f"\n⚠️  {total-passed} tests failed. Please fix issues before presentation.")
        return False

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick test - just check files exist
        print("🚀 Running quick test...")
        return test_data_files() and test_documentation()
    else:
        # Full test suite
        return run_comprehensive_test()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
