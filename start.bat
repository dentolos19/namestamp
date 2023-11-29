@echo off
call setup.bat
cd /d %~dp0
python src/main.py %*