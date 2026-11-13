"""Capítulo 7: El cajón (c7_00..c7_06) — Vencimiento en 1959, electrónica sin rollos, Crisis de Cuba 1962 y auge inalámbrico."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c7_s01_electronic_and_cuba(t):
    """c7_01..c7_03: La patente vence en 1959 (muere Antheil) -> Ingenieros la vuelven electrónica -> Crisis de Cuba 1962."""
    t0 = TL.s("c7_01")
    t_c7_02 = TL.s("c7_02")
    t_elec = TL.word("c7_02", "electrónica")
    t_c7_03 = TL.s("c7_03")
    t_cuba = TL.word("c7_03", "Cuba")

    if t < t_c7_03 - 0.15:
        cv = bg("navy_office_1942").copy()
        draw_place_only(cv, "1959 · FIN DE LA PATENTE", t, t0, border=LAMARR_CYAN)

        draw_table_with_prop(cv, 240, 248, prop_kind="radio" if t >= t_c7_02 else "drawer",
                             t=t, open_p=0.9)
        if t < t_c7_02 - 0.1:
            char(cv, "navy_officer", 156, 248, t, scale=2, arms="down", look=1, mood="neutral")
            window(cv, 114, 46, 252, 70, fill=(18, 22, 38), border=SOFT_GRAY, alpha=0.95)
            draw_text(cv, "1959 · LA PATENTE VENCIÓ", 240, 56, "press", 8, GOLD, align="center")
            draw_text(cv, "ESE MISMO AÑO MURIÓ ANTHEIL", 240, 76, "silk", 8, CREAM, align="center")
            draw_text(cv, "SIN VER SU IDEA EN ACCIÓN", 240, 94, "silk", 8, SOFT_GRAY, align="center")
        else:
            char(cv, "engineer", 156, 248, t, scale=2, arms="work", look=1, mood="happy")
            char(cv, "navy_officer", 324, 248, t, scale=2, arms="point_l", look=-1, mood="happy")
            window(cv, 114, 46, 252, 72, fill=(14, 24, 42), border=LAMARR_CYAN, alpha=0.95)
            draw_text(cv, "RESCATADA DEL CAJÓN:", 240, 56, "silk", 8, GOLD, align="center")
            draw_text(cv, "¡AHORA ERA 100% ELECTRÓNICA!", 240, 74, "press", 8,
                      LAMARR_CYAN if t >= t_elec - 0.2 else CREAM, align="center")
            draw_text(cv, "TRANSISTORES EN LUGAR DE PAPEL", 240, 94, "silk", 8, CHALK_GREEN, align="center")
        return vignette(cv, 0.36)

    # c7_03: 1962 Crisis de los misiles en Cuba — los barcos de EE. UU. ya usaban el sistema
    cv = bg("atlantic_night_1940").copy()
    draw_place_only(cv, "1962 · CRISIS DE LOS MISILES EN CUBA", t, t_c7_03, border=LAMARR_CYAN)

    draw_table_with_prop(cv, 240, 248, prop_kind="radio", t=t)
    char(cv, "navy_officer", 152, 248, t, scale=2, arms="point", look=1, mood="neutral")
    char(cv, "engineer", 328, 248, t, scale=2, arms="type", look=-1, mood="neutral")

    window(cv, 114, 44, 252, 92, fill=(12, 22, 42), border=LAMARR_CYAN, alpha=0.95)
    draw_text(cv, "OCTUBRE DE 1962 · BLOQUEO DE CUBA", 240, 52, "silk", 8, GOLD, align="center")
    draw_text(cv, "LOS BARCOS DE EE. UU. YA USABAN", 240, 68, "silk", 8, CREAM, align="center")
    draw_text(cv, "COMUNICACIONES POR SALTO DE CANAL", 240, 84, "press", 8, LAMARR_CYAN, align="center")
    draw_freq_lanes(cv, 126, 98, 228, 32, t, n_lanes=3, speed=4.8, hopping=True, show_labels=False)
    return vignette(cv, 0.36)


def c7_s02_isolated_and_world_grows(t):
    """c7_04..c7_06: Hedy no cobró nada y vivió aislada -> Años 80 y 90: pieza clave inalámbrica -> El mundo olvidó su nombre."""
    t_c7_04 = TL.s("c7_04")
    t_ais = TL.word("c7_04", "aislada")
    t_c7_05 = TL.s("c7_05")
    t_inal = TL.word("c7_05", "inalámbricas")
    t_c7_06 = TL.s("c7_06")
    t_olv = TL.word("c7_06", "olvidó")

    cv = bg("florida_living_1970").copy()
    draw_place_only(cv, "AÑOS 1970 – 1990 · FLORIDA, EE. UU.", t, t_c7_04, border=GOLD)

    draw_table_with_prop(cv, 292, 248, prop_kind="radio" if t >= t_c7_05 else "patent", t=t)
    char(cv, "hedy_older", 176, 248, t, scale=2,
         arms="think" if t >= t_c7_05 else "down",
         look=1, mood="sad" if t < t_c7_05 else "neutral")

    # En c7_05 y c7_06, ondas cian/magenta cruzan el cielo de la ventana mostrando cómo su idea llena el mundo
    if t >= t_c7_05 - 0.15:
        draw_freq_lanes(cv, 194, 42, 236, 56, t, n_lanes=3, speed=5.2, hopping=True, show_labels=False)

    window(cv, 114, 46, 252, 74, fill=(18, 20, 38), border=LAMARR_CYAN if t >= t_c7_05 else GOLD, alpha=0.95)
    if t < t_c7_05 - 0.1:
        draw_text(cv, "HEDY NO COBRÓ NI UN DÓLAR:", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "LA PATENTE HABÍA VENCIDO EN 1959", 240, 74, "silk", 8, CREAM, align="center")
        if t >= t_ais - 0.4:
            draw_text(cv, "VIVIÓ SUS ÚLTIMOS AÑOS AISLADA", 240, 94, "press", 8, SOFT_GRAY, align="center")
    elif t < t_c7_06 - 0.1:
        draw_text(cv, "AÑOS 80 Y 90 · REVOLUCIÓN MÓVIL:", 240, 56, "silk", 8, GOLD, align="center")
        draw_text(cv, "SALTAR DE FRECUENCIA SE VOLVIÓ", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "CLAVE EN REDES INALÁMBRICAS", 240, 94, "press", 8, LAMARR_CYAN, align="center")
    else:
        draw_text(cv, "EL MUNDO SE LLENÓ DE SU IDEA.", 240, 58, "press", 8, LAMARR_CYAN, align="center")
        if t >= t_olv - 0.35:
            draw_text(cv, "Y SE OLVIDÓ DE SU NOMBRE.", 240, 82, "press", 8, GOLD, align="center")
            draw_text(cv, "HASTA QUE ALGUIEN VOLVIÓ A MIRAR", 240, 100, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.36)


SCENES = [
    (TL.s("c7_00") - 0.15, TL.s("c7_01"), make_card(7, ["EL CAJÓN"], "1959 – 1990 · DE CUBA AL MUNDO")),
    (TL.s("c7_01") - 0.15, TL.s("c7_04"), c7_s01_electronic_and_cuba),
    (TL.s("c7_04") - 0.15, TL.s("c8_00"), c7_s02_isolated_and_world_grows),
]


def scenes():
    return [(s[0], s[2], None, "ch07") for s in SCENES]


def music(A):
    t0 = TL.s("c7_00")
    t_grow = TL.s("c7_05")
    t_end = TL.s("c8_00")
    A.add_pad(t0, t_grow - t0, [110.0, 146.83, 220.0], amp=0.038)
    A.add_pad(t_grow, t_end - t_grow, [110.0, 164.81, 220.0, 329.63], amp=0.044)


def sfx(A):
    A.fx_thud(TL.s("c7_01"), 0.09)
    A.fx_pop(TL.s("c7_02"), 0.09)
    A.fx_sparkle(TL.word("c7_03", "Cuba"), 0.10)
    A.fx_pop(TL.word("c7_04", "aislada"), 0.08)
    A.fx_sweep(TL.s("c7_05"), 0.5, 180, 420, 0.08)
    A.fx_chime(TL.s("c7_06"), 0.11)
