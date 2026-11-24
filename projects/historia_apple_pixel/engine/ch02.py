"""Capítulo 2: El Turno de Medianoche (Atari y Breakout, 1974)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch2 = make_card(2, ["EL TURNO DE MEDIANOCHE"], "TALLER DE VIDEOJUEGOS · 1974")


def scene_ch2_main(t):
    t_01 = TL.start("c2_01")
    t_02 = TL.start("c2_02")
    t_03 = TL.start("c2_03")
    t_04 = TL.start("c2_04")
    t_05 = TL.start("c2_05")
    t_06 = TL.start("c2_06")

    cv = bg("atari_arcade_workshop_1974")
    grade(cv, tint=(1.04, 0.96, 0.88), dark=0.07)
    ground_y = 224

    if t < t_02:
        # c2_01: Dieta de frutas, sin ducha ni desodorante, compañeros quejándose
        draw_chapter_header(cv, t, t_01, "CAP. 2", "EL TURNO DE MEDIANOCHE", "ATARI · CALIFORNIA · 1974")
        floor_prop(cv, draw_atari_bench_prop, 240, ground_y)

        window(cv, 94, 48, 292, 56, fill=(24, 18, 30), border=CORAL, alpha=0.94)
        draw_text(cv, "JOBS A LOS 19 AÑOS · TÉCNICO EN ATARI", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "DIETA DE FRUTAS · SIN DUCHA NI DESODORANTE", 240, 76, "silk", 8, CORAL, align="center")

        char(cv, "jobs_1977", 154, ground_y, t, scale=2, look=1, r_arm="up", talk=talk_v(t, True))
        tx, tw, tlook = pace(t, t_01, 336, 404, period=2.2, pause=0.25)
        char(cv, "atari_tech", tx, ground_y, t, scale=2, walk=tw, look=-1, brows="sad", frown=True, l_arm="up")
        bubble(cv, "¡NO SE PUEDE RESPIRAR!", int(tx), ground_y - 104, align="center")

    elif t < t_03:
        # c2_02: Nolan Bushnell inventa el turno noche + "Dos Steves por el precio de uno"
        draw_place_only(cv, "EL TURNO DE LA NOCHE · «DOS STEVES POR EL PRECIO DE UNO»", t, t_02, border=GOLD)
        floor_prop(cv, draw_arcade_cabinet_prop, 240, ground_y)

        window(cv, 94, 42, 292, 62, fill=(16, 20, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "SOLUCIÓN: EL TURNO DE MEDIANOCHE", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "JOBS DEJABA ENTRAR A WOZNIAK DE NOCHE", 240, 70, "silk", 8, CREAM, align="center")
        draw_text(cv, "«DOS STEVES POR EL PRECIO DE UNO»", 240, 86, "silk", 8, CYAN, align="center")

        char(cv, "bushnell", 104, ground_y, t, scale=2, look=1, smile=True, r_arm="point", talk=talk_v(t, True))
        char(cv, "jobs_1977", 316, ground_y, t, scale=2, look=-1)
        char(cv, "wozniak_1977", 386, ground_y, t, scale=2, look=-1, smile=True)
        person_card(cv, "nolan_bushnell", "NOLAN BUSHNELL", "FUNDADOR DE ATARI · JEFE DE JOBS EN 1974",
                    t, t_02 + 0.35, dur=3.5)

    elif t < t_04:
        # c2_03: El encargo del juego de ladrillos: $700 + bono de $100 por cada chip menos
        draw_place_only(cv, "EL ENCARGO DE BREAKOUT · MENOS CHIPS = MÁS DINERO", t, t_03, border=CYAN)
        floor_prop(cv, draw_arcade_cabinet_prop, 240, ground_y)

        window(cv, 94, 42, 292, 68, fill=(14, 22, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "JUEGO DE ROMPER LADRILLOS", 240, 52, "press", 8, CYAN, align="center")
        draw_text(cv, "PAGO BASE: 700 DÓLARES", 240, 70, "press", 8, GOLD, align="center")
        draw_text(cv, "BONO SECRETO: +100 $ POR CADA CHIP MENOS", 240, 88, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "bushnell", 136, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "jobs_1977", 344, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_05:
        # c2_04: "Vamos mitad y mitad" · Wozniak 4 noches sin dormir -> 44 chips
        draw_place_only(cv, "4 NOCHES SIN DORMIR · EL MILAGRO DE LOS 44 CHIPS", t, t_04, border=GOLD)
        floor_prop(cv, draw_atari_bench_prop, 240, ground_y)

        p_cnt = clamp01((t - t_04) / 3.8)
        chips_now = int(round(100 - 56 * p_cnt))
        window(cv, 94, 42, 292, 68, fill=(16, 20, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "JOBS A WOZ: «VAMOS MITAD Y MITAD»", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, f"CHIPS EN LA PLACA: {chips_now}", 240, 70, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "4 DÍAS Y 4 NOCHES SIN DORMIR", 240, 88, "silk", 8, GOLD, align="center")

        char(cv, "wozniak_1977", 156, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "jobs_1977", 328, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_06:
        # c2_05: El cheque de $350 vs el bono oculto de $5.000
        draw_place_only(cv, "LA CUENTA DE JOBS · 350 DÓLARES CONTRA 5.000", t, t_05, border=CORAL)
        floor_prop(cv, draw_atari_bench_prop, 240, ground_y)

        window(cv, 94, 40, 292, 78, fill=(24, 16, 28), border=CORAL, alpha=0.96)
        draw_text(cv, "LO QUE JOBS LE DIO A WOZNIAK:", 240, 50, "silk", 8, CREAM, align="center")
        draw_text(cv, "CHEQUE: 350 DÓLARES (MITAD DE 700)", 240, 66, "press", 8, CYAN, align="center")
        draw_text(cv, "LO QUE JOBS COBRÓ EN SECRETO:", 240, 84, "silk", 8, GOLD, align="center")
        draw_text(cv, "BONO DE ATARI: 5.000 DÓLARES", 240, 100, "press", 8, CORAL, align="center")

        char(cv, "wozniak_1977", 148, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "jobs_1977", 332, ground_y, t, scale=2, look=-1)

    else:
        # c2_06: 10 años después, Wozniak se entera leyendo un libro
        grade(cv, tint=(0.88, 0.92, 1.05), dark=0.16)
        draw_place_only(cv, "10 AÑOS DESPUÉS · LA VERDAD EN UN LIBRO", t, t_06, border=CYAN)
        floor_prop(cv, draw_office_desk_1977, 240, ground_y)

        window(cv, 94, 44, 292, 68, fill=(14, 18, 34), border=CYAN, alpha=0.95)
        draw_text(cv, "10 AÑOS DESPUÉS · LEYENDO UN LIBRO", 240, 56, "press", 8, CYAN, align="center")
        draw_text(cv, "WOZNIAK DESCUBRIÓ EL BONO DE 5.000 $", 240, 74, "silk", 8, CREAM, align="center")
        draw_text(cv, "LLORÓ · PERO NUNCA ABANDONÓ A SU AMIGO", 240, 92, "silk", 8, GOLD, align="center")

        char(cv, "wozniak_1977", 174, ground_y, t, scale=2, look=1, brows="sad", frown=True)
        char(cv, "jobs_1977", 336, ground_y, t, scale=2, look=-1)

    return vignette(cv, 0.35)


def scenes():
    return [
        (TL.chapter_start(2) - 0.15, card_ch2, None),
        (TL.start("c2_01"), scene_ch2_main, lambda t: cam_push(t, TL.start("c2_01"), chapter_end(2), 1.0, 1.03)),
    ]
