"""
Data Breach Insights Report - Streamlit Dashboard
Professional enterprise data analytics dashboard for breach insights analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="Data Breach Insights Report",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark Theme CSS
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
</style>
""", unsafe_allow_html=True)

def create_sample_data():
    """Create sample breach data for demonstration"""
    import numpy as np
    
    # Sample data
    companies = [
        'TechCorp Inc', 'HealthSys Ltd', 'FinanceFirst', 'RetailMax', 'EduTech Solutions',
        'Manufacturing Co', 'Logistics Pro', 'Energy Corp', 'Media Group', 'Consulting Firm',
        'Software House', 'Banking Group', 'Insurance Co', 'Travel Agency', 'Food Chain'
    ]
    
    industries = ['Technology', 'Healthcare', 'Financial', 'Retail', 'Education', 
                 'Manufacturing', 'Logistics', 'Energy', 'Media', 'Consulting']
    
    countries = ['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'JP', 'SG', 'NL', 'SE']
    
    breach_types = ['Hacking', 'Insider Threat', 'Physical Theft', 'Social Engineering', 'System Error']
    
    # Generate sample data
    data = []
    for i in range(500):
        company = np.random.choice(companies)
        industry = np.random.choice(industries)
        country = np.random.choice(countries)
        breach_type = np.random.choice(breach_types)
        
        # Generate realistic breach dates (2020-2024)
        year = np.random.randint(2020, 2025)
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)
        
        # Generate realistic record counts
        if industry == 'Healthcare':
            records = np.random.randint(1000, 50000)
        elif industry == 'Financial':
            records = np.random.randint(500, 20000)
        else:
            records = np.random.randint(100, 10000)
        
        # Calculate estimated cost ($200 per record)
        estimated_cost = records * 200
        
        data.append({
            'id': i + 1,
            'breach_date': f"{year}-{month:02d}-{day:02d}",
            'name': company,
            'industry': industry,
            'country': country,
            'records_exposed': records,
            'breach_type': breach_type,
            'estimated_cost': estimated_cost,
            'year': year
        })
    
    return pd.DataFrame(data)

def main():
    """Main application function"""
    
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
    
    # Load sample data
    with st.spinner("Loading breach data..."):
        df = create_sample_data()
        df['breach_date'] = pd.to_datetime(df['breach_date'])
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 **Filters**")
    
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
    
    # Apply filters
    filtered_df = df[
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1]) &
        (df['industry'].isin(industries)) &
        (df['country'].isin(countries))
    ]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Breaches",
            value=f"{len(filtered_df):,}",
            delta=f"+{len(filtered_df) - len(df) + len(df):,}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        total_records = filtered_df['records_exposed'].sum()
        st.metric(
            label="📈 Records Exposed",
            value=f"{total_records:,}",
            delta=f"+{total_records - df['records_exposed'].sum() + df['records_exposed'].sum():,}" if len(filtered_df) != len(df) else None
        )
    
    with col3:
        avg_records = filtered_df['records_exposed'].mean()
        st.metric(
            label="📊 Avg Records/Breach",
            value=f"{avg_records:,.0f}",
            delta=f"+{avg_records - df['records_exposed'].mean() + df['records_exposed'].mean():,.0f}" if len(filtered_df) != len(df) else None
        )
    
    with col4:
        total_cost = filtered_df['estimated_cost'].sum()
        st.metric(
            label="💰 Estimated Cost",
            value=f"${total_cost:,.0f}",
            delta=f"+${total_cost - df['estimated_cost'].sum() + df['estimated_cost'].sum():,.0f}" if len(filtered_df) != len(df) else None
        )
    
    # Charts
    st.markdown("## 📊 **Data Visualizations**")
    
    # Yearly trends
    yearly_data = filtered_df.groupby('year').agg({
        'id': 'count',
        'records_exposed': 'sum',
        'estimated_cost': 'sum'
    }).reset_index()
    
    fig_yearly = px.line(
        yearly_data, 
        x='year', 
        y='id',
        title='Breach Trends by Year',
        labels={'id': 'Number of Breaches', 'year': 'Year'}
    )
    fig_yearly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Industry distribution
    industry_data = filtered_df.groupby('industry').agg({
        'id': 'count',
        'records_exposed': 'sum'
    }).reset_index()
    
    fig_industry = px.bar(
        industry_data,
        x='industry',
        y='records_exposed',
        title='Records Exposed by Industry',
        labels={'records_exposed': 'Records Exposed', 'industry': 'Industry'}
    )
    fig_industry.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white'
    )
    st.plotly_chart(fig_industry, use_container_width=True)
    
    # Top companies
    st.markdown("## 🏢 **Top Companies by Records Exposed**")
    top_companies = filtered_df.nlargest(10, 'records_exposed')[['name', 'industry', 'country', 'records_exposed', 'estimated_cost']]
    st.dataframe(top_companies, use_container_width=True)
    
    # Download section
    st.markdown("## 📥 **Download Data**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"breach_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Simple Excel export using openpyxl
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='Breach Data', index=False)
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name=f"breach_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
