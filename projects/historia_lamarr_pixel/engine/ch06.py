"""Capítulo 6: Bonos y besos (c6_00..c6_07) — La Marina archiva la patente y Hedy recauda 25 millones vendiendo bonos."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c6_s01_navy_rejects(t):
    """c6_01..c6_03: Regalan la patente a la Marina -> La descartan ('no entra un piano') -> Sugieren vender bonos de guerra."""
    t0 = TL.s("c6_01")
    t_desc = TL.word("c6_01", "descartó")
    t_c6_02 = TL.s("c6_02")
    t_piano = TL.word("c6_02", "piano")
    t_c6_03 = TL.s("c6_03")
    t_bonos = TL.word("c6_03", "bonos")

    cv = bg("navy_office_1942").copy()
    draw_place_only(cv, "MARINA DE EE. UU. · 1942", t, t0, border=AMBER)

    draw_table_with_prop(cv, 240, 248, prop_kind="drawer" if t >= t_desc - 0.2 else "patent",
                         t=t, open_p=0.8 if t < t_c6_03 else 0.1)

    char(cv, "navy_officer", 144, 248, t, scale=2,
         arms="cross" if t < t_c6_03 else "point", look=1, mood="neutral",
         talk=talk_v(t, t >= t_desc))
    char(cv, "antheil", 312, 248, t, scale=2,
         arms="shrug" if t >= t_c6_02 else "offer", look=-1, mood="sad")
    char(cv, "hedy_glam", 368, 248, t, scale=2,
         arms="hips" if t >= t_c6_03 else "down", look=-1, mood="sad")

    window(cv, 114, 44, 252, 76, fill=(18, 24, 38), border=CHALK_RED if t < t_c6_03 else GOLD, alpha=0.95)
    if t < t_c6_02 - 0.1:
        draw_text(cv, "DONARON LA PATENTE A LA MARINA", 240, 54, "silk", 8, CREAM, align="center")
        if t >= t_desc - 0.25:
            draw_text(cv, "RESPUESTA: «DESCARTADA»", 240, 74, "press", 8, CHALK_RED, align="center")
            draw_text(cv, "«NO ENTRA EN UN TORPEDO»", 240, 94, "silk", 8, GOLD, align="center")
    elif t < t_c6_03 - 0.1:
        draw_text(cv, "SOSPECHA DE GEORGE ANTHEIL:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "EL ERROR FUE NOMBRAR «UN PIANO»", 240, 74, "press", 8,
                  LAMARR_CYAN if t >= t_piano - 0.2 else CREAM, align="center")
        draw_text(cv, "DELANTE DE LOS OFICIALES", 240, 94, "silk", 8, SOFT_GRAY, align="center")
    else:
        draw_text(cv, "LA SUGERENCIA PARA HEDY:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "«AYUDE CON SU FAMA Y SU CARA»", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_bonos - 0.3:
            draw_text(cv, "VENDIENDO BONOS DE GUERRA", 240, 94, "press", 8, CHALK_GREEN, align="center")
    return vignette(cv, 0.36)


def c6_s02_war_bonds_and_punchline(t):
    """c6_04..c6_07: Beso por US$ 25.000 -> 7 millones en una noche, 25 millones en la gira -> El mismo marinero -> Remate."""
    t_c6_04 = TL.s("c6_04")
    t_siete = TL.word("c6_04", "siete")
    t_c6_05 = TL.s("c6_05")
    t_veint = TL.word("c6_05", "veinticinco")
    t_c6_06 = TL.s("c6_06")
    t_mismo = TL.word("c6_06", "mismo")
    t_c6_07 = TL.s("c6_07")
    t_cajon = TL.word("c6_07", "cajón")

    if t < t_c6_07 - 0.15:
        cv = bg("hollywood_dressing_room").copy()
        CONF.draw(cv, t)
        draw_place_only(cv, "GIRA DE BONOS DE GUERRA · EE. UU. (1942)", t, t_c6_04, border=GOLD)

        draw_table_with_prop(cv, 240, 248, prop_kind="patent", t=t)
        char(cv, "hedy_glam", 168, 248, t, scale=2, arms="wave", look=1, mood="happy")
        char(cv, "sailor", 312, 248, t, scale=2,
             arms="cheer" if t >= t_c6_06 else "up", look=-1, mood="happy")

        window(cv, 114, 44, 252, 76, fill=(22, 18, 38), border=GOLD, alpha=0.95)
        if t < t_c6_05 - 0.1:
            draw_text(cv, "1 BESO POR US$ 25.000 EN BONOS", 240, 54, "silk", 8, CREAM, align="center")
            if t >= t_siete - 0.3:
                draw_text(cv, "¡US$ 7 MILLONES EN UNA NOCHE!", 240, 74, "press", 8, GOLD, align="center")
                draw_text(cv, "RÉCORD DE RECAUDACIÓN", 240, 94, "silk", 8, CHALK_GREEN, align="center")
        elif t < t_c6_06 - 0.1:
            draw_text(cv, "GIRA POR VARIAS CIUDADES:", 240, 54, "silk", 8, CREAM, align="center")
            draw_text(cv, "¡UNOS US$ 25 MILLONES!", 240, 74, "press", 8,
                      CHALK_GREEN if t >= t_veint - 0.3 else GOLD, align="center")
            draw_text(cv, "PARA FINANCIAR EL ESFUERZO ALIADO", 240, 94, "silk", 8, LAMARR_CYAN, align="center")
        else:
            draw_text(cv, "EL SECRETO DEL SHOW:", 240, 54, "silk", 8, GOLD, align="center")
            draw_text(cv, "EL MARINERO «ELEGIDO AL AZAR»", 240, 74, "silk", 8, CREAM, align="center")
            if t >= t_mismo - 0.3:
                draw_text(cv, "¡ERA SIEMPRE EL MISMO ACTOR!", 240, 94, "press", 8, LAMARR_CYAN, align="center")
        return vignette(cv, 0.34)

    # c6_07: Remate del Capítulo 6 ("Su cara recaudó millones. Su idea quedó en un cajón.")
    cv = bg("navy_office_1942").copy()
    cv = grade(cv, mul=(0.82, 0.85, 0.95))
    draw_place_only(cv, "ARCHIVO DE LA MARINA · 1942", t, t_c6_07, border=CHALK_RED)

    draw_table_with_prop(cv, 240, 248, prop_kind="drawer", t=t, open_p=0.15)
    char(cv, "hedy_glam", 162, 248, t, scale=2, arms="down", look=1, mood="sad")

    window(cv, 114, 48, 252, 70, fill=(16, 20, 36), border=GOLD, alpha=0.96)
    draw_text(cv, "SU CARA RECAUDÓ MILLONES.", 240, 60, "press", 8, GOLD, align="center")
    if t >= t_cajon - 0.45:
        draw_text(cv, "SU IDEA QUEDÓ EN UN CAJÓN.", 240, 84, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "SELLADA COMO «CLASIFICADA»", 240, 102, "silk", 8, SOFT_GRAY, align="center")
    return vignette(cv, 0.40)


SCENES = [
    (TL.s("c6_00") - 0.15, TL.s("c6_01"), make_card(6, ["BONOS", "Y BESOS"], "1942 – 1945 · EE. UU.")),
    (TL.s("c6_01") - 0.15, TL.s("c6_04"), c6_s01_navy_rejects),
    (TL.s("c6_04") - 0.15, TL.s("c7_00"), c6_s02_war_bonds_and_punchline),
]


def scenes():
    return [(s[0], s[2], None, "ch06") for s in SCENES]


def music(A):
    return


def sfx(A):
    A.fx_thud(TL.word("c6_01", "descartó"), 0.10)
    A.fx_chime(TL.word("c6_04", "siete"), 0.10)
    A.fx_sparkle(TL.word("c6_05", "veinticinco"), 0.09)
    A.fx_pop(TL.word("c6_06", "mismo"), 0.08)
    A.fx_thud(TL.word("c6_07", "cajón"), 0.10)
