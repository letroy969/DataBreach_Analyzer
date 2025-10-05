-- Data Breach Insights Report - Analytical Queries (SQLite Compatible)
-- Core queries for Excel, Power BI, and Jupyter notebook analysis

-- ==============================================
-- 1. TIME SERIES ANALYSIS
-- ==============================================

-- Breaches per year (for trend analysis)
SELECT 
    strftime('%Y', breach_date) AS year,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records_per_breach
FROM breaches
GROUP BY strftime('%Y', breach_date)
ORDER BY year;

-- Monthly breach trends (last 2 years)
SELECT 
    strftime('%Y', breach_date) AS year,
    strftime('%m', breach_date) AS month,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records
FROM breaches
WHERE breach_date >= date('now', '-2 years')
GROUP BY strftime('%Y', breach_date), strftime('%m', breach_date)
ORDER BY year, month;

-- Quarterly analysis
SELECT 
    strftime('%Y', breach_date) AS year,
    CASE 
        WHEN strftime('%m', breach_date) IN ('01','02','03') THEN 'Q1'
        WHEN strftime('%m', breach_date) IN ('04','05','06') THEN 'Q2'
        WHEN strftime('%m', breach_date) IN ('07','08','09') THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records
FROM breaches
GROUP BY strftime('%Y', breach_date), quarter
ORDER BY year, quarter;

-- ==============================================
-- 2. INDUSTRY ANALYSIS
-- ==============================================

-- Top 10 industries by total records exposed
SELECT 
    industry,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records,
    MAX(records_exposed) AS max_records,
    MIN(breach_date) AS first_breach,
    MAX(breach_date) AS latest_breach
FROM breaches
GROUP BY industry
ORDER BY total_records DESC
LIMIT 10;

-- Average breach size per industry
SELECT 
    industry,
    COUNT(*) AS breach_count,
    ROUND(AVG(records_exposed), 0) AS avg_breach_size,
    ROUND((SELECT AVG(records_exposed) FROM breaches b2 WHERE b2.industry = breaches.industry), 0) AS median_breach_size
FROM breaches
GROUP BY industry
ORDER BY avg_breach_size DESC;

-- Industry breach frequency (breaches per year)
SELECT 
    industry,
    COUNT(*) AS total_breaches,
    COUNT(DISTINCT strftime('%Y', breach_date)) AS years_active,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT strftime('%Y', breach_date)), 2) AS avg_breaches_per_year
FROM breaches
GROUP BY industry
ORDER BY avg_breaches_per_year DESC;

-- ==============================================
-- 3. GEOGRAPHIC ANALYSIS
-- ==============================================

-- Top countries by breach count and records
SELECT 
    country,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records,
    ROUND(SUM(records_exposed) * 100.0 / (SELECT SUM(records_exposed) FROM breaches), 2) AS percentage_of_total
FROM breaches
GROUP BY country
ORDER BY total_records DESC
LIMIT 15;

-- Breach distribution by region (using country lookup)
SELECT 
    cl.region,
    COUNT(b.id) AS breach_count,
    SUM(b.records_exposed) AS total_records,
    AVG(b.records_exposed) AS avg_records
FROM breaches b
JOIN country_lookup cl ON b.country = cl.country_code
GROUP BY cl.region
ORDER BY total_records DESC;

-- ==============================================
-- 4. BREACH TYPE ANALYSIS
-- ==============================================

-- Breach types by frequency and impact
SELECT 
    breach_type,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM breaches), 2) AS percentage_of_breaches
FROM breaches
GROUP BY breach_type
ORDER BY total_records DESC;

-- Breach type effectiveness by industry
SELECT 
    industry,
    breach_type,
    COUNT(*) AS breach_count,
    AVG(records_exposed) AS avg_records
FROM breaches
GROUP BY industry, breach_type
HAVING COUNT(*) >= 3  -- Only show combinations with 3+ breaches
ORDER BY industry, avg_records DESC;

-- ==============================================
-- 5. SEVERITY ANALYSIS
-- ==============================================

-- Breach severity distribution
SELECT 
    bs.severity_level,
    bs.description,
    COUNT(b.id) AS breach_count,
    SUM(b.records_exposed) AS total_records
FROM breaches b
JOIN breach_severity bs ON b.records_exposed >= bs.records_min 
    AND b.records_exposed <= bs.records_max
GROUP BY bs.severity_level, bs.description
ORDER BY bs.records_min;

-- Large breaches (>1M records) analysis
SELECT 
    name,
    industry,
    country,
    breach_date,
    records_exposed,
    breach_type,
    source_url
FROM breaches
WHERE records_exposed >= 1000000
ORDER BY records_exposed DESC;

-- ==============================================
-- 6. COMPARATIVE ANALYSIS
-- ==============================================

-- Year-over-year change in breach counts
WITH yearly_breaches AS (
    SELECT 
        strftime('%Y', breach_date) AS year,
        COUNT(*) AS breach_count,
        SUM(records_exposed) AS total_records
    FROM breaches
    GROUP BY strftime('%Y', breach_date)
)
SELECT 
    year,
    breach_count,
    total_records,
    LAG(breach_count) OVER (ORDER BY year) AS prev_year_breaches,
    LAG(total_records) OVER (ORDER BY year) AS prev_year_records,
    ROUND((breach_count - LAG(breach_count) OVER (ORDER BY year)) * 100.0 / 
          LAG(breach_count) OVER (ORDER BY year), 2) AS yoy_breach_change_pct,
    ROUND((total_records - LAG(total_records) OVER (ORDER BY year)) * 100.0 / 
          LAG(total_records) OVER (ORDER BY year), 2) AS yoy_records_change_pct
FROM yearly_breaches
ORDER BY year;

-- Industry performance vs average
WITH industry_stats AS (
    SELECT 
        industry,
        COUNT(*) AS breach_count,
        AVG(records_exposed) AS avg_records,
        (SELECT AVG(records_exposed) FROM breaches) AS overall_avg
    FROM breaches
    GROUP BY industry
)
SELECT 
    industry,
    breach_count,
    ROUND(avg_records, 0) AS avg_records,
    ROUND(overall_avg, 0) AS overall_avg,
    ROUND((avg_records - overall_avg) * 100.0 / overall_avg, 2) AS vs_overall_pct
FROM industry_stats
ORDER BY avg_records DESC;

-- ==============================================
-- 7. DETAILED EXPLORATION QUERIES
-- ==============================================

-- Top 20 largest breaches with full details
SELECT 
    name,
    industry,
    country,
    breach_date,
    records_exposed,
    breach_type,
    source_url,
    ROUND(records_exposed * 100.0 / (SELECT SUM(records_exposed) FROM breaches), 4) AS percentage_of_total
FROM breaches
ORDER BY records_exposed DESC
LIMIT 20;

-- Recent breaches (last 6 months)
SELECT 
    name,
    industry,
    country,
    breach_date,
    records_exposed,
    breach_type,
    source_url
FROM breaches
WHERE breach_date >= date('now', '-6 months')
ORDER BY breach_date DESC;

-- Breach patterns by day of week
SELECT 
    CASE 
        WHEN strftime('%w', breach_date) = '0' THEN 'Sunday'
        WHEN strftime('%w', breach_date) = '1' THEN 'Monday'
        WHEN strftime('%w', breach_date) = '2' THEN 'Tuesday'
        WHEN strftime('%w', breach_date) = '3' THEN 'Wednesday'
        WHEN strftime('%w', breach_date) = '4' THEN 'Thursday'
        WHEN strftime('%w', breach_date) = '5' THEN 'Friday'
        ELSE 'Saturday'
    END AS day_of_week,
    COUNT(*) AS breach_count,
    AVG(records_exposed) AS avg_records
FROM breaches
GROUP BY strftime('%w', breach_date)
ORDER BY breach_count DESC;

-- ==============================================
-- 8. SUMMARY STATISTICS
-- ==============================================

-- Overall dataset summary
SELECT 
    COUNT(*) AS total_breaches,
    SUM(records_exposed) AS total_records_exposed,
    AVG(records_exposed) AS avg_records_per_breach,
    MIN(records_exposed) AS min_records,
    MAX(records_exposed) AS max_records,
    MIN(breach_date) AS earliest_breach,
    MAX(breach_date) AS latest_breach,
    COUNT(DISTINCT industry) AS unique_industries,
    COUNT(DISTINCT country) AS unique_countries,
    COUNT(DISTINCT breach_type) AS unique_breach_types
FROM breaches;