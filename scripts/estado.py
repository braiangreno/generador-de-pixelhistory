"""Estado de un proyecto (o la lista de proyectos), para el agente y para Agent 009 Studio.

Uso:
  python scripts/estado.py --lista [--json]        # proyectos: slug, título, estado, idiomas
  python scripts/estado.py <proyecto>              # resumen legible
  python scripts/estado.py <proyecto> --json       # todo en JSON (lo lee el estudio)

Revisa el guion (los tres idiomas con los mismos ids), el plan de producción (escenas, fondos, retratos, música y
textos en pantalla traducidos), las voces, el arte, las hojas de contacto y los entregables. No llama a ninguna API ni
modifica nada. Las claves se informan solo como sí/no.
"""
import argparse
import ast
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comun import LANG_CONFIG, PROJECTS_DIR, VOZ_DE_PRUEBA, proyecto_dir, tiene_clave, utf8_console  # noqa: E402

LAYOUTS = ("title_card", "chapter_card", "dialogue_scene", "lab_scene", "split_vs", "data_bars",
           "living_room_tv", "calendar_stamp")
MUSICA = ("mystery", "build", "bright", "summer", "rain", "puzzle", "triumph", "winter")
BRAZOS = ("down", "type", "write", "wave", "point", "point_l", "cheer", "hold", "think", "shrug", "cross", "hip")
ANIMOS = ("happy", "worried", "sad", "neutral")
CLIMA = ("rain", "snow", "confetti")
ID_RE = re.compile(r"^(s\d{2}|c\d{1,2}_\d{2})$")
NOMBRE_RE = re.compile(r"^[a-z0-9_]{1,60}$")
MAX_TARJETA = 32
ARTE_PROVISORIO = os.path.join("assets", "ARTE_PROVISORIO.txt")


def _leer(path, default=None):
    """JSON de un archivo del proyecto. Si está roto devuelve ({'__error__': motivo})."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # archivo a medio escribir o editado a mano
        return {"__error__": str(e)[:200]}


def presets(pdir):
    """Nombres de personajes que entiende el motor de ESTE proyecto (CAST de engine/sprites.py), sin importarlo."""
    path = os.path.join(pdir, "engine", "sprites.py")
    nombres = set()
    try:
        with open(path, encoding="utf-8") as f:
            arbol = ast.parse(f.read())
    except Exception:
        return nombres
    for nodo in ast.walk(arbol):
        dic = None
        if isinstance(nodo, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAST" for t in nodo.targets):
            dic = nodo.value
        elif (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute) and nodo.func.attr == "update"
              and isinstance(nodo.func.value, ast.Name) and nodo.func.value.id == "CAST" and nodo.args):
            dic = nodo.args[0]
        if isinstance(dic, ast.Dict):
            for k in dic.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    nombres.add(k.value)
    return nombres


def capitulo_de(lid):
    m = re.match(r"^c(\d+)_", str(lid or ""))
    return int(m.group(1)) if m else 0


def puntero_lfs(path):
    """True si el archivo es un puntero de Git LFS (el medio de verdad no se bajó: `git lfs pull`)."""
    try:
        if os.path.getsize(path) > 1024:
            return False
        with open(path, "rb") as f:
            return f.read(40).startswith(b"version https://git-lfs")
    except OSError:
        return False


def capitulos_a_mano(pdir):
    return sorted(int(os.path.basename(p)[2:4]) for p in glob.glob(os.path.join(pdir, "engine", "ch[0-9][0-9].py")))


# --------------------------------------------------------------------------------------------- guion

def revisar_guion(pdir, langs):
    info, problemas, guiones = {}, [], {}
    base = None
    a_mano = set(capitulos_a_mano(pdir))
    for lg in ("es", "en", "pt"):
        archivo = LANG_CONFIG[lg]["script"]
        data = _leer(os.path.join(pdir, archivo))
        if data is None:
            info[lg] = None
            if lg in langs:
                problemas.append(f"Falta {archivo}.")
            continue
        if not isinstance(data, list):
            info[lg] = None
            problemas.append(f"{archivo} está roto: {data.get('__error__') if isinstance(data, dict) else 'no es una lista'}.")
            continue
        # Los guiones viejos (documentales de IA y de Videojuegos) no tienen "ch": sale del id, como hace el motor.
        filas = [r if "ch" in r else {**r, "ch": capitulo_de(r.get("id"))} for r in data if isinstance(r, dict)]
        guiones[lg] = filas
        caps = sorted({r.get("ch") for r in filas if isinstance(r.get("ch"), int)})
        info[lg] = {"lineas": len(filas), "capitulos": caps,
                    "caracteres": sum(len(str(r.get("speak", ""))) for r in filas)}
        vistos = set()
        for i, r in enumerate(filas):
            lid = r.get("id")
            if not isinstance(lid, str) or not ID_RE.match(lid):
                problemas.append(f"{archivo}: la línea {i + 1} tiene un id inválido ({lid!r}); van s01, s02… o c1_00, c1_01…")
            elif lid in vistos:
                problemas.append(f"{archivo}: el id {lid} está repetido.")
            vistos.add(lid)
            if not str(r.get("speak", "")).strip():
                problemas.append(f"{archivo}: {lid} no tiene 'speak' (lo que lee la voz).")
            if isinstance(lid, str) and ID_RE.match(lid) and lid.startswith("c") and capitulo_de(lid) != r.get("ch"):
                problemas.append(f"{archivo}: {lid} dice ch={r.get('ch')!r} pero su id es del capítulo {capitulo_de(lid)}.")
        if lg == "es":
            base = filas
            for ch in caps:
                if ch >= 1 and ch not in a_mano and f"c{ch}_00" not in vistos:
                    problemas.append(f"El capítulo {ch} no tiene su placa c{ch}_00 («Capítulo {ch}. Título.»).")
        elif base is not None:
            ids_base = [(r.get("id"), r.get("ch"), r.get("pause")) for r in base]
            ids_lg = [(r.get("id"), r.get("ch"), r.get("pause")) for r in filas]
            if ids_base != ids_lg:
                distintos = [a[0] for a, b in zip(ids_base, ids_lg) if a != b][:5]
                problemas.append(f"{archivo} no tiene los mismos id, ch y pause que el español, en el mismo orden"
                                 + (f" (por ejemplo {', '.join(map(str, distintos))})" if distintos else
                                    f" ({len(ids_lg)} líneas contra {len(ids_base)})") + ".")
    original = os.path.join(pdir, "guion.txt")
    info["original_caracteres"] = os.path.getsize(original) if os.path.exists(original) else 0
    return info, problemas, guiones


# --------------------------------------------------------------------------------------------- plan

def _textos_de_escena(sc):
    """Textos que el motor dibuja en pantalla para una escena (tienen que estar traducidos)."""
    out = []
    for k in ("header", "subheader", "stamp"):
        if isinstance(sc.get(k), str):
            out.append(sc[k])
    lt = sc.get("lower_third")
    if isinstance(lt, dict):
        out += [lt.get(k) for k in ("title", "sub") if isinstance(lt.get(k), str)]
    for c in sc.get("cards") or []:
        if isinstance(c, dict):
            if isinstance(c.get("title"), str):
                out.append(c["title"])
            for ln in c.get("lines") or []:
                txt = ln[0] if isinstance(ln, (list, tuple)) and ln else ln
                if isinstance(txt, str):
                    out.append(txt)
    for ch in sc.get("characters") or []:
        if isinstance(ch, dict) and isinstance(ch.get("bubble"), str):
            out.append(ch["bubble"])
    for ln in sc.get("title_lines") or []:
        if isinstance(ln, str):
            out.append(ln)
    if isinstance(sc.get("years"), str):
        out.append(sc["years"])
    for b in sc.get("bars") or []:
        if isinstance(b, (list, tuple)) and b and isinstance(b[0], str):
            out.append(b[0])
    return [t for t in out if t and re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", t)]


def revisar_plan(pdir, guiones):
    plan = _leer(os.path.join(pdir, "production_plan.json"))
    if plan is None:
        # Un documental con todos sus capítulos escritos a mano (los de referencia) no necesita plan.
        return {"existe": False, "capitulos_a_mano": [f"ch{c:02d}" for c in capitulos_a_mano(pdir)]}, []
    if not isinstance(plan, dict) or "__error__" in plan:
        return {"existe": False}, [f"production_plan.json está roto: {plan.get('__error__') if isinstance(plan, dict) else 'no es un objeto'}."]
    problemas, avisos = [], []
    fondos = [b for b in plan.get("backgrounds") or [] if isinstance(b, dict)]
    retratos = [p for p in plan.get("portraits") or [] if isinstance(p, dict)]
    escenas = [s for s in plan.get("scenes") or [] if isinstance(s, dict)]
    musica = plan.get("chapter_music") if isinstance(plan.get("chapter_music"), dict) else {}
    nombres_bg = {b.get("name") for b in fondos}
    nombres_por = {p.get("name") for p in retratos}

    for b in fondos:
        if not NOMBRE_RE.match(str(b.get("name", ""))):
            problemas.append(f"Fondo con nombre inválido ({b.get('name')!r}): minúsculas, números y _.")
        if not str(b.get("prompt", "")).strip():
            problemas.append(f"Al fondo {b.get('name')} le falta el 'prompt' (lugar y año, en inglés).")
    for p in retratos:
        if not NOMBRE_RE.match(str(p.get("name", ""))):
            problemas.append(f"Retrato con nombre inválido ({p.get('name')!r}): minúsculas, números y _.")
        faltan = [k for k in ("persona", "quien", "anio", "rasgos") if not str(p.get(k, "")).strip()]
        if faltan:
            problemas.append(f"Al retrato {p.get('name')} le falta {', '.join(faltan)} (con eso se arma el parecido).")
    for ch, estilo in musica.items():
        if estilo not in MUSICA:
            problemas.append(f"chapter_music[{ch}] = {estilo!r} no existe. Estilos: {', '.join(MUSICA)}.")

    es = guiones.get("es") or []
    orden = {r.get("id"): i for i, r in enumerate(es)}
    cap = {r.get("id"): r.get("ch") for r in es}
    cast = presets(pdir)
    por_cap = {}
    textos = []
    for i, sc in enumerate(escenas):
        lid = sc.get("line_id") or sc.get("start_line")
        donde = f"Escena {i + 1} ({lid})"
        if lid not in orden:
            problemas.append(f"{donde}: line_id no existe en el guion en español.")
        else:
            por_cap[cap[lid]] = por_cap.get(cap[lid], 0) + 1
            fin = sc.get("end_line") or lid
            if fin not in orden:
                problemas.append(f"{donde}: end_line {fin!r} no existe en el guion.")
            elif orden[fin] < orden[lid]:
                problemas.append(f"{donde}: end_line {fin} está antes que line_id.")
            elif cap.get(fin) != cap.get(lid):
                problemas.append(f"{donde}: line_id y end_line son de capítulos distintos.")
        layout = sc.get("layout", "dialogue_scene")
        if layout not in LAYOUTS:
            problemas.append(f"{donde}: layout {layout!r} no existe. Opciones: {', '.join(LAYOUTS)}.")
        for clave in ("bg", "bg_left", "bg_right"):
            nombre = sc.get(clave)
            if nombre and layout not in ("title_card", "chapter_card") and nombre not in nombres_bg:
                problemas.append(f"{donde}: {clave} {nombre!r} no está en backgrounds del plan.")
        if sc.get("portrait") and sc["portrait"] not in nombres_por:
            problemas.append(f"{donde}: portrait {sc['portrait']!r} no está en portraits del plan.")
        if sc.get("weather") and sc["weather"] not in CLIMA:
            problemas.append(f"{donde}: weather {sc['weather']!r} no existe ({', '.join(CLIMA)}).")
        for c in sc.get("characters") or []:
            if isinstance(c, str):
                c = {"preset": c}
            if not isinstance(c, dict):
                problemas.append(f"{donde}: un personaje no tiene la forma esperada.")
                continue
            if cast and c.get("preset", "inge") not in cast:
                problemas.append(f"{donde}: el personaje {c.get('preset')!r} no existe. Presets: {', '.join(sorted(cast))}.")
            if c.get("arms") and str(c["arms"]).strip() not in BRAZOS:
                problemas.append(f"{donde}: arms {c['arms']!r} no existe ({', '.join(BRAZOS)}).")
            try:
                if not 250 <= int(c.get("feet", 260)) <= 266:
                    avisos.append(f"{donde}: feet {c.get('feet')} deja al personaje flotando o enterrado (va de 260 a 264).")
                if not 16 <= int(c.get("x", 240)) <= 464:
                    avisos.append(f"{donde}: x {c.get('x')} saca al personaje de la pantalla (16 a 464).")
                if int(c.get("scale", 2)) not in (1, 2, 3):
                    avisos.append(f"{donde}: scale {c.get('scale')} (usá 2 o 3).")
            except (TypeError, ValueError):
                problemas.append(f"{donde}: x, feet y scale de los personajes van con números.")
        for c in sc.get("cards") or []:
            for ln in (c.get("lines") or []) if isinstance(c, dict) else []:
                txt = ln[0] if isinstance(ln, (list, tuple)) and ln else ln
                if isinstance(txt, str) and len(txt) > MAX_TARJETA:
                    avisos.append(f"{donde}: la línea de tarjeta {txt!r} pasa las {MAX_TARJETA} letras (se parte en dos).")
        textos += _textos_de_escena(sc)

    capitulos = sorted({r.get("ch") for r in es if isinstance(r.get("ch"), int)})
    a_mano = capitulos_a_mano(pdir)
    sin_escenas = [c for c in capitulos if c not in por_cap and c not in a_mano]
    if escenas and sin_escenas:
        avisos.append("Capítulos sin escenas en el plan ni chNN.py: "
                      + ", ".join(map(str, sin_escenas)) + " (se ven con escenas automáticas genéricas).")

    trad = plan.get("translations_map") if isinstance(plan.get("translations_map"), dict) else {}
    sin_traducir = {}
    for lg in ("en", "pt"):
        if lg not in guiones:
            continue
        mapa = trad.get(lg) if isinstance(trad.get(lg), dict) else {}
        faltan = sorted({t for t in textos if t not in mapa})
        if faltan:
            sin_traducir[lg] = faltan
            problemas.append(f"{len(faltan)} textos en pantalla sin traducir al {lg.upper()} en translations_map "
                             f"(por ejemplo: {', '.join(repr(t) for t in faltan[:4])}).")
    for k in ("title", "subtitle", "slug"):
        if not str(plan.get(k, "")).strip():
            avisos.append(f"Al plan le falta '{k}'.")
    for k in ("titles", "subtitles"):
        d = plan.get(k)
        if not isinstance(d, dict) or not all(str(d.get(lg, "")).strip() for lg in guiones):
            avisos.append(f"Al plan le falta '{k}' en todos los idiomas (lo usan miniaturas y Shorts).")

    info = {
        "existe": True,
        "titulo": plan.get("title", ""),
        "slug": plan.get("slug", ""),
        "fondos": [b.get("name") for b in fondos],
        "retratos": [p.get("name") for p in retratos],
        "escenas": len(escenas),
        "escenas_por_capitulo": {str(k): v for k, v in sorted(por_cap.items())},
        "capitulos_a_mano": [f"ch{c:02d}" for c in a_mano],
        "musica": musica,
        "creditos_imagenes": (plan.get("creditos") or {}).get("imagenes", "") if isinstance(plan.get("creditos"), dict) else "",
        "presets": sorted(cast),
        "sin_traducir": {lg: v[:40] for lg, v in sin_traducir.items()},
        "avisos": avisos[:40],
    }
    return info, problemas[:60]


# --------------------------------------------------------------------------------------------- voces y arte

def revisar_voces(pdir, guiones):
    marcas = set()
    p = os.path.join(pdir, VOZ_DE_PRUEBA)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            marcas = {ln.strip() for ln in f if ":" in ln and not ln.startswith("#")}
    out = {}
    for lg, filas in guiones.items():
        carpeta = os.path.join(pdir, LANG_CONFIG[lg]["vo"])
        listas, faltan, sin_tiempos, chars, lfs = 0, [], [], 0, 0
        for r in filas:
            lid = r.get("id")
            mp3 = os.path.join(carpeta, f"{lid}.mp3")
            if os.path.exists(mp3) and puntero_lfs(mp3):
                lfs += 1
            elif os.path.exists(mp3) and os.path.getsize(mp3) > 800:
                if os.path.exists(os.path.join(carpeta, f"{lid}.json")):
                    listas += 1
                else:
                    sin_tiempos.append(lid)
            else:
                faltan.append(lid)
                chars += len(str(r.get("speak", "")))
        out[lg] = {"total": len(filas), "listas": listas, "faltan": faltan[:40], "faltan_total": len(faltan),
                   "sin_tiempos": sin_tiempos[:40], "caracteres_pendientes": chars, "sin_bajar_lfs": lfs,
                   "de_prueba": sum(1 for m in marcas if m.startswith(f"{lg}:"))}
    return out


def revisar_arte(pdir, plan_info):
    provisorios = []
    p = os.path.join(pdir, ARTE_PROVISORIO)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            provisorios = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]

    def estado(nombres, carpeta):
        listos = [n for n in nombres if os.path.exists(os.path.join(pdir, "assets", carpeta, f"{n}.png"))]
        return {"listos": listos, "faltan": [n for n in nombres if n not in listos]}

    def archivos(rel, exts=("png", "jpg", "jpeg", "webp")):
        out = []
        for ext in exts:
            out += glob.glob(os.path.join(pdir, rel, f"*.{ext}"))
        return sorted(os.path.relpath(f, pdir).replace(os.sep, "/") for f in out)

    return {
        "fondos": estado(plan_info.get("fondos") or [], "bg"),
        "retratos": estado(plan_info.get("retratos") or [], "portraits"),
        "provisorios": provisorios,
        "candidatos": archivos(os.path.join("gen", "candidatos")),
        "referencias": archivos(os.path.join("gen", "referencias")),
    }


def _duracion(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, timeout=20)
        return round(float(out.stdout.decode().strip()), 1)
    except Exception:
        return None


def entregables(pdir):
    filas = []
    for patron in ("renders/*.mp4", "renders/shorts/*.mp4", "renders/*.png", "renders/subtitulos/*.srt",
                   "renders/shorts/*.srt", "YOUTUBE_PACK.md"):
        for f in sorted(glob.glob(os.path.join(pdir, patron))):
            nombre = os.path.basename(f)
            if nombre.startswith("video_mudo") or nombre.startswith("Master_PixelArt"):
                continue
            rel = os.path.relpath(f, pdir).replace(os.sep, "/")
            fila = {"archivo": rel, "mb": round(os.path.getsize(f) / (1024 * 1024), 2)}
            if puntero_lfs(f):
                fila["sin_bajar_lfs"] = True  # el archivo de verdad está en Git LFS y no se bajó
            elif rel.startswith("renders/") and rel.count("/") == 1 and f.endswith(".mp4"):
                fila["segundos"] = _duracion(f)  # solo los masters: medir los Shorts tarda
            filas.append(fila)
    return filas


# --------------------------------------------------------------------------------------------- todo junto

def estado_proyecto(slug):
    pdir = proyecto_dir(slug)
    meta = _leer(os.path.join(pdir, "project_meta.json"), {}) or {}
    if not isinstance(meta, dict) or "__error__" in meta:
        meta = {}
    langs = [lg for lg in (meta.get("languages") or ["es", "en", "pt"]) if lg in LANG_CONFIG]
    guion, prob_guion, guiones = revisar_guion(pdir, langs)
    plan, prob_plan = revisar_plan(pdir, guiones)
    voces = revisar_voces(pdir, guiones)
    arte = revisar_arte(pdir, plan)
    hojas = sorted(os.path.relpath(f, pdir).replace(os.sep, "/") for f in glob.glob(os.path.join(pdir, "frames", "*.png")))
    archivos = entregables(pdir)

    pendientes = []
    for lg in langs:
        if not guion.get(lg):
            pendientes.append(f"Guion en {lg.upper()}")
    if not plan.get("existe") and not plan.get("capitulos_a_mano"):
        pendientes.append("Plan de producción (production_plan.json)")
    for lg, v in voces.items():
        if lg not in langs:
            continue
        if v["faltan_total"]:
            pendientes.append(f"Voces {lg.upper()}: faltan {v['faltan_total']} de {v['total']} ({v['caracteres_pendientes']} caracteres)")
        if v["sin_tiempos"]:
            pendientes.append(f"Voces {lg.upper()}: {len(v['sin_tiempos'])} sin tiempos (sincronizar con Whisper)")
        if v["de_prueba"]:
            pendientes.append(f"Voces {lg.upper()}: {v['de_prueba']} son de PRUEBA (no se entregan)")
        if v.get("sin_bajar_lfs"):
            pendientes.append(f"Voces {lg.upper()}: {v['sin_bajar_lfs']} están en Git LFS sin bajar (git lfs pull en la carpeta del repo)")
    faltan_arte = arte["fondos"]["faltan"] + arte["retratos"]["faltan"]
    if faltan_arte:
        pendientes.append(f"Arte: faltan {len(faltan_arte)} imágenes ({', '.join(faltan_arte[:6])})")
    if arte["provisorios"]:
        pendientes.append(f"Arte: {len(arte['provisorios'])} imágenes PROVISORIAS, no son de IA")
    nombres = {os.path.basename(a["archivo"]) for a in archivos}
    for lg in langs:
        master = f"{plan.get('slug') or ''}_{lg.upper()}.mp4"
        if plan.get("slug") and master not in nombres:
            pendientes.append(f"Master {lg.upper()} (renders/{master})")
    sin_bajar = [a["archivo"] for a in archivos if a.get("sin_bajar_lfs")]
    if sin_bajar:
        pendientes.append(f"{len(sin_bajar)} entregables están en Git LFS sin bajar (git lfs pull): {', '.join(sin_bajar[:4])}")
    if not any(a["archivo"].startswith("renders/shorts/") and a["archivo"].endswith(".mp4") for a in archivos):
        pendientes.append("Shorts por capítulo (renders/shorts/)")
    if not any(a["archivo"].endswith(".srt") for a in archivos):
        pendientes.append("Subtítulos .srt")
    problemas = prob_guion + prob_plan

    return {
        "proyecto": os.path.basename(pdir),
        "titulo": meta.get("title", ""),
        "idiomas": langs,
        "etapa": meta.get("stage_name", ""),
        "actualizado": meta.get("updated_at", ""),
        "guion": guion,
        "plan": plan,
        "voces": voces,
        "arte": arte,
        "hojas": hojas,
        "entregables": archivos,
        "claves": {"elevenlabs": tiene_clave("elevenlabs_api_key"), "gemini": tiene_clave("gemini_api_key"),
                   "openai": tiene_clave("openai_api_key")},
        "problemas": problemas,
        "pendientes": pendientes,
        "listo_para_entregar": not pendientes and not problemas,
    }


def lista():
    out = []
    if not os.path.isdir(PROJECTS_DIR):
        return out
    for d in sorted(os.listdir(PROJECTS_DIR)):
        pdir = os.path.join(PROJECTS_DIR, d)
        if not os.path.isdir(os.path.join(pdir, "engine")):
            continue
        meta = _leer(os.path.join(pdir, "project_meta.json"), {}) or {}
        if not isinstance(meta, dict) or "__error__" in meta:
            meta = {}
        out.append({"proyecto": d, "titulo": meta.get("title", ""), "etapa": meta.get("stage_name", ""),
                    "idiomas": meta.get("languages") or [], "actualizado": meta.get("updated_at", "")})
    return out


def main():
    utf8_console()
    ap = argparse.ArgumentParser(description="Estado de un proyecto Pixeloide.")
    ap.add_argument("proyecto", nargs="?")
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.lista or not args.proyecto:
        data = lista()
        if args.json:
            print(json.dumps(data, ensure_ascii=False))
        else:
            for p in data:
                print(f"{p['proyecto']:32s} {p['titulo'][:40]:40s} {p['etapa']}")
        return
    data = estado_proyecto(args.proyecto)
    if args.json:
        print(json.dumps(data, ensure_ascii=False))
        return
    print(f"{data['proyecto']} — {data['titulo']} ({', '.join(data['idiomas'])})")
    for k in ("problemas", "pendientes"):
        print(f"\n{k.upper()}:")
        for x in data[k] or ["(nada)"]:
            print(f"  - {x}")
    print("\nENTREGABLES:")
    for a in data["entregables"] or [{"archivo": "(ninguno)", "mb": 0}]:
        print(f"  {a['archivo']:60s} {a['mb']:8.2f} MB" + (f"  {a['segundos']} s" if a.get("segundos") else ""))


if __name__ == "__main__":
    main()
