@echo off
title EpiQual App Launcher
echo ===================================================
echo   EpiQual: Outbreak Qualitative Data Assistant
echo   Checking environment & background services...
echo ===================================================

:: 1. Force sync latest code from GitHub (overwrites uncommitted local blocks safely)
git fetch origin main >nul 2>&1
git reset --hard origin/main >nul 2>&1

:: 2. Auto-verify required Python dependencies are installed
python -m pip install --quiet streamlit openai python-docx pypdf faster-whisper

:: 3. Launch Ollama in the background if not already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo   [OK] Ollama Local AI Engine is active.
) else (
    echo   [STARTING] Launching Ollama Local AI Engine...
    start /B ollama serve
    timeout /t 3 >nul
)

echo.
echo   Launching EpiQual Dashboard...
echo ===================================================

:: 4. Run Streamlit App
python -m streamlit run app.py --client.toolbarMode=minimal

pause