"""
AI-powered insights module for the Data Breach Insights Report.
Provides intelligent analysis and recommendations based on breach data.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class AIInsights:
    """AI-powered insights generator for breach data analysis."""
    
    def __init__(self):
        """Initialize the AI insights generator."""
        self.insights_cache = {}
    
    @st.cache_data
    def generate_insights(_self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate AI-powered insights from breach data.
        
        Args:
            df (pd.DataFrame): Breach data
            
        Returns:
            Dict[str, Any]: Generated insights
        """
        try:
            insights = {
                'risk_assessment': _self._assess_risk_levels(df),
                'trend_analysis': _self._analyze_trends(df),
                'industry_recommendations': _self._generate_industry_recommendations(df),
                'geographic_insights': _self._analyze_geographic_patterns(df),
                'cost_impact': _self._analyze_cost_impact(df),
                'prevention_strategies': _self._suggest_prevention_strategies(df)
            }
            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {'error': str(e)}
    
    def _assess_risk_levels(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Assess risk levels based on breach data."""
        if df.empty:
            return {'overall_risk': 'Low', 'factors': []}
        
        # Calculate risk factors
        total_records = df['records_exposed'].sum()
        total_cost = df['estimated_cost'].sum()
        breach_count = len(df)
        
        # Risk assessment logic
        risk_factors = []
        overall_risk = 'Low'
        
        if total_records > 100_000_000:  # 100M+ records
            risk_factors.append("Extremely high volume of exposed records")
            overall_risk = 'Critical'
        elif total_records > 10_000_000:  # 10M+ records
            risk_factors.append("Very high volume of exposed records")
            overall_risk = 'High'
        elif total_records > 1_000_000:  # 1M+ records
            risk_factors.append("High volume of exposed records")
            overall_risk = 'Medium'
        
        if total_cost > 10_000_000_000:  # $10B+ cost
            risk_factors.append("Extremely high financial impact")
            overall_risk = 'Critical' if overall_risk != 'Critical' else 'Critical'
        elif total_cost > 1_000_000_000:  # $1B+ cost
            risk_factors.append("Very high financial impact")
            overall_risk = 'High' if overall_risk in ['Low', 'Medium'] else overall_risk
        
        if breach_count > 1000:
            risk_factors.append("Very high frequency of breaches")
            overall_risk = 'High' if overall_risk in ['Low', 'Medium'] else overall_risk
        elif breach_count > 100:
            risk_factors.append("High frequency of breaches")
            overall_risk = 'Medium' if overall_risk == 'Low' else overall_risk
        
        return {
            'overall_risk': overall_risk,
            'factors': risk_factors,
            'metrics': {
                'total_records_exposed': total_records,
                'total_estimated_cost': total_cost,
                'total_breaches': breach_count
            }
        }
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trends in breach data."""
        if df.empty or 'year' not in df.columns:
            return {'trend': 'No trend data available'}
        
        # Group by year
        yearly_data = df.groupby('year').agg({
            'records_exposed': 'sum',
            'estimated_cost': 'sum',
            'id': 'count'
        }).rename(columns={'id': 'breach_count'})
        
        if len(yearly_data) < 2:
            return {'trend': 'Insufficient data for trend analysis'}
        
        # Calculate trends
        years = sorted(yearly_data.index)
        recent_years = years[-3:] if len(years) >= 3 else years
        
        trend_analysis = {
            'breach_frequency': self._calculate_trend(yearly_data['breach_count']),
            'records_exposed': self._calculate_trend(yearly_data['records_exposed']),
            'financial_impact': self._calculate_trend(yearly_data['estimated_cost']),
            'recent_performance': yearly_data.loc[recent_years].to_dict('index') if recent_years else {}
        }
        
        return trend_analysis
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction from a time series."""
        if len(series) < 2:
            return 'Insufficient data'
        
        # Simple linear trend calculation
        x = range(len(series))
        y = series.values
        
        # Calculate slope
        n = len(x)
        slope = (n * sum(x[i] * y[i] for i in range(n)) - sum(x) * sum(y)) / (n * sum(xi**2 for xi in x) - sum(x)**2)
        
        if slope > 0:
            return 'Increasing'
        elif slope < 0:
            return 'Decreasing'
        else:
            return 'Stable'
    
    def _generate_industry_recommendations(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Generate industry-specific recommendations."""
        if df.empty or 'industry' not in df.columns:
            return {'recommendations': ['No industry data available']}
        
        # Analyze industry patterns
        industry_stats = df.groupby('industry').agg({
            'records_exposed': ['sum', 'mean', 'count'],
            'estimated_cost': ['sum', 'mean']
        }).round(2)
        
        recommendations = {}
        
        # Generate recommendations for each industry
        for industry in industry_stats.index:
            industry_recs = []
            records_sum = industry_stats.loc[industry, ('records_exposed', 'sum')]
            records_mean = industry_stats.loc[industry, ('records_exposed', 'mean')]
            breach_count = industry_stats.loc[industry, ('records_exposed', 'count')]
            
            if records_sum > df['records_exposed'].quantile(0.8):
                industry_recs.append(f"🚨 {industry} shows extremely high breach volumes - implement enhanced monitoring")
            
            if records_mean > df['records_exposed'].mean() * 1.5:
                industry_recs.append(f"📊 {industry} has above-average breach sizes - review data protection strategies")
            
            if breach_count > df.groupby('industry').size().quantile(0.8):
                industry_recs.append(f"⚠️ {industry} experiences frequent breaches - strengthen incident response")
            
            if not industry_recs:
                industry_recs.append(f"✅ {industry} shows relatively good security posture")
            
            recommendations[industry] = industry_recs
        
        return recommendations
    
    def _analyze_geographic_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze geographic patterns in breach data."""
        if df.empty or 'country' not in df.columns:
            return {'patterns': 'No geographic data available'}
        
        country_stats = df.groupby('country').agg({
            'records_exposed': ['sum', 'count'],
            'estimated_cost': 'sum'
        }).round(2)
        
        # Identify high-risk countries
        high_risk_countries = country_stats[
            country_stats[('records_exposed', 'sum')] > df['records_exposed'].quantile(0.8)
        ].index.tolist()
        
        return {
            'high_risk_countries': high_risk_countries,
            'country_statistics': country_stats.to_dict('index'),
            'geographic_diversity': df['country'].nunique(),
            'recommendations': [
                f"Focus security resources on {', '.join(high_risk_countries[:3])}" if high_risk_countries 
                else "Geographic risk distribution appears balanced"
            ]
        }
    
    def _analyze_cost_impact(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze cost impact of breaches."""
        if df.empty:
            return {'analysis': 'No cost data available'}
        
        total_cost = df['estimated_cost'].sum()
        avg_cost = df['estimated_cost'].mean()
        median_cost = df['estimated_cost'].median()
        
        # Cost analysis
        cost_analysis = {
            'total_impact': f"${total_cost:,.0f}",
            'average_per_breach': f"${avg_cost:,.0f}",
            'median_breach_cost': f"${median_cost:,.0f}",
            'cost_distribution': {
                'low_cost': len(df[df['estimated_cost'] < df['estimated_cost'].quantile(0.33)]),
                'medium_cost': len(df[(df['estimated_cost'] >= df['estimated_cost'].quantile(0.33)) & 
                                    (df['estimated_cost'] < df['estimated_cost'].quantile(0.67))]),
                'high_cost': len(df[df['estimated_cost'] >= df['estimated_cost'].quantile(0.67)])
            }
        }
        
        return cost_analysis
    
    def _suggest_prevention_strategies(self, df: pd.DataFrame) -> List[str]:
        """Suggest prevention strategies based on breach patterns."""
        if df.empty:
            return ['No data available for strategy recommendations']
        
        strategies = []
        
        # Analyze breach types if available
        if 'breach_type' in df.columns:
            breach_types = df['breach_type'].value_counts()
            top_breach_type = breach_types.index[0] if not breach_types.empty else None
            
            if top_breach_type:
                if 'Hacking' in top_breach_type or 'Cyber' in top_breach_type:
                    strategies.append("🛡️ Strengthen network security and implement advanced threat detection")
                elif 'Insider' in top_breach_type:
                    strategies.append("👥 Enhance employee training and implement access controls")
                elif 'Physical' in top_breach_type:
                    strategies.append("🏢 Improve physical security measures and device management")
                elif 'Social' in top_breach_type:
                    strategies.append("🎯 Conduct regular security awareness training and phishing simulations")
        
        # General recommendations based on data patterns
        if df['records_exposed'].sum() > 10_000_000:
            strategies.append("📊 Implement data minimization and encryption for large datasets")
        
        if len(df) > 100:
            strategies.append("🔄 Establish robust incident response procedures and regular security audits")
        
        strategies.extend([
            "🔐 Implement multi-factor authentication across all systems",
            "📱 Regular security assessments and penetration testing",
            "🚨 Deploy comprehensive monitoring and alerting systems",
            "📚 Maintain up-to-date security policies and procedures"
        ])
        
        return strategies[:8]  # Limit to 8 strategies
    
    def format_insights_for_display(self, insights: Dict[str, Any]) -> str:
        """Format insights for display in the Streamlit app."""
        if 'error' in insights:
            return f"❌ Error generating insights: {insights['error']}"
        
        formatted_text = "## 🤖 AI-Powered Insights\n\n"
        
        # Risk Assessment
        if 'risk_assessment' in insights:
            risk = insights['risk_assessment']
            risk_emoji = {'Low': '🟢', 'Medium': '🟡', 'High': '🟠', 'Critical': '🔴'}
            formatted_text += f"### Risk Assessment: {risk_emoji.get(risk['overall_risk'], '⚪')} {risk['overall_risk']}\n"
            
            for factor in risk.get('factors', []):
                formatted_text += f"- {factor}\n"
            formatted_text += "\n"
        
        # Prevention Strategies
        if 'prevention_strategies' in insights:
            formatted_text += "### 🛡️ Recommended Prevention Strategies\n"
            for strategy in insights['prevention_strategies'][:5]:  # Show top 5
                formatted_text += f"- {strategy}\n"
            formatted_text += "\n"
        
        return formatted_text
