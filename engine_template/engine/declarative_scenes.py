"""Motor de escenas declarativo 16-bit (`declarative_scenes.py`).
Lee `production_plan.json` en la raíz del proyecto y construye dinámicamente:
- Todas las escenas animadas a 30/60 fps sincronizadas con `TL.s(lid)` y `TL.e(lid)`
- Personajes siempre apoyados sobre el piso (`feet=260..264`) con proporciones coherentes
- Cajas RPG (`window`) auto-ajustadas al ancho real del texto en ES, EN y PT para que jamás desborden
- Banda sonora chiptune procedural (`music(A)`) y efectos de sonido (`sfx(A)`) sincronizados al milisegundo
"""
import glob
import json
import math
import os
import re

from PIL import Image, ImageDraw
from common import *  # noqa

PLAN_PATH = os.path.join(ROOT, "production_plan.json")
PLAN = json.load(open(PLAN_PATH, encoding="utf-8")) if os.path.exists(PLAN_PATH) else {}

# Capítulos que ya tienen su módulo escrito a mano (engine/chNN.py): acá no se dibujan ni suenan.
_HECHOS = {int(os.path.basename(p)[2:4]) for p in
           glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch[0-9][0-9].py"))}


def _capitulo(lid):
    m = re.match(r"^c(\d+)_", str(lid or ""))
    return int(m.group(1)) if m else 0

PHOSPHOR = (100, 255, 140)
# El robot «La Máquina» va solo en documentales de IA: production_plan.json lo pide con "robot": true.
ROBOT = PLAN.get("robot") is True
RED_STAMP = (235, 65, 65)


def _char_spec(c_dict):
    """Convierte un diccionario de personaje del plan en un spec compatible con sprites.py."""
    if isinstance(c_dict, str):
        return c_dict if c_dict in S.CAST else "inge"
    preset = c_dict.get("preset", "inge")
    base = dict(S.CAST.get(preset, S.CAST["inge"]))
    for k in ("skin", "hair", "hair_style", "shirt", "pants", "glasses", "tie", "coat", "beard", "skirt"):
        if k in c_dict and c_dict[k] is not None:
            val = c_dict[k]
            base[k] = tuple(val) if isinstance(val, list) else val
    return base


def _safe_header_banner(cv, title, subtitle, t, t0, border=GOLD):
    """Banner superior centrado que ajusta su ancho y fuente automáticamente para nunca desbordar."""
    p = ease_out(prog(t, t0, t0 + 0.35))
    if p <= 0:
        return
    dy = int((1.0 - p) * -18)
    tw16, _ = text_size(title, "press", 16)
    fsize = 16 if tw16 <= 420 else 8
    tw_main, _ = text_size(title, "press", fsize)
    tw_sub, _ = text_size(subtitle, "silk", 8) if subtitle else (0, 0)
    bw = min(464, max(260, max(tw_main, tw_sub) + 32))
    bh = 44 if subtitle else 30
    bx = 240 - bw // 2
    by = 8 + dy
    window(cv, bx, by, bw, bh, fill=(16, 20, 46), border=border, alpha=0.94 * p)
    ty = by + (8 if fsize == 16 else 10)
    draw_text(cv, title, 240, ty, "press", fsize, GOLD, align="center",
              reveal=(t - t0) * 32, alpha=p)
    if subtitle:
        draw_text(cv, subtitle, 240, by + bh - 14, "silk", 8, CYAN, align="center",
                  reveal=max(0.0, (t - t0 - 0.15) * 40), alpha=p)


def _safe_info_box(cv, x, y, title, lines, t, t0, border=GOLD, min_w=160, max_w=236):
    """Caja RPG que mide el texto traducido y envuelve líneas largas para jamás salirse del margen."""
    a, dy = pop(t, t0)
    if a <= 0:
        return
    tw_t, _ = text_size(title, "press", 8) if title else (0, 0)
    wrapped = []
    content_w = max(min_w - 20, min(max_w - 20, tw_t))
    for item in lines:
        txt = item[0] if isinstance(item, (list, tuple)) else str(item)
        col = tuple(item[1]) if isinstance(item, (list, tuple)) and len(item) > 1 else CREAM
        # envolvemos si supera max_w - 20
        words = tr(txt, "silk").split()
        cur = ""
        for w in words:
            cand = (cur + " " + w).strip()
            cw, _ = text_size(cand, "silk", 8)
            if cw <= max_w - 20 or not cur:
                cur = cand
            else:
                wrapped.append((cur, col))
                content_w = max(content_w, text_size(cur, "silk", 8)[0])
                cur = w
        if cur:
            wrapped.append((cur, col))
            content_w = max(content_w, text_size(cur, "silk", 8)[0])

    box_w = min(max_w, max(min_w, content_w + 22))
    box_h = (22 if title else 10) + len(wrapped) * 13 + 8
    bx = max(8, min(W - box_w - 8, int(x)))
    by = max(8, min(H - box_h - 8, int(y + dy)))
    window(cv, bx, by, box_w, box_h, fill=(18, 22, 50), border=border, alpha=0.94 * a)
    cy = by + 8
    if title:
        draw_text(cv, title, bx + box_w // 2, cy, "press", 8, GOLD, align="center", alpha=a)
        ImageDraw.Draw(cv).line([(bx + 8, cy + 11), (bx + box_w - 8, cy + 11)], fill=(*GOLD_D, int(220 * a)))
        cy += 16
    for idx, (ltxt, lcol) in enumerate(wrapped):
        draw_text(cv, ltxt, bx + box_w // 2, cy + idx * 13, "silk", 8, lcol, align="center", alpha=a)


def _render_scene_spec(sc_spec):
    """Construye la función `fn(t)` para una escena del plan de producción."""
    lid = sc_spec.get("line_id") or sc_spec.get("start_line")
    end_lid = sc_spec.get("end_line") or lid
    t0 = TL.s(lid) if lid in TL.lines else float(sc_spec.get("t0", 0.0))
    t1 = TL.e(end_lid) if end_lid in TL.lines else (t0 + 6.0)
    layout = sc_spec.get("layout", "dialogue_scene")
    bg_name = sc_spec.get("bg", "bg_main")
    header = sc_spec.get("header", "")
    subheader = sc_spec.get("subheader", "")
    year_badge = sc_spec.get("year", "")
    lt = sc_spec.get("lower_third")
    chars = sc_spec.get("characters", [])
    cards = sc_spec.get("cards", [])
    por_name = sc_spec.get("portrait")
    weather = sc_spec.get("weather")

    if layout == "chapter_card":
        ch_num = int(sc_spec.get("chapter", 1))
        ch_lines = sc_spec.get("title_lines") or [header or f"CAPÍTULO {ch_num}"]
        ch_years = sc_spec.get("years") or subheader or year_badge or ""
        return make_card(ch_num, ch_lines, ch_years, snow=(weather == "snow"), robot_face="happy" if ROBOT else None)

    def fn(t):
        dt = max(0.0, t - t0)
        # 1. Placa de título principal (estilo Apertura)
        if layout == "title_card":
            cv = vgradient((4, 12, 16), (10, 26, 36), 12)
            STARS.draw(cv, t * 0.6, alpha=0.75)
            p_open = ease_out(prog(t, t0, t0 + 0.5))
            bw, bh = int(436 * p_open), 146
            if bw > 20:
                window(cv, 240 - bw // 2, 54, bw, bh, fill=(8, 18, 28), border=PHOSPHOR, alpha=0.95)
            if p_open >= 0.95:
                if year_badge:
                    draw_text(cv, year_badge, 240, 72, "silk", 8, CYAN, align="center", reveal=dt * 30)
                main_t = header or PLAN.get("title", "PIXELOIDE DOCUMENTARY")
                f_sz = 16 if text_size(main_t, "press", 16)[0] <= 406 else 8
                draw_text(cv, main_t, 240, 104, "press", f_sz, align="center", gradient=GOLD_RAMP,
                          outline_w=2, reveal=max(0.0, (dt - 0.2) * 24))
                if subheader:
                    draw_text(cv, subheader, 240, 142, "press", 8, PHOSPHOR, align="center",
                              reveal=max(0.0, (dt - 0.55) * 32))
                # Punto de fósforo rebotando
                bx = int(240 + math.sin(t * 2.6) * 140)
                by = int(176 - abs(math.cos(t * 5.2)) * 14)
                draw_phosphor_dot(cv, bx, by, r=3)
            if ROBOT:
                robot(cv, 442, 256, t, face="excited", scale=1)
            return vignette(cv, 0.28)

        # 2. Pantalla dividida comparativa (Split VS / 1958 vs 2026)
        if layout == "split_vs":
            bg_left = bg(sc_spec.get("bg_left", bg_name)).copy()
            bg_right = bg(sc_spec.get("bg_right", bg_name)).copy()
            cv = new_canvas(INK)
            cv.paste(bg_left.crop((0, 0, 240, H)), (0, 0))
            p_r = ease_out(prog(t, t0 + 0.35, t0 + 0.9))
            if p_r > 0:
                rw = int(240 * p_r)
                cv.paste(bg_right.crop((240, 0, 240 + rw, H)), (240, 0))
            d = ImageDraw.Draw(cv)
            d.line([(240, 0), (240, H)], fill=(*GOLD, 255), width=2)
            _safe_header_banner(cv, header, subheader, t, t0)
            for idx, c_box in enumerate(cards[:2]):
                cx = 16 if idx == 0 else 252
                _safe_info_box(cv, cx, 64, c_box.get("title", ""), c_box.get("lines", []),
                               t, t0 + 0.3 + idx * 0.35, border=PHOSPHOR if idx == 0 else CYAN,
                               min_w=190, max_w=212)
            for idx, ch_item in enumerate(chars[:2]):
                cx = ch_item.get("x", 92 if idx == 0 else 388)
                char(cv, _char_spec(ch_item), cx, 260, t, scale=int(ch_item.get("scale", 2)),
                     talk=talk_v(t, TL.speaking(t) is not None), mood=ch_item.get("mood", "happy"))
            return vignette(cv, 0.25)

        # 3. Escena general sobre fondo 16-bit
        cv = bg(bg_name).copy()
        d = ImageDraw.Draw(cv)

        if weather == "rain":
            RAIN.draw(cv, t, alpha=190)
        elif weather == "snow":
            SNOW.draw(cv, t, density=0.75)
        elif weather == "confetti":
            CONF.draw(cv, t - t0)

        # Detalles procedurales según arquetipo
        if layout == "lab_scene":
            # Osciloscopio de escritorio con onda verde estrictamente dentro del monitor (x=293..311, y=148..166)
            d.rectangle([291, 146, 313, 168], fill=(10, 26, 16, 255), outline=(90, 120, 95, 255))
            pts = []
            for x_osc in range(293, 312):
                y_osc = 157 + math.sin((x_osc - 293) * 0.55 - t * 9.0) * 5.0
                pts.append((x_osc, max(149, min(165, int(round(y_osc))))))
            if len(pts) > 1:
                d.line(pts, fill=(*PHOSPHOR, 255), width=1)
        elif layout == "living_room_tv":
            # Pantalla de TV encuadrada dentro del bisel (x=211..309, y=70..129)
            d.rectangle([211, 70, 309, 129], fill=(14, 24, 54, 255), outline=(60, 80, 130, 255))
            bx = int(260 + math.sin(t * 3.8) * 34)
            by = int(102 + math.cos(t * 2.7) * 14)
            draw_phosphor_dot(cv, bx, by, r=2, color=CYAN)
        elif layout == "data_bars":
            # Gráfico de barras animado
            bars_data = sc_spec.get("bars") or [("1980", 0.25, CYAN), ("2000", 0.55, GOLD), ("2026", 0.95, PHOSPHOR)]
            window(cv, 44, 62, 392, 144, fill=(14, 18, 42), border=GOLD, alpha=0.94)
            for bi, b_item in enumerate(bars_data[:4]):
                blab = b_item[0]
                bval = float(b_item[1])
                bcol = tuple(b_item[2]) if len(b_item) > 2 else GOLD
                p_b = ease_out(prog(t, t0 + 0.25 + bi * 0.2, t0 + 0.95 + bi * 0.2))
                by_bar = 80 + bi * 30
                draw_text(cv, str(blab), 58, by_bar + 4, "press", 8, CREAM)
                max_bw = 260
                cur_bw = max(4, int(max_bw * bval * p_b))
                d.rectangle([148, by_bar, 148 + cur_bw, by_bar + 16], fill=(*bcol, 255), outline=(*INK, 255))

        # Banner superior si existe
        if header:
            _safe_header_banner(cv, header, subheader, t, t0)

        # Año grande si existe y no hay banner que lo tape
        if year_badge and not header:
            bigyear(cv, str(year_badge), 240, 22, t, t0, size=32)

        # Retrato pixel-art 64x64 si la escena lo incluye
        if por_name:
            px_x = sc_spec.get("portrait_x", 24)
            px_y = sc_spec.get("portrait_y", 64)
            portrait_card(cv, por_name, px_x, px_y)

        # Tarjetas informativas RPG auto-ajustadas
        for idx, c_box in enumerate(cards[:2]):
            cx = c_box.get("x", 248 if por_name or chars else (24 if idx == 0 else 248))
            cy = c_box.get("y", 64 + idx * 68)
            _safe_info_box(cv, cx, cy, c_box.get("title", ""), c_box.get("lines", []),
                           t, t0 + 0.25 + idx * 0.3, border=GOLD if idx == 0 else CYAN)

        # Personajes apoyados SIEMPRE sobre el piso (y=260..262)
        speaking_now = TL.speaking(t) is not None
        for idx, ch_item in enumerate(chars):
            cx = int(ch_item.get("x", 110 + idx * 95))
            c_feet = int(ch_item.get("feet", 260))
            c_scale = int(ch_item.get("scale", 2))
            is_speaker = (idx == 0 and speaking_now)
            char(cv, _char_spec(ch_item), cx, c_feet, t, scale=c_scale,
                 talk=talk_v(t, is_speaker),
                 arms=ch_item.get("arms", " hip" if idx % 2 else "down").strip(),
                 mood=ch_item.get("mood", "happy"))
            if ch_item.get("bubble"):
                b_txt = ch_item["bubble"]
                b_y = c_feet - 48 * c_scale - 4
                bubble(cv, b_txt, cx, max(44, b_y), reveal=max(0.0, (dt - 0.45) * 22))

        # Sello rojo si es calendar_stamp
        if layout == "calendar_stamp" and dt > 0.75:
            stamp_txt = sc_spec.get("stamp", "DESTACADO")
            sw, _ = text_size(stamp_txt, "press", 8)
            sx = 240 - (sw + 16) // 2
            d.rectangle([sx, 186, sx + sw + 16, 206], fill=(40, 8, 12, 240), outline=(*RED_STAMP, 255), width=2)
            draw_text(cv, stamp_txt, 240, 192, "press", 8, RED_STAMP, align="center")

        # Zócalo inferior (lower_third) seguro dentro del margen
        if lt and isinstance(lt, dict):
            lower_third(cv, lt.get("title", ""), lt.get("sub", ""), t, t0 + 0.2, t1 - 0.1, x=24, y=214)

        return vignette(cv, 0.25)

    return fn


def scenes():
    out = []
    plan_scenes = PLAN.get("scenes", [])
    if not plan_scenes:
        # Fallback automático: genera 1 escena por línea del guion
        for i, lid in enumerate(TL.order):
            L = TL.lines[lid]
            if _capitulo(lid) in _HECHOS:
                continue
            if lid.endswith("_00"):
                ch_n = L["chapter"]
                out.append((L["start"] - 0.3, make_card(ch_n, [L["sub"].upper()], "", robot_face="question" if ROBOT else None), None, ch_n))
            else:
                spec = {
                    "line_id": lid,
                    "end_line": lid,
                    "layout": "title_card" if i == 0 else "dialogue_scene",
                    "header": L["sub"][:36].upper(),
                    "characters": [{"preset": "inge", "x": 110, "feet": 260, "scale": 2}],
                }
                out.append((L["start"], _render_scene_spec(spec), lambda t, s=L["start"], e=L["end"]: cam_push(t, s, e, 1.0, 1.06),
                            _capitulo(lid)))
        return out

    for sc_spec in plan_scenes:
        lid = sc_spec.get("line_id") or sc_spec.get("start_line")
        if _capitulo(lid) in _HECHOS:
            continue
        end_lid = sc_spec.get("end_line") or lid
        t0 = (TL.s(lid) - 0.3 if str(lid).endswith("_00") else TL.s(lid)) if lid in TL.lines else float(sc_spec.get("t0", 0.0))
        t1 = TL.e(end_lid) if end_lid in TL.lines else (t0 + 6.0)
        fn = _render_scene_spec(sc_spec)
        cam_kind = sc_spec.get("camera", "push")
        if cam_kind == "none" or sc_spec.get("layout") in ("chapter_card", "title_card"):
            cam = None
        else:
            cam = lambda t, a=t0, b=t1: cam_push(t, a, b, 1.0, 1.07)
        # El 4.º valor es el capítulo: así `video.py sheet ch03` encuentra también las escenas del plan.
        out.append((max(0.0, t0), fn, cam, _capitulo(lid)))
    return out


STYLE_MAP = {
    "mystery": "st_mystery",
    "build": "st_build",
    "bright": "st_bright",
    "summer": "st_summer_lead",
    "rain": "st_rain",
    "puzzle": "st_puzzle",
    "triumph": "st_triumph",
    "winter": "st_winter",
}

DEFAULT_CHORDS = [
    [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")],
    [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")],
    [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")],
    [("E", "min"), ("C", "maj"), ("G", "maj"), ("D", "maj")],
]


def music(A):
    ch_styles = PLAN.get("chapter_music", {})
    chapters = [0] + list(getattr(TL, "chapters", []))
    for idx, ch in enumerate(chapters):
        if ch in _HECHOS:
            continue
        t0 = 0.0 if ch == 0 else TL.chapter_start(ch)
        t1 = TL.chapter_start(chapters[idx + 1]) if idx + 1 < len(chapters) else (TL.e(TL.order[-1]) + 2.4 if TL.order else TL.total - 12.0)
        if t1 <= t0:
            continue
        st_name = ch_styles.get(str(ch)) or ["mystery", "build", "bright", "puzzle", "rain", "summer", "triumph", "winter"][idx % 8]
        st_fn = getattr(A, STYLE_MAP.get(st_name, "st_build"), A.st_build)
        chords = DEFAULT_CHORDS[idx % len(DEFAULT_CHORDS)]
        bpm = 108 + (idx % 4) * 6
        A.section(t0, t1, bpm, chords, st_fn)


def sfx(A):
    for sc_spec in PLAN.get("scenes", []):
        lid = sc_spec.get("line_id") or sc_spec.get("start_line")
        if not lid or lid not in TL.lines or _capitulo(lid) in _HECHOS:
            continue
        t0 = TL.s(lid)
        lay = sc_spec.get("layout", "")
        if lay == "lab_scene":
            A.hum_1958(t0, min(t0 + 6.0, TL.e(lid)))
            A.plic(t0 + 0.4)
        elif lay == "calendar_stamp":
            A.stamp_hit(t0 + 0.75)
        elif lay == "split_vs":
            A.whoosh(t0 + 0.35)
        else:
            A.pop_sfx(t0 + 0.25, 580, 0.045)
