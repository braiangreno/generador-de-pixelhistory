"""Prepara una imagen del proyecto para mirarla: una hoja de contacto, un arte, o un cuadro de un video.

La achica a un tamaño cómodo (los modelos que miran imágenes no necesitan más de ~1568 px de lado) y la deja en
gen/_vistas/. La usa Agent 009 Studio para mostrársela a sus agentes y al chat.

Uso:
  python scripts/vista.py <proyecto> frames/sheet_all.png [--max 1568] [--json]
  python scripts/vista.py <proyecto> renders/Mi_Video_ES.mp4 --segundo 12.5 --json

Solo abre archivos de frames/, renders/, assets/ y gen/ del proyecto (nunca fuera de su carpeta).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import proyecto_dir, utf8_console  # noqa: E402

from PIL import Image  # noqa: E402

CARPETAS = ("frames", "renders", "assets", "gen")
IMAGENES = (".png", ".jpg", ".jpeg", ".webp")
VIDEOS = (".mp4", ".mov")
MAX_BYTES = 3_500_000  # una imagen por encima de esto se guarda en JPEG


def ruta_segura(pdir, rel):
    rel = (rel or "").replace("\\", "/").strip().lstrip("/")
    partes = [p for p in rel.split("/") if p not in ("", ".")]
    if not partes or ".." in partes or partes[0] not in CARPETAS:
        raise SystemExit(f"Solo puedo abrir archivos de {', '.join(CARPETAS)} del proyecto (pediste {rel!r}).")
    destino = os.path.realpath(os.path.join(pdir, *partes))
    base = os.path.realpath(pdir)
    if os.path.commonpath([destino, base]) != base:
        raise SystemExit("Ese archivo está fuera del proyecto.")
    if not os.path.isfile(destino):
        raise SystemExit(f"No existe {rel}.")
    return destino, "/".join(partes)


def cuadro_de_video(path, segundo, salida):
    proc = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0.0, segundo):.3f}", "-i", path,
                           "-frames:v", "1", salida], capture_output=True, timeout=60)
    if proc.returncode != 0 or not os.path.exists(salida):
        raise SystemExit(f"No pude sacar el cuadro del segundo {segundo} ({proc.stderr.decode(errors='ignore')[:200]}).")
    return salida


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Achica una imagen (o un cuadro de video) del proyecto para mirarla.")
    ap.add_argument("proyecto")
    ap.add_argument("archivo", help="ruta relativa al proyecto, por ejemplo frames/sheet_all.png")
    ap.add_argument("--max", type=int, default=1568, help="lado más largo, en píxeles (200 a 4000)")
    ap.add_argument("--segundo", type=float, default=None, help="para un video: qué instante mirar")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    pdir = proyecto_dir(args.proyecto)
    origen, rel = ruta_segura(pdir, args.archivo)
    lado = max(200, min(4000, args.max))
    carpeta = os.path.join(pdir, "gen", "_vistas")
    os.makedirs(carpeta, exist_ok=True)
    clave = hashlib.sha1(f"{rel}|{args.segundo}|{lado}".encode("utf-8")).hexdigest()[:10]
    base = os.path.splitext(os.path.basename(rel))[0][:40]

    ext = os.path.splitext(origen)[1].lower()
    if ext in VIDEOS:
        segundo = args.segundo if args.segundo is not None else 1.0
        origen = cuadro_de_video(origen, segundo, os.path.join(carpeta, f"_cuadro_{clave}.png"))
    elif ext not in IMAGENES:
        raise SystemExit(f"No sé mostrar archivos {ext} (sí imágenes y videos).")

    with Image.open(origen) as im:
        im.load()
        original = im.size
        im = im.convert("RGB")
        escala = min(1.0, lado / max(im.size))
        if escala < 1.0:
            im = im.resize((max(1, round(im.size[0] * escala)), max(1, round(im.size[1] * escala))), Image.LANCZOS)
        salida = os.path.join(carpeta, f"{base}_{clave}.png")
        im.save(salida, optimize=True)
        if os.path.getsize(salida) > MAX_BYTES:
            os.remove(salida)
            salida = os.path.join(carpeta, f"{base}_{clave}.jpg")
            im.save(salida, quality=88)
        tam = im.size
    if ext in VIDEOS:
        os.remove(origen)  # el cuadro sacado del video ya está en la vista

    out = {"ruta": os.path.relpath(salida, pdir).replace(os.sep, "/"), "ancho": tam[0], "alto": tam[1],
           "original": list(original), "de": rel}
    if args.segundo is not None or ext in VIDEOS:
        out["segundo"] = args.segundo if args.segundo is not None else 1.0
    print(json.dumps(out, ensure_ascii=False) if args.json else f"{out['ruta']} ({tam[0]}x{tam[1]})")


if __name__ == "__main__":
    main()
