@echo off
title Launching EpiQual...
echo ===================================================
echo   EpiQual: Outbreak Qualitative Data Assistant
echo   Checking background services...
echo ===================================================

:: 1. Silently pull the latest bug fixes from GitHub
git fetch origin main && git reset --hard origin/main

:: 2. Check if Ollama service is running; if not, launch it silently in the background
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo.
    echo   [!] Starting Ollama Local AI Engine...
    start /B "" "ollama" serve >nul 2>&1
    timeout /t 3 /nobreak >nul
) else (
    echo   [OK] Ollama Local AI Engine is already active.
)

echo.
echo   Launching the App...
echo ===================================================

:: 3. Start the Streamlit app safely
call python -m streamlit run app.py --client.toolbarMode=minimal

:: 4. Keep window open if the app crashes so you can read the error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Something went wrong while launching EpiQual.
    echo Please make sure Python and required libraries are installed!
    echo.
    pause
)
