@echo off
rem Instala todo lo que necesita el agente Pixeloide (Python, FFmpeg, Remotion) y crea el .env para las claves.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\instalar.ps1"
echo.
pause
