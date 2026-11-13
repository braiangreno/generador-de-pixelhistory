"""Capítulo 8: Mil seiscientos saltos (c8_00..c8_08) — Premio EFF 1997, Salón de la Fama 2014,
LA PIZARRA 3 (Bluetooth y 1.600 saltos/s), el cierre poético y el llamado a comentar antes de Pixeloide Studios."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from i18n import tr as i18n_tr


def c8_s01_awards_and_hall_of_fame(t):
    """c8_01..c8_02: Premio EFF 1997 a los 82 años -> Salón de la Fama de los Inventores (2014) y portada de Google (2015)."""
    t0 = TL.s("c8_01")
    t_prem = TL.word("c8_01", "premio")
    t_c8_02 = TL.s("c8_02")
    t_salon = TL.word("c8_02", "Salón")
    t_goog = TL.word("c8_02", "portada")

    cv = bg("hall_of_fame_modern").copy()
    STARS.draw(cv, t, alpha=0.65)
    draw_place_only(cv, "1997 – 2015 · RECONOCIMIENTO MUNDIAL", t, t0, border=GOLD)

    draw_table_with_prop(cv, 240, 248, prop_kind="trophy", t=t)

    if t < t_c8_02 - 0.1:
        char(cv, "hedy_older", 156, 248, t, scale=2, arms="wave", look=1, mood="happy")
        char(cv, "engineer", 324, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

        window(cv, 114, 44, 252, 74, fill=(14, 20, 42), border=GOLD, alpha=0.95)
        draw_text(cv, "1997 · PREMIO PIONEROS DIGITALES", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "PARA HEDY LAMARR (82 AÑOS) Y ANTHEIL", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "POR FIN EL MUNDO SUPO SU NOMBRE", 240, 94, "silk", 8, LAMARR_CYAN, align="center")
        return vignette(cv, 0.34)

    # c8_02: Murió en 2000 -> En 2014 entra al Salón de la Fama de los Inventores -> 2015 homenaje de Google
    CONF.draw(cv, t)
    char(cv, "hedy_inventor", 158, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    char(cv, "antheil", 322, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

    window(cv, 114, 44, 252, 78, fill=(14, 20, 42), border=LAMARR_CYAN, alpha=0.95)
    draw_text(cv, "HEDY LAMARR (1914 – 2000)", 240, 54, "silk", 8, GOLD, align="center")
    draw_text(cv, "2014: SALÓN DE LA FAMA DE INVENTORES", 240, 72, "press", 8, LAMARR_CYAN, align="center")
    if t >= t_goog - 0.45:
        draw_text(cv, "2015: GOOGLE LE DEDICA SU PORTADA", 240, 92, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "EL DÍA DE SU CUMPLEAÑOS (9 DE NOV)", 240, 108, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.32)


def c8_s02_pizarra_bluetooth(t):
    """c8_03..c8_05: LA PIZARRA 3 — Bluetooth clásico (79 canales, 1.600 saltos/s), wifi/microondas y del rollo de papel al chip."""
    t0 = TL.s("c8_03")
    t_mil = TL.word("c8_03", "seiscientas")
    t_c8_04 = TL.s("c8_04")
    t_c8_05 = TL.s("c8_05")
    t_chip = TL.word("c8_05", "chip")

    cv = draw_pizarra_frame(t, t0, "1.600 SALTOS POR SEGUNDO",
                            summary_es="SALTAR JUNTOS PARA NO CORTARSE",
                            t_summary=t_c8_05)
    d = ImageDraw.Draw(cv)

    window(cv, 116, 40, 248, 160, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96, inner=(38, 78, 54))

    if t < t_c8_04 - 0.1:
        # Paso 1 (c8_03): Bluetooth clásico reparte su señal en 79 canales y salta 1.600 veces/s
        draw_text(cv, "BLUETOOTH CLÁSICO HOY:", 240, 48, "silk", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "79 CANALES · 1.600 SALTOS / SEG", 240, 64, "press", 8, CHALK_CYAN, align="center")
        draw_freq_lanes(cv, 126, 80, 228, 92, t, n_lanes=5, speed=7.5 if t >= t_mil - 0.2 else 4.5,
                        hopping=True, show_labels=True)
        draw_text(cv, "¡MÁS RÁPIDO QUE CUALQUIER RUIDO!", 240, 178, "silk", 8, CHALK_GREEN, align="center")

    elif t < t_c8_05 - 0.1:
        # Paso 2 (c8_04): Si un canal está ocupado por wifi o microondas, tus auriculares saltan a otro
        draw_text(cv, "¿WIFI O MICROONDAS CERCA?", 240, 48, "silk", 8, CHALK_YELLOW, align="center")
        draw_freq_lanes(cv, 126, 66, 228, 94, t, n_lanes=4, speed=6.2,
                        jammed_lane=2, hopping=True, show_labels=True)
        draw_text(cv, "SI EL CANAL 3 ESTÁ OCUPADO,", 240, 164, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "¡SALTA A OTRO Y NO SE CORTA!", 240, 178, "press", 8, CHALK_GREEN, align="center")

    else:
        # Paso 3 (c8_05): El rollo de papel de 1942 -> hoy es un microchip
        draw_text(cv, "EL MISMO TRUCO EN TU BOLSILLO:", 240, 48, "silk", 8, CHALK_YELLOW, align="center")
        # Izquierda: Rollo perforado (1942) -> Derecha: Microchip (Hoy)
        draw_piano_roll(cv, 148, 68, 38, 76, t, speed=24.0, alpha=0.95)
        draw_text(cv, "1942: ROLLO", 167, 150, "silk", 8, CHALK_YELLOW, align="center")

        draw_text(cv, ">>>", 232, 102, "press", 8, CHALK_CYAN, align="center")

        # Microchip en pixel art a la derecha (x=276..332, y=78..134)
        cx_c, cy_c = 304, 106
        for pin_i in range(-18, 22, 8):
            d.line([(cx_c + pin_i, cy_c - 28), (cx_c + pin_i, cy_c + 28)], fill=(*GOLD, 255), width=2)
            d.line([(cx_c - 28, cy_c + pin_i), (cx_c + 28, cy_c + pin_i)], fill=(*GOLD, 255), width=2)
        d.rectangle([cx_c - 22, cy_c - 22, cx_c + 22, cy_c + 22], fill=(22, 32, 48, 255), outline=(*CHALK_CYAN, 255), width=2)
        draw_text(cv, "BT", cx_c, cy_c - 4, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "HOY: CHIP", 304, 150, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "SALTAR JUNTOS, EN SECRETO", 240, 174, "press", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.28)


def c8_s03_finale_piano_torpedo(t):
    """c8_06..c8_07: 'Piensa en un piano dentro de un torpedo. Y en una mujer a la que le pedían que se quedara quieta.'"""
    t0 = TL.s("c8_06")
    t_c8_07 = TL.s("c8_07")
    t_quieta = TL.word("c8_07", "quieta")

    cv = bg("hollywood_dining_patent").copy()
    STARS.draw(cv, t, alpha=0.65)
    draw_place_only(cv, "HEDY LAMARR · LEGADO ETERNO", t, t0, border=GOLD)

    # Piano de cola + mesa con auriculares inalámbricos y torpedo/patente
    draw_grand_piano_prop(cv, 328, 248, t=t, play=True)
    draw_table_with_prop(cv, 228, 248, prop_kind="headphones", t=t)

    char(cv, "hedy_inventor", 148, 248, t, scale=2,
         arms="cheer" if t >= t_c8_07 else "wave", look=1, mood="happy")
    glow(cv, 148, 152, 26, LAMARR_CYAN, 0.55)

    window(cv, 114, 44, 252, 78, fill=(14, 18, 38), border=GOLD, alpha=0.96)
    if t < t_c8_07 - 0.1:
        draw_text(cv, "CUANDO CONECTES TUS AURICULARES,", 240, 56, "silk", 8, CREAM, align="center")
        draw_text(cv, "PIENSA EN UN PIANO", 240, 74, "press", 8, GOLD, align="center")
        draw_text(cv, "DENTRO DE UN TORPEDO.", 240, 94, "press", 8, LAMARR_CYAN, align="center")
    else:
        draw_text(cv, "Y EN UNA MUJER A LA QUE LE PEDÍAN", 240, 56, "silk", 8, CREAM, align="center")
        draw_text(cv, "QUE SE QUEDARA QUIETA.", 240, 76, "press", 8, GOLD, align="center")
        if t >= t_quieta - 0.35:
            draw_text(cv, "HEDY LAMARR (1914 – 2000)", 240, 96, "press", 8, LAMARR_CYAN, align="center")
    return vignette(cv, 0.34)


def c8_s04_comment_cta(t):
    """c8_08: Llamado a la acción final antes de la placa de Pixeloide Studios: invita a comentar el próximo episodio."""
    t0 = TL.s("c8_08") - 0.20
    t_vo = TL.s("c8_08")
    t_end_vo = TL.e("c8_08")

    cv = bg("hall_of_fame_modern").copy()
    d = ImageDraw.Draw(cv)

    # Ventana RPG principal (x=118..362, w=244 -> cabe 1:1 en 16:9 y en 9:16 sin escalar)
    a, dy = pop(t, t0, dur=0.32)
    window(cv, 118, 28 + dy, 244, 122, fill=(14, 20, 38), border=GOLD)

    # Etiqueta superior dorada
    d.rectangle([144, 35 + dy, 336, 49 + dy], fill=(32, 44, 72, 255), outline=(*LAMARR_CYAN, 255))
    draw_text(cv, "PRÓXIMO EPISODIO · TU IDEA", 240, 38 + dy, "silk", 8, GOLD, align="center")

    # Pregunta principal
    draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 70 + dy, "press", 8, LAMARR_CYAN, align="center")

    # Caja interactiva de comentario con efecto de escritura y cursor titilante
    d.rectangle([126, 86 + dy, 354, 108 + dy], fill=(8, 12, 24, 255), outline=(*GOLD, 255))
    d.rectangle([132, 91 + dy, 144, 100 + dy], fill=(*LAMARR_CYAN, 255))
    d.polygon([(135, 100 + dy), (139, 100 + dy), (135, 104 + dy)], fill=(*LAMARR_CYAN, 255))

    full_msg = i18n_tr("DEJALO EN LOS COMENTARIOS...")
    typed_p = clamp01((t - t_vo) / 2.2)
    n_chars = max(1, int(len(full_msg) * typed_p))
    cur = "|" if int(t * 4) % 2 == 0 else " "
    draw_text(cv, full_msg[:n_chars] + cur, 150, 93 + dy, "silk", 8, GOLD, align="left")

    draw_text(cv, "¿CIENCIA? · ¿VIDEOJUEGOS? · ¿CINE?", 240, 115 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "¡TE LEEMOS ABAJO!", 240, 132 + dy, "press", 8, CHALK_GREEN, align="center")

    # Hedy Lamarr saludando en el piso junto a la mesa con auriculares inalámbricos
    char(cv, "hedy_inventor", 168, 248, t, scale=2, arms="wave", look=1, mood="happy",
         talk=talk_v(t, t_vo <= t <= t_end_vo))
    draw_table_with_prop(cv, 308, 248, prop_kind="headphones", t=t)

    cv = vignette(cv, 0.32)
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c8_08") + 2.2

SCENES = [
    (TL.s("c8_00") - 0.15, TL.s("c8_01"), make_card(8, ["MIL SEISCIENTOS", "SALTOS"], "1997 – HOY · EN TU BOLSILLO")),
    (TL.s("c8_01") - 0.15, TL.s("c8_03"), c8_s01_awards_and_hall_of_fame),
    (TL.s("c8_03") - 0.15, TL.s("c8_06"), c8_s02_pizarra_bluetooth),
    (TL.s("c8_06") - 0.15, TL.s("c8_08") - 0.20, c8_s03_finale_piano_torpedo),
    (TL.s("c8_08") - 0.20, T_END, c8_s04_comment_cta),
]


def scenes():
    return [(s[0], s[2], None, "ch08") for s in SCENES]


def music(A):
    t0 = TL.s("c8_00")
    t_fin = TL.s("c8_06")
    t_end_vo = TL.e("c8_08")
    A.add_pad(t0, t_fin - t0, [110.0, 164.81, 220.0, 261.63], amp=0.040)
    A.add_pad(t_fin, t_end_vo - t_fin + 1.2, [130.81, 196.0, 261.63, 329.63], amp=0.045)


def sfx(A):
    A.fx_chime(TL.word("c8_01", "premio"), 0.11)
    A.fx_sparkle(TL.word("c8_02", "Salón"), 0.11)
    A.fx_pop(TL.s("c8_03"), 0.09)
    A.fx_pop(TL.s("c8_04"), 0.08)
    A.fx_sparkle(TL.word("c8_05", "chip"), 0.11)
    A.fx_chime(TL.s("c8_06"), 0.12)
    A.fx_chime(TL.s("c8_07"), 0.13)
    A.fx_pop(TL.s("c8_08"), 0.11)
    A.fx_sparkle(TL.s("c8_08") + 0.35, 0.11)
