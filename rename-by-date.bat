@echo off
cd /d %~dp0
call setup.bat
python src/date-rename.py %*
pause >nul