"""Capítulo 6: Una ventana en el living (Feria Mundial 1939, explosión de los años 50, La Pizarra 3 y el color RGB)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import draw_tv_table_prop


def draw_fair_mic_prop(cv, x, feet=248, t=0.0):
    """Podio con micrófono de la Feria Mundial de Nueva York (1939) apoyado en el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 32, 5, 85)
        d.rectangle([cx - 18, top_y, cx + 18, fy], fill=(42, 52, 78, 255), outline=(*GOLD, 255))
        draw_text(canvas, "RCA", cx, top_y + 12, "press", 8, GOLD, align="center")
        d.line([(cx, top_y - 12), (cx, top_y)], fill=(192, 198, 210, 255), width=2)
        d.ellipse([cx - 5, top_y - 20, cx + 5, top_y - 10], fill=(214, 220, 232, 255), outline=(*INK, 255))
    floor_prop(cv, _draw, x, feet)


def c6_s01_world_fair_and_boom(t):
    """c6_01..c6_03: Feria Mundial de Nueva York (1939) y explosión de hogares con TV (1950 vs 1960 + América Latina)."""
    t0 = TL.s("c6_01")
    t_c6_02 = TL.s("c6_02")
    t_c6_03 = TL.s("c6_03")
    t_lat = TL.word("c6_03", "Latina")

    cv = bg("rca_skyscraper_court").copy() if t < t_c6_02 - 0.1 else bg("living_room_1950s").copy()
    lbl_hdr = "FERIA MUNDIAL DE NUEVA YORK · 1939" if t < t_c6_02 - 0.1 else "AÑOS 1950 – 1960 · LA TELE EXPLOTA"
    draw_place_only(cv, lbl_hdr, t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 42, 244, 108, fill=(16, 22, 38), border=GOLD, alpha=0.95)
    if t < t_c6_02 - 0.1:
        draw_text(cv, "FERIA MUNDIAL · NUEVA YORK (1939)", 240, 52, "silk", 8, GOLD, align="center")
        draw_text(cv, "SARNOFF PRESENTA LA TELEVISIÓN", 240, 74, "press", 8, CREAM, align="center")
        draw_text(cv, "«COMO SI FUERA SUYA»", 240, 98, "silk", 8, CHALK_RED, align="center")
        char(cv, "sarnoff", 184, 248, t, scale=2, arms="wave", look=1, mood="happy",
             talk=talk_v(t, True))
        draw_fair_mic_prop(cv, 240, 248, t)
        draw_tv_table_prop(cv, 312, 248, t, mode="scan")
    else:
        # Grilla de 10 casitas mostrando 1 de cada 10 (1950) -> 9 de cada 10 (1960)
        n_lit = 9 if t >= t_c6_03 - 0.1 else 1
        yr_str = "1960: 9 DE CADA 10 CASAS" if t >= t_c6_03 - 0.1 else "1950: 1 DE CADA 10 CASAS"
        draw_text(cv, yr_str, 240, 50, "press", 8, CHALK_GREEN if n_lit == 9 else GOLD, align="center")
        for i in range(10):
            col_i = i % 5
            row_i = i // 5
            hx = 142 + col_i * 42
            hy = 74 + row_i * 26
            lit = i < n_lit
            c_house = CHALK_GREEN if lit else (52, 58, 72)
            d.rectangle([hx, hy, hx + 24, hy + 14], fill=(*c_house, 255), outline=(*INK, 255))
            d.polygon([(hx - 2, hy), (hx + 12, hy - 8), (hx + 26, hy)], fill=(*shade(c_house, 0.8), 255))
        if t >= t_lat - 0.25:
            draw_text(cv, "AMÉRICA LATINA: AÑOS 50", 240, 130, "silk", 8, TESLA_CYAN, align="center")
        else:
            draw_text(cv, "HOGARES CON TELEVISOR EN EE. UU.", 240, 130, "silk", 8, CREAM, align="center")

        char(cv, "farnsworth_young", 148, 248, t, scale=2, arms="point", look=1, mood="happy")
        draw_tv_table_prop(cv, 240, 248, t, mode="scan")
        char(cv, "pem", 332, 248, t, scale=2, arms="wave", look=-1, mood="happy")

    return vignette(cv, 0.35)


def c6_s02_pizarra_frames_and_bands(t):
    """c6_04..c6_06: LA PIZARRA 3 — Movimiento (25-30 imágenes/s), +500 renglones y franjas al filmar con celular."""
    t0 = TL.s("c6_04")
    t_c6_05 = TL.s("c6_05")
    t_c6_06 = TL.s("c6_06")

    cv = draw_pizarra_frame(t, t0, "MOVIMIENTO Y BARRIDO",
                            summary_es="30 IMÁGENES/S · MITAD DEL DIBUJO",
                            t_summary=t_c6_06 + 1.2)
    d = ImageDraw.Draw(cv)

    if t < t_c6_05 - 0.1:
        # Paso 1: Muchas imágenes quietas por segundo -> el cerebro las une
        d.rectangle([124, 46, 356, 186], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "1. IMÁGENES QUIETAS POR SEGUNDO", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        for i in range(4):
            fx = 136 + i * 52
            d.rectangle([fx, 76, fx + 44, 122], fill=(26, 62, 42, 255), outline=(*CHALK_GREEN, 255))
            # Pelotita o figura avanzando cuadro a cuadro
            by_ball = 106 - abs(int(math.sin((i + int(t * 8)) * 0.8) * 18))
            d.ellipse([fx + 16, by_ball - 6, fx + 28, by_ball + 6], fill=(*CHALK_YELLOW, 255))
            draw_text(cv, f"#{i+1}", fx + 22, 128, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL CEREBRO LAS UNE = MOVIMIENTO", 240, 154, "silk", 8, CHALK_CYAN, align="center")
    elif t < t_c6_06 - 0.1:
        # Paso 2: +500 renglones por imagen y 25 a 30 imágenes por segundo
        d.rectangle([124, 46, 356, 186], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "2. LA TELE DE TUBO (CRT)", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        draw_scanline_beam(cv, 148, 72, 184, 62, t, rows=10, speed=2.4, color=CHALK_GREEN)
        draw_text(cv, "+500 RENGLONES POR IMAGEN", 240, 144, "press", 8, CHALK_WHITE, align="center")
        draw_text(cv, "25 A 30 IMÁGENES POR SEGUNDO", 240, 162, "silk", 8, CHALK_CYAN, align="center")
    else:
        # Paso 3: Si filmas una tele vieja con el celular ves franjas (mitad del dibujo)
        d.rectangle([124, 44, 356, 194], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "3. ¿POR QUÉ SE VEN FRANJAS?", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        # Tele a la izquierda con franja a medio pintar + celular a la derecha filmándola
        d.rectangle([144, 72, 232, 134], fill=(12, 26, 18, 255), outline=(*CHALK_GREEN, 255))
        band_y = 74 + int((t * 32) % 44)
        d.rectangle([146, band_y, 230, band_y + 16], fill=(98, 234, 142, 220))
        # Celular a la derecha
        d.rectangle([268, 74, 316, 134], fill=(24, 32, 44, 255), outline=(*CHALK_CYAN, 255))
        d.rectangle([272, 82, 312, 124], fill=(14, 28, 20, 255))
        d.rectangle([274, band_y + 4, 310, band_y + 14], fill=(98, 234, 142, 220))
        draw_text(cv, "LA CÁMARA LA AGARRA A MITAD DEL DIBUJO", 240, 148, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.28)


def c6_s03_rgb_and_living_window(t):
    """c6_07..c6_08: Los tres puntitos de color (Rojo, Verde, Azul) y la ventana en el living familiar."""
    t0 = TL.s("c6_07")
    t_c6_08 = TL.s("c6_08")

    cv = bg("living_room_1950s").copy()
    draw_place_only(cv, "EL COLOR (RGB) · UNA VENTANA EN EL LIVING", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 42, 244, 106, fill=(16, 20, 34), border=GOLD, alpha=0.95)
    if t < t_c6_08 - 0.1:
        draw_text(cv, "LLEGÓ EL COLOR: 3 PUNTITOS (RGB)", 240, 50, "press", 8, GOLD, align="center")
        rgb_items = [
            (176, "ROJO", (248, 84, 84)),
            (240, "VERDE", (92, 238, 128)),
            (304, "AZUL", (84, 168, 255)),
        ]
        for rx, r_lbl, r_col in rgb_items:
            glow(cv, rx, 88, 18, r_col, 0.55)
            d.ellipse([rx - 12, 76, rx + 12, 100], fill=(*r_col, 255), outline=(*CREAM, 255))
            draw_text(cv, r_lbl, rx, 106, "silk", 8, r_col, align="center")
        draw_text(cv, "TU PANTALLA TODAVÍA USA ESOS TRES", 240, 126, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "DE LA RADIO AL TELEVISOR", 240, 52, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "UNA VENTANA EN EL LIVING", 240, 76, "press", 8, GOLD, align="center")
        draw_text(cv, "LA FAMILIA REUNIDA FRENTE A LA PANTALLA", 240, 104, "silk", 8, CREAM, align="center")

    char(cv, "farnsworth_young", 146, 248, t, scale=2, arms="point", look=1, mood="happy")
    draw_tv_table_prop(cv, 240, 248, t, mode="color_rgb")
    char(cv, "pem", 334, 248, t, scale=2, arms="wave", look=-1, mood="happy")

    return vignette(cv, 0.34)


SCENES = [
    (TL.s("c6_00") - 0.15, TL.s("c6_01"), make_card(6, ["UNA VENTANA EN", "EL LIVING"], "1939 – 1960 · EL MUNDO")),
    (TL.s("c6_01") - 0.15, TL.s("c6_04"), c6_s01_world_fair_and_boom),
    (TL.s("c6_04") - 0.15, TL.s("c6_07"), c6_s02_pizarra_frames_and_bands),
    (TL.s("c6_07") - 0.15, TL.s("c7_00"), c6_s03_rgb_and_living_window),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c6_00"), TL.e("c6_08") - TL.s("c6_00"), (196.0, 233.08, 293.66), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c6_01"), 0.08)
    A.fx_chime(TL.s("c6_03"), 0.10)
    A.fx_pop(TL.s("c6_04"), 0.08)
    A.fx_sparkle(TL.s("c6_07"), 0.11)
