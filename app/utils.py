"""
Utility functions for the Data Breach Insights Dashboard
"""

import pandas as pd

def format_number(num):
    """Format large numbers with commas"""
    if pd.isna(num):
        return "N/A"
    return f"{num:,.0f}"

def format_currency(amount):
    """Format currency amounts"""
    if pd.isna(amount):
        return "N/A"
    return f"${amount:,.0f}"

def calculate_percentage_change(old_val, new_val):
    """Calculate percentage change between two values"""
    if pd.isna(old_val) or pd.isna(new_val) or old_val == 0:
        return 0
    return ((new_val - old_val) / old_val) * 100

def create_summary_stats(df):
    """Create summary statistics for the dataset"""
    return {
        'total_records': len(df),
        'total_exposed': df['records_exposed'].sum() if 'records_exposed' in df.columns else 0,
        'total_cost': df['estimated_cost'].sum() if 'estimated_cost' in df.columns else 0
    }