"""Locución con ElevenLabs + tiempos por carácter (para sincronizar la animación palabra por palabra).

Uso:
  python scripts/voces.py <proyecto> --estimar            # cuenta caracteres (lo que cobra ElevenLabs), no gasta nada
  python scripts/voces.py <proyecto>                      # genera las frases que faltan en es, en y pt
  python scripts/voces.py <proyecto> --idiomas es --solo c1_03,c1_04 --forzar   # rehace frases puntuales
  python scripts/voces.py <proyecto> --prueba             # voz sintética de PRUEBA (sin API, solo para probar)

Voces (Manual de Marca Pixeloide):
  ES: Carlos Aguilar (8MeTTgXVwMEhRVfblXOj), speed 1.08 — nunca cambiarla salvo pedido explícito.
  EN: pNInz6obpgDQGcFmaJgB y PT: Rxw6ylGPvxzn3gsuOExL, eleven_multilingual_v2, speed 1.0 (natural).

Salida por frase: audio/vo{,_en,_pt}/<id>.mp3 y <id>.json (alineación de ElevenLabs).
Con clave real NUNCA cae a la voz sintética en silencio: si una frase falla, se corta con error.
La voz de prueba deja audio/VOZ_DE_PRUEBA.txt; producir.py avisa mientras exista.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import LANG_CONFIG, VOZ_DE_PRUEBA, idiomas, leer_json, proyecto_dir, settings, utf8_console  # noqa: E402

FALLBACK_MODEL = "eleven_multilingual_v2"


def config_voces(cfg):
    return {
        "es": {"voice": cfg.get("voice_es_id") or "8MeTTgXVwMEhRVfblXOj",
               "model": os.environ.get("VOICE_ES_MODEL", "eleven_v4"),
               "speed": float(cfg.get("voice_es_speed") or 1.08)},
        "en": {"voice": cfg.get("voice_en_id") or "pNInz6obpgDQGcFmaJgB", "model": FALLBACK_MODEL, "speed": 1.0},
        "pt": {"voice": cfg.get("voice_pt_id") or "Rxw6ylGPvxzn3gsuOExL", "model": FALLBACK_MODEL, "speed": 1.0},
    }


def tts(api_key, voice, model, speed, text, prev_text, next_text):
    """Llama a /with-timestamps. Devuelve (audio_bytes, alignment, modelo_usado)."""
    fmt = "mp3_44100_192"
    body = {
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.80, "style": 0.35,
                           "use_speaker_boost": True, "speed": speed},
    }
    if prev_text:
        body["previous_text"] = prev_text
    if next_text:
        body["next_text"] = next_text
    ultimo = ""
    for intento in range(5):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format={fmt}"
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                     headers={"xi-api-key": api_key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return base64.b64decode(data["audio_base64"]), data.get("alignment") or {}, body["model_id"]
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="ignore")
            ultimo = f"HTTP {e.code}: {msg[:300]}"
            low = msg.lower()
            if e.code in (401,):
                raise SystemExit("ElevenLabs rechazó la clave (401). Revisá ELEVENLABS_API_KEY en el .env.")
            if "quota" in low or "credits" in low or e.code == 402:
                raise SystemExit(f"ElevenLabs: sin créditos suficientes. {ultimo}")
            if "output_format" in low and fmt != "mp3_44100_128":
                fmt = "mp3_44100_128"  # planes que no permiten 192 kbps
                continue
            if body["model_id"] != FALLBACK_MODEL and ("model" in low or e.code in (404, 422)):
                body["model_id"] = FALLBACK_MODEL
                continue
            if "previous_text" in low or "next_text" in low:
                body.pop("previous_text", None)
                body.pop("next_text", None)
                continue
            if e.code == 429 or e.code >= 500:
                time.sleep(2.0 * (intento + 1))
                continue
            raise SystemExit(f"ElevenLabs falló: {ultimo}")
        except (urllib.error.URLError, TimeoutError) as e:
            ultimo = str(e)
            time.sleep(2.0 * (intento + 1))
    raise SystemExit(f"ElevenLabs no respondió bien después de varios intentos: {ultimo}")


def marcas_prueba(pdir):
    p = os.path.join(pdir, VOZ_DE_PRUEBA)
    if not os.path.exists(p):
        return set()
    return {ln.strip() for ln in open(p, encoding="utf-8") if ":" in ln and not ln.startswith("#")}


def guardar_marcas(pdir, marcas):
    p = os.path.join(pdir, VOZ_DE_PRUEBA)
    if not marcas:
        if os.path.exists(p):
            os.remove(p)
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Frases con VOZ SINTÉTICA DE PRUEBA (no entregar). Se borra solo al regenerarlas con ElevenLabs.\n")
        for m in sorted(marcas):
            f.write(m + "\n")


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Genera la locución del proyecto con ElevenLabs.")
    ap.add_argument("proyecto")
    ap.add_argument("--idiomas", default=None, help="es,en,pt (por defecto: los del proyecto)")
    ap.add_argument("--solo", default="", help="ids separados por coma (c1_01,c1_02)")
    ap.add_argument("--forzar", action="store_true", help="regenera aunque ya exista")
    ap.add_argument("--estimar", action="store_true", help="solo cuenta caracteres, no llama a la API")
    ap.add_argument("--prueba", action="store_true", help="voz sintética local de prueba (sin API)")
    args = ap.parse_args()

    pdir = proyecto_dir(args.proyecto)
    meta = leer_json(os.path.join(pdir, "project_meta.json"), {}) or {}
    langs = idiomas(args.idiomas or ",".join(meta.get("languages") or ["es", "en", "pt"]))
    solo = {x.strip() for x in args.solo.split(",") if x.strip()}
    cfg = settings()
    voces = config_voces(cfg)
    marcas = marcas_prueba(pdir)

    pendientes = {}
    for lg in langs:
        lines = leer_json(os.path.join(pdir, LANG_CONFIG[lg]["script"]), None)
        if lines is None:
            print(f"[{lg.upper()}] falta {LANG_CONFIG[lg]['script']}: lo salteo.")
            continue
        out_dir = os.path.join(pdir, LANG_CONFIG[lg]["vo"])
        os.makedirs(out_dir, exist_ok=True)
        todo = []
        for i, row in enumerate(lines):
            lid = row["id"]
            if solo and lid not in solo:
                continue
            mp3 = os.path.join(out_dir, f"{lid}.mp3")
            js = os.path.join(out_dir, f"{lid}.json")
            existe = os.path.exists(mp3) and os.path.exists(js) and os.path.getsize(mp3) > 800
            es_prueba = f"{lg}:{lid}" in marcas
            if existe and not args.forzar and not (es_prueba and not args.prueba):
                continue
            prev_t = lines[i - 1]["speak"] if i > 0 else None
            next_t = lines[i + 1]["speak"] if i + 1 < len(lines) else None
            todo.append((lid, row["speak"], prev_t, next_t, mp3, js))
        pendientes[lg] = todo

    total_chars = sum(len(x[1]) for todo in pendientes.values() for x in todo)
    for lg, todo in pendientes.items():
        v = voces[lg]
        print(f"[{lg.upper()}] {len(todo)} frases pendientes, {sum(len(x[1]) for x in todo)} caracteres "
              f"(voz {v['voice']}, modelo {v['model']}, speed {v['speed']})")
    print(f"TOTAL: {total_chars} caracteres a sintetizar.")
    if args.estimar or total_chars == 0:
        if marcas:
            print(f"Ojo: {len(marcas)} frases tienen voz de PRUEBA (ver {VOZ_DE_PRUEBA}).")
        return

    if args.prueba:
        from app.pipeline.tts_service import _fallback_synth_voice
        for lg, todo in pendientes.items():
            for lid, text, _p, _n, mp3, js in todo:
                _fallback_synth_voice(text, mp3, js)
                marcas.add(f"{lg}:{lid}")
                print(f"  [{lg.upper()}] {lid} voz de PRUEBA")
        guardar_marcas(pdir, marcas)
        print(f"Listo con voz SINTÉTICA DE PRUEBA. No es para entregar: marcado en {VOZ_DE_PRUEBA}.")
        return

    api_key = (cfg.get("elevenlabs_api_key") or "").strip()
    if not api_key:
        raise SystemExit("Falta ELEVENLABS_API_KEY. Pegala en el archivo .env de la raíz del repo "
                         "(ELEVENLABS_API_KEY=...) o usá --prueba para una voz sintética de prueba.")

    hechas = 0
    for lg, todo in pendientes.items():
        v = voces[lg]
        for k, (lid, text, prev_t, next_t, mp3, js) in enumerate(todo, 1):
            audio, alignment, modelo = tts(api_key, v["voice"], v["model"], v["speed"], text, prev_t, next_t)
            if modelo != v["model"]:
                print(f"  (el modelo {v['model']} no está disponible: sigo con {modelo})")
                v["model"] = modelo
            if not alignment.get("characters"):
                raise SystemExit(f"ElevenLabs no devolvió la alineación para {lg}:{lid}.")
            with open(mp3, "wb") as f:
                f.write(audio)
            with open(js, "w", encoding="utf-8") as f:
                json.dump(alignment, f, ensure_ascii=False)
            marcas.discard(f"{lg}:{lid}")
            hechas += 1
            print(f"  [{lg.upper()} {k:02d}/{len(todo):02d}] {lid} OK")
    guardar_marcas(pdir, marcas)
    print(f"Listo: {hechas} frases con ElevenLabs ({total_chars} caracteres).")


if __name__ == "__main__":
    main()
