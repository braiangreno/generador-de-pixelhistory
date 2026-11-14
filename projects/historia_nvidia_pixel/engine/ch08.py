"""Capítulo 8: La semana (noviembre de 2026: The New York Times y Reuters, la carta, la renuncia de Jensen Huang el 12 de noviembre, Colette Kress interina y la citación del Congreso para el 1 de diciembre)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c8_card = make_card(8, ["LA SEMANA"], "NOVIEMBRE DE 2026 · LA RENUNCIA")


def c8_s01_doubts_and_newspapers(t):
    """c8_01..c8_04: Dudas desde octubre -> fin de semana de noviembre (NYT) -> carta y junta -> más notas (NYT y Reuters)."""
    t0 = TL.s("c8_01")
    t_c8_02 = TL.s("c8_02")
    t_c8_03 = TL.s("c8_03")
    t_c8_04 = TL.s("c8_04")

    cv = bg("boardroom_night").copy()
    draw_place_only(cv, "NOVIEMBRE DE 2026 · SALA DE DIRECTORIO", t, t0, border=STOCK_RED)

    if t < t_c8_02 - 0.12:
        pts_down = [0.92, 0.84, 0.76, 0.68, 0.58, 0.48]
        draw_stock_chart(cv, 98, 42, 284, 96, pts_down, progress=clamp01((t - t0) / 2.2),
                         col_up=STOCK_RED, col_down=STOCK_RED, split_idx=0)
        draw_text(cv, "DESDE FINES DE OCTUBRE DE 2026:", 240, 50, "silk", 8, CREAM, align="center")
        draw_text(cv, "TEMOR POR LA DEUDA EN CHIPS DE IA", 240, 68, "press", 8, STOCK_RED, align="center")
        char(cv, "analyst_a", 148, 248, t, scale=2, arms="cross", look=1, mood="sad")
        char(cv, "analyst_b", 332, 248, t, scale=2, arms="talk", look=-1, mood="sad")
        return vignette(cv, 0.38)

    if t < t_c8_03 - 0.12:
        # c8_02: Un diario cae sobre el escritorio (investigación del New York Times)
        draw_nvidia_prop(cv, 240, 248, kind="ceo_desk", t=t, state=1.0)
        a, dy = pop(t, t_c8_02 - 0.05)
        window(cv, 98, 40 + dy, 284, 102, fill=(24, 12, 16), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "PRIMER FIN DE SEMANA DE NOVIEMBRE", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "INVESTIGACIÓN DE THE NEW YORK TIMES:", 240, 70 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "RELACIÓN EN AÑOS ANTERIORES CON UNA", 240, 88 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "MUJER INVESTIGADA POR EE. UU. (CHINA)", 240, 106 + dy, "silk", 8, STOCK_RED, align="center")
        return vignette(cv, 0.38)

    if t < t_c8_04 - 0.12:
        # c8_03: Carta sobre el escritorio + directorio reunido de noche
        draw_nvidia_prop(cv, 240, 248, kind="ceo_desk", t=t, state=1.0)
        char(cv, "board_member_a", 136, 248, t, scale=2, arms="cross", look=1, mood="sad")
        char(cv, "board_member_b", 344, 248, t, scale=2, arms="cross", look=-1, mood="sad")
        a, dy = pop(t, t_c8_03 - 0.05)
        window(cv, 98, 40 + dy, 284, 102, fill=(18, 22, 32), border=GOLD, alpha=0.96)
        draw_text(cv, "LA RESPUESTA DE HUANG Y LA JUNTA", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "HUANG RECONOCIÓ LA RELACIÓN EN UNA CARTA", 240, 70 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA JUNTA INVESTIGÓ CON ABOGADOS EXTERNOS:", 240, 88 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "«SIN FILTRACIÓN DE SECRETOS»", 240, 106 + dy, "press", 8, GPU_GREEN, align="center")
        return vignette(cv, 0.38)

    # c8_04: Se apilan más diarios (The New York Times y Reuters: relaciones con empleadas de la compañía)
    draw_nvidia_prop(cv, 240, 248, kind="ceo_desk", t=t, state=3.0)
    a, dy = pop(t, t_c8_04 - 0.05)
    window(cv, 98, 40 + dy, 284, 102, fill=(28, 12, 16), border=STOCK_RED, alpha=0.96)
    draw_text(cv, "LOS DÍAS SIGUIENTES: NUEVAS NOTAS", 240, 50 + dy, "press", 8, STOCK_RED, align="center")
    draw_text(cv, "THE NEW YORK TIMES Y AGENCIA REUTERS", 240, 70 + dy, "silk", 8, GOLD, align="center")
    draw_text(cv, "OTRAS RELACIONES CON EMPLEADAS,", 240, 88 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "INCLUIDA UNA SUBORDINADA DIRECTA", 240, 106 + dy, "silk", 8, STOCK_RED, align="center")
    return vignette(cv, 0.40)


def c8_s02_resignation_kress_and_congress(t):
    """c8_05..c8_08: 12 de noviembre de 2026 (renuncia tras 33 años, silla vacía y ventilador que se detiene) -> Colette Kress interina -> citación del Congreso (1 dic) -> calendario que pierde una hoja solo."""
    t_c8_05 = TL.s("c8_05")
    t_c8_06 = TL.s("c8_06")
    t_c8_07 = TL.s("c8_07")
    t_c8_08 = TL.s("c8_08")

    if t < t_c8_06 - 0.12:
        # c8_05: Oficina vacía de noche, silla vacía, saco colgado y ventilador de la GPU que se detiene
        cv = bg("empty_ceo_office").copy()
        draw_place_only(cv, "12 DE NOVIEMBRE DE 2026 · OFICINA VACÍA", t, t_c8_05, border=STOCK_RED)
        draw_nvidia_prop(cv, 210, 248, kind="ceo_desk", t=t, state=2.0)
        # Ventilador que frena hasta detenerse por completo
        dt_stop = max(0.0, t - t_c8_05)
        fan_sp = max(0.0, 12.0 * (1.0 - clamp01(dt_stop / 1.8)))
        draw_gpu_card(cv, 356, 196, t, scale=1, fan_speed=fan_sp, led_col=STOCK_RED)

        a, dy = pop(t, t_c8_05 + 0.05)
        window(cv, 98, 42 + dy, 284, 92, fill=(24, 10, 14), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "12 DE NOVIEMBRE DE 2026", 240, 52 + dy, "press", 8, STOCK_RED, align="center")
        draw_text(cv, "JENSEN HUANG RENUNCIÓ COMO CEO", 240, 74 + dy, "press", 8, CREAM, align="center")
        draw_text(cv, "DESPUÉS DE 33 AÑOS AL FRENTE DE NVIDIA", 240, 94 + dy, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.42)

    if t < t_c8_07 - 0.12:
        # c8_06: Colette Kress asume como directora interina
        cv = bg("boardroom_night").copy()
        draw_place_only(cv, "SALA DE DIRECTORIO · TRANSICIÓN DE MANDO", t, t_c8_06, border=GOLD)
        char(cv, "board_member_a", 138, 248, t, scale=2, arms="idle", look=1, mood="neutral")
        char(cv, "kress", 240, 248, t, scale=2, arms="talk", look=1, mood="neutral",
             talk=talk_v(t, t_c8_06 <= t <= TL.e("c8_06")))
        char(cv, "board_member_b", 342, 248, t, scale=2, arms="idle", look=-1, mood="neutral")

        a, dy = pop(t, t_c8_06 - 0.05)
        window(cv, 98, 42 + dy, 284, 88, fill=(18, 22, 32), border=GOLD, alpha=0.96)
        draw_text(cv, "COLETTE KRESS · DIRECTORA INTERINA", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "DIRECTORA DE FINANZAS DE LA EMPRESA", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "QUEDÓ A CARGO DE MANERA PROVISORIA", 240, 92 + dy, "silk", 8, SOFT_GRAY, align="center")
        return vignette(cv, 0.36)

    if t < t_c8_08 - 0.12:
        # c8_07: Capitolio de noche + sobre con sello oficial para declarar el 1 de diciembre
        cv = bg("capitol_dome_night").copy()
        draw_place_only(cv, "WASHINGTON D. C. · CONGRESO DE EE. UU.", t, t_c8_07, border=STOCK_RED)
        a, dy = pop(t, t_c8_07 - 0.05)
        window(cv, 98, 42 + dy, 284, 96, fill=(22, 14, 20), border=STOCK_RED, alpha=0.96)
        draw_text(cv, "TRES COMISIONES DEL CONGRESO", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "CITARON A HUANG A DECLARAR", 240, 72 + dy, "press", 8, STOCK_RED, align="center")
        draw_text(cv, "FECHA DE AUDIENCIA: 1 DE DICIEMBRE", 240, 92 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "SEGURIDAD NACIONAL Y ACCESO A CHIPS", 240, 110 + dy, "silk", 8, SOFT_GRAY, align="center")
        return vignette(cv, 0.38)

    # c8_08: El calendario en la pared pierde una hoja solo
    cv = bg("empty_ceo_office").copy()
    draw_place_only(cv, "NOVIEMBRE DE 2026 · FIN DE UNA ERA", t, t_c8_08, border=STOCK_RED)
    draw_nvidia_prop(cv, 210, 248, kind="ceo_desk", t=t, state=2.0)
    tear_p = clamp01((t - t_c8_08 - 0.15) / 1.1)
    draw_calendar_30(cv, 352, 148, t, scale=1, tear_p=tear_p, highlight_30=True)

    a, dy = pop(t, t_c8_08 - 0.05)
    window(cv, 98, 42 + dy, 284, 86, fill=(24, 10, 14), border=STOCK_RED, alpha=0.96)
    draw_text(cv, "EN UNA SOLA SEMANA", 240, 52 + dy, "press", 8, STOCK_RED, align="center")
    draw_text(cv, "LA EMPRESA MÁS VALIOSA DEL MUNDO", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "SE QUEDÓ SIN SU FUNDADOR", 240, 94 + dy, "press", 8, GOLD, align="center")
    return vignette(cv, 0.42)


def scenes():
    return [
        (TL.s("c8_00") - 0.15, c8_card),
        (TL.s("c8_01"), c8_s01_doubts_and_newspapers,
         lambda t: cam_push(t, TL.s("c8_01"), TL.s("c8_05"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c8_05"), c8_s02_resignation_kress_and_congress,
         lambda t: cam_push(t, TL.s("c8_05"), TL.s("c9_00"), 1.0, 1.03, (240, 135), (240, 134))),
    ]


def music(A):
    # Pulso grave y notas espaciadas de tensión periodística
    A.add_pad(TL.s("c8_00"), TL.e("c8_08") - TL.s("c8_00"), (110.0, 130.81, 164.81), amp=0.015)


def sfx(A):
    A.fx_thud(TL.s("c8_02") + 0.15, 0.07)
    A.fx_pop(TL.s("c8_03") + 0.15, 0.05)
    A.fx_thud(TL.s("c8_04") + 0.2, 0.06)
    A.fx_sweep(TL.s("c8_05") + 0.2, 0.06)
    A.fx_thud(TL.s("c8_07") + 0.2, 0.06)
