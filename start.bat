@echo off
setlocal enabledelayedexpansion
echo ===== Report Agent Setup and Startup =====
echo.

echo Checking for Node.js dependencies...
if exist node_modules (
    echo Frontend dependencies found.
) else (
    echo Installing frontend dependencies...
    call npm install
    echo Frontend dependencies installed.
)

echo.
echo Checking for Python virtual environment...
cd backend

IF EXIST venv (
    echo Virtual environment found.
) ELSE (
    echo Checking for Python 3.11...
    where python | findstr "3.11" > nul
    if %errorlevel% equ 0 (
        echo Python 3.11 found.
        for /f "tokens=*" %%i in ('where python ^| findstr "3.11"') do set PY311=%%i
        echo Using Python 3.11: !PY311!
        "!PY311!" -m venv venv
    ) else (
        echo Python 3.11 not found, checking for py launcher...
        where py > nul 2>&1
        if %errorlevel% equ 0 (
            echo Py launcher found, trying to use Python 3.11...
            py -3.11 --version > nul 2>&1
            if %errorlevel% equ 0 (
                echo Python 3.11 found via py launcher.
                py -3.11 -m venv venv
            ) else (
                echo Python 3.11 not found via py launcher, using default Python.
                python -m venv venv
            )
        ) else (
            echo Py launcher not found, using default Python.
            python -m venv venv
        )
    )
    echo Virtual environment created.

    echo Activating virtual environment...
    call venv\Scripts\activate

    echo Installing Python dependencies...
    pip install -r requirements.txt
    
    echo Fixing numpy/pandas compatibility issue...
    pip uninstall -y numpy pandas
    pip install numpy==1.24.3
    pip install pandas==2.1.1
    echo Fixed numpy/pandas compatibility issue.
)

echo Virtual environment is ready.

call venv\Scripts\activate

echo Starting backend server...
start cmd /k "cd %CD% && call venv\Scripts\activate && python run.py"
cd ..

echo Starting frontend server...
start cmd /k npm run dev

echo Both servers are now running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: The backend is running in a Python virtual environment.
