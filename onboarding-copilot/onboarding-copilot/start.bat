@echo off
REM ===============================================================
REM  Compass — one-click launcher for Windows
REM  Just double-click this file (or run it from cmd) to start.
REM  Requires: Python 3.10+ on PATH.
REM ===============================================================

setlocal
cd /d "%~dp0"

echo.
echo === Compass launcher ===
echo Working dir: %CD%
echo.

REM --- 1. Check Python is installed --------------------------------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not on PATH.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo and make sure "Add python.exe to PATH" is checked.
    pause
    exit /b 1
)

REM --- 2. Create venv if missing -----------------------------------
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Creating virtual environment in .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Virtual environment already exists.
)

REM --- 3. Activate venv --------------------------------------------
call ".venv\Scripts\activate.bat"

REM --- 4. Install / upgrade deps -----------------------------------
echo [2/3] Installing dependencies (this may take a minute on first run)...
python -m pip install --disable-pip-version-check --quiet -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed. See output above.
    pause
    exit /b 1
)

REM --- 5. Launch server --------------------------------------------
echo [3/3] Starting Compass on http://localhost:8000
echo.
echo Press Ctrl+C to stop.
echo.
python -m uvicorn app.main:app --reload --port 8000

REM Keep window open if uvicorn exited on its own (e.g. crash).
pause
endlocal
