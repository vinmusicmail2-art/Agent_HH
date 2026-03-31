@echo off
title Agent HH — Установка
echo ========================================
echo   Agent HH — Установка зависимостей
echo ========================================
echo.

:: ── Python ──
echo [1/2] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден.
    echo Скачайте Python 3.9+ с https://python.org и повторите.
    pause
    exit /b 1
)
python --version
echo Установка Python-зависимостей...
cd /d "%~dp0backend"
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА при установке Python-зависимостей.
    pause
    exit /b 1
)
cd /d "%~dp0"

:: ── Node.js / Electron ──
echo.
echo [2/2] Проверка Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Node.js не найден.
    echo Скачайте Node.js с https://nodejs.org и повторите.
    pause
    exit /b 1
)
node --version
echo Установка Node-зависимостей (Electron)...
cd /d "%~dp0frontend"
npm install
if errorlevel 1 (
    echo ОШИБКА при установке Node-зависимостей.
    pause
    exit /b 1
)
cd /d "%~dp0"

echo.
echo ========================================
echo   Установка завершена успешно!
echo   Запустите ЗАПУСК.bat для старта.
echo ========================================
pause
