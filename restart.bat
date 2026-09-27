@echo off
REM Restart pet app
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq*" 2>nul
timeout /t 3 /nobreak >nul
start "" "启动桌宠.bat"
echo App restarted