@echo off
rem Carga tus claves (ElevenLabs, Gemini, OpenAI) en el .env sin mostrarlas en pantalla, y las prueba.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Primero hace doble clic en INSTALAR.bat
  pause
  exit /b 1
)
set PYTHONUTF8=1
".venv\Scripts\python.exe" scripts\claves.py
echo.
pause
