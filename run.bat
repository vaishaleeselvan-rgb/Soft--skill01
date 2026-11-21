@echo off
title Campus Opportunity Verification Portal
echo ========================================================
echo   Starting Campus Opportunity Verification Portal
echo ========================================================
echo.
cd /d "%~dp0"
echo Starting the web server and opening your browser...
echo.
".venv\Scripts\python.exe" app.py
pause
