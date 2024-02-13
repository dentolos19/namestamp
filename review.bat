@echo off
cd /d %~dp0
call setup.bat
cls
pip-review --interactive
pip freeze > requirements.txt