# Data Breach Insights Report - Windows Setup Script
# This script sets up the React dashboard for development on Windows

Write-Host "🚀 Setting up Data Breach Insights Report Dashboard..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node -v
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 16+ and try again." -ForegroundColor Red
    exit 1
}

# Check Node.js version
$version = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
if ($version -lt 16) {
    Write-Host "❌ Node.js version 16+ is required. Current version: $nodeVersion" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green

# Create public/data directory if it doesn't exist
if (!(Test-Path "public/data")) {
    Write-Host "📁 Creating public/data directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "public/data" -Force
}

# Copy sample data if it exists
if (Test-Path "data/sample_breaches.csv") {
    Write-Host "📄 Copying sample data to public directory..." -ForegroundColor Yellow
    Copy-Item "data/sample_breaches.csv" "public/data/"
    Write-Host "✅ Sample data copied to public/data/" -ForegroundColor Green
} else {
    Write-Host "⚠️  Sample data not found. The app will generate sample data automatically." -ForegroundColor Yellow
}

# Run linting
Write-Host "🔍 Running code quality checks..." -ForegroundColor Yellow
npm run lint

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Linting issues found. Run 'npm run lint:fix' to fix them." -ForegroundColor Yellow
}

# Format code
Write-Host "🎨 Formatting code..." -ForegroundColor Yellow
npm run format

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "1. Run 'npm run dev' to start the development server" -ForegroundColor White
Write-Host "2. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host "3. Explore the dashboard features" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "- README.md - Complete project documentation" -ForegroundColor White
Write-Host "- docs/architecture.md - System architecture" -ForegroundColor White
Write-Host "- docs/demo_script.md - 3-minute demo guide" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Ready to showcase your data analytics skills!" -ForegroundColor Green

