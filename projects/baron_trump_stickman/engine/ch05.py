"""Capítulo 5: Cómo nace una teoría (Reddit/4chan 2017, rompecabezas, dominio público, Snopes)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch5 = make_card(5, ["CÓMO NACE UNA TEORÍA"], "INTERNET · 2017")


def _draw_puzzle_pieces(cv, sep=0.0, glued=False):
    """Dibuja 4 piezas de rompecabezas en el panel central que no encajan realmente."""
    d = ImageDraw.Draw(cv)
    pieces = [
        (140 - int(sep * 16), 92 - int(sep * 8), (168, 84, 62), "LIBRO"),
        (246 + int(sep * 16), 92 - int(sep * 8), (62, 128, 178), "TÍO"),
        (140 - int(sep * 16), 132 + int(sep * 8), (82, 152, 96), "TESLA"),
        (246 + int(sep * 16), 132 + int(sep * 8), (156, 98, 168), "TORRE"),
    ]
    for px, py, col, lbl in pieces:
        d.rectangle([px, py, px + 92, py + 32], fill=(*col, 255), outline=(*INK, 255), width=2)
        draw_text(cv, lbl, px + 46, py + 10, "press", 8, CREAM, align="center")
    if glued:
        d.line([(234, 96), (244, 158)], fill=(252, 232, 92, 220), width=4)
        d.line([(146, 128), (332, 128)], fill=(252, 232, 92, 220), width=4)


def scene_ch5(t):
    t_01 = TL.start("c5_01")
    t_02 = TL.start("c5_02")
    t_03 = TL.start("c5_03")
    t_04 = TL.start("c5_04")
    t_05 = TL.start("c5_05")
    t_06 = TL.start("c5_06")
    t_07 = TL.start("c5_07")
    ground_y = 224

    if t < t_02:
        # c5_01: Foro genérico de 2017: mensajes que se apilan
        cv = bg("forum_room_2017")
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "FOROS DE INTERNET · 2017", t, t_01, border=CYAN)
        floor_prop(cv, draw_forum_desk_prop, 240, ground_y)
        window(cv, 76, 44, 328, 82, fill=(14, 18, 32), border=CYAN, alpha=0.95)
        draw_text(cv, "FOROS DE INTERNET · 2017", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "CADA USUARIO SUMABA UNA PIEZA", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "MENSAJES · HILOS · TEORÍAS", 240, 96, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.34)

    if t < t_03:
        # c5_02: Piezas de rompecabezas separadas (todas reales)
        cv = bg("forum_room_2017")
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "PIEZAS REALES", t, t_02, border=GOLD)
        window(cv, 76, 44, 328, 152, fill=(16, 20, 34), border=GOLD, alpha=0.95)
        draw_text(cv, "NINGUNA PIEZA ERA FALSA DEL TODO", 240, 56, "press", 8, GOLD, align="center")
        _draw_puzzle_pieces(cv, sep=0.35, glued=False)
        draw_text(cv, "LOS LIBROS · EL TÍO · LOS PAPELES", 240, 174, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_04:
        # c5_03: Lo falso era el pegamento
        cv = bg("forum_room_2017")
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "EL PEGAMENTO", t, t_03, border=PINK)
        window(cv, 76, 44, 328, 152, fill=(22, 16, 28), border=PINK, alpha=0.95)
        draw_text(cv, "LO FALSO ERA EL PEGAMENTO", 240, 56, "press", 8, PINK, align="center")
        _draw_puzzle_pieces(cv, sep=0.0, glued=True)
        draw_text(cv, "NO ENCAJAN, PERO QUEDAN PEGADAS", 240, 174, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_05:
        # c5_04: Biblioteca digital genérica (dominio público gratis)
        cv = bg("library_1893")
        grade(cv, tint=(0.94, 0.98, 1.06), dark=0.14)
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "DOMINIO PÚBLICO", t, t_04, border=GREEN)
        floor_prop(cv, draw_book_stack_prop, 240, ground_y)
        window(cv, 76, 44, 328, 72, fill=(14, 24, 28), border=GREEN, alpha=0.95)
        draw_text(cv, "LIBROS DE DOMINIO PÚBLICO", 240, 54, "press", 8, GREEN, align="center")
        draw_text(cv, "GRATIS EN INTERNET · A UN CLIC", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "CUALQUIERA PODÍA REVISARLOS", 240, 92, "silk", 8, CYAN, align="center")
        return vignette(cv, 0.34)

    if t < t_06:
        # c5_05: Sello de verificado sobre los libros y falso sobre la máquina (Snopes)
        cv = bg("forum_room_2017")
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "VERIFICACIÓN DE DATOS", t, t_05, border=GREEN)
        window(cv, 76, 44, 328, 140, fill=(16, 20, 32), border=CYAN, alpha=0.96)
        draw_text(cv, "VERIFICACIÓN DE DATOS", 240, 56, "press", 8, CYAN, align="center")
        d = ImageDraw.Draw(cv)
        d.rectangle([98, 82, 232, 134], fill=(22, 58, 36, 255), outline=(*GREEN, 255), width=2)
        draw_text(cv, "LOS LIBROS", 165, 92, "silk", 8, CREAM, align="center")
        draw_text(cv, "REALES", 165, 110, "press", 8, GREEN, align="center")
        d.rectangle([248, 82, 382, 134], fill=(64, 22, 28, 255), outline=(*PINK, 255), width=2)
        draw_text(cv, "LA MÁQUINA", 315, 92, "silk", 8, CREAM, align="center")
        draw_text(cv, "FALSA", 315, 110, "press", 8, PINK, align="center")
        draw_text(cv, "BARON ES TÍTULO · DON TAMBIÉN", 240, 156, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.34)

    if t < t_07:
        # c5_06: Video vertical genérico con contador de vistas que sube
        cv = bg("forum_room_2017")
        draw_chapter_header(cv, "CAP. 5 · CÓMO NACE UNA TEORÍA", "MILLONES DE VISTAS", t, t_06, border=PINK)
        d = ImageDraw.Draw(cv)
        p_cnt = ease_out(prog(t, t_06, t_06 + 3.5))
        views = int(120000 + p_cnt * 4880000)
        window(cv, 76, 44, 328, 140, fill=(16, 18, 30), border=PINK, alpha=0.96)
        draw_text(cv, "VIDEOS CORTOS VIRALES", 240, 56, "press", 8, GOLD, align="center")
        draw_text(cv, f"{views:,}".replace(",", "."), 240, 88, "press", 16, PINK, align="center")
        draw_text(cv, "MILLONES DE VISTAS", 240, 124, "press", 8, CREAM, align="center")
        draw_text(cv, "SIEMPRE CON LAS MISMAS PIEZAS", 240, 148, "silk", 8, CYAN, align="center")
        return vignette(cv, 0.34)

    # c5_07: El rompecabezas se despega solo
    cv = new_canvas((12, 14, 22))
    p_sep = ease_out(prog(t, t_07, t_07 + 2.0))
    window(cv, 76, 46, 328, 152, fill=(18, 18, 28), border=GOLD, alpha=0.96)
    draw_text(cv, "UNA CASUALIDAD NO SE COMPARTE", 240, 58, "press", 8, GREY, align="center")
    _draw_puzzle_pieces(cv, sep=p_sep * 0.9, glued=False)
    draw_text(cv, "UNA CONSPIRACIÓN, SÍ.", 240, 174, "press", 8, GOLD, align="center")
    return vignette(cv, 0.38)


def scenes():
    return [
        (TL.start("c5_00") - 0.1, card_ch5, None),
        (TL.start("c5_01") - 0.1, scene_ch5, lambda t: cam_push(t, TL.start("c5_01"), TL.end("c5_07"), 1.0, 1.03)),
    ]
