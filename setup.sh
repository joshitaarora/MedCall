#!/bin/bash

# MedCall Quick Start Script
# This script sets up and runs both backend and frontend

echo "🏥 MedCall - Quick Start"
echo "========================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Setup Backend
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key"
fi

cd ..

# Setup Frontend
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Run 'npm start' in the frontend directory"
echo "3. Run 'python app.py' in the backend directory (with venv activated)"
echo ""
echo "🚀 Happy hacking!"
