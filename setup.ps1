# MedCall Quick Start Script for Windows
# This script sets up and runs both backend and frontend

Write-Host "🏥 MedCall - Quick Start" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 16 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Setup Backend
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Gray
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python packages..." -ForegroundColor Gray
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Gray
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit backend\.env and add your OpenAI API key" -ForegroundColor Yellow
}

Set-Location ..

# Setup Frontend
Write-Host ""
Write-Host "📦 Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm packages..." -ForegroundColor Gray
    npm install
}

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Gray
    Copy-Item .env.example .env
}

Set-Location ..

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your OpenAI API key to backend\.env" -ForegroundColor White
Write-Host "2. Open a terminal in 'frontend' directory and run: npm start" -ForegroundColor White
Write-Host "3. Open another terminal in 'backend' directory and run:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Happy hacking!" -ForegroundColor Green
