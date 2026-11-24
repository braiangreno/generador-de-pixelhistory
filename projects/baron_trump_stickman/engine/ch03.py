"""Capítulo 3: Millones de libros — LA PIZARRA 1 (Paradoja del cumpleaños y Ley de los Números Grandes)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch3 = make_card(3, ["MILLONES DE LIBROS"], "LA PIZARRA · PROBABILIDAD")


def scene_ch3_pizarra(t):
    t_01 = TL.start("c3_01")
    t_02 = TL.start("c3_02")
    t_03 = TL.start("c3_03")
    t_04 = TL.start("c3_04")
    t_05 = TL.start("c3_05")
    t_06 = TL.start("c3_06")
    t_07 = TL.start("c3_07")

    cv = draw_pizarra_frame(
        t, t_01, "LEY DE LOS NÚMEROS GRANDES",
        summary_es="ENTRE MILLONES DE LIBROS, UNO ACIERTA",
        t_summary=t_07 + 0.2
    )
    d = ImageDraw.Draw(cv)
    window(cv, 76, 42, 328, 156, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.95)

    if t < t_02:
        # c3_01: Biblioteca que no termina nunca en tiza
        draw_text(cv, "¿CÓMO ACERTÓ UN LIBRO DE 1893?", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        for row in range(3):
            y_sh = 96 + row * 28
            d.line([(106, y_sh), (374, y_sh)], fill=(*CHALK_WHITE, 220), width=2)
            for bx in range(112, 368, 14):
                bh = 16 + ((bx + row * 5) % 7)
                d.rectangle([bx, y_sh - bh, bx + 9, y_sh - 1], outline=(*CHALK_CYAN, 220), width=1)
        draw_text(cv, "VAMOS A LA PIZARRA", 240, 172, "silk", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, 340, 124, t)

    elif t < t_03:
        # c3_02: Sala con 23 personas y dos tortas de cumpleaños iguales
        draw_text(cv, "PARADOJA DEL CUMPLEAÑOS", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        # 23 cabecitas en tiza
        for i in range(23):
            cx = 114 + (i % 8) * 34
            cy = 84 + (i // 8) * 26
            col = CHALK_YELLOW if i in (4, 15) else CHALK_WHITE
            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(*col, 255), width=2)
        draw_text(cv, "23 PERSONAS -> MÁS DEL 50%", 240, 154, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "DE PROBABILIDAD DE COINCIDIR", 240, 174, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, 320, 132, t)

    elif t < t_04:
        # c3_03: Líneas que unen a cada persona con todas las demás -> 253 parejas
        draw_text(cv, "253 PAREJAS POSIBLES", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        pts = []
        for i in range(14):
            ang = i * 2 * math.pi / 14
            pts.append((240 + int(math.cos(ang) * 74), 124 + int(math.sin(ang) * 42)))
        p_net = ease_out(prog(t, t_03, t_03 + 2.5))
        total_pairs = len(pts) * (len(pts) - 1) // 2
        lim = int(total_pairs * p_net)
        cnt = 0
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if cnt >= lim:
                    break
                d.line([pts[i], pts[j]], fill=(*CHALK_CYAN, 120), width=1)
                cnt += 1
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(*CHALK_YELLOW, 255))
        num_disp = int(round(253 * p_net))
        draw_text(cv, f"{num_disp} PAREJAS", 240, 174, "press", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, 314, 124, t)

    elif t < t_05:
        # c3_04: Biblioteca enorme del siglo XIX con miles de personajes
        draw_text(cv, "MILLONES DE LIBROS DEL SIGLO XIX", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        d.rectangle([108, 84, 212, 152], outline=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "MILES DE", 160, 102, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "PERSONAJES", 160, 122, "silk", 8, CHALK_WHITE, align="center")
        d.line([(218, 118), (262, 118)], fill=(*CHALK_YELLOW, 255), width=2)
        d.rectangle([268, 84, 372, 152], outline=(*CHALK_YELLOW, 255), width=2)
        draw_text(cv, "MILLONES", 320, 102, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "BUSCANDO", 320, 122, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "COMBINACIONES CASI INFINITAS", 240, 172, "silk", 8, CHALK_GREEN, align="center")

    elif t < t_06:
        # c3_05: Televisor genérico con familia de dibujos genérica (sin logos)
        draw_text(cv, "EL MISMO EFECTO EN TELEVISIÓN", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        # TV en tiza
        d.rectangle([148, 80, 268, 154], outline=(*CHALK_WHITE, 255), width=2)
        d.line([(196, 80), (182, 66)], fill=(*CHALK_WHITE, 255), width=2)
        d.line([(218, 80), (232, 66)], fill=(*CHALK_WHITE, 255), width=2)
        # 4 siluetas genéricas de familia
        for fx in (172, 196, 220, 244):
            d.ellipse([fx - 6, 104, fx + 6, 116], outline=(*CHALK_YELLOW, 255), width=2)
            d.line([(fx, 116), (fx, 138)], fill=(*CHALK_YELLOW, 255), width=2)
        draw_text(cv, "AÑO 2000", 332, 96, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "ERA UN CHISTE", 332, 116, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "NO PROFECÍA", 332, 134, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "CIENTOS DE EPISODIOS Y CHISTES", 240, 172, "silk", 8, CHALK_WHITE, align="center")

    elif t < t_07:
        # c3_06: Flecha clavada en la pared; después alguien dibuja el blanco alrededor
        draw_text(cv, "LA FALACIA DEL FRANCOTIRADOR", 240, 54, "press", 8, CHALK_YELLOW, align="center")
        cx, cy = 240, 118
        p_ring = ease_out(prog(t, t_06 + 1.2, t_06 + 3.2))
        if p_ring > 0.05:
            for rad, col in ((34, CHALK_WHITE), (22, CHALK_CYAN), (11, CHALK_YELLOW)):
                rr = int(rad * p_ring)
                if rr > 2:
                    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(*col, 255), width=2)
        # Flecha clavada en el centro
        d.line([(cx - 48, cy - 18), (cx, cy)], fill=(*CHALK_GREEN, 255), width=3)
        d.polygon([(cx, cy), (cx - 10, cy - 8), (cx - 6, cy + 4)], fill=(*CHALK_GREEN, 255))
        draw_text(cv, "DIBUJAR EL BLANCO DESPUÉS DE TIRAR", 240, 172, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, cx + 26, cy + 16, t)

    else:
        # c3_07: Remate EN UNA FRASE
        draw_text(cv, "LEY DE LOS NÚMEROS GRANDES", 240, 74, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "ENTRE MILLONES DE LIBROS,", 240, 108, "press", 8, CHALK_WHITE, align="center")
        draw_text(cv, "ALGUNO TENÍA QUE ACERTAR.", 240, 132, "press", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.30)


def scenes():
    return [
        (TL.start("c3_00") - 0.1, card_ch3, None),
        (TL.start("c3_01") - 0.1, scene_ch3_pizarra, None),
    ]
