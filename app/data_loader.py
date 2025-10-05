"""
Data Breach Insights Report - Data Loader Module

This module handles data loading, cleaning, and preprocessing for the Streamlit dashboard.
Supports both CSV files and database connections with caching for optimal performance.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
import sqlite3
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Handles data loading and preprocessing for the breach insights dashboard."""
    
    def __init__(self):
        # Use absolute path to ensure we find the data file
        current_dir = Path(__file__).parent.parent
        self.data_path = current_dir / "data" / "sample_breaches.csv"
        self.powerbi_data_path = current_dir / "powerbi" / "breaches_for_powerbi.csv"
        self.db_path = current_dir / "data.db"
        
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def load_data(_self, source: str = "csv") -> pd.DataFrame:
        """
        Load breach data from CSV or database with caching.
        
        Args:
            source (str): Data source - 'csv' or 'db'
            
        Returns:
            pd.DataFrame: Cleaned breach data
        """
        try:
            # Try powerbi data first (most comprehensive)
            if source == "csv" and _self.powerbi_data_path.exists():
                df = pd.read_csv(_self.powerbi_data_path)
                logger.info(f"Loaded {len(df)} records from PowerBI CSV")
            elif source == "csv" and _self.data_path.exists():
                df = pd.read_csv(_self.data_path)
                logger.info(f"Loaded {len(df)} records from basic CSV")
            elif source == "db" and _self.db_path.exists():
                conn = sqlite3.connect(_self.db_path)
                df = pd.read_sql_query("SELECT * FROM breaches", conn)
                conn.close()
                logger.info(f"Loaded {len(df)} records from database")
            else:
                # Fallback to sample data
                df = _self._create_sample_data()
                logger.warning("Using sample data - no data files found")
            
            return _self._clean_data(df)
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return _self._create_sample_data()
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess the breach data.
        
        Args:
            df (pd.DataFrame): Raw breach data
            
        Returns:
            pd.DataFrame: Cleaned data with additional calculated fields
        """
        # Standardize column names - handle different date column variations
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(date_keyword in col_lower for date_keyword in ['date', 'breach_date', 'incident_date', 'occurred']):
                column_mapping[col] = 'breach_date'
            elif any(records_keyword in col_lower for records_keyword in ['records', 'exposed', 'affected', 'compromised']):
                column_mapping[col] = 'records_exposed'
            elif any(company_keyword in col_lower for company_keyword in ['company', 'organization', 'entity', 'name']):
                column_mapping[col] = 'name'
        
        # Apply column mapping
        df = df.rename(columns=column_mapping)
        
        # Ensure required columns exist, create them if missing
        required_columns = {
            'breach_date': '2020-01-01',
            'records_exposed': 0,
            'name': 'Unknown Company',
            'industry': 'Unknown',
            'country': 'Unknown',
            'breach_type': 'Unknown'
        }
        
        for col, default_val in required_columns.items():
            if col not in df.columns:
                df[col] = default_val
                logger.warning(f"Column '{col}' not found, using default value")
        
        # Convert date column
        df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
        
        # Extract year for filtering
        df['year'] = df['breach_date'].dt.year
        
        # Clean numeric columns
        df['records_exposed'] = pd.to_numeric(df['records_exposed'], errors='coerce')
        
        # Calculate estimated cost ($200 per record)
        df['estimated_cost'] = df['records_exposed'] * 200
        
        # Clean text columns
        df['industry'] = df['industry'].str.strip().str.title()
        df['country'] = df['country'].str.strip().str.upper()
        df['breach_type'] = df['breach_type'].str.strip().str.title()
        df['name'] = df['name'].str.strip()
        
        # Handle missing values
        df['industry'] = df['industry'].fillna('Unknown')
        df['country'] = df['country'].fillna('Unknown')
        df['breach_type'] = df['breach_type'].fillna('Unknown')
        df['records_exposed'] = df['records_exposed'].fillna(0)
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['breach_date'])
        
        # Ensure we have an 'id' column for counting purposes
        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)
            logger.info("Added 'id' column for data processing")
        
        logger.info(f"Data cleaned: {len(df)} valid records")
        return df
    
    def _create_sample_data(self) -> pd.DataFrame:
        """Create sample data if no data files are available."""
        sample_data = {
            'id': range(1, 101),
            'breach_date': pd.date_range('2020-01-01', periods=100, freq='D'),
            'name': [f'Company {i}' for i in range(1, 101)],
            'industry': np.random.choice(['Healthcare', 'Financial', 'Technology', 'Retail', 'Government'], 100),
            'country': np.random.choice(['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'JP'], 100),
            'records_exposed': np.random.randint(1000, 1000000, 100),
            'breach_type': np.random.choice(['Hacking', 'Insider', 'Physical', 'Social Engineering', 'System Error'], 100),
            'source_url': [f'https://example.com/breach-{i}' for i in range(1, 101)]
        }
        return pd.DataFrame(sample_data)
    
    @st.cache_data
    def get_filtered_data(_self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to the dataset.
        
        Args:
            df (pd.DataFrame): Source data
            filters (Dict): Filter parameters
            
        Returns:
            pd.DataFrame: Filtered data
        """
        filtered_df = df.copy()
        
        # Year range filter
        if 'year_range' in filters and filters['year_range']:
            min_year, max_year = filters['year_range']
            filtered_df = filtered_df[
                (filtered_df['year'] >= min_year) & 
                (filtered_df['year'] <= max_year)
            ]
        
        # Industry filter
        if 'industries' in filters and filters['industries']:
            filtered_df = filtered_df[filtered_df['industry'].isin(filters['industries'])]
        
        # Country filter
        if 'countries' in filters and filters['countries']:
            filtered_df = filtered_df[filtered_df['country'].isin(filters['countries'])]
        
        # Breach type filter
        if 'breach_types' in filters and filters['breach_types']:
            filtered_df = filtered_df[filtered_df['breach_type'].isin(filters['breach_types'])]
        
        # Company name search
        if 'company_search' in filters and filters['company_search']:
            search_term = filters['company_search'].lower()
            filtered_df = filtered_df[
                filtered_df['name'].str.lower().str.contains(search_term, na=False)
            ]
        
        return filtered_df
    
    @st.cache_data
    def get_kpi_metrics(_self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate key performance indicators.
        
        Args:
            df (pd.DataFrame): Source data
            
        Returns:
            Dict: KPI metrics
        """
        return {
            'total_breaches': len(df),
            'total_records': df['records_exposed'].sum(),
            'avg_cost': df['estimated_cost'].mean() / 1_000_000,  # Convert to millions
            'most_affected_industry': df['industry'].mode().iloc[0] if not df.empty else 'N/A',
            'avg_breach_size': df['records_exposed'].mean(),
            'total_cost': df['estimated_cost'].sum() / 1_000_000_000,  # Convert to billions
            'unique_companies': df['name'].nunique(),
            'unique_countries': df['country'].nunique()
        }
    
    @st.cache_data
    def get_industry_breakdown(_self, df: pd.DataFrame) -> pd.DataFrame:
        """Get industry distribution data."""
        # Use the first column as count if 'id' doesn't exist
        count_col = 'id' if 'id' in df.columns else df.columns[0]
        
        agg_dict = {
            count_col: 'count',
            'records_exposed': 'sum',
            'estimated_cost': 'sum'
        }
        
        # Only include columns that exist
        agg_dict = {col: func for col, func in agg_dict.items() if col in df.columns}
        
        result = df.groupby('industry').agg(agg_dict).reset_index()
        
        # Rename the count column to breach_count
        if count_col in result.columns:
            result = result.rename(columns={count_col: 'breach_count'})
        
        return result
    
    @st.cache_data
    def get_yearly_trends(_self, df: pd.DataFrame) -> pd.DataFrame:
        """Get yearly trend data."""
        # Use the first column as count if 'id' doesn't exist
        count_col = 'id' if 'id' in df.columns else df.columns[0]
        
        agg_dict = {
            count_col: 'count',
            'records_exposed': 'sum',
            'estimated_cost': 'sum'
        }
        
        # Only include columns that exist
        agg_dict = {col: func for col, func in agg_dict.items() if col in df.columns}
        
        result = df.groupby('year').agg(agg_dict).reset_index()
        
        # Rename the count column to breach_count
        if count_col in result.columns:
            result = result.rename(columns={count_col: 'breach_count'})
        
        return result
    
    @st.cache_data
    def get_country_data(_self, df: pd.DataFrame) -> pd.DataFrame:
        """Get country distribution data."""
        # Use the first column as count if 'id' doesn't exist
        count_col = 'id' if 'id' in df.columns else df.columns[0]
        
        agg_dict = {
            count_col: 'count',
            'records_exposed': 'sum',
            'estimated_cost': 'sum'
        }
        
        # Only include columns that exist
        agg_dict = {col: func for col, func in agg_dict.items() if col in df.columns}
        
        result = df.groupby('country').agg(agg_dict).reset_index()
        
        # Rename the count column to breach_count
        if count_col in result.columns:
            result = result.rename(columns={count_col: 'breach_count'})
        
        return result
    
    @st.cache_data
    def get_top_companies(_self, df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
        """Get top companies by records exposed."""
        return df.nlargest(limit, 'records_exposed')[
            ['name', 'industry', 'country', 'records_exposed', 'estimated_cost', 'breach_date']
        ].reset_index(drop=True)

