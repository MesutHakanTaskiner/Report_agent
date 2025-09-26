@echo off
setlocal enableextensions enabledelayedexpansion

REM === Stable project paths ===
set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "VENV=%BACKEND%\venv"
set "VENV_PY=%VENV%\Scripts\python.exe"
set "VENV_PIP=%VENV%\Scripts\pip.exe"

echo ===== Report Agent Setup and Startup =====
echo.

REM === Frontend deps (project root) ===
echo Checking for Node.js dependencies...
if exist "%ROOT%node_modules" (
    echo Frontend dependencies found.
) else (
    echo Installing frontend dependencies...
    pushd "%ROOT%"
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed. Aborting.
        popd
        exit /b 1
    )
    popd
    echo Frontend dependencies installed.
)

echo.

REM === Create venv if needed ===
echo Checking for Python virtual environment...
if exist "%VENV_PY%" (
    echo Virtual environment found.
) else (
    echo Creating virtual environment...
    call :FIND_PY311 PY_CMD
    if not defined PY_CMD (
        echo [WARN] Could not find Python 3.11 explicitly. Falling back to default 'python'.
        set "PY_CMD=python"
    )
    pushd "%BACKEND%"
    "%PY_CMD%" -m venv "venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Aborting.
        popd
        exit /b 1
    )
    popd
    echo Virtual environment created at: "%VENV%"
)

echo Virtual environment is ready.
echo.

REM === Install backend deps into the venv (no activation required) ===
echo Installing Python dependencies...
if not exist "%VENV_PY%" (
    echo [ERROR] venv Python not found at "%VENV_PY%". Aborting.
    exit /b 1
)
pushd "%BACKEND%"
"%VENV_PY%" -m pip --upgrade pip
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [WARN] requirements install reported issues; continuing to numpy/pandas pin.
)

echo Fixing numpy/pandas compatibility issue...
"%VENV_PY%" -m pip uninstall -y numpy pandas
"%VENV_PY%" -m pip install numpy==1.24.3
"%VENV_PY%" -m pip install pandas==2.1.1
if errorlevel 1 (
    echo [ERROR] Failed to install pinned numpy/pandas. Check your requirements & wheels.
)
popd
echo Fixed numpy/pandas compatibility issue.
echo.

REM === Start backend using the venv’s python directly (no activation) ===
echo Starting backend server...
start "" cmd /k ""%VENV_PY%" "%BACKEND%\run.py""
if errorlevel 1 (
    echo [ERROR] Failed to start backend window.
)

REM === Start frontend (project root) ===
echo Starting frontend server...
start "" cmd /k "cd /d "%ROOT%" && npm run dev"

echo.
echo Both servers are now running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: The backend is running with "%VENV_PY%".
goto :EOF

REM === Helper: find a usable Python 3.11 ===
:FIND_PY311
REM Tries (in order): a python.exe with 3.11 in its path, then py launcher 3.11, else empty
setlocal
set "FOUND="
for /f "tokens=* usebackq" %%P in (`where python 2^>nul ^| findstr /i "3.11.0"`) do (
    set "FOUND=%%P"
    goto :found
)

REM py launcher route
where py >nul 2>&1
if not errorlevel 1 (
    py -3.11 --version >nul 2>&1
    if not errorlevel 1 (
        set "FOUND=py -3.11"
    )
)

:found
endlocal & (
    if defined FOUND (set "%~1=%FOUND%") else (set "%~1=")
)
goto :EOF
