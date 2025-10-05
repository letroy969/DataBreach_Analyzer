#!/usr/bin/env python3
"""
Test SQL queries for Data Breach Insights Report.
"""

import sqlite3
import pandas as pd

def test_queries():
    """Test the analytical queries."""
    # Connect to database
    conn = sqlite3.connect('data.db')
    
    # Test queries
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
    
    for query_name, query_sql in queries:
        print(f"\n📈 {query_name}:")
        try:
            df = pd.read_sql_query(query_sql, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    test_queries()
