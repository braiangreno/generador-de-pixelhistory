"""Capítulo 5: El desierto en México (c5_00..c5_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import READER_1, READER_2

LYNCH = {
    "name": "David Lynch",
    "skin": (238, 198, 164), "hair": (74, 54, 42), "hair_style": "parted",
    "shirt": (246, 246, 250), "jacket": (28, 30, 38),
    "tie": (40, 40, 48), "pants": (24, 26, 34),
}
CREW_CAM = {
    "name": "Crew Camera",
    "skin": (224, 178, 140), "hair": (54, 40, 32), "hair_style": "short",
    "shirt": (196, 174, 134), "jacket": (78, 66, 52),
    "pants": (48, 44, 38),
}
YOUNG_DENIS = {
    "name": "Young Denis",
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
    dx, dy = shake(t, t2 + 0.15, dur=0.25, amp=3)
    cv = bg("bg_mexico_studio_1984").copy()

    window(cv, 16, 10, 448, 36, fill=(18, 18, 28), border=GOLD if t < t2 else RED, alpha=0.95)
    if t < t2:
        draw_text(cv, "1984 · PRIMERA ADAPTACIÓN AL CINE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DIRIGIDA POR DAVID LYNCH EN CIUDAD DE MÉXICO", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t1) * 32)
    elif t < t3:
        draw_text(cv, "FRACASO COMERCIAL EN TAQUILLA", 240, 16, "press", 8, RED, align="center")
        draw_text(cv, "COSTÓ US$ 40 MILLONES · RECAUDÓ MENOS DE US$ 31M", 240, 30, "silk", 8, CREAM, align="center",
                  reveal=(t - t2) * 32)
    else:
        draw_text(cv, "GOLPE DE LA CRÍTICA Y RUPTURA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA CRÍTICA LA DESTROZÓ · LYNCH RENEGÓ DE ELLA", 240, 30, "press", 8, RED, align="center",
                  reveal=(t - t3) * 32)

    # David Lynch dirige en c5_01; se preocupa en c5_02 ("menos de 31"); y se da vuelta alejándose cuando dice "Lynch terminó renegando de ella"
    t_renegando = TL.word("c5_03", "renegando")
    if t < t3:
        char(cv, LYNCH, 88, 260, t, scale=2,
             arms="point" if t < t2 else "shrug", look=1,
             mood="focused" if t < t2 else "sad", talk=talk_v(t, t < t2))
        char(cv, CREW_CAM, 154, 260, t, scale=2,
             arms="work" if t < t2 else "hips", look=-1, mood="neutral")
    else:
        lx, lph = walk(t, t_renegando, TL.e("c5_03"), 88, 42)
        char(cv, LYNCH, lx, 260, t, scale=2, walk=lph,
             arms="cross", look=-1 if t >= t_renegando else 1, mood="sad")
        char(cv, CREW_CAM, 154, 260, t, scale=2, arms="shrug", look=-1, mood="sad")

    # Panel derecho con retrato de Lynch y balance de taquilla
    a_p, dy_p = pop(t, t1 + 0.05)
    window(cv, 196, 56 + dy_p, 260, 114, fill=(20, 20, 32), border=GOLD if t < t2 else RED, alpha=0.96 * a_p)
    portrait(cv, "lynch", 206, 68 + dy_p, 64)
    draw_text(cv, "DAVID LYNCH", 280, 68 + dy_p, "press", 8, GOLD)
    draw_text(cv, "ESTUDIOS CHURUBUSCO · 1984", 280, 84 + dy_p, "silk", 8, CYAN)

    if t < t2:
        draw_text(cv, "8 SETS GIGANTES Y", 280, 104 + dy_p, "silk", 8, CREAM, reveal=(t - t1 - 0.2) * 28)
        draw_text(cv, "PRODUCCIÓN MONUMENTAL", 280, 118 + dy_p, "silk", 8, CREAM, reveal=(t - t1 - 0.5) * 28)
    elif t < t3:
        draw_text(cv, "COSTO: US$ 40M", 280, 102 + dy_p, "press", 8, GOLD)
        draw_text(cv, "EE. UU.: < US$ 31M", 280, 120 + dy_p, "press", 8, RED)
    else:
        a_r, dy_r = pop(t, t3 + 0.05)
        window(cv, 278, 100 + dy_r, 168, 52, fill=(76, 18, 24), border=RED, alpha=0.98 * a_r)
        draw_text(cv, "CRÍTICA: NEGATIVA", 362, 112 + dy_r, "press", 8, CREAM, align="center")
        draw_text(cv, "SIN CORTE FINAL", 362, 130 + dy_r, "silk", 8, GOLD, align="center")

    return offset_canvas(cv, dx, dy)


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
        draw_text(cv, "ADELANTE EN LA FILA: UN CHICO DE 17 AÑOS", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t4) * 32)
    elif t < t6:
        draw_text(cv, "HABÍA LEÍDO LA NOVELA A LOS 13 AÑOS", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "«ALGÚN DÍA ALGUIEN LO VA A VOLVER A INTENTAR»", 240, 30, "press", 8, CREAM, align="center",
                  reveal=(t - t5) * 32)
    else:
        draw_text(cv, "LA SEMILLA DEL FUTURO DIRECTOR DE DUNE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ESE ALGUIEN IBA A SER ÉL", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t6) * 32)

    # Fila de espectadores en la vereda nevada; el joven Denis da un paso adelante y piensa en "Salió pensando" (c5_05)
    t_libro = TL.word("c5_04", "libro")
    ydx, ydph = walk(t, t5, t5 + 0.85, 236, 286)
    char(cv, READER_1, 74, 260, t, scale=2, arms="cross", look=1)
    char(cv, READER_2, 142, 260, t, scale=2, arms="hips", look=1)

    # El joven Denis Villeneuve adelante en la fila
    if t >= t6:
        cv = spotlight(cv, int(ydx), 48, 266, 36, 110, color=(255, 215, 110), strength=0.35)
    yd_arms = "point" if t >= t6 else ("think" if t >= t5 else ("note" if t >= t_libro else "hold"))
    char(cv, YOUNG_DENIS, ydx, 260, t, scale=2, walk=ydph,
         arms=yd_arms, look=1, mood="happy" if t >= t6 else "focused")

    # Tarjeta sobre el joven Denis con entrada pop()
    if t < t5:
        a_c, dy_c = pop(t, t4 + 0.1)
        window(cv, 196, 64 + dy_c, 244, 66, fill=(16, 24, 44), border=CYAN, alpha=0.95 * a_c)
        draw_text(cv, "QUEBEC, CANADÁ · 1984", 318, 76 + dy_c, "silk", 8, CYAN, align="center")
        draw_text(cv, "17 AÑOS EN LA FILA", 318, 94 + dy_c, "press", 8, GOLD, align="center")
        draw_text(cv, "LECTOR DE DUNE DESDE LOS 13", 318, 112 + dy_c, "silk", 8, CREAM, align="center")
    elif t < t6:
        a_c, dy_c = pop(t, t5 + 0.05)
        window(cv, 184, 62 + dy_c, 268, 70, fill=(20, 26, 48), border=GOLD, alpha=0.96 * a_c)
        draw_text(cv, "AL SALIR DEL CINE EN 1984:", 318, 74 + dy_c, "silk", 8, GOLD, align="center")
        draw_text(cv, "«ALGÚN DÍA ALGUIEN LO VA", 318, 94 + dy_c, "press", 8, CREAM, align="center",
                  reveal=(t - t5 - 0.1) * 28)
        draw_text(cv, "A VOLVER A INTENTAR...»", 318, 112 + dy_c, "press", 8, CREAM, align="center",
                  reveal=(t - t5 - 0.5) * 28)
    else:
        a_c, dy_c = pop(t, t6 + 0.05)
        window(cv, 184, 58 + dy_c, 268, 82, fill=(36, 24, 12), border=GOLD, alpha=0.98 * a_c)
        draw_text(cv, "ESE CHICO DE 17 AÑOS ERA", 318, 70 + dy_c, "silk", 8, CYAN, align="center")
        draw_text(cv, "DENIS VILLENEUVE", 318, 90 + dy_c, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "ESE ALGUIEN IBA A SER ÉL", 318, 118 + dy_c, "press", 8, CREAM, align="center")
        sparkle(cv, 198, 88 + dy_c, t, 3)
        sparkle(cv, 438, 94 + dy_c, t + 1.1, 3)

    return cv


def scenes():
    return [
        (TL.chapter_start(5) - 0.3, make_card(5, ["EL DESIERTO", "EN MÉXICO"], "1984 · DAVID LYNCH Y EL ESTRENO", snow=True), None),
        (TL.s("c5_01") - 0.15, scene_lynch_mexico, lambda t: (1.0 + cam_punch(t, [TL.s("c5_02"), TL.s("c5_03")], 0.06), 240, 140)),
        (TL.s("c5_04") - 0.15, scene_young_villeneuve_1984, lambda t: cam_push(t, TL.s("c5_04"), TL.e("c5_06"), 1.0, 1.12, (240, 145), (295, 145))),
    ]
