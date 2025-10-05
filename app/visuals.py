"""
Data Breach Insights Report - Visualization Module (FIXED)

This module contains all Plotly chart configurations and visualization functions
for the Streamlit dashboard with professional styling and interactivity.
FIXED: All text, labels, and data names are now clearly visible.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

# Modern Dark Theme Color Scheme
COLORS = {
    'primary': '#00d4ff',      # Cyan blue
    'secondary': '#7c3aed',    # Purple
    'accent': '#10b981',       # Green
    'background': '#1e1e1e',   # Dark card background
    'text': '#ffffff',         # White text
    'text_secondary': '#b3b3b3',  # Secondary text
    'success': '#10b981',       # Green
    'warning': '#f59e0b',       # Amber
    'danger': '#ef4444'         # Red
}

# Modern Color palette for charts
CHART_COLORS = [
    '#00d4ff', '#7c3aed', '#10b981', '#f59e0b', '#ef4444', 
    '#06b6d4', '#84cc16', '#f97316', '#8b5cf6', '#ec4899'
]

def get_standard_layout():
    """Get standard layout configuration for all charts with modern dark theme."""
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',  # Transparent to match dark theme
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent to match dark theme
        'font_family': 'Inter, sans-serif',
        'font': dict(size=14, color=COLORS['text']),  # White text for dark theme
        'title_font_size': 20,
        'title_x': 0.5,
        'title_font': dict(size=20, color=COLORS['text']),  # White title for dark theme
        'xaxis': dict(
            title_font=dict(size=16, color=COLORS['text']),  # White axis titles
            tickfont=dict(size=14, color=COLORS['text_secondary']),    # Secondary text for ticks
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',         # Very subtle white grid
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        'yaxis': dict(
            title_font=dict(size=16, color=COLORS['text']),  # White axis titles
            tickfont=dict(size=14, color=COLORS['text_secondary']),    # Secondary text for ticks
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',         # Very subtle white grid
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        'legend': dict(
            font=dict(size=14, color=COLORS['text']),      # White legend text
            bgcolor='rgba(30,30,30,0.9)',                # Dark card background
            bordercolor='rgba(255,255,255,0.2)',      # Subtle white border
            borderwidth=1
        )
    }

class ChartBuilder:
    """Builds professional Plotly charts for the breach insights dashboard."""
    
    @staticmethod
    def create_trends_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create a line chart showing breach trends over time.
        
        Args:
            df (pd.DataFrame): Yearly trend data
            
        Returns:
            go.Figure: Plotly line chart
        """
        fig = px.line(
            df, 
            x='year', 
            y='breach_count',
            title='📈 Breach Trends Over Time',
            labels={'breach_count': 'Number of Breaches', 'year': 'Year'},
            color_discrete_sequence=[COLORS['primary']],
            markers=True
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        
        # Customize traces
        fig.update_traces(
            line=dict(width=4, color=COLORS['primary']),
            marker=dict(size=10, color=COLORS['accent'], line=dict(width=2, color='white')),
            hovertemplate='<b style="color: #ffffff;">Year:</b> <span style="color: #1fb6b6;">%{x}</span><br><b style="color: #ffffff;">Breaches:</b> <span style="color: #ffb86b;">%{y}</span><br><extra></extra>'
        )
        
        return fig
    
    @staticmethod
    def create_industry_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create a horizontal bar chart for top industries.
        
        Args:
            df (pd.DataFrame): Industry breakdown data
            
        Returns:
            go.Figure: Plotly horizontal bar chart
        """
        # Sort by breach count and take top 10
        df_sorted = df.nlargest(10, 'breach_count')
        
        fig = px.bar(
            df_sorted,
            x='breach_count',
            y='industry',
            orientation='h',
            title='🏢 Top Industries by Breach Count',
            labels={'breach_count': 'Number of Breaches', 'industry': 'Industry'},
            color='breach_count',
            color_continuous_scale=[COLORS['primary'], COLORS['secondary']]
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=500)
        
        # Customize traces
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=2,
            hovertemplate='<b style="color: #ffffff;">%{y}</b><br><b style="color: #ffffff;">Breaches:</b> <span style="color: #ffb86b;">%{x}</span><br><extra></extra>'
        )
        
        return fig
    
    @staticmethod
    def create_industry_donut(df: pd.DataFrame) -> go.Figure:
        """
        Create a donut chart for industry distribution.
        
        Args:
            df (pd.DataFrame): Industry breakdown data
            
        Returns:
            go.Figure: Plotly donut chart
        """
        fig = px.pie(
            df,
            values='breach_count',
            names='industry',
            title='🧭 Industry Distribution',
            hole=0.4,
            color_discrete_sequence=CHART_COLORS
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=500)
        
        # Customize traces
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b style="color: #ffffff;">%{label}</b><br><b style="color: #ffffff;">Breaches:</b> <span style="color: #ffb86b;">%{value}</span><br><b style="color: #ffffff;">Percentage:</b> <span style="color: #1fb6b6;">%{percent}</span><extra></extra>'
        )
        
        return fig
    
    @staticmethod
    def create_country_map(df: pd.DataFrame) -> go.Figure:
        """
        Create a choropleth map for country distribution.
        
        Args:
            df (pd.DataFrame): Country data
            
        Returns:
            go.Figure: Plotly choropleth map
        """
        # Country code mapping for common countries
        country_mapping = {
            'US': 'USA', 'CA': 'CAN', 'GB': 'GBR', 'DE': 'DEU', 'FR': 'FRA',
            'AU': 'AUS', 'JP': 'JPN', 'IN': 'IND', 'BR': 'BRA', 'MX': 'MEX',
            'IT': 'ITA', 'ES': 'ESP', 'NL': 'NLD', 'SE': 'SWE', 'NO': 'NOR',
            'DK': 'DNK', 'FI': 'FIN', 'CH': 'CHE', 'AT': 'AUT', 'BE': 'BEL'
        }
        
        df_mapped = df.copy()
        df_mapped['country_code'] = df_mapped['country'].map(country_mapping)
        df_mapped = df_mapped.dropna(subset=['country_code'])
        
        fig = px.choropleth(
            df_mapped,
            locations='country_code',
            color='breach_count',
            hover_name='country',
            hover_data={'breach_count': True, 'records_exposed': True},
            title='🌎 Breaches by Country',
            color_continuous_scale=[COLORS['primary'], COLORS['secondary'], COLORS['accent']],
            labels={'breach_count': 'Number of Breaches'}
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=500)
        
        # Customize geo
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)'
            )
        )
        
        return fig
    
    @staticmethod
    def create_cost_scatter(df: pd.DataFrame) -> go.Figure:
        """
        Create a scatter plot showing cost vs records correlation.
        
        Args:
            df (pd.DataFrame): Company data with cost and records
            
        Returns:
            go.Figure: Plotly scatter plot
        """
        fig = px.scatter(
            df,
            x='records_exposed',
            y='estimated_cost',
            color='industry',
            size='records_exposed',
            hover_name='name',
            hover_data=['country', 'breach_date'],
            title='💰 Cost vs Records Exposed',
            labels={
                'records_exposed': 'Records Exposed',
                'estimated_cost': 'Estimated Cost ($)',
                'industry': 'Industry'
            },
            color_discrete_sequence=CHART_COLORS
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=600)
        
        # Customize traces
        fig.update_traces(
            marker=dict(opacity=0.8, line=dict(width=2, color='white')),
            selector=dict(mode='markers'),
            hovertemplate='<b style="color: #ffffff;">%{hovertext}</b><br><b style="color: #ffffff;">Records:</b> <span style="color: #ffb86b;">%{x:,}</span><br><b style="color: #ffffff;">Cost:</b> <span style="color: #1fb6b6;">$%{y:,.0f}</span><br><b style="color: #ffffff;">Industry:</b> <span style="color: #ffb86b;">%{marker.color}</span><extra></extra>'
        )
        
        return fig
    
    @staticmethod
    def create_breach_type_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create a bar chart for breach types.
        
        Args:
            df (pd.DataFrame): Breach type data
            
        Returns:
            go.Figure: Plotly bar chart
        """
        breach_counts = df['breach_type'].value_counts().reset_index()
        breach_counts.columns = ['breach_type', 'count']
        
        fig = px.bar(
            breach_counts,
            x='breach_type',
            y='count',
            title='🔒 Breach Types Distribution',
            labels={'count': 'Number of Breaches', 'breach_type': 'Breach Type'},
            color='count',
            color_continuous_scale=[COLORS['primary'], COLORS['secondary']]
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=500)
        
        # Customize traces
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=2,
            hovertemplate='<b style="color: #ffffff;">%{x}</b><br><b style="color: #ffffff;">Breaches:</b> <span style="color: #ffb86b;">%{y}</span><br><extra></extra>'
        )
        
        return fig
    
    @staticmethod
    def create_cost_trends_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create a dual-axis chart showing both breach count and cost trends.
        
        Args:
            df (pd.DataFrame): Yearly trend data
            
        Returns:
            go.Figure: Plotly dual-axis chart
        """
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Add breach count line
        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df['breach_count'],
                name='Breach Count',
                line=dict(color=COLORS['primary'], width=4),
                marker=dict(size=10, color=COLORS['accent'])
            ),
            secondary_y=False
        )
        
        # Add cost line
        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df['estimated_cost'] / 1_000_000,  # Convert to millions
                name='Cost (Millions $)',
                line=dict(color=COLORS['secondary'], width=4),
                marker=dict(size=10, color=COLORS['accent'])
            ),
            secondary_y=True
        )
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(
            title='📊 Breach Count vs Cost Trends',
            height=500
        )
        
        # Customize axes
        fig.update_xaxes(title_text="Year", title_font=dict(size=16, color='#1e293b'))
        fig.update_yaxes(title_text="Number of Breaches", secondary_y=False, title_font=dict(size=16, color='#1e293b'))
        fig.update_yaxes(title_text="Cost (Millions $)", secondary_y=True, title_font=dict(size=16, color='#1e293b'))
        
        return fig
    
    @staticmethod
    def create_metrics_gauge(value: float, title: str, max_value: float = 100) -> go.Figure:
        """
        Create a gauge chart for KPI metrics.
        
        Args:
            value (float): Current value
            title (str): Gauge title
            max_value (float): Maximum value for the gauge
            
        Returns:
            go.Figure: Plotly gauge chart
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 18, 'color': '#ffffff'}},
            delta={'reference': max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value], 'tickfont': {'size': 14, 'color': '#ffffff'}},
                'bar': {'color': COLORS['primary']},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': COLORS['background']},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': COLORS['warning']},
                    {'range': [max_value * 0.8, max_value], 'color': COLORS['danger']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        # Apply standard layout
        fig.update_layout(**get_standard_layout())
        fig.update_layout(height=400)
        
        return fig
