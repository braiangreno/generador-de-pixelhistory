# ============================================================================
# Instalador del agente Pixeloide (Windows). Se usa con doble clic en INSTALAR.bat.
# Instala: entorno Python 3.12 (.venv) con Pillow, NumPy, faster-whisper y el panel web;
# FFmpeg (si falta); Remotion + su navegador headless; y crea el .env para las claves.
# Se puede correr las veces que haga falta: lo que ya está instalado se saltea.
# ============================================================================
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Repo

function Paso($texto) { Write-Host ""; Write-Host "== $texto" -ForegroundColor Cyan }
function Aviso($texto) { Write-Host "   $texto" -ForegroundColor Yellow }
function Tiene($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

Paso "Python 3.12 (entorno .venv)"
$Py = Join-Path $Repo ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) {
    if (Tiene "uv") { uv venv --python 3.12 .venv }
    elseif (Tiene "py") { py -3.12 -m venv .venv }
    else { throw "No encuentro Python 3.12. Instalalo con: winget install Python.Python.3.12  (y volvé a correr INSTALAR.bat)" }
    if (-not (Test-Path $Py)) { throw "No se pudo crear el entorno .venv" }
}
if (Tiene "uv") { uv pip install --python $Py -r requirements.txt }
else { & $Py -m pip install --upgrade pip; & $Py -m pip install -r requirements.txt }
if ($LASTEXITCODE -ne 0) { throw "Falló la instalación de las librerías de Python" }

Paso "Whisper en la placa de video (NVIDIA)"
if (Tiene "nvidia-smi") {
    if (Tiene "uv") { uv pip install --python $Py -r requirements-gpu.txt }
    else { & $Py -m pip install -r requirements-gpu.txt }
    if ($LASTEXITCODE -ne 0) { Aviso "No se pudieron instalar cuBLAS/cuDNN: Whisper va a usar la CPU." }
} else {
    Write-Host "   no hay placa NVIDIA: Whisper va a usar la CPU"
}

Paso "FFmpeg"
if (Tiene "ffmpeg") {
    Write-Host "   ya está instalado"
} elseif (Tiene "winget") {
    winget install --id Gyan.FFmpeg -e
    Aviso "FFmpeg instalado: cerrá esta ventana y abrí INSTALAR.bat de nuevo para que Windows lo encuentre."
} else {
    Aviso "Falta FFmpeg: instalalo desde https://www.gyan.dev/ffmpeg/builds/ y agregalo al PATH."
}

Paso "Remotion (motion graphics)"
if (Tiene "npm") {
    Push-Location (Join-Path $Repo "remotion-pixeloide")
    npm install
    if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Falló npm install en remotion-pixeloide" }
    npx remotion browser ensure
    Pop-Location
} else {
    Aviso "Falta Node.js para Remotion (winget install OpenJS.NodeJS.LTS). El motor de video funciona igual sin él."
}

Paso "Archivo de claves (.env)"
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Aviso "Creé .env: cargá tus claves con doble clic en CLAVES.bat (ElevenLabs, Gemini y OpenAI)."
} else {
    Write-Host "   ya existe (no lo toco)"
}

Paso "Chequeo final"
$env:PYTHONUTF8 = "1"
& $Py scripts\verificar.py
