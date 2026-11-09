"""Capítulo 2: Más de veinte rechazos (c2_00..c2_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, READER_1, READER_2

LANIER = {
    "skin": (235, 194, 156), "hair": (76, 56, 40), "hair_style": "parted",
    "glasses": True,
    "shirt": (240, 244, 250), "jacket": (44, 62, 92),
    "tie": (180, 48, 48), "pants": (38, 48, 70),
}
PUBLISHER_NO = {
    "skin": (226, 184, 148), "hair": (130, 130, 138), "hair_style": "bald",
    "shirt": (230, 230, 235), "jacket": (72, 72, 82),
    "tie": (90, 90, 105), "pants": (54, 54, 64),
}


# ===========================================================================
# ESCENA 7 (c2_01): Más de veinte rechazos editoriales
# ===========================================================================
def scene_twenty_rejections(t):
    t0 = TL.s("c2_01")
    u = clamp01((t - t0) / max(1.0, TL.e("c2_01") - t0))
    cv = bg("bg_chilton_office_1965").copy()
    cv = grade(cv, mul=(0.82, 0.78, 0.85), add=(8, 0, 6), sat=0.85, k=0.9)

    window(cv, 16, 10, 448, 36, fill=(32, 14, 18), border=RED, alpha=0.95)
    n_rej = min(23, int(1 + u * 24))
    draw_text(cv, f"EDITORIALES QUE DIJERON NO: {n_rej}+", 240, 16, "press", 8, RED, align="center")
    draw_text(cv, "EL MANUSCRITO REBOTA DE PUERTA EN PUERTA", 240, 30, "silk", 8, CREAM, align="center")

    # Frank Herbert sosteniendo el manuscrito a la izquierda (feet=260)
    char(cv, HERBERT, 92, 260, t, scale=2, arms="cross", look=1, mood="sad")
    char(cv, PUBLISHER_NO, 396, 260, t, scale=2, arms="hips", look=-1, mood="angry")
    robot(cv, 36, 260, t, face="sad", scale=1)

    # Tres grandes sellos de rechazo en el centro
    reasons = [
        ("DEMASIADO LARGA", 0.10),
        ("DEMASIADO COMPLICADA", 0.38),
        ("DEMASIADO RARA", 0.66),
    ]
    for idx, (txt, th_u) in enumerate(reasons):
        if u >= th_u:
            ry = 60 + idx * 46
            window(cv, 144, ry, 206, 38, fill=(76, 18, 22), border=RED, alpha=0.96)
            draw_text(cv, f"RECHAZO #{idx * 7 + 5}", 247, ry + 8, "silk", 8, GOLD, align="center")
            draw_text(cv, txt, 247, ry + 21, "press", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 8 (c2_02, c2_03): Chilton Books (manuales de autos) y Sterling Lanier
# ===========================================================================
def scene_chilton_lanier(t):
    t2 = TL.s("c2_02")
    t3 = TL.s("c2_03")
    cv = bg("bg_chilton_office_1965").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(14, 24, 38), border=GOLD, alpha=0.95)
    if t < t3:
        draw_text(cv, "EDITORIAL CHILTON · FILADELFia", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "FAMOSA POR SUS MANUALES PARA ARREGLAR AUTOS", 240, 30, "silk", 8, CYAN, align="center")
    else:
        draw_text(cv, "EL EDITOR STERLING LANIER APUESTA POR DUNE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "LEYÓ LA REVISTA Y PAGÓ US$ 7.500 DE ADELANTO", 240, 30, "silk", 8, GREEN, align="center")

    # Estante visual de manuales de mecánica automotriz a la izquierda
    window(cv, 20, 56, 176, 94, fill=(18, 28, 48), border=CYAN, alpha=0.94)
    draw_text(cv, "CATÁLOGO CHILTON", 108, 64, "press", 8, CYAN, align="center")
    for idx, m_lbl in enumerate(("MOTOR V8 · 1964", "FRENOS Y CAJA", "CARBURADORES")):
        my = 80 + idx * 20
        d.rectangle([30, my, 186, my + 16], fill=(34, 58, 96, 255), outline=(*GOLD, 255))
        draw_text(cv, m_lbl, 108, my + 4, "silk", 8, CREAM, align="center")

    # Retrato y contrato de Sterling Lanier a la derecha
    window(cv, 212, 56, 248, 94, fill=(22, 32, 24), border=GREEN if t >= t3 else GOLD, alpha=0.95)
    portrait(cv, "lanier", 222, 66, 64)
    draw_text(cv, "STERLING LANIER", 296, 68, "press", 8, GOLD)
    draw_text(cv, "EDITOR DE CHILTON", 296, 84, "silk", 8, CYAN)
    if t < t3:
        draw_text(cv, "«YO PUBLICO ESTA", 296, 102, "silk", 8, CREAM)
        draw_text(cv, "NOVELA.»", 296, 116, "silk", 8, CREAM)
    else:
        window(cv, 294, 100, 154, 38, fill=(18, 68, 32), border=GREEN, alpha=0.98)
        draw_text(cv, "ADELANTO FIRMADO", 371, 107, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$ 7.500", 371, 121, "press", 8, GOLD, align="center")

    # Herbert y Lanier dándose la mano en el piso de la oficina (feet=260)
    char(cv, HERBERT, 148, 260, t, scale=2, arms="point", look=1, mood="happy")
    char(cv, LANIER, 272, 260, t, scale=2, arms="point", look=-1, talk=talk_v(t, True))
    robot(cv, 418, 260, t, face="happy", scale=1)

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 9 (c2_04, c2_05, c2_06): Despido de Lanier y Premios Hugo + Nébula (1966)
# ===========================================================================
def scene_release_and_awards(t):
    t4 = TL.s("c2_04")
    t5 = TL.s("c2_05")
    t6 = TL.s("c2_06")
    cv = bg("bg_bookstore_1965").copy()
    d = ImageDraw.Draw(cv)

    window(cv, 16, 10, 448, 36, fill=(24, 18, 14), border=GOLD, alpha=0.95)
    if t < t5:
        draw_text(cv, "AGOSTO DE 1965 · PRIMERA EDICIÓN", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECIO: US$ 5,95 · CARO Y DE VENTAS LENTAS", 240, 30, "silk", 8, CYAN, align="center")
    elif t < t6:
        draw_text(cv, "CONSECUENCIA EN LA EDITORIAL CHILTON", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "A STERLING LANIER LO DESPIDIERON", 240, 30, "press", 8, RED, align="center")
    else:
        draw_text(cv, "1966 · GIRO HISTÓRICO Y BOCA EN BOCA", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "GANA LOS DOS PREMIOS MÁS IMPORTANTES DEL GÉNERO", 240, 30, "silk", 8, GREEN, align="center")

    if t < t6:
        # Libro caro en vidriera y despido de Lanier
        window(cv, 148, 58, 184, 86, fill=(32, 20, 18), border=RED if t >= t5 else GOLD, alpha=0.95)
        draw_text(cv, "DUNE (1965)", 240, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECIO: US$ 5,95", 240, 86, "silk", 8, CREAM, align="center")
        if t < t5:
            draw_text(cv, "VENTAS INICIALES BAJAS", 240, 106, "silk", 8, RED, align="center")
        else:
            window(cv, 164, 102, 152, 28, fill=(130, 22, 22), border=RED, alpha=0.98)
            draw_text(cv, "LANIER DESPEDIDO", 240, 112, "press", 8, CREAM, align="center")

        char(cv, LANIER, 110, 260, t, scale=2, arms="cross", look=1, mood="sad")
        char(cv, HERBERT, 360, 260, t, scale=2, arms="hips", look=-1, mood="sad")
        robot(cv, 424, 260, t, face="sad", scale=1)
    else:
        # 1966: Premios Nébula y Hugo + lectores pasándose el libro de mano en mano
        CONF.draw(cv, t)
        window(cv, 56, 56, 174, 86, fill=(28, 24, 12), border=GOLD, alpha=0.96)
        draw_text(cv, "PREMIO NÉBULA", 143, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "1966 · MEJOR NOVELA", 143, 86, "silk", 8, CREAM, align="center")
        draw_text(cv, "1ª EDICIÓN DEL PREMIO", 143, 104, "silk", 8, CYAN, align="center")

        window(cv, 250, 56, 174, 86, fill=(28, 24, 12), border=GOLD, alpha=0.96)
        draw_text(cv, "PREMIO HUGO", 337, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "1966 · MEJOR NOVELA", 337, 86, "silk", 8, CREAM, align="center")
        draw_text(cv, "CONSAGRACIÓN MUNDIAL", 337, 104, "silk", 8, GREEN, align="center")

        # Herbert y dos lectores pasándose el libro de mano en mano (feet=260)
        char(cv, HERBERT, 92, 260, t, scale=2, arms="cheer", look=1, mood="happy")
        char(cv, READER_1, 224, 260, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, READER_2, 326, 260, t, scale=2, arms="point", look=-1, mood="happy")
        # Libro dorado pasando entre los dos lectores
        bx = int(244 + 48 * (0.5 + 0.5 * math.sin(t * 3.2)))
        d.rectangle([bx - 10, 204, bx + 10, 226], fill=(238, 174, 58, 255), outline=(*INK, 255))
        robot(cv, 424, 260, t, face="excited", scale=1)

    draw_sand_ripple(cv, t, y_base=262, x_start=36, x_end=444)
    return cv


def scenes():
    return [
        (TL.chapter_start(2) - 0.3, make_card(2, ["MÁS DE VEINTE", "RECHAZOS"], "1965 - 1966 · CHILTON BOOKS Y PREMIOS")),
        (TL.s("c2_01") - 0.15, scene_twenty_rejections),
        (TL.s("c2_02") - 0.15, scene_chilton_lanier),
        (TL.s("c2_04") - 0.15, scene_release_and_awards),
    ]
