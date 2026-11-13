"""Capítulo 8: Valió la pena (Alunizaje de 1969, YouTube/Streaming, regreso a los surcos de Idaho y CTA comentarios)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from i18n import tr as i18n_tr
from ch01 import draw_tv_table_prop, draw_plow_prop


def c8_s01_moon_landing_1969(t):
    """c8_01..c8_02: 20 de julio de 1969 (600 millones de personas ven la Luna); Farnsworth y Pem: «Valió la pena»."""
    t0 = TL.s("c8_01")
    t_c8_02 = TL.s("c8_02")
    t_val = TL.word("c8_02", "valido")

    cv = bg("moon_landing_living_1969").copy()
    draw_place_only(cv, "20 DE JULIO DE 1969 · EL ALUNIZAJE", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 40, 244, 110, fill=(14, 20, 36), border=TESLA_CYAN, alpha=0.95)
    if t < t_c8_02 - 0.1:
        draw_text(cv, "20 DE JULIO DE 1969 · APOLO 11", 240, 48, "press", 8, GOLD, align="center")
        # Pantalla mostrando la superficie lunar y dos astronautas
        d.rectangle([168, 64, 312, 118], fill=(16, 22, 32, 255), outline=(*TESLA_CYAN, 255))
        d.rectangle([170, 100, 310, 116], fill=(164, 172, 186, 255))
        # Bandera y siluetas de astronautas en la Luna
        d.line([(240, 74), (240, 100)], fill=(240, 240, 245, 255), width=1)
        d.rectangle([241, 74, 256, 84], fill=(214, 68, 68, 255))
        d.rectangle([206, 82, 218, 100], fill=(238, 242, 248, 255), outline=(*INK, 255))
        d.rectangle([266, 82, 278, 100], fill=(224, 230, 240, 255), outline=(*INK, 255))
        draw_text(cv, "600 MILLONES DE PERSONAS EN VIVO", 240, 128, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "FARNSWORTH Y PEM EN SU LIVING", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_crt_tv(cv, 204, 66, 72, 48, t, mode="moon")
        if t >= t_val - 0.35:
            d.rectangle([134, 118, 346, 142], fill=(22, 44, 32, 255), outline=(*GOLD, 255))
            draw_text(cv, "«TODO VALIÓ LA PENA»", 240, 126, "press", 8, GOLD, align="center")
        else:
            draw_text(cv, "MIRANDO LA LUNA POR TELEVISIÓN", 240, 126, "silk", 8, CREAM, align="center")

    char(cv, "farnsworth_older", 148, 248, t, scale=2,
         arms="offer" if t >= t_c8_02 else "point", look=1, mood="happy",
         talk=talk_v(t, t >= t_val - 0.3))
    draw_tv_table_prop(cv, 240, 248, t, mode="moon")
    char(cv, "pem", 332, 248, t, scale=2, arms="wave", look=-1, mood="happy")

    return vignette(cv, 0.34)


def c8_s02_streaming_and_youtube(t):
    """c8_03..c8_04: Murió en 1971; hoy casi la mitad del tiempo en TV es streaming y la plataforma #1 es YouTube."""
    t0 = TL.s("c8_03")
    t_str = TL.word("c8_03", "streaming")
    t_c8_04 = TL.s("c8_04")

    cv = bg("moon_landing_living_1969").copy()
    draw_place_only(cv, "DE 1971 A HOY · STREAMING Y YOUTUBE", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 42, 244, 108, fill=(16, 20, 36), border=GOLD, alpha=0.95)
    if t < t_c8_04 - 0.1:
        draw_text(cv, "PHILO FARNSWORTH (1906 – 1971)", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "HOY FRENTE AL TELEVISOR:", 240, 74, "silk", 8, TESLA_CYAN, align="center")
        # Barra de progreso mostrando ~50% Streaming
        d.rectangle([144, 92, 336, 112], fill=(28, 34, 52, 255), outline=(*GOLD, 255))
        d.rectangle([146, 94, 242, 110], fill=(*CHALK_GREEN, 255))
        draw_text(cv, "CASI LA MITAD YA ES STREAMING", 240, 122, "press", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "LA PLATAFORMA MÁS VISTA EN TV:", 240, 50, "silk", 8, CREAM, align="center")
        # Icono de YouTube pixel art
        d.rectangle([206, 68, 274, 106], fill=(228, 44, 44, 255), outline=(*CREAM, 255))
        d.polygon([(232, 77), (232, 97), (252, 87)], fill=(255, 255, 255, 255))
        draw_text(cv, "YOUTUBE · ¡SÍ, ESTA!", 240, 118, "press", 8, GOLD, align="center")

    draw_tv_table_prop(cv, 240, 248, t, mode="youtube" if t >= t_c8_04 - 0.1 else "scan")
    return vignette(cv, 0.34)


def c8_s03_finale_match_cut(t):
    """c8_05..c8_06: La imagen se sigue dibujando línea por línea -> Match cut al chico en el campo arado de Idaho."""
    t0 = TL.s("c8_05")
    t_c8_06 = TL.s("c8_06")

    cv = bg("idaho_plow_field").copy()
    draw_place_only(cv, "LÍNEA POR LÍNEA · IDAHO (1920 – 2026)", t, t0, border=CHALK_GREEN)

    window(cv, 118, 42, 244, 106, fill=(14, 24, 20), border=CHALK_GREEN, alpha=0.95)
    if t < t_c8_06 - 0.1:
        draw_text(cv, "CAMBIÓ TODO, PERO LA IDEA SIGUE:", 240, 50, "silk", 8, CREAM, align="center")
        draw_scanline_beam(cv, 142, 66, 196, 52, t, rows=7, speed=1.8, color=CHALK_GREEN)
        draw_text(cv, "SE DIBUJA LÍNEA POR LÍNEA", 240, 126, "press", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "TODO EMPEZÓ CON UN CHICO", 240, 52, "press", 8, GOLD, align="center")
        draw_scanline_beam(cv, 142, 68, 196, 48, t, rows=6, speed=1.4, color=AMBER)
        draw_text(cv, "QUE MIRÓ HACIA ATRÁS MIENTRAS ARABA.", 240, 126, "silk", 8, CREAM, align="center")

    char(cv, "farnsworth_boy", 172, 248, t, scale=2, arms="point", look=1, mood="happy")
    draw_plow_prop(cv, 288, 248, t)

    return vignette(cv, 0.34)


def c8_s04_comment_cta(t):
    """c8_07: Llamado a la acción final antes de la placa de Pixeloide Studios: invita a comentar el próximo episodio."""
    t0 = TL.s("c8_07") - 0.20
    t_vo = TL.s("c8_07")
    t_end_vo = TL.e("c8_07")

    cv = bg("idaho_plow_field").copy()
    cv = grade(cv, mul=(0.75, 0.78, 0.88))
    d = ImageDraw.Draw(cv)

    # Ventana RPG principal (x=118..362, w=244 -> cabe 1:1 en 16:9 y en 9:16 sin escalar)
    a, dy = pop(t, t0, dur=0.32)
    window(cv, 118, 28 + dy, 244, 122, fill=(14, 20, 38), border=GOLD)

    d.rectangle([144, 35 + dy, 336, 49 + dy], fill=(32, 44, 72, 255), outline=(*CHALK_GREEN, 255))
    draw_text(cv, "PRÓXIMO EPISODIO · TU IDEA", 240, 38 + dy, "silk", 8, GOLD, align="center")

    draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 70 + dy, "press", 8, CHALK_GREEN, align="center")

    # Caja interactiva de comentario con efecto de escritura y cursor titilante
    d.rectangle([126, 86 + dy, 354, 108 + dy], fill=(8, 12, 24, 255), outline=(*GOLD, 255))
    d.rectangle([132, 91 + dy, 144, 100 + dy], fill=(*CHALK_GREEN, 255))
    d.polygon([(135, 100 + dy), (139, 100 + dy), (135, 104 + dy)], fill=(*CHALK_GREEN, 255))

    full_msg = i18n_tr("DEJALO EN LOS COMENTARIOS...")
    typed_p = clamp01((t - t_vo) / 2.2)
    n_chars = max(1, int(len(full_msg) * typed_p))
    cur = "|" if int(t * 4) % 2 == 0 else " "
    draw_text(cv, full_msg[:n_chars] + cur, 150, 93 + dy, "silk", 8, GOLD, align="left")

    draw_text(cv, "¿CIENCIA? · ¿VIDEOJUEGOS? · ¿CINE?", 240, 115 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "¡TE LEEMOS ABAJO!", 240, 132 + dy, "press", 8, CHALK_GREEN, align="center")

    # Philo Farnsworth saludando junto a una mesa con televisor CRT
    char(cv, "farnsworth_young", 168, 248, t, scale=2, arms="wave", look=1, mood="happy",
         talk=talk_v(t, t_vo <= t <= t_end_vo))
    draw_tv_table_prop(cv, 308, 248, t, mode="scan")

    cv = vignette(cv, 0.32)
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c8_07") + 2.2

SCENES = [
    (TL.s("c8_00") - 0.15, TL.s("c8_01"), make_card(8, ["VALIÓ LA", "PENA"], "1969 – 2026 · EL MUNDO")),
    (TL.s("c8_01") - 0.15, TL.s("c8_03"), c8_s01_moon_landing_1969),
    (TL.s("c8_03"), TL.s("c8_05"), c8_s02_streaming_and_youtube),
    (TL.s("c8_05"), TL.s("c8_07") - 0.20, c8_s03_finale_match_cut),
    (TL.s("c8_07") - 0.20, T_END, c8_s04_comment_cta),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c8_00"), TL.e("c8_07") - TL.s("c8_00"), (220.0, 261.63, 329.63), amp=0.015)


def sfx(A):
    A.fx_sparkle(TL.s("c8_01"), 0.10)
    A.fx_chime(TL.word("c8_02", "valido"), 0.12)
    A.fx_pop(TL.s("c8_04"), 0.10)
    A.fx_chime(TL.s("c8_06"), 0.12)
    A.fx_pop(TL.s("c8_07"), 0.11)
    A.fx_sparkle(TL.s("c8_07") + 0.35, 0.11)
