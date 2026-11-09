# ============================================================================
# Lanzador de Pixeloide Studio Server en Windows
# ============================================================================
$ErrorActionPreference = "Stop"
$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $AppDir

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
}

Write-Host "=== PIXELOIDE STUDIO SERVER · JUGAMOS EN SERIO. ===" -ForegroundColor Cyan
Write-Host "Abriendo panel web en http://localhost:8080 ..." -ForegroundColor Green

python -m uvicorn app.main:app --host 0.0.0.0 --port 8080
