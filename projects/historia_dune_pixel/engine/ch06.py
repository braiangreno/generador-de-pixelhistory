"""Capítulo 6: El chico de trece años (c6_00..c6_06)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch05 import CREW_CAM

VILLENEUVE = {
    "name": "Denis Villeneuve",
    "skin": (236, 194, 158), "hair": (88, 82, 80), "hair_style": "parted",
    "beard": (78, 72, 70),
    "shirt": (54, 58, 68), "jacket": (28, 32, 42),
    "pants": (24, 28, 36),
}
PRODUCER = {
    "name": "Mary Parent",
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
        draw_text(cv, "«¿CUÁL ES SU PROYECTO SOÑADO?» — «DUNE»", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t1) * 32)
    else:
        draw_text(cv, "LA ENTREVISTA QUE LO CAMBIÓ TODO", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA PRODUCTORA LEYÓ LA NOTA Y LO LLAMÓ", 240, 30, "press", 8, GREEN, align="center",
                  reveal=(t - t2) * 32)

    vx, vph, _ = pace(t, t1, 48, 128, period=2.6, pause=0.2)
    char(cv, VILLENEUVE, vx, 260, t, scale=2, walk=vph,
         arms="cheer" if t >= t2 else "point", look=1, talk=talk_v(t, True), mood="happy")
    if t >= t2:
        px, pph, _ = pace(t, t2, 442, 368, period=2.5, pause=0.2)
        char(cv, PRODUCER, px, 260, t, scale=2, walk=pph, arms="wave", look=-1, mood="happy", talk=talk_v(t, True))

    a_w, dy_w = pop(t, t1 + 0.05)
    window(cv, 172, 58 + dy_w, 268, 98, fill=(26, 16, 22), border=GOLD if t < t2 else GREEN, alpha=0.96 * a_w)
    portrait(cv, "villeneuve", 184, 68 + dy_w, 64)
    draw_text(cv, "DENIS VILLENEUVE", 260, 68 + dy_w, "press", 8, GOLD)
    draw_text(cv, "VENECIA · SEPTIEMBRE 2016", 260, 84 + dy_w, "silk", 8, CYAN)
    if t < t2:
        a_r, dy_r = pop(t, t1 + 0.35)
        window(cv, 258, 100 + dy_r, 168, 42, fill=(58, 32, 14), border=GOLD, alpha=0.98 * a_r)
        draw_text(cv, "RESPUESTA:", 342, 108 + dy_r, "silk", 8, CREAM, align="center")
        draw_text(cv, "«DUNE»", 342, 122 + dy_r, "press", 8, GOLD, align="center")
    else:
        a_r, dy_r = pop(t, t2 + 0.05)
        window(cv, 258, 100 + dy_r, 168, 42, fill=(16, 56, 32), border=GREEN, alpha=0.98 * a_r)
        draw_text(cv, "DERECHOS RECIÉN COMPRADOS", 342, 108 + dy_r, "silk", 8, CREAM, align="center")
        draw_text(cv, "¡CONTRATADO!", 342, 122 + dy_r, "press", 8, GOLD, align="center")
        sparkle(cv, 268, 112 + dy_r, t, 3)

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
        draw_text(cv, "LOS DIBUJOS DE DUNE QUE HABÍA HECHO A LOS 13 AÑOS", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t3) * 32)

        vx, vph, _ = pace(t, t3, 48, 126, period=2.6, pause=0.2)
        char(cv, VILLENEUVE, vx, 260, t, scale=2, walk=vph, arms="note", look=1, mood="happy", talk=talk_v(t, True))

        a_nb, dy_nb = pop(t, t3 + 0.1)
        window(cv, 168, 56 + dy_nb, 286, 142, fill=(32, 24, 18), border=GOLD, alpha=0.96 * a_nb)
        draw_paper(cv, 184, 70 + dy_nb, 118, 112, color=(244, 232, 198))
        # Boceto infantil de dunas y dos soles en el cuaderno
        d.ellipse([264, 84 + dy_nb, 280, 100 + dy_nb], fill=(224, 112, 42, 255))
        d.ellipse([242, 92 + dy_nb, 252, 102 + dy_nb], fill=(238, 168, 68, 255))
        d.polygon([(190, 162 + dy_nb), (226, 128 + dy_nb), (296, 162 + dy_nb)],
                  fill=(216, 164, 88, 255), outline=(120, 82, 38, 255))
        draw_text(cv, "DUNE · 1980", 243, 166 + dy_nb, "silk", 8, INK, align="center")

        draw_text(cv, "CUADERNO ESCOLAR", 376, 84 + dy_nb, "press", 8, GOLD, align="center")
        draw_text(cv, "DENIS · 13 AÑOS", 376, 104 + dy_nb, "silk", 8, CYAN, align="center")
        draw_text(cv, "STORYBOARDS", 376, 124 + dy_nb, "silk", 8, CREAM, align="center")
        draw_text(cv, "GUARDADOS 36 AÑOS", 376, 140 + dy_nb, "silk", 8, GREEN, align="center")
        return cv

    # Escena 20: Rodaje en los desiertos reales de Jordania y Abu Dabi; libro dividido en 2 películas
    cv = bg("bg_wadi_rum_2019").copy()
    draw_sand_wind(cv, t, density=48, color=(244, 208, 138))

    window(cv, 16, 10, 448, 36, fill=(28, 18, 10), border=GOLD, alpha=0.95)
    draw_text(cv, "RODAJE EN LOS DESIERTOS DE JORDANIA Y ABU DABI", 240, 16, "silk", 8, CYAN, align="center")
    draw_text(cv, "DIVIDIÓ LA NOVELA EN DOS PELÍCULAS", 240, 30, "press", 8, GOLD, align="center",
              reveal=(t - t4) * 32)

    # Villeneuve y su camarógrafo recorriendo el desierto de Wadi Rum
    vx, vph, _ = pace(t, t4, 44, 120, period=2.5, pause=0.2)
    cx, cph, _ = pace(t, t4 + 0.3, 442, 372, period=2.7, pause=0.2)
    char(cv, VILLENEUVE, vx, 260, t, scale=2, walk=vph, arms="point", look=1, mood="focused", talk=talk_v(t, True))
    char(cv, CREW_CAM, cx, 260, t, scale=2, walk=cph, arms="work", look=-1, mood="focused")

    # Dos claquetas / bloques con entrada pop()
    a1, dy1 = pop(t, t4 + 0.1)
    window(cv, 152, 66 + dy1, 134, 84, fill=(34, 22, 12), border=GOLD, alpha=0.96 * a1)
    draw_text(cv, "PELÍCULA 1", 219, 80 + dy1, "silk", 8, CYAN, align="center")
    draw_text(cv, "PARTE UNO", 219, 102 + dy1, "press", 8, GOLD, align="center")
    draw_text(cv, "LA PRIMERA MITAD", 219, 124 + dy1, "silk", 8, CREAM, align="center")

    if t >= t4 + 0.45:
        a2, dy2 = pop(t, t4 + 0.45)
        window(cv, 300, 66 + dy2, 134, 84, fill=(34, 22, 12), border=GOLD, alpha=0.96 * a2)
        draw_text(cv, "PELÍCULA 2", 367, 80 + dy2, "silk", 8, CYAN, align="center")
        draw_text(cv, "PARTE DOS", 367, 102 + dy2, "press", 8, GOLD, align="center")
        draw_text(cv, "EL DESENLACE", 367, 124 + dy2, "silk", 8, CREAM, align="center")

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
        draw_text(cv, "ESTRENO EN CINES Y STREAMING EL MISMO DÍA", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t5) * 32)

        a1, dy1 = pop(t, t5 + 0.05)
        window(cv, 24, 62 + dy1, 196, 68, fill=(28, 16, 22), border=RED, alpha=0.95 * a1)
        draw_text(cv, "CINES EN PANDEMIA", 122, 74 + dy1, "press", 8, RED, align="center")
        draw_text(cv, "DEMORA DE CASI 1 AÑO", 122, 94 + dy1, "silk", 8, CREAM, align="center")
        draw_text(cv, "VILLENEUVE PROTESTÓ", 122, 110 + dy1, "silk", 8, GOLD, align="center")

        if t >= t5 + 0.45:
            a2, dy2 = pop(t, t5 + 0.45)
            window(cv, 260, 62 + dy2, 196, 68, fill=(16, 24, 42), border=CYAN, alpha=0.95 * a2)
            draw_text(cv, "OCTUBRE DE 2021", 358, 74 + dy2, "press", 8, CYAN, align="center")
            draw_text(cv, "CINES + STREAMING", 358, 94 + dy2, "silk", 8, CREAM, align="center")
            draw_text(cv, "EL MISMO DÍA", 358, 110 + dy2, "silk", 8, GOLD, align="center")

        vx, vph, vlk = pace(t, t5, 168, 312, period=2.4, pause=0.2)
        char(cv, VILLENEUVE, vx, 260, t, scale=2, walk=vph, arms="shrug", look=vlk, mood="angry", talk=talk_v(t, True))
        return cv

    # c6_06: Más de 400 millones de dólares y 6 Premios Óscar
    cv = bg("bg_oscars_stage_2022").copy()
    d = ImageDraw.Draw(cv)
    CONF.draw(cv, t)

    window(cv, 16, 10, 448, 36, fill=(28, 22, 10), border=GOLD, alpha=0.96)
    draw_text(cv, "ÉXITO CONTRA TODO PRONÓSTICO · +US$ 400 MILLONES", 240, 16, "press", 8, GOLD, align="center")
    draw_text(cv, "GANÓ 6 PREMIOS ÓSCAR · LA MÁS GANADORA DE LA NOCHE", 240, 30, "silk", 8, GREEN, align="center",
              reveal=(t - t6) * 32)

    vx, vph, _ = pace(t, t6, 42, 114, period=2.5, pause=0.2)
    px, pph, _ = pace(t, t6 + 0.3, 446, 384, period=2.6, pause=0.2)
    char(cv, VILLENEUVE, vx, 260, t, scale=2, walk=vph, arms="cheer", look=1, mood="happy")
    char(cv, PRODUCER, px, 260, t, scale=2, walk=pph, arms="cheer", look=-1, mood="happy")

    a_o, dy_o = pop(t, t6 + 0.05)
    window(cv, 146, 58 + dy_o, 292, 112, fill=(28, 22, 12), border=GOLD, alpha=0.96 * a_o)
    draw_text(cv, "TAQUILLA MUNDIAL: +US$ 400M", 292, 70 + dy_o, "press", 8, GREEN, align="center")
    draw_text(cv, "6 PREMIOS ÓSCAR", 292, 90 + dy_o, "press", 16, GOLD, align="center", outline_w=2)

    # 6 estatuillas doradas apareciendo secuencialmente con pop()
    for i in range(6):
        t_os = t6 + 0.2 + i * 0.18
        if t >= t_os:
            ao, dyo = pop(t, t_os, dur=0.25)
            ox = 180 + i * 42
            oy = 124 + dyo
            d.ellipse([ox - 4, oy, ox + 4, oy + 8], fill=(255, 220, 92, 255))
            d.rectangle([ox - 5, oy + 8, ox + 5, oy + 24], fill=(245, 198, 68, 255), outline=(*INK, 255))
            d.rectangle([ox - 7, oy + 24, ox + 7, oy + 28], fill=(120, 90, 34, 255))

    return cv


def scenes():
    return [
        (TL.chapter_start(6) - 0.3, make_card(6, ["EL CHICO DE", "TRECE AÑOS"], "2016 - 2022 · DENIS VILLENEUVE"), None),
        (TL.s("c6_01") - 0.15, scene_venice_2016, lambda t: (1.0 + cam_punch(t, [TL.s("c6_02") + 0.05], 0.07), 240, 140)),
        (TL.s("c6_03") - 0.15, scene_drawings_and_desert, lambda t: cam_push(t, TL.s("c6_03"), TL.s("c6_05"), 1.0, 1.09, (240, 140), (255, 135))),
        (TL.s("c6_05") - 0.15, scene_pandemic_and_oscars, lambda t: (1.0 + cam_punch(t, [TL.s("c6_06") + 0.05], 0.08), 240, 135)),
    ]
