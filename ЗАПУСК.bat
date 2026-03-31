@echo off
title Agent HH
echo ========================================
echo   Agent HH — Запуск
echo ========================================
echo.

:: Запуск бэкенда в фоне
echo Запуск сервера API...
start "HH Backend" /MIN cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

:: Пауза для инициализации сервера
echo Ожидание запуска сервера...
timeout /t 3 /nobreak >nul

:: Запуск Electron
echo Запуск приложения...
cd /d "%~dp0frontend"
npx electron .

:: Если Electron закрыт — завершаем бэкенд
echo.
echo Приложение закрыто. Остановка сервера...
taskkill /FI "WINDOWTITLE eq HH Backend" /F >nul 2>&1
cd /d "%~dp0"
