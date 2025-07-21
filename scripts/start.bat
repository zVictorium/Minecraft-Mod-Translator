@echo off
setlocal enabledelayedexpansion
title Minecraft Mod Translator

:: Change to project root directory
cd /d "%~dp0\.."

:: Check if virtual environment exists
if not exist ".venv\Scripts\activate" (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first to initialize the environment.
    pause
    exit /b 1
)

:: Activate virtual environment
call .venv\Scripts\activate
if errorlevel 1 (
    echo Error: Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Run the CLI app in app mode
mod-translator app %*

:: Add a pause at the end so the window doesn't close immediately
echo.
echo Press Enter to exit...
pause > nul