"""Capítulo 9: ¿El final? (caída de US$1,7 billones vs ventas récord de US$108.000M, el calendario de 30 días, regreso a la mesa vacía de 1993, la pregunta final y CTA de comentarios antes del cierre de Pixeloide Studios)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c9_card = make_card(9, ["¿EL FINAL?"], "1993 - 2026 · TREINTA DÍAS")

T_END = TL.e("c9_06") + 2.8


def c9_s01_drop_vs_sales_and_calendar(t):
    """c9_01..c9_03: –US$1,7 billones en seis semanas -> centros de datos vendiendo US$108.000 millones -> el calendario de 30 días en la pared."""
    t0 = TL.s("c9_01")
    t_c9_02 = TL.s("c9_02")
    t_c9_03 = TL.s("c9_03")

    if t < t_c9_02 - 0.12:
        cv = bg("wall_street_floor").copy()
        draw_place_only(cv, "OCTUBRE - NOVIEMBRE 2026 · LA CAÍDA EN BOLSA", t, t0, border=STOCK_RED)
        pts_crash = [0.95, 0.86, 0.78, 0.68, 0.56, 0.44, 0.34]
        draw_stock_chart(cv, 98, 42, 284, 104, pts_crash, progress=clamp01((t - t0) / 2.2),
                         col_up=STOCK_RED, col_down=STOCK_RED, split_idx=0)
        draw_text(cv, "SEIS SEMANAS SEGUIDAS EN ROJO", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "–US$ 1,7 BILLONES DE VALOR", 240, 72, "press", 8, STOCK_RED, align="center")
        draw_text(cv, "DESDE EL PICO DE OCTUBRE DE 2026", 240, 92, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.38)

    if t < t_c9_03 - 0.12:
        # c9_02: Los servidores siguen encendidos: US$108.000 millones de ventas en el último trimestre
        cv = bg("datacenter_gold").copy()
        draw_place_only(cv, "CENTROS DE DATOS · VENTAS RÉCORD", t, t_c9_02, border=GPU_GREEN)
        draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=2.0)
        a, dy = pop(t, t_c9_02 - 0.05)
        window(cv, 98, 42 + dy, 284, 96, fill=(14, 24, 20), border=GPU_GREEN, alpha=0.96)
        draw_text(cv, "PERO LOS CHIPS SE SIGUEN VENDIENDO", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
        draw_text(cv, "ÚLTIMO TRIMESTRE INFORMADO:", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$ 108.000 MILLONES EN VENTAS", 240, 94 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "CASI EL DOBLE QUE UN AÑO ANTES", 240, 114 + dy, "silk", 8, SOFT_GRAY, align="center")
        return vignette(cv, 0.32)

    # c9_03: El calendario de 30 días en la pared: la frase que repitió durante 33 años
    cv = bg("empty_ceo_office").copy()
    draw_place_only(cv, "LA FRASE DE LOS 33 AÑOS", t, t_c9_03, border=GOLD)
    draw_nvidia_prop(cv, 198, 248, kind="ceo_desk", t=t, state=1.0)
    draw_calendar_30(cv, 352, 146, t, scale=1, tear_p=0.0, highlight_30=True)

    a, dy = pop(t, t_c9_03 - 0.05)
    window(cv, 98, 40 + dy, 284, 96, fill=(18, 20, 30), border=GOLD, alpha=0.96)
    draw_text(cv, "DURANTE 33 AÑOS REPITIÓ LO MISMO:", 240, 50 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "«A TREINTA DÍAS DE QUEBRAR»", 240, 70 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "AUN CUANDO VALÍA BILLONES DE DÓLARES:", 240, 92 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "SU FORMA DE NO RELAJARSE NUNCA", 240, 110 + dy, "silk", 8, GPU_GREEN, align="center")
    return vignette(cv, 0.36)


def c9_s02_empty_diner_and_question(t):
    """c9_04..c9_05: Regreso al restaurante de ruta de 1993 con la mesa vacía, tres tazas humeando y el chip verde parpadeando sobre la servilleta."""
    t_c9_04 = TL.s("c9_04")
    t_c9_05 = TL.s("c9_05")

    cv = bg("diner_1993").copy()
    draw_place_only(cv, "SAN JOSÉ, CALIFORNIA · LA MESA DE 1993", t, t_c9_04, border=GOLD)
    # Mesa vacía (sin los fundadores) con las 3 tazas de café humeando y el chip brillando sobre la servilleta
    draw_nvidia_prop(cv, 240, 248, kind="diner_table", t=t, state=2.0)

    if t < t_c9_05 - 0.12:
        a, dy = pop(t, t_c9_04 - 0.05)
        window(cv, 98, 42 + dy, 284, 88, fill=(22, 16, 26), border=GOLD, alpha=0.95)
        draw_text(cv, "HOY NVIDIA TIENE LAS FÁBRICAS Y EL SOFTWARE", 240, 52 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PERO POR PRIMERA VEZ DESDE AQUELLA MESA,", 240, 72 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "NO TIENE A SU FUNDADOR", 240, 92 + dy, "press", 8, STOCK_RED, align="center")
        return vignette(cv, 0.36)

    # c9_05: La pregunta final con el destello verde del chip sobre la servilleta
    a, dy = pop(t, t_c9_05 - 0.05)
    window(cv, 98, 42 + dy, 284, 96, fill=(14, 24, 20), border=GPU_GREEN, alpha=0.96)
    draw_text(cv, "LA PREGUNTA QUE QUEDA ABIERTA:", 240, 52 + dy, "silk", 8, GOLD, align="center")
    draw_text(cv, "¿ES ESTE EL FINAL DE NVIDIA?", 240, 74 + dy, "press", 8, CREAM, align="center")
    draw_text(cv, "¿O SOLO OTRO DE ESOS TREINTA DÍAS?", 240, 96 + dy, "press", 8, GPU_GREEN, align="center")
    sparkle(cv, 249, 210, t * 2.5, 4, GPU_GREEN)
    return vignette(cv, 0.36)


def c9_s03_comment_cta(t):
    """c9_06..T_END: Invitación al público a comentar qué historia quieren ver en el próximo episodio antes del cierre de Pixeloide Studios."""
    t0 = TL.s("c9_06")
    cv = bg("diner_1993").copy()
    draw_place_only(cv, "PIXELOIDE STUDIOS · PRÓXIMO EPISODIO", t, t0, border=GPU_GREEN)
    draw_nvidia_prop(cv, 240, 248, kind="diner_table", t=t, state=2.0)
    draw_calendar_30(cv, 108, 152, t, scale=1, tear_p=0.0, highlight_30=True)
    draw_gpu_card(cv, 372, 174, t, scale=1, fan_speed=14.0, led_col=GPU_GREEN)

    a, dy = pop(t, t0 - 0.05)
    window(cv, 98, 40 + dy, 284, 98, fill=(14, 22, 28), border=GOLD, alpha=0.96)
    draw_text(cv, "¿QUÉ OPINÁS VOS?", 240, 50 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "¿QUÉ OTRA HISTORIA TE GUSTARÍA VER", 240, 72 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 90 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "¡DEJALO EN LOS COMENTARIOS!", 240, 110 + dy, "press", 8, GPU_GREEN, align="center")
    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.s("c9_00") - 0.15, c9_card),
        (TL.s("c9_01"), c9_s01_drop_vs_sales_and_calendar,
         lambda t: cam_push(t, TL.s("c9_01"), TL.s("c9_04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c9_04"), c9_s02_empty_diner_and_question,
         lambda t: cam_push(t, TL.s("c9_04"), TL.s("c9_06"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c9_06"), c9_s03_comment_cta,
         lambda t: cam_push(t, TL.s("c9_06"), T_END, 1.0, 1.025, (240, 135), (240, 135))),
    ]


def music(A):
    A.add_pad(TL.s("c9_00"), T_END - TL.s("c9_00"), (146.83, 174.61, 220.0), amp=0.015)


def sfx(A):
    A.fx_thud(TL.s("c9_01") + 0.15, 0.06)
    A.fx_chime(TL.s("c9_02") + 0.2, 0.06)
    A.fx_pop(TL.s("c9_04") + 0.2, 0.05)
    A.fx_sparkle(TL.s("c9_05") + 0.35, 0.06)
    A.fx_chime(TL.s("c9_06") + 0.2, 0.06)
