"""Capítulo 4: El problema del torpedo (c4_00..c4_07) — Atlántico 1940 y LA PIZARRA 1 (Frecuencia, Canal y Bloqueo)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c4_s01_atlantic_1940(t):
    """c4_01..c4_02: En 1940 un submarino hunde barco con niños británicos -> Hedy quiere ayudar y recuerda las cenas en Viena."""
    t0 = TL.s("c4_01")
    t_c4_02 = TL.s("c4_02")
    t_viena = TL.word("c4_02", "Viena")

    if t < t_c4_02 - 0.15:
        cv = bg("atlantic_night_1940").copy()
        RAIN.draw(cv, t)
        draw_place_only(cv, "ATLÁNTICO NORTE · SEPTIEMBRE DE 1940", t, t0, border=CHALK_RED)

        window(cv, 116, 48, 248, 74, fill=(14, 20, 36), border=CHALK_RED, alpha=0.94)
        draw_text(cv, "GUERRA EN EL ATLÁNTICO (1940)", 240, 58, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "SUBMARINO HUNDE BARCO DE EVACUACIÓN", 240, 78, "silk", 8, CREAM, align="center")
        draw_text(cv, "CON NIÑOS BRITÁNICOS RUMBO A CANADÁ", 240, 96, "silk", 8, GOLD, align="center")

        draw_table_with_prop(cv, 240, 248, prop_kind="radio", t=t)
        char(cv, "navy_officer", 148, 248, t, scale=2, arms="down", look=1, mood="sad")
        return vignette(cv, 0.42)

    # c4_02: Hedy en Hollywood decide ayudar y recuerda las cenas en Viena
    cv = bg("hollywood_dining_patent").copy()
    draw_place_only(cv, "HOLLYWOOD · 1940", t, t_c4_02, border=LAMARR_CYAN)

    draw_table_with_prop(cv, 276, 248, prop_kind="torpedo", t=t)
    char(cv, "hedy_inventor", 172, 248, t, scale=2, arms="think", look=1, mood="worried")
    glow(cv, 172, 152, 24, LAMARR_CYAN, 0.55)

    window(cv, 116, 48, 248, 68, fill=(16, 22, 42), border=LAMARR_CYAN, alpha=0.94)
    draw_text(cv, "HEDY QUERÍA AYUDAR A LOS ALIADOS", 240, 58, "silk", 8, GOLD, align="center")
    if t >= t_viena - 0.4:
        draw_text(cv, "Y RECORDÓ LAS CENAS EN VIENA:", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL PROBLEMA DE LOS TORPEDOS", 240, 94, "press", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.36)


def c4_s02_pizarra_torpedo(t):
    """c4_03..c4_07: LA PIZARRA 1 — Frecuencia, Canal y por qué el enemigo deja sordo al torpedo."""
    t0 = TL.s("c4_03")
    t_c4_04 = TL.s("c4_04")
    t_c4_05 = TL.s("c4_05")
    t_c4_06 = TL.s("c4_06")
    t_sordo = TL.word("c4_06", "sordo")
    t_c4_07 = TL.s("c4_07")

    cv = draw_pizarra_frame(t, t0, "FRECUENCIA Y CANAL",
                            summary_es="UN SOLO CANAL ES FÁCIL DE TAPAR",
                            t_summary=t_c4_07)
    d = ImageDraw.Draw(cv)

    # Panel central de tiza dentro de x=116..364 (w=248) para compatibilidad 1:1 con 9:16
    window(cv, 116, 42, 248, 156, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96, inner=(38, 78, 54))

    if t < t_c4_04 - 0.1:
        # Paso 1: Barco -> onda de radio -> Torpedo bajo el agua
        draw_text(cv, "TORPEDO GUIADO POR RADIO:", 240, 50, "silk", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "COMO UN AUTO A CONTROL REMOTO", 240, 66, "silk", 8, CHALK_WHITE, align="center")
        # Barco a la izquierda (x=142) y Torpedo a la derecha (x=312)
        d.polygon([(130, 122), (178, 122), (170, 134), (138, 134)], fill=(*CHALK_WHITE, 255))
        d.rectangle([146, 112, 162, 122], fill=(*CHALK_CYAN, 255))
        draw_text(cv, "BARCO", 154, 140, "silk", 8, CHALK_CYAN, align="center")

        d.ellipse([292, 118, 344, 132], fill=(*CHALK_YELLOW, 255), outline=(*INK, 255))
        draw_text(cv, "TORPEDO", 318, 140, "silk", 8, CHALK_YELLOW, align="center")

        # Onda viajando del barco al torpedo
        pts = [(x, 125 + int(round(math.sin(x * 0.25 - t * 12.0) * 5))) for x in range(184, 288, 3)]
        d.line(pts, fill=(*CHALK_CYAN, 255), width=2)
        draw_text(cv, "ÓRDENES POR RADIO >>>", 240, 166, "press", 8, CHALK_GREEN, align="center")

    elif t < t_c4_06 - 0.1:
        # Paso 2 (c4_04 y c4_05): Frecuencia = vibraciones/seg -> Cada frecuencia es un canal -> Torpedo escucha 1 solo
        hdr = "FRECUENCIA = VIBRACIONES / SEG" if t < t_c4_05 else "CADA FRECUENCIA ES UN CANAL:"
        draw_text(cv, hdr, 240, 50, "silk", 8, CHALK_YELLOW, align="center")
        draw_freq_lanes(cv, 126, 68, 228, 92, t, n_lanes=3, speed=2.8, jammed_lane=None,
                        hopping=False, show_labels=True)
        sub_l = "CADA EMISORA VIBRA A SU RITMO" if t < t_c4_05 else "EL TORPEDO ESCUCHA UN SOLO CANAL (CH 2)"
        draw_text(cv, sub_l, 240, 168, "silk", 8, CHALK_CYAN, align="center")

    else:
        # Paso 3 (c4_06 y c4_07): El enemigo encuentra ese canal y lo llena de ruido -> ¡El torpedo queda sordo!
        draw_text(cv, "¡EL ENEMIGO LLENA EL CANAL DE RUIDO!", 240, 50, "silk", 8, CHALK_RED, align="center")
        draw_freq_lanes(cv, 126, 68, 228, 92, t, n_lanes=3, speed=2.8, jammed_lane=1,
                        hopping=False, show_labels=True)
        msg_b = "EL TORPEDO QUEDA SORDO (PIERDE RUMBO)" if t >= t_sordo - 0.25 else "COMO GRITAR ENCIMA DE TU VOZ"
        draw_text(cv, msg_b, 240, 168, "press" if t >= t_sordo - 0.25 else "silk", 8,
                  CHALK_RED if t >= t_sordo - 0.25 else CHALK_YELLOW, align="center")

    return vignette(cv, 0.28)


SCENES = [
    (TL.s("c4_00") - 0.15, TL.s("c4_01"), make_card(4, ["EL PROBLEMA", "DEL TORPEDO"], "1940 · EL ATLÁNTICO")),
    (TL.s("c4_01") - 0.15, TL.s("c4_03"), c4_s01_atlantic_1940),
    (TL.s("c4_03") - 0.15, TL.s("c5_00"), c4_s02_pizarra_torpedo),
]


def scenes():
    return [(s[0], s[2], None, "ch04") for s in SCENES]


def music(A):
    return


def sfx(A):
    A.fx_thud(TL.s("c4_01") + 0.3, 0.09)
    A.fx_sparkle(TL.word("c4_02", "Viena"), 0.08)
    A.fx_pop(TL.s("c4_03"), 0.08)
    A.fx_thud(TL.word("c4_06", "sordo"), 0.10)
    A.fx_chime(TL.s("c4_07"), 0.10)
