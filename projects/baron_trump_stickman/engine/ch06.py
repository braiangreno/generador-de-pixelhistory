"""Capítulo 6: Viajar al futuro — LA PIZARRA 2 (Dilatación del tiempo, Einstein, Gemelos Kelly, GPS)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch6 = make_card(6, ["VIAJAR AL FUTURO"], "LA ESTACIÓN ESPACIAL Y LA PIZARRA")


def scene_ch6(t):
    t_01 = TL.start("c6_01")
    t_02 = TL.start("c6_02")
    t_03 = TL.start("c6_03")
    t_04 = TL.start("c6_04")
    t_05 = TL.start("c6_05")
    t_06 = TL.start("c6_06")
    t_07 = TL.start("c6_07")

    if t < t_02:
        # c6_01: Estación espacial girando sobre la Tierra
        cv = bg("space_station")
        draw_chapter_header(cv, "CAP. 6 · VIAJAR AL FUTURO", "LA PREGUNTA DE FONDO", t, t_01, border=CYAN)
        window(cv, 76, 48, 328, 72, fill=(10, 18, 36), border=CYAN, alpha=0.94)
        draw_text(cv, "¿SE PUEDE VIAJAR EN EL TIEMPO?", 240, 58, "press", 8, CYAN, align="center")
        draw_text(cv, "AL FUTURO, SÍ. UN POQUITO.", 240, 82, "press", 8, GOLD, align="center")
        return vignette(cv, 0.34)

    # c6_02..c6_07: LA PIZARRA 2 — EL TIEMPO SE ESTIRA
    cv = draw_pizarra_frame(
        t, t_02, "EL TIEMPO SE ESTIRA",
        summary_es="AL FUTURO, SÍ · 1 SEGUNDO POR SEGUNDO",
        t_summary=t_07 + 0.2
    )
    d = ImageDraw.Draw(cv)
    window(cv, 76, 42, 328, 156, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.95)

    if t < t_03:
        # c6_02: Einstein y dos relojes iguales
        draw_text(cv, "RELATIVIDAD · ALBERT EINSTEIN", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        draw_pocket_watch(cv, 174, 116, t, r=24, reverse=False, speed=1.4)
        draw_pocket_watch(cv, 306, 116, t, r=24, reverse=False, speed=1.4)
        draw_text(cv, "EL TIEMPO NO PASA IGUAL PARA TODOS", 240, 170, "silk", 8, CHALK_WHITE, align="center")
        person_card(cv, "einstein", "ALBERT EINSTEIN", "FÍSICO · RELATIVIDAD",
                    t, t_02 + 0.3, dur=3.4)

    elif t < t_04:
        # c6_03: Un reloj quieto en la Tierra y otro en nave rápida (avanza más lento)
        draw_text(cv, "DILATACIÓN DEL TIEMPO", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        draw_pocket_watch(cv, 168, 112, t, r=22, reverse=False, speed=2.4)
        draw_text(cv, "QUIETO (NORMAL)", 168, 146, "silk", 8, CHALK_WHITE, align="center")
        draw_pocket_watch(cv, 312, 112, t, r=22, reverse=False, speed=0.6)
        draw_text(cv, "MUY RÁPIDO (LENTO)", 312, 146, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "MÁS VELOCIDAD = TIEMPO MÁS LENTO", 240, 172, "silk", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, 344, 128, t)

    elif t < t_05:
        # c6_04: 6 meses en la Estación Espacial -> ≈ 0,005 segundos más joven
        draw_text(cv, "6 MESES EN ÓRBITA", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "≈ 0,005 SEGUNDOS", 240, 96, "press", 16, CHALK_CYAN, align="center")
        draw_text(cv, "CINCO MILÉSIMAS DE SEGUNDO", 240, 134, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "MÁS JOVEN AL VOLVER A LA TIERRA", 240, 156, "silk", 8, CHALK_GREEN, align="center")

    elif t < t_06:
        # c6_05: Gemelos astronautas Scott y Mark Kelly
        draw_text(cv, "SCOTT Y MARK KELLY (NASA)", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        d.rectangle([104, 82, 228, 148], outline=(*CHALK_CYAN, 255), width=2)
        draw_text(cv, "SCOTT KELLY", 166, 94, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "1 AÑO EN ÓRBITA", 166, 116, "silk", 8, CHALK_WHITE, align="center")
        d.rectangle([252, 82, 376, 148], outline=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "MARK KELLY", 314, 94, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "EN LA TIERRA", 314, 116, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "SCOTT VOLVIÓ MILÉSIMAS MÁS JOVEN", 240, 170, "silk", 8, CHALK_GREEN, align="center")

    elif t < t_07:
        # c6_06: Satélite GPS corrige su reloj -> mapa en celular
        draw_text(cv, "SATÉLITES GPS EN TU CELULAR", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        # Satélite en tiza izquierda
        d.rectangle([136, 98, 168, 120], outline=(*CHALK_CYAN, 255), width=2)
        d.rectangle([108, 102, 136, 116], outline=(*CHALK_WHITE, 255), width=1)
        d.rectangle([168, 102, 196, 116], outline=(*CHALK_WHITE, 255), width=1)
        draw_text(cv, "GPS", 152, 128, "press", 8, CHALK_CYAN, align="center")
        # Ondas hacia celular derecha
        d.line([(204, 112), (288, 112)], fill=(*CHALK_YELLOW, 255), width=2)
        d.rectangle([296, 86, 344, 144], outline=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "MAPA", 320, 108, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "SIN CORRECCIÓN: ERROR DE KILÓMETROS", 240, 170, "silk", 8, CHALK_WHITE, align="center")

    else:
        # c6_07: Remate EN UNA FRASE
        draw_text(cv, "AL FUTURO, SÍ", 240, 74, "press", 16, CHALK_YELLOW, align="center")
        draw_text(cv, "TODOS VIAJAMOS AL FUTURO.", 240, 114, "press", 8, CHALK_WHITE, align="center")
        draw_text(cv, "A UN SEGUNDO POR SEGUNDO.", 240, 138, "press", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.30)


def scenes():
    return [
        (TL.start("c6_00") - 0.1, card_ch6, None),
        (TL.start("c6_01") - 0.1, scene_ch6, None),
    ]
