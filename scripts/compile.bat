@echo off
setlocal enabledelayedexpansion
title Minecraft Mod Translator - Compilation Script

echo ====================================
echo  Minecraft Mod Translator Compiler
echo ====================================
echo.

:: Change to project root directory
cd /d "%~dp0\.."

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated successfully.

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully.

:: Check if PyInstaller is installed
echo Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully.
) else (
    echo PyInstaller is already installed.
)

:: Clean previous builds
if exist "build" (
    echo Cleaning previous build directory...
    rmdir /s /q build
)

if exist "dist" (
    echo Cleaning previous dist directory...
    rmdir /s /q dist
)

:: Create dist directory
mkdir dist 2>nul

:: Create wrapper script for app version
echo Creating wrapper script for app version...
echo import sys > temp_app_wrapper.py
echo import os >> temp_app_wrapper.py
echo sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src')) >> temp_app_wrapper.py
echo sys.argv.append('app') >> temp_app_wrapper.py
echo from app.commands.app import main >> temp_app_wrapper.py
echo if __name__ == '__main__': >> temp_app_wrapper.py
echo     main() >> temp_app_wrapper.py

:: Get pyfiglet fonts location
echo Finding pyfiglet fonts location...
for /f "delims=" %%i in ('python -c "import pyfiglet; import os; print(os.path.dirname(pyfiglet.__file__))"') do set PYFIGLET_PATH=%%i
echo Pyfiglet path: %PYFIGLET_PATH%

:: Compile the CLI application
echo.
echo ====================================
echo    Compiling CLI Application...
echo ====================================
echo.

pyinstaller --onefile ^
    --name "mod-translator" ^
    --icon docs\logo\logo.ico ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --clean ^
    --noconfirm ^
    --console ^
    --add-data "src;src" ^
    --add-data "%PYFIGLET_PATH%\fonts;pyfiglet\fonts" ^
    --hidden-import "app" ^
    --hidden-import "app.commands" ^
    --hidden-import "app.commands.command_line" ^
    --hidden-import "app.commands.app" ^
    --hidden-import "app.commands.translate" ^
    --hidden-import "deep_translator" ^
    --hidden-import "rich" ^
    --hidden-import "questionary" ^
    --hidden-import "pyfiglet" ^
    --hidden-import "pyfiglet.fonts" ^
    --collect-data pyfiglet ^
    --hidden-import "argparse" ^
    --hidden-import "json" ^
    --paths src ^
    src/app/__main__.py

if errorlevel 1 (
    echo.
    echo ====================================
    echo     CLI Compilation FAILED!
    echo ====================================
    pause
    exit /b 1
)

echo CLI application compiled successfully.

:: Compile the APP application
echo.
echo ====================================
echo  Compiling Interactive Application...
echo ====================================
echo.

pyinstaller --onefile ^
    --name "Minecraft Mod Translator" ^
    --icon docs\logo\logo.ico ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --clean ^
    --noconfirm ^
    --console ^
    --add-data "src;src" ^
    --add-data "%PYFIGLET_PATH%\fonts;pyfiglet\fonts" ^
    --hidden-import "app" ^
    --hidden-import "app.commands" ^
    --hidden-import "app.commands.command_line" ^
    --hidden-import "app.commands.app" ^
    --hidden-import "app.commands.translate" ^
    --hidden-import "deep_translator" ^
    --hidden-import "rich" ^
    --hidden-import "questionary" ^
    --hidden-import "pyfiglet" ^
    --hidden-import "pyfiglet.fonts" ^
    --collect-data pyfiglet ^
    --hidden-import "argparse" ^
    --hidden-import "json" ^
    --paths src ^
    temp_app_wrapper.py

if errorlevel 1 (
    echo.
    echo ====================================
    echo     APP Compilation FAILED!
    echo ====================================
    del temp_app_wrapper.py 2>nul
    pause
    exit /b 1
)

echo Interactive application compiled successfully.

:: Clean up wrapper script
del temp_app_wrapper.py 2>nul

:: Check if executables were created
set CLI_EXISTS=0
set APP_EXISTS=0

if exist "dist\mod-translator.exe" (
    set CLI_EXISTS=1
)

if exist "dist\Minecraft Mod Translator.exe" (
    set APP_EXISTS=1
)

if %CLI_EXISTS%==1 if %APP_EXISTS%==1 (
    echo.
    echo ====================================
    echo     Compilation SUCCESSFUL!
    echo ====================================
    echo.
    echo CLI Executable: dist\mod-translator.exe
    dir "dist\mod-translator.exe" | find "mod-translator.exe"
    echo.
    echo APP Executable: dist\Minecraft Mod Translator.exe
    dir "dist\Minecraft Mod Translator.exe" | find "Minecraft Mod Translator.exe"
    echo.
    echo Usage:
    echo   CLI: "dist\mod-translator.exe" [commands]
    echo   APP: "dist\Minecraft Mod Translator.exe"
    echo.
) else (
    echo.
    echo ====================================
    echo     Compilation FAILED!
    echo ====================================
    if %CLI_EXISTS%==0 echo Error: CLI executable not found in dist directory
    if %APP_EXISTS%==0 echo Error: APP executable not found in dist directory
    pause
    exit /b 1
)

:: Clean up build artifacts
echo Cleaning build artifacts...
if exist "build" rmdir /s /q build
if exist "mod-translator.spec" del "mod-translator.spec"
if exist "Minecraft Mod Translator.spec" del "Minecraft Mod Translator.spec"

echo.
echo ====================================
echo     Compilation Complete!
echo ====================================
echo.

pause
