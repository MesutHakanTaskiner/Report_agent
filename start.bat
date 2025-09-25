@echo off
echo Installing Python dependencies...
cd backend
echo Starting backend server...
start cmd /k python run.py
cd ..
echo Starting frontend server...
start cmd /k npm run dev
echo Both servers are now running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
