"""Capítulo 3: El héroe era una advertencia (c3_00..c3_07)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, READER_1, READER_2

EDITOR_CAMPBELL = {
    "skin": (232, 188, 150), "hair": (165, 165, 172), "hair_style": "parted",
    "glasses": True,
    "shirt": (238, 238, 242), "jacket": (82, 54, 48),
    "tie": (140, 42, 42), "pants": (52, 44, 42),
}


# ===========================================================================
# ESCENA 10 (c3_01, c3_02): Libro de culto a fines de los 60 y El Mesías de Dune (1969)
# ===========================================================================
def scene_cult_and_messiah(t):
    t1 = TL.s("c3_01")
    t2 = TL.s("c3_02")
    cv = bg("bg_campus_1968").copy()

    window(cv, 16, 10, 448, 36, fill=(22, 18, 14), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "FINES DE LOS AÑOS 60 · FENÓMENO CONTRACULTURAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "DUNE YA ERA UN LIBRO DE CULTO ENTRE LOS JÓVENES", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "1969 · FRANK HERBERT PUBLICA LA CONTINUACIÓN", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "EL MESÍAS DE DUNE", 240, 30, "press", 8, GOLD, align="center")

    # Jóvenes universitarios y Herbert en el campus (feet=260)
    char(cv, READER_1, 88, 260, t, scale=2, arms="point", look=1, mood="happy")
    char(cv, READER_2, 168, 260, t, scale=2, arms="note", look=1, mood="happy")
    char(cv, HERBERT, 368, 260, t, scale=2, arms="point", look=-1, talk=talk_v(t, True))
    robot(cv, 430, 260, t, face="question" if t >= t2 else "happy", scale=1)

    if t < t2:
        window(cv, 140, 64, 200, 68, fill=(24, 32, 22), border=GREEN, alpha=0.95)
        draw_text(cv, "FENÓMENO EN CAMPUS", 240, 76, "press", 8, GOLD, align="center")
        draw_text(cv, "ECOLOGÍA Y REBELDÍA", 240, 94, "silk", 8, CREAM, align="center")
        draw_text(cv, "FINES DE LOS 60", 240, 110, "silk", 8, CYAN, align="center")
    else:
        window(cv, 128, 58, 224, 88, fill=(38, 18, 24), border=GOLD, alpha=0.96)
        draw_text(cv, "SEGUNDA NOVELA (1969)", 240, 68, "silk", 8, CYAN, align="center")
        draw_text(cv, "EL MESÍAS DE DUNE", 240, 88, "press", 8, GOLD, align="center")
        draw_text(cv, "EL PROTAGONISTA VISTO", 240, 110, "silk", 8, CREAM, align="center")
        draw_text(cv, "DESDE SU LADO MÁS OSCURO", 240, 124, "silk", 8, RED, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=36, x_end=444)
    return cv


# ===========================================================================
# ESCENA 11 (c3_03, c3_04, c3_05): La advertencia sobre los líderes carismáticos
# ===========================================================================
def scene_hero_warning(t):
    t3 = TL.s("c3_03")
    t4 = TL.s("c3_04")
    t5 = TL.s("c3_05")
    cv = bg("bg_herbert_study_1960").copy()

    window(cv, 16, 10, 448, 36, fill=(28, 16, 18), border=GOLD, alpha=0.95)
    if t < t4:
        draw_text(cv, "EL EDITOR DE LA PRIMERA HISTORIA LA RECHAZÓ", 240, 16, "press", 8, RED, align="center")
        draw_text(cv, "«LOS LECTORES QUIEREN HÉROES, NO ANTIHÉROES»", 240, 30, "silk", 8, CREAM, align="center")
    elif t < t5:
        draw_text(cv, "EL MENSAJE CENTRAL DE FRANK HERBERT", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "EL HÉROE ERA UNA ADVERTENCIA", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "RECUERDA ESE LIBRO", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "ES EL QUE LLEGA AL CINE EN DICIEMBRE", 240, 30, "silk", 8, CYAN, align="center")

    char(cv, HERBERT, 100, 260, t, scale=2, arms="point", look=1, talk=talk_v(t, True))
    char(cv, EDITOR_CAMPBELL, 392, 260, t, scale=2, arms="cross", look=-1, mood="angry" if t < t4 else "neutral")
    robot(cv, 38, 260, t, face="surprised" if t >= t5 else "question", scale=1)

    if t < t4:
        window(cv, 148, 66, 196, 84, fill=(64, 18, 22), border=RED, alpha=0.96)
        draw_text(cv, "REVISTA ANALOG · 1969", 246, 78, "silk", 8, GOLD, align="center")
        draw_text(cv, "RECHAZADO", 246, 98, "press", 16, RED, align="center", outline_w=2)
        draw_text(cv, "NO QUERÍA UN ANTIHÉROE", 246, 126, "silk", 8, CREAM, align="center")
    elif t < t5:
        window(cv, 138, 62, 216, 94, fill=(24, 18, 34), border=GOLD, alpha=0.96)
        draw_text(cv, "LA TESIS DE HERBERT", 246, 74, "press", 8, GOLD, align="center")
        draw_text(cv, "UN LÍDER CARISMÁTICO", 246, 96, "press", 8, CREAM, align="center")
        draw_text(cv, "PUEDE SER EL MAYOR", 246, 114, "press", 8, RED, align="center")
        draw_text(cv, "DE LOS PELIGROS", 246, 132, "press", 8, RED, align="center")
    else:
        window(cv, 132, 60, 228, 98, fill=(36, 24, 12), border=GOLD, alpha=0.98)
        draw_text(cv, "EL MESÍAS DE DUNE (1969)", 246, 74, "press", 8, GOLD, align="center")
        draw_text(cv, "BASE DE LA 3ª PELÍCULA", 246, 96, "silk", 8, CYAN, align="center")
        window(cv, 152, 114, 188, 30, fill=(78, 42, 14), border=CREAM, alpha=0.98)
        draw_text(cv, "ESTRENO: DICIEMBRE", 246, 125, "press", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=36, x_end=444)
    return cv


# ===========================================================================
# ESCENA 12 (c3_06, c3_07): Las 6 novelas de Herbert y Arrakis Planitia en Titán (2009)
# ===========================================================================
def scene_six_novels_and_titan(t):
    t6 = TL.s("c3_06")
    t7 = TL.s("c3_07")
    cv = bg("bg_saturn_titan_2009").copy()
    d = ImageDraw.Draw(cv)
    STARS.draw(cv, t * 0.4, alpha=0.75)

    window(cv, 16, 10, 448, 36, fill=(12, 18, 34), border=GOLD, alpha=0.95)
    if t < t7:
        draw_text(cv, "EL LEGADO LITERARIO DE FRANK HERBERT (1920 - 1986)", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ESCRIBIÓ SEIS NOVELAS DE DUNE", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "2009 · TITÁN, LA LUNA DE SATURNO", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "HOY HAY UNA ARRAKIS DE VERDAD EN EL SISTEMA SOLAR", 240, 30, "silk", 8, CYAN, align="center")

    if t < t7:
        # Los 6 tomos dorados de la saga original de Frank Herbert
        window(cv, 36, 62, 408, 124, fill=(16, 20, 38), border=GOLD, alpha=0.94)
        draw_text(cv, "LAS 6 CRÓNICAS DE DUNE (1965 - 1985)", 240, 74, "press", 8, GOLD, align="center")
        yrs = ["1965", "1969", "1976", "1981", "1984", "1985"]
        for i, yr in enumerate(yrs):
            bx = 56 + i * 62
            by = 94
            d.rectangle([bx, by, bx + 48, by + 68], fill=(184, 112, 38, 255), outline=(*GOLD, 255), width=2)
            draw_text(cv, f"TOMO {i + 1}", bx + 24, by + 16, "silk", 8, CREAM, align="center")
            draw_text(cv, yr, bx + 24, by + 38, "press", 8, GOLD, align="center")
        portrait(cv, "herbert", 208, 192, 64)
    else:
        # Retícula astronómica sobre las llanuras de Titán: ARRAKIS PLANITIA
        cx, cy = 240, 184
        r = 34 + int(round(math.sin(t * 4.0) * 3))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*CYAN, 235), width=2)
        d.line([(cx - r - 10, cy), (cx - r + 8, cy)], fill=(*CYAN, 235), width=2)
        d.line([(cx + r - 8, cy), (cx + r + 10, cy)], fill=(*CYAN, 235), width=2)
        d.line([(cx, cy - r - 10), (cx, cy - r + 8)], fill=(*CYAN, 235), width=2)
        d.line([(cx, cy + r - 8), (cx, cy + r + 10)], fill=(*CYAN, 235), width=2)

        window(cv, 84, 62, 312, 74, fill=(12, 22, 42), border=CYAN, alpha=0.95)
        draw_text(cv, "UNIÓN ASTRONÓMICA INTERNACIONAL", 240, 72, "silk", 8, CYAN, align="center")
        draw_text(cv, "ARRAKIS PLANITIA", 240, 90, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "LLANURA REAL EN LA LUNA TITÁN (SATURNO)", 240, 116, "silk", 8, CREAM, align="center")

    robot(cv, 428, 258, t, face="excited", scale=1)
    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


def scenes():
    return [
        (TL.chapter_start(3) - 0.3, make_card(3, ["EL HÉROE ERA", "UNA ADVERTENCIA"], "1968 - 2009 · EL MESÍAS Y TITÁN")),
        (TL.s("c3_01") - 0.15, scene_cult_and_messiah),
        (TL.s("c3_03") - 0.15, scene_hero_warning),
        (TL.s("c3_06") - 0.15, scene_six_novels_and_titan),
    ]
