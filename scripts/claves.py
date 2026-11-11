"""Carga y prueba las claves del agente (ElevenLabs, Gemini, OpenAI) en el .env de la raíz del repo.

Uso (o doble clic en CLAVES.bat):
  python scripts/claves.py            # pide cada clave sin mostrarla, la prueba y la guarda en .env
  python scripts/claves.py --probar   # solo prueba las que ya están (no pide nada)

Nunca imprime una clave: solo dice si anda y qué modelos de imagen habilita la cuenta.
El .env queda en texto plano en esta PC (está en .gitignore: no se sube a GitHub).
"""
import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import REPO, utf8_console  # noqa: E402

ENV = os.path.join(REPO, ".env")
CLAVES = [
    ("ELEVENLABS_API_KEY", "ElevenLabs (voces del narrador)"),
    ("GEMINI_API_KEY", "Gemini (Nano Banana: fondos y retratos)"),
    ("OPENAI_API_KEY", "OpenAI (GPT Image: fondos y retratos)"),
]


def leer_env():
    vals = {}
    if os.path.exists(ENV):
        for ln in open(ENV, encoding="utf-8-sig"):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                vals[k.strip()] = v.strip()
    return vals


def guardar_env(nuevas):
    lineas = open(ENV, encoding="utf-8-sig").read().splitlines() if os.path.exists(ENV) else []
    hechas = set()
    for i, ln in enumerate(lineas):
        k = ln.split("=", 1)[0].strip()
        if not ln.lstrip().startswith("#") and "=" in ln and k in nuevas:
            lineas[i] = f"{k}={nuevas[k]}"
            hechas.add(k)
    lineas += [f"{k}={v}" for k, v in nuevas.items() if k not in hechas]
    tmp = ENV + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lineas) + "\n")
    os.replace(tmp, ENV)


def _get(url, headers):
    req = urllib.request.Request(url, headers={"User-Agent": "pixeloide-claves/1.0", **headers})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"_texto": e.read().decode("utf-8", errors="ignore")[:300]}
    except Exception as e:
        return 0, {"_texto": str(e)[:200]}


def probar(nombre, clave):
    """Devuelve (ok, detalle). Nunca incluye la clave en el detalle."""
    if nombre == "ELEVENLABS_API_KEY":
        code, data = _get("https://api.elevenlabs.io/v1/user/subscription", {"xi-api-key": clave})
        if code == 200:
            usados, tope = data.get("character_count"), data.get("character_limit")
            extra = f" — plan {data.get('tier', '?')}, {usados:,} de {tope:,} caracteres usados" if tope else ""
            return True, "anda" + extra.replace(",", ".")
        if code == 401 and "permission" in data.get("_texto", "").lower():
            return True, "anda (clave con permisos limitados: no deja ver el saldo)"
        return False, f"rechazada (HTTP {code})"
    if nombre == "GEMINI_API_KEY":
        code, data = _get("https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000", {"x-goog-api-key": clave})
        if code != 200:
            return False, f"rechazada (HTTP {code})"
        modelos = sorted(m["name"].split("/", 1)[-1] for m in data.get("models", [])
                         if "image" in m.get("name", "") and "generateContent" in m.get("supportedGenerationMethods", []))
        return True, "anda — modelos de imagen: " + (", ".join(modelos) or "ninguno visible (revisá el plan)")
    if nombre == "OPENAI_API_KEY":
        code, data = _get("https://api.openai.com/v1/models", {"Authorization": f"Bearer {clave}"})
        if code != 200:
            return False, f"rechazada (HTTP {code})"
        modelos = sorted(m["id"] for m in data.get("data", []) if m.get("id", "").startswith("gpt-image"))
        return True, "anda — modelos de imagen: " + (", ".join(modelos) or "ninguno (la organización puede necesitar verificación)")
    return False, "desconocida"


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Carga y prueba las claves del agente.")
    ap.add_argument("--probar", action="store_true", help="solo probar las claves que ya están en .env")
    args = ap.parse_args()

    if not os.path.exists(ENV) and os.path.exists(os.path.join(REPO, ".env.example")):
        with open(os.path.join(REPO, ".env.example"), encoding="utf-8") as src, open(ENV, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    actuales = leer_env()
    nuevas = {}
    print("Claves del agente Pixeloide (se guardan en .env, que no se sube a GitHub).\n")
    for nombre, para in CLAVES:
        valor = actuales.get(nombre, "")
        if not args.probar:
            estado = "ya cargada" if valor else "vacía"
            pegada = getpass.getpass(f"{para} [{estado}] — pegá la clave y Enter (Enter solo = no cambiar): ").strip()
            if pegada:
                valor = pegada.strip().strip('"').strip("'")
        if not valor:
            print(f"  {nombre}: sin cargar\n")
            continue
        ok, detalle = probar(nombre, valor)
        print(f"  {nombre}: {'OK' if ok else 'ERROR'} — {detalle}\n")
        if not args.probar and valor != actuales.get(nombre, ""):
            if ok:
                nuevas[nombre] = valor
            else:
                print(f"  (no la guardo porque el proveedor la rechazó)\n")
    if nuevas:
        guardar_env(nuevas)
        print(f"Guardadas en .env: {', '.join(nuevas)}")
    elif not args.probar:
        print("No cambié nada en .env.")


if __name__ == "__main__":
    main()
