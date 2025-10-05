"""
Data Breach Insights Report - Streamlit Dashboard

Professional enterprise data analytics dashboard for breach insights analysis.
Features interactive visualizations, AI-powered insights, and comprehensive filtering.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add app directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader
from visuals import ChartBuilder
from ai_insights import AIInsights
import io

# Set xlsxwriter flag to False for Streamlit Cloud compatibility
HAS_XLSXWRITER = False

# Page configuration
st.set_page_config(
    page_title="Data Breach Insights Report",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS with Professional Styling
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
    
    /* Custom Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Clean Professional Header */
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
    
    /* Modern KPI Cards */
    .kpi-card {
        background: var(--bg-card);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-primary);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent-gradient-alt);
    }
    
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        z-index: 1;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-primary);
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid var(--accent-primary);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: var(--accent-gradient);
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    .sidebar .stSelectbox label,
    .sidebar .stSlider label,
    .sidebar .stTextInput label,
    .sidebar .stFileUploader label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar .stSelectbox > div > div,
    .sidebar .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        border-radius: 8px;
    }
    
    .sidebar .stSlider > div > div > div {
        background: var(--bg-card);
    }
    
    /* Chart Containers */
    .js-plotly-plot {
        background: var(--bg-card);
        border-radius: 12px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }
    
    /* Data Tables */
    .stDataFrame {
        background: var(--bg-card);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }
    
    .stDataFrame th {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        font-weight: 600;
        font-size: 14px;
        border-bottom: 1px solid var(--border);
    }
    
    .stDataFrame td {
        font-size: 14px;
        color: var(--text-primary);
        border-bottom: 1px solid var(--border);
        background: var(--bg-card);
    }
    
    .stDataFrame tr:hover {
        background: var(--bg-hover);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary);
        color: var(--bg-primary);
        font-weight: 600;
    }
    
    /* Buttons */
    .stDownloadButton > button,
    .stButton > button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover,
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--text-secondary);
        border-top: 1px solid var(--border);
        margin-top: 4rem;
        background: var(--bg-secondary);
        border-radius: 16px;
    }
    
    .footer a {
        color: var(--accent-primary);
        text-decoration: none;
        font-weight: 500;
        margin: 0 1rem;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: var(--accent-secondary);
    }
    
    /* Text Styling */
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    .stMarkdown h1, 
    .stMarkdown h2, 
    .stMarkdown h3 {
        color: var(--text-primary);
        font-weight: 700;
    }
    
    /* Status Messages */
    .stSuccess {
        background: var(--success);
        color: white;
        border-radius: 8px;
    }
    
    .stError {
        background: var(--error);
        color: white;
        border-radius: 8px;
    }
    
    .stInfo {
        background: var(--accent-primary);
        color: var(--bg-primary);
        border-radius: 8px;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
    
    /* Animation for loading */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-card, .section-header {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .header-main {
            flex-direction: column;
            gap: 1rem;
        }
        
        .header-title-section h1 {
            font-size: 2.2rem;
        }
        
        .header-title-section p {
            font-size: 1rem;
        }
        
        .header-icon {
            font-size: 2.5rem;
        }
        
        .header-features {
            gap: 0.5rem;
        }
        
        .feature-tag {
            font-size: 0.8rem;
            padding: 0.3rem 0.8rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .kpi-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_excel_file(df, filename_prefix="breach_data"):
    """Create a formatted Excel file with sorted data."""
    # Create an in-memory Excel file
    output = io.BytesIO()
    
    # Sort data by records exposed (descending) and then by date
    sorted_df = df.sort_values(['records_exposed', 'breach_date'], ascending=[False, False])
    
    # Choose engine based on availability
    engine = 'xlsxwriter' if HAS_XLSXWRITER else 'openpyxl'
    
    with pd.ExcelWriter(output, engine=engine) as writer:
        # Write the sorted data
        sorted_df.to_excel(writer, sheet_name='Breach Data', index=False)
        
        # Apply formatting only if xlsxwriter is available
        if HAS_XLSXWRITER:
            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Breach Data']
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            number_format = workbook.add_format({'num_format': '#,##0'})
            currency_format = workbook.add_format({'num_format': '$#,##0'})
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            
            # Set column widths
            worksheet.set_column('A:A', 10)  # ID
            worksheet.set_column('B:B', 12)  # Date
            worksheet.set_column('C:C', 25)  # Company
            worksheet.set_column('D:D', 15)  # Industry
            worksheet.set_column('E:E', 10)  # Country
            worksheet.set_column('F:F', 15)  # Records
            worksheet.set_column('G:G', 20)  # Breach Type
            worksheet.set_column('H:H', 15)  # Estimated Cost
            worksheet.set_column('I:I', 10)  # Year
            
            # Apply header formatting
            for col_num, value in enumerate(sorted_df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Apply number formatting to specific columns
            if 'records_exposed' in sorted_df.columns:
                col_idx = list(sorted_df.columns).index('records_exposed')
                worksheet.set_column(col_idx, col_idx, 15, number_format)
            
            if 'estimated_cost' in sorted_df.columns:
                col_idx = list(sorted_df.columns).index('estimated_cost')
                worksheet.set_column(col_idx, col_idx, 15, currency_format)
            
            if 'breach_date' in sorted_df.columns:
                col_idx = list(sorted_df.columns).index('breach_date')
                worksheet.set_column(col_idx, col_idx, 12, date_format)
        
        # Add summary sheet
        summary_data = {
            'Metric': ['Total Breaches', 'Total Records Exposed', 'Average Records per Breach', 'Total Estimated Cost', 'Average Cost per Breach'],
            'Value': [
                len(sorted_df),
                sorted_df['records_exposed'].sum(),
                sorted_df['records_exposed'].mean(),
                sorted_df['estimated_cost'].sum(),
                sorted_df['estimated_cost'].mean()
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Format summary sheet only if xlsxwriter is available
        if HAS_XLSXWRITER:
            summary_worksheet = writer.sheets['Summary']
            summary_worksheet.set_column('A:A', 25)
            summary_worksheet.set_column('B:B', 20, number_format)
            
            # Apply header formatting to summary
            for col_num, value in enumerate(summary_df.columns.values):
                summary_worksheet.write(0, col_num, value, header_format)
    
    output.seek(0)
    return output.getvalue()

def main():
    """Main application function."""
    
    # Initialize components
    data_loader = DataLoader()
    chart_builder = ChartBuilder()
    ai_insights = AIInsights()
    
    # Clean Professional Header
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
                <span class="feature-tag">Real-time Analytics</span>
                <span class="feature-tag">AI-Powered</span>
                <span class="feature-tag">Professional</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading breach data..."):
        df = data_loader.load_data()
    
    if df.empty:
        st.error("No data available. Please check your data files.")
        return
    
    # Sidebar filters
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0; text-align: center; font-weight: 600;">🔍 Filters & Controls</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Year range filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    
    # Ensure min_value is less than max_value for the slider
    if min_year == max_year:
        min_year = max_year - 1 if max_year > 2020 else 2019
        max_year = max_year + 1 if max_year < 2024 else 2024
    
    year_range = st.sidebar.slider(
        "📅 Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(int(df['year'].min()), int(df['year'].max())),
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
        default=sorted(df['country'].unique())[:10]
    )
    
    # Breach type filter
    breach_types = st.sidebar.multiselect(
        "🔒 Breach Types",
        options=sorted(df['breach_type'].unique()),
        default=sorted(df['breach_type'].unique())
    )
    
    # Company search
    company_search = st.sidebar.text_input(
        "🔍 Search Companies",
        placeholder="Enter company name..."
    )
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload Data File",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'tsv', 'txt'],
        accept_multiple_files=False,
        help="Upload your own breach data file (CSV, Excel, JSON, Parquet, TSV, or TXT)"
    )
    
    # Apply filters
    filters = {
        'year_range': year_range,
        'industries': industries,
        'countries': countries,
        'breach_types': breach_types,
        'company_search': company_search
    }
    
    filtered_df = data_loader.get_filtered_data(df, filters)
    
    # Handle file upload
    if uploaded_file is not None:
        try:
            # Show file info
            st.sidebar.info(f"📁 File: {uploaded_file.name}")
            
            # Read the uploaded file based on file type
            file_name = uploaded_file.name.lower()
            content_type = uploaded_file.type.lower()
            
            # Determine file extension
            if '.' in file_name:
                file_extension = file_name.split('.')[-1]
            else:
                # Try to detect from content type
                if 'csv' in content_type or 'text/csv' in content_type:
                    file_extension = 'csv'
                elif 'json' in content_type:
                    file_extension = 'json'
                elif ('excel' in content_type or 'spreadsheet' in content_type or 
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type):
                    file_extension = 'xlsx'
                else:
                    file_extension = 'csv'  # Default fallback
            
            # Additional check for Excel files
            if ('xlsx' in file_name or 'xls' in file_name or 
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type or
                'application/vnd.ms-excel' in content_type):
                file_extension = 'xlsx'
            
            if file_extension == 'csv':
                uploaded_df = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                # Read Excel file - use first sheet by default
                uploaded_df = pd.read_excel(uploaded_file, sheet_name=0)
            elif file_extension == 'json':
                # Read JSON file
                uploaded_df = pd.read_json(uploaded_file)
            elif file_extension == 'parquet':
                # Read Parquet file
                uploaded_df = pd.read_parquet(uploaded_file)
            elif file_extension == 'tsv':
                # Read TSV file (tab-separated values)
                uploaded_df = pd.read_csv(uploaded_file, sep='\t')
            elif file_extension == 'txt':
                # Try to read as CSV first, then TSV if that fails
                try:
                    uploaded_df = pd.read_csv(uploaded_file, sep=',')
                except:
                    uploaded_df = pd.read_csv(uploaded_file, sep='\t')
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            # Show file info
            st.sidebar.info(f"📊 Columns: {list(uploaded_df.columns)}")
            st.sidebar.info(f"📈 Rows: {len(uploaded_df)}")
            
            # Clean and process the data
            uploaded_df = data_loader._clean_data(uploaded_df)
            st.sidebar.success(f"✅ Loaded {len(uploaded_df)} records from uploaded file")
            
            # Apply filters to uploaded data
            filtered_df = data_loader.get_filtered_data(uploaded_df, filters)
            
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {str(e)}")
            st.sidebar.info("💡 **Tip:** Make sure your file has columns like 'date', 'records', 'company', 'industry', etc.")
            st.sidebar.info("📋 **Supported formats:** CSV, Excel (.xlsx, .xls), JSON, Parquet, TSV, TXT")
            # Continue with original data if upload fails
            filtered_df = data_loader.get_filtered_data(df, filters)
    
    # KPI Cards
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpis = data_loader.get_kpi_metrics(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-container">
                <div>
                    <div class="metric-value">{format_number(kpis['total_breaches'])}</div>
                    <div class="metric-label">Total Breaches</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-container">
                <div>
                    <div class="metric-value">{format_number(kpis['total_records'])}</div>
                    <div class="metric-label">Records Exposed</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-container">
                <div>
                    <div class="metric-value">{format_currency(kpis['avg_cost'], '')}M</div>
                    <div class="metric-label">Avg Cost (Millions)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-container">
                <div>
                    <div class="metric-value">{kpis['most_affected_industry']}</div>
                    <div class="metric-label">Top Industry</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<div class="section-header">📈 Data Visualizations</div>', unsafe_allow_html=True)
    
    # Row 1: Trends and Industry
    col1, col2 = st.columns(2)
    
    with col1:
        yearly_trends = data_loader.get_yearly_trends(filtered_df)
        trends_chart = chart_builder.create_trends_chart(yearly_trends)
        st.plotly_chart(trends_chart, use_container_width=True)
    
    with col2:
        industry_breakdown = data_loader.get_industry_breakdown(filtered_df)
        industry_chart = chart_builder.create_industry_chart(industry_breakdown)
        st.plotly_chart(industry_chart, use_container_width=True)
    
    # Row 2: Country Map and Industry Donut
    col1, col2 = st.columns(2)
    
    with col1:
        country_data = data_loader.get_country_data(filtered_df)
        if not country_data.empty:
            country_map = chart_builder.create_country_map(country_data)
            st.plotly_chart(country_map, use_container_width=True)
        else:
            st.info("No country data available for mapping")
    
    with col2:
        industry_donut = chart_builder.create_industry_donut(industry_breakdown)
        st.plotly_chart(industry_donut, use_container_width=True)
    
    # Row 3: Cost Analysis
    if not filtered_df.empty:
        cost_scatter = chart_builder.create_cost_scatter(filtered_df)
        st.plotly_chart(cost_scatter, use_container_width=True)
    
    # AI Insights Section
    st.markdown('<div class="section-header">🤖 AI-Powered Insights</div>', unsafe_allow_html=True)
    
    # Tabs for different insights
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Summary", "🏢 Industry Analysis", "📈 Trend Analysis", "⚠️ Risk Assessment"])
    
    with tab1:
        with st.spinner("Generating executive summary..."):
            summary = ai_insights.generate_executive_summary(filtered_df, kpis)
            st.markdown(summary)
    
    with tab2:
        with st.spinner("Analyzing industry patterns..."):
            industry_insights = ai_insights.generate_industry_insights(filtered_df)
            st.markdown(industry_insights)
    
    with tab3:
        with st.spinner("Analyzing trends..."):
            trend_analysis = ai_insights.generate_trend_analysis(filtered_df)
            st.markdown(trend_analysis)
    
    with tab4:
        with st.spinner("Assessing risks..."):
            risk_assessment = ai_insights.generate_risk_assessment(filtered_df)
            st.markdown(risk_assessment)
    
    # Data Explorer Section
    st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
    
    # Top companies table
    st.subheader("🏆 Top Companies by Records Exposed")
    top_companies = data_loader.get_top_companies(filtered_df, 10)
    
    if not top_companies.empty:
        # Format the display
        display_df = top_companies.copy()
        display_df['records_exposed'] = display_df['records_exposed'].apply(lambda x: format_number(x))
        display_df['estimated_cost'] = display_df['estimated_cost'].apply(lambda x: format_currency(x))
        display_df['breach_date'] = display_df['breach_date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = top_companies.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"top_companies_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            excel_data = create_excel_file(top_companies, "top_companies")
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"top_companies_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("No data available for the selected filters")
    
    # Full data table
    st.subheader("📊 Complete Dataset")
    
    if st.checkbox("Show full dataset", value=False):
        # Format for display
        display_full_df = filtered_df.copy()
        display_full_df['records_exposed'] = display_full_df['records_exposed'].apply(lambda x: format_number(x))
        display_full_df['estimated_cost'] = display_full_df['estimated_cost'].apply(lambda x: format_currency(x))
        display_full_df['breach_date'] = display_full_df['breach_date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_full_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download full dataset buttons
        col1, col2 = st.columns(2)
        
        with col1:
            full_csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=full_csv_data,
                file_name=f"breach_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            full_excel_data = create_excel_file(filtered_df, "breach_data")
            st.download_button(
                label="📊 Download Excel",
                data=full_excel_data,
                file_name=f"breach_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>Data Breach Insights Report</strong></p>
        <p>Professional Data Analytics Dashboard | Built with Streamlit</p>
        <p>
            <a href="https://github.com/yourusername/data-breach-insights" target="_blank">📁 View Source</a> |
            <a href="https://linkedin.com/in/sihle-dladla" target="_blank">💼 LinkedIn</a> |
            <a href="mailto:lindaletroy27@gmail.com">📧 Contact</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
