"""Apertura (Un libro olvidado, 1893-2017) + Capítulo 1 (El escritor, Ingersoll Lockwood)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL


# ===========================================================================
# APERTURA: UN LIBRO OLVIDADO (s01..s07)
# ===========================================================================

def scene_opening(t):
    t_s01 = TL.start("s01")
    t_s02 = TL.start("s02")
    t_s03 = TL.start("s03")
    t_s04 = TL.start("s04")
    t_s05 = TL.start("s05")
    t_s06 = TL.start("s06")
    t_s07 = TL.start("s07")
    ground_y = 224

    # s07: Placa de título principal sobre la biblioteca
    if t >= t_s07 - 0.1:
        cv = bg("library_1893")
        grade(cv, tint=(1.04, 0.94, 0.82), dark=0.45)
        draw_pocket_watch(cv, 240, 44, t, r=18, reverse=True, speed=1.6)
        p_in = ease_out(prog(t, t_s07, t_s07 + 0.6))
        window(cv, 38, 72, 404, 134, fill=(18, 16, 24), border=GOLD, alpha=0.95)
        draw_text(cv, "DOCUMENTAL PIXELOIDE · 1893 — 2017", 240, 84, "press", 8, CYAN, align="center")
        draw_text(cv, "UN CHICO LLAMADO", 240, 104, "press", 24, align="center", gradient=GOLD_RAMP,
                  reveal=max(1, int((t - t_s07 + 0.2) * 24)))
        draw_text(cv, "BARON TRUMP", 240, 134, "press", 24, align="center", gradient=CREAM_RAMP,
                  reveal=max(1, int((t - t_s07 - 0.1) * 24)))
        draw_text(cv, "TRUMP Y SU HIJO, ¿VIAJEROS EN EL TIEMPO?", 240, 174, "silk", 8, GOLD,
                  align="center", alpha=p_in)
        draw_text(cv, "POR PIXELOIDE STUDIOS", 240, 190, "silk", 8, GREY, align="center", alpha=p_in)
        return vignette(cv, 0.36)

    # s06: Negro + reloj de bolsillo cuyas agujas giran al revés
    if t >= t_s06 - 0.1:
        cv = new_canvas((10, 10, 16))
        draw_pocket_watch(cv, 240, 118, t, r=36, reverse=True, speed=3.6)
        window(cv, 76, 174, 328, 52, fill=(16, 18, 30), border=GOLD, alpha=0.95)
        draw_text(cv, "¿Y SI NO ERA UNA NOVELA?", 240, 184, "press", 8, GOLD, align="center")
        draw_text(cv, "¿Y SI ERA UN MENSAJE?", 240, 202, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.35)

    # s05: Torre genérica de vidrio oscuro de noche con signo de pregunta (sin logos ni personas)
    if t >= t_s05 - 0.1:
        cv = bg("nyc_tower_night")
        grade(cv, tint=(0.94, 0.98, 1.06), dark=0.10)
        draw_place_only(cv, "NUEVA YORK · 2017", t, t_s05, border=CYAN)
        window(cv, 76, 46, 328, 72, fill=(14, 18, 34), border=CYAN, alpha=0.94)
        draw_text(cv, "2017 · ESTADOS UNIDOS", 240, 58, "press", 8, CYAN, align="center")
        draw_text(cv, "PRESIDENTE: DONALD TRUMP", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "HIJO MENOR: BARRON", 240, 94, "press", 8, GOLD, align="center")
        # Signo de pregunta enorme sobre la torre
        bob = int(math.sin(t * 4.0) * 3)
        draw_text(cv, "?", 240, 134 + bob, "press", 36, align="center", gradient=GOLD_RAMP, outline_w=2)
        return vignette(cv, 0.34)

    # s04: Pantallas de computadora con foros genéricos y círculos rojos
    if t >= t_s04 - 0.1:
        cv = bg("forum_room_2017")
        grade(cv, tint=(0.92, 0.98, 1.08), dark=0.10)
        draw_place_only(cv, "INTERNET · 2017", t, t_s04, border=CYAN)
        floor_prop(cv, draw_forum_desk_prop, 240, ground_y)
        window(cv, 76, 44, 328, 78, fill=(14, 18, 34), border=PINK, alpha=0.95)
        draw_text(cv, "INTERNET · 2017", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "ALGUIEN ENCONTRÓ EL LIBRO DE 1893", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "CÍRCULOS ROJOS · FLECHAS · TEORÍAS", 240, 94, "silk", 8, PINK, align="center")
        return vignette(cv, 0.34)

    # s03: Viaja a Rusia, cruza portal hacia mundo escondido, sabio Don
    if t >= t_s03 - 0.1:
        cv = bg("castle_tunnel_1893")
        grade(cv, tint=(1.06, 0.96, 0.84), dark=0.06)
        draw_place_only(cv, "EL LIBRO DE 1893 · EL PORTAL", t, t_s03, border=GOLD)
        window(cv, 76, 44, 328, 66, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "VIAJE A RUSIA Y UN PORTAL", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "GUIADO POR UN SABIO LLAMADO DON", 240, 74, "silk", 8, CREAM, align="center")
        bx, bw = walk(t, t_s03, t_s04, 130, 260)
        char(cv, "baron_boy", bx, ground_y, t, scale=2, walk=bw, look=1, r_arm="point")
        char(cv, "don_fum", 350, ground_y, t, scale=2, look=-1, talk=talk_v(t, True))
        return vignette(cv, 0.34)

    # s02: Castillo Trump, chico con perro enorme (Bulger)
    if t >= t_s02 - 0.1:
        cv = bg("castle_tunnel_1893")
        grade(cv, tint=(1.08, 0.96, 0.82), dark=0.06)
        draw_place_only(cv, "BARON TRUMP · 1893", t, t_s02, border=GOLD)
        floor_prop(cv, draw_bulger_dog_prop, 316, ground_y)
        window(cv, 76, 44, 328, 66, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "BARON TRUMP", 240, 54, "press", 16, GOLD, align="center")
        draw_text(cv, "VIVÍA EN EL CASTILLO TRUMP", 240, 82, "silk", 8, CREAM, align="center")
        char(cv, "baron_boy", 196, ground_y, t, scale=2, look=1, smile=True, l_arm="up")
        return vignette(cv, 0.34)

    # s01: Biblioteca polvorienta, libro viejo, reloj de bolsillo
    cv = bg("library_1893")
    grade(cv, tint=(1.08, 0.96, 0.82), dark=0.08)
    draw_place_only(cv, "NUEVA YORK · 1893", t, t_s01, border=GOLD)
    floor_prop(cv, lambda c, x, f: draw_library_table_prop(c, x, f, t=t, book_open=False), 240, ground_y)
    window(cv, 76, 44, 328, 66, fill=(22, 18, 24), border=GOLD, alpha=0.94)
    draw_text(cv, "NUEVA YORK · 1893", 240, 54, "press", 8, GOLD, align="center")
    draw_text(cv, "UN LIBRO DE AVENTURAS PARA CHICOS", 240, 74, "silk", 8, CREAM, align="center")
    char(cv, "lockwood", 142, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
    return vignette(cv, 0.34)


# ===========================================================================
# CAPÍTULO 1: EL ESCRITOR (c1_00..c1_06)
# ===========================================================================

card_ch1 = make_card(1, ["EL ESCRITOR"], "NUEVA YORK · SIGLO XIX")


def scene_ch1_writer(t):
    t_01 = TL.start("c1_01")
    t_02 = TL.start("c1_02")
    t_03 = TL.start("c1_03")
    t_04 = TL.start("c1_04")
    t_05 = TL.start("c1_05")
    t_06 = TL.start("c1_06")
    ground_y = 224

    if t < t_02:
        # c1_01: Ingersoll Lockwood en su despacho
        cv = bg("lawyer_office_1893")
        grade(cv, tint=(1.08, 0.96, 0.84), dark=0.06)
        draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "INGERSOLL LOCKWOOD · NUEVA YORK", t, t_01, border=GOLD)
        floor_prop(cv, draw_lawyer_desk_1893_prop, 240, ground_y)
        window(cv, 76, 44, 328, 62, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "INGERSOLL LOCKWOOD", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "ABOGADO · DIPLOMÁTICO · ESCRITOR", 240, 74, "silk", 8, CREAM, align="center")
        char(cv, "lockwood", 156, ground_y, t, scale=2, look=1, r_arm="write", talk=talk_v(t, True))
        person_card(cv, "lockwood", "INGERSOLL LOCKWOOD", "ABOGADO Y ESCRITOR · SIGLO XIX",
                    t, t_01 + 0.35, dur=3.5)
        return vignette(cv, 0.34)

    if t < t_03:
        # c1_02: Librería de época, 1889 y 1893, la gente pasa sin mirar
        cv = bg("bookshop_1893")
        grade(cv, tint=(1.08, 0.96, 0.84), dark=0.06)
        draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "1889 Y 1893 · LIBROS OLVIDADOS", t, t_02, border=GOLD)
        window(cv, 76, 44, 328, 62, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "1889 · 1893", 240, 54, "press", 16, GOLD, align="center")
        draw_text(cv, "LES FUE MAL · OLVIDADOS POR UN SIGLO", 240, 82, "silk", 8, CREAM, align="center")
        px1, pw1 = walk(t, t_02, t_03, 90, 390)
        px2, pw2 = walk(t, t_02, t_03, 380, 110)
        char(cv, "passerby_a", px1, ground_y, t, scale=2, walk=pw1, look=1)
        char(cv, "passerby_b", px2, ground_y, t, scale=2, walk=pw2, look=-1)
        return vignette(cv, 0.34)

    if t < t_04:
        # c1_03: Chico noble alemán y su perro Bulger
        cv = bg("castle_tunnel_1893")
        grade(cv, tint=(1.08, 0.96, 0.84), dark=0.06)
        draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "BULGER, EL PERRO", t, t_03, border=GOLD)
        floor_prop(cv, draw_bulger_dog_prop, 310, ground_y)
        window(cv, 76, 44, 328, 62, fill=(22, 18, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "NOBLE ALEMÁN · INQUIETO", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "VIAJA CON SU PERRO BULGER", 240, 74, "silk", 8, CREAM, align="center")
        char(cv, "baron_boy", 180, ground_y, t, scale=2, look=1, smile=True, r_arm="point")
        return vignette(cv, 0.34)

    if t < t_05:
        # c1_04: Folleto El último presidente (1896)
        cv = bg("lawyer_office_1893")
        grade(cv, tint=(1.08, 0.96, 0.84), dark=0.08)
        draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "EL ÚLTIMO PRESIDENTE · 1896", t, t_04, border=GOLD)
        floor_prop(cv, draw_lawyer_desk_1893_prop, 240, ground_y)
        window(cv, 76, 44, 328, 72, fill=(22, 18, 24), border=GOLD, alpha=0.95)
        draw_text(cv, "EL ÚLTIMO PRESIDENTE · 1896", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "UN FOLLETO FINO SOBRE EL CAOS", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "TRAS UNA ELECCIÓN INESPERADA", 240, 92, "silk", 8, GREY, align="center")
        char(cv, "lockwood", 142, ground_y, t, scale=2, look=1, talk=talk_v(t, True))
        return vignette(cv, 0.34)

    if t < t_06:
        # c1_05: Multitud furiosa marcha hacia un hotel de la Quinta Avenida
        cv = bg("fifth_ave_1896")
        grade(cv, tint=(1.06, 0.94, 0.82), dark=0.06)
        draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "QUINTA AVENIDA · 1896", t, t_05, border=PINK)
        window(cv, 76, 44, 328, 62, fill=(26, 16, 20), border=PINK, alpha=0.94)
        draw_text(cv, "MULTITUD FURIOSA · 1896", 240, 54, "press", 8, PINK, align="center")
        draw_text(cv, "MARCHA HACIA UN HOTEL ELEGANTE", 240, 74, "silk", 8, CREAM, align="center")
        mx1, mw1 = walk(t, t_05, t_06, 100, 260)
        mx2, mw2 = walk(t, t_05, t_06, 160, 320)
        char(cv, "mob_a", mx1, ground_y, t, scale=2, walk=mw1, look=1, brows="angry", l_arm="up")
        char(cv, "mob_b", mx2, ground_y, t, scale=2, walk=mw2, look=1, brows="angry", r_arm="up")
        return vignette(cv, 0.34)

    # c1_06: Tres libros olvidados con polvo -> ojos de 2017
    cv = bg("library_1893")
    grade(cv, tint=(1.04, 0.94, 0.82), dark=0.22)
    draw_chapter_header(cv, "CAP. 1 · EL ESCRITOR", "TRES LIBROS OLVIDADOS", t, t_06, border=GOLD)
    floor_prop(cv, draw_book_stack_prop, 240, ground_y)
    window(cv, 76, 46, 328, 66, fill=(18, 16, 24), border=GOLD, alpha=0.95)
    draw_text(cv, "TRES LIBROS OLVIDADOS", 240, 56, "press", 8, GOLD, align="center")
    draw_text(cv, "LEÍDOS CON LOS OJOS DE 2017", 240, 78, "silk", 8, CREAM, align="center")
    return vignette(cv, 0.38)


def scenes():
    return [
        (0.0, scene_opening, lambda t: cam_push(t, 0.0, TL.start("c1_00"), 1.0, 1.03)),
        (TL.start("c1_00") - 0.1, card_ch1, None),
        (TL.start("c1_01") - 0.1, scene_ch1_writer, lambda t: cam_push(t, TL.start("c1_01"), TL.end("c1_06"), 1.0, 1.03)),
    ]
