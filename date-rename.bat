@echo off
cd /d %~dp0
call setup.bat
python date-rename.py %*
pause >nul