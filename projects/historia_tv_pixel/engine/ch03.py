"""Capítulo 3: Los surcos (Cabaña en EE. UU., arado en Idaho y el pizarrón del profesor Tolman, 1906-1922)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import draw_plow_prop


def draw_teacher_desk_prop(cv, x, feet=248, t=0.0, show_paper=False):
    """Escritorio del profesor Justin Tolman apoyado en el suelo (feet=248) con el papel del dibujo."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 40
        shadow_ellipse(canvas, cx, fy, 38, 5, 85)
        d.rectangle([cx - 28, top_y + 5, cx - 22, fy], fill=(78, 48, 28, 255), outline=(*INK, 255))
        d.rectangle([cx + 22, top_y + 5, cx + 28, fy], fill=(78, 48, 28, 255), outline=(*INK, 255))
        d.rectangle([cx - 32, top_y, cx + 32, top_y + 6], fill=(122, 78, 42, 255), outline=(*INK, 255))
        # Libros de química apilados sobre el escritorio
        d.rectangle([cx - 24, top_y - 10, cx - 8, top_y], fill=(156, 52, 48, 255), outline=(*INK, 255))
        d.rectangle([cx - 22, top_y - 16, cx - 10, top_y - 10], fill=(52, 96, 142, 255), outline=(*INK, 255))
        if show_paper:
            glow(canvas, cx + 10, top_y - 8, 16, GOLD, 0.5)
            d.rectangle([cx + 2, top_y - 14, cx + 20, top_y - 1], fill=(246, 240, 222, 255), outline=(*INK, 255))
            d.line([(cx + 5, top_y - 10), (cx + 17, top_y - 10)], fill=(42, 92, 138, 255))
            d.line([(cx + 5, top_y - 6), (cx + 17, top_y - 6)], fill=(42, 92, 138, 255))
    floor_prop(cv, _draw, x, feet)


def c3_s01_cabin_and_furrows(t):
    """c3_01..c3_03: Cabaña de troncos sin luz eléctrica -> 14 años arando en Idaho (haz de electrones)."""
    t0 = TL.s("c3_01")
    t_seis = TL.word("c3_01", "seis")
    t_c3_02 = TL.s("c3_02")
    t_elec = TL.word("c3_02", "electrones")
    t_c3_03 = TL.s("c3_03")

    cv = bg("idaho_plow_field").copy()
    draw_place_only(cv, "UTAH E IDAHO · 1906 – 1920", t, t0, border=AMBER)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 44, 244, 102, fill=(18, 22, 34), border=GOLD, alpha=0.94)
    if t < t_c3_02 - 0.1:
        draw_text(cv, "PHILO FARNSWORTH (1906)", 240, 52, "press", 8, GOLD, align="center")
        # Cabaña de troncos en el panel central
        d.rectangle([212, 76, 268, 112], fill=(104, 64, 36, 255), outline=(*INK, 255))
        d.polygon([(204, 76), (240, 58), (276, 76)], fill=(72, 42, 24, 255), outline=(*INK, 255))
        d.rectangle([234, 92, 246, 112], fill=(58, 34, 20, 255))
        lbl_c = "6 AÑOS: «VOY A SER INVENTOR»" if t >= t_seis - 0.2 else "CABAÑA DE TRONCOS · SIN LUZ ELÉCTRICA"
        draw_text(cv, lbl_c, 240, 124, "silk", 8, CHALK_GREEN if t >= t_seis - 0.2 else CREAM, align="center")
        char(cv, "farnsworth_boy", 204, 248, t, scale=2,
             arms="cheer" if t >= t_seis - 0.2 else "think", look=1, mood="happy")
    else:
        # 14 años: arando con caballos -> haz de electrones barriendo renglón por renglón
        draw_text(cv, "14 AÑOS · CAMPO ARADO EN IDAHO", 240, 52, "silk", 8, AMBER, align="center")
        draw_scanline_beam(cv, 138, 66, 204, 52, t, rows=7, speed=1.6, color=CHALK_GREEN, beam_col=TESLA_CYAN)
        if t < t_c3_03 - 0.1:
            lbl_b = "HAZ DE ELECTRONES: RENGLÓN POR RENGLÓN" if t >= t_elec - 0.2 else "MIRÓ LOS SURCOS HACIA ATRÁS"
            draw_text(cv, lbl_b, 240, 126, "silk", 8, CHALK_GREEN if t >= t_elec - 0.2 else CREAM, align="center")
        else:
            draw_text(cv, "SIN DISCOS · SOLO ELECTRICIDAD", 240, 126, "press", 8, TESLA_CYAN, align="center")

        char(cv, "farnsworth_boy", 172, 248, t, scale=2, arms="point", look=1, mood="happy")
        draw_plow_prop(cv, 286, 248, t)

    return vignette(cv, 0.35)


def c3_s02_tolman_chalkboard(t):
    """c3_04..c3_05: Aula de química (1922), pizarrón con el esquema de TV y el papel guardado por Tolman."""
    t0 = TL.s("c3_04")
    t_papel = TL.word("c3_04", "papel")
    t_rec = TL.word("c3_04", "Recuerda")
    t_c3_05 = TL.s("c3_05")

    cv = bg("school_chalkboard_1922").copy()
    draw_place_only(cv, "ESCUELA SECUNDARIA · IDAHO (1922)", t, t0, border=CHALK_YELLOW)
    d = ImageDraw.Draw(cv)

    # El pizarrón de la clase donde Farnsworth (15 años) dibuja la cámara electrónica
    window(cv, 118, 42, 244, 108, fill=BOARD_GREEN, border=WOOD_FRAME, alpha=0.96, inner=(42, 82, 58))
    draw_text(cv, "EL DIBUJO EN EL PIZARRÓN (15 AÑOS)", 240, 50, "silk", 8, CHALK_YELLOW, align="center")

    # Diagrama de tubo disector de imagen en tiza blanca y verde
    d.ellipse([142, 70, 186, 112], outline=(*CHALK_WHITE, 255), width=2)
    d.rectangle([186, 82, 254, 100], outline=(*CHALK_WHITE, 255), width=2)
    draw_scanline_beam(cv, 266, 70, 78, 42, t, rows=5, speed=1.5, color=CHALK_GREEN)
    d.line([(186, 91), (266, 91)], fill=(*CHALK_CYAN, 255), width=2)

    if t < t_papel - 0.15:
        draw_text(cv, "PROFESOR JUSTIN TOLMAN", 240, 126, "silk", 8, CREAM, align="center")
    elif t < t_c3_05 - 0.1:
        # Tolman copia el dibujo en un papel y lo guarda ("Recuerda ese papel")
        d.rectangle([136, 118, 344, 142], fill=(22, 46, 34, 255), outline=(*GOLD, 255))
        lbl_p = "¡RECUERDA ESE PAPEL!" if t >= t_rec - 0.2 else "TOLMAN COPIÓ EL DIBUJO EN UN PAPEL"
        draw_text(cv, lbl_p, 240, 126, "press" if t >= t_rec - 0.2 else "silk", 8,
                  GOLD if t >= t_rec - 0.2 else CREAM, align="center")
    else:
        draw_text(cv, "15 AÑOS · DIBUJÓ LA TELEVISIÓN", 240, 126, "press", 8, CHALK_YELLOW, align="center")

    char(cv, "farnsworth_boy", 148, 248, t, scale=2,
         arms="write" if t < t_papel else "point", look=1, mood="happy",
         talk=talk_v(t, t < t_papel - 0.4))
    draw_teacher_desk_prop(cv, 244, 248, t, show_paper=(t >= t_papel - 0.2))
    char(cv, "tolman", 336, 248, t, scale=2,
         arms="note" if (t_papel - 0.3 <= t < t_c3_05) else "point_l",
         look=-1, mood="happy",
         talk=talk_v(t, t_papel - 0.4 <= t < t_rec))

    return vignette(cv, 0.34)


SCENES = [
    (TL.s("c3_00") - 0.15, TL.s("c3_01"), make_card(3, ["LOS", "SURCOS"], "1906 – 1922 · IDAHO")),
    (TL.s("c3_01") - 0.15, TL.s("c3_04"), c3_s01_cabin_and_furrows),
    (TL.s("c3_04") - 0.15, TL.s("c4_00"), c3_s02_tolman_chalkboard),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c3_00"), TL.e("c3_05") - TL.s("c3_00"), (174.61, 220.0, 261.63), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c3_02"), 0.08)
    A.fx_chime(TL.s("c3_03"), 0.09)
    A.fx_sparkle(TL.word("c3_04", "papel"), 0.10)
    A.fx_chime(TL.s("c3_05"), 0.11)
