@echo off
cd /d "%~dp0\.."
".venv\Scripts\python.exe" "validation\locked_human_runner.py"
if errorlevel 1 pause