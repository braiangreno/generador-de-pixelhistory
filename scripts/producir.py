"""Corre las etapas de producción de un proyecto (QA, audio, render, masters, subtítulos, miniaturas y shorts).

Uso:
  python scripts/producir.py <proyecto> --pasos hoja                 # hojas de contacto para revisar (rápido)
  python scripts/producir.py <proyecto> --pasos hoja --capitulo ch03 --idiomas es,en,pt
  python scripts/producir.py <proyecto> --pasos todo                 # todo, en orden
  python scripts/producir.py <proyecto> --pasos audio,video,master,srt --idiomas es --workers 16

Pasos (en este orden): timeline, hoja, audio, video, master, srt, miniaturas, shorts  (o "todo").
  timeline   → lista de frases con sus tiempos (valida voces + guion)
  hoja       → frames/sheet_<cap|all>[_en|_pt].png (un cuadro por escena) y sheet_v_* (cómo queda en 9:16)
  audio      → música chiptune + efectos + mezcla con ducking (ES) y mezclas EN/PT
  video      → renders/video_mudo[_en|_pt].mp4 (1920x1080, 30 fps, en paralelo)
  master     → renders/<Slug>_<ES|EN|PT>.mp4 con audio a -14 LUFS (sin subtítulos quemados)
  srt        → renders/subtitulos/<Slug>_<ES|EN|PT>.srt
  miniaturas → renders/Miniatura_YouTube_<LANG>.png + renders/Short_Vertical_<LANG>.mp4
  shorts     → renders/shorts/Short_CapNN_<LANG>.mp4 (9:16 redibujado a pantalla completa) + .srt
"""
import argparse
import datetime
import glob
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import (VOZ_DE_PRUEBA, duracion, escribir_json, idiomas, leer_json, proyecto_dir, run,  # noqa: E402
                    utf8_console)

ORDEN = ["timeline", "hoja", "audio", "video", "master", "srt", "miniaturas", "shorts"]
ETAPA = {"timeline": 4, "hoja": 5, "audio": 6, "video": 7, "master": 7, "srt": 7, "miniaturas": 8, "shorts": 8}


def aviso_voz(pdir):
    p = os.path.join(pdir, VOZ_DE_PRUEBA)
    if os.path.exists(p):
        n = sum(1 for ln in open(p, encoding="utf-8") if ":" in ln and not ln.startswith("#"))
        print("\n" + "!" * 78)
        print(f"!!  OJO: {n} frases tienen VOZ SINTÉTICA DE PRUEBA. Esto NO es para entregar.")
        print("!!  Generá las voces reales con: python scripts/voces.py <proyecto>")
        print("!" * 78 + "\n", flush=True)
        return True
    return False


def aviso_arte(pdir):
    p = os.path.join(pdir, "assets", "ARTE_PROVISORIO.txt")
    if os.path.exists(p):
        nombres = [ln.strip() for ln in open(p, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
        if nombres:
            print("\n" + "!" * 78)
            print(f"!!  OJO: {len(nombres)} imágenes son PROVISORIAS (no son de IA): {', '.join(nombres)[:60]}")
            print("!!  Generalas con: python scripts/arte.py <proyecto>  (Nano Banana / GPT Image)")
            print("!" * 78 + "\n", flush=True)
            return True
    return False


def meta_update(pdir, **cambios):
    path = os.path.join(pdir, "project_meta.json")
    meta = leer_json(path, {}) or {}
    meta.update(cambios)
    meta["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    escribir_json(path, meta)


def entregables(pdir):
    filas = []
    for patron in ("renders/*.mp4", "renders/shorts/*.mp4", "renders/*.png", "renders/subtitulos/*.srt"):
        for f in sorted(glob.glob(os.path.join(pdir, patron))):
            nombre = os.path.basename(f)
            if nombre.startswith("video_mudo") or nombre.startswith("Master_PixelArt"):
                continue
            mb = os.path.getsize(f) / (1024 * 1024)
            extra = ""
            if f.endswith(".mp4"):
                try:
                    extra = f"  {duracion(f):7.1f} s"
                except Exception:
                    extra = "  (no se pudo medir)"
            filas.append(f"  {os.path.relpath(f, pdir):60s} {mb:8.2f} MB{extra}")
    return filas


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Etapas de producción Pixeloide.")
    ap.add_argument("proyecto")
    ap.add_argument("--pasos", default="hoja")
    ap.add_argument("--idiomas", default=None)
    ap.add_argument("--capitulo", default=None, help="para 'hoja': ch01, ch02... (por defecto, todas las escenas)")
    ap.add_argument("--workers", type=int, default=int(os.environ.get("RENDER_WORKERS", "0") or 0))
    args = ap.parse_args()

    pdir = proyecto_dir(args.proyecto)
    meta = leer_json(os.path.join(pdir, "project_meta.json"), {}) or {}
    langs = idiomas(args.idiomas or ",".join(meta.get("languages") or ["es", "en", "pt"]))
    pedidos = ORDEN if args.pasos.strip() == "todo" else [p.strip() for p in args.pasos.split(",") if p.strip()]
    malos = [p for p in pedidos if p not in ORDEN]
    if malos:
        raise SystemExit(f"Pasos desconocidos: {malos}. Válidos: {', '.join(ORDEN)} o todo.")
    pasos = [p for p in ORDEN if p in pedidos]
    workers = args.workers or min(16, max(2, (os.cpu_count() or 8) - 4))
    # Proyectos hechos con una versión vieja del motor (los 3 documentales de referencia): sin vista 9:16 en las
    # hojas y sin límite de hilos por encoder (con muchos workers x264 se queda sin memoria).
    with open(os.path.join(pdir, "engine", "video.py"), encoding="utf-8") as f:
        motor = f.read()
    tiene_sheetv = "sheetv" in motor
    if "PX_FFMPEG_THREADS" not in motor and workers > 6:
        print(f"(Motor viejo en este proyecto: uso 6 workers en vez de {workers}.)")
        workers = 6
    py = sys.executable
    prueba = aviso_voz(pdir)
    prueba = aviso_arte(pdir) or prueba
    t_ini = time.time()

    for paso in pasos:
        t0 = time.time()
        print(f"\n===== {paso.upper()} =====", flush=True)
        meta_update(pdir, status="running", stage=ETAPA[paso], stage_name=f"Paso: {paso}")
        if paso == "timeline":
            run([py, "engine/timeline.py"], pdir)
        elif paso == "hoja":
            # Modo estricto: si un capítulo sincroniza con una palabra que no existe en la frase, falla acá.
            for lg in langs:
                cap = [args.capitulo] if args.capitulo else []
                run([py, "engine/video.py", "sheet", *cap], pdir, {"PX_LANG": lg, "PX_STRICT_WORDS": "1"})
                if tiene_sheetv:
                    run([py, "engine/video.py", "sheetv", *cap], pdir, {"PX_LANG": lg, "PX_STRICT_WORDS": "1"})
            print("Revisá las hojas en frames/: sheet_<cap|all>[_en|_pt].png (16:9) y sheet_v_*.png (9:16).")
        elif paso == "audio":
            run([py, "engine/audio.py"], pdir)
            otros = [lg for lg in langs if lg != "es"]
            if otros:
                run([py, "tools/mix_multilingual.py", *otros], pdir)
        elif paso == "video":
            for lg in langs:
                run([py, "engine/video.py", "render", str(workers)], pdir, {"PX_LANG": lg})
        elif paso == "master":
            run([py, "tools/mux_all.py", *langs], pdir)
        elif paso == "srt":
            run([py, "tools/make_multilingual_subtitles.py", *langs], pdir)
        elif paso == "miniaturas":
            run([py, "tools/make_thumbnails_and_shorts.py", *langs], pdir)
        elif paso == "shorts":
            run([py, "tools/make_chapter_shorts.py", *langs], pdir, {"RENDER_WORKERS": workers})
        print(f"----- {paso} listo en {time.time() - t0:.0f} s", flush=True)

    final = pasos[-1] == "shorts" and set(ORDEN).issubset(pasos)
    meta_update(pdir, status="completed" if final and not prueba else "en_produccion",
                stage=ETAPA[pasos[-1]], stage_name=f"Último paso: {pasos[-1]}", progress=100 if final else 50)
    print(f"\nTerminado en {time.time() - t_ini:.0f} s.")
    filas = entregables(pdir)
    if filas:
        print("Entregables en el proyecto:")
        print("\n".join(filas))
    if prueba:
        aviso_voz(pdir)
        aviso_arte(pdir)


if __name__ == "__main__":
    main()
