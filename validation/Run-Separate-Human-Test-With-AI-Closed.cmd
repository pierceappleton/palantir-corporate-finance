@echo off
cd /d "%~dp0\.."
".venv\Scripts\python.exe" "validation\locked_human_government_2029.py"
if errorlevel 1 pause
