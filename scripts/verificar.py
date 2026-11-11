"""Chequeo del entorno del agente Pixeloide: librerías, FFmpeg, fuentes, Remotion y claves (sin mostrarlas).

Uso:
  python scripts/verificar.py
Sale con código 1 si falta algo imprescindible para renderizar.
"""
import importlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import PROJECTS_DIR, REMOTION_DIR, REPO, TEMPLATE_DIR, settings, utf8_console  # noqa: E402

OK, MAL, AVISO = "OK   ", "FALTA", "AVISO"


def linea(estado, que, detalle=""):
    print(f"  [{estado}] {que}" + (f" — {detalle}" if detalle else ""))


def salida(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                       errors="replace", timeout=60)
    except Exception as e:
        return f"ERROR: {e}"


def main():
    utf8_console()
    faltas = 0
    print("Python")
    en_venv = sys.prefix != sys.base_prefix
    linea(OK if en_venv else AVISO, f"Python {sys.version.split()[0]}", sys.executable if en_venv else
          "no es el .venv del repo: usá .venv\\Scripts\\python.exe")
    for mod, nombre, imprescindible in (("PIL", "Pillow", True), ("numpy", "NumPy", True),
                                        ("faster_whisper", "faster-whisper", False), ("pypdf", "pypdf", False),
                                        ("fastapi", "FastAPI (servidor web)", False),
                                        ("uvicorn", "Uvicorn (servidor web)", False)):
        try:
            m = importlib.import_module(mod)
            linea(OK, nombre, getattr(m, "__version__", ""))
        except Exception as e:
            linea(MAL if imprescindible else AVISO, nombre, str(e)[:80])
            faltas += imprescindible

    print("FFmpeg")
    for exe in ("ffmpeg", "ffprobe"):
        p = shutil.which(exe)
        linea(OK if p else MAL, exe, p or "no está en el PATH (winget install Gyan.FFmpeg)")
        faltas += not p
    if shutil.which("ffmpeg"):
        enc = salida(["ffmpeg", "-hide_banner", "-encoders"])
        filt = salida(["ffmpeg", "-hide_banner", "-filters"])
        linea(OK if "libx264" in enc else MAL, "codificador libx264")
        linea(OK if "loudnorm" in filt else MAL, "filtro loudnorm (-14 LUFS)")
        faltas += ("libx264" not in enc) + ("loudnorm" not in filt)

    print("Fuentes pixel del motor")
    for f in ("PressStart2P-Regular.ttf", "Silkscreen-Regular.ttf", "Silkscreen-Bold.ttf"):
        ok = os.path.exists(os.path.join(TEMPLATE_DIR, "fonts", f))
        linea(OK if ok else MAL, f)
        faltas += not ok

    print("Remotion (motion graphics)")
    node = shutil.which("node")
    linea(OK if node else AVISO, "Node.js", salida(["node", "--version"]).strip() if node else "no instalado")
    pkg = os.path.join(REMOTION_DIR, "node_modules", "remotion", "package.json")
    if os.path.exists(pkg):
        linea(OK, "remotion", json.load(open(pkg, encoding="utf-8")).get("version", "?"))
    else:
        linea(AVISO, "remotion", "falta npm install en remotion-pixeloide/")
    chrome = os.path.join(REMOTION_DIR, "node_modules", ".remotion", "chrome-headless-shell")
    linea(OK if os.path.isdir(chrome) else AVISO, "navegador headless de Remotion",
          "" if os.path.isdir(chrome) else "correr: npx remotion browser ensure (en remotion-pixeloide/)")

    print("Claves (solo si están, nunca su valor; cargalas con CLAVES.bat y probalas con scripts\\claves.py --probar)")
    cfg = settings()
    for k, nombre, para in (("elevenlabs_api_key", "ElevenLabs", "voces reales con tiempos por palabra"),
                            ("gemini_api_key", "Gemini", "Nano Banana: fondos y retratos con IA"),
                            ("openai_api_key", "OpenAI", "GPT Image: fondos y retratos con IA")):
        ok = bool((cfg.get(k) or "").strip())
        linea(OK if ok else AVISO, nombre, "configurada" if ok else f"no configurada ({para})")
    if not (cfg.get("gemini_api_key") or cfg.get("openai_api_key")):
        linea(AVISO, "Arte con IA", "sin Gemini ni OpenAI el agente no puede generar fondos ni retratos solo")

    print("Máquina")
    cpus = os.cpu_count() or 0
    linea(OK, f"{cpus} núcleos", f"render sugerido: --workers {min(16, max(2, cpus - 4))}")
    try:
        import ctranslate2
        import site
        n = ctranslate2.get_cuda_device_count()
        dlls = [os.path.join(b, "nvidia", sub, "bin", dll) for b in site.getsitepackages()
                for sub, dll in (("cublas", "cublas64_12.dll"), ("cudnn", "cudnn64_9.dll"))]
        tiene_libs = os.name != "nt" or sum(os.path.exists(p) for p in dlls) >= 2
        if n and tiene_libs:
            linea(OK, "Whisper en la GPU", f"{n} placa(s) CUDA con cuBLAS 12 y cuDNN 9 (large-v3-turbo)")
        elif n:
            linea(AVISO, "Whisper en la GPU", "hay placa NVIDIA pero faltan cuBLAS/cuDNN: INSTALAR.bat los instala")
        else:
            linea(AVISO, "Whisper en la GPU", "sin placa NVIDIA: Whisper usa la CPU (más lento)")
    except Exception:
        pass
    proyectos = sorted(d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d)))
    linea(OK, f"{len(proyectos)} proyectos en projects/", ", ".join(proyectos))
    print()
    if faltas:
        print(f"Faltan {faltas} cosas imprescindibles. Corré INSTALAR.bat en {REPO}")
        sys.exit(1)
    print("Todo listo para producir.")


if __name__ == "__main__":
    main()
