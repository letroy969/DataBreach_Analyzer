"""
Data Breach Insights Report - AI Insights Module

This module provides AI-powered insights and executive summaries
for the breach data analysis using OpenAI's API.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import json
from datetime import datetime
import os
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIInsights:
    """Generates AI-powered insights and executive summaries."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = openai
            except Exception as e:
                st.warning(f"OpenAI API key not configured: {e}")
    
    def generate_executive_summary(self, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
        """
        Generate an AI-powered executive summary.
        
        Args:
            df (pd.DataFrame): Source data
            kpis (Dict[str, Any]): Key performance indicators
            
        Returns:
            str: Executive summary
        """
        if not self.client:
            return self._generate_fallback_summary(df, kpis)
        
        try:
            # Prepare data context
            context = self._prepare_data_context(df, kpis)
            
            prompt = f"""
            As a senior data analyst, provide a concise executive summary of this data breach analysis:
            
            Data Context:
            {context}
            
            Please provide:
            1. Key findings (3-4 bullet points)
            2. Risk assessment
            3. Recommendations
            4. Business impact
            
            Keep it professional and actionable for C-level executives.
            """
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a senior data analyst specializing in cybersecurity and risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating AI summary: {e}")
            return self._generate_fallback_summary(df, kpis)
    
    def generate_industry_insights(self, df: pd.DataFrame) -> str:
        """
        Generate industry-specific insights.
        
        Args:
            df (pd.DataFrame): Source data
            
        Returns:
            str: Industry insights
        """
        if not self.client:
            return self._generate_fallback_industry_insights(df)
        
        try:
            industry_stats = df.groupby('industry').agg({
                'id': 'count',
                'records_exposed': 'sum',
                'estimated_cost': 'sum'
            }).reset_index()
            
            context = f"""
            Industry Analysis:
            {industry_stats.to_string()}
            
            Top 3 industries by breach count:
            {industry_stats.nlargest(3, 'id')[['industry', 'id']].to_string()}
            """
            
            prompt = f"""
            Analyze these industry breach patterns and provide insights:
            {context}
            
            Focus on:
            1. Industry risk patterns
            2. Vulnerability trends
            3. Sector-specific recommendations
            """
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity risk analyst specializing in industry-specific threat assessment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating industry insights: {e}")
            return self._generate_fallback_industry_insights(df)
    
    def generate_trend_analysis(self, df: pd.DataFrame) -> str:
        """
        Generate trend analysis insights.
        
        Args:
            df (pd.DataFrame): Source data
            
        Returns:
            str: Trend analysis
        """
        if not self.client:
            return self._generate_fallback_trend_analysis(df)
        
        try:
            # Create yearly trends
            yearly_trends = df.groupby(df['breach_date'].dt.year).agg({
                'id': 'count',
                'records_exposed': 'sum',
                'estimated_cost': 'sum'
            }).reset_index()
            
            context = f"""
            Yearly Trends:
            {yearly_trends.to_string()}
            
            Growth rates:
            - Breach count: {self._calculate_growth_rate(yearly_trends, 'id')}%
            - Records exposed: {self._calculate_growth_rate(yearly_trends, 'records_exposed')}%
            - Estimated cost: {self._calculate_growth_rate(yearly_trends, 'estimated_cost')}%
            """
            
            prompt = f"""
            Analyze these breach trends and provide insights:
            {context}
            
            Focus on:
            1. Trend patterns and anomalies
            2. Growth implications
            3. Future predictions
            """
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data analyst specializing in trend analysis and forecasting."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating trend analysis: {e}")
            return self._generate_fallback_trend_analysis(df)
    
    def generate_risk_assessment(self, df: pd.DataFrame) -> str:
        """
        Generate risk assessment insights.
        
        Args:
            df (pd.DataFrame): Source data
            
        Returns:
            str: Risk assessment
        """
        if not self.client:
            return self._generate_fallback_risk_assessment(df)
        
        try:
            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(df)
            
            context = f"""
            Risk Assessment Metrics:
            {json.dumps(risk_metrics, indent=2)}
            """
            
            prompt = f"""
            Based on these risk metrics, provide a comprehensive risk assessment:
            {context}
            
            Include:
            1. Overall risk level
            2. Key risk factors
            3. Mitigation strategies
            4. Priority recommendations
            """
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity risk assessment expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating risk assessment: {e}")
            return self._generate_fallback_risk_assessment(df)
    
    def _prepare_data_context(self, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
        """Prepare data context for AI analysis."""
        return f"""
        Dataset Overview:
        - Total breaches: {kpis.get('total_breaches', 0):,}
        - Total records exposed: {kpis.get('total_records', 0):,}
        - Average cost: ${kpis.get('avg_cost', 0):.1f}M
        - Most affected industry: {kpis.get('most_affected_industry', 'N/A')}
        - Date range: {df['breach_date'].min()} to {df['breach_date'].max()}
        - Industries: {df['industry'].nunique()}
        - Countries: {df['country'].nunique()}
        """
    
    def _calculate_growth_rate(self, df: pd.DataFrame, column: str) -> float:
        """Calculate growth rate for a column."""
        if len(df) < 2:
            return 0
        
        first_value = df[column].iloc[0]
        last_value = df[column].iloc[-1]
        
        if first_value == 0:
            return 0
        
        return ((last_value - first_value) / first_value) * 100
    
    def _calculate_risk_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics."""
        return {
            'total_breaches': len(df),
            'avg_breach_size': df['records_exposed'].mean(),
            'max_breach_size': df['records_exposed'].max(),
            'critical_breaches': len(df[df['records_exposed'] >= 1_000_000]),
            'high_risk_industries': df['industry'].value_counts().head(3).to_dict(),
            'insider_threat_percentage': (df['breach_type'] == 'Insider').mean() * 100,
            'avg_cost_per_breach': df['estimated_cost'].mean(),
            'total_estimated_cost': df['estimated_cost'].sum()
        }
    
    def _generate_fallback_summary(self, df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
        """Generate fallback summary without AI."""
        return f"""
        **Executive Summary**
        
        **Key Findings:**
        • {kpis.get('total_breaches', 0):,} total breaches analyzed
        • {kpis.get('total_records', 0):,} records exposed
        • ${kpis.get('avg_cost', 0):.1f}M average cost per breach
        • {kpis.get('most_affected_industry', 'N/A')} most affected industry
        
        **Risk Assessment:**
        • High frequency of breaches in critical sectors
        • Significant financial impact across industries
        • Need for enhanced security measures
        
        **Recommendations:**
        • Implement comprehensive security frameworks
        • Focus on insider threat detection
        • Regular security assessments and training
        """
    
    def _generate_fallback_industry_insights(self, df: pd.DataFrame) -> str:
        """Generate fallback industry insights."""
        industry_stats = df.groupby('industry').agg({
            'id': 'count',
            'records_exposed': 'sum'
        }).reset_index()
        
        top_industry = industry_stats.loc[industry_stats['id'].idxmax()]
        
        return f"""
        **Industry Analysis**
        
        **Top Risk Industries:**
        • {top_industry['industry']}: {top_industry['id']} breaches, {top_industry['records_exposed']:,} records
        
        **Key Insights:**
        • Healthcare and Financial sectors show highest breach frequency
        • Insider threats prevalent across all industries
        • Need for industry-specific security protocols
        """
    
    def _generate_fallback_trend_analysis(self, df: pd.DataFrame) -> str:
        """Generate fallback trend analysis."""
        yearly_trends = df.groupby(df['breach_date'].dt.year).size()
        
        return f"""
        **Trend Analysis**
        
        **Yearly Patterns:**
        • {yearly_trends.index.min()}-{yearly_trends.index.max()} analysis period
        • Peak breach year: {yearly_trends.idxmax()} with {yearly_trends.max()} incidents
        
        **Key Trends:**
        • Increasing breach sophistication over time
        • Growing financial impact per incident
        • Need for proactive security measures
        """
    
    def _generate_fallback_risk_assessment(self, df: pd.DataFrame) -> str:
        """Generate fallback risk assessment."""
        critical_breaches = len(df[df['records_exposed'] >= 1_000_000])
        
        return f"""
        **Risk Assessment**
        
        **Risk Level: HIGH**
        
        **Key Risk Factors:**
        • {critical_breaches} critical breaches (1M+ records)
        • Average breach size: {df['records_exposed'].mean():,.0f} records
        • Total estimated cost: ${df['estimated_cost'].sum() / 1_000_000:.1f}M
        
        **Mitigation Priorities:**
        • Implement zero-trust security architecture
        • Enhance insider threat detection
        • Regular security training and awareness
        """
