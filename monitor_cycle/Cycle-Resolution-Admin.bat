@echo off
title Monitor Resolution Cycle (Admin Mode)

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges.
) else (
    echo Requesting administrator privileges...
    echo.
    echo This script needs admin rights to attempt resolution changes.
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo ========================================
echo   MONITOR RESOLUTION CYCLE (ADMIN)
echo ========================================
echo.
echo Attempting to change resolution with elevated privileges...
echo.

:: Try to run the PowerShell script with admin rights
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Cycle-Monitor-Resolution-Registry.ps1"

echo.
echo ========================================
echo   ADMIN MODE COMPLETE
echo ========================================
echo.
echo If resolution change failed, try these alternatives:
echo.
echo 1. Graphics Driver Control Panel (most reliable)
echo 2. Windows Settings > System > Display
echo 3. Third-party tools like QRes or CRU
echo.
pause
