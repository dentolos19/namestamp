@echo off
cd /d %~dp0
uv run pyinstaller src/main.py %*