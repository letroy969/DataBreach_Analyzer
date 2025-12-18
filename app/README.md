# Data Breach Insights Report - Streamlit Dashboard

Professional enterprise data analytics dashboard for breach insights analysis. Features interactive visualizations, AI-powered insights, and comprehensive filtering.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/data-breach-insights.git
   cd data-breach-insights
   ```

2. **Install dependencies**
   ```bash
   pip install -r app/requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app/app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📊 Features

### Interactive Dashboard
- **KPI Cards**: Total breaches, records exposed, average cost, top industry
- **Interactive Charts**: Trends, industry breakdown, country maps, cost analysis
- **Advanced Filtering**: Year range, industry, country, breach type, company search
- **Data Export**: CSV download with filtered results

### AI-Powered Insights
- **Executive Summary**: C-level insights and recommendations
- **Industry Analysis**: Sector-specific risk patterns
- **Trend Analysis**: Historical patterns and predictions
- **Risk Assessment**: Comprehensive risk evaluation

### Professional UI
- **Dark Blue/Teal/Orange Theme**: Consistent with project branding
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, animations, tooltips
- **Export Options**: CSV download, data sharing

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the app directory:

```bash
# Optional: OpenAI API key for AI insights
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Database connection
DATABASE_URL=sqlite:///data.db
```

### Data Sources

The application supports multiple data sources:

1. **CSV Files**: Place your data in `data/sample_breaches.csv`
2. **SQLite Database**: Use `data.db` in the project root
3. **File Upload**: Upload CSV files through the sidebar
4. **Sample Data**: Fallback sample data if no files found

### Data Format

Your CSV should have these columns:
- `id`: Unique identifier
- `breach_date`: Date of breach (YYYY-MM-DD)
- `name`: Company name
- `industry`: Industry sector
- `country`: Country code (e.g., US, CA, GB)
- `records_exposed`: Number of records exposed
- `breach_type`: Type of breach
- `source_url`: Source URL (optional)

## 🚀 Deployment

### Streamlit Cloud

1. **Fork the repository** on GitHub
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your forked repository
   - Set main file path to `app/app.py`
   - Click "Deploy"

3. **Configure environment variables** in Streamlit Cloud:
   - Go to app settings
   - Add `OPENAI_API_KEY` if using AI features

### Local Deployment

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run locally
streamlit run app/app.py

# Run with custom port
streamlit run app/app.py --server.port 8502
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .
COPY data/ ./data/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t breach-insights .
docker run -p 8501:8501 breach-insights
```

## 📈 Usage

### Basic Usage

1. **Load Data**: The app automatically loads data from `data/sample_breaches.csv`
2. **Apply Filters**: Use the sidebar to filter by year, industry, country, etc.
3. **View Charts**: Interactive visualizations update based on filters
4. **Export Data**: Download filtered results as CSV

### Advanced Features

1. **AI Insights**: Enable OpenAI API key for AI-powered summaries
2. **File Upload**: Upload your own CSV files through the sidebar
3. **Custom Filtering**: Combine multiple filters for precise analysis
4. **Data Export**: Download top companies or full dataset

### Keyboard Shortcuts

- `r`: Refresh data
- `f`: Focus on filters
- `e`: Export data
- `h`: Show help

## 🔧 Customization

### Styling

Modify the CSS in `app.py` to change colors, fonts, and layout:

```python
# Update color scheme
COLORS = {
    'primary': '#your-color',
    'secondary': '#your-color',
    'accent': '#your-color'
}
```

### Adding Charts

Create new chart functions in `visuals.py`:

```python
@staticmethod
def create_custom_chart(df: pd.DataFrame) -> go.Figure:
    # Your custom chart code
    pass
```

### Adding Filters

Add new filters in `app.py`:

```python
# Add to sidebar
custom_filter = st.sidebar.selectbox(
    "Custom Filter",
    options=df['custom_column'].unique()
)
```

## 🐛 Troubleshooting

### Common Issues

1. **No data loading**:
   - Check if `data/sample_breaches.csv` exists
   - Verify CSV format matches requirements
   - Check file permissions

2. **Charts not displaying**:
   - Ensure Plotly is installed: `pip install plotly`
   - Check browser console for errors
   - Try refreshing the page

3. **AI insights not working**:
   - Verify OpenAI API key is set
   - Check API key permissions
   - Ensure internet connection

4. **Performance issues**:
   - Reduce dataset size for testing
   - Use caching for large datasets
   - Check system resources

### Debug Mode

Run with debug information:

```bash
streamlit run app/app.py --logger.level debug
```

### Logs

Check Streamlit logs for errors:

```bash
# View logs
streamlit run app/app.py --server.headless true
```

## 📚 API Reference

### DataLoader Class

```python
# Load data
df = data_loader.load_data(source='csv')

# Apply filters
filtered_df = data_loader.get_filtered_data(df, filters)

# Get KPIs
kpis = data_loader.get_kpi_metrics(df)
```

### ChartBuilder Class

```python
# Create charts
trends_chart = chart_builder.create_trends_chart(df)
industry_chart = chart_builder.create_industry_chart(df)
```

### AIInsights Class

```python
# Generate insights
summary = ai_insights.generate_executive_summary(df, kpis)
industry_insights = ai_insights.generate_industry_insights(df)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Email**: lindaletroy27@gmail.com
- **LinkedIn**: [Sihle Dladla](https://linkedin.com/in/sihle-dladla)
- **GitHub**: [Repository Issues](https://github.com/yourusername/data-breach-insights/issues)

---

**Built with ❤️ by Sihle Dladla**  
_ICT Diploma Student | University of Mpumalanga_




