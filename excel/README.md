# Excel Workbook Instructions

## 📊 breach_analysis.xlsx

This Excel workbook demonstrates professional data analyst skills including pivot tables, charts, and advanced formulas.

### 📋 Workbook Structure

#### 1. **RAW Tab** 📥

- **Purpose**: Raw data import from CSV
- **Content**: Direct import of `data/sample_breaches.csv`
- **Formatting**:
  - Headers in row 1
  - Data starts from row 2
  - No formulas or calculations
  - Preserve original data integrity

#### 2. **CLEAN Tab** 🧹

- **Purpose**: Cleaned and enhanced data for analysis
- **Content**:
  - All data from RAW tab
  - Additional calculated columns:
    - `Year` = `=YEAR([@breach_date])`
    - `Month` = `=MONTH([@breach_date])`
    - `Quarter` = `=ROUNDUP(MONTH([@breach_date])/3,0)`
    - `Is_Large_Breach` = `=IF([@records_exposed]>=1000000,"Yes","No")`
    - `Severity_Level` = `=IFS([@records_exposed]<=1000,"Low",[@records_exposed]<=10000,"Medium",[@records_exposed]<=100000,"High",[@records_exposed]<=1000000,"Critical",TRUE,"Catastrophic")`
    - `Standard_Industry` = `=XLOOKUP([@industry],industry_map[raw],industry_map[standard])`

#### 3. **industry_map Tab** 🗺️

- **Purpose**: Lookup table for industry standardization
- **Columns**:
  - `raw`: Original industry names
  - `standard`: Standardized industry names
  - `category`: Industry category
  - `risk_level`: Risk assessment

#### 4. **PIVOT_BreachesByYear Tab** 📈

- **Purpose**: Time series analysis of breaches
- **Pivot Table**:
  - **Rows**: Year
  - **Values**: Count of breaches, Sum of records_exposed
  - **Filters**: Industry, Country, Breach Type
- **Charts**: Line chart showing breach trends over time

#### 5. **PIVOT_IndustryRecords Tab** 🏭

- **Purpose**: Industry analysis by records exposed
- **Pivot Table**:
  - **Rows**: Industry
  - **Values**: Sum of records_exposed, Count of breaches
  - **Sort**: Descending by total records
- **Charts**: Stacked bar chart by industry

#### 6. **PIVOT_Geography Tab** 🌍

- **Purpose**: Geographic distribution analysis
- **Pivot Table**:
  - **Rows**: Country
  - **Values**: Count of breaches, Sum of records_exposed
  - **Filters**: Industry, Year
- **Charts**: Map chart (if available) or column chart

#### 7. **CHARTS Tab** 📊

- **Purpose**: Centralized chart collection
- **Charts**:
  - Line chart: Breaches by year
  - Stacked bar: Records by industry
  - Pie chart: Breach type distribution
  - Scatter plot: Breach size vs frequency

#### 8. **Executive_Summary Tab** 👔

- **Purpose**: One-page executive summary
- **Content**:
  - Key metrics (KPI cards)
  - Top 3 insights
  - Trend analysis
  - Recommendations
  - Single embedded chart

### 🔧 Excel Skills Demonstrated

#### 1. **Pivot Tables** 📊

```excel
# Create pivot table from CLEAN data
Insert > PivotTable > Use CLEAN data
- Rows: Industry
- Values: Sum of records_exposed, Count of breaches
- Filters: Year, Country, Breach Type
```

#### 2. **XLOOKUP Formula** 🔍

```excel
# Industry standardization
=XLOOKUP([@industry],industry_map[raw],industry_map[standard])
```

#### 3. **Conditional Formatting** 🎨

```excel
# Highlight top 10% breach sizes
Select records_exposed column > Conditional Formatting > Top/Bottom Rules > Top 10%
```

#### 4. **Slicers** 🔍

```excel
# Add slicers to pivot tables
PivotTable Tools > Insert Slicer > Select: Industry, Country, Year
```

#### 5. **Advanced Formulas** 🧮

```excel
# Severity classification
=IFS([@records_exposed]<=1000,"Low",
     [@records_exposed]<=10000,"Medium",
     [@records_exposed]<=100000,"High",
     [@records_exposed]<=1000000,"Critical",
     TRUE,"Catastrophic")

# Year-over-year change
=IFERROR(([@current_year]-[@previous_year])/[@previous_year],"N/A")
```

### 📋 Step-by-Step Creation Instructions

#### Step 1: Import Raw Data

1. Open Excel
2. Data > Get Data > From Text/CSV
3. Select `data/sample_breaches.csv`
4. Import to new sheet named "RAW"

#### Step 2: Create Clean Data

1. Copy RAW data to new sheet "CLEAN"
2. Add calculated columns using formulas above
3. Format as Excel Table (Ctrl+T)
4. Name table "breach_data"

#### Step 3: Create Industry Lookup

1. New sheet "industry_map"
2. Add lookup table with columns: raw, standard, category, risk_level
3. Format as Excel Table named "industry_map"

#### Step 4: Create Pivot Tables

1. Insert > PivotTable from CLEAN data
2. Create separate sheets for each pivot table
3. Add appropriate rows, values, and filters
4. Format pivot tables professionally

#### Step 5: Add Charts

1. Select pivot table data
2. Insert > Recommended Charts
3. Choose appropriate chart types
4. Format charts with consistent theme

#### Step 6: Create Slicers

1. Select pivot table
2. PivotTable Tools > Insert Slicer
3. Choose relevant fields
4. Format slicers consistently

#### Step 7: Executive Summary

1. New sheet "Executive_Summary"
2. Add KPI cards with key metrics
3. Insert single chart showing main trend
4. Add text boxes with insights
5. Format for single-page printing

### 🎨 Design Theme

- **Primary Color**: #0b2948 (Dark Blue)
- **Accent Color**: #1fb6b6 (Teal)
- **Highlight Color**: #ffb86b (Orange)
- **Font**: Calibri, 11pt
- **Headers**: Bold, 12pt

### 📊 Key Metrics to Highlight

1. **Total Breaches**: Count of all incidents
2. **Total Records Exposed**: Sum of all records
3. **Average Breach Size**: Mean records per breach
4. **Year-over-Year Change**: Percentage change
5. **Top Industry**: Industry with most records
6. **Largest Breach**: Single largest incident

### 🔄 Data Refresh Instructions

1. **Update Raw Data**:

   - Replace RAW tab with new CSV data
   - CLEAN tab will auto-update formulas

2. **Refresh Pivot Tables**:

   - Right-click pivot table > Refresh
   - Or Data > Refresh All

3. **Update Charts**:
   - Charts will auto-update with pivot table changes

### 📱 Mobile/Print Optimization

- **Print Setup**: Portrait, Fit to 1 page
- **Executive Summary**: Optimized for single-page printing
- **Charts**: High contrast for print visibility
- **Fonts**: Minimum 10pt for readability

### 🎯 Recruiter Demo Points

1. **Pivot Table Mastery**: Show filtering and grouping
2. **Formula Expertise**: Demonstrate XLOOKUP and IFS
3. **Data Visualization**: Explain chart choices
4. **Business Intelligence**: Connect data to insights
5. **Professional Formatting**: Clean, consistent design

---

**Note**: This workbook demonstrates professional Excel skills that recruiters look for in data analyst positions. The combination of technical skills (pivot tables, formulas) and business acumen (executive summary, insights) showcases both analytical and communication abilities.
