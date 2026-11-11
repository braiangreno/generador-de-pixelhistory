# ============================================================================
# Lanzador de Pixeloide Studio Server en Windows
# Escucha solo en esta PC (127.0.0.1): el panel no tiene contraseña, así que no se abre a la red.
# Para abrirlo a la red a propósito:  $env:PIXELOIDE_HOST = "0.0.0.0"; .\start_windows.ps1
# ============================================================================
$ErrorActionPreference = "Stop"
$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $AppDir

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
}

$Py = Join-Path $AppDir ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) {
    Write-Host "Falta instalar: doble clic en INSTALAR.bat primero." -ForegroundColor Yellow
    exit 1
}
$BindHost = if ($env:PIXELOIDE_HOST) { $env:PIXELOIDE_HOST } else { "127.0.0.1" }
$env:PYTHONUTF8 = "1"

Write-Host "=== PIXELOIDE STUDIO SERVER · JUGAMOS EN SERIO. ===" -ForegroundColor Cyan
Write-Host "Abriendo panel web en http://localhost:8080 ..." -ForegroundColor Green
Start-Process "http://localhost:8080"

& $Py -m uvicorn app.main:app --host $BindHost --port 8080
