@echo off
title CODE COMBAT Pro - Local Server
cd /d "%~dp0"
echo ======================================================================
echo    CODE COMBAT Pro - Offline Competitive Programming Platform
echo ======================================================================
echo.
echo [*] Starting Code Combat Pro server on http://127.0.0.1:8000 ...
echo [*] Opening default web browser automatically...
echo.
python -u main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python was not found or encountered an error.
    echo Make sure Python 3.8+ is installed and added to PATH.
    pause
)
