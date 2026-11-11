"""Tiempos palabra por palabra con Whisper (faster-whisper), para voces que NO vienen de ElevenLabs.

Uso:
  python scripts/transcribir.py <proyecto>                     # crea <id>.json para cada <id>.mp3 sin alineación (ES)
  python scripts/transcribir.py <proyecto> --idioma en --todas  # rehace la alineación de todas las frases en inglés
  python scripts/transcribir.py --archivo C:\\voz\\narracion.wav --idioma es --salida transcript.json

Con proyecto: escribe audio/vo{,_en,_pt}/<id>.json con el mismo formato que ElevenLabs
(characters + character_start/end_times_seconds) usando el texto de "speak" del guion, así
TL.word(id, "palabra") funciona igual. Las palabras del guion se emparejan con las que oyó Whisper
(aunque Whisper escriba "1957" donde el guion dice "mil novecientos cincuenta y siete").

Dispositivo: intenta la GPU (CUDA) y si no puede usa la CPU. Modelo por defecto: large-v3-turbo en GPU,
medium en CPU (--modelo para cambiarlo; la primera vez se descarga).
"""
import argparse
import difflib
import glob
import json
import os
import re
import site
import subprocess
import sys
import unicodedata

import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")  # Windows sin symlinks: el caché igual funciona

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import LANG_CONFIG, leer_json, proyecto_dir, utf8_console  # noqa: E402

PALABRA = re.compile(r"\w+", re.UNICODE)


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn" and (c.isalnum()))


def cargar_audio(path, sr=16000):
    """Audio mono 16 kHz en float32 decodificado con FFmpeg (no depende de PyAV, que cambió su API)."""
    out = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"])
    return np.frombuffer(out, dtype=np.float32).copy()


def _dll_dirs_nvidia():
    """Si están instalados los paquetes pip de NVIDIA (cuBLAS/cuDNN), los agrega al buscador de DLL."""
    if os.name != "nt":
        return
    for base in site.getsitepackages():
        for d in glob.glob(os.path.join(base, "nvidia", "*", "bin")):
            try:
                os.add_dll_directory(d)
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")
            except OSError:
                pass


def cargar_modelo(nombre, dispositivo, muestra):
    from faster_whisper import WhisperModel
    _dll_dirs_nvidia()
    if dispositivo in ("auto", "cuda"):
        try:
            m = WhisperModel(nombre or "large-v3-turbo", device="cuda", compute_type="float16")
            list(m.transcribe(cargar_audio(muestra)[:16000 * 5], language="es", beam_size=1)[0])  # la GPU falla recién al usarla
            print(f"Whisper {nombre or 'large-v3-turbo'} en GPU (CUDA).")
            return m
        except Exception as e:
            if dispositivo == "cuda":
                raise SystemExit(f"No pude usar la GPU: {e}")
            print(f"(GPU no disponible para Whisper: {str(e)[:120]}... uso la CPU)")
    m = WhisperModel(nombre or "medium", device="cpu", compute_type="int8")
    print(f"Whisper {nombre or 'medium'} en CPU.")
    return m


def palabras_whisper(modelo, audio, idioma):
    segs, _info = modelo.transcribe(cargar_audio(audio), language=idioma, word_timestamps=True, beam_size=5,
                                    condition_on_previous_text=False)
    out = []
    for s in segs:
        for w in (s.words or []):
            if norm(w.word):
                out.append((w.word.strip(), float(w.start), float(w.end)))
    return out


def alinear(texto, oidas, dur_total):
    """Devuelve tiempos por carácter de `texto` a partir de las palabras que oyó Whisper."""
    toks = [(m.start(), m.end(), norm(m.group())) for m in PALABRA.finditer(texto)]
    n = len(toks)
    tiempos = [None] * n
    if oidas and n:
        sm = difflib.SequenceMatcher(a=[t[2] for t in toks], b=[norm(w[0]) for w in oidas], autojunk=False)
        for a, b, size in sm.get_matching_blocks():
            for k in range(size):
                tiempos[a + k] = (oidas[b + k][1], oidas[b + k][2])
        if not any(tiempos):  # nada coincide (otro idioma, números): reparto en el rango hablado
            ini, fin = oidas[0][1], oidas[-1][2]
            tiempos[0], tiempos[-1] = (ini, ini), (fin, fin)
    elif n:
        tiempos[0], tiempos[-1] = (0.0, 0.0), (dur_total, dur_total)
    # interpolar las palabras sin pareja según su largo
    i = 0
    while i < n:
        if tiempos[i] is not None:
            i += 1
            continue
        j = i
        while j < n and tiempos[j] is None:
            j += 1
        t_a = tiempos[i - 1][1] if i > 0 else 0.0
        t_b = tiempos[j][0] if j < n else (dur_total if dur_total else t_a + 0.4 * (j - i))
        largo = [max(1, len(toks[k][2])) for k in range(i, j)]
        total = sum(largo)
        acc = 0
        for k in range(i, j):
            s = t_a + (t_b - t_a) * acc / total
            acc += largo[k - i]
            tiempos[k] = (s, t_a + (t_b - t_a) * acc / total)
        i = j
    starts = [0.0] * len(texto)
    ends = [0.0] * len(texto)
    for idx, (a, b, _w) in enumerate(toks):
        s, e = tiempos[idx]
        e = max(e, s + 0.01)
        for c in range(a, b):
            f0 = (c - a) / (b - a)
            f1 = (c - a + 1) / (b - a)
            starts[c] = s + (e - s) * f0
            ends[c] = s + (e - s) * f1
    # espacios y signos: quedan entre la palabra anterior y la siguiente
    ult = 0.0
    sig = [None] * len(texto)
    prox = None
    for c in range(len(texto) - 1, -1, -1):
        if any(a <= c < b for a, b, _ in toks):
            prox = starts[c]
        sig[c] = prox
    en_palabra = [False] * len(texto)
    for a, b, _ in toks:
        for c in range(a, b):
            en_palabra[c] = True
    for c in range(len(texto)):
        if en_palabra[c]:
            ult = ends[c]
        else:
            starts[c] = ult
            ends[c] = sig[c] if sig[c] is not None else ult
    return {
        "characters": list(texto),
        "character_start_times_seconds": [round(x, 4) for x in starts],
        "character_end_times_seconds": [round(max(x, y), 4) for x, y in zip(ends, starts)],
    }


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Alineación palabra por palabra con Whisper.")
    ap.add_argument("proyecto", nargs="?")
    ap.add_argument("--idioma", default="es", choices=list(LANG_CONFIG))
    ap.add_argument("--todas", action="store_true", help="rehace también las frases que ya tienen .json")
    ap.add_argument("--solo", default="")
    ap.add_argument("--archivo", help="transcribir un archivo suelto (sin proyecto)")
    ap.add_argument("--salida", default="transcript.json")
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--dispositivo", default="auto", choices=["auto", "cuda", "cpu"])
    args = ap.parse_args()

    if args.archivo:
        modelo = cargar_modelo(args.modelo, args.dispositivo, args.archivo)
        segs, _ = modelo.transcribe(cargar_audio(args.archivo), language=args.idioma, word_timestamps=True, beam_size=5)
        res = []
        for s in segs:
            res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                        "words": [{"w": w.word, "s": w.start, "e": w.end} for w in (s.words or [])]})
            print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}")
        with open(args.salida, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        print("Guardado:", args.salida)
        return

    if not args.proyecto:
        raise SystemExit("Indicá un proyecto o --archivo.")
    pdir = proyecto_dir(args.proyecto)
    cfg = LANG_CONFIG[args.idioma]
    lines = leer_json(os.path.join(pdir, cfg["script"]), None)
    if lines is None:
        raise SystemExit(f"Falta {cfg['script']}")
    vo = os.path.join(pdir, cfg["vo"])
    solo = {x.strip() for x in args.solo.split(",") if x.strip()}
    trabajo = []
    for row in lines:
        lid = row["id"]
        mp3 = os.path.join(vo, f"{lid}.mp3")
        js = os.path.join(vo, f"{lid}.json")
        if (solo and lid not in solo) or not os.path.exists(mp3):
            continue
        if os.path.exists(js) and not args.todas:
            continue
        trabajo.append((lid, row.get("speak", ""), mp3, js))
    if not trabajo:
        print("No hay frases para alinear (todas tienen .json; usá --todas para rehacerlas).")
        return
    from _comun import duracion
    modelo = cargar_modelo(args.modelo, args.dispositivo, trabajo[0][2])
    for k, (lid, texto, mp3, js) in enumerate(trabajo, 1):
        oidas = palabras_whisper(modelo, mp3, args.idioma)
        al = alinear(texto, oidas, duracion(mp3))
        if os.path.exists(js):
            # Los tiempos anteriores (por ejemplo, los exactos que dio ElevenLabs) quedan en una copia: no se pierden.
            import shutil
            shutil.copyfile(js, js + ".anterior")
        with open(js, "w", encoding="utf-8") as f:
            json.dump(al, f, ensure_ascii=False)
        pareadas = len(oidas)
        print(f"  [{k:02d}/{len(trabajo):02d}] {lid}: {pareadas} palabras oídas -> {js[len(pdir) + 1:]}")


if __name__ == "__main__":
    main()
