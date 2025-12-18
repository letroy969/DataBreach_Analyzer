"""
Test script for the Streamlit application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader
from visuals import ChartBuilder
from utils import format_number, format_currency
from insights import AIInsights

def test_imports():
    """Test that all modules can be imported successfully."""
    print("✅ Testing imports...")
    
    try:
        from data_loader import DataLoader
        print("✅ DataLoader imported successfully")
    except Exception as e:
        print(f"❌ DataLoader import failed: {e}")
        return False
    
    try:
        from visuals import ChartBuilder
        print("✅ ChartBuilder imported successfully")
    except Exception as e:
        print(f"❌ ChartBuilder import failed: {e}")
        return False
    
    try:
        from utils import format_number, format_currency
        print("✅ Utils imported successfully")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    try:
        from insights import AIInsights
        print("✅ AIInsights imported successfully")
    except Exception as e:
        print(f"❌ AIInsights import failed: {e}")
        return False
    
    return True

def test_data_loader():
    """Test the DataLoader class."""
    print("\n✅ Testing DataLoader...")
    
    try:
        loader = DataLoader()
        print("✅ DataLoader initialized")
        
        # Test sample data creation
        sample_df = loader._create_sample_data()
        print(f"✅ Sample data created: {len(sample_df)} records")
        
        # Test data cleaning
        cleaned_df = loader._clean_data(sample_df)
        print(f"✅ Data cleaned: {len(cleaned_df)} records")
        
        # Test KPI calculation
        kpis = loader.get_kpi_metrics(cleaned_df)
        print(f"✅ KPIs calculated: {kpis['total_breaches']} breaches")
        
        return True
    except Exception as e:
        print(f"❌ DataLoader test failed: {e}")
        return False

def test_visuals():
    """Test the ChartBuilder class."""
    print("\n✅ Testing ChartBuilder...")
    
    try:
        builder = ChartBuilder()
        print("✅ ChartBuilder initialized")
        
        # Create sample data for testing
        import pandas as pd
        import numpy as np
        
        sample_data = {
            'year': [2020, 2021, 2022, 2023, 2024],
            'breach_count': [10, 15, 20, 25, 30],
            'industry': ['Healthcare', 'Financial', 'Technology', 'Retail', 'Government'],
            'breach_count_industry': [5, 8, 12, 7, 9]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Test trend chart
        trends_chart = builder.create_trends_chart(df)
        print("✅ Trends chart created")
        
        # Test industry chart
        industry_df = pd.DataFrame({
            'industry': ['Healthcare', 'Financial', 'Technology'],
            'breach_count': [10, 15, 20]
        })
        industry_chart = builder.create_industry_chart(industry_df)
        print("✅ Industry chart created")
        
        return True
    except Exception as e:
        print(f"❌ ChartBuilder test failed: {e}")
        return False

def test_utils():
    """Test utility functions."""
    print("\n✅ Testing Utils...")
    
    try:
        from utils import format_number, format_currency, calculate_percentage_change
        
        # Test number formatting
        formatted = format_number(1500000, 1, "M")
        print(f"✅ Number formatting: {formatted}")
        
        # Test currency formatting
        currency = format_currency(2500000)
        print(f"✅ Currency formatting: {currency}")
        
        # Test percentage change
        change, change_str = calculate_percentage_change(100, 80)
        print(f"✅ Percentage change: {change_str}")
        
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_insights():
    """Test the AIInsights class."""
    print("\n✅ Testing AIInsights...")
    
    try:
        insights = AIInsights()
        print("✅ AIInsights initialized")
        
        # Test fallback summary generation
        import pandas as pd
        sample_df = pd.DataFrame({
            'breach_date': pd.date_range('2020-01-01', periods=10),
            'records_exposed': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
            'industry': ['Healthcare'] * 5 + ['Financial'] * 5,
            'estimated_cost': [200000, 400000, 600000, 800000, 1000000, 1200000, 1400000, 1600000, 1800000, 2000000]
        })
        
        kpis = {'total_breaches': 10, 'total_records': 55000, 'avg_cost': 1.1, 'most_affected_industry': 'Healthcare'}
        
        summary = insights.generate_executive_summary(sample_df, kpis)
        print("✅ Executive summary generated")
        print(f"Summary length: {len(summary)} characters")
        
        return True
    except Exception as e:
        print(f"❌ AIInsights test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Streamlit App Tests\n")
    
    tests = [
        test_imports,
        test_data_loader,
        test_visuals,
        test_utils,
        test_insights
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Streamlit app is ready to run.")
        print("\n🚀 To run the app:")
        print("   streamlit run app/app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()




