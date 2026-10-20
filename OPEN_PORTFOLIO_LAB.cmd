@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python environment missing. Follow README.md setup instructions.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" "analysis\interactive_surplus_portfolio_lab.py"
if errorlevel 1 pause
