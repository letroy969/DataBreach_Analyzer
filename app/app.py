"""
Data Breach Insights Report - Advanced Streamlit Dashboard
Professional enterprise data analytics dashboard for breach insights analysis.
Features AI insights, advanced visualizations, and comprehensive data analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Data Breach Insights Report",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Dark Theme Variables */
    :root {
        --bg-primary: #0a0a0a;
        --bg-secondary: #1a1a1a;
        --bg-tertiary: #2a2a2a;
        --bg-card: #1e1e1e;
        --bg-hover: #333333;
        --text-primary: #ffffff;
        --text-secondary: #b3b3b3;
        --text-muted: #808080;
        --accent-primary: #00d4ff;
        --accent-secondary: #7c3aed;
        --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --accent-gradient-alt: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --border: #404040;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main App Background */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Professional Header */
    .main-header {
        background: var(--accent-gradient);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .header-container {
        position: relative;
        z-index: 2;
        text-align: center;
    }
    
    .header-main {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .header-icon {
        font-size: 3rem;
        opacity: 0.9;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    
    .header-title-section h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.01em;
    }
    
    .header-title-section p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 400;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    .header-divider {
        width: 100px;
        height: 2px;
        background: rgba(255,255,255,0.3);
        margin: 0 auto 1.5rem auto;
        border-radius: 1px;
    }
    
    .header-features {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .feature-tag {
        background: rgba(255,255,255,0.15);
        padding: 0.4rem 1rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.2s ease;
    }
    
    .feature-tag:hover {
        background: rgba(255,255,255,0.25);
        transform: translateY(-1px);
    }
    
    /* AI Insights Section */
    .ai-insights {
        background: var(--bg-card);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .insight-card {
        background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
    }
    
    .insight-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .risk-indicator {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .risk-high { background: var(--error); color: white; }
    .risk-medium { background: var(--warning); color: black; }
    .risk-low { background: var(--success); color: white; }
    
    /* Chart containers */
    .chart-container {
        background: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid var(--border);
    }
</style>
""", unsafe_allow_html=True)

# Utility Functions
def format_number(num: int) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return f"{num:,}"

def create_sample_data():
    """Create comprehensive sample breach data"""
    companies = [
        'TechCorp Inc', 'HealthSys Ltd', 'FinanceFirst', 'RetailMax', 'EduTech Solutions',
        'Manufacturing Co', 'Logistics Pro', 'Energy Corp', 'Media Group', 'Consulting Firm',
        'Software House', 'Banking Group', 'Insurance Co', 'Travel Agency', 'Food Chain',
        'Government Agency', 'Research Lab', 'Legal Firm', 'Real Estate Co', 'Automotive Inc'
    ]
    
    industries = ['Technology', 'Healthcare', 'Financial', 'Retail', 'Education', 
                 'Manufacturing', 'Logistics', 'Energy', 'Media', 'Consulting',
                 'Government', 'Legal', 'Real Estate', 'Automotive', 'Research']
    
    countries = ['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'JP', 'SG', 'NL', 'SE', 'IT', 'ES', 'BR', 'IN', 'CN']
    
    breach_types = ['Hacking', 'Insider Threat', 'Physical Theft', 'Social Engineering', 
                   'System Error', 'Malware', 'Ransomware', 'Phishing', 'DDoS', 'Data Leak']
    
    attack_vectors = ['External', 'Internal', 'Partner', 'Third-party', 'Unknown']
    
    # Generate realistic data
    data = []
    for i in range(500):
        company = np.random.choice(companies)
        industry = np.random.choice(industries)
        country = np.random.choice(countries)
        breach_type = np.random.choice(breach_types)
        attack_vector = np.random.choice(attack_vectors)
        
        # Generate realistic breach dates (2020-2024)
        year = np.random.randint(2020, 2025)
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)
        
        # Industry-specific record patterns
        if industry == 'Healthcare':
            records = np.random.randint(1000, 50000)
            severity = np.random.choice(['High', 'Medium'], p=[0.7, 0.3])
        elif industry == 'Financial':
            records = np.random.randint(500, 20000)
            severity = np.random.choice(['High', 'Medium'], p=[0.8, 0.2])
        elif industry == 'Government':
            records = np.random.randint(2000, 100000)
            severity = np.random.choice(['High', 'Medium', 'Low'], p=[0.6, 0.3, 0.1])
        else:
            records = np.random.randint(100, 10000)
            severity = np.random.choice(['High', 'Medium', 'Low'], p=[0.3, 0.5, 0.2])
        
        # Calculate estimated cost based on industry and records
        base_cost = records * 200
        if industry in ['Healthcare', 'Financial', 'Government']:
            base_cost *= 1.5
        if severity == 'High':
            base_cost *= 1.3
        
        data.append({
            'id': i + 1,
            'breach_date': f"{year}-{month:02d}-{day:02d}",
            'name': company,
            'industry': industry,
            'country': country,
            'records_exposed': records,
            'breach_type': breach_type,
            'attack_vector': attack_vector,
            'severity': severity,
            'estimated_cost': base_cost,
            'year': year,
            'month': month,
            'quarter': f"Q{(month-1)//3 + 1}"
        })
    
    return pd.DataFrame(data)

@st.cache_data
def load_and_clean_data(file=None):
    """Load and clean data from file or create sample data"""
    try:
        if file is not None:
            # File upload handling
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file)
            elif file_extension == 'json':
                df = pd.read_json(file)
            elif file_extension == 'parquet':
                df = pd.read_parquet(file)
            elif file_extension == 'tsv':
                df = pd.read_csv(file, sep='\t')
            elif file_extension == 'txt':
                df = pd.read_csv(file, sep='\t')
            else:
                st.error(f"Unsupported file format: {file_extension}")
                return create_sample_data()
            
            # Standardize column names
            column_mapping = {
                'company': 'name',
                'organization': 'name',
                'entity_name': 'name',
                'date': 'breach_date',
                'breach_year': 'year',
                'records': 'records_exposed',
                'records_compromised': 'records_exposed',
                'cost': 'estimated_cost',
                'estimated_damage': 'estimated_cost',
                'type': 'breach_type',
                'breach_category': 'breach_type'
            }
            
            df.columns = [column_mapping.get(col.lower(), col) for col in df.columns]
            
            # Add missing columns if needed
            if 'id' not in df.columns:
                df['id'] = range(1, len(df) + 1)
            if 'year' not in df.columns and 'breach_date' in df.columns:
                df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
                df['year'] = df['breach_date'].dt.year
            if 'estimated_cost' not in df.columns and 'records_exposed' in df.columns:
                df['estimated_cost'] = df['records_exposed'] * 200
            
            logger.info(f"Loaded {len(df)} records from uploaded file")
            return df
            
        else:
            return create_sample_data()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.error(f"Data loading error: {str(e)}")
        return create_sample_data()

def generate_ai_insights(df: pd.DataFrame) -> Dict:
    """Generate AI-powered insights from breach data"""
    insights = {}
    
    # Risk Analysis
    total_breaches = len(df)
    total_records = df['records_exposed'].sum()
    avg_records = df['records_exposed'].mean()
    total_cost = df['estimated_cost'].sum()
    
    # Industry Risk Assessment
    industry_risk = df.groupby('industry').agg({
        'records_exposed': ['sum', 'mean', 'count'],
        'estimated_cost': 'sum'
    }).round(2)
    
    industry_risk.columns = ['total_records', 'avg_records', 'breach_count', 'total_cost']
    industry_risk['risk_score'] = (
        industry_risk['total_records'] / industry_risk['total_records'].max() * 0.4 +
        industry_risk['avg_records'] / industry_risk['avg_records'].max() * 0.3 +
        industry_risk['breach_count'] / industry_risk['breach_count'].max() * 0.3
    )
    
    high_risk_industries = industry_risk.nlargest(3, 'risk_score').index.tolist()
    
    # Breach Type Analysis
    breach_type_analysis = df.groupby('breach_type').agg({
        'records_exposed': ['sum', 'mean'],
        'id': 'count'
    }).round(2)
    
    breach_type_analysis.columns = ['total_records', 'avg_records', 'count']
    most_common_type = breach_type_analysis.nlargest(1, 'count').index[0]
    
    # Temporal Analysis
    yearly_trends = df.groupby('year').agg({
        'id': 'count',
        'records_exposed': 'sum',
        'estimated_cost': 'sum'
    })
    
    # Risk Indicators
    insider_threats = df[df['breach_type'] == 'Insider Threat']['records_exposed'].sum()
    insider_percentage = (insider_threats / total_records) * 100
    
    large_breaches = df[df['records_exposed'] > 10000]['records_exposed'].sum()
    large_breach_percentage = (large_breaches / total_records) * 100
    
    insights = {
        'total_breaches': total_breaches,
        'total_records': total_records,
        'avg_records': avg_records,
        'total_cost': total_cost,
        'high_risk_industries': high_risk_industries,
        'most_common_type': most_common_type,
        'insider_percentage': insider_percentage,
        'large_breach_percentage': large_breach_percentage,
        'industry_risk': industry_risk,
        'breach_type_analysis': breach_type_analysis,
        'yearly_trends': yearly_trends
    }
    
    return insights

def create_advanced_visualizations(df: pd.DataFrame, insights: Dict):
    """Create advanced data visualizations"""
    
    # 1. Risk Heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=df.groupby(['industry', 'breach_type']).size().unstack(fill_value=0).values,
        x=df['breach_type'].unique(),
        y=df['industry'].unique(),
        colorscale='Reds',
        showscale=True
    ))
    
    fig_heatmap.update_layout(
        title="Breach Risk Heatmap: Industry vs Breach Type",
        xaxis_title="Breach Type",
        yaxis_title="Industry",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    # 2. Scatter Plot: Records vs Cost
    fig_scatter = px.scatter(
        df, 
        x='records_exposed', 
        y='estimated_cost',
        color='industry',
        size='records_exposed',
        hover_data=['name', 'breach_type', 'severity'],
        title="Records Exposed vs Estimated Cost by Industry"
    )
    
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    # 3. Geographic Distribution
    country_data = df.groupby('country').agg({
        'records_exposed': 'sum',
        'id': 'count'
    }).reset_index()
    
    fig_geo = px.choropleth(
        country_data,
        locations='country',
        color='records_exposed',
        hover_data=['id'],
        title="Geographic Distribution of Data Breaches",
        color_continuous_scale='Reds'
    )
    
    fig_geo.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    # 4. Time Series with Multiple Metrics
    monthly_data = df.groupby(['year', 'month']).agg({
        'id': 'count',
        'records_exposed': 'sum',
        'estimated_cost': 'sum'
    }).reset_index()
    
    monthly_data['date'] = pd.to_datetime(monthly_data[['year', 'month']].assign(day=1))
    
    fig_timeseries = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Breach Count', 'Records Exposed', 'Estimated Cost'),
        vertical_spacing=0.08
    )
    
    fig_timeseries.add_trace(
        go.Scatter(x=monthly_data['date'], y=monthly_data['id'], name='Breach Count'),
        row=1, col=1
    )
    
    fig_timeseries.add_trace(
        go.Scatter(x=monthly_data['date'], y=monthly_data['records_exposed'], name='Records Exposed'),
        row=2, col=1
    )
    
    fig_timeseries.add_trace(
        go.Scatter(x=monthly_data['date'], y=monthly_data['estimated_cost'], name='Estimated Cost'),
        row=3, col=1
    )
    
    fig_timeseries.update_layout(
        title="Temporal Analysis: Breach Trends Over Time",
        height=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    
    return {
        'heatmap': fig_heatmap,
        'scatter': fig_scatter,
        'geographic': fig_geo,
        'timeseries': fig_timeseries
    }

def main():
    """Main application function"""
    
    # Professional Header
    st.markdown("""
    <div class="main-header">
        <div class="header-container">
            <div class="header-main">
                <div class="header-icon">🛡️</div>
                <div class="header-title-section">
                    <h1>Data Breach Insights Report</h1>
                    <p>Advanced Analytics Dashboard for Cybersecurity Intelligence</p>
                </div>
            </div>
            <div class="header-divider"></div>
            <div class="header-features">
                <span class="feature-tag">AI-Powered Insights</span>
                <span class="feature-tag">Advanced Visualizations</span>
                <span class="feature-tag">Risk Assessment</span>
                <span class="feature-tag">Real-time Analytics</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown("## 📁 **Data Source**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your breach data file",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'tsv', 'txt'],
            help="Supported formats: CSV, Excel, JSON, Parquet, TSV, TXT"
        )
    
    with col2:
        use_sample = st.checkbox("Use Sample Data", value=True, help="Load with sample breach data for demonstration")
    
    # Load data
    if uploaded_file and not use_sample:
        df = load_and_clean_data(uploaded_file)
    else:
        df = load_and_clean_data()
    
    # Ensure data types
    df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
    if 'year' not in df.columns:
        df['year'] = df['breach_date'].dt.year
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 **Advanced Filters**")
    
    # Year range filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    
    year_range = st.sidebar.slider(
        "📅 Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Industry filter
    industries = st.sidebar.multiselect(
        "🏢 Industries",
        options=sorted(df['industry'].unique()),
        default=sorted(df['industry'].unique())[:5]
    )
    
    # Country filter
    countries = st.sidebar.multiselect(
        "🌍 Countries",
        options=sorted(df['country'].unique()),
        default=sorted(df['country'].unique())[:5]
    )
    
    # Breach type filter
    if 'breach_type' in df.columns:
        breach_types = st.sidebar.multiselect(
            "🔓 Breach Types",
            options=sorted(df['breach_type'].unique()),
            default=sorted(df['breach_type'].unique())
        )
    else:
        breach_types = []
    
    # Severity filter
    if 'severity' in df.columns:
        severities = st.sidebar.multiselect(
            "⚠️ Severity Levels",
            options=sorted(df['severity'].unique()),
            default=sorted(df['severity'].unique())
        )
    else:
        severities = []
    
    # Apply filters
    filtered_df = df[
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1]) &
        (df['industry'].isin(industries)) &
        (df['country'].isin(countries))
    ]
    
    if breach_types:
        filtered_df = filtered_df[filtered_df['breach_type'].isin(breach_types)]
    
    if severities:
        filtered_df = filtered_df[filtered_df['severity'].isin(severities)]
    
    # Generate AI Insights
    insights = generate_ai_insights(filtered_df)
    
    # KPI Cards with enhanced styling
    st.markdown("## 📊 **Key Performance Indicators**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: var(--accent-primary); margin-bottom: 0.5rem;">Total Breaches</h3>
            <h2 style="color: white; margin: 0;">{format_number(insights['total_breaches'])}</h2>
            <p style="color: var(--text-secondary); margin: 0;">Security Incidents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: var(--accent-primary); margin-bottom: 0.5rem;">Records Exposed</h3>
            <h2 style="color: white; margin: 0;">{format_number(insights['total_records'])}</h2>
            <p style="color: var(--text-secondary); margin: 0;">Data Records</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: var(--accent-primary); margin-bottom: 0.5rem;">Avg Records/Breach</h3>
            <h2 style="color: white; margin: 0;">{format_number(int(insights['avg_records']))}</h2>
            <p style="color: var(--text-secondary); margin: 0;">Per Incident</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: var(--accent-primary); margin-bottom: 0.5rem;">Estimated Cost</h3>
            <h2 style="color: white; margin: 0;">${format_number(int(insights['total_cost']))}</h2>
            <p style="color: var(--text-secondary); margin: 0;">Total Impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Insights Section
    st.markdown("## 🤖 **AI-Powered Security Insights**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-header">
                <span>🔍</span>
                <span>High-Risk Industries</span>
            </div>
            <p>Top vulnerable sectors: {', '.join(insights['high_risk_industries'])}</p>
            <div style="margin-top: 1rem;">
                <span class="risk-indicator risk-high">High Risk</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-header">
                <span>⚠️</span>
                <span>Threat Analysis</span>
            </div>
            <p>Most common breach type: <strong>{insights['most_common_type']}</strong></p>
            <p>Insider threats: {insights['insider_percentage']:.1f}% of total records</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced Visualizations
    st.markdown("## 📈 **Advanced Data Visualizations**")
    
    # Create visualizations
    charts = create_advanced_visualizations(filtered_df, insights)
    
    # Display charts in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Risk Heatmap", "📊 Scatter Analysis", "🌍 Geographic", "📅 Time Series"])
    
    with tab1:
        st.plotly_chart(charts['heatmap'], use_container_width=True)
    
    with tab2:
        st.plotly_chart(charts['scatter'], use_container_width=True)
    
    with tab3:
        st.plotly_chart(charts['geographic'], use_container_width=True)
    
    with tab4:
        st.plotly_chart(charts['timeseries'], use_container_width=True)
    
    # Industry Risk Analysis
    st.markdown("## 🏢 **Industry Risk Assessment**")
    
    industry_risk_df = insights['industry_risk'].reset_index()
    industry_risk_df = industry_risk_df.sort_values('risk_score', ascending=False)
    
    # Create risk score visualization
    fig_risk = px.bar(
        industry_risk_df.head(10),
        x='industry',
        y='risk_score',
        title="Industry Risk Scores",
        color='risk_score',
        color_continuous_scale='Reds'
    )
    
    fig_risk.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Top Companies Analysis
    st.markdown("## 🏆 **Top Companies by Impact**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Records Exposed")
        top_records = filtered_df.nlargest(10, 'records_exposed')[['name', 'industry', 'country', 'records_exposed']]
        st.dataframe(top_records, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Estimated Cost")
        top_cost = filtered_df.nlargest(10, 'estimated_cost')[['name', 'industry', 'country', 'estimated_cost']]
        st.dataframe(top_cost, use_container_width=True)
    
    # Export Section
    st.markdown("## 📥 **Export & Download**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"breach_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Excel Export with multiple sheets
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Breach Data', index=False)
            insights['industry_risk'].to_excel(writer, sheet_name='Industry Risk')
            insights['breach_type_analysis'].to_excel(writer, sheet_name='Breach Types')
            insights['yearly_trends'].to_excel(writer, sheet_name='Yearly Trends')
        
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📊 Download Excel Report",
            data=excel_data,
            file_name=f"breach_insights_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        # Summary Report
        summary_report = f"""
# Data Breach Insights Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total Breaches: {insights['total_breaches']:,}
- Total Records Exposed: {insights['total_records']:,}
- Estimated Cost: ${insights['total_cost']:,}
- Average Records per Breach: {insights['avg_records']:,.0f}

## Key Insights
- High-Risk Industries: {', '.join(insights['high_risk_industries'])}
- Most Common Breach Type: {insights['most_common_type']}
- Insider Threat Percentage: {insights['insider_percentage']:.1f}%
- Large Breach Percentage: {insights['large_breach_percentage']:.1f}%

## Recommendations
1. Focus security investments on high-risk industries
2. Implement enhanced monitoring for insider threats
3. Develop incident response plans for large-scale breaches
4. Regular security assessments and training programs
        """
        
        st.download_button(
            label="📋 Download Summary",
            data=summary_report,
            file_name=f"breach_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True
        )

if __name__ == "__main__":
    main()