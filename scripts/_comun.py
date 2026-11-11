"""Utilidades compartidas por los scripts del agente Pixeloide (rutas, claves, comandos).

Reglas:
- Las claves se leen de las variables de entorno, del `.env` de la raíz del repo o de `data/settings.json`
  (lo que usa también el servidor web). Nunca se imprimen: solo se informa si están o no.
- Todos los comandos hijos corren con UTF-8 forzado para que las tildes no se rompan en la consola de Windows.
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(REPO, "projects")
TEMPLATE_DIR = os.path.join(REPO, "engine_template")
REMOTION_DIR = os.path.join(REPO, "remotion-pixeloide")

if REPO not in sys.path:
    sys.path.insert(0, REPO)

LANG_CONFIG = {
    "es": {"script": "script_full.json", "vo": os.path.join("audio", "vo"), "suf": ""},
    "en": {"script": "script_full_en.json", "vo": os.path.join("audio", "vo_en"), "suf": "_en"},
    "pt": {"script": "script_full_pt.json", "vo": os.path.join("audio", "vo_pt"), "suf": "_pt"},
}

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_]{0,63}$")
VOZ_DE_PRUEBA = os.path.join("audio", "VOZ_DE_PRUEBA.txt")


def utf8_console():
    """Evita el texto roto (mojibake) al imprimir tildes en la consola de Windows."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def settings():
    """Configuración del estudio (claves, voces, workers) con la misma lógica que el servidor web.
    Un valor de ejemplo ("tu_..._api_key") cuenta como clave vacía."""
    from app.config import get_settings
    cfg = get_settings()
    for k, v in list(cfg.items()):
        if k.endswith("_api_key") and isinstance(v, str) and (v.strip().lower().startswith("tu_") or "***" in v):
            cfg[k] = ""
    return cfg


def tiene_clave(nombre):
    """True si la clave existe (sin devolverla nunca)."""
    return bool((settings().get(nombre) or "").strip())


def proyecto_dir(nombre):
    """Ruta segura de un proyecto dentro de projects/ (rechaza nombres raros o rutas)."""
    nombre = (nombre or "").strip().rstrip("/\\")
    if os.path.isabs(nombre) or "/" in nombre or "\\" in nombre:
        nombre = os.path.basename(os.path.normpath(nombre))
    if not SLUG_RE.match(nombre):
        raise SystemExit(f"Nombre de proyecto inválido: {nombre!r} (solo minúsculas, números y _).")
    pdir = os.path.join(PROJECTS_DIR, nombre)
    if not os.path.isdir(pdir):
        disponibles = ", ".join(sorted(d for d in os.listdir(PROJECTS_DIR)
                                       if os.path.isdir(os.path.join(PROJECTS_DIR, d))))
        raise SystemExit(f"No existe el proyecto {nombre!r}. Proyectos: {disponibles}")
    return pdir


def leer_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def escribir_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def env_hijo(extra=None):
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    if extra:
        env.update({k: str(v) for k, v in extra.items()})
    return env


def run(cmd, cwd, extra_env=None):
    """Corre un comando mostrando su salida en vivo. Falla con un mensaje claro si termina mal."""
    print(f"\n$ {' '.join(str(c) for c in cmd)}" + (f"   [{', '.join(f'{k}={v}' for k, v in extra_env.items())}]" if extra_env else ""), flush=True)
    proc = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env_hijo(extra_env))
    if proc.returncode != 0:
        raise SystemExit(f"El comando falló (código {proc.returncode}): {' '.join(str(c) for c in cmd)}")


def idiomas(arg, default="es,en,pt"):
    langs = [x.strip().lower() for x in (arg or default).split(",") if x.strip()]
    malos = [x for x in langs if x not in LANG_CONFIG]
    if malos:
        raise SystemExit(f"Idiomas no soportados: {malos}. Usá es, en, pt.")
    return langs


def duracion(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", path])
    return float(out.decode().strip())
