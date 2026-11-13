"""Apertura: Sexta Avenida 1973 (s01..s05) + Capítulo 1: El ladrillo (c1_00..c1_07)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def s01_sixth_ave_opening(t):
    """s01..s02: Cooper en la Sexta Avenida de Nueva York (abril de 1973) levanta el ladrillo y marca."""
    t_s01 = TL.s("s01")
    t_s02 = TL.s("s02")
    t_lev = TL.word("s02", "Levanta")
    t_vuelta = TL.word("s02", "vuelta")

    cv = bg("nyc_sixth_ave_1973").copy()
    draw_place_only(cv, "NUEVA YORK · 3 DE ABRIL DE 1973", t, t_s01, border=AMBER)

    # Cooper camina en s01 y se detiene a probar el ladrillo
    x_coop, w_coop = walk(t, t_s01, t_s01 + 2.4, 148, 224)
    raising_brick = t >= t_lev - 0.15
    coop_arms = "phone_r" if raising_brick else "hold"

    # Peatones de 1973 que caminan y se dan vuelta sorprendidos en s02
    turned = t >= t_vuelta - 0.2
    char(cv, "passerby_73_a", 132, 248, t, scale=2, arms="down",
         facing=1 if turned else -1, look=1 if turned else -1,
         mood="surprised" if turned else "neutral")
    char(cv, "passerby_73_b", 336, 248, t, scale=2, arms="down",
         facing=-1 if turned else 1, look=-1 if turned else 1,
         mood="surprised" if turned else "neutral")

    char(cv, "cooper_1973", x_coop, 248, t, scale=2, walk=w_coop,
         arms=coop_arms, look=1, mood="happy" if raising_brick else "neutral")

    if raising_brick:
        draw_held_brick(cv, x_coop, 248, t, waves=(t >= t_s02 + 1.2), facing=1)

    if turned:
        draw_text(cv, "!", 132, 134, "press", 16, GOLD, align="center")
        draw_text(cv, "?", 336, 134, "press", 16, TESLA_CYAN, align="center")

    if t >= t_s02:
        a, dy = pop(t, t_s02)
        window(cv, 120, 46 + dy, 240, 42, fill=(24, 18, 14), border=GOLD, alpha=0.94)
        draw_text(cv, "MOTOROLA DYNATAC · PROTOTIPO", 240, 54 + dy, "silk", 8, GOLD, align="center")
        draw_text(cv, "HABLANDO EN PLENA CALLE", 240, 70 + dy, "press", 8, CREAM, align="center")

    return vignette(cv, 0.35)


def s03_rival_call_and_title(t):
    """s03..s05: Llamada a Joel Engel (pantalla dividida / oficina rival) -> remate y título del episodio."""
    t_s03 = TL.s("s03")
    t_joel = TL.word("s03", "Joel")
    t_s04 = TL.s("s04")
    t_s05 = TL.s("s05")

    if t < t_s05 - 0.15:
        cv = bg("nyc_sixth_ave_1973").copy()
        draw_place_only(cv, "SEXTA AVENIDA -> BELL LABS", t, t_s03, border=TESLA_CYAN)

        # Cooper a la izquierda en la vereda con el ladrillo en la oreja
        char(cv, "cooper_1973", 148, 248, t, scale=2, arms="phone_r", look=1, mood="happy",
             talk=talk_v(t, t_s03 <= t < t_s04))
        draw_held_brick(cv, 148, 248, t, waves=True, facing=1)

        # A la derecha, Joel Engel en su escritorio con teléfono fijo de disco
        if t >= t_joel - 0.35:
            draw_rotary_phone_table(cv, 308, 248, t, ringing=(t < t_joel + 0.5), off_hook=(t >= t_joel + 0.5))
            char(cv, "engel_bell", 348, 248, t, scale=2,
                 arms="think" if t >= t_joel + 0.5 else "down",
                 facing=-1, look=-1, mood="worried")

        a, dy = pop(t, t_s03)
        window(cv, 118, 44 + dy, 244, 52, fill=(16, 22, 38), border=GOLD if t >= t_s04 else TESLA_CYAN)
        if t < t_s04 - 0.1:
            draw_text(cv, "DESTINATARIO: JOEL ENGEL", 240, 52 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "JEFE DEL EQUIPO RIVAL (BELL LABS)", 240, 72 + dy, "silk", 8, CREAM, align="center")
        else:
            draw_text(cv, "3 DE ABRIL DE 1973:", 240, 52 + dy, "silk", 8, TESLA_CYAN, align="center")
            draw_text(cv, "FUE PARA PRESUMIR", 240, 70 + dy, "press", 8, GOLD, align="center")

        if t >= t_s04 - 0.1:
            bubble(cv, "«TE LLAMO DESDE LA CALLE»", 148, 134, fill=(255, 246, 210))

        return vignette(cv, 0.36)

    # s05: Placa de título de apertura con el panal celular y las 4 barras de señal
    cv = bg("modern_street_2026").copy()
    cv = grade(cv, mul=(0.55, 0.65, 0.85))
    draw_place_only(cv, "MÁS LÍNEAS QUE PERSONAS EN EL PLANETA", t, t_s05, border=TESLA_CYAN)

    a, dy = pop(t, t_s05 - 0.1)
    window(cv, 116, 48 + dy, 248, 122, fill=(12, 18, 36), border=GOLD, alpha=0.95)
    draw_honeycomb_grid(cv, 136, 134 + dy, r_cell=6, ring=1, t=t, color=TESLA_CYAN, highlight_idx=int(t * 3) % 7)
    draw_signal_bars(cv, 332, 144 + dy, bars_lit=4, scale=1, color=GOLD)
    draw_text(cv, "UNA LLAMADA", 240, 62 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(1, int((t - t_s05 + 0.2) * 24)))
    draw_text(cv, "AL RIVAL", 240, 88 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s05 - 0.15) * 24)))
    draw_text(cv, "LA HISTORIA DEL SMARTPHONE", 240, 118 + dy, "silk", 8, TESLA_CYAN, align="center",
              reveal=max(0, int((t - t_s05 - 0.45) * 32)))
    draw_text(cv, "1947 -> 2026", 240, 136 + dy, "press", 8, CREAM, align="center",
              reveal=max(0, int((t - t_s05 - 0.65) * 32)))
    return vignette(cv, 0.35)


# ===========================================================================
# CAPÍTULO 1: EL LADRILLO (c1_01 .. c1_07)
# ===========================================================================

def c1_s01_car_phone_vs_cooper(t):
    """c1_01..c1_02: Teléfono de auto ocupando el baúl vs la visión de Martin Cooper en Motorola."""
    t0 = TL.s("c1_01")
    t_c1_02 = TL.s("c1_02")
    cv = bg("motorola_lab_1973").copy()
    draw_place_only(cv, "MOTOROLA · SCHAUMBURG, ILLINOIS", t, t0, border=AMBER)
    d = ImageDraw.Draw(cv)

    if t < t_c1_02 - 0.1:
        # Panel central mostrando un auto de los 70 con el baúl lleno por el equipo de radio y batería
        window(cv, 118, 46, 244, 118, fill=(20, 26, 40), border=AMBER)
        draw_text(cv, "TELÉFONO DE AUTO (AÑOS 70)", 240, 54, "press", 8, GOLD, align="center")
        # Silueta de sedán clásico con baúl abierto
        d.rectangle([148, 96, 316, 116], fill=(168, 72, 48, 255), outline=(*INK, 255))
        d.polygon([(178, 96), (196, 78), (268, 78), (286, 96)], fill=(168, 72, 48, 255), outline=(*INK, 255))
        for wx in (176, 288):
            d.ellipse([wx - 10, 110, wx + 10, 130], fill=(28, 28, 34, 255), outline=(*INK, 255))
        # Caja pesada de radio en el baúl (x=284..314)
        d.rectangle([282, 82, 314, 108], fill=(72, 82, 96, 255), outline=(*GOLD, 255))
        draw_text(cv, "BAÚL LLENO + MUCHA BATERÍA", 240, 140, "silk", 8, CHALK_RED, align="center")
        char(cv, "motorola_eng", 156, 248, t, scale=2, arms="shrug", look=1, mood="worried")
        return vignette(cv, 0.36)

    # c1_02: Martin Cooper propone un teléfono de mano para hablar desde cualquier lado
    window(cv, 118, 46, 244, 96, fill=(16, 28, 46), border=TESLA_CYAN)
    draw_text(cv, "LA IDEA DE MARTIN COOPER:", 240, 54, "silk", 8, TESLA_CYAN, align="center")
    draw_text(cv, "NO LLAMAR DESDE UN AUTO", 240, 74, "press", 8, CHALK_RED, align="center")
    draw_text(cv, "HABLAR DESDE CUALQUIER LADO", 240, 96, "press", 8, GOLD, align="center")
    draw_text(cv, "PROYECTO DYNATAC (1972-1973)", 240, 118, "silk", 8, CREAM, align="center")

    char(cv, "cooper_1973", 172, 248, t, scale=2, arms="point", look=1, mood="happy",
         talk=talk_v(t, True))
    char(cv, "motorola_eng", 308, 248, t, scale=2, arms="note", facing=-1, look=-1, mood="neutral")
    return vignette(cv, 0.36)


def c1_s02_prototype_specs(t):
    """c1_03..c1_05: El prototipo DynaTAC en la mesa: >1 kg de batería, 3 funciones, 30 min hablar vs 10 h carga."""
    t_c1_03 = TL.s("c1_03")
    t_c1_04 = TL.s("c1_04")
    t_c1_05 = TL.s("c1_05")

    cv = bg("motorola_lab_1973").copy()
    draw_place_only(cv, "LABORATORIO MOTOROLA · 1973", t, t_c1_03, border=GOLD)

    # Mesa de trabajo apoyada en el suelo con el prototipo DynaTAC
    draw_dynatac_workbench(cv, 240, 248, t,
                           open_battery=(t < t_c1_04),
                           charging=(t >= t_c1_05))
    char(cv, "cooper_1973", 144, 248, t, scale=2,
         arms="point" if t < t_c1_05 else "hips", look=1, mood="happy",
         talk=talk_v(t, t >= t_c1_05))
    char(cv, "motorola_eng", 336, 248, t, scale=2,
         arms="work" if t < t_c1_04 else "down", facing=-1, look=-1)

    if t < t_c1_04:
        window(cv, 118, 44, 244, 88, fill=(22, 26, 42), border=GOLD)
        draw_text(cv, "PESO: MÁS DE 1 KILO", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "CASI TODO EL INTERIOR ERA BATERÍA", 240, 76, "silk", 8, CREAM, align="center")
        d = ImageDraw.Draw(cv)
        d.rectangle([144, 96, 336, 114], fill=(34, 38, 52, 255), outline=(*INK, 255))
        d.rectangle([146, 98, 316, 112], fill=(238, 184, 52, 255))
        draw_text(cv, "85% BATERÍA", 240, 101, "silk", 8, INK, align="center", outline=None, shadow=False)
    elif t < t_c1_05:
        window(cv, 118, 44, 244, 92, fill=(16, 26, 44), border=TESLA_CYAN)
        draw_text(cv, "SIN PANTALLA · SOLO 3 COSAS:", 240, 54, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "1. MARCAR", 240, 74, "press", 8, GOLD, align="center")
        draw_text(cv, "2. HABLAR", 240, 92, "press", 8, CREAM, align="center")
        draw_text(cv, "3. ESCUCHAR", 240, 110, "press", 8, CHALK_GREEN, align="center")
    else:
        window(cv, 118, 44, 244, 92, fill=(24, 20, 36), border=AMBER)
        draw_text(cv, "BATERÍA DEL PROTOTIPO:", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "HABLAR: 30 MINUTOS", 240, 72, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "CARGAR: 10 HORAS", 240, 92, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "«NADIE AGUANTABA 30 MIN EL LADRILLO»", 240, 114, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.36)


def c1_s03_store_1983_and_punchline(t):
    """c1_06..c1_07: Llega a las tiendas en 1983 a US$3.995 -> De llamar a un lugar a llamar a una persona."""
    t_c1_06 = TL.s("c1_06")
    t_c1_07 = TL.s("c1_07")
    t_pers = TL.word("c1_07", "persona")

    cv = bg("storefront_simon_1994").copy()
    draw_place_only(cv, "TIENDAS COMERCIALES · 1983", t, t_c1_06, border=GOLD)

    draw_dynatac_workbench(cv, 240, 248, t, open_battery=False, charging=False)
    char(cv, "cooper_1973", 148, 248, t, scale=2, arms="offer", look=1, mood="happy")

    if t < t_c1_07 - 0.1:
        a, dy = pop(t, t_c1_06)
        window(cv, 118, 44 + dy, 244, 94, fill=(18, 24, 42), border=GOLD)
        draw_text(cv, "MOTOROLA DYNATAC 8000X (1983)", 240, 54 + dy, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "US$ 3.995", 240, 74 + dy, "press", 16, GOLD, align="center")
        draw_text(cv, "HOY SERÍAN MÁS DE US$ 10.000", 240, 108 + dy, "silk", 8, CREAM, align="center")
    else:
        a, dy = pop(t, t_c1_07 - 0.1)
        window(cv, 116, 44 + dy, 248, 96, fill=(14, 22, 38), border=TESLA_CYAN)
        draw_text(cv, "HASTA ENTONCES:", 240, 54 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "LLAMABAS A UN LUGAR", 240, 72 + dy, "press", 8, AMBER, align="center")
        if t >= t_pers - 0.6:
            draw_text(cv, "DESDE ENTONCES:", 240, 96 + dy, "silk", 8, TESLA_CYAN, align="center")
            draw_text(cv, "LLAMAS A UNA PERSONA", 240, 114 + dy, "press", 8, GOLD, align="center")

    return vignette(cv, 0.36)


def scenes():
    return [
        (0.0, s01_sixth_ave_opening,
         lambda t: cam_push(t, 0.0, TL.s("s03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("s03") - 0.15, s03_rival_call_and_title,
         lambda t: cam_push(t, TL.s("s03"), TL.s("c1_00"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_00") - 0.15, make_card(1, ["EL LADRILLO"], "1973 – 1983 · NUEVA YORK Y MOTOROLA"),
         None, "ch01"),
        (TL.s("c1_01") - 0.15, c1_s01_car_phone_vs_cooper,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_03") - 0.15, c1_s02_prototype_specs,
         lambda t: cam_push(t, TL.s("c1_03"), TL.s("c1_06"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_06") - 0.15, c1_s03_store_1983_and_punchline,
         lambda t: cam_push(t, TL.s("c1_06"), TL.s("c2_00"), 1.0, 1.035, (240, 135)), "ch01"),
    ]


def music(A):
    t0 = 0.0
    t_end = TL.s("c2_00")
    A.add_pad(t0, t_end - t0, [110.0, 164.81, 220.0], amp=0.036)


def sfx(A):
    A.fx_pop(TL.word("s02", "Levanta"), 0.08)
    A.fx_chime(TL.s("s04"), 0.10)
    A.fx_sparkle(TL.s("s05"), 0.10)
    A.fx_pop(TL.s("c1_03"), 0.08)
    A.fx_chime(TL.s("c1_07"), 0.10)
