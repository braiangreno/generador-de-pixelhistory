"""Capítulo 5: El desierto en México (c5_00..c5_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import READER_1, READER_2

LYNCH = {
    "skin": (238, 198, 164), "hair": (74, 54, 42), "hair_style": "parted",
    "shirt": (246, 246, 250), "jacket": (28, 30, 38),
    "tie": (40, 40, 48), "pants": (24, 26, 34),
}
YOUNG_DENIS = {
    "skin": (236, 194, 158), "hair": (68, 48, 36), "hair_style": "parted",
    "shirt": (210, 62, 54), "jacket": (44, 72, 118),
    "pants": (42, 52, 74),
}


# ===========================================================================
# ESCENA 15 (c5_01, c5_02, c5_03): El rodaje de David Lynch en México (1984)
# ===========================================================================
def scene_lynch_mexico(t):
    t1 = TL.s("c5_01")
    t2 = TL.s("c5_02")
    t3 = TL.s("c5_03")
    cv = bg("bg_mexico_studio_1984").copy()

    window(cv, 16, 10, 448, 36, fill=(18, 18, 28), border=GOLD if t < t2 else RED, alpha=0.95)
    if t < t2:
        draw_text(cv, "1984 · PRIMERA ADAPTACIÓN AL CINE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DIRIGIDA POR DAVID LYNCH EN CIUDAD DE MÉXICO", 240, 30, "silk", 8, CYAN, align="center")
    elif t < t3:
        draw_text(cv, "FRACASO COMERCIAL EN TAQUILLA", 240, 16, "press", 8, RED, align="center")
        draw_text(cv, "COSTÓ US$ 40 MILLONES · RECAUDÓ MENOS DE US$ 31M", 240, 30, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "GOLPE DE LA CRÍTICA Y RUPTURA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA CRÍTICA LA DESTROZÓ · LYNCH RENEGÓ DE ELLA", 240, 30, "press", 8, RED, align="center")

    # David Lynch en el set de filmación (feet=260)
    char(cv, LYNCH, 104, 260, t, scale=2, arms="point" if t < t3 else "cross", look=1, mood="sad" if t >= t2 else "focused")
    robot(cv, 42, 260, t, face="sad" if t >= t2 else "question", scale=1)

    # Panel derecho con retrato de Lynch y balance de taquilla
    window(cv, 188, 56, 268, 114, fill=(20, 20, 32), border=GOLD if t < t2 else RED, alpha=0.96)
    portrait(cv, "lynch", 200, 68, 64)
    draw_text(cv, "DAVID LYNCH", 276, 68, "press", 8, GOLD)
    draw_text(cv, "ESTUDIOS CHURUBUSCO · 1984", 276, 84, "silk", 8, CYAN)

    if t < t2:
        draw_text(cv, "8 SETS GIGANTES Y", 276, 104, "silk", 8, CREAM)
        draw_text(cv, "PRODUCCIÓN MONUMENTAL", 276, 118, "silk", 8, CREAM)
    elif t < t3:
        draw_text(cv, "COSTO: US$ 40M", 276, 102, "press", 8, GOLD)
        draw_text(cv, "EE. UU.: < US$ 31M", 276, 120, "press", 8, RED)
    else:
        window(cv, 274, 100, 170, 52, fill=(76, 18, 24), border=RED, alpha=0.98)
        draw_text(cv, "CRÍTICA: NEGATIVA", 359, 112, "press", 8, CREAM, align="center")
        draw_text(cv, "SIN CORTE FINAL", 359, 130, "silk", 8, GOLD, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 16 Y 17 (c5_04, c5_05, c5_06): El chico canadiense de 17 años en la fila (1984)
# ===========================================================================
def scene_young_villeneuve_1984(t):
    t4 = TL.s("c5_04")
    t5 = TL.s("c5_05")
    t6 = TL.s("c5_06")
    cv = bg("bg_cinema_1984_line").copy()
    SNOW.draw(cv, t, density=0.65)

    window(cv, 16, 10, 448, 36, fill=(14, 20, 38), border=GOLD if t >= t6 else CYAN, alpha=0.95)
    if t < t5:
        draw_text(cv, "DICIEMBRE DE 1984 · DÍA DEL ESTRENO EN CANADÁ", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ADELANTE EN LA FILA: UN CHICO DE 17 AÑOS", 240, 30, "press", 8, GOLD, align="center")
    elif t < t6:
        draw_text(cv, "HABÍA LEÍDO LA NOVELA A LOS 13 AÑOS", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "«ALGÚN DÍA ALGUIEN LO VA A VOLVER A INTENTAR»", 240, 30, "press", 8, CREAM, align="center")
    else:
        draw_text(cv, "LA SEMILLA DEL FUTURO DIRECTOR DE DUNE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ESE ALGUIEN IBA A SER ÉL", 240, 30, "press", 8, GOLD, align="center")

    # Fila de espectadores en la vereda nevada (feet=260)
    char(cv, READER_1, 88, 260, t, scale=2, arms="cross", look=1)
    char(cv, READER_2, 160, 260, t, scale=2, arms="hips", look=1)

    # El joven Denis Villeneuve adelante en la fila (x=280, feet=260)
    if t >= t6:
        cv = spotlight(cv, 280, 48, 266, 36, 110, color=(255, 215, 110), strength=0.32)
    char(cv, YOUNG_DENIS, 280, 260, t, scale=2, arms="point" if t >= t6 else "note", look=1, mood="happy")
    robot(cv, 412, 260, t, face="excited" if t >= t6 else "question", scale=1)

    # Tarjeta sobre el joven Denis
    if t < t5:
        window(cv, 196, 64, 244, 66, fill=(16, 24, 44), border=CYAN, alpha=0.95)
        draw_text(cv, "QUEBEC, CANADÁ · 1984", 318, 76, "silk", 8, CYAN, align="center")
        draw_text(cv, "17 AÑOS EN LA FILA", 318, 94, "press", 8, GOLD, align="center")
        draw_text(cv, "LECTOR DE DUNE DESDE LOS 13", 318, 112, "silk", 8, CREAM, align="center")
    elif t < t6:
        window(cv, 184, 62, 268, 70, fill=(20, 26, 48), border=GOLD, alpha=0.96)
        draw_text(cv, "AL SALIR DEL CINE EN 1984:", 318, 74, "silk", 8, GOLD, align="center")
        draw_text(cv, "«ALGÚN DÍA ALGUIEN LO VA", 318, 94, "press", 8, CREAM, align="center")
        draw_text(cv, "A VOLVER A INTENTAR...»", 318, 112, "press", 8, CREAM, align="center")
    else:
        window(cv, 184, 58, 268, 82, fill=(36, 24, 12), border=GOLD, alpha=0.98)
        draw_text(cv, "ESE CHICO DE 17 AÑOS ERA", 318, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "DENIS VILLENEUVE", 318, 90, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "ESE ALGUIEN IBA A SER ÉL", 318, 118, "press", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


def scenes():
    return [
        (TL.chapter_start(5) - 0.3, make_card(5, ["EL DESIERTO", "EN MÉXICO"], "1984 · DAVID LYNCH Y EL ESTRENO", snow=True)),
        (TL.s("c5_01") - 0.15, scene_lynch_mexico),
        (TL.s("c5_04") - 0.15, scene_young_villeneuve_1984),
    ]
