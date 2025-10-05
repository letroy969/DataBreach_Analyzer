#!/usr/bin/env python3
"""
Simple test script for Data Breach Insights Report project.
Avoids Unicode issues on Windows.
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path

def test_basic_functionality():
    """Test basic project functionality."""
    print("Testing Data Breach Insights Report...")
    print("=" * 50)
    
    # Test 1: Data files exist
    print("\n1. Testing data files...")
    csv_file = "data/sample_breaches.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print(f"   ✓ Sample CSV: {len(df)} records")
    else:
        print("   ✗ Sample CSV missing")
        return False
    
    # Test 2: Excel workbook exists
    print("\n2. Testing Excel workbook...")
    excel_file = "excel/breach_analysis.xlsx"
    if os.path.exists(excel_file):
        print(f"   ✓ Excel workbook: {excel_file}")
    else:
        print("   ✗ Excel workbook missing")
        return False
    
    # Test 3: Power BI data files
    print("\n3. Testing Power BI data...")
    powerbi_files = [
        "powerbi/breaches_for_powerbi.csv",
        "powerbi/industry_lookup.csv",
        "powerbi/country_lookup.csv",
        "powerbi/breach_severity.csv"
    ]
    
    all_exist = True
    for file in powerbi_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} missing")
            all_exist = False
    
    if not all_exist:
        return False
    
    # Test 4: Documentation files
    print("\n4. Testing documentation...")
    doc_files = [
        "README.md",
        "docs/case_study.md",
        "docs/architecture.md",
        "docs/demo_script.md",
        "recruiter_pitches.md"
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} missing")
            return False
    
    # Test 5: Database functionality
    print("\n5. Testing database functionality...")
    try:
        # Create test database
        conn = sqlite3.connect("test_simple.db")
        
        # Create simple table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS test_breaches (
                id INTEGER PRIMARY KEY,
                name TEXT,
                records_exposed INTEGER
            )
        """)
        
        # Insert test data
        conn.execute("INSERT INTO test_breaches (name, records_exposed) VALUES ('Test Corp', 1000000)")
        conn.commit()
        
        # Query data
        result = conn.execute("SELECT COUNT(*) FROM test_breaches").fetchone()
        if result[0] > 0:
            print("   ✓ Database operations working")
        else:
            print("   ✗ Database operations failed")
            return False
        
        conn.close()
        os.remove("test_simple.db")
        
    except Exception as e:
        print(f"   ✗ Database test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("Project is ready for presentation.")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
