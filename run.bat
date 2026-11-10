@echo off
REM ==============================================================================
REM Breast Cancer AI Diagnostic Platform - Universal Windows Runner
REM ==============================================================================
echo ======================================================================
echo  Breast Cancer AI Diagnostic Platform - Windows Launcher
echo ======================================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your Windows PATH.
    echo Please install Python 3.10 or 3.11 from https://www.python.org/
    pause
    exit /b 1
)

if not exist ".venv" (
    echo [*] Creating virtual environment in .venv...
    python -m venv .venv
    echo [*] Installing dependencies from requirements.txt...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

if not exist "sample_scans\benign_scan_01_fibroadenoma.png" (
    echo [*] Generating synthetic sample scans...
    python generate_sample_data.py
)

echo [*] Starting Streamlit dashboard on http://localhost:8501 ...
streamlit run app.py --server.port 8501
pause
