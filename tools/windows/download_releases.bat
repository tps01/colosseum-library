@echo off
rem Reuse the adjacent PowerShell helper; downloads go to the shared tools folder.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0download_releases.ps1"
exit /b %errorlevel%
