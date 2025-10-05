# Power BI Dashboard - Data Breach Insights Report

## 📊 breach_insights.pbix

This Power BI dashboard demonstrates professional BI skills including data modeling, DAX measures, and interactive visualizations.

### 🎯 Dashboard Overview

The dashboard consists of 4 main pages plus an executive summary, designed to provide comprehensive insights into data breach patterns and trends.

### 📋 Dashboard Pages

#### 1. **Overview Page** 🏠

**Purpose**: Landing page with key metrics and trends

**Visuals**:

- **KPI Cards** (Top row):

  - Total Breaches: `[TotalBreaches]`
  - Total Records Exposed: `[TotalRecords]`
  - Average Breach Size: `[AvgBreachSize]`
  - Breaches This Year: `[BreachesThisYear]`

- **Line Chart**: Breaches by Year

  - X-axis: Year
  - Y-axis: Count of Breaches
  - Legend: Breach Type

- **Stacked Bar Chart**: Top 10 Industries by Records

  - X-axis: Industry
  - Y-axis: Sum of Records Exposed
  - Color: Breach Type

- **Table**: Recent Large Breaches (>1M records)
  - Columns: Name, Industry, Country, Date, Records, Type

**Filters**:

- Date Range Slicer
- Industry Slicer
- Country Slicer
- Breach Type Slicer

#### 2. **Geography Page** 🌍

**Purpose**: Geographic analysis and mapping

**Visuals**:

- **Map Visual**: Breach Distribution by Country

  - Location: Country
  - Size: Sum of Records Exposed
  - Color: Count of Breaches

- **Bar Chart**: Top 15 Countries by Breaches

  - X-axis: Country
  - Y-axis: Count of Breaches

- **Donut Chart**: Regional Distribution

  - Category: Region (derived from country)
  - Values: Sum of Records Exposed

- **Table**: Country Details
  - Columns: Country, Region, Breach Count, Total Records, Avg Size

**Filters**:

- Region Slicer
- Year Slicer
- Industry Slicer

#### 3. **Industry Page** 🏭

**Purpose**: Industry-specific analysis and trends

**Visuals**:

- **Clustered Bar Chart**: Breaches by Industry and Type

  - X-axis: Industry
  - Y-axis: Count of Breaches
  - Legend: Breach Type

- **Line Chart**: Industry Trends Over Time

  - X-axis: Year
  - Y-axis: Count of Breaches
  - Legend: Industry

- **Scatter Plot**: Breach Size vs Frequency

  - X-axis: Count of Breaches
  - Y-axis: Average Records Exposed
  - Size: Total Records Exposed
  - Color: Industry

- **Table**: Industry Performance Metrics
  - Columns: Industry, Breach Count, Total Records, Avg Size, Risk Level

**Filters**:

- Industry Slicer
- Breach Type Slicer
- Year Range Slicer

#### 4. **Incident Explorer Page** 🔍

**Purpose**: Detailed incident analysis and exploration

**Visuals**:

- **Data Table**: All Breaches with Search

  - Columns: Name, Industry, Country, Date, Records, Type, Source URL
  - Search functionality enabled
  - Sortable columns

- **Histogram**: Breach Size Distribution

  - X-axis: Records Exposed (binned)
  - Y-axis: Count of Breaches

- **Pie Chart**: Breach Type Distribution

  - Category: Breach Type
  - Values: Count of Breaches

- **Card**: Selected Breach Details
  - Shows details of selected breach from table

**Filters**:

- Text Search Box
- Date Range Slicer
- Industry Slicer
- Country Slicer
- Records Range Slicer

#### 5. **Executive Page** 👔

**Purpose**: PDF-ready executive summary

**Layout**:

- **Header**: Project title and date
- **KPI Section**: Key metrics in card format
- **Insights Section**: 3 key findings with supporting charts
- **Recommendations Section**: Actionable recommendations
- **Footer**: Data sources and methodology

**Visuals**:

- Key metrics cards
- Single trend chart (breaches by year)
- Industry distribution chart
- Summary table

### 🔧 Data Model

#### Tables

1. **breaches** (Main fact table)

   - id, breach_date, name, industry, country, records_exposed, breach_type, source_url

2. **industry_lookup** (Dimension table)

   - industry, category, risk_level

3. **country_lookup** (Dimension table)

   - country_code, country_name, region, gdp_per_capita

4. **breach_severity** (Dimension table)
   - severity_level, records_min, records_max, description

#### Relationships

- breaches[industry] → industry_lookup[industry] (Many-to-One)
- breaches[country] → country_lookup[country_code] (Many-to-One)
- breaches[records_exposed] → breach_severity (Many-to-One, based on ranges)

### 📊 DAX Measures

#### Core Measures

```dax
TotalBreaches = COUNTROWS(breaches)

TotalRecords = SUM(breaches[records_exposed])

AvgBreachSize = AVERAGE(breaches[records_exposed])

BreachesThisYear =
CALCULATE(
    [TotalBreaches],
    YEAR(breaches[breach_date]) = YEAR(TODAY())
)

BreachesLastYear =
CALCULATE(
    [TotalBreaches],
    YEAR(breaches[breach_date]) = YEAR(TODAY()) - 1
)
```

#### Year-over-Year Measures

```dax
YoY_Breaches_Change =
DIVIDE(
    [BreachesThisYear] - [BreachesLastYear],
    [BreachesLastYear],
    0
)

YoY_Breaches_Change_Pct =
FORMAT([YoY_Breaches_Change], "0.0%")
```

#### Severity Measures

```dax
LargeBreaches =
CALCULATE(
    [TotalBreaches],
    breaches[records_exposed] >= 1000000
)

CriticalBreaches =
CALCULATE(
    [TotalBreaches],
    breaches[records_exposed] >= 100000
)
```

#### Industry Measures

```dax
TopIndustry =
TOPN(1,
    SUMMARIZE(breaches, breaches[industry], "Breaches", [TotalBreaches]),
    [Breaches], DESC
)

TopIndustryName =
SELECTCOLUMNS([TopIndustry], "Industry", breaches[industry])
```

### 🎨 Design Theme

#### Color Palette

- **Primary**: #0b2948 (Dark Blue)
- **Accent**: #1fb6b6 (Teal)
- **Highlight**: #ffb86b (Orange)
- **Success**: #28a745 (Green)
- **Warning**: #ffc107 (Yellow)
- **Danger**: #dc3545 (Red)

#### Typography

- **Headers**: Segoe UI Bold, 16-24pt
- **Body**: Segoe UI Regular, 10-12pt
- **Captions**: Segoe UI Light, 9-10pt

#### Visual Guidelines

- Consistent spacing (16px grid)
- Rounded corners (4px radius)
- Subtle shadows for depth
- High contrast for accessibility

### 🔌 Data Connection

#### CSV Connection

1. **Get Data** → **Text/CSV**
2. Select `data/sample_breaches.csv`
3. Configure data types:
   - breach_date: Date
   - records_exposed: Whole Number
   - All others: Text

#### PostgreSQL Connection (Optional)

1. **Get Data** → **Database** → **PostgreSQL database**
2. Server: `localhost`
3. Database: `breach_db`
4. Username: `breach_user`
5. Password: `breach_password`

**Note**: Requires Npgsql driver installation

### 📱 Mobile Optimization

#### Responsive Design

- Use responsive visuals where possible
- Optimize for tablet viewing
- Ensure touch-friendly interactions

#### Mobile Layout

- Stack visuals vertically
- Use larger fonts
- Simplify complex interactions

### 📄 PDF Export

#### Executive Page Export

1. Select **Executive** page
2. **File** → **Export** → **Export to PDF**
3. Settings:
   - Page size: A4
   - Orientation: Portrait
   - Quality: High
   - Include: All visuals

#### Export Location

- Save to: `docs/executive_report.pdf`
- Include in repository for sharing

### 🔄 Data Refresh

#### Automatic Refresh

- Set up scheduled refresh in Power BI Service
- Refresh frequency: Daily
- Data source: CSV file or database

#### Manual Refresh

- **Home** → **Refresh** → **Refresh all**
- Or use **Refresh** button in each visual

### 🎯 Recruiter Demo Points

#### Technical Skills

1. **Data Modeling**: Show relationships and measures
2. **DAX Expertise**: Explain complex measures
3. **Visualization Design**: Discuss chart choices
4. **Performance**: Demonstrate filtering and interactions

#### Business Skills

1. **Storytelling**: Walk through insights
2. **Executive Communication**: Show PDF export
3. **Data Interpretation**: Explain trends and patterns
4. **Actionable Insights**: Connect data to recommendations

### 🛠️ Troubleshooting

#### Common Issues

1. **Data not loading**: Check file paths and permissions
2. **Visuals not updating**: Refresh data or check filters
3. **Performance issues**: Optimize data model or reduce visuals
4. **Export problems**: Check page layout and content

#### Support Resources

- Power BI Documentation: https://docs.microsoft.com/power-bi/
- DAX Reference: https://dax.guide/
- Community Forum: https://community.powerbi.com/

---

**Note**: This dashboard demonstrates professional Power BI skills including data modeling, DAX measures, interactive visualizations, and executive reporting. The combination of technical expertise and business acumen showcases both analytical and communication abilities.
