# Power BI Data Connection Instructions

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
