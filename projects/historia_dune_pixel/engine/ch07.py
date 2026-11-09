"""Capítulo 7: La segunda mitad (c7_00..c7_05)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, READER_1, READER_2
from ch06 import VILLENEUVE


# ===========================================================================
# ESCENA 22 (c7_01, c7_02): Marzo de 2024, solo en cines y más de US$ 700 millones
# ===========================================================================
def scene_part_two_boxoffice(t):
    t1 = TL.s("c7_01")
    t2 = TL.s("c7_02")
    cv = bg("bg_cinema_2024_packed").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(28, 18, 10), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "MARZO DE 2024 · LLEGA DUNE: PARTE DOS", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "ESTA VEZ, ESTRENO EXCLUSIVO EN SALAS DE CINE", 240, 30, "silk", 8, CYAN, align="center")
    else:
        draw_text(cv, "EXPLOSIÓN EN LA TAQUILLA MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "RECAUDÓ MÁS DE US$ 700 MILLONES (+US$ 300M QUE LA 1ª)", 240, 30, "press", 8, GOLD, align="center")

    char(cv, VILLENEUVE, 84, 260, t, scale=2, arms="cheer" if t >= t2 else "point", look=1, mood="happy")
    char(cv, READER_1, 368, 260, t, scale=2, arms="cheer", look=-1, mood="happy")
    char(cv, READER_2, 428, 260, t, scale=2, arms="point", look=-1, mood="happy")
    robot(cv, 32, 260, t, face="excited", scale=1)

    # Panel comparativo de taquilla
    window(cv, 140, 56, 200, 114, fill=(22, 16, 12), border=GOLD, alpha=0.96)
    draw_text(cv, "DUNE EN CINES", 240, 66, "press", 8, GOLD, align="center")

    # Barra Parte 1
    draw_text(cv, "PARTE UNO: +US$ 400M", 240, 84, "silk", 8, CYAN, align="center")
    d.rectangle([156, 96, 156 + 96, 108], fill=(72, 185, 235, 255), outline=(*INK, 255))

    # Barra Parte 2 animada
    u2 = clamp01((t - t1) / max(1.0, TL.e("c7_02") - t1))
    w_p2 = int(168 * ease_out(u2))
    draw_text(cv, "PARTE DOS: +US$ 700M", 240, 118, "press", 8, GOLD, align="center")
    d.rectangle([156, 132, 156 + max(12, w_p2), 146], fill=(245, 190, 62, 255), outline=(*GOLD, 255))
    draw_text(cv, "SOLO EN CINES · 2024", 240, 154, "silk", 8, GREEN, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 23 Y 24 (c7_03, c7_04, c7_05): 20 millones de libros y la parte incómoda
# ===========================================================================
def scene_twenty_million_and_turn(t):
    t3 = TL.s("c7_03")
    t4 = TL.s("c7_04")
    t5 = TL.s("c7_05")

    if t < t5:
        cv = bg("bg_bookstore_1965").copy()
        window(cv, 16, 10, 448, 36, fill=(24, 18, 12), border=GOLD, alpha=0.95)
        if t < t4:
            draw_text(cv, "LA NOVELA ORIGINAL DE AGOSTO DE 1965", 240, 16, "silk", 8, CYAN, align="center")
            draw_text(cv, "CASI 20 MILLONES DE EJEMPLARES VENDIDOS", 240, 30, "press", 8, GOLD, align="center")
        else:
            draw_text(cv, "DE UNAS NOTAS EN OREGÓN (1957) AL CINE MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
            draw_text(cv, "UNA DE LAS SAGAS MÁS GRANDES DE LA HISTORIA", 240, 30, "press", 8, GOLD, align="center")

        char(cv, HERBERT, 96, 260, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, VILLENEUVE, 384, 260, t, scale=2, arms="point", look=-1, mood="happy")
        robot(cv, 38, 260, t, face="excited", scale=1)

        window(cv, 144, 62, 192, 104, fill=(32, 22, 14), border=GOLD, alpha=0.96)
        draw_text(cv, "DUNE (1965 → 2024)", 240, 74, "silk", 8, CYAN, align="center")
        draw_text(cv, "20.000.000", 240, 94, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "DE EJEMPLARES", 240, 118, "press", 8, CREAM, align="center")
        draw_text(cv, "DE UN ARTÍCULO INCONCLUSO", 240, 140, "silk", 8, GREEN, align="center")

        draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
        return cv

    # Escena 24 (c7_05): "Pero faltaba la parte incómoda."
    cv = bg("bg_wadi_rum_2019").copy()
    cv = grade(cv, mul=(0.68, 0.58, 0.55), add=(10, 0, 8), sat=0.9, k=0.9)
    draw_sand_wind(cv, t, density=52, color=(224, 174, 108))

    window(cv, 44, 72, 392, 96, fill=(28, 14, 18), border=RED, alpha=0.96)
    draw_text(cv, "EL GIRO DE LA HISTORIA", 240, 86, "silk", 8, GOLD, align="center")
    draw_text(cv, "PERO FALTABA LA", 240, 106, "press", 16, CREAM, align="center", outline_w=2)
    draw_text(cv, "PARTE INCÓMODA", 240, 130, "press", 16, RED, align="center", outline_w=2)

    char(cv, VILLENEUVE, 96, 260, t, scale=2, arms="cross", look=1, mood="focused")
    robot(cv, 404, 260, t, face="question", scale=1)
    draw_sand_ripple(cv, t, y_base=258, x_start=40, x_end=440)
    return cv


def scenes():
    return [
        (TL.chapter_start(7) - 0.3, make_card(7, ["LA SEGUNDA", "MITAD"], "2024 · SOLO EN CINES Y 20 MILLONES DE LIBROS")),
        (TL.s("c7_01") - 0.15, scene_part_two_boxoffice),
        (TL.s("c7_03") - 0.15, scene_twenty_million_and_turn),
    ]
