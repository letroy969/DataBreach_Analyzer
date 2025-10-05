# 🛡️ Data Breach Insights Report

A comprehensive analytics dashboard for cybersecurity breach data analysis, built with Streamlit.

## 🚀 Features

- **📊 Interactive Data Visualizations** - Real-time charts and graphs
- **🔍 Advanced Filtering** - Filter by date, industry, country, and more
- **📈 Trend Analysis** - Yearly trends and breach patterns
- **🏢 Company Insights** - Top companies by breach impact
- **🌍 Geographic Analysis** - Country-wise breach distribution
- **📋 Data Export** - Download reports in CSV and Excel formats
- **🤖 AI-Powered Insights** - Intelligent analysis and recommendations

## 📁 Project Structure

```
data-breach-insights/
├── app/
│   ├── app.py              # Main Streamlit application
│   ├── data_loader.py      # Data loading and processing
│   ├── visuals.py          # Chart configurations
│   ├── ai_insights.py      # AI-powered insights
│   └── requirements.txt    # App dependencies
├── data/
│   └── sample_breaches.csv # Sample breach data
├── powerbi/
│   └── breaches_for_powerbi.csv # PowerBI formatted data
├── requirements.txt        # Main dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
└── README.md              # This file
```

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app/app.py
   ```

## 📊 Data Sources

The dashboard supports multiple data sources:
- CSV files with breach data
- Excel files (.xlsx, .xls)
- JSON files
- Parquet files
- SQLite databases

## 🎨 Features

### Data Upload
- Drag and drop file upload
- Support for multiple file formats
- Automatic column mapping
- Data validation and cleaning

### Visualizations
- Interactive charts with Plotly
- Dark theme optimized for cybersecurity professionals
- Responsive design for all devices
- Export capabilities for presentations

### Analytics
- Yearly breach trends
- Industry breakdown analysis
- Geographic distribution
- Cost impact calculations
- AI-generated insights

## 🌐 Deployment

This application is designed to be deployed on Streamlit Cloud:

1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Configure the app path as `app/app.py`
4. Deploy!

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue in the GitHub repository.