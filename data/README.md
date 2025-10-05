# Data Sources and Schema

This directory contains sample data and documentation for the Data Breach Insights Report project.

## 📊 Sample Dataset

**File**: `sample_breaches.csv` (500 rows)

### Schema Description

| Column            | Type    | Description                   | Example                        |
| ----------------- | ------- | ----------------------------- | ------------------------------ |
| `id`              | INTEGER | Unique identifier             | 1                              |
| `breach_date`     | DATE    | Date of breach incident       | 2023-03-15                     |
| `name`            | TEXT    | Organization name             | Acme Corp                      |
| `industry`        | TEXT    | Industry sector               | Healthcare                     |
| `country`         | TEXT    | Country code (ISO 3166-1)     | US                             |
| `records_exposed` | BIGINT  | Number of records compromised | 1500000                        |
| `breach_type`     | TEXT    | Type of breach                | Hacking                        |
| `source_url`      | TEXT    | Reference URL                 | https://example.com/breach-123 |

### Data Quality Notes

- **Date Format**: Standardized to YYYY-MM-DD
- **Industry**: Standardized using mapping table (see `mappings/industry_lookup.csv`)
- **Country**: ISO 3166-1 alpha-2 codes
- **Records Exposed**: Numeric values, no nulls
- **Breach Types**: Categorized (Hacking, Insider, Physical, etc.)

## 🔗 Public Data Sources

### Primary Sources

1. **Kaggle Data Breaches Dataset**

   - **URL**: https://www.kaggle.com/datasets/arindam235/cyber-security-breaches-data
   - **Description**: Comprehensive dataset of cybersecurity breaches from 2004-2023
   - **Size**: ~10,000 records
   - **License**: CC0 1.0 Universal
   - **Citation**: "Cyber Security Breaches Data" by Arindam, Kaggle, 2023

2. **Privacy Rights Clearinghouse Data Breach Chronology**

   - **URL**: https://privacyrights.org/data-breaches
   - **Description**: Chronological database of data breaches since 2005
   - **Size**: ~9,000 records
   - **License**: Public domain
   - **Citation**: Privacy Rights Clearinghouse, "Data Breach Chronology", 2023

3. **Have I Been Pwned API** (Optional Enrichment)
   - **URL**: https://haveibeenpwned.com/API/v3
   - **Description**: Real-time breach data and email verification
   - **Rate Limits**: 1 request per 1.5 seconds (free tier)
   - **API Key**: Required for bulk queries
   - **Citation**: Troy Hunt, "Have I Been Pwned", 2023

### Data Acquisition Instructions

#### Download Full Datasets

```bash
# Kaggle dataset (requires Kaggle API)
pip install kaggle
kaggle datasets download -d arindam235/cyber-security-breaches-data
unzip cyber-security-breaches-data.zip

# Privacy Rights Clearinghouse (manual download)
# Visit: https://privacyrights.org/data-breaches
# Download CSV export of breach chronology
```

#### Data Processing Pipeline

```python
# Run the sample data generator
python scripts/produce_sample_csv.py

# Or process real data
python scripts/process_kaggle_data.py --input kaggle_data.csv --output data/breaches.csv
```

## 📋 Data Dictionary

### Industry Categories

- **Healthcare**: Hospitals, clinics, medical records
- **Financial**: Banks, credit unions, payment processors
- **Technology**: Software companies, cloud providers
- **Retail**: E-commerce, brick-and-mortar stores
- **Government**: Federal, state, local agencies
- **Education**: Universities, schools, research institutions
- **Other**: Miscellaneous sectors

### Breach Types

- **Hacking**: External cyber attacks
- **Insider**: Internal malicious or accidental
- **Physical**: Theft of physical devices/documents
- **Social Engineering**: Phishing, pretexting
- **System Error**: Accidental exposure
- **Unknown**: Unspecified cause

### Country Codes

Using ISO 3166-1 alpha-2 standard:

- **US**: United States
- **GB**: United Kingdom
- **CA**: Canada
- **AU**: Australia
- **DE**: Germany
- **FR**: France
- **JP**: Japan
- **IN**: India
- **BR**: Brazil
- **CN**: China

## ⚠️ Legal and Ethical Usage

### Privacy Considerations

- **No PII**: Sample data contains no personally identifiable information
- **Synthetic Data**: Generated data for demonstration purposes
- **Public Sources**: Only publicly available breach information
- **Anonymized**: Organization names are fictional

### Usage Guidelines

- ✅ Educational and demonstration purposes
- ✅ Portfolio and resume projects
- ✅ Research and analysis
- ❌ Commercial use without permission
- ❌ Re-identification attempts
- ❌ Malicious or harmful purposes

### Data Retention

- Sample data: Permanent (synthetic)
- Real data: Follow source licensing terms
- Personal data: Not collected or stored

## 🔄 Data Updates

### Sample Data

- **Frequency**: Static (generated once)
- **Version**: 1.0
- **Last Updated**: 2024-01-15

### Real Data

- **Kaggle**: Updated monthly
- **PRC**: Updated weekly
- **HIBP**: Real-time API

## 📞 Support

For questions about data sources or usage:

- Check the main README.md
- Review the case study in docs/case_study.md
- Open an issue in the repository

---

**Note**: This dataset is designed for educational and demonstration purposes. Always verify data accuracy and follow ethical guidelines when working with real breach data.
