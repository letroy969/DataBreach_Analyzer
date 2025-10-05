#!/usr/bin/env python3
"""
Data Breach Insights Report - Advanced Analytics

This script demonstrates advanced data analysis techniques including:
- Time series analysis and decomposition
- Clustering analysis for breach pattern identification
- Predictive modeling for breach risk assessment
- Statistical analysis and hypothesis testing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_explore_data():
    """Load and perform initial data exploration."""
    print("📊 Loading and exploring data...")
    
    # Load data
    df = pd.read_csv('../data/sample_breaches.csv')
    df['breach_date'] = pd.to_datetime(df['breach_date'])
    df['year'] = df['breach_date'].dt.year
    df['month'] = df['breach_date'].dt.month
    df['quarter'] = df['breach_date'].dt.quarter
    
    print(f"📊 Dataset loaded: {len(df)} records")
    print(f"📅 Date range: {df['breach_date'].min().strftime('%Y-%m-%d')} to {df['breach_date'].max().strftime('%Y-%m-%d')}")
    print(f"🔢 Total records exposed: {df['records_exposed'].sum():,}")
    
    # Basic statistics
    print("\n📈 Dataset Overview:")
    print(f"• Total breaches: {len(df):,}")
    print(f"• Total records exposed: {df['records_exposed'].sum():,}")
    print(f"• Average breach size: {df['records_exposed'].mean():,.0f}")
    print(f"• Median breach size: {df['records_exposed'].median():,.0f}")
    print(f"• Largest breach: {df['records_exposed'].max():,}")
    print(f"• Unique industries: {df['industry'].nunique()}")
    print(f"• Unique countries: {df['country'].nunique()}")
    print(f"• Unique breach types: {df['breach_type'].nunique()}")
    
    return df

def time_series_analysis(df):
    """Perform time series analysis and decomposition."""
    print("\n📈 Performing time series analysis...")
    
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.stattools import adfuller
    
    # Create monthly time series
    monthly_breaches = df.set_index('breach_date').resample('M').size()
    monthly_records = df.set_index('breach_date').resample('M')['records_exposed'].sum()
    
    # Plot time series
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Time Series Analysis of Data Breaches', fontsize=16, fontweight='bold')
    
    # Breaches per month
    axes[0,0].plot(monthly_breaches.index, monthly_breaches.values, linewidth=2, color='#0b2948')
    axes[0,0].set_title('Breaches per Month')
    axes[0,0].set_ylabel('Number of Breaches')
    axes[0,0].grid(True, alpha=0.3)
    
    # Records exposed per month
    axes[0,1].plot(monthly_records.index, monthly_records.values, linewidth=2, color='#1fb6b6')
    axes[0,1].set_title('Records Exposed per Month')
    axes[0,1].set_ylabel('Records Exposed')
    axes[0,1].grid(True, alpha=0.3)
    
    # Yearly trends
    yearly_breaches = df.groupby('year').size()
    axes[1,0].bar(yearly_breaches.index, yearly_breaches.values, color='#ffb86b', alpha=0.8)
    axes[1,0].set_title('Breaches by Year')
    axes[1,0].set_xlabel('Year')
    axes[1,0].set_ylabel('Number of Breaches')
    
    # Quarterly patterns
    quarterly_breaches = df.groupby('quarter').size()
    axes[1,1].pie(quarterly_breaches.values, labels=[f'Q{q}' for q in quarterly_breaches.index], 
                  autopct='%1.1f%%', colors=['#0b2948', '#1fb6b6', '#ffb86b', '#28a745'])
    axes[1,1].set_title('Breach Distribution by Quarter')
    
    plt.tight_layout()
    plt.show()
    
    # Seasonal decomposition
    if len(monthly_breaches) >= 24:  # Need at least 2 years for decomposition
        decomposition = seasonal_decompose(monthly_breaches, model='additive', period=12)
        
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        fig.suptitle('Seasonal Decomposition of Breach Frequency', fontsize=16, fontweight='bold')
        
        decomposition.observed.plot(ax=axes[0], color='#0b2948', linewidth=2)
        axes[0].set_title('Original Time Series')
        axes[0].set_ylabel('Breaches')
        
        decomposition.trend.plot(ax=axes[1], color='#1fb6b6', linewidth=2)
        axes[1].set_title('Trend Component')
        axes[1].set_ylabel('Trend')
        
        decomposition.seasonal.plot(ax=axes[2], color='#ffb86b', linewidth=2)
        axes[2].set_title('Seasonal Component')
        axes[2].set_ylabel('Seasonal')
        
        decomposition.resid.plot(ax=axes[3], color='#dc3545', linewidth=2)
        axes[3].set_title('Residual Component')
        axes[3].set_ylabel('Residual')
        
        plt.tight_layout()
        plt.show()
        
        # Stationarity test
        adf_result = adfuller(monthly_breaches.dropna())
        print(f"\n📊 Augmented Dickey-Fuller Test:")
        print(f"• ADF Statistic: {adf_result[0]:.4f}")
        print(f"• p-value: {adf_result[1]:.4f}")
        print(f"• Critical Values: {adf_result[4]}")
        print(f"• Stationary: {'Yes' if adf_result[1] < 0.05 else 'No'}")

def clustering_analysis(df):
    """Perform clustering analysis for breach pattern identification."""
    print("\n🔍 Performing clustering analysis...")
    
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    
    # Prepare features for clustering
    features = df[['records_exposed', 'year', 'month', 'quarter']].copy()
    
    # Add categorical features as dummy variables
    industry_dummies = pd.get_dummies(df['industry'], prefix='industry')
    country_dummies = pd.get_dummies(df['country'], prefix='country')
    type_dummies = pd.get_dummies(df['breach_type'], prefix='type')
    
    # Combine all features
    clustering_features = pd.concat([features, industry_dummies, country_dummies, type_dummies], axis=1)
    
    # Standardize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(clustering_features)
    
    print(f"🔍 Clustering features prepared: {scaled_features.shape[1]} dimensions")
    
    # Determine optimal number of clusters
    k_range = range(2, 11)
    inertias = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_features)
        
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(scaled_features, cluster_labels))
    
    # Plot elbow curve and silhouette scores
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
    axes[0].set_title('Elbow Method for Optimal K')
    axes[0].set_xlabel('Number of Clusters (k)')
    axes[0].set_ylabel('Inertia')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(k_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
    axes[1].set_title('Silhouette Score vs Number of Clusters')
    axes[1].set_xlabel('Number of Clusters (k)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Find optimal k
    optimal_k = k_range[np.argmax(silhouette_scores)]
    print(f"🎯 Optimal number of clusters: {optimal_k} (silhouette score: {max(silhouette_scores):.3f})")
    
    # Perform K-means clustering with optimal k
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_features)
    df['cluster'] = cluster_labels
    
    # PCA for visualization
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(scaled_features)
    
    # Plot clusters
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(pca_features[:, 0], pca_features[:, 1], c=cluster_labels, 
                         cmap='viridis', alpha=0.7, s=50)
    plt.title('Breach Clusters (PCA Visualization)', fontsize=16, fontweight='bold')
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
    plt.colorbar(scatter, label='Cluster')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f"📊 PCA explained variance: {pca.explained_variance_ratio_.sum():.1%}")
    
    # Analyze cluster characteristics
    cluster_analysis = df.groupby('cluster').agg({
        'records_exposed': ['count', 'mean', 'median', 'std'],
        'industry': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
        'breach_type': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown',
        'country': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'
    }).round(0)
    
    cluster_analysis.columns = ['Count', 'Avg_Records', 'Median_Records', 'Std_Records', 
                               'Top_Industry', 'Top_Type', 'Top_Country']
    
    print("\n🔍 Cluster Analysis:")
    print(cluster_analysis)
    
    return optimal_k

def predictive_modeling(df):
    """Perform predictive modeling for breach risk assessment."""
    print("\n🤖 Performing predictive modeling...")
    
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, roc_auc_score, roc_curve
    from sklearn.preprocessing import LabelEncoder
    
    # Create target variable: Large breach (>1M records)
    df['is_large_breach'] = (df['records_exposed'] >= 1000000).astype(int)
    
    # Prepare features for modeling
    feature_columns = ['year', 'month', 'quarter']
    X_categorical = df[['industry', 'country', 'breach_type']].copy()
    
    # Encode categorical variables
    le_industry = LabelEncoder()
    le_country = LabelEncoder()
    le_type = LabelEncoder()
    
    X_categorical['industry_encoded'] = le_industry.fit_transform(df['industry'])
    X_categorical['country_encoded'] = le_country.fit_transform(df['country'])
    X_categorical['type_encoded'] = le_type.fit_transform(df['breach_type'])
    
    # Combine features
    X = pd.concat([df[feature_columns], X_categorical[['industry_encoded', 'country_encoded', 'type_encoded']]], axis=1)
    y = df['is_large_breach']
    
    print(f"🎯 Target variable distribution:")
    print(f"• Large breaches: {y.sum()} ({y.mean()*100:.1f}%)")
    print(f"• Small/Medium breaches: {(1-y).sum()} ({(1-y).mean()*100:.1f}%)")
    print(f"• Features: {X.shape[1]}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train multiple models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    results = {}
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        results[name] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'auc': auc_score
        }
        
        print(f"\n📊 {name} Results:")
        print(f"• AUC Score: {auc_score:.3f}")
        print(f"• Classification Report:")
        print(classification_report(y_test, y_pred))
    
    # Plot ROC curves
    plt.figure(figsize=(10, 8))
    
    for name, result in results.items():
        fpr, tpr, _ = roc_curve(y_test, result['probabilities'])
        plt.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {result["auc"]:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - Large Breach Prediction', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Feature importance (Random Forest)
    rf_model = results['Random Forest']['model']
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance, x='importance', y='feature', palette='viridis')
    plt.title('Feature Importance - Random Forest Model', fontsize=16, fontweight='bold')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()
    
    return results

def statistical_analysis(df):
    """Perform statistical analysis and hypothesis testing."""
    print("\n🔬 Performing statistical analysis...")
    
    from scipy import stats
    from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
    
    # Hypothesis 1: Different industries have different breach sizes
    print("🔬 Hypothesis Testing Results:")
    print("\n1. Industry vs Breach Size (Kruskal-Wallis Test):")
    
    industry_groups = [group['records_exposed'].values for name, group in df.groupby('industry')]
    h_stat, p_value = kruskal(*industry_groups)
    print(f"• H-statistic: {h_stat:.4f}")
    print(f"• p-value: {p_value:.4f}")
    print(f"• Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'} between industries")
    
    # Hypothesis 2: Different breach types have different impact
    print("\n2. Breach Type vs Impact (Kruskal-Wallis Test):")
    
    type_groups = [group['records_exposed'].values for name, group in df.groupby('breach_type')]
    h_stat, p_value = kruskal(*type_groups)
    print(f"• H-statistic: {h_stat:.4f}")
    print(f"• p-value: {p_value:.4f}")
    print(f"• Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'} between breach types")
    
    # Hypothesis 3: Recent years have larger breaches
    print("\n3. Recent Years vs Breach Size (Mann-Whitney U Test):")
    
    recent_breaches = df[df['year'] >= 2022]['records_exposed']
    older_breaches = df[df['year'] < 2022]['records_exposed']
    
    u_stat, p_value = mannwhitneyu(recent_breaches, older_breaches, alternative='two-sided')
    print(f"• U-statistic: {u_stat:.4f}")
    print(f"• p-value: {p_value:.4f}")
    print(f"• Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'} between recent and older breaches")
    
    # Correlation analysis
    correlation_data = df[['records_exposed', 'year', 'month', 'quarter']].copy()
    
    # Add encoded categorical variables
    from sklearn.preprocessing import LabelEncoder
    le_industry = LabelEncoder()
    le_country = LabelEncoder()
    le_type = LabelEncoder()
    
    correlation_data['industry_encoded'] = le_industry.fit_transform(df['industry'])
    correlation_data['country_encoded'] = le_country.fit_transform(df['country'])
    correlation_data['type_encoded'] = le_type.fit_transform(df['breach_type'])
    
    # Calculate correlation matrix
    correlation_matrix = correlation_data.corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix - Breach Characteristics', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Key Correlations:")
    print(f"• Records vs Year: {correlation_matrix.loc['records_exposed', 'year']:.3f}")
    print(f"• Records vs Industry: {correlation_matrix.loc['records_exposed', 'industry_encoded']:.3f}")
    print(f"• Records vs Type: {correlation_matrix.loc['records_exposed', 'type_encoded']:.3f}")

def generate_insights(df, optimal_k, results):
    """Generate key insights and recommendations."""
    print("\n🎯 KEY INSIGHTS FROM ADVANCED ANALYSIS:")
    print("=" * 50)
    
    # Time series insights
    yearly_trend = df.groupby('year').size()
    trend_direction = "increasing" if yearly_trend.iloc[-1] > yearly_trend.iloc[0] else "decreasing"
    print(f"\n📈 TEMPORAL TRENDS:")
    print(f"• Breach frequency is {trend_direction} over time")
    print(f"• Peak year: {yearly_trend.idxmax()} with {yearly_trend.max()} breaches")
    print(f"• Recent trend: {yearly_trend.iloc[-2:].mean():.1f} breaches per year (last 2 years)")
    
    # Clustering insights
    cluster_summary = df.groupby('cluster').agg({
        'records_exposed': ['count', 'mean'],
        'industry': lambda x: x.mode().iloc[0]
    }).round(0)
    
    print(f"\n🔍 CLUSTERING INSIGHTS:")
    print(f"• Identified {optimal_k} distinct breach patterns")
    print(f"• Cluster characteristics:")
    for cluster_id in range(optimal_k):
        cluster_data = df[df['cluster'] == cluster_id]
        top_industry = cluster_data['industry'].mode().iloc[0]
        avg_size = cluster_data['records_exposed'].mean()
        print(f"  - Cluster {cluster_id}: {len(cluster_data)} breaches, avg {avg_size:,.0f} records, top industry: {top_industry}")
    
    # Predictive model insights
    best_model = max(results.items(), key=lambda x: x[1]['auc'])
    print(f"\n🤖 PREDICTIVE MODELING:")
    print(f"• Best performing model: {best_model[0]} (AUC: {best_model[1]['auc']:.3f})")
    print(f"• Model can predict large breaches with {best_model[1]['auc']*100:.1f}% accuracy")
    
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"1. Focus on high-risk industries identified in clustering analysis")
    print(f"2. Implement predictive monitoring based on {best_model[0]} model")
    print(f"3. Develop industry-specific security frameworks")
    print(f"4. Enhance threat detection for identified breach patterns")
    print(f"5. Regular model retraining with new breach data")

def main():
    """Main function to run all analyses."""
    print("🚀 Starting Data Breach Insights Advanced Analysis")
    print("=" * 60)
    
    # Load and explore data
    df = load_and_explore_data()
    
    # Time series analysis
    time_series_analysis(df)
    
    # Clustering analysis
    optimal_k = clustering_analysis(df)
    
    # Predictive modeling
    results = predictive_modeling(df)
    
    # Statistical analysis
    statistical_analysis(df)
    
    # Generate insights
    generate_insights(df, optimal_k, results)
    
    print(f"\n✅ Analysis completed successfully!")
    print(f"📊 Processed {len(df)} breach records")
    print(f"🔍 Identified {optimal_k} breach patterns")
    print(f"🤖 Best model: {max(results.items(), key=lambda x: x[1]['auc'])[0]}")
    print(f"📅 Analysis completed on {datetime.now().strftime('%B %d, %Y at %H:%M')}")

if __name__ == "__main__":
    main()
