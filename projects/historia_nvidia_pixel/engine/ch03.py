"""Capítulo 3: Miles de manos (GeForce 256 en 1999 + LA PIZARRA 1: ¿Qué es una GPU? CPU profesor vs GPU aula de miles de alumnos)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c3_card = make_card(3, ["MILES DE", "MANOS"], "1999 · GEFORCE 256 Y LA PIZARRA")


def c3_s01_geforce256_gamer(t):
    """c3_01: En 1999 NVIDIA sale a la bolsa y lanza la GeForce 256, la primera GPU del mundo."""
    t0 = TL.s("c3_01")
    cv = bg("gamer_bedroom_1999").copy()
    draw_place_only(cv, "ESTADOS UNIDOS · 1999 · GEFORCE 256", t, t0, border=GPU_GREEN)

    draw_nvidia_prop(cv, 268, 248, kind="gpu_pedestal", t=t, state=1.0)
    char(cv, "gamer_boy", 156, 248, t, scale=2, arms="cheer", look=1, mood="happy",
         talk=talk_v(t, t0 <= t < TL.e("c3_01")))

    a, dy = pop(t, t0 + 0.1)
    window(cv, 104, 42 + dy, 272, 92, fill=(14, 28, 22), border=GPU_GREEN, alpha=0.95)
    draw_text(cv, "1999 · GEFORCE 256", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
    draw_text(cv, "SALIDA A LA BOLSA DE NVIDIA", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "LA PRIMERA «GPU» DEL MUNDO", 240, 94 + dy, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.32)


def c3_s02_pizarra_gpu(t):
    """c3_02..c3_06: LA PIZARRA 1 — ¿Qué es una GPU?
    - c3_02: Pantalla con 2 millones de píxeles cambiando 60 veces por segundo.
    - c3_03: CPU = profesor brillante que resuelve cuentas difíciles una por una.
    - c3_04: GPU = aula con miles de alumnos haciendo cuentas simples todos al mismo tiempo.
    - c3_05: Cada alumno pinta un píxel y entre todos aparece un paisaje.
    - c3_06: EN UNA FRASE: UNA CPU PIENSA RÁPIDO · UNA GPU EN PARALELO."""
    t0 = TL.s("c3_02")
    t_c3_03 = TL.s("c3_03")
    t_c3_04 = TL.s("c3_04")
    t_c3_05 = TL.s("c3_05")
    t_c3_06 = TL.s("c3_06")

    cv = draw_pizarra_frame(t, t0, "GPU · MILES DE MANOS",
                            summary_es="UNA CPU PIENSA RÁPIDO · UNA GPU EN PARALELO",
                            t_summary=t_c3_06)
    d = ImageDraw.Draw(cv)

    if t < t_c3_03 - 0.1:
        # c3_02: Cuadrícula de 2.000.000 de píxeles a 60 Hz
        window(cv, 98, 42, 284, 152, fill=(14, 36, 26), border=CHALK_WHITE, alpha=0.95)
        draw_text(cv, "2.000.000 DE PUNTITOS (PÍXELES)", 240, 50, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "CAMBIAN DE COLOR 60 VECES POR SEGUNDO", 240, 66, "silk", 8, CREAM, align="center")
        gx0, gy0 = 152, 84
        for r in range(8):
            for c in range(16):
                px = gx0 + c * 11
                py = gy0 + r * 11
                active = ((r * 7 + c * 5 + int(t * 18)) % 5 == 0)
                col_p = CHALK_GREEN if active else (36, 78, 56)
                d.rectangle([px, py, px + 8, py + 8], fill=(*col_p, 255), outline=(*CHALK_WHITE, 120))
        draw_chalk_hand(cv, gx0 + int((t * 60) % 160), gy0 + 44, t)
        return vignette(cv, 0.26)

    if t < t_c3_04 - 0.1:
        # c3_03: La CPU como un profesor brillante resolviendo cuentas una por una
        window(cv, 98, 42, 284, 152, fill=(14, 36, 26), border=CHALK_CYAN, alpha=0.95)
        draw_text(cv, "LA CPU: UN PROFESOR BRILLANTE", 240, 50, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "RESUELVE PROBLEMAS DIFÍCILES, UNO POR UNO", 240, 68, "silk", 8, CREAM, align="center")
        char(cv, "prof_cpu", 168, 182, t, scale=2, arms="write", look=1, mood="neutral")
        # Lista de ecuaciones resolviéndose de a una
        eqs = ["1)  ∫ f(x) dx = 42.8", "2)  √(9841) = 99.2", "3)  EN ESPERA...", "4)  EN ESPERA..."]
        for i, eq in enumerate(eqs):
            col_e = CHALK_YELLOW if i == int(t * 2) % 2 else SOFT_GRAY
            draw_text(cv, eq, 224, 94 + i * 18, "silk", 8, col_e)
        return vignette(cv, 0.26)

    # c3_04..c3_06: La GPU como un aula de miles de alumnos pintando píxeles al mismo tiempo
    window(cv, 98, 40, 284, 156, fill=(14, 36, 26), border=CHALK_GREEN, alpha=0.95)
    if t < t_c3_05 - 0.1:
        draw_text(cv, "LA GPU: AULA DE MILES DE ALUMNOS", 240, 48, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "CUENTAS SIMPLES · TODAS AL MISMO TIEMPO", 240, 64, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "MILES DE MANOS A LA VEZ", 240, 48, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "CADA ALUMNO PINTA UN PÍXEL DEL PAISAJE", 240, 64, "silk", 8, CREAM, align="center")

    # Cuadrícula de pupitres/alumnos pintando en paralelo un paisaje de montañas y sol
    gx0, gy0 = 136, 82
    landscape = [
        "0000011110000000",
        "0000111111002200",
        "0001111111102200",
        "0011113311110000",
        "0111133331111000",
        "3333333333333333",
        "4444444444444444",
    ]
    cmap = {"0": (32, 82, 128), "1": (88, 168, 112), "2": CHALK_YELLOW, "3": (64, 198, 118), "4": (46, 138, 84)}
    reveal_p = clamp01((t - t_c3_04) / 2.5)
    for r, row_s in enumerate(landscape):
        for c, ch_c in enumerate(row_s):
            px = gx0 + c * 13
            py = gy0 + r * 14
            col_cell = cmap[ch_c] if (t >= t_c3_05 - 0.2 or ((r * 16 + c) / 112.0) <= reveal_p) else (28, 58, 42)
            d.rectangle([px, py, px + 10, py + 10], fill=(*col_cell, 255), outline=(*CHALK_WHITE, 140))

    return vignette(cv, 0.26)


def scenes():
    return [
        (TL.s("c3_00") - 0.15, c3_card),
        (TL.s("c3_01"), c3_s01_geforce256_gamer,
         lambda t: cam_push(t, TL.s("c3_01"), TL.s("c3_02"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c3_02"), c3_s02_pizarra_gpu,
         lambda t: cam_push(t, TL.s("c3_02"), TL.s("c4_00"), 1.0, 1.025, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("c3_00"), TL.e("c3_06") - TL.s("c3_00"), (174.61, 220.0, 261.63), amp=0.016)


def sfx(A):
    A.fx_sparkle(TL.s("c3_01") + 0.25, 0.06)
    A.fx_pop(TL.s("c3_02") + 0.15, 0.05)
    A.fx_pop(TL.s("c3_03") + 0.15, 0.05)
    A.fx_chime(TL.s("c3_04") + 0.2, 0.06)
    A.fx_sparkle(TL.s("c3_06") + 0.2, 0.06)
