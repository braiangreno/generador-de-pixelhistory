"""Capítulo 4: Simon (El primer smartphone de IBM en 1994, pantalla táctil con lápiz y por qué llegó demasiado temprano)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c4_s01_ibm_simon_features(t):
    """c4_01..c4_02: En 1994 IBM lanza Simon: pantalla táctil con lápiz, agenda, notas, correo y fax."""
    t0 = TL.s("c4_01")
    t_c4_02 = TL.s("c4_02")

    cv = bg("storefront_simon_1994").copy()
    draw_place_only(cv, "ESTADOS UNIDOS · 1994 · IBM SIMON", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    draw_simon_pedestal(cv, 240, 248, t)
    char(cv, "simon_buyer", 152, 248, t, scale=2,
         arms="point" if t >= t_c4_02 else "down", look=1, mood="happy")

    window(cv, 118, 42, 244, 102, fill=(16, 28, 44), border=TESLA_CYAN)
    if t < t_c4_02:
        draw_text(cv, "IBM SIMON (1994)", 240, 52, "press", 16, GOLD, align="center")
        draw_text(cv, "TELÉFONO CON PANTALLA TÁCTIL", 240, 82, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "13 AÑOS ANTES DEL IPHONE", 240, 102, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL PRIMERO DE LA HISTORIA", 240, 120, "silk", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "SE USABA CON UN LÁPIZ (STYLUS)", 240, 50, "silk", 8, GOLD, align="center")
        # 4 íconos LCD verdes del IBM Simon
        feats = [("AGENDA", 134), ("NOTAS", 190), ("CORREO", 248), ("FAX", 308)]
        for lbl, fx in feats:
            d.rectangle([fx, 68, fx + 46, 98], fill=(118, 192, 128, 255), outline=(*INK, 255))
            draw_text(cv, lbl, fx + 23, 80, "silk", 8, INK, align="center", outline=None, shadow=False)
        draw_text(cv, "HOY SE LO CONSIDERA EL 1º SMARTPHONE", 240, 114, "silk", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.36)


def c4_s02_simon_limits_and_legacy(t):
    """c4_03..c4_06: Medio kilo, 1 hora de batería, US$899, 50.000 vendidos -> llegó demasiado temprano."""
    t0 = TL.s("c4_03")
    t_c4_04 = TL.s("c4_04")
    t_c4_05 = TL.s("c4_05")
    t_c4_06 = TL.s("c4_06")

    cv = bg("storefront_simon_1994").copy()
    draw_place_only(cv, "IBM SIMON · 1994", t, t0, border=AMBER)

    draw_simon_pedestal(cv, 240, 248, t)
    char(cv, "simon_buyer", 152, 248, t, scale=2,
         arms="shrug" if t < t_c4_05 else "think", look=1, mood="worried")

    window(cv, 116, 42, 248, 104, fill=(22, 20, 36), border=GOLD if t >= t_c4_06 else CHALK_RED)
    if t < t_c4_04:
        draw_text(cv, "LOS PROBLEMAS EN 1994:", 240, 50, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "• PESO: 500 GRAMOS (MEDIO KILO)", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "• BATERÍA: DURABA 1 SOLA HORA", 240, 84, "silk", 8, GOLD, align="center")
        draw_text(cv, "• PRECIO: CASI US$ 900", 240, 100, "silk", 8, CREAM, align="center")
        draw_text(cv, "• SIN INTERNET EN EL BOLSILLO", 240, 118, "silk", 8, CHALK_RED, align="center")
    elif t < t_c4_05:
        draw_text(cv, "VENTAS TOTALES: ~50.000 UNIDADES", 240, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "DURACIÓN EN TIENDAS: 6 MESES", 240, 82, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "RETIRADO EN FEBRERO DE 1995", 240, 110, "silk", 8, SOFT_GRAY, align="center")
    elif t < t_c4_06 - 0.1:
        draw_text(cv, "PIEZAS QUE AÚN NO EXISTÍAN:", 240, 52, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "[ ] BATERÍAS DE LITIO DURADERAS", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "[ ] INTERNET MÓVIL RÁPIDO", 240, 94, "silk", 8, CREAM, align="center")
        draw_text(cv, "[ ] PANTALLA PARA EL DEDO", 240, 114, "silk", 8, GOLD, align="center")
    else:
        draw_text(cv, "IBM SIMON (1994):", 240, 54, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "NO FRACASÓ POR MALO.", 240, 78, "press", 8, CREAM, align="center")
        draw_text(cv, "LLEGÓ DEMASIADO TEMPRANO.", 240, 104, "press", 8, GOLD, align="center")

    return vignette(cv, 0.36)


def scenes():
    return [
        (TL.s("c4_00") - 0.15, make_card(4, ["SIMON"], "1994 · EL PRIMER SMARTPHONE"),
         None, "ch04"),
        (TL.s("c4_01") - 0.15, c4_s01_ibm_simon_features,
         lambda t: cam_push(t, TL.s("c4_01"), TL.s("c4_03"), 1.0, 1.03, (240, 135)), "ch04"),
        (TL.s("c4_03") - 0.15, c4_s02_simon_limits_and_legacy,
         lambda t: cam_push(t, TL.s("c4_03"), TL.s("c5_00"), 1.0, 1.03, (240, 135)), "ch04"),
    ]


def music(A):
    t0 = TL.s("c4_00")
    t_end = TL.s("c5_00")
    A.add_pad(t0, t_end - t0, [110.0, 164.81, 220.0], amp=0.036)


def sfx(A):
    A.fx_pop(TL.s("c4_01"), 0.08)
    A.fx_thud(TL.s("c4_03"), 0.08)
    A.fx_chime(TL.s("c4_06"), 0.10)
