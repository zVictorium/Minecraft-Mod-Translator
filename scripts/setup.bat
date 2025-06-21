@echo off
setlocal enabledelayedexpansion
title Minecraft Mod Translator - Setup Script

echo ====================================
echo  Minecraft Mod Translator Setup
echo ====================================
echo.

:: Change to project root directory
cd /d "%~dp0\.."

:: Upgrade pip to latest version
echo Upgrading pip to latest version...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Error: Failed to upgrade pip!
    pause
    exit /b 1
)
echo Pip upgraded successfully.

:: Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment!
    pause
    exit /b 1
)
echo Virtual environment created successfully.

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate
if errorlevel 1 (
    echo Error: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo Virtual environment activated successfully.

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully.

:: Install package in development mode
echo Installing package in development mode...
pip install -e .
if errorlevel 1 (
    echo Error: Failed to install package in development mode!
    pause
    exit /b 1
)
echo Package installed successfully.

echo.
echo ====================================
echo      Setup Complete!
echo ====================================
echo.

:: Show help for the CLI tool
echo Displaying help for mod-translator...
mod-translator --help

pause