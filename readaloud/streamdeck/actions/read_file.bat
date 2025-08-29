@echo off
cd /d "%~dp0..\.."
REM You can modify this file path as needed
set FILE_PATH="C:\temp\example.txt"
python streamdeck\simple_integration.py file %FILE_PATH%
