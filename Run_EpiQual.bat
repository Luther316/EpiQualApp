@echo off
title Launching EpiQual...
echo ===================================================
echo   EpiQual: Outbreak Qualitative Data Assistant
echo   Checking for updates from Teacher...
echo ===================================================

:: 1. Silently pull the latest bug fixes from GitHub
git pull origin main

echo.
echo   Launching the App...
echo ===================================================

:: 2. Start the app safely and hide developer tools
call python -m streamlit run app.py --client.toolbarMode=hidden

:: 3. Keep window open if the app crashes so students can see the error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Something went wrong while launching EpiQual. 
    echo Please make sure Python is installed and requirements.txt was run!
    echo.
    pause
)