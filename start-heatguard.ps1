# HeatGuard Startup Script for Windows PowerShell
# Starts backend and frontend in separate terminals

$ErrorActionPreference = "Continue"

Write-Host "======================================"
Write-Host "HeatGuard - Complete System Startup"
Write-Host "======================================"
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Function to test if command exists
function Test-CommandExists {
    param($cmd)
    try {
        $null = where.exe $cmd 2>$null
        return $?
    }
    catch {
        return $false
    }
}

# Check Node.js
Write-Host "Checking Node.js and npm..." -ForegroundColor Yellow
if (Test-CommandExists "node.exe") {
    try {
        $nodeVersion = node -v
        $npmVersion = npm -v
        Write-Host " - Node.js $nodeVersion found" -ForegroundColor Green
        Write-Host " - npm $npmVersion found" -ForegroundColor Green
    }
    catch {
        Write-Host " - Node.js found but version check failed" -ForegroundColor Yellow
    }
} else {
    Write-Host " - Node.js or npm NOT FOUND!" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
if (Test-CommandExists "python.exe") {
    try {
        $pythonVersion = python --version
        Write-Host " - $pythonVersion found" -ForegroundColor Green
    }
    catch {
        Write-Host " - Python found but version check failed" -ForegroundColor Yellow
    }
} else {
    Write-Host " - Python NOT FOUND!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check frontend dependencies
Write-Host "Checking frontend dependencies..." -ForegroundColor Yellow
$nodeModulesPath = $scriptDir + "\frontend\node_modules"
if (-Not (Test-Path $nodeModulesPath)) {
    Write-Host " - Installing npm packages (first time only)..." -ForegroundColor Gray
    $frontendPath = $scriptDir + "\frontend"
    Push-Location $frontendPath
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host " - npm install failed!" -ForegroundColor Red
        Pop-Location
        Read-Host "Press Enter to exit"
        exit 1
    }
    Pop-Location
    Write-Host " - Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host " - Frontend dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================"
Write-Host "Starting HeatGuard System"
Write-Host "======================================"
Write-Host ""

# Start Backend
Write-Host "Starting Backend (Flask)..." -ForegroundColor Yellow
$backendPath = $scriptDir + "\backend"
$backendCmd = "cd `"$backendPath`"; python app.py"
Start-Process PowerShell -ArgumentList @("-NoExit", "-Command", $backendCmd)

# Wait for backend
Write-Host "Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 4

# Start Frontend
Write-Host "Starting Frontend (React)..." -ForegroundColor Yellow
$frontendPath = $scriptDir + "\frontend"
$frontendCmd = "cd `"$frontendPath`"; npm run dev"
Start-Process PowerShell -ArgumentList @("-NoExit", "-Command", $frontendCmd)

Write-Host ""
Write-Host "======================================"
Write-Host "HeatGuard System Started!"
Write-Host "======================================"
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Cyan
Write-Host "  Frontend:     http://localhost:5173" -ForegroundColor White
Write-Host "  Backend API:  http://localhost:5000/api" -ForegroundColor White
Write-Host ""
Write-Host "Test Accounts:" -ForegroundColor Cyan
Write-Host "  worker1 / password123" -ForegroundColor White
Write-Host "  supervisor1 / admin123" -ForegroundColor White
Write-Host ""

# Try to open browser
Start-Sleep -Seconds 2
try {
    Start-Process "http://localhost:5173" -ErrorAction SilentlyContinue
    Write-Host "Browser opened to http://localhost:5173" -ForegroundColor Green
}
catch {
    Write-Host "Please visit http://localhost:5173 manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete!"
