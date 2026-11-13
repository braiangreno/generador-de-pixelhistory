"""Capítulo 2: La jaula de oro (c2_00..c2_07) — Fritz Mandl, las cenas de armamento en Viena y la fuga de 1937."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c2_s01_mandl_and_copies(t):
    """c2_01..c2_03: Casamiento con Fritz Mandl -> mansión vigilada -> intento fallido de comprar todas las copias."""
    t0 = TL.s("c2_01")
    t_c2_02 = TL.s("c2_02")
    t_vig = TL.word("c2_02", "vigilada")
    t_c2_03 = TL.s("c2_03")
    t_nuevas = TL.word("c2_03", "nuevas")

    cv = bg("vienna_mansion_cage").copy()
    draw_place_only(cv, "VIENA · MANSIÓN DE FRITZ MANDL (1933)", t, t0, border=GOLD)

    if t < t_c2_03 - 0.15:
        window(cv, 118, 46, 244, 66, fill=(24, 18, 34), border=GOLD, alpha=0.94)
        if t < t_c2_02 - 0.1:
            draw_text(cv, "FRITZ MANDL · FABRICANTE DE ARMAS", 240, 56, "silk", 8, GOLD, align="center")
            draw_text(cv, "UNO DE LOS MAYORES DE AUSTRIA", 240, 74, "silk", 8, CREAM, align="center")
            draw_text(cv, "SE CASARON ESE MISMO AÑO (1933)", 240, 92, "press", 8, LAMARR_CYAN, align="center")
        else:
            draw_text(cv, "LA JAULA DE ORO", 240, 56, "press", 8, GOLD, align="center")
            draw_text(cv, "RODEADA DE LUJO...", 240, 76, "silk", 8, CREAM, align="center")
            if t >= t_vig - 0.25:
                draw_text(cv, "...Y SIEMPRE VIGILADA", 240, 92, "press", 8, CHALK_RED, align="center")

        char(cv, "mandl", 168, 248, t, scale=2, arms="cross" if t >= t_c2_02 else "down",
             look=1, mood="neutral")
        char(cv, "hedy_glam", 304, 248, t, scale=2, arms="down", look=-1,
             mood="sad" if t >= t_c2_02 else "neutral")
        return vignette(cv, 0.38)

    # c2_03: Mandl intenta comprar todas las copias de la película, pero siguen saliendo copias nuevas
    draw_table_with_prop(cv, 240, 248, prop_kind="film_cans", t=t)
    char(cv, "mandl", 152, 248, t, scale=2, arms="point", look=1, mood="worried",
         talk=talk_v(t, t < t_nuevas))
    char(cv, "hedy_glam", 328, 248, t, scale=2, arms="cross", look=-1, mood="neutral")

    window(cv, 118, 46, 244, 66, fill=(24, 18, 34), border=CHALK_RED if t >= t_nuevas - 0.2 else GOLD)
    draw_text(cv, "OBSESIÓN: COMPRAR CADA COPIA", 240, 56, "silk", 8, GOLD, align="center")
    if t < t_nuevas - 0.2:
        draw_text(cv, "«¡QUE NADIE MÁS VEA ESA PELÍCULA!»", 240, 76, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "NO PUDO: ¡HACÍAN COPIAS NUEVAS!", 240, 76, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "EL LABORATORIO SEGUÍA IMPRIMIENDO", 240, 94, "silk", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.38)


def c2_s02_weapons_dinners(t):
    """c2_04..c2_05: Cenas con militares y clientes de Mussolini -> Ella escucha sobre armas guiadas por radio y bloqueo."""
    t_c2_04 = TL.s("c2_04")
    t_muss = TL.word("c2_04", "Mussolini")
    t_c2_05 = TL.s("c2_05")
    t_esc = TL.word("c2_05", "escuchaba")
    t_radio = TL.word("c2_05", "radio")
    t_bloq = TL.word("c2_05", "bloquearlas")

    cv = bg("vienna_mansion_cage").copy()
    draw_place_only(cv, "CENAS DE ARMAMENTO · VIENA (1935)", t, t_c2_04, border=AMBER)

    # Mesa con radio/maqueta militar en el centro y los comensales alrededor
    draw_table_with_prop(cv, 232, 248, prop_kind="radio" if t >= t_radio - 0.3 else "torpedo", t=t)

    char(cv, "mandl", 128, 248, t, scale=2, arms="point", look=1, mood="happy",
         talk=talk_v(t, t < t_c2_05))
    char(cv, "general_guest", 182, 248, t, scale=2, arms="cross", look=1, mood="neutral",
         talk=talk_v(t, t_c2_05 <= t < t_bloq))
    char(cv, "hedy_glam", 336, 248, t, scale=2,
         arms="think" if t >= t_esc - 0.2 else "down", look=-1, mood="neutral")

    if t >= t_esc - 0.2:
        glow(cv, 336, 152, 22, LAMARR_CYAN, 0.55)

    window(cv, 116, 46, 248, 72, fill=(16, 22, 38), border=LAMARR_CYAN if t >= t_esc - 0.2 else GOLD)
    if t < t_c2_05 - 0.1:
        draw_text(cv, "REUNIONES CON MILITARES", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "CLIENTES DE ARMAS Y TECNOLOGÍA", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_muss - 0.3:
            draw_text(cv, "CLIENTE: GOBIERNO DE MUSSOLINI", 240, 92, "press", 8, CHALK_RED, align="center")
    else:
        draw_text(cv, "ELLA ESCUCHABA Y RECORDABA TODO:", 240, 56, "silk", 8, LAMARR_CYAN, align="center")
        draw_text(cv, "1. TORPEDOS GUIADOS POR RADIO", 240, 74, "press", 8, CREAM, align="center")
        if t >= t_bloq - 0.3:
            draw_text(cv, "2. EL PROBLEMA: ¡FÁCILES DE BLOQUEAR!", 240, 94, "silk", 8, CHALK_RED, align="center")
    return vignette(cv, 0.38)


def c2_s03_maid_escape(t):
    """c2_06..c2_07: En 1937 escapa disfrazada de mucama -> Se fue con lo puesto y con todo lo que había escuchado."""
    t_c2_06 = TL.s("c2_06")
    t_muc = TL.word("c2_06", "mucama")
    t_c2_07 = TL.s("c2_07")
    t_esc = TL.word("c2_07", "escuchado")

    cv = bg("vienna_street_1914").copy()
    cv = grade(cv, mul=(0.75, 0.82, 1.05))
    draw_place_only(cv, "FUGA NOCTURNA · 1937", t, t_c2_06, border=LAMARR_CYAN)

    # Hedy disfrazada de mucama caminando decidida hacia la derecha (libertad)
    x_h, w_h = walk(t, t_c2_06, t_c2_07 + 0.5, 136, 292)
    char(cv, "hedy_maid", x_h, 248, t, scale=2, walk=w_h,
         arms="think" if t >= t_c2_07 else "down", look=1, mood="happy")

    if t >= t_c2_07 - 0.15:
        glow(cv, int(x_h), 152, 24, LAMARR_CYAN, 0.6)

    window(cv, 116, 46, 248, 70, fill=(14, 20, 38), border=GOLD if t < t_c2_07 else LAMARR_CYAN)
    if t < t_c2_07 - 0.1:
        draw_text(cv, "1937 · ESCAPE HACIA PARÍS Y LONDRES", 240, 56, "silk", 8, GOLD, align="center")
        if t >= t_muc - 0.3:
            draw_text(cv, "DISFRAZADA DE MUCAMA", 240, 76, "press", 8, LAMARR_CYAN, align="center")
            draw_text(cv, "DEJANDO ATRÁS LA JAULA DE ORO", 240, 94, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "SE FUE CON LO PUESTO.", 240, 56, "press", 8, CREAM, align="center")
        if t >= t_esc - 0.45:
            draw_text(cv, "Y CON LOS SECRETOS DE ESAS CENAS", 240, 76, "silk", 8, GOLD, align="center")
            draw_text(cv, "GUARDADOS EN SU CABEZA.", 240, 94, "press", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.38)


SCENES = [
    (TL.s("c2_00") - 0.15, TL.s("c2_01"), make_card(2, ["LA JAULA", "DE ORO"], "1933 – 1937 · VIENA")),
    (TL.s("c2_01") - 0.15, TL.s("c2_04"), c2_s01_mandl_and_copies),
    (TL.s("c2_04") - 0.15, TL.s("c2_06"), c2_s02_weapons_dinners),
    (TL.s("c2_06") - 0.15, TL.s("c3_00"), c2_s03_maid_escape),
]


def scenes():
    return [(s[0], s[2], None, "ch02") for s in SCENES]


def music(A):
    t0 = TL.s("c2_00")
    t_esc = TL.s("c2_06")
    t_end = TL.s("c3_00")
    A.add_pad(t0, t_esc - t0, [110.0, 146.83, 220.0], amp=0.038)
    A.add_pad(t_esc, t_end - t_esc, [110.0, 164.81, 220.0, 329.63], amp=0.044)


def sfx(A):
    A.fx_pop(TL.s("c2_01"), 0.09)
    A.fx_thud(TL.word("c2_02", "vigilada"), 0.10)
    A.fx_pop(TL.word("c2_03", "nuevas"), 0.09)
    A.fx_thud(TL.word("c2_04", "Mussolini"), 0.09)
    A.fx_sparkle(TL.word("c2_05", "escuchaba"), 0.10)
    A.fx_sweep(TL.s("c2_06"), 0.45, 220, 440, 0.08)
    A.fx_chime(TL.word("c2_07", "escuchado"), 0.11)
