#!/bin/bash

# Data Breach Insights Report - Setup Script
# This script sets up the React dashboard for development

echo "🚀 Setting up Data Breach Insights Report Dashboard..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create public/data directory if it doesn't exist
if [ ! -d "public/data" ]; then
    echo "📁 Creating public/data directory..."
    mkdir -p public/data
fi

# Copy sample data if it exists
if [ -f "data/sample_breaches.csv" ]; then
    echo "📄 Copying sample data to public directory..."
    cp data/sample_breaches.csv public/data/
    echo "✅ Sample data copied to public/data/"
else
    echo "⚠️  Sample data not found. The app will generate sample data automatically."
fi

# Run linting
echo "🔍 Running code quality checks..."
npm run lint

if [ $? -ne 0 ]; then
    echo "⚠️  Linting issues found. Run 'npm run lint:fix' to fix them."
fi

# Format code
echo "🎨 Formatting code..."
npm run format

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Run 'npm run dev' to start the development server"
echo "2. Open http://localhost:3000 in your browser"
echo "3. Explore the dashboard features"
echo ""
echo "📚 Documentation:"
echo "- README.md - Complete project documentation"
echo "- docs/architecture.md - System architecture"
echo "- docs/demo_script.md - 3-minute demo guide"
echo ""
echo "🚀 Ready to showcase your data analytics skills!"

