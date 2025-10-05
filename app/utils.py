"""
Data Breach Insights Report - Utility Functions

This module contains helper functions, data processing utilities,
and common operations used throughout the Streamlit application.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime, timedelta
import json

def format_number(value: float, decimals: int = 0, suffix: str = "") -> str:
    """
    Format numbers with appropriate suffixes (K, M, B).
    
    Args:
        value (float): Number to format
        decimals (int): Number of decimal places
        suffix (str): Additional suffix
        
    Returns:
        str: Formatted number string
    """
    if pd.isna(value) or value == 0:
        return "0" + suffix
    
    abs_value = abs(value)
    
    if abs_value >= 1_000_000_000:
        formatted = f"{value / 1_000_000_000:.{decimals}f}B"
    elif abs_value >= 1_000_000:
        formatted = f"{value / 1_000_000:.{decimals}f}M"
    elif abs_value >= 1_000:
        formatted = f"{value / 1_000:.{decimals}f}K"
    else:
        formatted = f"{value:.{decimals}f}"
    
    return formatted + suffix

def format_currency(value: float, currency: str = "$") -> str:
    """
    Format currency values with appropriate suffixes.
    
    Args:
        value (float): Currency value
        currency (str): Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value) or value == 0:
        return f"{currency}0"
    
    abs_value = abs(value)
    
    if abs_value >= 1_000_000_000:
        formatted = f"{currency}{value / 1_000_000_000:.1f}B"
    elif abs_value >= 1_000_000:
        formatted = f"{currency}{value / 1_000_000:.1f}M"
    elif abs_value >= 1_000:
        formatted = f"{currency}{value / 1_000:.1f}K"
    else:
        formatted = f"{currency}{value:,.0f}"
    
    return formatted

def calculate_percentage_change(current: float, previous: float) -> Tuple[float, str]:
    """
    Calculate percentage change between two values.
    
    Args:
        current (float): Current value
        previous (float): Previous value
        
    Returns:
        Tuple[float, str]: (change_value, change_string)
    """
    if previous == 0:
        return 0, "0%"
    
    change = ((current - previous) / previous) * 100
    change_str = f"{change:+.1f}%"
    
    return change, change_str

def get_risk_level(records_exposed: int) -> Tuple[str, str]:
    """
    Determine risk level based on records exposed.
    
    Args:
        records_exposed (int): Number of records exposed
        
    Returns:
        Tuple[str, str]: (risk_level, color)
    """
    if records_exposed >= 1_000_000:
        return "Critical", "🔴"
    elif records_exposed >= 100_000:
        return "High", "🟠"
    elif records_exposed >= 10_000:
        return "Medium", "🟡"
    else:
        return "Low", "🟢"

def get_industry_risk_score(industry: str) -> int:
    """
    Get risk score for different industries (1-10 scale).
    
    Args:
        industry (str): Industry name
        
    Returns:
        int: Risk score (1-10)
    """
    risk_scores = {
        'Healthcare': 9,
        'Financial': 8,
        'Government': 7,
        'Technology': 6,
        'Education': 5,
        'Retail': 4,
        'Manufacturing': 3,
        'Transportation': 2,
        'Media': 1
    }
    
    return risk_scores.get(industry, 5)

def clean_company_name(name: str) -> str:
    """
    Clean and standardize company names.
    
    Args:
        name (str): Raw company name
        
    Returns:
        str: Cleaned company name
    """
    if pd.isna(name):
        return "Unknown"
    
    # Remove common suffixes and clean up
    name = str(name).strip()
    name = re.sub(r'\s+(Inc|LLC|Ltd|Corp|Corporation|Company|Co)\.?$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)  # Remove extra spaces
    
    return name.title()

def get_country_full_name(country_code: str) -> str:
    """
    Get full country name from country code.
    
    Args:
        country_code (str): Two-letter country code
        
    Returns:
        str: Full country name
    """
    country_mapping = {
        'US': 'United States',
        'CA': 'Canada',
        'GB': 'United Kingdom',
        'DE': 'Germany',
        'FR': 'France',
        'AU': 'Australia',
        'JP': 'Japan',
        'IN': 'India',
        'BR': 'Brazil',
        'MX': 'Mexico',
        'IT': 'Italy',
        'ES': 'Spain',
        'NL': 'Netherlands',
        'SE': 'Sweden',
        'NO': 'Norway',
        'DK': 'Denmark',
        'FI': 'Finland',
        'CH': 'Switzerland',
        'AT': 'Austria',
        'BE': 'Belgium'
    }
    
    return country_mapping.get(country_code, country_code)

def create_summary_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create comprehensive summary statistics.
    
    Args:
        df (pd.DataFrame): Source data
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    if df.empty:
        return {}
    
    return {
        'total_records': len(df),
        'date_range': {
            'start': df['breach_date'].min(),
            'end': df['breach_date'].max()
        },
        'industries': df['industry'].nunique(),
        'countries': df['country'].nunique(),
        'companies': df['name'].nunique(),
        'total_exposed': df['records_exposed'].sum(),
        'avg_exposed': df['records_exposed'].mean(),
        'median_exposed': df['records_exposed'].median(),
        'total_cost': df['estimated_cost'].sum(),
        'avg_cost': df['estimated_cost'].mean(),
        'most_common_industry': df['industry'].mode().iloc[0] if not df['industry'].mode().empty else 'N/A',
        'most_common_country': df['country'].mode().iloc[0] if not df['country'].mode().empty else 'N/A',
        'most_common_breach_type': df['breach_type'].mode().iloc[0] if not df['breach_type'].mode().empty else 'N/A'
    }

def validate_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean filter parameters.
    
    Args:
        filters (Dict[str, Any]): Raw filter parameters
        
    Returns:
        Dict[str, Any]: Validated filters
    """
    validated = {}
    
    # Year range validation
    if 'year_range' in filters and filters['year_range']:
        min_year, max_year = filters['year_range']
        if min_year <= max_year:
            validated['year_range'] = (int(min_year), int(max_year))
    
    # List filters validation
    for key in ['industries', 'countries', 'breach_types']:
        if key in filters and filters[key]:
            validated[key] = [str(item).strip() for item in filters[key] if str(item).strip()]
    
    # Text search validation
    if 'company_search' in filters and filters['company_search']:
        search_term = str(filters['company_search']).strip()
        if search_term:
            validated['company_search'] = search_term
    
    return validated

def create_export_data(df: pd.DataFrame, format_type: str = 'csv') -> bytes:
    """
    Create export data in specified format.
    
    Args:
        df (pd.DataFrame): Data to export
        format_type (str): Export format ('csv', 'json', 'excel')
        
    Returns:
        bytes: Export data
    """
    if format_type == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif format_type == 'json':
        return df.to_json(orient='records', date_format='iso').encode('utf-8')
    elif format_type == 'excel':
        # For Excel, we'd need openpyxl, but for now return CSV
        return df.to_csv(index=False).encode('utf-8')
    else:
        return df.to_csv(index=False).encode('utf-8')

def get_breach_severity(records_exposed: int, industry: str) -> str:
    """
    Calculate breach severity based on records and industry.
    
    Args:
        records_exposed (int): Number of records exposed
        industry (str): Industry type
        
    Returns:
        str: Severity level
    """
    # Industry risk multipliers
    risk_multipliers = {
        'Healthcare': 1.5,
        'Financial': 1.3,
        'Government': 1.2,
        'Technology': 1.1,
        'Education': 1.0,
        'Retail': 0.9,
        'Manufacturing': 0.8
    }
    
    multiplier = risk_multipliers.get(industry, 1.0)
    adjusted_records = records_exposed * multiplier
    
    if adjusted_records >= 1_000_000:
        return "Critical"
    elif adjusted_records >= 100_000:
        return "High"
    elif adjusted_records >= 10_000:
        return "Medium"
    else:
        return "Low"

def create_time_series_data(df: pd.DataFrame, frequency: str = 'M') -> pd.DataFrame:
    """
    Create time series data for trend analysis.
    
    Args:
        df (pd.DataFrame): Source data
        frequency (str): Time frequency ('D', 'W', 'M', 'Q', 'Y')
        
    Returns:
        pd.DataFrame: Time series data
    """
    df_copy = df.copy()
    df_copy['date'] = pd.to_datetime(df_copy['breach_date'])
    df_copy.set_index('date', inplace=True)
    
    # Resample by frequency
    time_series = df_copy.resample(frequency).agg({
        'id': 'count',
        'records_exposed': 'sum',
        'estimated_cost': 'sum'
    }).fillna(0)
    
    time_series.columns = ['breach_count', 'total_records', 'total_cost']
    time_series.reset_index(inplace=True)
    
    return time_series

def calculate_correlation_matrix(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calculate correlation matrix for specified columns.
    
    Args:
        df (pd.DataFrame): Source data
        columns (List[str]): Columns to include in correlation
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    numeric_columns = df[columns].select_dtypes(include=[np.number]).columns
    return df[numeric_columns].corr()

def get_top_performers(df: pd.DataFrame, metric: str, limit: int = 10) -> pd.DataFrame:
    """
    Get top performers by specified metric.
    
    Args:
        df (pd.DataFrame): Source data
        metric (str): Metric to rank by
        limit (int): Number of top performers to return
        
    Returns:
        pd.DataFrame: Top performers
    """
    return df.nlargest(limit, metric).reset_index(drop=True)

def create_breach_timeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a timeline of breaches for visualization.
    
    Args:
        df (pd.DataFrame): Source data
        
    Returns:
        pd.DataFrame: Timeline data
    """
    timeline = df.copy()
    timeline['year_month'] = timeline['breach_date'].dt.to_period('M')
    
    timeline_summary = timeline.groupby('year_month').agg({
        'id': 'count',
        'records_exposed': 'sum',
        'estimated_cost': 'sum',
        'name': lambda x: ', '.join(x.head(3))  # Top 3 companies
    }).reset_index()
    
    timeline_summary.columns = ['period', 'breach_count', 'total_records', 'total_cost', 'top_companies']
    
    return timeline_summary

