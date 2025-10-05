#!/usr/bin/env python3
"""
Generate synthetic data breach dataset for demonstration purposes.

This script creates a realistic sample dataset with 500 breach records
that can be used for Excel, Power BI, and SQL analysis.
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import argparse
import os

# Data configuration
INDUSTRIES = [
    "Healthcare", "Financial", "Technology", "Retail", "Government",
    "Education", "Energy", "Manufacturing", "Transportation", "Media"
]

BREACH_TYPES = [
    "Hacking", "Insider", "Physical", "Social Engineering", 
    "System Error", "Unknown"
]

COUNTRIES = [
    "US", "GB", "CA", "AU", "DE", "FR", "JP", "IN", "BR", "CN",
    "IT", "ES", "NL", "SE", "NO", "DK", "FI", "CH", "AT", "BE"
]

# Industry-specific breach patterns
INDUSTRY_PATTERNS = {
    "Healthcare": {
        "common_types": ["Hacking", "Insider", "System Error"],
        "avg_records": 50000,
        "max_records": 10000000,
        "org_prefixes": ["Health", "Medical", "Care", "Hospital", "Clinic"]
    },
    "Financial": {
        "common_types": ["Hacking", "Insider", "Social Engineering"],
        "avg_records": 100000,
        "max_records": 50000000,
        "org_prefixes": ["Bank", "Credit", "Finance", "Capital", "Trust"]
    },
    "Technology": {
        "common_types": ["Hacking", "System Error", "Insider"],
        "avg_records": 200000,
        "max_records": 100000000,
        "org_prefixes": ["Tech", "Cloud", "Data", "Software", "Systems"]
    },
    "Retail": {
        "common_types": ["Hacking", "Physical", "System Error"],
        "avg_records": 75000,
        "max_records": 20000000,
        "org_prefixes": ["Retail", "Store", "Market", "Shop", "Commerce"]
    },
    "Government": {
        "common_types": ["Hacking", "Insider", "Physical"],
        "avg_records": 150000,
        "max_records": 50000000,
        "org_prefixes": ["Gov", "Federal", "State", "Agency", "Department"]
    }
}

def generate_org_name(industry: str) -> str:
    """Generate realistic organization name based on industry."""
    patterns = INDUSTRY_PATTERNS.get(industry, INDUSTRY_PATTERNS["Technology"])
    prefix = random.choice(patterns["org_prefixes"])
    
    suffixes = ["Corp", "Inc", "LLC", "Ltd", "Group", "Systems", "Solutions", "Services"]
    suffix = random.choice(suffixes)
    
    # Add some variety
    if random.random() < 0.3:
        numbers = ["1", "2", "3", "International", "Global", "National"]
        middle = random.choice(numbers)
        return f"{prefix} {middle} {suffix}"
    else:
        return f"{prefix} {suffix}"

def generate_breach_date() -> str:
    """Generate random breach date between 2020-2024."""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Weight towards more recent dates using exponential distribution
    days_diff = (end_date - start_date).days
    # Use exponential distribution to bias towards recent dates
    random_factor = random.expovariate(1.0)  # Exponential distribution
    random_days = int(min(random_factor * days_diff / 3, days_diff))
    
    breach_date = start_date + timedelta(days=random_days)
    return breach_date.strftime("%Y-%m-%d")

def generate_records_exposed(industry: str) -> int:
    """Generate realistic number of records exposed based on industry."""
    patterns = INDUSTRY_PATTERNS.get(industry, INDUSTRY_PATTERNS["Technology"])
    avg = patterns["avg_records"]
    max_records = patterns["max_records"]
    
    # Use log-normal distribution for realistic breach sizes
    import math
    mu = math.log(avg)
    sigma = 1.0
    
    records = int(random.lognormvariate(mu, sigma))
    return min(records, max_records)

def generate_breach_type(industry: str) -> str:
    """Generate breach type based on industry patterns."""
    patterns = INDUSTRY_PATTERNS.get(industry, INDUSTRY_PATTERNS["Technology"])
    common_types = patterns["common_types"]
    
    # 70% chance of common type for industry, 30% random
    if random.random() < 0.7:
        return random.choice(common_types)
    else:
        return random.choice(BREACH_TYPES)

def generate_source_url(breach_id: int) -> str:
    """Generate realistic source URL."""
    domains = [
        "krebsonsecurity.com", "bleepingcomputer.com", "threatpost.com",
        "securityweek.com", "darkreading.com", "infosecurity-magazine.com",
        "cyberscoop.com", "therecord.media", "cybernews.com"
    ]
    
    domain = random.choice(domains)
    return f"https://{domain}/breach-{breach_id:04d}"

def generate_breach_record(breach_id: int) -> Dict[str, Any]:
    """Generate a single breach record."""
    industry = random.choice(INDUSTRIES)
    country = random.choice(COUNTRIES)
    
    return {
        "id": breach_id,
        "breach_date": generate_breach_date(),
        "name": generate_org_name(industry),
        "industry": industry,
        "country": country,
        "records_exposed": generate_records_exposed(industry),
        "breach_type": generate_breach_type(industry),
        "source_url": generate_source_url(breach_id)
    }

def main():
    """Generate sample CSV file."""
    parser = argparse.ArgumentParser(description="Generate sample breach data")
    parser.add_argument("--output", "-o", default="data/sample_breaches.csv",
                       help="Output CSV file path")
    parser.add_argument("--count", "-c", type=int, default=500,
                       help="Number of records to generate")
    parser.add_argument("--seed", "-s", type=int, default=42,
                       help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(args.seed)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Generate records
    records = []
    for i in range(1, args.count + 1):
        records.append(generate_breach_record(i))
    
    # Write CSV file
    fieldnames = ["id", "breach_date", "name", "industry", "country", 
                  "records_exposed", "breach_type", "source_url"]
    
    with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"Generated {args.count} breach records in {args.output}")
    
    # Print summary statistics
    total_records = sum(r["records_exposed"] for r in records)
    avg_records = total_records / len(records)
    
    print(f"\nSummary Statistics:")
    print(f"Total records exposed: {total_records:,}")
    print(f"Average breach size: {avg_records:,.0f}")
    print(f"Date range: {min(r['breach_date'] for r in records)} to {max(r['breach_date'] for r in records)}")
    
    # Industry breakdown
    industry_counts = {}
    for record in records:
        industry = record["industry"]
        industry_counts[industry] = industry_counts.get(industry, 0) + 1
    
    print(f"\nIndustry Distribution:")
    for industry, count in sorted(industry_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {industry}: {count} breaches")

if __name__ == "__main__":
    main()
