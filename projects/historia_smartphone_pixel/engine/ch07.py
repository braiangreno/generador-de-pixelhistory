"""Capítulo 7: Einstein en el bolsillo (Satélites GPS a 20.000 km, relojes atómicos y La Pizarra 3: GPS y Relatividad)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_satellite_icon(cv, cx, cy, col=TESLA_CYAN):
    d = ImageDraw.Draw(cv)
    d.rectangle([cx - 12, cy - 3, cx - 5, cy + 3], fill=(48, 96, 168, 255), outline=(*col, 255))
    d.rectangle([cx + 5, cy - 3, cx + 12, cy + 3], fill=(48, 96, 168, 255), outline=(*col, 255))
    d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=(214, 218, 228, 255), outline=(*INK, 255))


def c7_s01_gps_orbit(t):
    """c7_01..c7_02: Tu teléfono sabe dónde estás escuchando satélites a 20.000 km con relojes atómicos."""
    t0 = TL.s("c7_01")
    t_c7_02 = TL.s("c7_02")

    cv = bg("earth_orbit_gps").copy()
    draw_place_only(cv, "ÓRBITA TERRESTRE · 20.000 KM DE ALTURA", t, t0, border=TESLA_CYAN)

    char(cv, "pedestrian_modern", 240, 248, t, scale=2, arms="hold", look=0, mood="happy")
    draw_held_smartphone(cv, 240, 248, t, glow_col=TESLA_CYAN, facing=1)

    window(cv, 118, 42, 244, 106, fill=(10, 18, 38), border=GOLD if t >= t_c7_02 else TESLA_CYAN)
    if t < t_c7_02:
        draw_text(cv, "PARECE MAGIA:", 240, 52, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "SABE DÓNDE ESTÁS", 240, 74, "press", 8, GOLD, align="center")
        draw_phosphor_dot(cv, 240, 104, r=4, color=CHALK_RED)
        draw_text(cv, "PUNTO AZUL EN EL MAPA", 240, 122, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "SATÉLITES A 20.000 KM DE ALTURA", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        for sx, sy in ((162, 82), (240, 74), (318, 82)):
            draw_satellite_icon(cv, sx, sy, col=GOLD)
        draw_text(cv, "CADA UNO LLEVA UN RELOJ ATÓMICO", 240, 106, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECISIÓN DE MILMILLONÉSIMAS DE SEGUNDO", 240, 126, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.34)


def c7_s02_pizarra_gps_einstein(t):
    """c7_03..c7_07: LA PIZARRA 3 — 4 satélites, trilateración y los 38 microsegundos de la relatividad de Einstein."""
    t0 = TL.s("c7_03")
    t_c7_04 = TL.s("c7_04")
    t_c7_05 = TL.s("c7_05")
    t_c7_06 = TL.s("c7_06")
    t_c7_07 = TL.s("c7_07")

    cv = draw_pizarra_frame(
        t, t0, "GPS Y EINSTEIN",
        summary_es="SIN EINSTEIN, TU MAPA FALLARÍA 10 KM POR DÍA",
        t_summary=t_c7_06 + 0.4,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c7_04:
        # Paso 1: Cada satélite repite la hora todo el tiempo y tu teléfono compara
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_CYAN, alpha=0.92)
        draw_text(cv, "CADA SATÉLITE REPITE LA HORA", 240, 54, "silk", 8, CHALK_CYAN, align="center")
        draw_satellite_icon(cv, 184, 84, col=CHALK_YELLOW)
        draw_satellite_icon(cv, 296, 84, col=CHALK_YELLOW)
        d.line([(184, 92), (240, 142)], fill=(*CHALK_CYAN, 220), width=2)
        d.line([(296, 92), (240, 142)], fill=(*CHALK_YELLOW, 220), width=2)
        draw_text(cv, "12:00:00.001", 184, 102, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "12:00:00.004", 296, 102, "silk", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "TU TELÉFONO ESCUCHA Y COMPARA", 240, 164, "silk", 8, CHALK_WHITE, align="center")
    elif t < t_c7_05:
        # Paso 2: Con 4 satélites calcula el punto exacto donde estás
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_GREEN, alpha=0.92)
        draw_text(cv, "CON 4 SATÉLITES -> PUNTO EXACTO", 240, 54, "silk", 8, CHALK_GREEN, align="center")
        sats = [(154, 82), (210, 74), (270, 74), (326, 82)]
        for sx, sy in sats:
            draw_satellite_icon(cv, sx, sy, col=CHALK_CYAN)
            d.line([(sx, sy + 6), (240, 138)], fill=(*CHALK_GREEN, 190), width=1)
        draw_phosphor_dot(cv, 240, 138, r=4, color=CHALK_YELLOW)
        draw_text(cv, "MÁS TARDE = MÁS LEJOS", 240, 164, "silk", 8, CHALK_YELLOW, align="center")
    elif t < t_c7_06:
        # Paso 3: Allá arriba el tiempo pasa más rápido (+38 millonésimos de segundo por día)
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_YELLOW, alpha=0.92)
        draw_text(cv, "ALLÁ ARRIBA EL TIEMPO VA MÁS RÁPIDO", 240, 54, "silk", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "+38 MICROSEGUNDOS / DÍA", 240, 86, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "(38 MILLONÉSIMOS DE SEGUNDO)", 240, 112, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "MENOS GRAVEDAD A 20.000 KM", 240, 144, "silk", 8, CHALK_GREEN, align="center")
    else:
        # Paso 4 (c7_06..c7_07): Sin corregirlo, 10 km de error por día -> Einstein tiene razón
        window(cv, 118, 42, 244, 152, fill=BOARD_DARK, border=CHALK_WHITE, alpha=0.92)
        if t < t_c7_07 - 0.1:
            draw_text(cv, "SIN CORREGIR ESOS 38 MICROSEGUNDOS:", 240, 52, "silk", 8, CHALK_RED, align="center")
            draw_text(cv, "ERROR: 10 KM POR DÍA", 240, 78, "press", 8, CHALK_RED, align="center")
            draw_text(cv, "RELATIVIDAD DE EINSTEIN", 240, 106, "press", 8, CHALK_YELLOW, align="center")
        else:
            draw_text(cv, "RELATIVIDAD EN TU BOLSILLO:", 240, 54, "silk", 8, CHALK_CYAN, align="center")
            draw_text(cv, "CADA VEZ QUE ABRES UN MAPA,", 240, 82, "press", 8, CHALK_WHITE, align="center")
            draw_text(cv, "EINSTEIN TIENE RAZÓN.", 240, 108, "press", 8, CHALK_YELLOW, align="center")

    return cv


def scenes():
    return [
        (TL.s("c7_00") - 0.15, make_card(7, ["EINSTEIN EN", "EL BOLSILLO"], "20.000 KM · GPS Y RELATIVIDAD"),
         None, "ch07"),
        (TL.s("c7_01") - 0.15, c7_s01_gps_orbit,
         lambda t: cam_push(t, TL.s("c7_01"), TL.s("c7_03"), 1.0, 1.03, (240, 135)), "ch07"),
        (TL.s("c7_03") - 0.15, c7_s02_pizarra_gps_einstein,
         None, "ch07"),
    ]


def music(A):
    t0 = TL.s("c7_00")
    t_end = TL.s("c8_00")
    A.add_pad(t0, t_end - t0, [130.81, 196.0, 246.94, 293.66], amp=0.036)


def sfx(A):
    A.fx_sparkle(TL.s("c7_01"), 0.09)
    A.fx_sweep(TL.s("c7_03"), 0.4, 220, 440, 0.06)
    A.fx_chime(TL.s("c7_07"), 0.10)
