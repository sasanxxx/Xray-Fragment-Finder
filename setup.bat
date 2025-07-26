@echo off
echo ===================================================
echo =      Xray Fragment Tester Setup Script        =
echo ===================================================

echo.
echo [1/3] Installing Python libraries from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Python libraries. Please ensure pip is working.
    pause
    exit /b 1
)
echo SUCCESS: Python libraries installed.

echo.
echo [2/3] Downloading latest Xray-core for Windows (64-bit)...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/XTLS/Xray-core/releases/latest/download/Xray-windows-64.zip' -OutFile 'xray.zip'"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to download Xray-core. Please check your internet connection.
    pause
    exit /b 1
)
echo SUCCESS: Xray-core downloaded.

echo.
echo [3/3] Extracting Xray-core...
powershell -Command "Expand-Archive -Path 'xray.zip' -DestinationPath '.' -Force"
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to extract xray.zip. Please ensure you have permission to write in this folder.
    pause
    exit /b 1
)
del xray.zip
echo SUCCESS: xray.exe is ready.

echo.
echo ===================================================
echo =              Setup Complete!                    =
echo = You can now run the launcher.py script.         =
echo ===================================================
echo.
pause