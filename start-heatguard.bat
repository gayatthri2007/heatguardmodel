@echo off
REM HeatGuard Startup Script for Windows Command Prompt

setlocal enabledelayedexpansion

echo.
echo ======================================
echo HeatGuard - Complete System Startup
echo ======================================
echo.

REM Check Node.js
echo Checking Node.js and npm...
node --version >nul 2>&1
if errorlevel 1 (
    echo X Node.js or npm not found!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
for /f "delims=" %%i in ('node --version') do set NODE_VERSION=%%i
echo + Node.js %NODE_VERSION% found
node_modules\.bin\npm --version >nul 2>&1
if errorlevel 1 (
    echo X npm not found!
) else (
    for /f "delims=" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo + npm %NPM_VERSION% found
)

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
for /f "delims=" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo + %PYTHON_VERSION% found

echo.
echo Checking frontend dependencies...
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo + Frontend dependencies installed
) else (
    echo + Frontend dependencies already installed
)

echo.
echo ======================================
echo Starting HeatGuard System
echo ======================================
echo.

REM Start Backend in new window
echo Starting Backend (Flask Server)...
echo Backend will run on http://localhost:5000
start "HeatGuard Backend" cmd /k "cd backend && python app.py"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in new window
echo Starting Frontend (React + Vite)...
echo Frontend will run on http://localhost:5173
start "HeatGuard Frontend" cmd /k "cd frontend && npm run dev"

REM Wait a bit
timeout /t 5 /nobreak

echo.
echo ======================================
echo + HeatGuard System Started!
echo ======================================
echo.
echo Access points:
echo   Frontend:     http://localhost:5173
echo   Backend API:  http://localhost:5000/api
echo   Model Test:   http://localhost:5000/model-test
echo   Health Check: http://localhost:5000/api/health
echo.
echo Test Accounts:
echo   Worker:      worker1 / password123
echo   Supervisor:  supervisor1 / admin123
echo.
echo Opening browser...
timeout /t 3 /nobreak
start http://localhost:5173

echo.
echo Press Ctrl+C in either terminal to stop the service
echo.
pause
