@echo off
rem Reuse the adjacent PowerShell helper to install into windows\.venv.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_releases.ps1"
if errorlevel 1 exit /b %errorlevel%
echo Activate in Command Prompt with: call "%~dp0.venv\Scripts\activate.bat"
exit /b 0
