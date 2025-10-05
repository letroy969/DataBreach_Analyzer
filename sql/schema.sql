-- Data Breach Insights Report - Database Schema
-- SQLite compatible schema for breach analysis

-- Main breaches table
CREATE TABLE IF NOT EXISTS breaches (
    id INTEGER PRIMARY KEY,
    breach_date DATE NOT NULL,
    name TEXT NOT NULL,
    industry TEXT NOT NULL,
    country TEXT NOT NULL,
    records_exposed BIGINT NOT NULL,
    breach_type TEXT NOT NULL,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Industry lookup table for standardization
CREATE TABLE IF NOT EXISTS industry_lookup (
    raw_industry TEXT PRIMARY KEY,
    standard_industry TEXT NOT NULL,
    category TEXT,
    risk_level TEXT
);

-- Country lookup table for additional metadata
CREATE TABLE IF NOT EXISTS country_lookup (
    country_code TEXT PRIMARY KEY,
    country_name TEXT NOT NULL,
    region TEXT,
    gdp_per_capita REAL,
    population BIGINT
);

-- Breach severity classification
CREATE TABLE IF NOT EXISTS breach_severity (
    id INTEGER PRIMARY KEY,
    records_min BIGINT,
    records_max BIGINT,
    severity_level TEXT NOT NULL,
    description TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_breaches_date ON breaches(breach_date);
CREATE INDEX IF NOT EXISTS idx_breaches_industry ON breaches(industry);
CREATE INDEX IF NOT EXISTS idx_breaches_country ON breaches(country);
CREATE INDEX IF NOT EXISTS idx_breaches_type ON breaches(breach_type);
CREATE INDEX IF NOT EXISTS idx_breaches_records ON breaches(records_exposed);

-- Views for common queries (SQLite compatible)
CREATE VIEW IF NOT EXISTS v_breaches_by_year AS
SELECT 
    strftime('%Y', breach_date) AS year,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records,
    MIN(records_exposed) AS min_records,
    MAX(records_exposed) AS max_records
FROM breaches
GROUP BY strftime('%Y', breach_date)
ORDER BY year;

CREATE VIEW IF NOT EXISTS v_industry_summary AS
SELECT 
    industry,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records,
    MIN(breach_date) AS first_breach,
    MAX(breach_date) AS latest_breach
FROM breaches
GROUP BY industry
ORDER BY total_records DESC;

CREATE VIEW IF NOT EXISTS v_country_summary AS
SELECT 
    country,
    COUNT(*) AS breach_count,
    SUM(records_exposed) AS total_records,
    AVG(records_exposed) AS avg_records
FROM breaches
GROUP BY country
ORDER BY total_records DESC;

-- Insert industry lookup data
INSERT OR REPLACE INTO industry_lookup (raw_industry, standard_industry, category, risk_level) VALUES
('Healthcare', 'Healthcare', 'Critical Infrastructure', 'High'),
('Financial', 'Financial', 'Critical Infrastructure', 'High'),
('Technology', 'Technology', 'Information Technology', 'Medium'),
('Retail', 'Retail', 'Consumer Services', 'Medium'),
('Government', 'Government', 'Public Sector', 'High'),
('Education', 'Education', 'Public Sector', 'Medium'),
('Energy', 'Energy', 'Critical Infrastructure', 'High'),
('Manufacturing', 'Manufacturing', 'Industrial', 'Medium'),
('Transportation', 'Transportation', 'Critical Infrastructure', 'High'),
('Media', 'Media', 'Consumer Services', 'Low');

-- Insert country lookup data
INSERT OR REPLACE INTO country_lookup (country_code, country_name, region, gdp_per_capita, population) VALUES
('US', 'United States', 'North America', 65000, 331000000),
('GB', 'United Kingdom', 'Europe', 45000, 67000000),
('CA', 'Canada', 'North America', 50000, 38000000),
('AU', 'Australia', 'Oceania', 55000, 26000000),
('DE', 'Germany', 'Europe', 50000, 83000000),
('FR', 'France', 'Europe', 45000, 67000000),
('JP', 'Japan', 'Asia', 40000, 125000000),
('IN', 'India', 'Asia', 2000, 1380000000),
('BR', 'Brazil', 'South America', 8000, 213000000),
('CN', 'China', 'Asia', 10000, 1400000000),
('IT', 'Italy', 'Europe', 35000, 60000000),
('ES', 'Spain', 'Europe', 30000, 47000000),
('NL', 'Netherlands', 'Europe', 55000, 17000000),
('SE', 'Sweden', 'Europe', 55000, 10000000),
('NO', 'Norway', 'Europe', 75000, 5000000),
('DK', 'Denmark', 'Europe', 60000, 6000000),
('FI', 'Finland', 'Europe', 50000, 5500000),
('CH', 'Switzerland', 'Europe', 80000, 8000000),
('AT', 'Austria', 'Europe', 50000, 9000000),
('BE', 'Belgium', 'Europe', 45000, 11000000);

-- Insert breach severity levels
INSERT OR REPLACE INTO breach_severity (id, records_min, records_max, severity_level, description) VALUES
(1, 0, 1000, 'Low', 'Small breach with minimal impact'),
(2, 1001, 10000, 'Medium', 'Moderate breach requiring attention'),
(3, 10001, 100000, 'High', 'Large breach with significant impact'),
(4, 100001, 1000000, 'Critical', 'Major breach with severe consequences'),
(5, 1000001, 999999999999, 'Catastrophic', 'Massive breach with devastating impact');