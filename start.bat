@echo off
echo Checking for Python virtual environment...
cd backend

IF EXIST venv (
    echo Virtual environment found.
) ELSE (
    echo Creating Python virtual environment...
    python -m venv venv
    echo Virtual environment created.

    echo Installing Python dependencies...
    pip install -r requirements.txt
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting backend server...
start cmd /k "call venv\Scripts\activate && python run.py"
cd ..

echo Starting frontend server...
start cmd /k npm run dev

echo Both servers are now running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: The backend is running in a Python virtual environment.