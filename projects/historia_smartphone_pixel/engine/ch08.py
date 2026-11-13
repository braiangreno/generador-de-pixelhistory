"""Capítulo 8: Una llamada al rival (1 kg vs 200 g, 1 millón de veces el Apolo, 7.000 millones de líneas, regreso a 1973 y CTA de comentarios)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from i18n import tr as i18n_tr


def c8_s01_brick_vs_today_and_apollo(t):
    """c8_01..c8_02: El ladrillo (>1 kg) vs hoy (200 g) y más de un millón de veces la memoria del Apolo 11."""
    t0 = TL.s("c8_01")
    t_c8_02 = TL.s("c8_02")

    cv = bg("motorola_lab_1973").copy()
    draw_place_only(cv, "1973 VS HOY · DEL LADRILLO AL BOLSILLO", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    draw_dynatac_workbench(cv, 190, 248, t, open_battery=False, charging=False)
    if t < t_c8_02:
        char(cv, "cooper_1973", 124, 248, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, "pedestrian_modern", 336, 248, t, scale=2, arms="hold", facing=-1, look=-1, mood="happy")
        draw_held_smartphone(cv, 336, 248, t, glow_col=TESLA_CYAN, facing=-1)

        window(cv, 118, 44, 244, 96, fill=(16, 24, 42), border=GOLD)
        draw_text(cv, "1973: > 1.000 GRAMOS", 240, 56, "press", 8, AMBER, align="center")
        draw_text(cv, "SOLO SERVÍA PARA HABLAR", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "HOY: ~ 200 GRAMOS", 240, 96, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CINCO VECES MÁS LIVIANO", 240, 114, "silk", 8, CHALK_GREEN, align="center")
    else:
        char(cv, "astronaut", 136, 248, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, "pedestrian_modern", 336, 248, t, scale=2, arms="hold", facing=-1, look=-1, mood="happy")
        draw_held_smartphone(cv, 336, 248, t, glow_col=TESLA_CYAN, facing=-1)

        window(cv, 116, 42, 248, 102, fill=(14, 22, 42), border=TESLA_CYAN)
        draw_text(cv, "COMPUTADORA DEL APOLO 11 (1969)", 240, 52, "silk", 8, GOLD, align="center")
        draw_text(cv, "TU TELÉFONO TIENE:", 240, 72, "silk", 8, CREAM, align="center")
        draw_text(cv, "+1.000.000 X", 240, 90, "press", 16, TESLA_CYAN, align="center")
        draw_text(cv, "MÁS MEMORIA QUE EL APOLO", 240, 118, "silk", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.35)


def c8_s02_global_lines(t):
    """c8_03..c8_04: +7.000 millones de líneas de smartphone y todo lo que hacemos hoy con él."""
    t0 = TL.s("c8_03")
    t_c8_04 = TL.s("c8_04")

    cv = bg("modern_street_2026").copy()
    draw_place_only(cv, "PLANETA CONECTADO · 2026", t, t0, border=TESLA_CYAN)

    char(cv, "pedestrian_modern", 162, 248, t, scale=2, arms="hold", look=1, mood="happy")
    draw_held_smartphone(cv, 162, 248, t, glow_col=TESLA_CYAN, facing=1)
    char(cv, "indie_dev", 318, 248, t, scale=2, arms="hold", facing=-1, look=-1, mood="happy")
    draw_held_smartphone(cv, 318, 248, t, glow_col=GOLD, facing=-1)

    window(cv, 116, 42, 248, 104, fill=(14, 24, 44), border=GOLD if t >= t_c8_04 else TESLA_CYAN)
    if t < t_c8_04:
        draw_text(cv, "+7.000 MILLONES DE LÍNEAS", 240, 54, "press", 8, GOLD, align="center")
        draw_honeycomb_grid(cv, 240, 92, r_cell=11, ring=1, t=t, color=TESLA_CYAN, highlight_idx=int(t * 3) % 7)
        draw_text(cv, "MÁS LÍNEAS QUE PERSONAS EN LA TIERRA", 240, 124, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "EN TU BOLSILLO HOY:", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "ESCRIBIR · MIRAR · PAGAR · GPS", 240, 72, "press", 8, GOLD, align="center")
        draw_text(cv, "LLAMAR ES APENAS UNA PARTE", 240, 98, "silk", 8, CREAM, align="center")
        draw_signal_bars(cv, 224, 134, bars_lit=4, scale=2, color=CHALK_GREEN)

    return vignette(cv, 0.34)


def c8_s03_finale_match_cut(t):
    """c8_05..c8_06: Regreso a la vereda de Nueva York en 1973 -> La primera llamada fue para presumir. Algunas cosas no cambiaron."""
    t0 = TL.s("c8_05")
    t_c8_06 = TL.s("c8_06")

    cv = bg("nyc_sixth_ave_1973").copy()
    draw_place_only(cv, "SEXTA AVENIDA · NUEVA YORK (1973 -> 2026)", t, t0, border=GOLD)

    # Cooper en 1973 a la izquierda con el ladrillo y usuario moderno a la derecha con su smartphone
    char(cv, "cooper_1973", 156, 248, t, scale=2, arms="phone_r", look=1, mood="happy")
    draw_held_brick(cv, 156, 248, t, waves=True, facing=1)

    char(cv, "pedestrian_modern", 324, 248, t, scale=2, arms="hold", facing=-1, look=-1, mood="happy")
    draw_held_smartphone(cv, 324, 248, t, glow_col=TESLA_CYAN, facing=-1)

    window(cv, 116, 44, 248, 96, fill=(18, 22, 38), border=GOLD)
    if t < t_c8_06 - 0.1:
        draw_text(cv, "NUEVA YORK · 3 DE ABRIL DE 1973", 240, 54, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "UN LADRILLO EN LA OREJA", 240, 76, "press", 8, CREAM, align="center")
        draw_text(cv, "LLAMANDO A SU RIVAL", 240, 100, "press", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c8_06 - 0.1)
        draw_text(cv, "LA PRIMERA LLAMADA FUE PARA PRESUMIR.", 240, 58, "silk", 8, CREAM, align="center")
        draw_text(cv, "ALGUNAS COSAS", 240, 82, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "NO CAMBIARON.", 240, 104, "press", 8, GOLD, align="center")

    return vignette(cv, 0.35)


def c8_s04_comment_cta(t):
    """c8_07: Llamado a la acción final antes de la placa de Pixeloide Studios: invita a comentar el próximo episodio."""
    t0 = TL.s("c8_07") - 0.20
    t_vo = TL.s("c8_07")
    t_end_vo = TL.e("c8_07")

    cv = bg("modern_street_2026").copy()
    cv = grade(cv, mul=(0.65, 0.72, 0.88))
    d = ImageDraw.Draw(cv)

    # Ventana RPG principal (x=118..362, w=244 -> cabe 1:1 en 16:9 y en 9:16 sin escalar)
    a, dy = pop(t, t0, dur=0.32)
    window(cv, 118, 28 + dy, 244, 122, fill=(14, 20, 38), border=GOLD)

    d.rectangle([144, 35 + dy, 336, 49 + dy], fill=(32, 44, 72, 255), outline=(*TESLA_CYAN, 255))
    draw_text(cv, "PRÓXIMO EPISODIO · TU IDEA", 240, 38 + dy, "silk", 8, GOLD, align="center")

    draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 70 + dy, "press", 8, TESLA_CYAN, align="center")

    d.rectangle([126, 86 + dy, 354, 108 + dy], fill=(8, 12, 24, 255), outline=(*GOLD, 255))
    d.rectangle([132, 91 + dy, 144, 100 + dy], fill=(*TESLA_CYAN, 255))
    d.polygon([(135, 100 + dy), (139, 100 + dy), (135, 104 + dy)], fill=(*TESLA_CYAN, 255))

    full_msg = i18n_tr("DEJALO EN LOS COMENTARIOS...")
    typed_p = clamp01((t - t_vo) / 2.2)
    n_chars = max(1, int(len(full_msg) * typed_p))
    cur = "|" if int(t * 4) % 2 == 0 else " "
    draw_text(cv, full_msg[:n_chars] + cur, 150, 93 + dy, "silk", 8, GOLD, align="left")

    draw_text(cv, "¿CIENCIA? · ¿VIDEOJUEGOS? · ¿CINE?", 240, 115 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "¡TE LEEMOS ABAJO!", 240, 132 + dy, "press", 8, CHALK_GREEN, align="center")

    # Martin Cooper saludando junto a la mesa con el DynaTAC
    char(cv, "cooper_1973", 164, 248, t, scale=2, arms="wave", look=1, mood="happy",
         talk=talk_v(t, t_vo <= t <= t_end_vo))
    draw_dynatac_workbench(cv, 308, 248, t, open_battery=False, charging=False)

    cv = vignette(cv, 0.32)
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c8_07") + 2.2

SCENES = [
    (TL.s("c8_00") - 0.15, TL.s("c8_01"), make_card(8, ["UNA LLAMADA", "AL RIVAL"], "1973 – 2026 · EL MUNDO EN EL BOLSILLO")),
    (TL.s("c8_01") - 0.15, TL.s("c8_03"), c8_s01_brick_vs_today_and_apollo),
    (TL.s("c8_03") - 0.15, TL.s("c8_05"), c8_s02_global_lines),
    (TL.s("c8_05") - 0.15, TL.s("c8_07") - 0.20, c8_s03_finale_match_cut),
    (TL.s("c8_07") - 0.20, T_END, c8_s04_comment_cta),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    t0 = TL.s("c8_00")
    t_end_vo = TL.e("c8_07")
    A.add_pad(t0, t_end_vo - t0 + 1.2, [130.81, 196.0, 261.63, 329.63], amp=0.042)


def sfx(A):
    A.fx_pop(TL.s("c8_01"), 0.09)
    A.fx_chime(TL.word("c8_02", "Apolo"), 0.10)
    A.fx_sparkle(TL.s("c8_03"), 0.10)
    A.fx_chime(TL.s("c8_06"), 0.12)
    A.fx_pop(TL.s("c8_07"), 0.10)
