@echo off
chcp 65001 > nul
cd /d "%~dp0"
start pythonw bible.py
if %ERRORLEVEL% NEQ 0 (
    python bible.py
    pause
)
