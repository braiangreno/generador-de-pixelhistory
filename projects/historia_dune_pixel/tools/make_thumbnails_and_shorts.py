"""Genera las Miniaturas 16:9 de YouTube (1920x1080 en ES/EN/PT) y todos los Shorts 9:16 por capítulo
para "LA ARENA QUE NUNCA SE DETUVO — La historia de Dune (1957 → 2026)".
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
import i18n
import ch01
import ch06
import outro


def build_thumbnail(lang="es"):
    i18n.set_lang(lang)

    # Mitad izquierda: Dunas de Oregón 1957 (frío costero)
    bg_1957 = bg("bg_oregon_dunes_1957").copy()
    # Mitad derecha: Desierto ocre de Arrakis / Sala IMAX 2026
    bg_2026 = bg("bg_wadi_rum_2019").copy()
    bg_2026 = grade(bg_2026, mul=(1.12, 0.96, 0.78), add=(14, 6, 0), sat=1.15, k=0.9)

    p57 = np.array(bg_1957)
    p26 = np.array(bg_2026)
    out = np.zeros_like(p57)
    bayer4 = np.array([
        [0,  8,  2, 10],
        [12, 4, 14,  6],
        [3, 11,  1,  9],
        [15, 7, 13,  5],
    ], dtype=np.float32) / 16.0

    for y in range(H):
        split_x = 238 - (y - 135) * 0.22
        for x in range(W):
            u = clamp01((x - (split_x - 18)) / 36.0)
            use_26 = u > bayer4[y % 4, x % 4]
            out[y, x] = p26[y, x] if use_26 else p57[y, x]

    cv = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(cv)

    # Divisoria diagonal dorada y cian
    for dy_off, col in ((-2, (*CYAN, 220)), (0, (255, 255, 255, 255)), (2, (*GOLD, 235))):
        x_top = int(238 - (0 - 135) * 0.22) + dy_off
        x_bot = int(238 - (H - 135) * 0.22) + dy_off
        d.line([(x_top, 0), (x_bot, H)], fill=col, width=2)

    # Ondulación dorada bajo la arena cruzando de 1957 a 2026
    draw_sand_ripple(cv, 2.4, y_base=178, x_start=64, x_end=416, progress=0.82)

    # Personajes en las esquinas: Frank Herbert (1957) y Denis Villeneuve (2026)
    char(cv, ch01.HERBERT, 42, 188, 1.2, scale=2, arms="note", look=1, mood="happy")
    char(cv, ch06.VILLENEUVE, 438, 188, 1.5, scale=2, arms="point", look=-1, mood="happy")

    # Placas de año "1957" y "2026"
    window(cv, 14, 12, 86, 30, fill=(12, 24, 36), border=CYAN, alpha=0.95)
    draw_text(cv, "1957", 57, 19, "press", 16, CYAN, align="center", outline_w=2)

    window(cv, 380, 12, 86, 30, fill=(38, 22, 10), border=GOLD, alpha=0.95)
    draw_text(cv, "2026", 423, 19, "press", 16, GOLD, align="center", outline_w=2)

    # Sello Pixeloide Studios arriba al centro
    window(cv, 152, 10, 176, 26, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
    outro.draw_isotipo(cv, 160, 13, size=20)
    draw_text(cv, "PIXELOIDE STUDIOS", 250, 19, "press", 8, outro.PX_PAPER, align="center")

    # Cartel central de alto impacto para YouTube
    window(cv, 18, 186, 444, 74, fill=(18, 14, 24), border=GOLD, alpha=0.96)
    badge_str = {
        "es": "LA ARENA QUE NUNCA SE DETUVO · DOCUMENTAL 16-BIT",
        "en": "THE SAND THAT NEVER STOPPED · 16-BIT DOCUMENTARY",
        "pt": "A AREIA QUE NUNCA PAROU · DOCUMENTÁRIO 16-BIT",
    }[lang]
    title_str = {
        "es": "LA HISTORIA DE DUNE",
        "en": "THE STORY OF DUNE",
        "pt": "A HISTÓRIA DE DUNA",
    }[lang]
    sub_str = {
        "es": "DE UN ARTÍCULO SIN TERMINAR A 20 MILLONES DE LIBROS",
        "en": "FROM AN UNFINISHED ARTICLE TO 20 MILLION BOOKS",
        "pt": "DE UM ARTIGO INACABADO A 20 MILHÕES DE LIVROS",
    }[lang]

    draw_text(cv, badge_str, 240, 194, "silk", 8, CYAN, align="center")
    draw_text(cv, title_str, 240, 211, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, sub_str, 240, 239, "press", 8, CREAM, align="center", outline_w=1)

    cv = vignette(cv, 0.22)
    hi = cv.resize((1920, 1080), Image.NEAREST).convert("RGB")
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    out_path = os.path.join(ROOT, "renders", f"Miniatura_YouTube_{lang.upper()}.png")
    hi.save(out_path, quality=95)
    print(f"[THUMB] Saved {out_path}")
    return out_path


if __name__ == "__main__":
    for lg in ("es", "en", "pt"):
        build_thumbnail(lg)
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "make_chapter_shorts.py")])
