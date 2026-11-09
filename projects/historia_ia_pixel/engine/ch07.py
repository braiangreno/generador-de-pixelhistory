"""Capítulo 7: Atención (2017 – 2022)."""
from common import *  # noqa
import numpy as np

CH = 7
C_ = S.hexc

# --------------------------------------------------------------------------- reparto local
# los ocho autores de «Attention Is All You Need» (variaciones del investigador de Google)
GOOGLERS = [
    "googler",
    dict(name="Investigador 2", skin=S.SKIN["light"], hair=C_("5a3a22"), hair_style="side", glasses="black",
         top="hoodie", top_color=C_("6a6c76"), pants=C_("2a2a34")),
    dict(name="Investigadora 3", skin=S.SKIN["olive"], hair=C_("16121a"), hair_style="bangs",
         top="blazer", top_color=C_("d84a3a"), shirt=C_("f2eee8"), pants=C_("2a2a36")),
    dict(name="Investigador 4", skin=S.SKIN["fair"], hair=C_("c8a060"), hair_style="crew",
         top="tshirt", top_color=C_("f2b830"), pants=C_("3a4a6a")),
    dict(name="Investigador 5", skin=S.SKIN["light"], hair=C_("a04a22"), hair_style="curly", glasses="wire",
         top="shirt", top_color=C_("3a9a5a"), pants=C_("4a4a52")),
    dict(name="Investigador 6", skin=S.SKIN["brown"], hair=C_("141010"), hair_style="short", beard="stubble",
         top="sweater", top_color=C_("2a5aa8"), shirt=C_("e8e4dc"), pants=C_("2a2a34")),
    dict(name="Investigador 7", skin=S.SKIN["fair"], hair=C_("2a2020"), hair_style="wavy",
         top="tshirt", top_color=C_("e8e4dc"), pants=C_("4a3e34")),
    dict(name="Investigadora 8", skin=S.SKIN["asian"], hair=C_("3a2418"), hair_style="bun",
         top="turtleneck", top_color=C_("7a4aa8"), pants=C_("26262e")),
]

# gente variada para la multitud final
CROWD_TOPS = [C_("d84a3a"), C_("3a7ad8"), C_("f2b830"), C_("3a9a5a"), C_("7a4aa8"), C_("e87aa0"), C_("e8e4dc"),
              C_("2aa8a8"), C_("a86a3a"), C_("5a5a6a")]
CROWD_HAIR = [C_("141010"), C_("5a3a22"), C_("c8a060"), C_("a04a22"), C_("2a2020"), C_("b0aca4"), C_("3a2418")]
CROWD_STYLE = ["short", "side", "curly", "long", "bun", "crew", "wavy", "bangs", "fringe", "recede"]
CROWD_SKIN = list(S.SKIN.values())
CROWD_TOPK = ["tshirt", "hoodie", "sweater", "shirt", "blazer", "turtleneck"]


def crowd_spec(k):
    return dict(name=f"Persona {k}", skin=CROWD_SKIN[(k * 5) % len(CROWD_SKIN)],
                hair=CROWD_HAIR[(k * 3) % len(CROWD_HAIR)], hair_style=CROWD_STYLE[(k * 7) % len(CROWD_STYLE)],
                top=CROWD_TOPK[(k * 4) % len(CROWD_TOPK)], top_color=CROWD_TOPS[(k * 3 + 1) % len(CROWD_TOPS)],
                shirt=C_("eeeae0"), pants=C_("2a2a3a") if k % 2 else C_("3a4a6a"),
                glasses="black" if k % 5 == 2 else None)


# --------------------------------------------------------------------------- utilidades
def wrap(text, width, fname="silk", size=8):
    lines, cur = [], ""
    for wd in text.split():
        test = (cur + " " + wd).strip()
        if text_size(test, fname, size)[0] <= width:
            cur = test
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    return lines


def typed_lines(cv, lines, x, y, n, color, fname="silk", size=8, lh=11, cursor_t=None):
    """Dibuja líneas con n caracteres visibles en total (máquina de escribir)."""
    left = int(n)
    last = None
    for i, ln in enumerate(lines):
        if left <= 0:
            break
        k = min(len(ln), left)
        draw_text(cv, ln, x, y + i * lh, fname, size, color, outline=None, shadow=False, reveal=k)
        left -= k + 1
        last = (i, ln[:k])
    if cursor_t is not None and last is not None and int(cursor_t * 4) % 2 == 0:
        i, s = last
        cx = x + text_size(s, fname, size)[0] + 2 if s else x
        ImageDraw.Draw(cv).rectangle([cx, y + i * lh, cx + 3, y + i * lh + 7], fill=(*color, 255))


def stamp(cv, text, cx, cy, t, t0, color=(226, 58, 50), angle=8, size=16):
    if t < t0:
        return
    tw, th = text_size(text, "press", size)
    w, h = tw + 20, th + 18
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.rectangle([1, 1, w - 2, h - 2], outline=(*color, 255), width=2)
    d.rectangle([4, 4, w - 5, h - 5], outline=(*color, 255))
    draw_text(tmp, text, w // 2, 9, "press", size, color, align="center", outline=None, shadow=False)
    tmp = tmp.rotate(angle, Image.NEAREST, expand=True)
    p = prog(t, t0, t0 + 0.16)
    k = 2.2 - 1.2 * p
    if k > 1.01:
        tmp = tmp.resize((int(tmp.size[0] * k), int(tmp.size[1] * k)), Image.NEAREST)
    paste(cv, tmp, cx - tmp.size[0] // 2, cy - tmp.size[1] // 2, min(1.0, 0.4 + p))


def fmt_int(v):
    return f"{int(v):,}".replace(",", ".")


def _h(i, j, s=0):
    v = (i * 73856093) ^ (j * 19349663) ^ (s * 83492791)
    return ((v * 2654435761) & 0xFFFFFFFF) / 0xFFFFFFFF


# =========================================================================== escenas

def sc_google(t):
    """2017: ocho investigadores de Google publican «Attention Is All You Need»."""
    w = TL.word
    t_2017 = w("c7_01", "dos")
    t_ocho = w("c7_01", "ocho")
    t_goo = w("c7_01", "Google")
    t_pub = w("c7_01", "publican")
    t_tit = w("c7_01", "titulo")
    t_arr = w("c7_01", "arrogante")
    t_att = w("c7_01", "Attention")
    t_all = w("c7_01", "All")
    t_end = TL.e("c7_01")
    cv = bg("bg_google_office_2017").copy()
    done = t > t_end - 0.1
    # los ocho
    for i, spec in enumerate(GOOGLERS):
        ti = t_ocho + i * 0.13
        a, dy = pop(t, ti)
        if a <= 0:
            continue
        x = 34 + i * 59
        arms, mood = "down", "neutral"
        if t > t_arr:
            arms, mood = ("cross" if i % 2 else "hold"), "happy"
        if done:
            arms, mood = "cheer", "happy"
        hop = int(abs(math.sin(t * 7 + i)) * 6) if done else 0
        char(cv, spec, x, 264 + dy - hop, t, scale=2, alpha=a, arms=arms, mood=mood,
             look=0 if t < t_pub else (1 if x < 240 else -1))
        if ti < t < ti + 1.0:
            ab, dyb = pop(t, ti)
            draw_text(cv, str(i + 1), x, 132 + dyb, "press", 16, align="center", gradient=GOLD_RAMP)
    # 2017
    if t < t_pub + 0.2:
        a_out = 1 - prog(t, t_pub - 0.2, t_pub + 0.1)
        if a_out > 0:
            p = prog(t, t_2017, t_2017 + 0.55)
            yy = 30 - (1 - ease_out_back(p, 2.2)) * 50
            draw_text(cv, "2017", 240, int(yy), "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2,
                      alpha=min(p * 3, a_out))
    # el artículo
    if t > t_pub - 0.1:
        p = ease_out(prog(t, t_pub - 0.1, t_pub + 0.4))
        x0, y0 = 122, int(10 - (1 - p) * 170)
        pw, ph = 236, 116
        draw_paper(cv, x0, y0, pw, ph)
        draw_text(cv, "ARXIV · JUNIO 2017", x0 + pw // 2, y0 + 7, "silk", 8, (130, 124, 116), align="center",
                  outline=None, shadow=False)
        d = ImageDraw.Draw(cv)
        if t < t_att:
            if t > t_tit - 0.1:
                draw_text(cv, "TÍTULO:", x0 + 18, y0 + 26, "press", 8, (150, 140, 130), outline=None, shadow=False)
            if int(t * 4) % 2 == 0:
                d.rectangle([x0 + 18 + (64 if t > t_tit - 0.1 else 0), y0 + 38, x0 + 24 + (64 if t > t_tit - 0.1
                                                                                         else 0), y0 + 50],
                            fill=(*INK, 255))
        else:
            hl = prog(t, t_end - 0.1, t_end + 0.3)
            if hl > 0:
                d.rectangle([x0 + 14, y0 + 22, x0 + 14 + int((pw - 28) * ease_out(hl)), y0 + 64],
                            fill=(255, 226, 120, 255))
            r1 = (t - t_att) * 22
            r2 = (t - t_all) * 22
            draw_text(cv, "ATTENTION IS", x0 + pw // 2, y0 + 24, "press", 16, INK, align="center", outline=None,
                      shadow=False, reveal=r1)
            draw_text(cv, "ALL YOU NEED", x0 + pw // 2, y0 + 44, "press", 16, INK, align="center", outline=None,
                      shadow=False, reveal=r2)
        draw_text(cv, "VASWANI, SHAZEER, PARMAR, USZKOREIT,", x0 + pw // 2, y0 + 72, "silk", 8, (90, 86, 96),
                  align="center", outline=None, shadow=False)
        draw_text(cv, "JONES, GOMEZ, KAISER, POLOSUKHIN", x0 + pw // 2, y0 + 82, "silk", 8, (90, 86, 96),
                  align="center", outline=None, shadow=False)
        for k in range(3):
            ll = pw - 36 - (k * 23) % 40
            d.line([(x0 + 18, y0 + 96 + k * 6), (x0 + 18 + ll, y0 + 96 + k * 6)], fill=(190, 184, 172, 255))
        if done:
            for i in range(5):
                sparkle(cv, x0 + 10 + i * 54, y0 + 20 + (i % 2) * 48, t + i * 0.5, 3, GOLD)
    lower_third(cv, "GOOGLE · 2017", "GOOGLE BRAIN · GOOGLE RESEARCH", t, t_goo - 0.25, t_att - 0.1, x=16, y=226)
    return vignette(cv, 0.3)


WORDS = [("LA", 70, 88), ("MÁQUINA", 210, 88), ("APRENDE", 380, 88),
         ("A", 80, 170), ("PRESTAR", 220, 170), ("ATENCIÓN", 384, 170)]
# pesos de atención (fila = palabra que "mira")
ATT = [[0, 3, 1, 0, 0, 1], [1, 0, 3, 0, 1, 2], [0, 3, 0, 1, 2, 3],
       [0, 0, 2, 0, 3, 1], [0, 1, 2, 1, 0, 4], [0, 3, 2, 0, 4, 0]]


def puzzle_piece(d, x, y, s, col, knobs=(), border=INK):
    """Pieza de rompecabezas cuadrada con perillas (lados en `knobs`: 'r','b','l','t')."""
    r = s // 6
    d.rectangle([x, y, x + s, y + s], fill=(*col, 255), outline=(*border, 255))
    for k in knobs:
        cx, cy = {"r": (x + s + r - 1, y + s // 2), "b": (x + s // 2, y + s + r - 1),
                  "l": (x - r + 1, y + s // 2), "t": (x + s // 2, y - r + 1)}[k]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, 255), outline=(*border, 255))
    d.line([(x + 2, y + 2), (x + s - 3, y + 2)], fill=(*tuple(min(255, int(v * 1.25)) for v in col), 255))


def sc_attention(t):
    """El transformer lee todas las palabras a la vez y aprende a qué prestarle atención. La pieza que faltaba."""
    w = TL.word
    t_tr = w("c7_02", "transformer")
    t_arq = w("c7_02", "arquitectura")
    t_lee = w("c7_02", "lee")
    t_vez = w("c7_02", "vez")
    t_apr = w("c7_02", "aprende")
    t_es = w("c7_02", "es la pieza")
    t_falta = w("c7_02", "faltaba")
    cv = vgradient((4, 6, 18), (14, 24, 52), 10)
    STARS.draw(cv, t, alpha=0.5)
    d = ImageDraw.Draw(cv)
    dim = 1 - 0.7 * prog(t, t_es - 0.3, t_es + 0.1)
    if t > t_tr - 0.1:
        a, dy = pop(t, t_tr - 0.1, 0.4)
        draw_text(cv, "TRANSFORMER", 240, 14 + dy, "press", 24, align="center", gradient=CYAN_RAMP, outline_w=2)
    # líneas de atención
    if t > t_apr - 0.1 and dim > 0.5:
        focus = int((t - t_apr) / 0.45) % 6
        for i in range(6):
            for j in range(6):
                wgt = ATT[i][j]
                if i != focus or wgt == 0:
                    continue
                (_, xa, ya), (_, xb, yb) = WORDS[i], WORDS[j]
                pulse = 0.5 + 0.5 * math.sin(t * 9 + j)
                width = max(1, int(wgt * (0.6 + 0.4 * pulse)))
                col = (90 + 40 * wgt, 200 + 13 * wgt, 255)
                d.line([(xa, ya + 8), (xb, yb + 8)], fill=(*col, 255), width=width)
                # paquete de luz viajando
                k = ((t * 1.6 + j * 0.17) % 1.0)
                px, py = xa + (xb - xa) * k, ya + 8 + (yb - ya) * k
                d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(240, 255, 255, 255))
    # palabras
    flash = prog(t, t_lee, t_lee + 0.1) * (1 - prog(t, t_vez + 0.3, t_vez + 0.8))
    from i18n import get_lang
    for k, (wd, x, y) in enumerate(WORDS):
        if k == 3 and wd == "A" and get_lang() == "en":
            wd = "TO"
        a, dy = pop(t, t_arq - 0.2 + k * 0.08)
        if a <= 0:
            continue
        tw, _ = text_size(wd, "press", 16)
        focus = t > t_apr - 0.1 and int((t - t_apr) / 0.45) % 6 == k
        border = CYAN if (flash > 0 or focus) else (70, 90, 140)
        fill = (16, 50, 70) if (flash > 0 or focus) else (16, 20, 44)
        if dim < 0.6:
            border, fill = (40, 50, 80), (10, 12, 28)
        window(cv, x - tw // 2 - 8, y - 6 + dy, tw + 16, 30, fill=fill, border=border)
        col = CREAM if dim > 0.6 else (70, 76, 100)
        draw_text(cv, wd, x, y + 2 + dy, "press", 16, (220, 250, 255) if flash > 0 or focus else col,
                  align="center")
    if flash > 0:
        draw_text(cv, "TODAS LAS PALABRAS A LA VEZ", 240, 222, "press", 8, CYAN, align="center",
                  reveal=(t - t_lee) * 40)
    elif t > t_apr and dim > 0.5:
        draw_text(cv, "¿A QUÉ PRESTAR ATENCIÓN?", 240, 222, "press", 8, GOLD, align="center",
                  reveal=(t - t_apr) * 40)
    # la pieza que faltaba
    if t > t_es - 0.3:
        a = prog(t, t_es - 0.3, t_es)
        s = 34
        x0, y0 = 240 - int(1.5 * s), 100
        gold = (214, 168, 80)
        cells = [(0, 0, ("r", "b")), (1, 0, None), (2, 0, ("b",)), (0, 1, ("r",)), (1, 1, ("r",)), (2, 1, ())]
        # hueco
        d.rectangle([x0 + s, y0, x0 + 2 * s, y0 + s], fill=(6, 8, 18, 255), outline=(60, 50, 30, 255))
        for (cx, cy, kn) in cells:
            if kn is None:
                continue
            puzzle_piece(d, x0 + cx * s, y0 + cy * s, s, gold, kn)
        p = prog(t, t_falta - 0.45, t_falta)
        if p > 0:
            yy = int(y0 - (1 - ease_in_out(p)) * 90)
            col = (90, 220, 255) if p < 1 else ((200, 250, 255) if t < t_falta + 0.12 else CYAN)
            puzzle_piece(d, x0 + s, yy, s, col, ("r", "b"), border=(20, 60, 90))
            draw_text(cv, "T", x0 + s + s // 2, yy + 10, "press", 16, NAVY, align="center", outline=None,
                      shadow=False)
        if t > t_falta:
            for i in range(6):
                ang = i * math.pi / 3 + t
                sparkle(cv, int(240 + math.cos(ang) * 70), int(y0 + s + math.sin(ang) * 44), t + i * 0.4, 3,
                        CYAN if i % 2 else GOLD)
            a2, dy2 = pop(t, t_falta)
            draw_text(cv, "LA PIEZA QUE FALTABA", 240, 196 + dy2, "press", 8, GOLD, align="center")
    return vignette(cv, 0.4)


PAGES = ["WWW", "WIKI", "</>", "NEWS", "BLOG", "FORO", "LIBRO", "@", "PDF", "Q&A"]


def iso_cube(cv, cx, by, s, t, glow=1.0):
    d = ImageDraw.Draw(cv)
    hx = int(s * 0.87)
    top = [(cx, by - s), (cx - hx, by - s - s // 2), (cx, by - 2 * s), (cx + hx, by - s - s // 2)]
    left = [(cx, by), (cx - hx, by - s // 2), (cx - hx, by - s - s // 2), (cx, by - s)]
    right = [(cx, by), (cx + hx, by - s // 2), (cx + hx, by - s - s // 2), (cx, by - s)]
    d.polygon(left, fill=(24, 70, 110, 255), outline=(*INK, 255))
    d.polygon(right, fill=(14, 44, 76, 255), outline=(*INK, 255))
    d.polygon(top, fill=(60, 150, 200, 255), outline=(*INK, 255))
    # rejilla de neuronas en las caras
    n = max(2, s // 12)
    for i in range(1, n):
        f = i / n
        d.line([(cx - hx * f, by - s // 2 * f), (cx - hx * f, by - s // 2 * f - s)], fill=(40, 110, 160, 255))
        d.line([(cx + hx * f, by - s // 2 * f), (cx + hx * f, by - s // 2 * f - s)], fill=(26, 74, 116, 255))
        d.line([(cx, by - s * f), (cx - hx, by - s // 2 - s * f)], fill=(40, 110, 160, 255))
        d.line([(cx, by - s * f), (cx + hx, by - s // 2 - s * f)], fill=(26, 74, 116, 255))
    for i in range(n * 2):
        k = _h(i, int(t * 6)) > 0.6
        if k:
            fx, fy = _h(i, 3), _h(i, 5)
            px = int(cx - hx * fx)
            py = int(by - s // 2 * fx - s * fy)
            d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(160, 250, 255, 255))
    d.line([top[2], top[1]], fill=(140, 230, 255, 255))
    d.line([top[2], top[3]], fill=(140, 230, 255, 255))


def sc_llm(t):
    """Modelos de lenguaje cada vez más grandes, entrenados con el texto de internet."""
    w = TL.word
    t0 = TL.s("c7_03")
    t_mod = w("c7_03", "modelos")
    steps = [w("c7_03", "construyen"), w("c7_03", "cada"), w("c7_03", "grandes")]
    t_ent = w("c7_03", "entrenados")
    t_int = w("c7_03", "internet")
    cv = vgradient((6, 6, 16), (20, 18, 44), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 24):
        d.line([(x, 200), (240 + (x - 240) * 3, H)], fill=(30, 30, 62, 255))
    d.line([(0, 200), (W, 200)], fill=(50, 50, 96, 255))
    if t > t_mod - 0.1:
        a, dy = pop(t, t_mod - 0.1)
        draw_text(cv, "MODELOS DE LENGUAJE", 240, 12 + dy, "press", 16, align="center", gradient=CREAM_RAMP)
    # flujo de páginas de internet hacia el modelo
    lvl = sum(1 for s in steps if t > s) - 1
    sizes = [26, 46, 70]
    labels = [("GPT-1", "2018 · GRANDE"), ("GPT-2", "2019 · MÁS GRANDE"),
              ("GPT-3", "2020 · MUCHO MÁS GRANDE")]
    cx, by = 330, 196
    dens = 0.35 + 0.65 * prog(t, t_ent - 0.2, t_ent + 0.6)
    for k in range(18):
        if _h(k, 9) > dens:
            continue
        sp = 0.55 + _h(k, 1) * 0.35
        ph = (t * sp + _h(k, 2)) % 1.0
        sx = -40 + ph * (cx - 10 + 40)
        sy0 = 60 + _h(k, 3) * 130
        sy = sy0 + (by - 60 - sy0) * ph ** 2
        sc = 1 - 0.7 * ph ** 3
        if ph > 0.92:
            continue
        pw, phh = int(34 * sc), int(24 * sc)
        x1, y1 = int(sx), int(sy)
        d.rectangle([x1, y1, x1 + pw, y1 + phh], fill=(236, 232, 220, 255), outline=(*INK, 255))
        d.rectangle([x1 + 1, y1 + 1, x1 + pw - 1, y1 + 4], fill=(90, 140, 200, 255))
        if sc > 0.75:
            draw_text(cv, PAGES[k % len(PAGES)], x1 + pw // 2, y1 + 8, "silk", 8, INK, align="center", outline=None,
                      shadow=False)
        else:
            for ll in range(2):
                d.line([(x1 + 3, y1 + 8 + ll * 4), (x1 + pw - 4, y1 + 8 + ll * 4)], fill=(150, 146, 140, 255))
    if t > t_ent - 0.1:
        a, dy = pop(t, t_ent - 0.1)
        draw_text(cv, "TEXTO DE INTERNET", 86, 44 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, ">>>", 86, 56 + dy, "press", 8, GOLD, align="center")
    # el modelo
    if lvl >= 0:
        p = ease_out_back(prog(t, steps[lvl], steps[lvl] + 0.35))
        prev = sizes[lvl - 1] if lvl > 0 else 0
        s = int(prev + (sizes[lvl] - prev) * p)
        if s > 4:
            cv = spotlight(cv, cx, 0, by, 20, sizes[lvl] * 3, strength=0.12)
            iso_cube(cv, cx, by, s, t)
        name, sub = labels[lvl]
        draw_text(cv, name, cx, 208, "press", 16, align="center", gradient=CYAN_RAMP)
        draw_text(cv, sub, cx, 230, "silk", 8, GREY, align="center")
        # miniaturas de los anteriores
        for j in range(lvl):
            mx = 150 + j * 44
            draw_text(cv, labels[j][0], mx + 16, 244, "silk", 8, (110, 120, 150), align="center")
            iso_cube(cv, mx + 16, 238, 8 + j * 4, t)
    # Sam Altman e Ilya Sutskever (OpenAI) construyendo los modelos GPT
    for idx, (sp_key, xx) in enumerate((("altman", 42), ("sutskever", 96))):
        a_s, dy_s = pop(t, t0 + 0.15 + idx * 0.12)
        if a_s > 0:
            char(cv, sp_key, xx, 262 + dy_s, t, scale=2, alpha=a_s,
                 arms="point" if (lvl >= 0 and idx == 0) else "hold",
                 mood="happy" if lvl >= 1 else "neutral", look=1)
    if t > t_int:
        for i in range(4):
            sparkle(cv, cx - 60 + i * 40, 60 + (i % 2) * 30, t + i * 0.6, 3, CYAN)
    return vignette(cv, 0.4)


def laptop_back(cv, x, y, w=54, h=34):
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + w, y + h], fill=(70, 72, 82, 255), outline=(*INK, 255))
    d.rectangle([x + 2, y + 2, x + w - 2, y + 3], fill=(100, 102, 114, 255))
    d.ellipse([x + w // 2 - 4, y + h // 2 - 4, x + w // 2 + 4, y + h // 2 + 4], fill=(150, 152, 164, 255))
    d.rectangle([x - 6, y + h, x + w + 6, y + h + 4], fill=(110, 112, 124, 255), outline=(*INK, 255))


def chat_window(cv, x, y, w, h, t, header, msgs, badge=None, title_glow=0.0):
    d = ImageDraw.Draw(cv)
    d.rectangle([x + 3, y + 3, x + w + 3, y + h + 3], fill=(0, 0, 0, 120))
    d.rectangle([x, y, x + w, y + h], fill=(247, 247, 248, 255), outline=(*INK, 255))
    d.rectangle([x + 1, y + 1, x + w - 1, y + 18], fill=(32, 33, 42, 255))
    d.rectangle([x + 6, y + 5, x + 15, y + 14], fill=(16, 163, 127, 255))
    d.rectangle([x + 9, y + 8, x + 12, y + 11], fill=(240, 255, 250, 255))
    col = CREAM if title_glow <= 0 else ((255, 240, 160) if int(t * 8) % 2 else CREAM)
    draw_text(cv, header, x + 22, y + 6, "press", 8, col, outline=None, shadow=False)
    for i in range(3):
        d.ellipse([x + w - 30 + i * 8, y + 7, x + w - 26 + i * 8, y + 11], fill=(90, 92, 104, 255))
    if badge:
        bw, _ = text_size(badge, "silk", 8)
        bx = x + w - 40 - bw
        d.rectangle([bx - 4, y + 4, bx + bw + 3, y + 14], fill=(250, 200, 80, 255))
        draw_text(cv, badge, bx, y + 6, "silk", 8, INK, outline=None, shadow=False)
    yy = y + 24
    for (who, text, t0, rate) in msgs:
        if t < t0:
            break
        orig_len = len(text)
        text = tr(text, "silk")
        if orig_len > 0 and len(text) != orig_len:
            rate = rate * len(text) / orig_len
        lines = wrap(text, w - 40)
        rh = 10 + 11 * len(lines)
        if who == "bot":
            d.rectangle([x + 1, yy - 3, x + w - 1, yy + rh - 3], fill=(236, 236, 241, 255))
            d.rectangle([x + 6, yy, x + 17, yy + 11], fill=(16, 163, 127, 255))
            d.rectangle([x + 8, yy + 3, x + 9, yy + 5], fill=(255, 255, 255, 255))
            d.rectangle([x + 14, yy + 3, x + 15, yy + 5], fill=(255, 255, 255, 255))
            d.line([(x + 9, yy + 8), (x + 14, yy + 8)], fill=(255, 255, 255, 255))
        else:
            d.rectangle([x + 6, yy, x + 17, yy + 11], fill=(150, 90, 200, 255))
            draw_text(cv, "TÚ", x + 12, yy + 2, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        n = (t - t0) * rate
        if who == "bot" and n < 0:
            pass
        if who == "bot" and (t - t0) < 0.5:
            for k in range(3):
                if int((t - t0) * 8) % 3 >= k:
                    d.rectangle([x + 26 + k * 6, yy + 5, x + 28 + k * 6, yy + 7], fill=(90, 92, 104, 255))
        else:
            if who == "bot":
                n = (t - t0 - 0.5) * rate
            typed_lines(cv, lines, x + 24, yy + 2, n, (52, 53, 65), cursor_t=t if n < len(text) else None)
        yy += rh + 4
    # caja de entrada
    d.rectangle([x + 8, y + h - 20, x + w - 8, y + h - 7], fill=(255, 255, 255, 255), outline=(200, 200, 210, 255))
    draw_text(cv, "ENVIAR UN MENSAJE...", x + 14, y + h - 17, "silk", 8, (160, 160, 170), outline=None, shadow=False)
    d.rectangle([x + w - 20, y + h - 17, x + w - 13, y + h - 10], fill=(16, 163, 127, 255))


def sc_chat(t):
    """30 de noviembre de 2022: OpenAI lanza ChatGPT."""
    w = TL.word
    t_30 = w("c7_04", "treinta")
    t_oai = w("c7_04", "OpenAI")
    t_vp = w("c7_04", "vista")
    t_gpt = w("c7_04", "ChatGPT")
    cv = bg("bg_living_room_2022").copy()
    q_t0 = t_oai + 0.9
    q = "¿LAS MÁQUINAS PUEDEN PENSAR?"
    a_t0 = q_t0 + len(q) / 22 + 0.3
    typing = q_t0 - 0.1 < t < q_t0 + len(q) / 22
    reading = t > a_t0
    char(cv, "user", 156, 232, t, sit=True, scale=3, arms="type" if typing else "hold",
         mood="happy" if t > t_gpt - 0.3 else "neutral", look=1 if t > t_oai else 0)
    laptop_back(cv, 130, 156)
    # brillo de la pantalla
    if t > t_oai - 0.3:
        ImageDraw.Draw(cv).line([(132, 155), (182, 155)], fill=(170, 240, 220, 255))
    # Sam Altman presentando ChatGPT
    if t > t_oai - 0.15:
        a_sa, dy_sa = pop(t, t_oai - 0.15, 0.35)
        char(cv, "altman", 50, 264 + dy_sa, t, scale=3, alpha=a_sa,
             arms="point" if t > t_gpt - 0.1 else "wave", mood="happy", look=1)
        a_card = min(a_sa, 1 - prog(t, t_gpt + 0.8, t_gpt + 1.2))
        if a_card > 0:
            off = int((1 - ease_out(a_card)) * -120)
            portrait_card(cv, "sam_altman", 10 + off, 8)
            window(cv, 80 + off, 18, 138, 42)
            draw_text(cv, "SAM ALTMAN", 88 + off, 26, "press", 8, CREAM)
            draw_text(cv, "CEO · OPENAI", 88 + off, 42, "silk", 8, GOLD)
    # tarjeta de fecha
    if t_30 - 0.15 < t < t_oai - 0.1:
        a, dy = pop(t, t_30 - 0.15, 0.4)
        x0, y0 = 12, 10 + dy
        draw_paper(cv, x0, y0, 58, 62)
        d = ImageDraw.Draw(cv)
        d.rectangle([x0 + 1, y0 + 1, x0 + 57, y0 + 13], fill=(200, 60, 56, 255))
        draw_text(cv, "NOV 2022", x0 + 29, y0 + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        draw_text(cv, "30", x0 + 29, y0 + 24, "press", 24, INK, align="center", outline=None, shadow=False)
        window(cv, x0 + 64, y0 + 8, 148, 44)
        draw_text(cv, "30 DE NOVIEMBRE", x0 + 74, y0 + 18, "press", 8, CREAM, reveal=(t - t_30) * 30)
        draw_text(cv, "DE 2022", x0 + 74, y0 + 32, "press", 8, GOLD, reveal=(t - t_30 - 0.5) * 30)
    # ventana de chat
    if t > t_oai - 0.1:
        p = ease_out(prog(t, t_oai - 0.1, t_oai + 0.25))
        wx, wy, ww, wh = 228, 16, 242, 188
        hh = max(20, int(wh * p))
        if p < 1:
            window(cv, wx, wy, ww, hh)
        else:
            header = "CHATGPT" if t > t_gpt - 0.05 else "OPENAI"
            msgs = [("user", q, q_t0, 22),
                    ("bot", "¡BUENA PREGUNTA! ALAN TURING SE LA HIZO EN 1950. HOY PODÉS CONVERSAR CONMIGO Y "
                            "SACAR TUS PROPIAS CONCLUSIONES.", a_t0, 30)]
            chat_window(cv, wx, wy, ww, wh, t, header, msgs, badge="VISTA PREVIA" if t > t_vp - 0.1 else None,
                        title_glow=1.0 if t > t_gpt else 0.0)
    if t > t_gpt - 0.05:
        a, dy = pop(t, t_gpt - 0.05, 0.4)
        draw_text(cv, "CHATGPT", 349, 216 + dy, "press", 24, align="center",
                  gradient=[(200, 255, 236), (120, 230, 196), (40, 190, 150), (16, 140, 110)], outline_w=2)
        for i in range(4):
            sparkle(cv, 270 + i * 54, 214 + (i % 2) * 30, t + i * 0.5, 3, CREAM)
    return vignette(cv, 0.35)


def person_icon(d, x, y, col):
    d.rectangle([x + 1, y, x + 3, y + 2], fill=(*col, 255))
    d.rectangle([x, y + 3, x + 4, y + 7], fill=(*col, 255))


def sc_users(t):
    """Un millón de usuarios en cinco días; cien millones en dos meses (UBS). Récord absoluto."""
    w = TL.word
    t0 = TL.s("c7_05")
    t_mill = w("c7_05", "millon")
    t_usu = w("c7_05", "usuarios")
    t_ubs = w("c7_05", "Segun")
    t_meses = w("c7_05", "dos")
    t_cien = w("c7_05", "cien")
    t_ning = w("c7_05", "Ninguna")
    t_rap = w("c7_05", "rapido")
    cv = vgradient((4, 8, 20), (16, 30, 56), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 30):
        d.line([(x, 0), (x, H)], fill=(18, 32, 58, 255))
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(18, 32, 58, 255))
    chart = prog(t, t_ning - 0.25, t_ning + 0.05)
    # contador
    if t < t_meses:
        val = 1_000_000 * ease_in_out(prog(t, t0 + 0.1, t_mill + 0.1))
    else:
        p = prog(t, t_meses + 0.1, t_cien + 0.2)
        val = 1_000_000 * (100 ** (p ** 1.4))
        if p >= 1:
            val = 100_000_000
    big = 1 - chart
    if chart <= 0:
        # calendario de días / meses
        if t < t_meses:
            n_on = int(prog(t, t0 + 0.05, t_mill - 0.05) * 5 + 0.999) if t > t0 + 0.05 else 0
            labels = ["DÍA 1", "DÍA 2", "DÍA 3", "DÍA 4", "DÍA 5"]
        else:
            n_on = 1 + (t > t_meses + 0.6)
            labels = ["MES 1", "MES 2"]
        nb = len(labels)
        for i, lb in enumerate(labels):
            bx = 240 + int((i - (nb - 1) / 2) * 66) - 30
            on = i < n_on
            window(cv, bx, 20, 60, 26, fill=(50, 40, 16) if on else (16, 20, 40), border=GOLD if on else (70, 80, 110))
            draw_text(cv, lb, bx + 30, 29, "press", 8, GOLD if on else (90, 100, 130), align="center")
        draw_text(cv, fmt_int(val), 240, 76, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2,
                  alpha=big)
        draw_text(cv, "USUARIOS", 240, 120, "press", 16, CREAM, align="center", alpha=big)
        if t > t_usu - 0.1:
            a, dy = pop(t, t_usu - 0.1)
            txt = "EN 5 DÍAS" if t < t_meses else ("EN 2 MESES" if t > t_meses + 0.5 else "")
            if txt:
                draw_text(cv, txt, 240, 146 + dy, "press", 16, align="center", gradient=CYAN_RAMP, alpha=big)
        # gente que se suma (iconos)
        lit = int(240 * min(1.0, math.log10(max(1, val)) / 8.0))
        for k in range(240):
            ix, iy = 30 + (k % 60) * 7, 182 + (k // 60) * 11
            col = (90, 220, 255) if k < lit else (34, 44, 70)
            if k < lit and k > lit - 6:
                col = (220, 250, 255)
            person_icon(d, ix, iy, col)
    if t > t_ubs - 0.1:
        draw_text(cv, "FUENTE: ESTIMACIÓN DE UBS", 472, 256, "silk", 8, GREY, align="right",
                  reveal=(t - t_ubs + 0.1) * 40)
    # gráfico de crecimiento (sin cifras extra: solo la forma de las curvas)
    if chart > 0:
        draw_text(cv, "100 MILLONES EN 2 MESES", 240, 14, "press", 16, align="center", gradient=GOLD_RAMP,
                  alpha=chart)
        d = ImageDraw.Draw(cv)
        gx0, gy0, gx1, gy1 = 70, 52, 430, 214
        d.rectangle([gx0, gy0, gx1, gy1], fill=(8, 14, 30, 255), outline=(50, 64, 100, 255))
        for k in range(1, 4):
            yy = gy0 + (gy1 - gy0) * k // 4
            for xx in range(gx0 + 2, gx1, 6):
                d.point((xx, yy), fill=(40, 54, 90, 255))
        draw_text(cv, "USUARIOS", gx0 - 6, gy0 + 4, "silk", 8, GREY, align="right")
        draw_text(cv, "TIEMPO", gx1, gy1 + 4, "silk", 8, GREY, align="right")
        p = ease_out(prog(t, t_ning, t_ning + 1.4))
        # otras apps: curvas lentas
        for i, (k_, col) in enumerate(((0.55, (90, 110, 150)), (0.35, (110, 90, 140)), (0.22, (90, 130, 130)))):
            pts = []
            for s in range(0, 61):
                u = s / 60 * p
                v = k_ * (u ** 1.6)
                pts.append((gx0 + u * (gx1 - gx0), gy1 - v * (gy1 - gy0)))
            if len(pts) > 1:
                d.line(pts, fill=(*col, 255), width=2)
        if p > 0.3:
            draw_text(cv, "OTRAS APPS", gx1 - 6, gy1 - 60, "press", 8, (120, 140, 180), align="right",
                      alpha=prog(t, t_ning + 0.4, t_ning + 0.7))
        # ChatGPT: casi vertical
        pc = ease_out(prog(t, t_ning + 0.1, t_ning + 0.7))
        pts = []
        for s in range(0, 41):
            u = s / 40 * pc
            x = gx0 + u * 46
            y = gy1 - (u ** 2.2) * (gy1 - gy0 - 6)
            pts.append((x, y))
        if len(pts) > 1:
            d.line(pts, fill=(*GOLD, 255), width=3)
            tx, ty = pts[-1]
            for k in range(4):
                sparkle(cv, int(tx) + (k % 2) * 8 - 4, int(ty) + (k // 2) * 8 - 2, t + k, 3, GOLD)
            if pc > 0.9:
                draw_text(cv, "CHATGPT", int(tx) + 12, int(ty) + 6, "press", 8, GOLD)
        draw_text(cv, "NINGUNA APP DE CONSUMO CRECIÓ TAN RÁPIDO", 240, 232, "press", 8, CREAM, align="center",
                  reveal=(t - t_ning) * 26, alpha=chart)
        stamp(cv, "¡RÉCORD!", 330, 96, t, t_rap - 0.05, color=(255, 90, 70), angle=-8)
    return vignette(cv, 0.35)


def crowd_canvas(t, t0):
    cv = vgradient((6, 8, 22), (30, 26, 60), 10)
    STARS.draw(cv, t, alpha=0.6)
    d = ImageDraw.Draw(cv)
    # skyline
    for i in range(16):
        bx = i * 32 - 6
        bh = 40 + int(_h(i, 77) * 60)
        d.rectangle([bx, 176 - bh, bx + 28, 176], fill=(18, 18, 38, 255))
        for wy in range(176 - bh + 6, 172, 8):
            for wx in range(bx + 4, bx + 24, 7):
                if _h(wx, wy) > 0.55:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(230, 200, 110, 255))
    d.rectangle([0, 176, W, H], fill=(24, 22, 40, 255))
    rx, rfeet = 240, 120
    t_maq = TL.word("c7_06", "maquina")
    # líneas de datos hacia la máquina
    front = [(32 + k * 52, 270) for k in range(9)]
    back = [(18 + k * 30, 176) for k in range(16)]
    for k, (x, feet) in enumerate(front):
        hx, hy = x + 3, feet - 60
        d.line([(rx, rfeet - 30), (hx, hy)], fill=(40, 120, 170, 255))
        ph = (t * 0.9 + k * 0.13) % 1.0
        px, py = rx + (hx - rx) * ph, rfeet - 30 + (hy - rfeet + 30) * ph
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(160, 250, 255, 255))
    cv = spotlight(cv, rx, 0, rfeet, 20, 120, strength=0.18)
    robot(cv, rx, rfeet, t, face="heart" if t > t_maq else "talk", scale=2)
    d = ImageDraw.Draw(cv)
    # fila de atrás (escala 1)
    for k, (x, feet) in enumerate(back):
        spec = crowd_spec(k + 20)
        a, dy = pop(t, t0 + 0.1 + (k % 8) * 0.06)
        char(cv, spec, x, feet + dy, t, scale=1, arms="hold", alpha=a, look=1 if x < rx else -1)
        d = ImageDraw.Draw(cv)
        d.rectangle([x - 2, feet - 26, x + 1, feet - 23], fill=(140, 240, 255, 255))
        if int(t * 2.2 + k * 0.7) % 3 == 0 and t > t0 + 0.6:
            bubble(cv, "...", x, feet - 54, fname="silk")
    # fila de adelante (escala 2)
    texts = ["HOLA", "¿POR QUÉ?", "GRACIAS", "UN POEMA", "AYUDA", "¿Y SI...?", "JA JA", "CÓDIGO", "RECETA"]
    for k, (x, feet) in enumerate(front):
        spec = crowd_spec(k)
        a, dy = pop(t, t0 + 0.2 + k * 0.07)
        char(cv, spec, x, feet + dy, t, scale=2, arms="hold", alpha=a, mood="happy" if k % 2 else "neutral",
             talk=talk_v(t + k, (int(t * 1.5 + k) % 3) == 0))
        d = ImageDraw.Draw(cv)
        d.rectangle([x - 3, feet - 50, x + 3, feet - 44], fill=(140, 240, 255, 255))
        slot = int(t * 1.4 + k * 1.3) % 3
        if t > t0 + 0.5 + k * 0.1 and slot == (k % 3):
            bubble(cv, texts[k], x, feet - 108, fname="silk")
    return cv


def sc_turing_crowd(t):
    """La pregunta de Turing dejó de ser filosofía: millones de personas conversando con una máquina."""
    w = TL.word
    t_preg = w("c7_06", "pregunta")
    t_tur = w("c7_06", "Turing")
    t_fil = w("c7_06", "filosofia")
    t_mill = w("c7_06", "millones")
    t_conv = w("c7_06", "conversando")
    t_maq = w("c7_06", "maquina")
    wipe0 = t_mill - 0.3
    wp = ease_in_out(prog(t, wipe0, wipe0 + 0.4))
    if wp < 1:
        cv = bg("bg_turing_study").copy()
        RAIN.draw(cv, t, 200)
        char(cv, "turing", 404, 268, t, scale=3, arms="point_l" if t > t_preg else "think", mood="happy")
        draw_text(cv, "¿PUEDEN PENSAR", 210, 40, "press", 16, align="center", gradient=CYAN_RAMP,
                  reveal=(t - t_preg + 0.1) * 30)
        draw_text(cv, "LAS MÁQUINAS?", 210, 64, "press", 16, align="center", gradient=CYAN_RAMP,
                  reveal=(t - t_preg - 0.35) * 30)
        if t > t_tur - 0.2:
            a = prog(t, t_tur - 0.2, t_tur + 0.15)
            off = int((1 - ease_out(a)) * -120)
            portrait_card(cv, "alan_turing", 14 + off, 176)
            window(cv, 86 + off, 190, 190, 46)
            draw_text(cv, "ALAN TURING", 96 + off, 200, "press", 16, CREAM)
            draw_text(cv, "LA PREGUNTA DE 1950", 96 + off, 220, "silk", 8, GREY)
        if t > t_fil - 0.1:
            a, dy = pop(t, t_fil - 0.1)
            draw_text(cv, "FILOSOFÍA", 210, 104 + dy, "press", 16, (170, 170, 180), align="center")
            sp = ease_out(prog(t, t_fil + 0.4, t_fil + 0.7))
            if sp > 0:
                fw, _ = text_size("FILOSOFÍA", "press", 16)
                ImageDraw.Draw(cv).rectangle([210 - fw // 2, 111 + dy, 210 - fw // 2 + int(fw * sp), 113 + dy],
                                             fill=(240, 70, 60, 255))
        cv = vignette(cv, 0.4)
    if wp > 0:
        cr = crowd_canvas(t, wipe0 + 0.2)
        if t > t_mill - 0.1:
            a, dy = pop(t, t_mill - 0.1)
            draw_text(cr, "MILLONES DE PERSONAS", 240, 18 + dy, "press", 16, align="center",
                      gradient=CREAM_RAMP)
        if t > t_conv - 0.1:
            draw_text(cr, "CONVERSANDO CON UNA MÁQUINA", 240, 40, "press", 8, CYAN, align="center",
                      reveal=(t - t_conv + 0.1) * 35)
        cr = vignette(cr, 0.35)
        if wp >= 1:
            return cr
        xb = int(W * (1 - wp))
        out = cv.copy()
        out.paste(cr.crop((xb, 0, W, H)), (xb, 0))
        ImageDraw.Draw(out).rectangle([xb - 2, 0, xb, H], fill=(*CYAN, 255))
        return out
    return cv


# =========================================================================== montaje

def scenes():
    w = TL.word
    st = TL.chapter_start(CH)
    return [
        (st - 0.3, make_card(CH, ["ATENCIÓN"], "2017 – 2022"), None),
        (TL.s("c7_01") - 0.2, sc_google,
         lambda t: (1.0 + cam_punch(t, [w("c7_01", "ocho") + i * 0.13 for i in range(8)], 0.015)
                    + cam_punch(t, [TL.e("c7_01") - 0.1], 0.08), 240, 120)),
        (TL.s("c7_02") - 0.15, sc_attention,
         lambda t: (1.0 + cam_punch(t, [w("c7_02", "transformer"), w("c7_02", "lee")], 0.05)
                    + cam_punch(t, [w("c7_02", "faltaba")], 0.1), 240, 135)),
        (TL.s("c7_03") - 0.15, sc_llm,
         lambda t: (1.0 + cam_punch(t, [w("c7_03", "construyen"), w("c7_03", "cada"), w("c7_03", "grandes")], 0.06),
                    260, 135)),
        (TL.s("c7_04") - 0.15, sc_chat,
         lambda t: (1.0 + cam_punch(t, [w("c7_04", "ChatGPT")], 0.08), 240, 135)),
        (TL.s("c7_05") - 0.15, sc_users,
         lambda t: (1.0 + cam_punch(t, [w("c7_05", "millon") + 0.1, w("c7_05", "cien") + 0.2], 0.1)
                    + cam_punch(t, [w("c7_05", "Ninguna")], 0.08), 240, 120)),
        (TL.s("c7_06") - 0.15, sc_turing_crowd,
         lambda t: (cam_push(t, TL.s("c7_06"), w("c7_06", "millones") - 0.3, 1.0, 1.08, (240, 135), (220, 110))
                    if t < w("c7_06", "millones") - 0.3 else
                    cam_push(t, w("c7_06", "millones"), TL.e("c7_06") + 0.6, 1.0, 1.1, (240, 135), (240, 150)))),
    ]


# =========================================================================== audio

def music(A):
    w = TL.word
    st = TL.chapter_start(CH)
    end = chapter_end(CH)
    s = TL.s
    CGAF = [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")]
    A.section(st + 1.6, s("c7_02") - 0.15, 108, CGAF, A.st_bright)
    A.sting(w("c7_01", "Attention"), [72, 76, 79, 84], vol=0.05, step=0.1, hold=1.0)
    A.section(s("c7_02") - 0.15, s("c7_03") - 0.15, 108, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")],
              A.st_build)
    tf = w("c7_02", "faltaba")
    A.kick(A.music, tf, 0.4)
    A.sting(tf, [67, 72, 76, 79], vol=0.05, step=0.07, hold=1.0)
    A.section(s("c7_03") - 0.15, s("c7_04") - 0.15, 112, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")],
              A.st_bright)
    for k in ("construyen", "cada", "grandes"):
        A.kick(A.music, w("c7_03", k), 0.3)
    A.section(s("c7_04") - 0.15, s("c7_05") - 0.15, 108, CGAF, A.st_summer_lead)
    A.sting(w("c7_04", "ChatGPT"), [72, 76, 79, 84, 88], vol=0.05, step=0.08, hold=1.2)
    # crecimiento: build con riser hasta «Ninguna»
    tn = w("c7_05", "Ninguna")
    A.section(s("c7_05") - 0.15, tn, 116, [("F", "maj"), ("G", "maj"), ("A", "min"), ("G", "maj")], A.st_build)
    t_r0 = w("c7_05", "dos") - 0.2
    n = int((tn - t_r0) * A.SR)
    A.music.add(t_r0, A.noise(tn - t_r0, 3) * np.linspace(0, 1, n) ** 2, 0.06)
    tt, k = t_r0, 0
    while tt < tn - 0.05:
        pr = (tt - t_r0) / (tn - t_r0)
        A.note(A.music, tt, A.midi_hz(60 + [0, 4, 7, 12][k % 4] + int(pr * 12)), 0.06, duty=0.125, vol=0.045, s=0.4)
        tt += 0.16 - 0.1 * pr
        k += 1
    A.kick(A.music, tn, 0.55)
    A.crash(A.music, tn, 0.22)
    A.section(tn, s("c7_06") - 0.15, 116, CGAF, A.st_triumph)
    # Turing: un respiro misterioso, después la multitud
    tm = w("c7_06", "millones") - 0.3
    A.section(s("c7_06") - 0.15, tm, 84, [("D", "min"), ("Bb", "maj")], A.st_mystery)
    A.crash(A.music, tm + 0.3, 0.1)
    A.section(tm, end - 0.1, 112, [("F", "maj"), ("C", "maj"), ("G", "maj"), ("A", "min")], A.st_summer_lead)


def sfx(A):
    w = TL.word
    # Google
    A.whoosh(w("c7_01", "dos") - 0.1, 0.3, 0.05)
    for i in range(8):
        A.pop_sfx(w("c7_01", "ocho") + i * 0.13, 520 + i * 70, 0.05)
    A.whoosh(w("c7_01", "Google") - 0.3, 0.35, 0.04)
    A.whoosh(w("c7_01", "publican") - 0.1, 0.4, 0.05)
    A.typewriter(w("c7_01", "Attention"), w("c7_01", "Attention") + 12 / 22, 18, 0.04)
    A.typewriter(w("c7_01", "All"), w("c7_01", "All") + 12 / 22, 18, 0.04)
    A.coin(TL.e("c7_01") - 0.1, 0.05)
    # atención
    A.pop_sfx(w("c7_02", "transformer") - 0.1, 450)
    for k in range(6):
        A.blip(w("c7_02", "arquitectura") - 0.2 + k * 0.08, 900 + k * 90, 0.03, 0.03)
    for k in range(6):
        A.blip(w("c7_02", "lee") + k * 0.012, 1400 + k * 150, 0.05, 0.02)
    A.text_blips(w("c7_02", "aprende"), 24, 40, 0.012, 1700)
    tt = w("c7_02", "aprende")
    while tt < w("c7_02", "es la pieza") - 0.3:
        A.blip(tt, 1800, 0.02, 0.018, 0.125)
        tt += 0.45
    A.whoosh(w("c7_02", "faltaba") - 0.45, 0.45, 0.04)
    n = int(0.04 * A.SR)
    A.sfx.add(w("c7_02", "faltaba"), A.noise(0.04, 1) * np.exp(-np.arange(n) / A.SR * 120), 0.09)
    A.coin(w("c7_02", "faltaba") + 0.08, 0.05)
    # modelos
    A.pop_sfx(w("c7_03", "modelos") - 0.1, 480)
    for i, k in enumerate(("construyen", "cada", "grandes")):
        A.pop_sfx(w("c7_03", k), 300 + i * 120, 0.07)
        A.robot_beep(w("c7_03", k) + 0.1, 0.025)
    A.wind(w("c7_03", "entrenados") - 0.2, TL.e("c7_03") + 0.1, 0.03)
    # ChatGPT
    A.pop_sfx(w("c7_04", "treinta") - 0.15, 520)
    A.text_blips(w("c7_04", "treinta"), 15, 30, 0.015)
    A.whoosh(w("c7_04", "OpenAI") - 0.1, 0.3, 0.05)
    q_t0 = w("c7_04", "OpenAI") + 0.9
    q_len = len("¿LAS MÁQUINAS PUEDEN PENSAR?")
    A.typewriter(q_t0, q_t0 + q_len / 22, 16, 0.035)
    a_t0 = q_t0 + q_len / 22 + 0.3 + 0.5
    A.text_blips(a_t0, 60, 30, 0.012, 1300)
    A.pop_sfx(w("c7_04", "vista") - 0.1, 700, 0.04)
    A.join_jingle(w("c7_04", "ChatGPT") - 0.05, 0.06)
    # usuarios
    t0 = TL.s("c7_05")
    for k in range(5):
        A.blip(t0 + 0.05 + k * (w("c7_05", "millon") - t0 - 0.1) / 5, 800 + k * 100, 0.05, 0.035)
    tt = t0 + 0.1
    while tt < w("c7_05", "millon") + 0.1:
        A.blip(tt, 2200, 0.012, 0.015)
        tt += 0.06
    A.coin(w("c7_05", "millon") + 0.1, 0.06)
    tt = w("c7_05", "dos") + 0.1
    while tt < w("c7_05", "cien") + 0.2:
        A.blip(tt, 2400, 0.012, 0.015)
        tt += 0.045
    A.blip(w("c7_05", "dos") + 0.05, 900, 0.05, 0.035)
    A.blip(w("c7_05", "dos") + 0.65, 1000, 0.05, 0.035)
    A.coin(w("c7_05", "cien") + 0.2, 0.06)
    A.whoosh(w("c7_05", "Ninguna") - 0.25, 0.3, 0.05)
    for i in range(3):
        A.pop_sfx(w("c7_05", "Ninguna") + i * 0.25, 400 + i * 100, 0.05)
    A.kick(A.sfx, w("c7_05", "rapido") - 0.05, 0.3)
    # Turing -> multitud
    A.rain_amb(TL.s("c7_06") - 0.15, w("c7_06", "millones") - 0.1, 0.03)
    A.text_blips(w("c7_06", "pregunta") - 0.1, 26, 30, 0.018, 1100)
    A.whoosh(w("c7_06", "Turing") - 0.2, 0.3, 0.04)
    A.pop_sfx(w("c7_06", "filosofia") - 0.1, 500)
    A.chalk(w("c7_06", "filosofia") + 0.4, w("c7_06", "filosofia") + 0.7, 0.04)
    A.whoosh(w("c7_06", "millones") - 0.3, 0.45, 0.06)
    for i in range(14):
        A.pop_sfx(w("c7_06", "millones") + 0.2 + i * 0.2, 600 + (i * 97) % 500, 0.03)
    A.robot_beep(w("c7_06", "maquina"), 0.04)
