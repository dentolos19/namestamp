@echo off
cd /d %~dp0
call setup.bat
python src/main.py %*