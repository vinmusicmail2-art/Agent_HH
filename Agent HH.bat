@echo off
title Agent HH

echo Starting backend server...
start "HH Backend" /MIN cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Starting app...
cd /d "%~dp0frontend"
npx electron .

if errorlevel 1 (
  echo.
  echo ERROR: Could not start Electron.
  echo Run SETUP.bat first, then try again.
  pause
)
