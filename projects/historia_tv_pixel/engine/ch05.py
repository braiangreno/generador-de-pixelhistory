"""Capítulo 5: Goliat (RCA, David Sarnoff, Vladimir Zworykin y el juicio de patentes con el dibujo de 1922)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch04 import draw_sf_lab_bench_prop


def draw_court_podium_prop(cv, x, feet=248, t=0.0, show_paper=True):
    """Estrado judicial apoyado en el suelo (feet=248) donde el profesor Tolman exhibe el dibujo de 1922."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 44
        shadow_ellipse(canvas, cx, fy, 40, 5, 85)
        d.rectangle([cx - 24, top_y, cx + 24, fy], fill=(82, 48, 32, 255), outline=(*INK, 255))
        d.rectangle([cx - 28, top_y - 4, cx + 28, top_y + 3], fill=(124, 76, 44, 255), outline=(*GOLD, 255))
        if show_paper:
            glow(canvas, cx, top_y - 14, 20, GOLD, 0.55)
            d.rectangle([cx - 12, top_y - 24, cx + 12, top_y - 4], fill=(248, 242, 224, 255), outline=(*INK, 255))
            d.line([(cx - 8, top_y - 18), (cx + 8, top_y - 18)], fill=(38, 88, 134, 255))
            d.line([(cx - 8, top_y - 12), (cx + 8, top_y - 12)], fill=(38, 88, 134, 255))
    floor_prop(cv, _draw, x, feet)


def c5_s01_rca_and_zworykin(t):
    """c5_01..c5_03: RCA (David Sarnoff), visita de Vladimir Zworykin al laboratorio y rechazo de US$ 100.000."""
    t0 = TL.s("c5_01")
    t_c5_02 = TL.s("c5_02")
    t_gust = TL.word("c5_02", "gustado")
    t_c5_03 = TL.s("c5_03")
    t_no = TL.word("c5_03", "no")

    cv = bg("rca_skyscraper_court").copy() if t < t_c5_02 - 0.1 else bg("sf_lab_1927").copy()
    draw_place_only(cv, "RCA · NUEVA YORK Y SAN FRANCISCO (1930)", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 44, 244, 102, fill=(16, 20, 36), border=GOLD, alpha=0.95)
    if t < t_c5_02 - 0.1:
        draw_text(cv, "EL GIGANTE DE LA RADIO: RCA", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "DIRECTOR: DAVID SARNOFF", 240, 78, "silk", 8, CREAM, align="center")
        draw_text(cv, "QUERÍA LA TELEVISIÓN PARA ÉL", 240, 102, "silk", 8, CHALK_RED, align="center")
        char(cv, "sarnoff", 240, 248, t, scale=2, arms="cross", look=1, mood="neutral")
    elif t < t_c5_03 - 0.1:
        draw_text(cv, "VISITA DE VLADIMIR ZWORYKIN", 240, 52, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "INGENIERO JEFE DE RCA", 240, 72, "silk", 8, CREAM, align="center")
        if t >= t_gust - 0.3:
            d.rectangle([130, 92, 350, 132], fill=(24, 34, 52, 255), outline=(*GOLD, 255))
            draw_text(cv, "«ME HABRÍA GUSTADO", 240, 98, "silk", 8, GOLD, align="center")
            draw_text(cv, "INVENTARLO A MÍ»", 240, 114, "silk", 8, GOLD, align="center")
        char(cv, "farnsworth_young", 148, 248, t, scale=2, arms="offer", look=1, mood="happy")
        draw_sf_lab_bench_prop(cv, 244, 248, t, mode="scan")
        char(cv, "zworykin", 338, 248, t, scale=2, arms="think", look=-1, mood="happy")
    else:
        draw_text(cv, "OFERTA DE COMPRA DE RCA:", 240, 54, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$ 100.000 POR TODO", 240, 74, "press", 8, GOLD, align="center")
        if t >= t_no - 0.25:
            d.rectangle([152, 98, 328, 128], fill=(68, 22, 26, 255), outline=(*CHALK_RED, 255))
            draw_text(cv, "FARNSWORTH DIJO: ¡NO!", 240, 109, "press", 8, CHALK_RED, align="center")
        char(cv, "sarnoff", 156, 248, t, scale=2, arms="offer", look=1, mood="neutral")
        draw_sf_lab_bench_prop(cv, 244, 248, t, mode="dollar")
        char(cv, "farnsworth_young", 332, 248, t, scale=2, arms="cross", look=-1, mood="neutral")

    return vignette(cv, 0.35)


def c5_s02_patent_trial_victory(t):
    """c5_04..c5_07: Pleito de patentes, el profesor Tolman muestra el papel de 1922 y RCA paga US$ 1.000.000."""
    t0 = TL.s("c5_04")
    t_c5_05 = TL.s("c5_05")
    t_c5_06 = TL.s("c5_06")
    t_mill = TL.word("c5_06", "millón")
    t_c5_07 = TL.s("c5_07")

    cv = bg("rca_skyscraper_court").copy()
    draw_place_only(cv, "OFICINA DE PATENTES · 1934 – 1939", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 42, 244, 108, fill=(18, 22, 38), border=GOLD, alpha=0.95)
    if t < t_c5_05 - 0.1:
        draw_text(cv, "PLEITO DE PATENTES: RCA VS. FARNSWORTH", 240, 54, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "RCA: «LA IDEA ERA DE ZWORYKIN»", 240, 82, "silk", 8, CREAM, align="center")
        draw_text(cv, "BATALLA JUDICIAL EN WASHINGTON", 240, 110, "silk", 8, GOLD, align="center")
    elif t < t_c5_06 - 0.1:
        draw_text(cv, "¿TE ACUERDAS DEL PAPEL?", 240, 52, "press", 8, GOLD, align="center")
        # El dibujo de 1922 guardado por el profesor Tolman
        d.rectangle([146, 70, 334, 116], fill=(24, 42, 34, 255), outline=(*GOLD, 255))
        draw_text(cv, "BOCETO DE CLASE · AÑO 1922", 240, 78, "silk", 8, CREAM, align="center")
        draw_text(cv, "TESTIGO: PROFESOR TOLMAN", 240, 96, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "PRUEBA DECISIVA EN EL JUICIO", 240, 126, "silk", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "FALLO DE PATENTES (1934):", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "¡GANA FARNSWORTH!", 240, 68, "press", 8, CHALK_GREEN, align="center")
        if t >= t_mill - 0.35:
            d.rectangle([134, 88, 346, 118], fill=(22, 48, 34, 255), outline=(*GOLD, 255))
            draw_text(cv, "1939: RCA PAGA US$ 1.000.000", 240, 99, "press", 8, GOLD, align="center")
        if t >= t_c5_07 - 0.1:
            draw_text(cv, "CON UN DIBUJO DE PIZARRÓN", 240, 128, "silk", 8, CREAM, align="center")

    char(cv, "farnsworth_young", 142, 248, t, scale=2,
         arms="cheer" if t >= t_c5_06 else "down", look=1, mood="happy" if t >= t_c5_05 else "neutral")
    draw_court_podium_prop(cv, 240, 248, t, show_paper=(t >= t_c5_05 - 0.15))
    if t < t_c5_06:
        char(cv, "tolman", 336, 248, t, scale=2, arms="offer", look=-1, mood="happy",
             talk=talk_v(t, t_c5_05 <= t < t_c5_06))
    else:
        char(cv, "sarnoff", 336, 248, t, scale=2, arms="down", look=-1, mood="sad")

    return vignette(cv, 0.35)


SCENES = [
    (TL.s("c5_00") - 0.15, TL.s("c5_01"), make_card(5, ["GOLIAT"], "1930 – 1939 · EE. UU.")),
    (TL.s("c5_01") - 0.15, TL.s("c5_04"), c5_s01_rca_and_zworykin),
    (TL.s("c5_04") - 0.15, TL.s("c6_00"), c5_s02_patent_trial_victory),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    return


def sfx(A):
    A.fx_pop(TL.s("c5_01"), 0.08)
    A.fx_thud(TL.word("c5_03", "no"), 0.10)
    A.fx_sparkle(TL.s("c5_05"), 0.10)
    A.fx_chime(TL.s("c5_06"), 0.12)
