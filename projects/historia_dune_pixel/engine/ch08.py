"""Capítulo 8: Dunesday y Cierre Circular 1957 -> 2026 (c8_00..c8_07)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from ch01 import HERBERT, USDA_WORKER_1, USDA_WORKER_2, READER_1, READER_2
from ch06 import VILLENEUVE


# ===========================================================================
# ESCENA 25 (c8_01, c8_02): El Mesías de Dune en el cine y la despedida de Villeneuve
# ===========================================================================
def scene_messiah_adaptation(t):
    t1 = TL.s("c8_01")
    t2 = TL.s("c8_02")
    cv = bg("bg_wadi_rum_2019").copy()
    draw_sand_wind(cv, t, density=42, color=(242, 206, 134))

    window(cv, 16, 10, 448, 36, fill=(28, 18, 12), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "LA TERCERA PELÍCULA ADAPTA EL MESÍAS DE DUNE (1969)", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "EL LIBRO QUE AQUEL PRIMER EDITOR NO QUISO PUBLICAR", 240, 30, "silk", 8, CYAN, align="center")
    else:
        draw_text(cv, "EL CIERRE DE UNA ÉPOCA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "VILLENEUVE DIJO QUE SERÁ SU ÚLTIMA PELÍCULA DE DUNE", 240, 30, "press", 8, GOLD, align="center")

    char(cv, HERBERT, 88, 260, t, scale=2, arms="point", look=1, mood="happy")
    char(cv, VILLENEUVE, 384, 260, t, scale=2, arms="point", look=-1, talk=talk_v(t, True))
    robot(cv, 32, 260, t, face="excited", scale=1)

    window(cv, 136, 58, 208, 108, fill=(32, 20, 14), border=GOLD, alpha=0.96)
    draw_text(cv, "1969 → 2026", 240, 70, "silk", 8, CYAN, align="center")
    draw_text(cv, "EL MESÍAS DE DUNE", 240, 90, "press", 8, GOLD, align="center")
    if t < t2:
        draw_text(cv, "DE RECHAZADO EN 1969", 240, 114, "silk", 8, RED, align="center")
        draw_text(cv, "A SUPERPRODUCCIÓN MUNDIAL", 240, 130, "silk", 8, GREEN, align="center")
    else:
        window(cv, 152, 112, 176, 38, fill=(58, 32, 14), border=CREAM, alpha=0.98)
        draw_text(cv, "DENIS VILLENEUVE:", 240, 120, "silk", 8, CYAN, align="center")
        draw_text(cv, "«MI ÚLTIMA DUNE»", 240, 134, "press", 8, GOLD, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 26 (c8_03, c8_04, c8_05): 18 de diciembre, "Dunesday" y las pantallas IMAX
# ===========================================================================
def scene_dunesday_imax(t):
    t3 = TL.s("c8_03")
    t4 = TL.s("c8_04")
    t5 = TL.s("c8_05")
    cv = bg("bg_cinema_2024_packed").copy()

    window(cv, 16, 10, 448, 36, fill=(24, 16, 28), border=GOLD, alpha=0.95)
    if t < t4:
        draw_text(cv, "ESTRENO EN ESTADOS UNIDOS: 18 DE DICIEMBRE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MISMO DÍA QUE AVENGERS: DOOMSDAY", 240, 30, "silk", 8, CYAN, align="center")
    elif t < t5:
        draw_text(cv, "EL CHOQUE DE TITANES EN LA CARTELERA MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "INTERNET YA LE PUSO NOMBRE A ESE DÍA: DUNESDAY", 240, 30, "press", 8, GOLD, align="center")
    else:
        draw_text(cv, "LA VICTORIA EN FORMATO GIGANTE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "DUNE SE QUEDÓ CON LAS PANTALLAS IMAX DE SU ESTRENO", 240, 30, "press", 8, GREEN, align="center")

    char(cv, VILLENEUVE, 84, 260, t, scale=2, arms="cheer" if t >= t5 else "point", look=1, mood="happy")
    char(cv, READER_1, 368, 260, t, scale=2, arms="cheer", look=-1, mood="happy")
    char(cv, READER_2, 428, 260, t, scale=2, arms="point", look=-1, mood="happy")
    robot(cv, 32, 260, t, face="excited", scale=1)

    if t < t4:
        window(cv, 128, 58, 224, 98, fill=(24, 18, 34), border=GOLD, alpha=0.96)
        draw_text(cv, "18 DE DICIEMBRE", 240, 70, "press", 8, GOLD, align="center")
        window(cv, 140, 88, 94, 52, fill=(54, 32, 12), border=GOLD, alpha=0.98)
        draw_text(cv, "DUNE 3", 187, 102, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MESÍAS", 187, 120, "silk", 8, CREAM, align="center")

        window(cv, 246, 88, 94, 52, fill=(18, 44, 34), border=GREEN, alpha=0.98)
        draw_text(cv, "AVENGERS", 293, 102, "press", 8, GREEN, align="center")
        draw_text(cv, "DOOMSDAY", 293, 120, "silk", 8, CREAM, align="center")
    elif t < t5:
        window(cv, 124, 58, 232, 98, fill=(36, 22, 12), border=GOLD, alpha=0.98)
        draw_text(cv, "18 DE DICIEMBRE", 240, 72, "silk", 8, CYAN, align="center")
        draw_text(cv, "DUNESDAY", 240, 94, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, "EL EVENTO DEL CINE MUNDIAL", 240, 126, "silk", 8, CREAM, align="center")
    else:
        window(cv, 124, 58, 232, 98, fill=(14, 34, 42), border=CYAN, alpha=0.98)
        draw_text(cv, "EXCLUSIVA DE ESTRENO", 240, 72, "silk", 8, GOLD, align="center")
        draw_text(cv, "PANTALLAS IMAX", 240, 94, "press", 16, CYAN, align="center", outline_w=2)
        draw_text(cv, "RESERVADAS PARA DUNE", 240, 126, "press", 8, GREEN, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=40, x_end=440)
    return cv


# ===========================================================================
# ESCENA 27 Y 28 (c8_06, c8_07): Cierre circular — Oregón 1957 -> Sala IMAX 2026
# ===========================================================================
def scene_finale_sand_never_stopped(t):
    t6 = TL.s("c8_06")
    t7 = TL.s("c8_07")

    if t < t7 - 0.10:
        # Escena 27 (c8_06): En 1957, los hombres de Florence lograron frenar la arena con pasto
        cv = bg("bg_grass_planting_1957").copy()
        d = ImageDraw.Draw(cv)
        window(cv, 16, 10, 448, 36, fill=(14, 28, 22), border=GREEN, alpha=0.95)
        draw_text(cv, "1957 · FLORENCE, OREGÓN", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "LOS HOMBRES DE FLORENCE LOGRARON FRENAR LA ARENA CON PASTO", 240, 30, "silk", 8, GREEN, align="center")

        # Pasto verde firme cubriendo toda la duna
        for i in range(15):
            gx = 44 + i * 26
            gy = 252 + (i % 2) * 4
            for blade in (-4, -1, 2, 5):
                d.line([(gx, gy), (gx + blade, gy - 12)], fill=(64, 168, 78, 255), width=2)

        char(cv, USDA_WORKER_1, 136, 258, t, scale=2, arms="hips", look=1, mood="happy")
        char(cv, USDA_WORKER_2, 228, 258, t, scale=2, arms="cheer", look=1, mood="happy")
        char(cv, HERBERT, 356, 258, t, scale=2, arms="note", look=-1, mood="happy")
        robot(cv, 428, 258, t, face="happy", scale=1)

        # La ondulación de arena cruza hacia la derecha para hacer el Match Cut con el proyector IMAX
        u6 = clamp01((t - t6) / max(0.8, t7 - t6))
        draw_sand_ripple(cv, t, y_base=240, x_start=40, x_end=460, progress=u6)
        return cv

    # Escena 28 (c8_07): Match cut — La línea de arena se convierte en el haz de luz del proyector IMAX
    cv = bg("bg_imax_2026").copy()
    d = ImageDraw.Draw(cv)
    u7 = clamp01((t - t7) / max(1.0, TL.e("c8_07") - t7))

    # Haz de luz volumétrico dorado que nace de la ondulación de arena y se abre hacia la pantalla IMAX
    for k in range(18):
        y_beam = 66 + k * 5
        alpha_b = int(75 * (1.0 - abs(k - 9) / 10.0))
        d.line([(240, 14), (70 + k * 19, y_beam)], fill=(255, 215, 120, alpha_b), width=3)

    # Gran pantalla IMAX iluminada en el centro
    window(cv, 44, 42, 392, 136, fill=(24, 16, 10), border=GOLD, alpha=0.96)
    draw_sand_wind(cv, t, density=36, color=(255, 222, 148), y_min=48, y_max=170)
    draw_text(cv, "LA DE HERBERT, EN CAMBIO,", 240, 58, "silk", 8, CYAN, align="center")
    draw_text(cv, "NUNCA DEJÓ DE MOVERSE", 240, 78, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)

    draw_text(cv, "LA ARENA QUE NUNCA SE DETUVO", 240, 114, "press", 8, CREAM, align="center")
    draw_text(cv, "1957 → 2026", 240, 134, "press", 16, GOLD, align="center", outline_w=2)

    # La ondulación dorada atraviesa la pantalla IMAX sin detenerse jamás
    draw_sand_ripple(cv, t, y_base=164, x_start=76, x_end=404, progress=u7)

    # Espectadores y La Máquina viendo la pantalla gigante desde la sala (feet=262)
    char(cv, HERBERT, 76, 262, t, scale=2, arms="hips", look=1, mood="happy")
    char(cv, VILLENEUVE, 404, 262, t, scale=2, arms="hips", look=-1, mood="happy")
    robot(cv, 240, 262, t, face="excited", scale=1)
    return cv


def scenes():
    return [
        (TL.chapter_start(8) - 0.3, make_card(8, ["DUNESDAY"], "DICIEMBRE DE 2026 · EL MESÍAS EN IMAX")),
        (TL.s("c8_01") - 0.15, scene_messiah_adaptation),
        (TL.s("c8_03") - 0.15, scene_dunesday_imax),
        (TL.s("c8_06") - 0.15, scene_finale_sand_never_stopped),
    ]
