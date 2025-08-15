@echo off
echo ===================================================
echo =      Xray Fragment Tester Setup Script        =
echo ===================================================

:: --- URLs for Xray download ---
set "PRIMARY_URL=https://github.com/XTLS/Xray-core/releases/latest/download/Xray-windows-64.zip"
set "MIRROR_URL=https://github.com/sasanxxx/Xray-Fragment-Finder/releases/download/v1.0-assets/Xray-windows-64.zip"

echo.
echo [1/4] Creating Python virtual environment (venv)...
py -m venv venv
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create virtual environment. Please ensure Python and the 'venv' module are installed correctly.
    pause
    exit /b 1
)
echo SUCCESS: Virtual environment created.

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [3/4] Installing Python libraries...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Python libraries.
    pause
    exit /b 1
)
echo SUCCESS: Python libraries installed.

echo.
echo [4/4] Downloading Xray-core...
echo  -> Attempting to download from the official source...
powershell -Command "Invoke-WebRequest -Uri '%PRIMARY_URL%' -OutFile 'xray.zip'"

:: --- Fallback Logic ---
if %errorlevel% neq 0 (
    echo.
    echo  -> WARNING: Failed to download from the official link. Trying mirror...
    powershell -Command "Invoke-WebRequest -Uri '%MIRROR_URL%' -OutFile 'xray.zip'"
)

:: --- Final Check ---
if %errorlevel% neq 0 (
    echo.
    echo  -> ERROR: Failed to download Xray-core from both official and mirror links.
    echo     Please check your internet connection or the mirror link.
    pause
    exit /b 1
)
echo SUCCESS: Xray-core downloaded.

echo.
echo [+] Extracting Xray-core...
powershell -Command "Expand-Archive -Path 'xray.zip' -DestinationPath '.' -Force"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to extract xray.zip.
    pause
    exit /b 1
)
del xray.zip
echo SUCCESS: xray.exe is ready.

echo.
echo ===================================================================
echo =                      Setup Complete!                            =
echo = To run the application, please close this window and run run.bat =
echo ===================================================================
echo.
pause