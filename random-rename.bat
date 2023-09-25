@echo off
cd /d %~dp0
call setup.bat
python random-rename.py %*
pause >nul