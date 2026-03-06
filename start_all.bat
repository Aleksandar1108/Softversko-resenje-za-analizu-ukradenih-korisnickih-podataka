@echo off
echo Starting Backend and Frontend servers...
echo.

start "Backend Server" cmd /k "cd backend && start_server.bat"
timeout /t 3 /nobreak >nul

start "Frontend Server" cmd /k "cd frontend && start_server.bat"
timeout /t 3 /nobreak >nul

echo.
echo Servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul
