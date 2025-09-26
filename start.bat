@echo off
setlocal
set "EXIT_CODE=1"

rem Ensure the script runs from its own directory
pushd "%~dp0" >nul 2>&1 || (
    echo [ERROR] Unable to access script directory "%~dp0".
    goto :exit
)

set "PROJECT_ROOT=%CD%"

if not exist backend (
    echo [ERROR] Expected backend directory under "%PROJECT_ROOT%".
    goto :cleanup_root
)

pushd backend >nul 2>&1 || (
    echo [ERROR] Failed to enter backend directory.
    goto :cleanup_root
)

set "BACKEND_DIR=%CD%"
set "VENV_DIR=%BACKEND_DIR%\venv"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

where python >nul 2>&1 || (
    echo [ERROR] Python was not found on PATH.
    goto :cleanup_backend
)

set "PYTHON_VERSION="
set "PYTHON_MAJOR="
set "PYTHON_MINOR=0"
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
if not defined PYTHON_VERSION (
    echo [ERROR] Unable to determine Python version.
    goto :cleanup_backend
)
for /f "tokens=1 delims=." %%i in ("%PYTHON_VERSION%") do set "PYTHON_MAJOR=%%i"
for /f "tokens=2 delims=." %%i in ("%PYTHON_VERSION%") do set "PYTHON_MINOR=%%i"
if not defined PYTHON_MAJOR (
    echo [ERROR] Unable to parse Python major version from "%PYTHON_VERSION%".
    goto :cleanup_backend
)
for /f "delims=0123456789" %%i in ("%PYTHON_MAJOR%") do set "PYTHON_MAJOR="
if not defined PYTHON_MAJOR (
    echo [ERROR] Unexpected Python major version format.
    goto :cleanup_backend
)
for /f "delims=0123456789" %%i in ("%PYTHON_MINOR%") do set "PYTHON_MINOR="
if not defined PYTHON_MINOR (
    echo [ERROR] Unexpected Python minor version format.
    goto :cleanup_backend
)
if %PYTHON_MAJOR% LSS 3 (
    echo [ERROR] Python %PYTHON_VERSION% is not supported. Please use Python 3.x below 3.12.
    goto :cleanup_backend
)
if %PYTHON_MAJOR% GTR 3 (
    echo [ERROR] Python %PYTHON_VERSION% is not supported. Please use Python 3.x below 3.12.
    goto :cleanup_backend
)
if %PYTHON_MINOR% GEQ 12 (
    echo [ERROR] Python %PYTHON_VERSION% is not supported. Please use Python 3.x below 3.12.
    goto :cleanup_backend
)

echo Detected Python %PYTHON_VERSION%.

if exist "%VENV_ACTIVATE%" (
    echo Using existing Python virtual environment at "%VENV_DIR%".
) else (
    echo Creating Python virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        goto :cleanup_backend
    )

    if not exist requirements.txt (
        echo [ERROR] requirements.txt not found next to run.py.
        goto :cleanup_backend
    )

    echo Installing Python dependencies...
    "%VENV_PYTHON%" -m pip install --upgrade pip >nul 2>&1
    "%VENV_PYTHON%" -m pip install --disable-pip-version-check -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install backend dependencies.
        goto :cleanup_backend
    )
)

if not exist "%VENV_ACTIVATE%" (
    echo [ERROR] Virtual environment activation script missing at "%VENV_ACTIVATE%".
    goto :cleanup_backend
)

echo Activating virtual environment...
call "%VENV_ACTIVATE%"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    goto :cleanup_backend
)

if not exist run.py (
    echo [ERROR] run.py not found in "%BACKEND_DIR%".
    goto :cleanup_backend
)

echo Starting backend server...
start "" cmd /k "cd /d ""%BACKEND_DIR%"" && call ""%VENV_ACTIVATE%"" && python run.py"

popd >nul
set "BACKEND_DIR="

where npm >nul 2>&1 || (
    echo [WARNING] npm was not found on PATH. Frontend will not start.
    goto :cleanup_root
)

echo Starting frontend server...
start "" cmd /k "cd /d ""%PROJECT_ROOT%"" && npm run dev"

echo Both servers are now launching.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173

set "EXIT_CODE=0"

:cleanup_root
popd >nul
goto :exit

:cleanup_backend
popd >nul
set "BACKEND_DIR="
goto :cleanup_root

:exit
endlocal & exit /b %EXIT_CODE%
