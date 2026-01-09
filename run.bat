@echo off
echo ========================================
echo   PCBuild Assist - Starting Application
echo ========================================
echo.

REM Check if Python virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at .venv
    echo Please create it first: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/4] Activating Python virtual environment...
call .venv\Scripts\activate.bat

REM Check if backend dependencies are installed
echo [2/4] Checking backend dependencies...
cd backend
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

REM Start backend in a new window
echo [3/4] Starting backend server (FastAPI)...
start "PCBuild Backend - FastAPI" cmd /k "cd /d %~dp0 && call .venv\Scripts\activate.bat && cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo [4/4] Starting frontend server (Vite)...
cd ..\frontend
start "PCBuild Frontend - Vite" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:5000/docs
echo.
echo Press any key to open the frontend in your browser...
pause >nul

REM Open frontend in default browser
start http://localhost:5173

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
