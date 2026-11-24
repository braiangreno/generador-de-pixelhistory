"""Capítulo 8: El libro, otra vez (Regreso a la biblioteca, lápida 1918, fiesta de Hawking y CTA comentarios)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch8 = make_card(8, ["EL LIBRO, OTRA VEZ"], "NUEVA YORK · EL CIERRE")


def scene_ch8(t):
    t_01 = TL.start("c8_01")
    t_02 = TL.start("c8_02")
    t_03 = TL.start("c8_03")
    t_04 = TL.start("c8_04")
    t_05 = TL.start("c8_05")
    t_06 = TL.start("c8_06")
    t_07 = TL.start("c8_07")
    t_08 = TL.start("c8_08")
    ground_y = 224

    if t < t_02:
        # c8_01: Vuelve la biblioteca polvorienta de la apertura con libro abierto
        cv = bg("library_1893")
        grade(cv, tint=(1.08, 0.96, 0.82), dark=0.08)
        draw_chapter_header(cv, "CAP. 8 · EL LIBRO, OTRA VEZ", "NUEVA YORK · 1893", t, t_01, border=GOLD)
        floor_prop(cv, lambda c, x, f: draw_library_table_prop(c, x, f, t=t, book_open=True), 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "¿QUÉ ES BARON TRUMP?", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "UN LIBRO DE AVENTURAS DE 1893", 240, 76, "silk", 8, CREAM, align="center")
        char(cv, "lockwood", 142, ground_y, t, scale=2, look=1)
        return vignette(cv, 0.34)

    if t < t_03:
        # c8_02: Época de Julio Verne, castillo, perro y túnel
        cv = bg("castle_tunnel_1893")
        grade(cv, tint=(1.06, 0.96, 0.84), dark=0.06)
        draw_chapter_header(cv, "CAP. 8 · EL LIBRO, OTRA VEZ", "LA ÉPOCA DE JULIO VERNE", t, t_02, border=GOLD)
        floor_prop(cv, draw_bulger_dog_prop, 316, ground_y)
        window(cv, 76, 44, 328, 66, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "LA ÉPOCA DE JULIO VERNE", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "VIAJES FANTÁSTICOS BAJO TIERRA", 240, 76, "silk", 8, CREAM, align="center")
        char(cv, "baron_boy", 190, ground_y, t, scale=2, look=1, smile=True)
        return vignette(cv, 0.34)

    if t < t_04:
        # c8_03: Cementerio de Nueva York con lápida sencilla de 1918
        cv = bg("cemetery_1918")
        grade(cv, tint=(1.04, 0.94, 0.82), dark=0.10)
        draw_chapter_header(cv, "CAP. 8 · EL LIBRO, OTRA VEZ", "LOCKWOOD · 1841–1918", t, t_03, border=GOLD)
        floor_prop(cv, draw_tombstone_prop, 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(20, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "LOCKWOOD · 1841–1918", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "NUNCA SUPO QUE SE VOLVERÍA VIRAL", 240, 76, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.36)

    if t < t_05:
        # c8_04: Tablero de corcho: hilos rojos se sueltan uno por uno
        cv = bg("corkboard_bg")
        grade(cv, dark=0.14)
        draw_chapter_header(cv, "CAP. 8 · EL LIBRO, OTRA VEZ", "LA EXPLICACIÓN", t, t_04, border=CYAN)
        window(cv, 76, 44, 328, 86, fill=(16, 20, 32), border=CYAN, alpha=0.95)
        draw_text(cv, "COINCIDENCIAS EXPLICADAS:", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "MATEMÁTICA · TÍTULOS DE NOBLEZA", 240, 76, "silk", 8, GOLD, align="center")
        draw_text(cv, "TRES LIBROS MEZCLADOS EN INTERNET", 240, 96, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_06:
        # c8_05: Reloj de bolsillo: agujas giran al revés y se detienen
        cv = new_canvas((12, 14, 22))
        stopped = (t > t_05 + 3.0)
        draw_pocket_watch(cv, 240, 108, t, r=32, reverse=True, speed=2.6, stopped=stopped)
        window(cv, 76, 162, 328, 64, fill=(16, 20, 34), border=GOLD, alpha=0.95)
        draw_text(cv, "AL FUTURO VIAJAMOS DESPACIO", 240, 174, "press", 8, CYAN, align="center")
        draw_text(cv, "AL PASADO, NO LLEGÓ NADIE", 240, 196, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.36)

    if t < t_07:
        # c8_06: Sala de la fiesta de Hawking vacía con copas servidas
        cv = bg("cambridge_hall_2009")
        grade(cv, dark=0.12)
        draw_chapter_header(cv, "CAP. 8 · EL LIBRO, OTRA VEZ", "LA INVITACIÓN SIGUE PUBLICADA", t, t_06, border=GOLD)
        floor_prop(cv, draw_party_table_prop, 240, ground_y)
        window(cv, 76, 44, 328, 66, fill=(16, 18, 30), border=GOLD, alpha=0.95)
        draw_text(cv, "LA INVITACIÓN DE HAWKING", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "TIENE FECHA, HORA Y LUGAR", 240, 76, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.36)

    if t < t_08:
        # c8_07: Copa de champán servida, sola. Remate final.
        cv = bg("cambridge_hall_2009")
        grade(cv, dark=0.38)
        floor_prop(cv, draw_party_table_prop, 240, ground_y)
        window(cv, 76, 52, 328, 72, fill=(14, 16, 26), border=GOLD, alpha=0.96)
        draw_text(cv, "SI ALGUIEN VIAJA AL PASADO,", 240, 64, "press", 8, GOLD, align="center")
        draw_text(cv, "YA SABE DÓNDE LO ESPERA UNA FIESTA.", 240, 88, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.42)

    # c8_08: CTA comentarios antes del cierre oficial de Pixeloide Studios
    cv = bg("library_1893")
    grade(cv, dark=0.42)
    draw_pocket_watch(cv, 240, 48, t, r=18, reverse=True, speed=1.4)
    window(cv, 64, 82, 352, 92, fill=(14, 18, 34), border=CYAN, alpha=0.96)
    draw_text(cv, "¿QUÉ MISTERIO INVESTIGAMOS?", 240, 96, "press", 8, CYAN, align="center")
    draw_text(cv, "DÉJALO EN LOS COMENTARIOS", 240, 122, "press", 16, GOLD, align="center")
    draw_text(cv, "SUSCRÍBETE A PIXELOIDE STUDIOS", 240, 152, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.38)


def scenes():
    return [
        (TL.start("c8_00") - 0.1, card_ch8, None),
        (TL.start("c8_01") - 0.1, scene_ch8, lambda t: cam_push(t, TL.start("c8_01"), TL.end("c8_08"), 1.0, 1.03)),
    ]
