# Data Breach Insights Report - Streamlit Deployment Guide

This guide provides step-by-step instructions for deploying the professional Streamlit dashboard for the Data Breach Insights Report.

## 🚀 Quick Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Fork the Repository**
   - Go to your GitHub repository
   - Click "Fork" to create your own copy

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your forked repository
   - Set main file path to: `app/app.py`
   - Click "Deploy"

3. **Configure Environment Variables** (Optional)
   - Go to your app settings in Streamlit Cloud
   - Add `OPENAI_API_KEY` if you want AI-powered insights
   - Add `DATABASE_URL` if using external database

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/data-breach-insights.git
cd data-breach-insights

# Install dependencies
pip install -r app/requirements.txt

# Run the application
streamlit run app/app.py
```

### Option 3: Docker Deployment

```bash
# Build the Docker image
docker build -t breach-insights .

# Run the container
docker run -p 8501:8501 breach-insights
```

## 📊 Features Overview

### 🎯 Core Features
- **Interactive Dashboard**: Real-time filtering and visualization
- **Professional UI**: Dark blue/teal/orange theme matching project branding
- **AI Insights**: OpenAI-powered executive summaries and analysis
- **Data Export**: CSV download with filtered results
- **Responsive Design**: Works on desktop, tablet, and mobile

### 📈 Visualizations
- **Trend Analysis**: Line charts showing breach patterns over time
- **Industry Breakdown**: Bar charts and donut charts for sector analysis
- **Geographic Mapping**: Choropleth maps for country distribution
- **Cost Analysis**: Scatter plots showing cost vs records correlation
- **KPI Cards**: Key metrics with professional styling

### 🔍 Data Features
- **Advanced Filtering**: Year range, industry, country, breach type, company search
- **File Upload**: Upload your own CSV files
- **Data Export**: Download filtered results
- **Real-time Updates**: Charts update automatically with filter changes

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the `app/` directory:

```bash
# Optional: OpenAI API key for AI insights
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Database connection
DATABASE_URL=sqlite:///data.db

# Optional: Custom settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Data Sources

The application supports multiple data sources:

1. **CSV Files**: Place your data in `data/sample_breaches.csv`
2. **SQLite Database**: Use `data.db` in the project root
3. **File Upload**: Upload CSV files through the sidebar
4. **Sample Data**: Fallback sample data if no files found

### Required Data Format

Your CSV should have these columns:
```csv
id,breach_date,name,industry,country,records_exposed,breach_type,source_url
1,2022-04-03,Company A,Healthcare,US,1663419,Insider,https://example.com
```

## 🎨 Customization

### Color Scheme

Update colors in `app/visuals.py`:

```python
COLORS = {
    'primary': '#0b2948',      # Dark blue
    'secondary': '#1fb6b6',    # Teal
    'accent': '#ffb86b',       # Orange
    'background': '#f8fafc',   # Light gray
    'text': '#1e293b',         # Dark gray
}
```

### Adding New Charts

Create new chart functions in `app/visuals.py`:

```python
@staticmethod
def create_custom_chart(df: pd.DataFrame) -> go.Figure:
    # Your custom chart code
    fig = px.bar(df, x='column1', y='column2')
    return fig
```

### Adding New Filters

Add filters in `app/app.py`:

```python
# Add to sidebar
custom_filter = st.sidebar.selectbox(
    "Custom Filter",
    options=df['custom_column'].unique()
)
```

## 🚀 Production Deployment

### Streamlit Cloud Configuration

1. **Repository Settings**
   - Ensure `app/app.py` is the main file
   - Set Python version to 3.8+
   - Configure environment variables

2. **Performance Optimization**
   - Use `@st.cache_data` for expensive operations
   - Limit data size for better performance
   - Use pagination for large datasets

3. **Security**
   - Set `OPENAI_API_KEY` as secret
   - Use HTTPS for production
   - Implement authentication if needed

### Docker Production

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .
COPY data/ ./data/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

Build and deploy:

```bash
# Build image
docker build -t breach-insights:latest .

# Run container
docker run -d \
  --name breach-insights \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  breach-insights:latest
```

## 📊 Monitoring and Maintenance

### Health Checks

```bash
# Check if app is running
curl http://localhost:8501/_stcore/health

# Check logs
docker logs breach-insights
```

### Performance Monitoring

- Monitor memory usage
- Check response times
- Monitor error rates
- Track user engagement

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

## 🔧 Troubleshooting

### Common Issues

1. **App won't start**
   - Check Python version (3.8+)
   - Verify all dependencies installed
   - Check file paths

2. **Charts not displaying**
   - Ensure Plotly is installed
   - Check browser console for errors
   - Verify data format

3. **AI insights not working**
   - Verify OpenAI API key
   - Check API key permissions
   - Ensure internet connection

4. **Performance issues**
   - Reduce dataset size
   - Use caching
   - Check system resources

### Debug Mode

```bash
# Run with debug logging
streamlit run app/app.py --logger.level debug

# Check logs
tail -f ~/.streamlit/logs/streamlit.log
```

## 📈 Analytics and Usage

### Streamlit Cloud Analytics

- View app usage statistics
- Monitor performance metrics
- Track user engagement
- Analyze error rates

### Custom Analytics

Add tracking to your app:

```python
import streamlit as st

# Track page views
st.analytics.track("page_view", {"page": "dashboard"})

# Track user interactions
st.analytics.track("filter_applied", {"filter_type": "industry"})
```

## 🎯 Best Practices

### Code Organization
- Keep modules separate and focused
- Use type hints for better code quality
- Implement proper error handling
- Add comprehensive documentation

### Performance
- Use `@st.cache_data` for expensive operations
- Limit data size for better performance
- Implement lazy loading for large datasets
- Use pagination for tables

### Security
- Never commit API keys
- Use environment variables for secrets
- Implement proper authentication
- Validate user inputs

### User Experience
- Provide clear error messages
- Use loading indicators
- Implement responsive design
- Add helpful tooltips

## 📞 Support

- **Documentation**: [Streamlit Docs](https://docs.streamlit.io)
- **Community**: [Streamlit Forum](https://discuss.streamlit.io)
- **GitHub**: [Repository Issues](https://github.com/yourusername/data-breach-insights/issues)
- **Email**: lindaletroy27@gmail.com

---

**Built with ❤️ by Sihle Dladla**  
_ICT Diploma Student | University of Mpumalanga_

