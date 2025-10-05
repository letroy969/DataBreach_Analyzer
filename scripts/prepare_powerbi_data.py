#!/usr/bin/env python3
"""
Prepare data for Power BI dashboard.

This script creates Power BI-ready data files and generates
the executive report PDF content.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import os
from pathlib import Path

def load_and_enhance_data(csv_file: str) -> pd.DataFrame:
    """Load and enhance data for Power BI."""
    print(f"📊 Loading data from {csv_file}...")
    
    df = pd.read_csv(csv_file)
    
    # Convert date
    df['breach_date'] = pd.to_datetime(df['breach_date'])
    
    # Add derived columns
    df['year'] = df['breach_date'].dt.year
    df['month'] = df['breach_date'].dt.month
    df['quarter'] = df['breach_date'].dt.quarter
    df['is_large_breach'] = df['records_exposed'] >= 1000000
    
    # Severity classification
    def classify_severity(records):
        if records <= 1000:
            return 'Low'
        elif records <= 10000:
            return 'Medium'
        elif records <= 100000:
            return 'High'
        elif records <= 1000000:
            return 'Critical'
        else:
            return 'Catastrophic'
    
    df['severity_level'] = df['records_exposed'].apply(classify_severity)
    
    # Add region mapping
    region_mapping = {
        'US': 'North America', 'CA': 'North America',
        'GB': 'Europe', 'DE': 'Europe', 'FR': 'Europe', 'IT': 'Europe',
        'ES': 'Europe', 'NL': 'Europe', 'SE': 'Europe', 'NO': 'Europe',
        'DK': 'Europe', 'FI': 'Europe', 'CH': 'Europe', 'AT': 'Europe',
        'BE': 'Europe',
        'AU': 'Oceania',
        'JP': 'Asia', 'IN': 'Asia', 'CN': 'Asia',
        'BR': 'South America'
    }
    
    df['region'] = df['country'].map(region_mapping).fillna('Other')
    
    print(f"✅ Enhanced {len(df)} records for Power BI")
    return df

def create_lookup_tables():
    """Create dimension tables for Power BI."""
    
    # Industry lookup
    industry_lookup = pd.DataFrame({
        'industry': ['Healthcare', 'Financial', 'Technology', 'Retail', 'Government',
                    'Education', 'Energy', 'Manufacturing', 'Transportation', 'Media'],
        'category': ['Critical Infrastructure', 'Critical Infrastructure', 'Information Technology',
                    'Consumer Services', 'Public Sector', 'Public Sector', 'Critical Infrastructure',
                    'Industrial', 'Critical Infrastructure', 'Consumer Services'],
        'risk_level': ['High', 'High', 'Medium', 'Medium', 'High', 'Medium', 'High', 'Medium', 'High', 'Low']
    })
    
    # Country lookup
    country_lookup = pd.DataFrame({
        'country_code': ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'JP', 'IN', 'BR', 'CN',
                        'IT', 'ES', 'NL', 'SE', 'NO', 'DK', 'FI', 'CH', 'AT', 'BE'],
        'country_name': ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany',
                        'France', 'Japan', 'India', 'Brazil', 'China', 'Italy', 'Spain',
                        'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Switzerland',
                        'Austria', 'Belgium'],
        'region': ['North America', 'Europe', 'North America', 'Oceania', 'Europe',
                  'Europe', 'Asia', 'Asia', 'South America', 'Asia', 'Europe', 'Europe',
                  'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe'],
        'gdp_per_capita': [65000, 45000, 50000, 55000, 50000, 45000, 40000, 2000, 8000, 10000,
                          35000, 30000, 55000, 55000, 75000, 60000, 50000, 80000, 50000, 45000]
    })
    
    # Breach severity lookup
    breach_severity = pd.DataFrame({
        'severity_level': ['Low', 'Medium', 'High', 'Critical', 'Catastrophic'],
        'records_min': [0, 1001, 10001, 100001, 1000001],
        'records_max': [1000, 10000, 100000, 1000000, 999999999999],
        'description': ['Small breach with minimal impact',
                       'Moderate breach requiring attention',
                       'Large breach with significant impact',
                       'Major breach with severe consequences',
                       'Massive breach with devastating impact']
    })
    
    return industry_lookup, country_lookup, breach_severity

def create_powerbi_files(df: pd.DataFrame, output_dir: str):
    """Create Power BI-ready data files."""
    print(f"📁 Creating Power BI files in {output_dir}...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Main breaches table
    breaches_file = os.path.join(output_dir, 'breaches_for_powerbi.csv')
    df.to_csv(breaches_file, index=False)
    print(f"✅ Created {breaches_file}")
    
    # Lookup tables
    industry_lookup, country_lookup, breach_severity = create_lookup_tables()
    
    industry_file = os.path.join(output_dir, 'industry_lookup.csv')
    industry_lookup.to_csv(industry_file, index=False)
    print(f"✅ Created {industry_file}")
    
    country_file = os.path.join(output_dir, 'country_lookup.csv')
    country_lookup.to_csv(country_file, index=False)
    print(f"✅ Created {country_file}")
    
    severity_file = os.path.join(output_dir, 'breach_severity.csv')
    breach_severity.to_csv(severity_file, index=False)
    print(f"✅ Created {severity_file}")
    
    # Create data connection instructions
    instructions_file = os.path.join(output_dir, 'CONNECTION_INSTRUCTIONS.md')
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write("""# Power BI Data Connection Instructions

## 📊 Data Files
- `breaches_for_powerbi.csv` - Main data table
- `industry_lookup.csv` - Industry dimension table
- `country_lookup.csv` - Country dimension table
- `breach_severity.csv` - Severity dimension table

## 🔌 Connection Steps

### Method 1: CSV Files
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select each CSV file
4. Configure data types:
   - breach_date: Date
   - records_exposed: Whole Number
   - All others: Text

### Method 2: Database Connection
1. Get Data → Database → PostgreSQL database
2. Server: localhost
3. Database: breach_db
4. Username: breach_user
5. Password: breach_password

## 🔗 Relationships
- breaches[industry] → industry_lookup[industry]
- breaches[country] → country_lookup[country_code]
- breaches[records_exposed] → breach_severity (based on ranges)

## 📊 Key Measures
See powerbi/README.md for DAX measures and dashboard setup.
""")
    
    print(f"✅ Created {instructions_file}")

def generate_executive_summary(df: pd.DataFrame, output_file: str):
    """Generate executive summary content."""
    print(f"📄 Generating executive summary...")
    
    # Calculate key metrics
    total_breaches = len(df)
    total_records = df['records_exposed'].sum()
    avg_breach_size = df['records_exposed'].mean()
    largest_breach = df['records_exposed'].max()
    
    # Year-over-year analysis
    current_year = df['year'].max()
    prev_year = current_year - 1
    
    current_year_breaches = len(df[df['year'] == current_year])
    prev_year_breaches = len(df[df['year'] == prev_year])
    yoy_change = ((current_year_breaches - prev_year_breaches) / prev_year_breaches * 100) if prev_year_breaches > 0 else 0
    
    # Top industry
    top_industry = df.groupby('industry')['records_exposed'].sum().idxmax()
    top_industry_records = df.groupby('industry')['records_exposed'].sum().max()
    
    # Most common breach type
    top_breach_type = df['breach_type'].mode().iloc[0]
    breach_type_pct = (df['breach_type'] == top_breach_type).mean() * 100
    
    # Create summary content
    summary_content = f"""# Data Breach Insights Report - Executive Summary

## 📊 Key Metrics
- **Total Breaches Analyzed**: {total_breaches:,}
- **Total Records Exposed**: {total_records:,}
- **Average Breach Size**: {avg_breach_size:,.0f} records
- **Largest Single Breach**: {largest_breach:,} records
- **Year-over-Year Change**: {yoy_change:+.1f}%

## 🔍 Key Findings

### 1. Industry Concentration
The **{top_industry}** sector accounts for the highest number of exposed records ({top_industry_records:,}), representing {top_industry_records/total_records*100:.1f}% of all compromised data.

### 2. Attack Vector Analysis
**{top_breach_type}** attacks represent {breach_type_pct:.1f}% of all incidents, indicating a significant security vulnerability that requires immediate attention.

### 3. Temporal Trends
Breach frequency has {'increased' if yoy_change > 0 else 'decreased'} by {abs(yoy_change):.1f}% compared to the previous year, suggesting {'growing' if yoy_change > 0 else 'declining'} cybersecurity threats.

## 🎯 Recommendations

### Immediate Actions
1. **Strengthen Insider Threat Detection**: Implement advanced monitoring and access controls
2. **Enhance Industry-Specific Security**: Develop sector-specific security frameworks
3. **Improve Incident Response**: Reduce time-to-detection and containment

### Strategic Initiatives
1. **Zero Trust Architecture**: Implement comprehensive identity and access management
2. **Security Awareness Training**: Regular training for all employees
3. **Threat Intelligence Integration**: Proactive threat hunting and intelligence sharing

## 📈 Business Impact
- **Financial Risk**: Average breach cost estimated at $4.45M (IBM 2023 Cost of Data Breach Report)
- **Regulatory Compliance**: Ensure adherence to GDPR, CCPA, and industry regulations
- **Reputation Management**: Proactive communication and transparency strategies

## 🔒 Next Steps
1. Review current security posture against industry benchmarks
2. Implement recommended security controls and monitoring
3. Establish regular breach simulation and testing programs
4. Develop comprehensive incident response playbooks

---
*Report generated on {datetime.now().strftime('%B %d, %Y')}*
*Data source: {len(df)} breach incidents from 2020-2024*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Created executive summary: {output_file}")

def main():
    """Main function to prepare Power BI data."""
    parser = argparse.ArgumentParser(description="Prepare data for Power BI dashboard")
    parser.add_argument("--csv", default="data/sample_breaches.csv", help="Input CSV file")
    parser.add_argument("--output", default="powerbi", help="Output directory")
    parser.add_argument("--executive", default="docs/executive_report.md", help="Executive summary file")
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.csv):
        print(f"❌ CSV file not found: {args.csv}")
        return 1
    
    # Load and enhance data
    df = load_and_enhance_data(args.csv)
    
    # Create Power BI files
    create_powerbi_files(df, args.output)
    
    # Generate executive summary
    os.makedirs(os.path.dirname(args.executive), exist_ok=True)
    generate_executive_summary(df, args.executive)
    
    print(f"\n🎉 Power BI data preparation completed!")
    print(f"📁 Files created in: {args.output}/")
    print(f"📄 Executive summary: {args.executive}")
    print(f"💡 See {args.output}/CONNECTION_INSTRUCTIONS.md for setup steps")
    
    return 0

if __name__ == "__main__":
    exit(main())
