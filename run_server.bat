@echo off
setlocal

:: Determine the directory of this batch file (root of country_finder)
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

echo ===================================================
echo     STARTING COUNTRY FINDER AI (SAAS EDITION)
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Install Dependencies (Quietly, only if needed)
echo [INFO] Checking dependencies...
pip install -r requirements.txt >nul 2>&1

:: Start Backend
echo [INFO] Launching Backend API (FastAPI)...
:: We run uvicorn on the module 'backend.main' from the root directory
start "CountryFinder API" cmd /k "python -m backend.main"

:: Start Frontend (Simple Python Server for Development)
echo [INFO] Launching Frontend Server...
start "CountryFinder Frontend" cmd /k "cd frontend && python -m http.server 3000"

echo.
echo [SUCCESS] System is running!
echo ---------------------------------------------------
echo  - API Docs:      http://localhost:8000/docs
echo  - Frontend App:  http://localhost:3000
echo ---------------------------------------------------
echo.
echo Press any key to stop servers...
pause >nul

taskkill /F /IM python.exe >nul 2>&1
echo [INFO] Servers stopped.
