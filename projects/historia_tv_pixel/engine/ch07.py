"""Capítulo 7: Doctor X (Patentes vencidas y el programa de televisión 'I've Got a Secret' de 1957)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import draw_tv_table_prop


def draw_quiz_desk_prop(cv, x, feet=248, t=0.0, label="DOCTOR X"):
    """Escritorio de estudio de televisión de 1957 apoyado en el suelo (feet=248) con micrófono y cartel."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 38
        shadow_ellipse(canvas, cx, fy, 46, 5, 85)
        d.rectangle([cx - 34, top_y, cx + 34, fy], fill=(38, 46, 68, 255), outline=(*GOLD, 255))
        d.rectangle([cx - 38, top_y - 4, cx + 38, top_y + 2], fill=(214, 184, 108, 255), outline=(*INK, 255))
        d.rectangle([cx - 28, top_y + 8, cx + 28, top_y + 24], fill=(18, 22, 36, 255), outline=(*GOLD, 255))
        draw_text(canvas, label, cx, top_y + 12, "press", 8, GOLD, align="center")
        # Micrófono cromado sobre el escritorio
        d.line([(cx, top_y - 12), (cx, top_y - 4)], fill=(210, 218, 230, 255), width=2)
        d.ellipse([cx - 4, top_y - 18, cx + 4, top_y - 10], fill=(228, 234, 244, 255), outline=(*INK, 255))
    floor_prop(cv, _draw, x, feet)


def c7_s01_expired_patents(t):
    """c7_01..c7_02: Sus primeras patentes vencieron y no le gustaba lo que se transmitía."""
    t0 = TL.s("c7_01")
    t_c7_02 = TL.s("c7_02")

    cv = bg("living_room_1950s").copy()
    cv = grade(cv, mul=(0.82, 0.84, 0.92))
    draw_place_only(cv, "AÑOS 1950 · EL INVENTOR OLVIDADO", t, t0, border=AMBER)

    window(cv, 118, 44, 244, 100, fill=(18, 20, 34), border=AMBER, alpha=0.95)
    if t < t_c7_02 - 0.1:
        draw_text(cv, "¿Y PHILO FARNSWORTH?", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "NUNCA SE HIZO RICO CON LA TELE", 240, 76, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "SUS PATENTES VENCIERON AL DESPEGAR", 240, 98, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "SEGÚN CONTÓ SU HIJO:", 240, 54, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "NO LE GUSTABA LO QUE TRANSMITÍAN", 240, 76, "press", 8, GOLD, align="center")
        draw_text(cv, "«NO QUERÍA QUE SUS HIJOS LA MIRARAN»", 240, 100, "silk", 8, CREAM, align="center")

    char(cv, "farnsworth_older", 156, 248, t, scale=2, arms="cross", look=1, mood="neutral")
    draw_tv_table_prop(cv, 292, 248, t, mode="scan")

    return vignette(cv, 0.36)


def c7_s02_doctor_x_quiz_show(t):
    """c7_03..c7_06: 1957, programa de juegos ('Doctor X'), nadie lo reconoce, gana US$ 80 y cigarrillos."""
    t0 = TL.s("c7_03")
    t_c7_04 = TL.s("c7_04")
    t_c7_05 = TL.s("c7_05")
    t_och = TL.word("c7_05", "ochenta")
    t_c7_06 = TL.s("c7_06")

    cv = bg("tv_game_show_1957").copy()
    # Efecto blanco y negro clásico de televisión de 1957 con toques dorados en los rótulos
    cv = grade(cv, sat=0.25, mul=(0.95, 0.98, 1.05))
    draw_place_only(cv, "NUEVA YORK · PROGRAMA DE TV (1957)", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 40, 244, 110, fill=(18, 22, 34), border=GOLD, alpha=0.95)
    if t < t_c7_04 - 0.1:
        draw_text(cv, "PROGRAMA DE JUEGOS · 1957", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "INVITADO: «DOCTOR X»", 240, 72, "press", 8, GOLD, align="center")
        draw_text(cv, "LOS FAMOSOS DEBÍAN ADIVINAR SU SECRETO", 240, 98, "silk", 8, CREAM, align="center")
    elif t < t_c7_05 - 0.1:
        # El público en su casa leyó el secreto sobreimpreso en pantalla
        draw_text(cv, "SOBREIMPRESO PARA EL PÚBLICO EN CASA:", 240, 50, "silk", 8, GOLD, align="center")
        d.rectangle([130, 68, 350, 116], fill=(12, 16, 24, 255), outline=(*CREAM, 255))
        draw_text(cv, "SECRETO DEL DOCTOR X:", 240, 76, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "«INVENTÓ LA TELEVISIÓN ELECTRÓNICA»", 240, 96, "press", 8, CREAM, align="center")
    elif t < t_c7_06 - 0.1:
        draw_text(cv, "LOS FAMOSOS NO ADIVINARON", 240, 50, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "CONDUCTOR: «SIN USTED NO TENDRÍA TRABAJO»", 240, 72, "silk", 8, CREAM, align="center")
        if t >= t_och - 0.25:
            d.rectangle([132, 92, 348, 134], fill=(24, 38, 28, 255), outline=(*GOLD, 255))
            draw_text(cv, "PREMIO: US$ 80", 240, 100, "press", 8, GOLD, align="center")
            draw_text(cv, "+ 1 CARTÓN DE CIGARRILLOS", 240, 118, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "EL INVENTOR DE LA TELEVISIÓN", 240, 56, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "SALIÓ EN TELEVISIÓN", 240, 78, "press", 8, GOLD, align="center")
        draw_text(cv, "Y NADIE LO RECONOCIÓ.", 240, 104, "press", 8, CHALK_RED, align="center")

    char(cv, "tv_host", 136, 248, t, scale=2,
         arms="offer" if t >= t_c7_05 else "point", look=1, mood="happy",
         talk=talk_v(t, t_c7_05 <= t < t_och))
    draw_quiz_desk_prop(cv, 236, 248, t, label="DOCTOR X")
    char(cv, "farnsworth_older", 236, 248, t, scale=2,
         arms="wave" if t >= t_och else "down", look=-1, mood="happy")
    char(cv, "panelist", 348, 248, t, scale=2,
         arms="shrug" if t >= t_c7_05 else "think", look=-1, mood="neutral")

    return vignette(cv, 0.36)


SCENES = [
    (TL.s("c7_00") - 0.15, TL.s("c7_01"), make_card(7, ["DOCTOR X"], "1957 · NUEVA YORK")),
    (TL.s("c7_01") - 0.15, TL.s("c7_03"), c7_s01_expired_patents),
    (TL.s("c7_03") - 0.15, TL.s("c8_00"), c7_s02_doctor_x_quiz_show),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c7_00"), TL.e("c7_06") - TL.s("c7_00"), (174.61, 220.0, 293.66), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c7_03"), 0.08)
    A.fx_sparkle(TL.s("c7_04"), 0.10)
    A.fx_chime(TL.word("c7_05", "ochenta"), 0.10)
    A.fx_thud(TL.s("c7_06"), 0.09)
