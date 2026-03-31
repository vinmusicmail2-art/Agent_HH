@echo off
title Agent HH - Setup

echo.
echo === Agent HH Setup ===
echo.

echo [1/2] Installing Python libraries...
cd /d "%~dp0backend"
pip install fastapi uvicorn httpx
if errorlevel 1 (
  echo ERROR: pip failed. Make sure Python is installed.
  pause
  exit /b 1
)
echo Done!

echo.
echo [2/2] Installing Electron...
cd /d "%~dp0frontend"
npm install
if errorlevel 1 (
  echo ERROR: npm failed. Install Node.js from https://nodejs.org
  pause
  exit /b 1
)
echo Done!

echo.
echo === Setup complete! Run "Agent HH.bat" to start ===
echo.
pause
