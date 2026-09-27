@echo off
cd /d "%~dp0"
if exist "%~dp0runtime\pythonw.exe" (
  start "" "%~dp0runtime\pythonw.exe" run.py
) else (
  start "" "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\pythonw.exe" run.py
)