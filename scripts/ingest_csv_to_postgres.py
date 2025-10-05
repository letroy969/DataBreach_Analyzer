#!/usr/bin/env python3
"""
Data ingestion script for Data Breach Insights Report.

Loads CSV data into PostgreSQL or SQLite database for analysis.
Supports both local development and production environments.
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Database connection configurations
DB_CONFIGS = {
    'postgresql': {
        'default_url': 'postgresql://user:password@localhost:5432/breach_db',
        'driver': 'psycopg2'
    },
    'sqlite': {
        'default_url': 'sqlite:///data.db',
        'driver': 'sqlite3'
    }
}

def parse_database_url(db_url: str) -> Dict[str, Any]:
    """Parse database URL and return connection details."""
    if db_url.startswith('sqlite'):
        return {
            'type': 'sqlite',
            'url': db_url,
            'driver': 'sqlite3'
        }
    elif db_url.startswith('postgresql'):
        return {
            'type': 'postgresql',
            'url': db_url,
            'driver': 'psycopg2'
        }
    else:
        raise ValueError(f"Unsupported database URL: {db_url}")

def create_database_engine(db_url: str) -> Any:
    """Create SQLAlchemy engine for database connection."""
    try:
        engine = create_engine(db_url, echo=False)
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        sys.exit(1)

def load_schema(engine: Any, schema_file: str) -> bool:
    """Load database schema from SQL file."""
    try:
        schema_path = Path(schema_file)
        if not schema_path.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        with engine.connect() as conn:
            for statement in statements:
                if statement:
                    conn.execute(text(statement))
            conn.commit()
        
        print(f"✅ Schema loaded successfully from {schema_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading schema: {e}")
        return False

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the dataframe."""
    print("🧹 Cleaning data...")
    
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    # Convert breach_date to datetime
    df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
    
    # Ensure records_exposed is numeric
    df['records_exposed'] = pd.to_numeric(df['records_exposed'], errors='coerce')
    
    # Fill missing values
    df['source_url'] = df['source_url'].fillna('')
    df['breach_type'] = df['breach_type'].fillna('Unknown')
    
    # Standardize industry names (basic cleaning)
    df['industry'] = df['industry'].str.strip().str.title()
    
    # Remove any rows with invalid dates or records
    df = df.dropna(subset=['breach_date', 'records_exposed'])
    
    # Ensure records_exposed is positive
    df = df[df['records_exposed'] > 0]
    
    print(f"✅ Data cleaned: {len(df)} valid records")
    return df

def load_csv_data(engine: Any, csv_file: str, table_name: str = 'breaches') -> bool:
    """Load CSV data into database table."""
    try:
        print(f"📊 Loading data from {csv_file}...")
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        print(f"📈 Read {len(df)} records from CSV")
        
        # Clean the data
        df = clean_dataframe(df)
        
        # Load into database
        df.to_sql(
            table_name, 
            engine, 
            if_exists='replace', 
            index=False,
            method='multi'
        )
        
        print(f"✅ Successfully loaded {len(df)} records into {table_name} table")
        return True
        
    except Exception as e:
        print(f"❌ Error loading CSV data: {e}")
        return False

def verify_data_load(engine: Any, table_name: str = 'breaches') -> bool:
    """Verify that data was loaded correctly."""
    try:
        with engine.connect() as conn:
            # Check record count
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"📊 Total records in database: {count}")
            
            # Check date range
            result = conn.execute(text(f"""
                SELECT 
                    MIN(breach_date) as earliest,
                    MAX(breach_date) as latest,
                    SUM(records_exposed) as total_records
                FROM {table_name}
            """))
            row = result.fetchone()
            print(f"📅 Date range: {row[0]} to {row[1]}")
            print(f"🔢 Total records exposed: {row[2]:,}")
            
            # Check industry distribution
            result = conn.execute(text(f"""
                SELECT industry, COUNT(*) as count
                FROM {table_name}
                GROUP BY industry
                ORDER BY count DESC
                LIMIT 5
            """))
            print("🏭 Top 5 industries:")
            for row in result:
                print(f"   {row[0]}: {row[1]} breaches")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def run_sample_queries(engine: Any) -> None:
    """Run sample analytical queries to demonstrate functionality."""
    try:
        print("\n🔍 Running sample analytical queries...")
        
        queries = [
            ("Breaches by year", """
                SELECT 
                    strftime('%Y', breach_date) AS year,
                    COUNT(*) AS breach_count,
                    SUM(records_exposed) AS total_records
                FROM breaches
                GROUP BY strftime('%Y', breach_date)
                ORDER BY year
            """),
            ("Top 5 industries by records", """
                SELECT 
                    industry,
                    SUM(records_exposed) AS total_records
                FROM breaches
                GROUP BY industry
                ORDER BY total_records DESC
                LIMIT 5
            """),
            ("Breach types distribution", """
                SELECT 
                    breach_type,
                    COUNT(*) AS count
                FROM breaches
                GROUP BY breach_type
                ORDER BY count DESC
            """)
        ]
        
        with engine.connect() as conn:
            for query_name, query_sql in queries:
                print(f"\n📈 {query_name}:")
                result = conn.execute(text(query_sql))
                for row in result:
                    print(f"   {dict(row._mapping)}")
        
    except Exception as e:
        print(f"❌ Error running sample queries: {e}")

def main():
    """Main function to orchestrate data ingestion."""
    parser = argparse.ArgumentParser(
        description="Load breach data into database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # SQLite (default)
  python ingest_csv_to_postgres.py --csv data/sample_breaches.csv
  
  # PostgreSQL
  python ingest_csv_to_postgres.py --csv data/sample_breaches.csv --db postgresql://user:pass@localhost:5432/breach_db
  
  # Custom SQLite location
  python ingest_csv_to_postgres.py --csv data/sample_breaches.csv --db sqlite:///custom.db
        """
    )
    
    parser.add_argument(
        '--csv', 
        required=True,
        help='Path to CSV file to load'
    )
    parser.add_argument(
        '--db',
        default='sqlite:///data.db',
        help='Database URL (default: sqlite:///data.db)'
    )
    parser.add_argument(
        '--schema',
        default='sql/schema.sql',
        help='Path to schema SQL file (default: sql/schema.sql)'
    )
    parser.add_argument(
        '--table',
        default='breaches',
        help='Target table name (default: breaches)'
    )
    parser.add_argument(
        '--skip-schema',
        action='store_true',
        help='Skip schema loading (assumes tables exist)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify existing data, do not load new data'
    )
    parser.add_argument(
        '--sample-queries',
        action='store_true',
        help='Run sample analytical queries after loading'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.csv):
        print(f"❌ CSV file not found: {args.csv}")
        sys.exit(1)
    
    # Create database engine
    print(f"Connecting to database: {args.db}")
    engine = create_database_engine(args.db)
    
    # Load schema if not skipped
    if not args.skip_schema:
        if not load_schema(engine, args.schema):
            sys.exit(1)
    
    # Load data unless verify-only mode
    if not args.verify_only:
        if not load_csv_data(engine, args.csv, args.table):
            sys.exit(1)
    
    # Verify data load
    if not verify_data_load(engine, args.table):
        sys.exit(1)
    
    # Run sample queries if requested
    if args.sample_queries:
        run_sample_queries(engine)
    
    print("\n🎉 Data ingestion completed successfully!")
    print(f"💡 You can now run analytical queries using: sqlite3 {args.db.split(':///')[-1]} < sql/queries.sql")

if __name__ == "__main__":
    main()
