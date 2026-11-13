"""Capítulo 4: El signo de dólar (San Francisco 1927, La Pizarra 2: Electrones, la primera raya y Pem)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_sf_lab_bench_prop(cv, x, feet=248, t=0.0, mode="line"):
    """Mesa de laboratorio de San Francisco apoyada en el suelo (feet=248) con cámara y tubo receptor."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 46, 5, 85)
        d.rectangle([cx - 34, top_y + 5, cx - 28, fy], fill=(64, 42, 28, 255), outline=(*INK, 255))
        d.rectangle([cx + 28, top_y + 5, cx + 34, fy], fill=(64, 42, 28, 255), outline=(*INK, 255))
        d.rectangle([cx - 38, top_y, cx + 38, top_y + 6], fill=(108, 72, 42, 255), outline=(*INK, 255))
        # Tubo de cámara a la izquierda sobre la mesa
        d.rectangle([cx - 28, top_y - 18, cx - 8, top_y], fill=(58, 68, 82, 255), outline=(*INK, 255))
        d.ellipse([cx - 32, top_y - 16, cx - 24, top_y - 4], fill=(138, 214, 236, 255), outline=(*INK, 255))
        # Televisor / tubo receptor a la derecha sobre la mesa
        draw_crt_tv(canvas, cx + 2, top_y - 32, 34, 32, t, mode=mode)
    floor_prop(cv, _draw, x, feet)


def c4_s01_sf_lab_investors(t):
    """c4_01: 20 años, inversores ($25.000) y laboratorio en San Francisco junto a Pem."""
    t0 = TL.s("c4_01")
    t_pem = TL.word("c4_01", "Pem")

    cv = bg("sf_lab_1927").copy()
    draw_place_only(cv, "SAN FRANCISCO · 1926 – 1927", t, t0, border=TESLA_CYAN)

    window(cv, 118, 46, 244, 92, fill=(14, 24, 38), border=GOLD, alpha=0.94)
    draw_text(cv, "LABORATORIO EN SAN FRANCISCO", 240, 56, "silk", 8, TESLA_CYAN, align="center")
    draw_text(cv, "INVERSIÓN: US$ 25.000", 240, 76, "press", 8, GOLD, align="center")
    lbl_p = "SU ESPOSA PEM TRABAJABA CON ÉL" if t >= t_pem - 0.2 else "PHILO FARNSWORTH · 20 AÑOS"
    draw_text(cv, lbl_p, 240, 102, "silk", 8, CHALK_GREEN if t >= t_pem - 0.2 else CREAM, align="center")

    char(cv, "farnsworth_young", 152, 248, t, scale=2, arms="work", look=1, mood="happy")
    draw_sf_lab_bench_prop(cv, 244, 248, t, mode="scan")
    char(cv, "pem", 336, 248, t, scale=2, arms="note" if t >= t_pem - 0.2 else "work", look=-1, mood="happy")

    return vignette(cv, 0.35)


def c4_s02_pizarra_electrons(t):
    """c4_02..c4_03: LA PIZARRA 2 — Cámara convierte luz en electrones; imán los mueve en renglones."""
    t0 = TL.s("c4_02")
    t_c4_03 = TL.s("c4_03")
    t_nada = TL.word("c4_03", "Nada")

    cv = draw_pizarra_frame(t, t0, "HAZ DE ELECTRONES",
                            summary_es="NADA GIRA: TODO ES ELECTRICIDAD",
                            t_summary=t_nada)
    d = ImageDraw.Draw(cv)

    if t < t_c4_03 - 0.1:
        # Paso 1: Cámara convierte luz en electrones y un imán los mueve en renglones
        d.rectangle([124, 46, 356, 186], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "1. CÁMARA: LUZ -> ELECTRONES", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        # Lente izquierda -> chorro de electrones -> imán en herradura
        d.ellipse([138, 82, 162, 126], fill=(42, 92, 68, 255), outline=(*CHALK_CYAN, 255))
        draw_text(cv, "LUZ", 150, 132, "silk", 8, CHALK_YELLOW, align="center")
        # Imán deflectando electrones en renglones
        d.rectangle([204, 72, 244, 82], fill=(196, 62, 58, 255), outline=(*CHALK_WHITE, 255))
        d.rectangle([204, 126, 244, 136], fill=(58, 118, 196, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "IMÁN", 224, 142, "silk", 8, CHALK_WHITE, align="center")
        draw_scanline_beam(cv, 258, 76, 84, 56, t, rows=6, speed=1.6, color=CHALK_CYAN)
        draw_text(cv, "IZQUIERDA A DERECHA · ARRIBA ABAJO", 240, 164, "silk", 8, CREAM, align="center")
        draw_chalk_hand(cv, 224, 104, t)
    else:
        # Paso 2: En la pantalla, otro haz de electrones pinta sobre un vidrio que brilla
        d.rectangle([124, 46, 356, 192], fill=(16, 40, 28, 255), outline=(*CHALK_WHITE, 255))
        draw_text(cv, "2. PANTALLA: VIDRIO QUE BRILLA", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        # Cañón de electrones a la izquierda pintando sobre la pantalla de fósforo a la derecha
        d.rectangle([138, 96, 178, 116], fill=(42, 74, 58, 255), outline=(*CHALK_WHITE, 255))
        bx_tip = 216 + int(round(((t * 1.6 * 6) % 1.0) * 112))
        by_tip = 76 + int(((t * 1.6) % 1.0) * 6) * 9
        d.line([(178, 106), (bx_tip, by_tip)], fill=(*CHALK_CYAN, 255), width=2)
        draw_scanline_beam(cv, 212, 72, 126, 64, t, rows=6, speed=1.6, color=CHALK_GREEN)
        draw_text(cv, "HAZ PINTA SOBRE EL VIDRIO", 240, 148, "silk", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.28)


def c4_s03_first_line_and_dollar(t):
    """c4_04..c4_08: 7 de septiembre de 1927 (una raya), telegrama, el signo de dólar y la cara de Pem."""
    t0 = TL.s("c4_04")
    t_c4_05 = TL.s("c4_05")
    t_tele = TL.word("c4_05", "telegrama")
    t_c4_06 = TL.s("c4_06")
    t_dolar = TL.word("c4_06", "dólar")
    t_c4_07 = TL.s("c4_07")
    t_c4_08 = TL.s("c4_08")

    cv = bg("sf_lab_1927").copy()
    draw_place_only(cv, "7 DE SEPTIEMBRE DE 1927 · SAN FRANCISCO", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 42, 244, 108, fill=(14, 24, 34), border=CHALK_GREEN, alpha=0.95)
    tv_mode = "line"
    if t < t_c4_06 - 0.1:
        draw_text(cv, "7 DE SEPTIEMBRE DE 1927", 240, 50, "press", 8, GOLD, align="center")
        # Tubo mostrando la primera raya luminosa
        d.rectangle([188, 66, 292, 114], fill=(10, 28, 20, 255), outline=(*CHALK_GREEN, 255))
        glow(cv, 240, 90, 32, CHALK_GREEN, 0.55)
        d.line([(198, 90), (282, 90)], fill=(210, 255, 225, 255), width=3)
        if t >= t_tele - 0.2:
            d.rectangle([132, 120, 348, 142], fill=(24, 38, 28, 255), outline=(*GOLD, 255))
            draw_text(cv, "TELEGRAMA: «¡LA MALDITA COSA FUNCIONA!»", 240, 127, "silk", 8, GOLD, align="center")
        else:
            draw_text(cv, "UNA SOLA RAYA QUE BRILLABA", 240, 124, "silk", 8, CHALK_GREEN, align="center")
    elif t < t_c4_07 - 0.1:
        tv_mode = "dollar" if t >= t_dolar - 0.35 else "scan"
        draw_text(cv, "¿CUÁNDO VEREMOS ALGO DE DINERO?", 240, 50, "silk", 8, CREAM, align="center")
        d.rectangle([194, 66, 286, 118], fill=(10, 30, 20, 255), outline=(*GOLD, 255))
        if t >= t_dolar - 0.35:
            glow(cv, 240, 92, 28, CHALK_GREEN, 0.65)
            draw_text(cv, "$", 240, 78, "press", 24, CHALK_GREEN, align="center")
        draw_text(cv, "APARECIÓ UN SIGNO DE DÓLAR", 240, 128, "press", 8, GOLD, align="center")
    else:
        tv_mode = "pem" if t < t_c4_08 else "dollar"
        draw_text(cv, "PRIMERA CARA HUMANA: PEM", 240, 50, "press", 8, CHALK_GREEN, align="center")
        draw_crt_tv(cv, 204, 66, 72, 52, t, mode="pem")
        lbl_end = "ANTES DE UNA CARA, MOSTRÓ DINERO ($)" if t >= t_c4_08 - 0.1 else "PEM FARNSWORTH EN PANTALLA"
        draw_text(cv, lbl_end, 240, 128, "silk", 8, GOLD if t >= t_c4_08 - 0.1 else CREAM, align="center")

    char(cv, "farnsworth_young", 146, 248, t, scale=2,
         arms="cheer" if (t_c4_05 <= t < t_c4_06) else "point", look=1, mood="happy")
    draw_sf_lab_bench_prop(cv, 244, 248, t, mode=tv_mode)
    char(cv, "pem", 338, 248, t, scale=2, arms="wave" if t >= t_c4_07 else "work", look=-1, mood="happy")

    return vignette(cv, 0.35)


SCENES = [
    (TL.s("c4_00") - 0.15, TL.s("c4_01"), make_card(4, ["EL SIGNO DE", "DÓLAR"], "1927 · SAN FRANCISCO")),
    (TL.s("c4_01") - 0.15, TL.s("c4_02"), c4_s01_sf_lab_investors),
    (TL.s("c4_02") - 0.15, TL.s("c4_04"), c4_s02_pizarra_electrons),
    (TL.s("c4_04") - 0.15, TL.s("c5_00"), c4_s03_first_line_and_dollar),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c4_00"), TL.e("c4_08") - TL.s("c4_00"), (164.81, 207.65, 246.94), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c4_01"), 0.08)
    A.fx_chime(TL.s("c4_05"), 0.11)
    A.fx_sparkle(TL.word("c4_06", "dólar"), 0.12)
    A.fx_pop(TL.s("c4_07"), 0.09)
