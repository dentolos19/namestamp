@echo off
cd /d %~dp0

echo Checking virtual environment...
if not exist .venv (
  echo Setting up virtual environment...
  py -m venv .venv
)

call .venv\Scripts\activate.bat

echo Checking requirements...
pip install -r requirements.txt >nul