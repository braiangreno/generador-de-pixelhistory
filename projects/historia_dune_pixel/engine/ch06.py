"""Capítulo 6: El chico de trece años (c6_00..c6_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

VILLENEUVE = {
    "skin": (236, 194, 158), "hair": (88, 82, 80), "hair_style": "parted",
    "beard": (78, 72, 70),
    "shirt": (54, 58, 68), "jacket": (28, 32, 42),
    "pants": (24, 28, 36),
}
PRODUCER = {
    "skin": (234, 190, 154), "hair": (150, 110, 56), "hair_style": "long",
    "shirt": (240, 236, 245), "jacket": (148, 42, 62),
    "pants": (42, 38, 48),
}


# ===========================================================================
# ESCENA 18 (c6_01, c6_02): Festival de Venecia 2016 y el llamado
# ===========================================================================
def scene_venice_2016(t):
    t1 = TL.s("c6_01")
    t2 = TL.s("c6_02")
    cv = bg("bg_venice_press_2016").copy()

    window(cv, 16, 10, 448, 36, fill=(32, 14, 18), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "2016 · FESTIVAL DE CINE DE VENECIA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "«¿CUÁL ES SU PROYECTO SOÑADO?» — «DUNE»", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "LA ENTREVISTA QUE LO CAMBIÓ TODO", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA PRODUCTORA LEYÓ LA NOTA Y LO LLAMÓ", 240, 30, "press", 8, GREEN, align="center")

    char(cv, VILLENEUVE, 116, 260, t, scale=2, arms="point", look=1, talk=talk_v(t, True))
    if t >= t2:
        char(cv, PRODUCER, 376, 260, t, scale=2, arms="point", look=-1, mood="happy")
    robot(cv, 42, 260, t, face="excited", scale=1)

    window(cv, 176, 58, 268, 98, fill=(26, 16, 22), border=GOLD if t < t2 else GREEN, alpha=0.96)
    portrait(cv, "villeneuve", 188, 68, 64)
    draw_text(cv, "DENIS VILLENEUVE", 264, 68, "press", 8, GOLD)
    draw_text(cv, "VENECIA · SEPTIEMBRE 2016", 264, 84, "silk", 8, CYAN)
    if t < t2:
        window(cv, 262, 100, 168, 42, fill=(58, 32, 14), border=GOLD, alpha=0.98)
        draw_text(cv, "RESPUESTA:", 346, 108, "silk", 8, CREAM, align="center")
        draw_text(cv, "«DUNE»", 346, 122, "press", 8, GOLD, align="center")
    else:
        window(cv, 262, 100, 168, 42, fill=(16, 56, 32), border=GREEN, alpha=0.98)
        draw_text(cv, "DERECHOS RECIÉN COMPRADOS", 346, 108, "silk", 8, CREAM, align="center")
        draw_text(cv, "¡CONTRATADO!", 346, 122, "press", 8, GOLD, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 19 Y 20 (c6_03, c6_04): Los dibujos de los 13 años y el rodaje en Jordania/Abu Dabi
# ===========================================================================
def scene_drawings_and_desert(t):
    t3 = TL.s("c6_03")
    t4 = TL.s("c6_04")

    if t < t4:
        # Escena 19: Los dibujos de los 13 años encontrados en el escritorio de su padre
        cv = bg("bg_herbert_study_1960").copy()
        d = ImageDraw.Draw(cv)
        window(cv, 16, 10, 448, 36, fill=(26, 18, 14), border=GOLD, alpha=0.95)
        draw_text(cv, "EL HALLAZGO EN EL ESCRITORIO DE SU PADRE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LOS DIBUJOS DE DUNE QUE HABÍA HECHO A LOS 13 AÑOS", 240, 30, "press", 8, GOLD, align="center")

        char(cv, VILLENEUVE, 102, 260, t, scale=2, arms="note", look=1, mood="happy")
        robot(cv, 40, 260, t, face="happy", scale=1)

        window(cv, 168, 56, 286, 142, fill=(32, 24, 18), border=GOLD, alpha=0.96)
        draw_paper(cv, 184, 70, 118, 112, color=(244, 232, 198))
        # Boceto infantil de dunas y dos soles en el cuaderno
        d.ellipse([264, 84, 280, 100], fill=(224, 112, 42, 255))
        d.ellipse([242, 92, 252, 102], fill=(238, 168, 68, 255))
        d.polygon([(190, 162), (226, 128), (296, 162)], fill=(216, 164, 88, 255), outline=(120, 82, 38, 255))
        draw_text(cv, "DUNE · 1980", 243, 166, "silk", 8, INK, align="center")

        draw_text(cv, "CUADERNO ESCOLAR", 376, 84, "press", 8, GOLD, align="center")
        draw_text(cv, "DENIS · 13 AÑOS", 376, 104, "silk", 8, CYAN, align="center")
        draw_text(cv, "STORYBOARDS", 376, 124, "silk", 8, CREAM, align="center")
        draw_text(cv, "GUARDADOS 36 AÑOS", 376, 140, "silk", 8, GREEN, align="center")

        draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
        return cv

    # Escena 20: Rodaje en los desiertos reales de Jordania y Abu Dabi; libro dividido en 2 películas
    cv = bg("bg_wadi_rum_2019").copy()
    draw_sand_wind(cv, t, density=45, color=(244, 208, 138))

    window(cv, 16, 10, 448, 36, fill=(28, 18, 10), border=GOLD, alpha=0.95)
    draw_text(cv, "RODAJE EN LOS DESIERTOS DE JORDANIA Y ABU DABI", 240, 16, "silk", 8, CYAN, align="center")
    draw_text(cv, "DIVIDIÓ LA NOVELA EN DOS PELÍCULAS", 240, 30, "press", 8, GOLD, align="center")

    char(cv, VILLENEUVE, 104, 260, t, scale=2, arms="point", look=1, mood="focused")
    robot(cv, 42, 260, t, face="excited", scale=1)

    # Dos claquetas / bloques: PARTE UNO y PARTE DOS
    window(cv, 168, 66, 134, 84, fill=(34, 22, 12), border=GOLD, alpha=0.96)
    draw_text(cv, "PELÍCULA 1", 235, 80, "silk", 8, CYAN, align="center")
    draw_text(cv, "PARTE UNO", 235, 102, "press", 8, GOLD, align="center")
    draw_text(cv, "LA PRIMERA MITAD", 235, 124, "silk", 8, CREAM, align="center")

    window(cv, 316, 66, 134, 84, fill=(34, 22, 12), border=GOLD, alpha=0.96)
    draw_text(cv, "PELÍCULA 2", 383, 80, "silk", 8, CYAN, align="center")
    draw_text(cv, "PARTE DOS", 383, 102, "press", 8, GOLD, align="center")
    draw_text(cv, "EL DESENLACE", 383, 124, "silk", 8, CREAM, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 21 (c6_05, c6_06): Pandemia (2021), US$ 400M y 6 Premios Óscar
# ===========================================================================
def scene_pandemic_and_oscars(t):
    t5 = TL.s("c6_05")
    t6 = TL.s("c6_06")

    if t < t6:
        cv = bg("bg_pandemic_living_2021").copy()
        window(cv, 16, 10, 448, 36, fill=(18, 20, 34), border=RED, alpha=0.95)
        draw_text(cv, "2020 - 2021 · LA PANDEMIA DEMORA EL ESTRENO CASI UN AÑO", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "ESTRENO EN CINES Y STREAMING EL MISMO DÍA", 240, 30, "press", 8, GOLD, align="center")

        window(cv, 24, 62, 196, 68, fill=(28, 16, 22), border=RED, alpha=0.95)
        draw_text(cv, "CINES EN PANDEMIA", 122, 74, "press", 8, RED, align="center")
        draw_text(cv, "DEMORA DE CASI 1 AÑO", 122, 94, "silk", 8, CREAM, align="center")
        draw_text(cv, "VILLENEUVE PROTESTÓ", 122, 110, "silk", 8, GOLD, align="center")

        window(cv, 260, 62, 196, 68, fill=(16, 24, 42), border=CYAN, alpha=0.95)
        draw_text(cv, "OCTUBRE DE 2021", 358, 74, "press", 8, CYAN, align="center")
        draw_text(cv, "CINES + STREAMING", 358, 94, "silk", 8, CREAM, align="center")
        draw_text(cv, "EL MISMO DÍA", 358, 110, "silk", 8, GOLD, align="center")

        char(cv, VILLENEUVE, 240, 260, t, scale=2, arms="cross", look=1, mood="angry")
        robot(cv, 424, 260, t, face="surprised", scale=1)
        draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
        return cv

    # c6_06: Más de 400 millones de dólares y 6 Premios Óscar
    cv = bg("bg_oscars_stage_2022").copy()
    d = ImageDraw.Draw(cv)
    CONF.draw(cv, t)

    window(cv, 16, 10, 448, 36, fill=(28, 22, 10), border=GOLD, alpha=0.96)
    draw_text(cv, "ÉXITO CONTRA TODO PRONÓSTICO · +US$ 400 MILLONES", 240, 16, "press", 8, GOLD, align="center")
    draw_text(cv, "GANÓ 6 PREMIOS ÓSCAR · LA MÁS GANADORA DE LA NOCHE", 240, 30, "silk", 8, GREEN, align="center")

    char(cv, VILLENEUVE, 92, 260, t, scale=2, arms="cheer", look=1, mood="happy")
    robot(cv, 424, 260, t, face="excited", scale=1)

    window(cv, 152, 58, 292, 112, fill=(28, 22, 12), border=GOLD, alpha=0.96)
    draw_text(cv, "TAQUILLA MUNDIAL: +US$ 400M", 298, 70, "press", 8, GREEN, align="center")
    draw_text(cv, "6 PREMIOS ÓSCAR", 298, 90, "press", 16, GOLD, align="center", outline_w=2)

    # 6 estatuillas doradas alineadas
    for i in range(6):
        ox = 186 + i * 42
        oy = 124
        d.ellipse([ox - 4, oy, ox + 4, oy + 8], fill=(255, 220, 92, 255))
        d.rectangle([ox - 5, oy + 8, ox + 5, oy + 24], fill=(245, 198, 68, 255), outline=(*INK, 255))
        d.rectangle([ox - 7, oy + 24, ox + 7, oy + 28], fill=(120, 90, 34, 255))

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


def scenes():
    return [
        (TL.chapter_start(6) - 0.3, make_card(6, ["EL CHICO DE", "TRECE AÑOS"], "2016 - 2022 · DENIS VILLENEUVE")),
        (TL.s("c6_01") - 0.15, scene_venice_2016),
        (TL.s("c6_03") - 0.15, scene_drawings_and_desert),
        (TL.s("c6_05") - 0.15, scene_pandemic_and_oscars),
    ]
