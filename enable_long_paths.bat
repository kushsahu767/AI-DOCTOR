@echo off
REM Run PowerShell script as Administrator to enable Long Paths
REM This batch file will request admin privileges automatically

echo Checking for Administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    PowerShell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs"
    exit /b
)

echo.
echo Enabling Windows Long Path Support...
PowerShell -NoProfile -ExecutionPolicy Bypass -Command ^
    "New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1 -PropertyType DWORD -Force"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Long Path support has been enabled!
    echo You can now install elevenlabs with: pip install elevenlabs
    echo.
    pause
) else (
    echo.
    echo ERROR: Failed to enable Long Path support
    echo Please run this file as Administrator
    echo.
    pause
    exit /b 1
)
