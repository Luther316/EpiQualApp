@echo off
title Launching EpiQual...
echo ===================================================
echo   EpiQual: Outbreak Qualitative Data Assistant
echo   Checking for updates from Teacher...
echo ===================================================

:: 1. Silently pull the latest bug fixes from your GitHub
git pull origin main

echo.
echo   Launching the App...
echo ===================================================

:: 2. Start the app
python -m streamlit run app.py --client.toolbarMode=hidden

pause