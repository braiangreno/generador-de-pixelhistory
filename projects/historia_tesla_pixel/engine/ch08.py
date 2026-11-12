"""Capítulo 8: El hombre de las palomas (Hoteles de Nueva York, Medalla Edison, Habitación 3327, el Tesla y Match Cut final)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from i18n import tr as i18n_tr


def c8_s01_pigeons_and_medal(t):
    """9:02 - 9:26: Tesla anciano alimentando a la paloma blanca, la Medalla Edison vacía y la plaza llena de palomas."""
    t0 = TL.s("c8_01")
    t_blanca = TL.word("c8_01", "blanca")
    t_c8_02 = TL.s("c8_02")
    t_med = TL.word("c8_02", "Medalla")
    t_des = TL.word("c8_02", "desapareció")
    t_c8_03 = TL.s("c8_03")

    cv = bg("bg_ny_plaza_pigeons_1930").copy()
    draw_place_only(cv, "NUEVA YORK · AÑOS 1930", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    if t < t_c8_02:
        # Tesla anciano dándole de comer a las palomas en el suelo y a su paloma blanca favorita en la mano
        char(cv, "inventor_old", 240, 248, t, scale=2, arms="offer", look=1, mood="happy")

        def _draw_pigeons_feed(target_cv, fx, fy):
            for i, dx_p in enumerate((-64, -42, 42, 68)):
                draw_pigeon(target_cv, fx + dx_p, fy - 4, t + i * 0.4, white=False, peck=True)
            if t >= t_blanca - 0.6:
                glow(target_cv, fx + 20, fy - 34, 18, CREAM, 0.55)
            draw_pigeon(target_cv, fx + 20, fy - 32, t, white=True, peck=False)

        floor_prop(cv, _draw_pigeons_feed, 240, 248)
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

        def _draw_pigeons_flock(target_cv, fx, fy):
            for dx_p, dy_p, wh in ((-16, -42, False), (16, -42, True), (0, -62, False),
                                   (-36, -4, False), (36, -4, False), (-54, -2, False)):
                draw_pigeon(target_cv, fx + dx_p, fy + dy_p, t + (fx + dx_p) * 0.03, white=wh, peck=(dy_p > -18))

        floor_prop(cv, _draw_pigeons_flock, 268, 248)
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
        # Alféizar de la ventana desde donde despega la paloma blanca hacia el cielo invernal
        d_w = ImageDraw.Draw(cv)
        d_w.rectangle([198, 138, 304, 144], fill=(64, 48, 38, 255), outline=(*INK, 255))
        prog_fly = clamp01((t - t0) / 4.5)
        px = int(220 + 75 * prog_fly)
        py = int(136 - 42 * prog_fly)
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
    draw_rotating_arrows(cv, 240, 168, 36, ang, color=TESLA_CYAN, sand_groove=True, pulse=glow_p)

    if t < t_c8_09:
        window(cv, 120, 44, 240, 56, fill=(22, 18, 34), border=GOLD)
        draw_text(cv, "PARTERA: «HIJO DE LA TORMENTA»", 240, 54, "silk", 8, TESLA_VIOLET, align="center")
        if t >= t_luz - 0.35:
            draw_text(cv, "SU MADRE: «NO: DE LA LUZ»", 240, 74, "silk", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c8_09)
        window(cv, 120, 46 + dy, 240, 52, fill=(16, 22, 38), border=GOLD)
        draw_text(cv, "NIKOLA TESLA (1856 – 1943)", 240, 54 + dy, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "TUVIERON RAZÓN LAS DOS.", 240, 72 + dy, "press", 8, GOLD, align="center")

    cv = vignette(cv, 0.35)
    return cv


def c8_s04_comment_cta(t):
    """Llamado a la acción final antes de la placa de Pixeloide Studios: invita a comentar el próximo episodio."""
    t0 = TL.s("c8_10") - 0.20
    t_vo = TL.s("c8_10")
    t_end_vo = TL.e("c8_10")

    cv = bg("bg_night_grid_city").copy()
    d = ImageDraw.Draw(cv)

    # Ventana RPG principal (x=118..362, w=244 -> cabe 1:1 en 16:9 y en 9:16 sin escalar)
    a, dy = pop(t, t0, dur=0.32)
    window(cv, 118, 28 + dy, 244, 122, fill=(14, 20, 38), border=GOLD)

    # Etiqueta superior dorada
    d.rectangle([144, 35 + dy, 336, 49 + dy], fill=(32, 44, 72, 255), outline=(*TESLA_CYAN, 255))
    draw_text(cv, "PRÓXIMO EPISODIO · TU IDEA", 240, 38 + dy, "silk", 8, GOLD, align="center")

    # Pregunta principal
    draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 70 + dy, "press", 8, TESLA_CYAN, align="center")

    # Caja interactiva de comentario con efecto de escritura y cursor titilante
    d.rectangle([126, 86 + dy, 354, 108 + dy], fill=(8, 12, 24, 255), outline=(*GOLD, 255))
    # Icono de burbuja de comentario a la izquierda
    d.rectangle([132, 91 + dy, 144, 100 + dy], fill=(*TESLA_CYAN, 255))
    d.polygon([(135, 100 + dy), (139, 100 + dy), (135, 104 + dy)], fill=(*TESLA_CYAN, 255))

    full_msg = i18n_tr("DEJALO EN LOS COMENTARIOS...")
    typed_p = clamp01((t - t_vo) / 2.2)
    n_chars = max(1, int(len(full_msg) * typed_p))
    cur = "|" if int(t * 4) % 2 == 0 else " "
    draw_text(cv, full_msg[:n_chars] + cur, 150, 93 + dy, "silk", 8, GOLD, align="left")

    # Sugerencias de temas + llamado abajo
    draw_text(cv, "¿CIENCIA? · ¿VIDEOJUEGOS? · ¿CINE?", 240, 115 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "¡TE LEEMOS ABAJO!", 240, 132 + dy, "press", 8, CHALK_GREEN, align="center")

    # Nikola Tesla saludando en el piso junto a su paloma blanca sobre una mesita
    char(cv, "inventor", 168, 248, t, scale=2, arms="wave", look=1, mood="happy",
         talk=talk_v(t, t_vo <= t <= t_end_vo))

    def _draw_cta_pigeon_stand(target_cv, fx, fy):
        d_s = ImageDraw.Draw(target_cv)
        d_s.ellipse([fx - 20, fy - 4, fx + 20, fy + 3], fill=(0, 0, 0, 110))
        d_s.rectangle([fx - 4, fy - 28, fx + 4, fy], fill=(92, 56, 32, 255), outline=(*INK, 255))
        d_s.rectangle([fx - 16, fy - 34, fx + 16, fy - 28], fill=(124, 78, 44, 255), outline=(*GOLD, 255))
        glow(target_cv, fx, fy - 42, 18, CREAM, 0.55)
        draw_pigeon(target_cv, fx, fy - 38, t, white=True, peck=False)

    floor_prop(cv, _draw_cta_pigeon_stand, 312, 248)

    cv = vignette(cv, 0.32)
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c8_10") + 2.2

SCENES = [
    (TL.s("c8_00") - 0.15, TL.s("c8_01"), make_card(8, ["EL HOMBRE DE", "LAS PALOMAS"], "1917 – 1943 · NUEVA YORK", snow=True)),
    (TL.s("c8_01") - 0.15, TL.s("c8_04"), c8_s01_pigeons_and_medal),
    (TL.s("c8_04"), TL.s("c8_07"), c8_s02_room_3327_and_tesla_unit),
    (TL.s("c8_07"), TL.s("c8_10") - 0.20, c8_s03_finale_match_cut),
    (TL.s("c8_10") - 0.20, T_END, c8_s04_comment_cta),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 3 final: Piano íntimo para el hombre de las palomas y regreso luminoso al tema de las 4 flechas."""
    t0 = TL.s("c8_00")
    t_unit = TL.s("c8_05")
    t_end_vo = TL.e("c8_10")
    A.add_pad(t0, t_unit - t0, [110.0, 164.81, 220.0, 261.63], amp=0.036)
    A.add_pad(t_unit, t_end_vo - t_unit + 1.2, [130.81, 196.0, 261.63, 329.63], amp=0.044)


def sfx(A):
    A.fx_sparkle(TL.word("c8_01", "blanca"), 0.10)
    A.fx_pop(TL.word("c8_02", "Medalla"), 0.09)
    A.fx_chime(TL.word("c8_05", "tesla"), 0.11)
    A.fx_sweep(TL.s("c8_07"), 0.7, 110, 330, 0.08)
    A.fx_chime(TL.s("c8_09"), 0.13)
    A.fx_pop(TL.s("c8_10"), 0.11)
    A.fx_sparkle(TL.s("c8_10") + 0.35, 0.11)

