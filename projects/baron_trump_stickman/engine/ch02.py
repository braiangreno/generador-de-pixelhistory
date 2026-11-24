"""Capítulo 2: Las coincidencias (Baron ≠ Barron, Don Fum, 33 cuadras)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch2 = make_card(2, ["LAS COINCIDENCIAS"], "INTERNET Y MANHATTAN")


def _draw_corkboard_strings(cv, cut_progress=0.0):
    """Dibuja hilos rojos conectando piezas en el tablero de corcho."""
    d = ImageDraw.Draw(cv)
    pts = [(118, 62), (240, 56), (362, 64), (176, 108), (308, 108)]
    links = [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (2, 4)]
    for i, (a, b) in enumerate(links):
        if cut_progress > (i / len(links)):
            continue
        d.line([pts[a], pts[b]], fill=(216, 46, 52, 255), width=2)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(224, 52, 58, 255), outline=(*INK, 255))


def scene_ch2(t):
    t_01 = TL.start("c2_01")
    t_02 = TL.start("c2_02")
    t_03 = TL.start("c2_03")
    t_04 = TL.start("c2_04")
    t_05 = TL.start("c2_05")
    t_06 = TL.start("c2_06")
    t_07 = TL.start("c2_07")
    t_08 = TL.start("c2_08")
    ground_y = 224

    if t < t_02:
        # c2_01: Tablero de corcho con hilos rojos
        cv = bg("corkboard_bg")
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "LA LISTA DE INTERNET", t, t_01, border=PINK)
        _draw_corkboard_strings(cv, cut_progress=0.0)
        window(cv, 76, 48, 328, 76, fill=(22, 18, 26), border=PINK, alpha=0.94)
        draw_text(cv, "LA LISTA DE INTERNET", 240, 58, "press", 8, PINK, align="center")
        draw_text(cv, "BARON TRUMP · EL SABIO DON", 240, 78, "silk", 8, CREAM, align="center")
        draw_text(cv, "UN VIAJE A RUSIA", 240, 96, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.34)

    if t < t_03:
        # c2_02: Folleto unido a torre genérica
        cv = bg("nyc_tower_night")
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "EL ÚLTIMO PRESIDENTE Y LA TORRE", t, t_02, border=PINK)
        window(cv, 76, 48, 328, 72, fill=(14, 18, 34), border=PINK, alpha=0.94)
        draw_text(cv, "EL ÚLTIMO PRESIDENTE", 240, 58, "press", 8, PINK, align="center")
        draw_text(cv, "QUINTA AVENIDA · TORRE GENÉRICA", 240, 78, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_04:
        # c2_03: Lupa sobre Baron (1 r) vs Barron (2 r)
        cv = bg("corkboard_bg")
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "MIREMOS DE CERCA", t, t_03, border=GOLD)
        window(cv, 76, 44, 328, 86, fill=(18, 20, 32), border=GOLD, alpha=0.96)
        draw_text(cv, "BARON ≠ BARRON", 240, 56, "press", 16, GOLD, align="center")
        draw_text(cv, "BARON (UNA R) = TÍTULO DE NOBLEZA", 240, 88, "silk", 8, CREAM, align="center")
        draw_text(cv, "COMO CONDE O DUQUE", 240, 106, "silk", 8, CYAN, align="center")
        char(cv, "baron_boy", 240, ground_y, t, scale=2, look=0)
        return vignette(cv, 0.34)

    if t < t_05:
        # c2_04: Lupa sobre Don -> Don Fum
        cv = bg("corkboard_bg")
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "EL SABIO DEL LIBRO", t, t_04, border=GOLD)
        window(cv, 76, 44, 328, 86, fill=(18, 20, 32), border=GOLD, alpha=0.96)
        draw_text(cv, "DON FUM", 240, 56, "press", 16, GOLD, align="center")
        draw_text(cv, "«DON» ES UN TRATAMIENTO ESPAÑOL", 240, 88, "silk", 8, CREAM, align="center")
        draw_text(cv, "COMO EN DON QUIJOTE", 240, 106, "silk", 8, CYAN, align="center")
        char(cv, "don_fum", 240, ground_y, t, scale=2, look=0, talk=talk_v(t, True))
        return vignette(cv, 0.34)

    if t < t_06:
        # c2_05: Barco de inmigrantes de fines del siglo XIX desde Alemania
        cv = bg("harbor_1890")
        grade(cv, tint=(1.04, 0.96, 0.88), dark=0.06)
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "ORIGEN ALEMÁN · FINES DEL SIGLO XIX", t, t_05, border=GOLD)
        window(cv, 76, 44, 328, 66, fill=(18, 22, 34), border=GOLD, alpha=0.94)
        draw_text(cv, "ALEMANIA -> ESTADOS UNIDOS", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "CHICO NOBLE ALEMÁN · INMIGRACIÓN", 240, 76, "silk", 8, CREAM, align="center")
        char(cv, "passerby_a", 170, ground_y, t, scale=2, look=1)
        char(cv, "passerby_b", 310, ground_y, t, scale=2, look=-1)
        return vignette(cv, 0.34)

    if t < t_07:
        # c2_06: Mapa de Manhattan con regla midiendo 33 cuadras (calle 23 vs calle 56)
        cv = new_canvas((18, 26, 42))
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "MANHATTAN · QUINTA AVENIDA", t, t_06, border=CYAN)
        d = ImageDraw.Draw(cv)
        # Mapa estilizado de Manhattan en panel central
        window(cv, 76, 42, 328, 166, fill=(22, 32, 48), border=CYAN, alpha=0.96)
        draw_text(cv, "33 CUADRAS DE DISTANCIA", 240, 52, "press", 8, GOLD, align="center")
        # Línea de Quinta Avenida
        p_rule = ease_out(prog(t, t_06 + 0.3, t_06 + 2.4))
        x_a, x_b, y_line = 128, 352, 122
        d.line([(x_a, y_line), (x_b, y_line)], fill=(*GREY, 180), width=2)
        d.line([(x_a, y_line), (x_a + int((x_b - x_a) * p_rule), y_line)], fill=(*CYAN, 255), width=4)
        # Punto Calle 23 (Hotel 1896)
        d.ellipse([x_a - 6, y_line - 6, x_a + 6, y_line + 6], fill=(*GOLD, 255), outline=(*INK, 255), width=2)
        draw_text(cv, "CALLE 23", x_a, y_line + 14, "press", 8, GOLD, align="center")
        draw_text(cv, "HOTEL (1896)", x_a, y_line + 28, "silk", 8, CREAM, align="center")
        # Punto Calle 56 (Torre)
        d.ellipse([x_b - 6, y_line - 6, x_b + 6, y_line + 6], fill=(*PINK, 255), outline=(*INK, 255), width=2)
        draw_text(cv, "CALLE 56", x_b, y_line + 14, "press", 8, PINK, align="center")
        draw_text(cv, "TORRE ACTUAL", x_b, y_line + 28, "silk", 8, CREAM, align="center")
        # Contador de cuadras
        cuadras = int(round(33 * p_rule))
        draw_text(cv, f"{cuadras} CUADRAS", 240, 86, "press", 16, CYAN, align="center")
        return vignette(cv, 0.34)

    if t < t_08:
        # c2_07: Libros distintos juntados en internet
        cv = bg("library_1893")
        grade(cv, tint=(1.04, 0.94, 0.84), dark=0.14)
        draw_chapter_header(cv, "CAP. 2 · LAS COINCIDENCIAS", "LIBROS DISTINTOS", t, t_07, border=GOLD)
        floor_prop(cv, draw_book_stack_prop, 240, ground_y)
        window(cv, 76, 44, 328, 74, fill=(18, 18, 28), border=GOLD, alpha=0.95)
        draw_text(cv, "EN «EL ÚLTIMO PRESIDENTE»", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "NO APARECE NINGÚN BARON TRUMP", 240, 74, "silk", 8, PINK, align="center")
        draw_text(cv, "SE JUNTARON DESPUÉS EN INTERNET", 240, 92, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    # c2_08: Un hilo rojo se corta
    cv = bg("corkboard_bg")
    grade(cv, dark=0.32)
    p_cut = prog(t, t_08, t_08 + 1.8)
    _draw_corkboard_strings(cv, cut_progress=p_cut)
    window(cv, 76, 86, 328, 66, fill=(16, 16, 24), border=PINK, alpha=0.96)
    draw_text(cv, "LAS COINCIDENCIAS EXISTEN", 240, 98, "press", 8, GOLD, align="center")
    draw_text(cv, "PERO HUBO QUE AYUDARLAS UN POCO", 240, 118, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.38)


def scenes():
    return [
        (TL.start("c2_00") - 0.1, card_ch2, None),
        (TL.start("c2_01") - 0.1, scene_ch2, lambda t: cam_push(t, TL.start("c2_01"), TL.end("c2_08"), 1.0, 1.03)),
    ]
