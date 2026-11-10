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
    draw_sand_wind(cv, t, density=46, color=(242, 206, 134))

    window(cv, 16, 10, 448, 36, fill=(28, 18, 12), border=GOLD, alpha=0.95)
    if t < t2:
        draw_text(cv, "LA TERCERA PELÍCULA ADAPTA EL MESÍAS DE DUNE (1969)", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "EL LIBRO QUE AQUEL PRIMER EDITOR NO QUISO PUBLICAR", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t1) * 32)
    else:
        draw_text(cv, "EL CIERRE DE UNA ÉPOCA", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "VILLENEUVE DIJO QUE SERÁ SU ÚLTIMA PELÍCULA DE DUNE", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t2) * 32)

    t_ultima = TL.word("c8_02", "ultima")
    char(cv, HERBERT, 84, 260, t, scale=2,
         arms="point" if t < t2 else "note", look=1, mood="happy")
    char(cv, VILLENEUVE, 396, 260, t, scale=2,
         arms="wave" if t >= t_ultima else "point_l", look=-1,
         talk=talk_v(t, t >= t2), mood="happy")

    a_m, dy_m = pop(t, t1 + 0.05)
    window(cv, 136, 58 + dy_m, 208, 108, fill=(32, 20, 14), border=GOLD, alpha=0.96 * a_m)
    draw_text(cv, "1969 → 2026", 240, 70 + dy_m, "silk", 8, CYAN, align="center")
    draw_text(cv, "EL MESÍAS DE DUNE", 240, 90 + dy_m, "press", 8, GOLD, align="center")
    if t < t2:
        draw_text(cv, "DE RECHAZADO EN 1969", 240, 114 + dy_m, "silk", 8, RED, align="center")
        draw_text(cv, "A SUPERPRODUCCIÓN MUNDIAL", 240, 130 + dy_m, "silk", 8, GREEN, align="center")
    else:
        a_q, dy_q = pop(t, t2 + 0.05)
        window(cv, 152, 112 + dy_q, 176, 38, fill=(58, 32, 14), border=CREAM, alpha=0.98 * a_q)
        draw_text(cv, "DENIS VILLENEUVE:", 240, 120 + dy_q, "silk", 8, CYAN, align="center")
        draw_text(cv, "«MI ÚLTIMA DUNE»", 240, 134 + dy_q, "press", 8, GOLD, align="center")

    return cv


# ===========================================================================
# ESCENA 26 (c8_03, c8_04, c8_05): 18 de diciembre, "Dunesday" y las pantallas IMAX
# ===========================================================================
def scene_dunesday_imax(t):
    t3 = TL.s("c8_03")
    t4 = TL.s("c8_04")
    t5 = TL.s("c8_05")
    dx, dy = shake(t, t4 + 0.05, dur=0.25, amp=3)
    cv = bg("bg_cinema_2024_packed").copy()

    window(cv, 16, 10, 448, 36, fill=(24, 16, 28), border=GOLD, alpha=0.95)
    if t < t4:
        draw_text(cv, "ESTRENO EN ESTADOS UNIDOS: 18 DE DICIEMBRE", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MISMO DÍA QUE AVENGERS: DOOMSDAY", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t3) * 32)
    elif t < t5:
        draw_text(cv, "EL CHOQUE DE TITANES EN LA CARTELERA MUNDIAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "INTERNET YA LE PUSO NOMBRE A ESE DÍA: DUNESDAY", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t4) * 32)
    else:
        draw_text(cv, "LA VICTORIA EN FORMATO GIGANTE", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "DUNE SE QUEDÓ CON LAS PANTALLAS IMAX DE SU ESTRENO", 240, 30, "press", 8, GREEN, align="center",
                  reveal=(t - t5) * 32)

    t_avengers = TL.word("c8_03", "Avengers")
    char(cv, VILLENEUVE, 82, 260, t, scale=2,
         arms="cheer" if t >= t5 else "point", look=1, mood="happy")
    char(cv, READER_1, 384, 260, t, scale=2,
         arms="cheer" if t >= t4 else "point_l", look=-1, mood="happy")
    char(cv, READER_2, 434, 260, t, scale=2,
         arms="wave" if t >= t5 else "hips", look=-1, mood="happy")

    if t < t4:
        a_v, dy_v = pop(t, t3 + 0.05)
        window(cv, 128, 58 + dy_v, 224, 98, fill=(24, 18, 34), border=GOLD, alpha=0.96 * a_v)
        draw_text(cv, "18 DE DICIEMBRE", 240, 70 + dy_v, "press", 8, GOLD, align="center")
        window(cv, 140, 88 + dy_v, 94, 52, fill=(54, 32, 12), border=GOLD, alpha=0.98 * a_v)
        draw_text(cv, "DUNE 3", 187, 102 + dy_v, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MESÍAS", 187, 120 + dy_v, "silk", 8, CREAM, align="center")

        if t >= t_avengers - 0.15:
            a_av, dy_av = pop(t, t_avengers - 0.15)
            window(cv, 246, 88 + dy_av, 94, 52, fill=(18, 44, 34), border=GREEN, alpha=0.98 * a_av)
            draw_text(cv, "AVENGERS", 293, 102 + dy_av, "press", 8, GREEN, align="center")
            draw_text(cv, "DOOMSDAY", 293, 120 + dy_av, "silk", 8, CREAM, align="center")
    elif t < t5:
        a_d, dy_d = pop(t, t4 + 0.05)
        window(cv, 124, 58 + dy_d, 232, 98, fill=(36, 22, 12), border=GOLD, alpha=0.98 * a_d)
        draw_text(cv, "18 DE DICIEMBRE", 240, 72 + dy_d, "silk", 8, CYAN, align="center")
        draw_text(cv, "DUNESDAY", 240, 94 + dy_d, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, "EL EVENTO DEL CINE MUNDIAL", 240, 126 + dy_d, "silk", 8, CREAM, align="center")
        sparkle(cv, 140, 96 + dy_d, t, 3)
        sparkle(cv, 340, 98 + dy_d, t + 1.1, 3)
    else:
        a_i, dy_i = pop(t, t5 + 0.05)
        window(cv, 124, 58 + dy_i, 232, 98, fill=(14, 34, 42), border=CYAN, alpha=0.98 * a_i)
        draw_text(cv, "EXCLUSIVA DE ESTRENO", 240, 72 + dy_i, "silk", 8, GOLD, align="center")
        draw_text(cv, "PANTALLAS IMAX", 240, 94 + dy_i, "press", 16, CYAN, align="center", outline_w=2)
        draw_text(cv, "RESERVADAS PARA DUNE", 240, 126 + dy_i, "press", 8, GREEN, align="center")

    return offset_canvas(cv, dx, dy)


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
        draw_text(cv, "LOS HOMBRES DE FLORENCE LOGRARON FRENAR LA ARENA CON PASTO", 240, 30, "silk", 8, GREEN, align="center",
                  reveal=(t - t6) * 32)

        # Pasto verde firme cubriendo toda la duna y mecéndose con la brisa
        for i in range(15):
            gx = 44 + i * 26
            gy = 252 + (i % 2) * 4
            for blade in (-4, -1, 2, 5):
                sway = int(round(math.sin(t * 4.5 + i) * 2))
                d.line([(gx, gy), (gx + blade + sway, gy - 12)], fill=(64, 168, 78, 255), width=2)

        t_frenar = TL.word("c8_06", "frenar")
        char(cv, USDA_WORKER_1, 136, 258, t, scale=2, arms="hips", look=1, mood="happy")
        char(cv, USDA_WORKER_2, 224, 258, t, scale=2, arms="point" if t >= t_frenar else "work", look=1, mood="happy")
        char(cv, HERBERT, 368, 258, t, scale=2, arms="note", look=-1, mood="happy")
        return cv

    # Escena 28 (c8_07): Match cut — El haz de luz del proyector IMAX ilumina la sala repleta
    cv = bg("bg_imax_2026").copy()
    d = ImageDraw.Draw(cv)
    CONF.draw(cv, t)

    # Haz de luz volumétrico dorado que baja desde la cabina de proyección hacia la pantalla IMAX
    for k in range(18):
        y_beam = 66 + k * 5
        alpha_b = int(75 * (1.0 - abs(k - 9) / 10.0))
        d.line([(240, 14), (70 + k * 19, y_beam)], fill=(255, 215, 120, alpha_b), width=3)

    # Gran pantalla IMAX iluminada en el centro
    a_f, dy_f = pop(t, t7)
    window(cv, 32, 42 + dy_f, 416, 136, fill=(24, 16, 10), border=GOLD, alpha=0.96 * a_f)
    draw_sand_wind(cv, t, density=42, color=(255, 222, 148), y_min=48, y_max=170)
    draw_text(cv, "LA DE HERBERT, EN CAMBIO,", 240, 58 + dy_f, "silk", 8, CYAN, align="center")
    draw_text(cv, "NUNCA DEJÓ DE MOVERSE", 240, 78 + dy_f, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2,
              reveal=(t - t7 - 0.15) * 24)

    draw_text(cv, "LA ARENA QUE NUNCA SE DETUVO", 240, 114 + dy_f, "press", 8, CREAM, align="center")
    draw_text(cv, "1957 → 2026", 240, 134 + dy_f, "press", 16, GOLD, align="center", outline_w=2)

    # Frank Herbert, Denis Villeneuve y los espectadores contemplan la pantalla y celebran en "nunca dejó de moverse"
    t_moverse = TL.word("c8_07", "moverse")
    char(cv, HERBERT, 76, 262, t, scale=2, arms="cheer" if t >= t_moverse else "point", look=1, mood="happy")
    char(cv, READER_1, 178, 262, t, scale=2, arms="cheer" if t >= t_moverse else "hold", look=1, mood="happy")
    char(cv, READER_2, 302, 262, t, scale=2, arms="wave" if t >= t_moverse else "hold", look=-1, mood="happy")
    char(cv, VILLENEUVE, 404, 262, t, scale=2, arms="cheer" if t >= t_moverse else "point_l", look=-1, mood="happy")
    return cv


def scenes():
    return [
        (TL.chapter_start(8) - 0.3, make_card(8, ["DUNESDAY"], "DICIEMBRE DE 2026 · EL MESÍAS EN IMAX"), None),
        (TL.s("c8_01") - 0.15, scene_messiah_adaptation, lambda t: cam_push(t, TL.s("c8_01"), TL.s("c8_03"), 1.0, 1.09, (240, 140), (240, 130))),
        (TL.s("c8_03") - 0.15, scene_dunesday_imax, lambda t: (1.0 + cam_punch(t, [TL.s("c8_04"), TL.s("c8_05")], 0.07), 240, 140)),
        (TL.s("c8_06") - 0.15, scene_finale_sand_never_stopped, lambda t: cam_push(t, TL.s("c8_07"), TL.e("c8_07"), 1.0, 1.12, (240, 135), (240, 120))),
    ]
