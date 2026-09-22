@echo off
title CODE COMBAT Pro - LAN / College Lab Server
cd /d "%~dp0"
echo ======================================================================
echo    CODE COMBAT Pro - Multi-Client LAN Server for College Labs
echo ======================================================================
echo.
echo [*] Starting server on 0.0.0.0 (Accepting LAN / Wi-Fi connections)...
echo.
python -u main.py --lan
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python was not found or encountered an error.
    echo Make sure Python 3.8+ is installed and added to PATH.
    pause
)
