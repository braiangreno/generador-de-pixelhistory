"""Capítulo 7: Viajar al pasado — LA PIZARRA 3 (Paradoja del abuelo) + Fiesta de Hawking en Cambridge (2009)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch7 = make_card(7, ["VIAJAR AL PASADO"], "CAMBRIDGE, INGLATERRA · 2009")


def scene_ch7(t):
    t_01 = TL.start("c7_01")
    t_02 = TL.start("c7_02")
    t_03 = TL.start("c7_03")
    t_04 = TL.start("c7_04")
    t_05 = TL.start("c7_05")
    t_06 = TL.start("c7_06")
    t_07 = TL.start("c7_07")
    t_08 = TL.start("c7_08")
    ground_y = 224

    # c7_01..c7_04: LA PIZARRA 3 — VIAJAR AL PASADO
    if t < t_05:
        cv = draw_pizarra_frame(
            t, t_01, "LA PARADOJA DEL ABUELO",
            summary_es="AL PASADO, NADIE VINO",
            t_summary=t_08 + 10.0  # se muestra en el cierre de c7_08
        )
        d = ImageDraw.Draw(cv)
        window(cv, 76, 42, 328, 156, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.95)

        if t < t_02:
            # c7_01: Flecha del tiempo que da la vuelta
            draw_text(cv, "¿Y VIAJAR AL PASADO?", 240, 56, "press", 8, CHALK_YELLOW, align="center")
            d.arc([164, 84, 316, 156], 20, 320, fill=(*CHALK_CYAN, 255), width=3)
            d.polygon([(310, 102), (324, 96), (318, 114)], fill=(*CHALK_CYAN, 255))
            draw_text(cv, "AHÍ LA FÍSICA SE PONE DIFÍCIL", 240, 170, "silk", 8, CHALK_WHITE, align="center")
            draw_chalk_hand(cv, 318, 106, t)

        elif t < t_03:
            # c7_02: Viajero llega al pasado y se cruza con sus abuelos jóvenes
            draw_text(cv, "LA PARADOJA DEL ABUELO", 240, 54, "press", 8, CHALK_YELLOW, align="center")
            draw_text(cv, "VIAJAS AL PASADO", 156, 86, "press", 8, CHALK_CYAN, align="center")
            draw_text(cv, "EVITAS QUE SE CONOZCAN", 322, 86, "press", 8, CHALK_YELLOW, align="center")
            d.line([(218, 92), (254, 92)], fill=(*CHALK_WHITE, 255), width=2)
            draw_text(cv, "ENTONCES NUNCA NACISTE", 240, 126, "press", 8, PINK, align="center")
            draw_text(cv, "¿Y QUIÉN VIAJÓ?", 240, 154, "press", 16, CHALK_YELLOW, align="center")

        elif t < t_04:
            # c7_03: El dibujo se enreda como un nudo
            draw_text(cv, "CONTRADICCIÓN LÓGICA", 240, 54, "press", 8, CHALK_YELLOW, align="center")
            # Bucle / nudo en tiza
            pts = []
            for i in range(60):
                ang = i * 2 * math.pi / 60
                xx = 240 + int(math.sin(ang * 2) * 56)
                yy = 118 + int(math.sin(ang * 3) * 28)
                pts.append((xx, yy))
            d.line(pts, fill=(*CHALK_CYAN, 255), width=2)
            draw_text(cv, "IMPOSIBLE O SIN PODER CAMBIAR NADA", 240, 170, "silk", 8, CHALK_WHITE, align="center")

        else:
            # c7_04: Agujero de gusano (hoja doblada con atajo)
            draw_text(cv, "AGUJEROS DE GUSANO (TEORÍA)", 240, 54, "press", 8, CHALK_YELLOW, align="center")
            # Hoja doblada en U
            d.line([(130, 92), (320, 92)], fill=(*CHALK_WHITE, 255), width=2)
            d.line([(130, 146), (320, 146)], fill=(*CHALK_WHITE, 255), width=2)
            d.arc([296, 92, 344, 146], 270, 90, fill=(*CHALK_WHITE, 255), width=2)
            # Túnel atajo vertical brillante
            d.line([(190, 92), (190, 146)], fill=(*CHALK_CYAN, 255), width=4)
            draw_text(cv, "ATAJO", 232, 114, "press", 8, CHALK_CYAN, align="left")
            draw_text(cv, "NADIE SABE SI EXISTEN", 240, 170, "silk", 8, CHALK_GREEN, align="center")
            draw_chalk_hand(cv, 338, 120, t)

        return vignette(cv, 0.30)

    # c7_05: Rebobinado hasta Cambridge, 28 de junio de 2009 (sala elegante vacía, sin Hawking)
    if t < t_06:
        cv = bg("cambridge_hall_2009")
        draw_chapter_header(cv, "CAP. 7 · VIAJAR AL PASADO", "CAMBRIDGE · 28 DE JUNIO DE 2009", t, t_05, border=GOLD)
        floor_prop(cv, draw_party_table_prop, 240, ground_y)
        window(cv, 76, 44, 328, 72, fill=(18, 20, 32), border=GOLD, alpha=0.94)
        draw_text(cv, "CAMBRIDGE · 28 DE JUNIO DE 2009", 240, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "EXPERIMENTO DE STEPHEN HAWKING", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "FIESTA PARA VIAJEROS DEL TIEMPO", 240, 92, "silk", 8, CYAN, align="center")
        # Efecto visual de rebobinado durante el primer segundo
        if t < t_05 + 0.9:
            draw_text(cv, "<< REW", 446, 244, "press", 8, PINK, align="right")
        return vignette(cv, 0.34)

    if t < t_07:
        # c7_06: Sobre con invitación saliendo de una impresora al día siguiente
        cv = bg("cambridge_hall_2009")
        grade(cv, dark=0.14)
        draw_chapter_header(cv, "CAP. 7 · VIAJAR AL PASADO", "EL TRUCO DE LA INVITACIÓN", t, t_06, border=CYAN)
        p_out = prog(t, t_06 + 0.3, t_06 + 2.6)
        floor_prop(cv, lambda c, x, f: draw_printer_table_prop(c, x, f, p_out=p_out), 240, ground_y)
        window(cv, 76, 44, 328, 72, fill=(16, 20, 34), border=CYAN, alpha=0.95)
        draw_text(cv, "EL TRUCO DE HAWKING:", 240, 54, "press", 8, CYAN, align="center")
        draw_text(cv, "ENVIÓ LAS INVITACIONES DESPUÉS", 240, 74, "silk", 8, GOLD, align="center")
        draw_text(cv, "SOLO VIAJEROS PODÍAN ENTERARSE", 240, 92, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_08:
        # c7_07: Sala vacía, reloj avanza horas, no llegó nadie
        cv = bg("cambridge_hall_2009")
        grade(cv, dark=0.18)
        draw_chapter_header(cv, "CAP. 7 · VIAJAR AL PASADO", "NO LLEGÓ NADIE", t, t_07, border=GOLD)
        floor_prop(cv, draw_party_table_prop, 240, ground_y)
        draw_pocket_watch(cv, 240, 128, t, r=20, reverse=False, speed=4.2)
        window(cv, 76, 44, 328, 56, fill=(16, 18, 30), border=GOLD, alpha=0.95)
        draw_text(cv, "ESPERÓ UN BUEN RATO...", 240, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "NO LLEGÓ NADIE.", 240, 76, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.36)

    # c7_08: Rótulo EN UNA FRASE sobre pizarra
    cv = draw_pizarra_frame(
        t, t_08, "VIAJAR AL PASADO",
        summary_es="AL PASADO, NADIE VINO",
        t_summary=t_08
    )
    window(cv, 76, 48, 328, 124, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.95)
    draw_text(cv, "AL PASADO, NADIE VINO", 240, 72, "press", 16, CHALK_YELLOW, align="center")
    draw_text(cv, "SI SE PUDIERA VIAJAR AL PASADO,", 240, 114, "press", 8, CHALK_WHITE, align="center")
    draw_text(cv, "ESA FIESTA ESTARÍA LLENA.", 240, 138, "press", 8, CHALK_GREEN, align="center")
    return vignette(cv, 0.32)


def scenes():
    return [
        (TL.start("c7_00") - 0.1, card_ch7, None),
        (TL.start("c7_01") - 0.1, scene_ch7, None),
    ]
