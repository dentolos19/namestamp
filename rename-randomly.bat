@echo off
cd /d %~dp0
call setup.bat
python src/random-rename.py %*
pause >nul