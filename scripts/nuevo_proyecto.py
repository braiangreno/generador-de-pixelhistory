"""Crea un proyecto nuevo de documental 16-bit a partir del motor base (engine_template).

Uso:
  python scripts/nuevo_proyecto.py "La historia de Internet"
  python scripts/nuevo_proyecto.py "La historia de Internet" --guion C:\\ruta\\guion.pdf --idiomas es,en,pt
  python scripts/nuevo_proyecto.py "La historia de Internet" --slug historia_internet_pixel

Deja listo projects/<slug>/ con engine/, tools/, fonts/, las carpetas de audio, arte y renders,
el guion en guion.txt y project_meta.json. No llama a ninguna API.
"""
import argparse
import datetime
import os
import re
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import PROJECTS_DIR, REPO, SLUG_RE, TEMPLATE_DIR, escribir_json, idiomas, utf8_console  # noqa: E402

CARPETAS = [
    "assets/bg", "assets/portraits", "gen/backgrounds_raw", "gen/portraits_raw",
    "audio/vo", "audio/vo_en", "audio/vo_pt", "frames", "renders/subtitulos", "renders/shorts",
]

GITIGNORE = """# Generados en cada render (se rehacen solos)
renders/segments*/
renders/video_mudo*.mp4
audio/_tmp_*.wav
audio/vo*/_durations.json
gen/
__pycache__/
*.pyc
.env
"""

GITATTRIBUTES = """*.mp4 filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.gif filter=lfs diff=lfs merge=lfs -text
"""


def slugify(texto):
    s = unicodedata.normalize("NFD", texto.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return (s[:40].strip("_") or "documental") + "_pixel"


def leer_guion(path):
    from app.pipeline.script_director import extract_text_from_file
    if not os.path.isfile(path):
        raise SystemExit(f"No encuentro el guion: {path}")
    return extract_text_from_file(path)


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Crea un proyecto Pixeloide nuevo.")
    ap.add_argument("titulo", help="Título del documental (en español)")
    ap.add_argument("--slug", help="Nombre de la carpeta (minúsculas, números y _). Por defecto sale del título.")
    ap.add_argument("--guion", help="Archivo del guion (.txt, .md o .pdf)")
    ap.add_argument("--idiomas", default="es,en,pt")
    args = ap.parse_args()

    langs = idiomas(args.idiomas)
    slug = args.slug or slugify(args.titulo)
    if not SLUG_RE.match(slug):
        raise SystemExit(f"Slug inválido: {slug!r}")
    base, n = slug, 2
    while os.path.exists(os.path.join(PROJECTS_DIR, slug)):
        slug = f"{base}_{n}"
        n += 1
    pdir = os.path.join(PROJECTS_DIR, slug)

    for sub in ("engine", "tools", "fonts"):
        shutil.copytree(os.path.join(TEMPLATE_DIR, sub), os.path.join(pdir, sub),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for sub in CARPETAS:
        os.makedirs(os.path.join(pdir, sub), exist_ok=True)
    shutil.copy2(os.path.join(TEMPLATE_DIR, "ENGINE_GUIDE.md"), os.path.join(pdir, "ENGINE_GUIDE.md"))

    guion = leer_guion(args.guion) if args.guion else ""
    with open(os.path.join(pdir, "guion.txt"), "w", encoding="utf-8") as f:
        f.write(guion.strip() + "\n" if guion.strip() else "")
    with open(os.path.join(pdir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(GITIGNORE)
    with open(os.path.join(pdir, ".gitattributes"), "w", encoding="utf-8") as f:
        f.write(GITATTRIBUTES)

    ahora = datetime.datetime.now().isoformat(timespec="seconds")
    escribir_json(os.path.join(pdir, "project_meta.json"), {
        "id": slug,
        "title": args.titulo.strip(),
        "subtitle": "",
        "status": "en_produccion",
        "stage": 1,
        "stage_name": "Guion recibido",
        "progress": 0,
        "languages": langs,
        "created_at": ahora,
        "updated_at": ahora,
    })

    rel = os.path.relpath(pdir, REPO)
    print(f"Proyecto creado: {rel}")
    print(f"  guion.txt: {'con ' + str(len(guion)) + ' caracteres' if guion.strip() else 'vacío (pegá el guion ahí)'}")
    print(f"  idiomas: {', '.join(langs)}")
    print("Siguiente: escribir script_full.json (+ _en/_pt) y production_plan.json (ver la skill pixeloide-video-engine).")
    print(f"SLUG={slug}")


if __name__ == "__main__":
    main()
