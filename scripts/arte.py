"""Arte del documental generado con IA: fondos 480x270 y retratos 64x64 de las personas REALES de la historia.

Los retratos tienen que parecerse a la persona real (como los de los documentales de IA, Videojuegos y Dune):
en production_plan.json cada retrato lleva quién es y en qué año, y el prompt se arma solo.

  "portraits": [{"name": "frank_herbert", "persona": "Frank Herbert", "quien": "American journalist and science-fiction
                 writer, author of Dune", "anio": 1957, "rasgos": "short dark beard, horn-rimmed glasses, tweed jacket"}]
  "backgrounds": [{"name": "bg_dunas_1957", "prompt": "coastal sand dunes of Florence, Oregon in 1957 swallowing a road"}]

Uso:
  python scripts/arte.py <proyecto>                    # genera lo que falta: imágenes en gen/ > Nano Banana > GPT Image
  python scripts/arte.py <proyecto> --prompts          # no genera: muestra los prompts para usarlos en un conector
                                                       # (Higgsfield, etc.) y los guarda en gen/prompts_pendientes.json
  python scripts/arte.py <proyecto> --traer frank_herbert=https://.../imagen.png   # baja la imagen de un conector y la procesa
  python scripts/arte.py <proyecto> --solo frank_herbert --forzar                  # rehace uno
  python scripts/arte.py <proyecto> --motor gemini|openai|manual
  python scripts/arte.py <proyecto> --comparar --solo frank_herbert   # lo genera con Nano Banana Y con GPT Image:
                                                       # gen/candidatos/ + frames/arte_candidatos.png para mirarlos
  python scripts/arte.py <proyecto> --elegir frank_herbert=gptimage  # usa ese candidato (nanobanana|gptimage)
  python scripts/arte.py <proyecto> --motor procedural # SOLO borradores: fondos dibujados por código, marcados como provisorios

Foto de referencia (para gente poco conocida, o para clavar el parecido): dejala en gen/referencias/<name>.jpg|png
y se le pasa al modelo junto con el prompt (Gemini y OpenAI).

Claves (.env): GEMINI_API_KEY (Nano Banana) y/o OPENAI_API_KEY (GPT Image). Modelos: GEMINI_IMAGE_MODEL
(por defecto gemini-3.1-flash-image = Nano Banana 2) y OPENAI_IMAGE_MODEL (por defecto gpt-image-2); si el modelo
no existe se prueban los de respaldo. Cada imagen generada cuesta: pedí OK antes de una tanda grande.
"""
import argparse
import glob
import io
import mimetypes
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import escribir_json, leer_json, proyecto_dir, settings, utf8_console  # noqa: E402

from PIL import Image  # noqa: E402

from app.pipeline.ia_imagenes import (GEMINI_MODELOS, OPENAI_MODELOS, a_fondo, a_retrato,  # noqa: E402,F401
                                      gen_gemini, gen_openai, prompt_fondo, prompt_retrato)

ARTE_PROVISORIO = os.path.join("assets", "ARTE_PROVISORIO.txt")
MAX_DESCARGA = 30 * 1024 * 1024


def crudo(pdir, carpeta, nombre):
    for ext in ("png", "jpg", "jpeg", "webp"):
        hits = glob.glob(os.path.join(pdir, "gen", carpeta, f"{nombre}.{ext}"))
        if hits:
            return hits[0]
    return None


def huella_de(seleccion):
    """Lo que se va a generar, resumido: tipo, nombre, formato, prompt exacto y la foto de referencia de cada imagen."""
    import hashlib
    h = hashlib.sha256()
    for _idx, tipo, _item, nombre, _destino, prompt, aspect, _carpeta, ref in seleccion:
        foto = hashlib.sha256(ref[0]).hexdigest() if ref else ""
        h.update(f"{tipo}|{nombre}|{aspect}|{prompt}|{foto}|".encode("utf-8"))
    return h.hexdigest()[:32]


def referencia(pdir, nombre):
    path = crudo(pdir, "referencias", nombre)
    if not path:
        return None
    return open(path, "rb").read(), (mimetypes.guess_type(path)[0] or "image/png")


def traer(pdir, tipos, pedido):
    """Baja una imagen generada en un conector (https) y la deja como gen/<carpeta>/<name>.png."""
    if "=" not in pedido:
        raise SystemExit(f"--traer espera nombre=url, recibí {pedido!r}")
    nombre, url = pedido.split("=", 1)
    nombre, url = nombre.strip(), url.strip()
    if nombre not in tipos:
        raise SystemExit(f"{nombre!r} no está en production_plan.json (backgrounds/portraits).")
    if not url.lower().startswith("https://"):
        raise SystemExit("Solo bajo imágenes por https.")
    req = urllib.request.Request(url, headers={"User-Agent": "pixeloide-arte/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        datos = resp.read(MAX_DESCARGA + 1)
    if len(datos) > MAX_DESCARGA:
        raise SystemExit(f"La imagen de {nombre} pesa más de 30 MB.")
    im = Image.open(io.BytesIO(datos))
    im.load()  # falla acá si no es una imagen válida
    carpeta = os.path.join(pdir, "gen", "backgrounds_raw" if tipos[nombre] == "bg" else "portraits_raw")
    os.makedirs(carpeta, exist_ok=True)
    im.convert("RGB").save(os.path.join(carpeta, f"{nombre}.png"))
    print(f"  bajada {nombre} ({im.size[0]}x{im.size[1]}) -> gen/{os.path.basename(carpeta)}/{nombre}.png")
    return nombre


PROVEEDORES = {"nanobanana": "Nano Banana", "gptimage": "GPT Image"}


def hoja_candidatos(pdir, filas):
    """frames/arte_candidatos.png: por cada imagen, el original de cada modelo y cómo queda en pixel art."""
    from PIL import ImageDraw
    if not filas:
        return None
    celdas = []
    for nombre, tipo, cands in filas:
        for prov, im in cands:
            crudo_v = im.convert("RGB").copy()
            final = a_fondo(im) if tipo == "bg" else a_retrato(im)
            if tipo == "bg":
                crudo_v.thumbnail((480, 270))
                pix = final.resize((480, 270), Image.NEAREST)
            else:
                crudo_v.thumbnail((270, 270))
                pix = final.resize((256, 256), Image.NEAREST)
            celdas.append((f"{nombre} - {PROVEEDORES[prov]}", crudo_v, pix))
    ancho = max(c[1].width + c[2].width for c in celdas) + 30
    alto = sum(max(c[1].height, c[2].height) + 24 for c in celdas)
    hoja = Image.new("RGB", (ancho, alto), (24, 24, 32))
    d = ImageDraw.Draw(hoja)
    y = 0
    for titulo, a, b in celdas:
        d.text((6, y + 4), titulo, fill=(255, 220, 120))
        hoja.paste(a, (6, y + 20))
        hoja.paste(b, (a.width + 18, y + 20))
        y += max(a.height, b.height) + 24
    os.makedirs(os.path.join(pdir, "frames"), exist_ok=True)
    ruta = os.path.join(pdir, "frames", "arte_candidatos.png")
    hoja.save(ruta)
    return ruta


def provisorios(pdir):
    p = os.path.join(pdir, ARTE_PROVISORIO)
    return {ln.strip() for ln in open(p, encoding="utf-8") if ln.strip() and not ln.startswith("#")} if os.path.exists(p) else set()


def guardar_provisorios(pdir, nombres):
    p = os.path.join(pdir, ARTE_PROVISORIO)
    if not nombres:
        if os.path.exists(p):
            os.remove(p)
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Arte PROVISORIO (dibujado por código, no por IA). No entregar: regeneralo con IA.\n")
        f.write("\n".join(sorted(nombres)) + "\n")


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Genera con IA el arte pixel del proyecto.")
    ap.add_argument("proyecto")
    ap.add_argument("--motor", default="auto", choices=["auto", "manual", "gemini", "openai", "procedural"])
    ap.add_argument("--solo", default="")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--prompts", action="store_true", help="solo mostrar/guardar los prompts de lo que falta")
    ap.add_argument("--traer", action="append", default=[], metavar="NOMBRE=URL",
                    help="bajar una imagen generada en un conector (se puede repetir)")
    ap.add_argument("--comparar", action="store_true", help="generar con Nano Banana y GPT Image para elegir")
    ap.add_argument("--elegir", action="append", default=[], metavar="NOMBRE=nanobanana|gptimage",
                    help="usar un candidato de --comparar (se puede repetir)")
    ap.add_argument("--json", action="store_true", help="con --prompts: la lista en JSON (la lee Agent 009 Studio)")
    ap.add_argument("--huella", default="", help="la huella que dio --prompts: si lo que se va a generar cambió, no gasta nada")
    ap.add_argument("--max-imagenes", type=int, default=None, help="tope de imágenes aprobado: si se pasa, no gasta nada")
    args = ap.parse_args()

    pdir = proyecto_dir(args.proyecto)
    plan = leer_json(os.path.join(pdir, "production_plan.json"), {}) or {}
    trabajos = [("bg", b) for b in plan.get("backgrounds", [])] + [("retrato", p) for p in plan.get("portraits", [])]
    if not trabajos:
        raise SystemExit("production_plan.json no tiene 'backgrounds' ni 'portraits'.")
    tipos = {item.get("name"): tipo for tipo, item in trabajos if item.get("name")}
    solo = {x.strip() for x in args.solo.split(",") if x.strip()}
    traidos = {traer(pdir, tipos, pedido) for pedido in args.traer}
    for pedido in args.elegir:
        nombre, _, prov = pedido.partition("=")
        nombre, prov = nombre.strip(), prov.strip().lower()
        origen = os.path.join(pdir, "gen", "candidatos", f"{nombre}__{prov}.png")
        if nombre not in tipos or prov not in PROVEEDORES or not os.path.exists(origen):
            raise SystemExit(f"No hay candidato {nombre}__{prov}.png en gen/candidatos (corré --comparar antes).")
        carpeta = os.path.join(pdir, "gen", "backgrounds_raw" if tipos[nombre] == "bg" else "portraits_raw")
        os.makedirs(carpeta, exist_ok=True)
        Image.open(origen).convert("RGB").save(os.path.join(carpeta, f"{nombre}.png"))
        traidos.add(nombre)
        print(f"  elegido {nombre}: {PROVEEDORES[prov]}")
    if traidos:
        solo |= traidos
        args.forzar = True
        if args.motor == "auto":
            args.motor = "manual"

    cfg = settings()
    gkey = (cfg.get("gemini_api_key") or "").strip()
    okey = (cfg.get("openai_api_key") or "").strip()
    marcados = provisorios(pdir)
    pendientes, usados, faltan, comparados = [], {}, [], []
    if args.comparar and not (gkey or okey):
        raise SystemExit("--comparar necesita GEMINI_API_KEY y/o OPENAI_API_KEY en .env (cargalas con CLAVES.bat).")
    if args.comparar and solo:
        args.forzar = True  # comparar algo puntual aunque ya tenga imagen

    # Lo que se va a hacer en esta corrida (el mismo filtro para --prompts y para generar).
    seleccion = []
    for idx, (tipo, item) in enumerate(trabajos):
        nombre = item.get("name")
        if not nombre or (solo and nombre not in solo):
            continue
        destino = os.path.join(pdir, "assets", "bg" if tipo == "bg" else "portraits", f"{nombre}.png")
        provisorio = nombre in marcados
        if os.path.exists(destino) and not args.forzar and not (provisorio and args.motor != "procedural"):
            continue
        prompt = prompt_fondo(item) if tipo == "bg" else prompt_retrato(item)
        aspect = "16:9" if tipo == "bg" else "1:1"
        carpeta = "backgrounds_raw" if tipo == "bg" else "portraits_raw"
        ref = referencia(pdir, nombre) if tipo == "retrato" else None
        seleccion.append((idx, tipo, item, nombre, destino, prompt, aspect, carpeta, ref))
    huella = huella_de(seleccion)
    # Lo que se aprobó (Agent 009 Studio pasa la huella y el tope de --prompts): si el plan cambió desde entonces o se
    # pasa del tope, no se gasta nada.
    if not args.prompts and args.huella and args.huella != huella:
        raise SystemExit("El plan de arte cambió desde que se aprobó (lo que se iba a generar ya no es lo mismo). "
                         "No gasté nada: pedile al equipo que lo estime de nuevo.")
    if not args.prompts and args.max_imagenes is not None and len(seleccion) > args.max_imagenes:
        raise SystemExit(f"Son {len(seleccion)} imágenes y lo aprobado era hasta {args.max_imagenes}. No gasté nada.")

    for idx, tipo, item, nombre, destino, prompt, aspect, carpeta, ref in seleccion:
        if args.prompts:
            pendientes.append({"name": nombre, "tipo": tipo, "aspect_ratio": aspect, "prompt": prompt,
                               "destino": f"gen/{carpeta}/{nombre}.png",
                               "referencia": bool(ref)})
            continue
        if args.comparar:
            cands = []
            for prov, key, fn, extra in (("nanobanana", gkey, gen_gemini, aspect),
                                         ("gptimage", okey, gen_openai, "1536x1024" if tipo == "bg" else "1024x1024")):
                if not key:
                    continue
                try:
                    im, modelo = fn(key, prompt, extra, ref)
                except Exception as e:
                    print(f"  [aviso] {PROVEEDORES[prov]} no pudo con {nombre}: {e}")
                    continue
                os.makedirs(os.path.join(pdir, "gen", "candidatos"), exist_ok=True)
                im.save(os.path.join(pdir, "gen", "candidatos", f"{nombre}__{prov}.png"))
                cands.append((prov, im))
                print(f"  candidato {nombre:24s} <- {modelo}")
            if cands:
                comparados.append((nombre, tipo, cands))
            continue
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        im, origen = None, None
        raw = crudo(pdir, carpeta, nombre)
        if raw and args.motor in ("auto", "manual"):
            im, origen = Image.open(raw), "imagen en gen/"
        if im is None and args.motor in ("auto", "gemini") and gkey:
            try:
                im, origen = gen_gemini(gkey, prompt, aspect, ref)
            except Exception as e:
                print(f"  [aviso] Nano Banana no pudo con {nombre}: {e}")
        if im is None and args.motor in ("auto", "openai") and okey:
            try:
                im, origen = gen_openai(okey, prompt, "1536x1024" if tipo == "bg" else "1024x1024", ref)
            except Exception as e:
                print(f"  [aviso] GPT Image no pudo con {nombre}: {e}")
        if im is not None:
            if origen != "imagen en gen/":
                os.makedirs(os.path.join(pdir, "gen", carpeta), exist_ok=True)
                im.save(os.path.join(pdir, "gen", carpeta, f"{nombre}.png"))  # original, por si hay que reprocesar
            final = a_fondo(im) if tipo == "bg" else a_retrato(im)
            marcados.discard(nombre)
        elif args.motor == "procedural":
            from app.pipeline.asset_generator import _procedural_16bit_bg, _procedural_16bit_portrait
            final = (_procedural_16bit_bg(nombre, theme=item.get("theme", "lab"), seed=idx + 10) if tipo == "bg"
                     else _procedural_16bit_portrait(nombre, seed=idx + 100))
            origen = "PROVISORIO (código, no IA)"
            marcados.add(nombre)
        else:
            faltan.append((nombre, aspect, f"gen/{carpeta}/{nombre}.png"))
            continue
        final.save(destino)
        usados[origen] = usados.get(origen, 0) + 1
        print(f"  {tipo:7s} {nombre:28s} <- {origen}")

    if args.comparar:
        ruta = hoja_candidatos(pdir, comparados)
        if ruta:
            print(f"\nMirá {os.path.relpath(ruta, pdir)} y elegí con: --elegir <nombre>=nanobanana|gptimage")
        return

    if args.prompts:
        escribir_json(os.path.join(pdir, "gen", "prompts_pendientes.json"), pendientes)
        if args.json:
            import json
            print(json.dumps({"pendientes": pendientes, "claves": {"gemini": bool(gkey), "openai": bool(okey)},
                              "huella": huella, "cantidad": len(seleccion)}, ensure_ascii=False))
            return
        for p in pendientes:
            print(f"\n[{p['tipo']}] {p['name']}  ({p['aspect_ratio']})  ->  {p['destino']}"
                  + ("   (hay foto de referencia en gen/referencias/)" if p["referencia"] else ""))
            print(f"  {p['prompt']}")
        print(f"\n{len(pendientes)} imágenes por generar. Guardado en gen/prompts_pendientes.json.")
        return

    guardar_provisorios(pdir, marcados)
    print("Resumen:", ", ".join(f"{v} por {k}" for k, v in usados.items()) or "nada nuevo")
    if marcados:
        print(f"OJO: {len(marcados)} imágenes PROVISORIAS (no son de IA): {', '.join(sorted(marcados))}")
    if faltan:
        print("\nFaltan imágenes y no hay con qué generarlas acá (sin GEMINI_API_KEY ni OPENAI_API_KEY en .env).")
        print("Generalas con Nano Banana o GPT Image en un conector usando los prompts de --prompts, y bajalas con")
        print("  --traer nombre=URL   (o guardalas a mano en la ruta indicada y corré --motor manual):")
        for nombre, aspect, ruta in faltan:
            print(f"  - {nombre} ({aspect}) -> {ruta}")
        sys.exit(2)


if __name__ == "__main__":
    main()
