"""Capítulo 7: La segunda mitad (c7_00..c7_05)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, READER_1, READER_2
from ch06 import VILLENEUVE, PRODUCER


# ===========================================================================
# ESCENA 22 (c7_01, c7_02): Marzo de 2024, solo en cines y más de US$ 700 millones
# ===========================================================================
def scene_part_two_boxoffice(t):
    t1 = TL.s("c7_01")
    t2 = TL.s("c7_02")
    cv = bg("bg_cinema_2024_packed").copy()
    d = ImageDraw.Draw(cv)
    if t >= t2:
        CONF.draw(cv, t)

    window(cv, 16, 10, 448, 36, fill=(28, 18, 10), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "MARZO DE 2024 · LLEGA DUNE: PARTE DOS", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "ESTA VEZ, ESTRENO EXCLUSIVO EN SALAS DE CINE", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t1) * 32)
    else:
        draw_text(cv, "EXPLOSIÓN EN LA TAQUILLA MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "RECAUDÓ MÁS DE US$ 700 MILLONES (+US$ 300M QUE LA 1ª)", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t2) * 32)

    # Villeneuve presenta Parte Dos; los espectadores entran a la sala en "solo en cines" y celebran en "+US$ 700M"
    t_cines = TL.word("c7_01", "cines")
    r1x, r1ph = walk(t, t1 + 0.1, t_cines + 0.4, 438, 368)
    r2x, r2ph = walk(t, t1 + 0.25, t_cines + 0.55, 464, 418)
    char(cv, VILLENEUVE, 84, 260, t, scale=2,
         arms="cheer" if t >= t2 else "point", look=1, mood="happy")
    char(cv, READER_1, r1x, 260, t, scale=2, walk=r1ph,
         arms="cheer" if t >= t2 else "point_l", look=-1, mood="happy")
    char(cv, READER_2, r2x, 260, t, scale=2, walk=r2ph,
         arms="wave" if t >= t2 else "hold", look=-1, mood="happy")

    # Panel comparativo de taquilla con barras animadas
    a_b, dy_b = pop(t, t1 + 0.05)
    window(cv, 140, 56 + dy_b, 200, 114, fill=(22, 16, 12), border=GOLD, alpha=0.96 * a_b)
    draw_text(cv, "DUNE EN CINES", 240, 66 + dy_b, "press", 8, GOLD, align="center")

    # Barra Parte 1
    u1 = clamp01((t - t1) / 0.9)
    w_p1 = int(96 * ease_out(u1))
    draw_text(cv, "PARTE UNO: +US$ 400M", 240, 84 + dy_b, "silk", 8, CYAN, align="center")
    d.rectangle([156, 96 + dy_b, 156 + max(8, w_p1), 108 + dy_b], fill=(72, 185, 235, 255), outline=(*INK, 255))

    # Barra Parte 2 animada
    u2 = clamp01((t - t1 - 0.4) / max(1.0, TL.e("c7_02") - t1 - 0.4))
    w_p2 = int(168 * ease_out(u2))
    draw_text(cv, "PARTE DOS: +US$ 700M", 240, 118 + dy_b, "press", 8, GOLD, align="center")
    d.rectangle([156, 132 + dy_b, 156 + max(12, w_p2), 146 + dy_b], fill=(245, 190, 62, 255), outline=(*GOLD, 255))
    draw_text(cv, "SOLO EN CINES · 2024", 240, 154 + dy_b, "silk", 8, GREEN, align="center")

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
            draw_text(cv, "CASI 20 MILLONES DE EJEMPLARES VENDIDOS", 240, 30, "press", 8, GOLD, align="center",
                      reveal=(t - t3) * 32)
        else:
            draw_text(cv, "DE UNAS NOTAS EN OREGÓN (1957) AL CINE MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
            draw_text(cv, "UNA DE LAS SAGAS MÁS GRANDES DE LA HISTORIA", 240, 30, "press", 8, GOLD, align="center",
                      reveal=(t - t4) * 32)

        t_sagas = TL.word("c7_04", "sagas")
        char(cv, HERBERT, 88, 260, t, scale=2,
             arms="point" if t >= t4 else "note", look=1, mood="happy")
        char(cv, VILLENEUVE, 392, 260, t, scale=2,
             arms="cheer" if t >= t_sagas else "point_l", look=-1, mood="happy")

        a_m, dy_m = pop(t, t3 + 0.05)
        window(cv, 144, 62 + dy_m, 192, 104, fill=(32, 22, 14), border=GOLD, alpha=0.96 * a_m)
        draw_text(cv, "DUNE (1965 → 2024)", 240, 74 + dy_m, "silk", 8, CYAN, align="center")
        draw_text(cv, "20.000.000", 240, 94 + dy_m, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "DE EJEMPLARES", 240, 118 + dy_m, "press", 8, CREAM, align="center")
        draw_text(cv, "DE UN ARTÍCULO INCONCLUSO", 240, 140 + dy_m, "silk", 8, GREEN, align="center")
        sparkle(cv, 158, 96 + dy_m, t, 3)
        sparkle(cv, 322, 100 + dy_m, t + 1.3, 3)
        return cv

    # Escena 24 (c7_05): "Pero faltaba la parte incómoda."
    dx, dy = shake(t, t5 + 0.05, dur=0.25, amp=3)
    cv = bg("bg_wadi_rum_2019").copy()
    cv = grade(cv, mul=(0.68, 0.58, 0.55), add=(10, 0, 8), sat=0.9, k=0.9)
    draw_sand_wind(cv, t, density=56, color=(224, 174, 108))

    a_t, dy_t = pop(t, t5)
    window(cv, 44, 72 + dy_t, 392, 96, fill=(28, 14, 18), border=RED, alpha=0.96 * a_t)
    draw_text(cv, "EL GIRO DE LA HISTORIA", 240, 86 + dy_t, "silk", 8, GOLD, align="center")
    draw_text(cv, "PERO FALTABA LA", 240, 106 + dy_t, "press", 16, CREAM, align="center", outline_w=2)
    draw_text(cv, "PARTE INCÓMODA", 240, 130 + dy_t, "press", 16, RED, align="center", outline_w=2,
              reveal=(t - t5 - 0.15) * 26)

    char(cv, VILLENEUVE, 88, 260, t, scale=2, arms="think", look=1, mood="focused")
    char(cv, HERBERT, 392, 260, t, scale=2, arms="point_l", look=-1, mood="worried")
    return offset_canvas(cv, dx, dy)


def scenes():
    return [
        (TL.chapter_start(7) - 0.3, make_card(7, ["LA SEGUNDA", "MITAD"], "2024 · SOLO EN CINES Y 20 MILLONES DE LIBROS"), None),
        (TL.s("c7_01") - 0.15, scene_part_two_boxoffice, lambda t: (1.0 + cam_punch(t, [TL.s("c7_02")], 0.07), 240, 140)),
        (TL.s("c7_03") - 0.15, scene_twenty_million_and_turn, lambda t: (1.0 + cam_punch(t, [TL.s("c7_05")], 0.08), 240, 140)),
    ]
