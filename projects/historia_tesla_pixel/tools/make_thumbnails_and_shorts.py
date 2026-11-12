"""Genera las Miniaturas 16:9 de YouTube (1920x1080 en ES/EN/PT) y todos los Shorts 9:16 por capítulo
para "EL DIBUJO QUE ENCENDIÓ EL MUNDO — La historia de Nikola Tesla".
"""
import math
import os
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from common import *  # noqa
import i18n
import outro


def build_thumbnail(lang="es"):
    i18n.set_lang(lang)

    # Mitad izquierda: Parque de Budapest al atardecer (el dibujo en la arena, 1882)
    bg_left = bg("bg_budapest_park_sunset").copy()
    # Mitad derecha: Escenario eléctrico / Colorado Springs con rayos violetas y cian
    bg_right = bg("bg_colorado_springs_1899").copy()

    p_l = np.array(bg_left)
    p_r = np.array(bg_right)
    out = np.zeros_like(p_l)
    bayer4 = np.array([
        [0,  8,  2, 10],
        [12, 4, 14,  6],
        [3, 11,  1,  9],
        [15, 7, 13,  5],
    ], dtype=np.float32) / 16.0

    for y in range(H):
        split_x = 240 - (y - 135) * 0.22
        for x in range(W):
            u = clamp01((x - (split_x - 18)) / 36.0)
            use_r = u > bayer4[y % 4, x % 4]
            out[y, x] = p_r[y, x] if use_r else p_l[y, x]

    cv = Image.fromarray(out, "RGBA")
    d = ImageDraw.Draw(cv)

    # Divisoria diagonal eléctrica (cian y dorada)
    for dy_off, col in ((-2, (*TESLA_CYAN, 220)), (0, (255, 255, 255, 255)), (2, (*GOLD, 235))):
        x_top = int(240 - (0 - 135) * 0.22) + dy_off
        x_bot = int(240 - (H - 135) * 0.22) + dy_off
        d.line([(x_top, 0), (x_bot, H)], fill=col, width=2)

    # Motivo central: el círculo con cuatro flechas girando en el centro
    glow(cv, 240, 116, 52, TESLA_CYAN, 0.55)
    draw_rotating_arrows(cv, 240, 116, 36, 1.4, speed=2.2, color=GOLD, glow=TESLA_CYAN, sand_groove=True)
    draw_tesla_sparks(cv, 240, 116, 1.4, rays=6, max_len=54, color=TESLA_VIOLET)

    # Personajes en las esquinas: Tesla joven y Edison / Westinghouse
    char(cv, "inventor", 52, 186, 1.2, scale=2, arms="point", look=1, mood="happy")
    char(cv, "edison_gen", 428, 186, 1.5, scale=2, arms="shrug", look=-1, mood="angry")

    # Placas de año "1882" y "AC"
    window(cv, 14, 12, 86, 30, fill=(38, 24, 12), border=GOLD, alpha=0.95)
    draw_text(cv, "1882", 57, 19, "press", 16, GOLD, align="center", outline_w=2)

    window(cv, 380, 12, 86, 30, fill=(12, 24, 42), border=TESLA_CYAN, alpha=0.95)
    draw_text(cv, "50Hz", 423, 19, "press", 16, TESLA_CYAN, align="center", outline_w=2)

    # Sello Pixeloide Studios arriba al centro
    window(cv, 152, 10, 176, 26, fill=outro.PX_SURFACE, border=outro.PX_CYAN, alpha=0.95)
    outro.draw_isotipo(cv, 160, 13, size=20)
    draw_text(cv, "PIXELOIDE STUDIOS", 250, 19, "press", 8, outro.PX_PAPER, align="center")

    # Cartel central de alto impacto para YouTube
    window(cv, 18, 186, 444, 74, fill=(14, 16, 30), border=GOLD, alpha=0.96)
    badge_str = {
        "es": "EL DIBUJO QUE ENCENDIÓ EL MUNDO · DOCUMENTAL 16-BIT",
        "en": "THE DRAWING THAT LIT UP THE WORLD · 16-BIT DOCUMENTARY",
        "pt": "O DESENHO QUE ACENDEU O MUNDO · DOCUMENTÁRIO 16-BIT",
    }[lang]
    title_str = {
        "es": "LA HISTORIA DE TESLA",
        "en": "THE STORY OF TESLA",
        "pt": "A HISTÓRIA DE TESLA",
    }[lang]
    sub_str = {
        "es": "DE UN PALITO EN LA ARENA A ENCENDER EL PLANETA ENTERO",
        "en": "FROM A STICK IN THE SAND TO LIGHTING UP THE ENTIRE PLANET",
        "pt": "DE UM GRAVETO NA AREIA A ACENDER O PLANETA INTEIRO",
    }[lang]

    draw_text(cv, badge_str, 240, 194, "silk", 8, TESLA_CYAN, align="center")
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
