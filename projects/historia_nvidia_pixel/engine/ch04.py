"""Capítulo 4: La apuesta que nadie quería (CUDA en 2006, laboratorios científicos, el escepticismo de Wall Street y el puente verde hacia una ciudad que aún no existía)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c4_card = make_card(4, ["LA APUESTA QUE", "NADIE QUERÍA"], "2006 - 2012 · CUDA Y WALL STREET")


def c4_s01_cuda_and_science(t):
    """c4_01..c4_02: Escenario de 2006 (CUDA: placas de video para cualquier cálculo) -> científicos simulando física, clima y medicina."""
    t0 = TL.s("c4_01")
    t_c4_02 = TL.s("c4_02")

    if t < t_c4_02 - 0.12:
        cv = bg("stage_cuda_2006").copy()
        draw_place_only(cv, "SANTA CLARA · 2006 · EL LANZAMIENTO DE CUDA", t, t0, border=GPU_GREEN)
        draw_nvidia_prop(cv, 268, 248, kind="gpu_pedestal", t=t, state=1.0)
        char(cv, "huang", 168, 248, t, scale=2, arms="point", look=1, mood="happy",
             talk=talk_v(t, t0 <= t < t_c4_02 - 0.2))

        a, dy = pop(t, t0 + 0.1)
        window(cv, 98, 42 + dy, 284, 92, fill=(12, 26, 20), border=GPU_GREEN, alpha=0.95)
        draw_text(cv, "2006 · LA APUESTA DE CUDA", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
        draw_text(cv, "USAR LAS PLACAS DE VIDEO", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PARA CUALQUIER CÁLCULO, NO SOLO JUEGOS", 240, 94 + dy, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.32)

    # c4_02: Laboratorios con placas de juego simulando física, clima y medicina
    cv = bg("science_gpu_lab").copy()
    draw_place_only(cv, "LABORATORIOS · FÍSICA, CLIMA Y MEDICINA", t, t_c4_02, border=TESLA_CYAN)
    draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=1.0)
    char(cv, "scientist_a", 142, 248, t, scale=2, arms="work", look=1, mood="happy")
    char(cv, "scientist_b", 338, 248, t, scale=2, arms="note", look=-1, mood="happy")

    a, dy = pop(t, t_c4_02 - 0.05)
    window(cv, 98, 42 + dy, 284, 92, fill=(14, 24, 34), border=TESLA_CYAN, alpha=0.95)
    draw_text(cv, "MILES DE MANOS PARA LA CIENCIA", 240, 52 + dy, "press", 8, TESLA_CYAN, align="center")
    draw_text(cv, "CIENTÍFICOS Y PROGRAMADORES SIMULAN:", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "FÍSICA · CLIMA · MEDICINA", 240, 94 + dy, "press", 8, GPU_GREEN, align="center")
    return vignette(cv, 0.32)


def c4_s02_wallstreet_and_bridge(t):
    """c4_03..c4_05: Wall Street niega con la cabeza (US$10.000 millones estancados) -> el puente verde sobre la niebla."""
    t_c4_03 = TL.s("c4_03")
    t_c4_04 = TL.s("c4_04")
    t_c4_05 = TL.s("c4_05")

    if t < t_c4_05 - 0.12:
        cv = bg("wall_street_floor").copy()
        draw_place_only(cv, "WALL STREET · 2007 - 2012 · VALOR ESTANCADO", t, t_c4_03, border=GOLD)
        # Gráfico plano estancado alrededor de US$10.000 millones
        flat_pts = [0.34, 0.36, 0.33, 0.35, 0.34, 0.36, 0.35, 0.34, 0.35]
        draw_stock_chart(cv, 108, 42, 264, 96, flat_pts, progress=1.0, col_up=GOLD, col_down=GOLD)
        if t < t_c4_04 - 0.1:
            draw_text(cv, "WALL STREET: «CUESTA MUCHO Y NO DA PLATA»", 240, 52, "silk", 8, STOCK_RED, align="center")
        else:
            draw_text(cv, "VALOR QUIETO DURANTE AÑOS:", 240, 52, "silk", 8, CREAM, align="center")
            draw_text(cv, "US$ 10.000 MILLONES", 240, 70, "press", 8, GOLD, align="center")

        char(cv, "analyst_a", 156, 248, t, scale=2, arms="cross", look=1, mood="sad")
        char(cv, "analyst_b", 324, 248, t, scale=2, arms="shrug", look=-1, mood="sad")
        return vignette(cv, 0.36)

    # c4_05: Un puente de luz verde que avanza sobre la niebla hacia una ciudad que todavía no existía
    cv = bg("green_bridge_fog").copy()
    draw_place_only(cv, "UN PUENTE HACIA EL FUTURO", t, t_c4_05, border=GPU_GREEN)
    a, dy = pop(t, t_c4_05 - 0.05)
    window(cv, 98, 44 + dy, 284, 86, fill=(12, 26, 20), border=GPU_GREEN, alpha=0.95)
    draw_text(cv, "LA APUESTA SILENCIOSA", 240, 54 + dy, "press", 8, GPU_GREEN, align="center")
    draw_text(cv, "ERA UN PUENTE HACIA UNA CIUDAD", 240, 76 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "QUE TODAVÍA NO EXISTÍA.", 240, 96 + dy, "press", 8, GOLD, align="center")
    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.s("c4_00") - 0.15, c4_card),
        (TL.s("c4_01"), c4_s01_cuda_and_science,
         lambda t: cam_push(t, TL.s("c4_01"), TL.s("c4_03"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c4_03"), c4_s02_wallstreet_and_bridge,
         lambda t: cam_push(t, TL.s("c4_03"), TL.s("c5_00"), 1.0, 1.03, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("c4_00"), TL.e("c4_05") - TL.s("c4_00"), (164.81, 207.65, 246.94), amp=0.016)


def sfx(A):
    A.fx_pop(TL.s("c4_01") + 0.15, 0.05)
    A.fx_chime(TL.s("c4_02") + 0.2, 0.06)
    A.fx_thud(TL.s("c4_03") + 0.15, 0.06)
    A.fx_sweep(TL.s("c4_05") + 0.1, 0.45, 180, 420, 0.06)
