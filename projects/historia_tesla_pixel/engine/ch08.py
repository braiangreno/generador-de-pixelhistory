"""Capítulo 8: El hombre de las palomas (Hoteles de Nueva York, Medalla Edison, Habitación 3327, el Tesla y Match Cut final)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c8_s01_pigeons_and_medal(t):
    """9:02 - 9:26: Tesla anciano alimentando a la paloma blanca, la Medalla Edison vacía y la plaza llena de palomas."""
    t0 = TL.s("c8_01")
    t_blanca = TL.word("c8_01", "blanca")
    t_c8_02 = TL.s("c8_02")
    t_med = TL.word("c8_02", "Medalla")
    t_des = TL.word("c8_02", "desapareció")
    t_c8_03 = TL.s("c8_03")

    cv = bg("bg_ny_plaza_pigeons_1930").copy()
    draw_chapter_header(cv, t, t0, 8, "EL HOMBRE DE LAS PALOMAS", "NUEVA YORK · AÑOS 1930", border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    if t < t_c8_02:
        # Tesla anciano dándole de comer a las palomas y a su paloma blanca favorita
        char(cv, "inventor_old", 240, 248, t, scale=2, arms="offer", look=1, mood="happy")
        for i, px in enumerate((176, 198, 282, 308)):
            draw_pigeon(cv, px, 244, t + i * 0.4, white=False, peck=True)
        # La paloma blanca posada junto a su mano con un suave halo
        if t >= t_blanca - 0.6:
            glow(cv, 260, 214, 18, CREAM, 0.55)
        draw_pigeon(cv, 260, 216, t, white=True, peck=False)
        window(cv, 122, 54, 236, 44, fill=(18, 24, 38), border=CREAM)
        draw_text(cv, "NOCHES EN NUEVA YORK", 240, 62, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA PALOMA BLANCA", 240, 78, "silk", 8, GOLD, align="center")
    elif t < t_c8_03:
        # Ceremonia de la Medalla Edison: estrado con medalla dorada y silla vacía
        window(cv, 118, 48, 244, 126, fill=(24, 20, 32), border=GOLD)
        draw_text(cv, "CEREMONIA · MEDALLA EDISON (1917)", 240, 56, "silk", 8, GOLD, align="center")
        # Medalla dorada en estuche sobre el atril
        d.ellipse([226, 76, 254, 104], fill=(*GOLD, 255), outline=(*CREAM, 255))
        draw_text(cv, "M", 240, 86, "press", 8, INK, align="center")
        # Silla del homenajeado vacía cuando dice "desapareció"
        d.rectangle([222, 116, 258, 142], fill=(92, 36, 44, 255), outline=(*GOLD, 255))
        draw_text(cv, "¿DÓNDE ESTÁ TESLA?" if t >= t_des - 0.25 else "EL PREMIO MÁS IMPORTANTE",
                  240, 152, "silk", 8, CHALK_RED if t >= t_des - 0.25 else CREAM, align="center")
        char(cv, "organizer", 152, 248, t, scale=2, arms="shrug" if t >= t_des - 0.2 else "offer",
             look=1, mood="surprised" if t >= t_des - 0.2 else "happy")
    else:
        # Lo encuentran en la plaza cubierto de palomas
        char(cv, "organizer", 148, 248, t, scale=2, arms="point", look=1, mood="surprised")
        char(cv, "inventor_old", 268, 248, t, scale=2, arms="up", look=-1, mood="happy")
        for px, py, wh in ((252, 206, False), (284, 206, True), (268, 186, False),
                           (232, 244, False), (304, 244, False), (214, 246, False)):
            draw_pigeon(cv, px, py, t + px * 0.03, white=wh, peck=(py > 230))
        window(cv, 124, 54, 232, 42, fill=(18, 24, 38), border=TESLA_CYAN)
        draw_text(cv, "EN LA PLAZA CERCANA:", 240, 62, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CUBIERTO DE PALOMAS", 240, 78, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.36)


def c8_s02_room_3327_and_tesla_unit(t):
    """9:26 - 9:53: Habitación 3327 en 1943, mini-lección de la unidad 'El Tesla' (1,5 a 3 T) y motores de inducción."""
    t0 = TL.s("c8_04")
    t_c8_05 = TL.s("c8_05")
    t_tes = TL.word("c8_05", "tesla")
    t_iman = TL.word("c8_05", "imán")
    t_c8_06 = TL.s("c8_06")

    if t < t_c8_05:
        cv = bg("bg_hotel_3327_winter_1943").copy()
        SNOW.draw(cv, t, density=0.35)
        draw_place_only(cv, "HABITACIÓN 3327 · NUEVA YORK (1943)", t, t0, border=SOFT_GRAY)
        # Paloma blanca alejándose por la ventana hacia el cielo invernal
        prog_fly = clamp01((t - t0) / 4.5)
        px = int(220 + 75 * prog_fly)
        py = int(138 - 44 * prog_fly)
        glow(cv, px, py, 16, CREAM, 0.5)
        draw_pigeon(cv, px, py, t * 2.0, white=True, peck=False)

        window(cv, 122, 54, 236, 52, fill=(16, 20, 32), border=SOFT_GRAY)
        draw_text(cv, "7 DE ENERO DE 1943 · 86 AÑOS", 240, 62, "silk", 8, CREAM, align="center")
        draw_text(cv, "SOLO Y CASI SIN DINERO", 240, 80, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.42)

    cv = bg("bg_hospital_factory_1960").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c8_06:
        # Mini lección integrada en escena (dentro de x=118..362): UNIDAD EL TESLA (T)
        draw_place_only(cv, "1960 · LA UNIDAD «EL TESLA» (T)", t, t_c8_05, border=TESLA_CYAN)
        window(cv, 118, 44, 244, 158, fill=(16, 28, 42), border=TESLA_CYAN)
        draw_text(cv, "1,5 A 3 TESLAS", 240, 52, "press", 8, TESLA_CYAN, align="center")

        # Arriba: Resonador magnético de hospital (1,5 A 3 TESLAS)
        d.rectangle([132, 72, 348, 122], fill=(24, 42, 62, 255), outline=(*TESLA_CYAN, 255))
        d.ellipse([142, 78, 182, 116], fill=(220, 232, 244, 255), outline=(*TESLA_CYAN, 255))
        draw_rotating_arrows(cv, 162, 97, 11, t * 3.2, color=TESLA_CYAN, pulse=0.9)
        draw_text(cv, "RESONADOR DE HOSPITAL:", 264, 82, "silk", 8, CREAM, align="center")
        draw_text(cv, "1,5 A 3 TESLAS", 264, 98, "silk", 8, GOLD, align="center")

        # Abajo: Imán de refrigerador (0,005 TESLAS / unas milésimas)
        if t >= t_iman - 0.5:
            d.rectangle([132, 130, 348, 184], fill=(28, 36, 48, 255), outline=(*GOLD, 255))
            d.rectangle([148, 138, 176, 176], fill=(210, 218, 226, 255), outline=(*INK, 255))
            d.rectangle([158, 148, 166, 156], fill=(*CHALK_RED, 255))  # Imán chiquito
            draw_text(cv, "IMÁN DE REFRIGERADOR:", 264, 144, "silk", 8, CREAM, align="center")
            draw_text(cv, "0,005 TESLAS (MILÉSIMAS)", 264, 160, "silk", 8, CHALK_YELLOW, align="center")
        return vignette(cv, 0.30)

    # c8_06: Motores de inducción girando en fábricas, bombas de agua y ventiladores
    draw_place_only(cv, "SUS MOTORES SIGUEN GIRANDO HOY", t, t_c8_06, border=GOLD)
    window(cv, 118, 48, 244, 148, fill=(16, 26, 40), border=GOLD)
    draw_text(cv, "EL MOTOR DE INDUCCIÓN DE TESLA", 240, 56, "silk", 8, GOLD, align="center")

    items = [
        (162, 114, "FÁBRICAS", TESLA_CYAN),
        (240, 114, "BOMBAS", CHALK_GREEN),
        (318, 114, "VENTILADORES", GOLD),
    ]
    for ix, iy, lbl, col in items:
        d.ellipse([ix - 26, iy - 26, ix + 26, iy + 26], fill=(22, 36, 54, 255), outline=(*col, 255))
        draw_rotating_arrows(cv, ix, iy, 18, t * 4.0, color=col, pulse=0.9)
        draw_text(cv, lbl, ix, iy + 34, "silk", 8, CREAM, align="center")
    draw_text(cv, "EL MISMO IMÁN QUE GIRA SOLO", 240, 172, "silk", 8, TESLA_CYAN, align="center")
    return vignette(cv, 0.30)


def c8_s03_finale_match_cut(t):
    """9:53 - Fin de narrativa: Regreso a tu casa -> Match cut con las 4 flechas en la arena de Budapest."""
    t0 = TL.s("c8_07")
    t_c8_08 = TL.s("c8_08")
    t_tor = TL.word("c8_08", "tormenta")
    t_luz = TL.word("c8_08", "luz")
    t_c8_09 = TL.s("c8_09")
    t_end_vo = TL.e("c8_09")

    if t < t_c8_08:
        # Regreso al plano 1 de la apertura: la habitación oscura y la corriente que va y viene hacia tu pantalla
        cv = bg("bg_dark_room_screen").copy()
        d = ImageDraw.Draw(cv)
        glow(cv, 240, 130, 74, TESLA_CYAN, 0.45)
        for i in range(9):
            px = int((130 + i * 26 + math.sin(t * 9.0) * 10))
            py = int(208 - (i / 8.0) * 48)
            col = TESLA_SPARK if i % 2 == 0 else TESLA_CYAN
            d.rectangle([px - 2, py - 2, px + 2, py + 2], fill=(*col, 255))
        window(cv, 120, 48, 240, 52, fill=(14, 20, 36), border=TESLA_CYAN)
        draw_text(cv, "AHORA MISMO EN TU CASA:", 240, 56, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "LA CORRIENTE VA Y VIENE (AC)", 240, 74, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.38)

    # Match cut al parque de Budapest al atardecer con el dibujo en la arena
    cv = bg("bg_budapest_park_sunset").copy()
    # Si ya pasó c8_09 + 1.0s, las 4 flechas detienen suavemente su giro y queda corte a negro antes del outro
    if t <= t_c8_09 + 0.9:
        ang = t * 2.8
    else:
        ang = (t_c8_09 + 0.9) * 2.8

    glow_p = 0.85 if t >= t_luz - 0.2 else 0.45
    draw_rotating_arrows(cv, 240, 198, 40, ang, color=TESLA_CYAN, sand_groove=True, pulse=glow_p)

    if t < t_c8_09:
        window(cv, 118, 48, 244, 58, fill=(22, 18, 34), border=GOLD)
        draw_text(cv, "PARTERA: «HIJO DE LA TORMENTA»", 240, 58, "silk", 8, TESLA_VIOLET, align="center")
        if t >= t_luz - 0.35:
            draw_text(cv, "SU MADRE: «NO: DE LA LUZ»", 240, 78, "silk", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c8_09)
        window(cv, 120, 52 + dy, 240, 52, fill=(16, 22, 38), border=GOLD)
        draw_text(cv, "NIKOLA TESLA (1856 – 1943)", 240, 60 + dy, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "TUVIERON RAZÓN LAS DOS.", 240, 78 + dy, "press", 8, GOLD, align="center")

    cv = vignette(cv, 0.35)
    # Dos segundos de pausa / fundido a negro antes del cierre de marca de Pixeloide Studios
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c8_09") + 2.8

SCENES = [
    (TL.s("c8_01"), TL.s("c8_04"), c8_s01_pigeons_and_medal),
    (TL.s("c8_04"), TL.s("c8_07"), c8_s02_room_3327_and_tesla_unit),
    (TL.s("c8_07"), T_END, c8_s03_finale_match_cut),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 3 final: Piano íntimo para el hombre de las palomas y regreso luminoso al tema de las 4 flechas."""
    t0 = TL.s("c8_01")
    t_unit = TL.s("c8_05")
    t_end_vo = TL.e("c8_09")
    A.add_pad(t0, t_unit - t0, [110.0, 164.81, 220.0, 261.63], amp=0.036)
    A.add_pad(t_unit, t_end_vo - t_unit + 1.2, [130.81, 196.0, 261.63, 329.63], amp=0.044)


def sfx(A):
    A.fx_sparkle(TL.word("c8_01", "blanca"), 0.10)
    A.fx_pop(TL.word("c8_02", "Medalla"), 0.09)
    A.fx_chime(TL.word("c8_05", "tesla"), 0.11)
    A.fx_sweep(TL.s("c8_07"), 0.7, 110, 330, 0.08)
    A.fx_chime(TL.s("c8_09"), 0.13)

