"""Capítulo 2: Treinta días (Tokio, Shoichiro Irimajiri de Sega, US$5 millones, RIVA 128 y el lema de los 30 días)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c2_card = make_card(2, ["TREINTA", "DÍAS"], "1996 - 1997 · TOKIO Y CALIFORNIA")


def c2_s01_tokyo_sega_meeting(t):
    """c2_01..c2_03: Huang vuela a Japón a ver a Shoichiro Irimajiri (Sega), le dice la verdad y pide US$5 millones."""
    t0 = TL.s("c2_01")
    t_c2_02 = TL.s("c2_02")
    t_c2_03 = TL.s("c2_03")

    cv = bg("tokyo_office_1996").copy()
    draw_place_only(cv, "TOKIO, JAPÓN · 1996 · OFICINA DE SEGA", t, t0, border=GOLD)

    draw_nvidia_prop(cv, 240, 248, kind="tokyo_tea_table", t=t, state=(1.0 if t >= t_c2_03 else 0.0))
    char(cv, "huang", 156, 248, t, scale=2,
         arms="offer" if t >= t_c2_02 else "down", look=1, mood="sad" if t < t_c2_03 else "happy",
         talk=talk_v(t, t0 <= t < t_c2_03 - 0.2))
    char(cv, "irimajiri", 324, 248, t, scale=2,
         arms="think" if t < t_c2_03 + 1.2 else "wave", look=-1, mood="neutral" if t < t_c2_03 + 1.2 else "happy",
         talk=talk_v(t, t >= t_c2_03 + 1.2))

    if t < t_c2_02 - 0.12:
        a, dy = pop(t, t0 + 0.1)
        window(cv, 104, 42 + dy, 272, 84, fill=(20, 18, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "SHOICHIRO IRIMAJIRI · SEGA", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "HUANG VOLÓ A JAPÓN A VERLO", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "Y LE DIJO LA VERDAD DE FRENTE", 240, 94 + dy, "silk", 8, TESLA_CYAN, align="center")
    elif t < t_c2_03 - 0.12:
        a, dy = pop(t, t_c2_02 - 0.1)
        window(cv, 98, 42 + dy, 284, 92, fill=(22, 18, 32), border=TESLA_CYAN, alpha=0.95)
        draw_text(cv, "EL PEDIDO IMPOSIBLE", 240, 50 + dy, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "1. «NUESTRO CHIP NO SIRVE: BUSQUEN OTRO»", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "2. QUE LOS US$ 5.000.000 QUEDEN EN NVIDIA", 240, 92 + dy, "silk", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c2_03 - 0.1)
        window(cv, 104, 42 + dy, 272, 88, fill=(18, 28, 24), border=GPU_GREEN, alpha=0.95)
        draw_text(cv, "DOS DÍAS DESPUÉS: ACEPTÓ", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
        draw_text(cv, "AUN SABIENDO QUE PODÍA PERDERLO TODO,", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "IRIMAJIRI SALVÓ A NVIDIA CON US$ 5M", 240, 94 + dy, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.34)


def c2_s02_riva128_motto_and_shares(t):
    """c2_04..c2_06: RIVA 128 (1 millón en 4 meses), el lema 'estamos a 30 días de quebrar' y las acciones de Sega."""
    t_c2_04 = TL.s("c2_04")
    t_c2_05 = TL.s("c2_05")
    t_c2_06 = TL.s("c2_06")

    if t < t_c2_06 - 0.12:
        cv = bg("california_chip_lab_1997").copy()
        draw_place_only(cv, "CALIFORNIA · 1997 · EL CHIP RIVA 128", t, t_c2_04, border=GPU_GREEN)
        draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=1.0)
        tear_p = clamp01((t - t_c2_05) / 1.2) if t >= t_c2_05 else 0.0
        draw_calendar_30(cv, 62, 68, t, scale=1, tear_p=tear_p, highlight_30=True)

        char(cv, "huang", 148, 248, t, scale=2,
             arms="cheer" if t < t_c2_05 else "point", look=1, mood="happy",
             talk=talk_v(t, t_c2_04 <= t < t_c2_06 - 0.2))
        char(cv, "cofounder_a", 332, 248, t, scale=2, arms="work", look=-1, mood="happy")

        if t < t_c2_05 - 0.12:
            a, dy = pop(t, t_c2_04 - 0.05)
            window(cv, 104, 42 + dy, 272, 92, fill=(16, 28, 22), border=GPU_GREEN, alpha=0.95)
            draw_text(cv, "RIVA 128 · HECHO CON TRIÁNGULOS", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
            draw_text(cv, "SEIS MESES DE VIDA PARA JUGARLO TODO", 240, 74 + dy, "silk", 8, CREAM, align="center")
            draw_text(cv, "1.000.000 DE UNIDADES EN 4 MESES", 240, 94 + dy, "silk", 8, GOLD, align="center")
        else:
            a, dy = pop(t, t_c2_05 - 0.05)
            window(cv, 98, 42 + dy, 284, 92, fill=(26, 16, 22), border=GOLD, alpha=0.96)
            draw_text(cv, "LA FRASE DE CADA REUNIÓN", 240, 52 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "«ESTAMOS A 30 DÍAS DE QUEBRAR»", 240, 74 + dy, "silk", 8, STOCK_RED, align="center")
            draw_text(cv, "RECUERDA ESA FRASE.", 240, 96 + dy, "silk", 8, CHALK_YELLOW, align="center")
        return vignette(cv, 0.34)

    # c2_06: En Tokio, Sega vende sus acciones al salir a la bolsa (hoy valdrían ~US$1 billón)
    cv = bg("tokyo_office_1996").copy()
    draw_place_only(cv, "TOKIO · LAS ACCIONES DE SEGA", t, t_c2_06, border=GOLD)
    draw_nvidia_prop(cv, 240, 248, kind="tokyo_tea_table", t=t, state=1.0)
    char(cv, "irimajiri", 240, 248, t, scale=2, arms="hold", look=1, mood="neutral")
    a, dy = pop(t, t_c2_06 - 0.05)
    window(cv, 98, 42 + dy, 284, 92, fill=(22, 18, 30), border=GOLD, alpha=0.96)
    draw_text(cv, "LAS ACCIONES DE SEGA", 240, 52 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "SEGA LAS VENDIÓ AL SALIR A LA BOLSA", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "SEGÚN HUANG, HOY VALDRÍAN ~US$ 1 BILLÓN", 240, 94 + dy, "silk", 8, GPU_GREEN, align="center")
    return vignette(cv, 0.36)


def scenes():
    return [
        (TL.s("c2_00") - 0.15, c2_card),
        (TL.s("c2_01"), c2_s01_tokyo_sega_meeting,
         lambda t: cam_push(t, TL.s("c2_01"), TL.s("c2_04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c2_04"), c2_s02_riva128_motto_and_shares,
         lambda t: cam_push(t, TL.s("c2_04"), TL.s("c3_00"), 1.0, 1.03, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("c2_00"), TL.e("c2_06") - TL.s("c2_00"), (196.0, 246.94, 293.66), amp=0.016)


def sfx(A):
    A.fx_pop(TL.s("c2_01") + 0.15, 0.05)
    A.fx_chime(TL.s("c2_03") + 0.4, 0.06)
    A.fx_sparkle(TL.s("c2_04") + 0.3, 0.06)
    A.fx_sweep(TL.s("c2_05") + 0.1, 0.35, 220, 440, 0.05)
    A.fx_chime(TL.s("c2_06") + 0.3, 0.06)
