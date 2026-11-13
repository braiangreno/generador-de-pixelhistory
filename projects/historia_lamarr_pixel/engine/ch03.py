"""Capítulo 3: La mujer más linda del mundo (c3_00..c3_08) — El barco con Louis B. Mayer, MGM y Howard Hughes."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c3_s01_ship_and_mayer(t):
    """c3_01..c3_03: Rechaza contrato chico en Londres -> Sube al mismo barco que Mayer -> Contrato 4x mejor y nombre Hedy Lamarr."""
    t0 = TL.s("c3_01")
    t_no = TL.word("c3_01", "no")
    t_c3_02 = TL.s("c3_02")
    t_c3_03 = TL.s("c3_03")
    t_cuatro = TL.word("c3_03", "cuatro")
    t_nom = TL.word("c3_03", "Hedy")

    cv = bg("ocean_liner_1937").copy()
    STARS.draw(cv, t, alpha=0.65)
    place_lbl = "LONDRES · 1937" if t < t_c3_02 else "TRANSATLÁNTICO RUMBO A NUEVA YORK"
    draw_place_only(cv, place_lbl, t, t0, border=GOLD)

    char(cv, "mayer", 158, 248, t, scale=2,
         arms="offer" if t < t_no else ("cheer" if t >= t_c3_03 else "think"),
         look=1, mood="happy" if t >= t_c3_03 else "neutral",
         talk=talk_v(t, t < t_no or t >= t_c3_03))
    char(cv, "hedy_glam", 312, 248, t, scale=2,
         arms="cross" if (t_no - 0.2 <= t < t_c3_02) else ("wave" if t >= t_nom - 0.2 else "hips"),
         look=-1, mood="happy")

    window(cv, 116, 46, 248, 72, fill=(14, 22, 42), border=GOLD, alpha=0.94)
    if t < t_c3_02 - 0.1:
        draw_text(cv, "LOUIS B. MAYER · JEFE DE MGM", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "OFERTA INICIAL: CONTRATO CHICO", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_no - 0.25:
            draw_text(cv, "RESPUESTA DE ELLA: «NO»", 240, 92, "press", 8, CHALK_RED, align="center")
    elif t < t_c3_03 - 0.1:
        draw_text(cv, "EL PLAN EN ALTA MAR", 240, 56, "press", 8, LAMARR_CYAN, align="center")
        draw_text(cv, "SACÓ PASAJE EN EL MISMO BARCO", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "EN EL QUE MAYER VOLVÍA A EE. UU.", 240, 94, "silk", 8, GOLD, align="center")
    else:
        draw_text(cv, "AL BAJAR EN NUEVA YORK:", 240, 56, "silk", 8, CREAM, align="center")
        draw_text(cv, "¡CONTRATO 4 VECES MEJOR!", 240, 74, "press", 8, CHALK_GREEN, align="center")
        if t >= t_nom - 0.35:
            draw_text(cv, "NUEVO NOMBRE: HEDY LAMARR", 240, 94, "press", 8, GOLD, align="center")
    return vignette(cv, 0.35)


def c3_s02_star_and_inventions(t):
    """c3_04..c3_05: Éxito inmediato en Hollywood -> Entre toma y toma se aburre e inventa (pastilla gaseosa, semáforo)."""
    t_c3_04 = TL.s("c3_04")
    t_c3_05 = TL.s("c3_05")
    t_past = TL.word("c3_05", "pastilla")
    t_sem = TL.word("c3_05", "semáforo")

    cv = bg("hollywood_dressing_room").copy()
    draw_place_only(cv, "ESTUDIOS MGM · HOLLYWOOD (1938)", t, t_c3_04, border=GOLD)

    if t < t_c3_05 - 0.15:
        draw_table_with_prop(cv, 296, 248, prop_kind="film_cans", t=t)
        char(cv, "hedy_glam", 184, 248, t, scale=2, arms="wave", look=1, mood="happy")

        window(cv, 116, 46, 248, 68, fill=(24, 18, 36), border=GOLD, alpha=0.94)
        draw_text(cv, "ESTRELLA DE HOLLYWOOD", 240, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "«LA MUJER MÁS LINDA DEL MUNDO»", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "ÉXITO INMEDIATO · VARIOS FILMS AL AÑO", 240, 94, "silk", 8, LAMARR_CYAN, align="center")
        return vignette(cv, 0.35)

    # c3_05: En el camarín entre toma y toma inventa una pastilla de gaseosa y un semáforo mejorado
    draw_table_with_prop(cv, 268, 248, prop_kind="soda_lamp", t=t)
    char(cv, "hedy_inventor", 172, 248, t, scale=2, arms="work", look=1, mood="happy")

    window(cv, 116, 46, 248, 72, fill=(16, 24, 42), border=LAMARR_CYAN, alpha=0.94)
    draw_text(cv, "ENTRE TOMA Y TOMA: INVENTABA", 240, 56, "press", 8, LAMARR_CYAN, align="center")
    draw_text(cv, "1. PASTILLA DE AGUA -> GASEOSA", 240, 76, "silk", 8,
              GOLD if t >= t_past - 0.2 else CREAM, align="center")
    if t >= t_sem - 0.35:
        draw_text(cv, "2. SEMÁFORO MEJORADO", 240, 94, "silk", 8, CHALK_GREEN, align="center")
    return vignette(cv, 0.35)


def c3_s03_hughes_and_wings(t):
    """c3_06..c3_08: Howard Hughes le da equipos -> Ala más rápida (pez + pájaro) -> 'Hollywood le pagaba por quedarse quieta'."""
    t_c3_06 = TL.s("c3_06")
    t_ala = TL.word("c3_06", "ala")
    t_c3_07 = TL.s("c3_07")
    t_genio = TL.word("c3_07", "genio")
    t_c3_08 = TL.s("c3_08")
    t_no = TL.word("c3_08", "no")

    cv = bg("hollywood_dressing_room").copy()
    draw_place_only(cv, "LABORATORIO EN SU CAMARÍN · HOLLYWOOD", t, t_c3_06, border=LAMARR_CYAN)

    draw_table_with_prop(cv, 240, 248, prop_kind="patent", t=t)
    char(cv, "hedy_inventor", 156, 248, t, scale=2,
         arms="write" if t < t_c3_07 else ("cheer" if t >= t_no - 0.2 else "point"),
         look=1, mood="happy")
    char(cv, "hughes", 324, 248, t, scale=2,
         arms="cheer" if (t_c3_07 - 0.1 <= t < t_c3_08) else "down",
         look=-1, mood="happy", talk=talk_v(t, t_c3_07 <= t < t_c3_08 - 0.2))

    window(cv, 114, 44, 252, 78, fill=(14, 22, 42), border=GOLD if t >= t_c3_07 else LAMARR_CYAN, alpha=0.95)
    d = ImageDraw.Draw(cv)
    if t < t_c3_07 - 0.1:
        draw_text(cv, "DISEÑO PARA HOWARD HUGHES:", 240, 54, "silk", 8, GOLD, align="center")
        draw_text(cv, "PEZ MÁS VELOZ + PÁJARO MÁS VELOZ", 240, 72, "silk", 8, CREAM, align="center")
        if t >= t_ala - 0.3:
            draw_text(cv, "= UN ALA DE AVIÓN MÁS RÁPIDA", 240, 92, "press", 8, LAMARR_CYAN, align="center")
            d.arc([168, 102, 312, 118], 185, 355, fill=(*LAMARR_CYAN, 255), width=2)
    elif t < t_c3_08 - 0.1:
        draw_text(cv, "HOWARD HUGHES:", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "«ERES UN GENIO»", 240, 78, "press", 16 if False else 8, CHALK_GREEN, align="center")
        draw_text(cv, "EQUIPOS CIENTÍFICOS EN EL SET", 240, 98, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "LE PAGABAN POR QUEDARSE QUIETA.", 240, 58, "silk", 8, CREAM, align="center")
        if t >= t_no - 0.3:
            draw_text(cv, "ELLA NO SABÍA QUEDARSE QUIETA.", 240, 82, "press", 8, GOLD, align="center")
            draw_text(cv, "Y LA GUERRA ESTABA POR EMPEZAR", 240, 100, "silk", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.36)


SCENES = [
    (TL.s("c3_00") - 0.15, TL.s("c3_01"), make_card(3, ["LA MÁS LINDA", "DEL MUNDO"], "1937 – 1939 · LONDRES Y HOLLYWOOD")),
    (TL.s("c3_01") - 0.15, TL.s("c3_04"), c3_s01_ship_and_mayer),
    (TL.s("c3_04") - 0.15, TL.s("c3_06"), c3_s02_star_and_inventions),
    (TL.s("c3_06") - 0.15, TL.s("c4_00"), c3_s03_hughes_and_wings),
]


def scenes():
    return [(s[0], s[2], None, "ch03") for s in SCENES]


def music(A):
    t0 = TL.s("c3_00")
    t_inv = TL.s("c3_05")
    t_end = TL.s("c4_00")
    A.add_pad(t0, t_inv - t0, [130.81, 196.0, 261.63, 329.63], amp=0.040)
    A.add_pad(t_inv, t_end - t_inv, [146.83, 220.0, 293.66, 369.99], amp=0.042)


def sfx(A):
    A.fx_pop(TL.word("c3_01", "no"), 0.09)
    A.fx_sweep(TL.s("c3_02"), 0.5, 160, 360, 0.07)
    A.fx_chime(TL.word("c3_03", "cuatro"), 0.11)
    A.fx_sparkle(TL.word("c3_04", "éxito"), 0.09)
    A.fx_sparkle(TL.word("c3_05", "pastilla"), 0.09)
    A.fx_pop(TL.word("c3_06", "ala"), 0.09)
    A.fx_chime(TL.word("c3_07", "genio"), 0.11)
    A.fx_pop(TL.word("c3_08", "no"), 0.09)
