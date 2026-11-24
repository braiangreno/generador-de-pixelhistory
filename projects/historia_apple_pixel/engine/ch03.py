"""Capítulo 3: Los Ochocientos Dólares Más Caros de la Historia (1976)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch3 = make_card(3, ["LOS 800 DÓLARES MÁS CAROS"], "GARAJE DE LOS ALTOS · 1976")


def scene_ch3_main(t):
    t_01 = TL.start("c3_01")
    t_02 = TL.start("c3_02")
    t_03 = TL.start("c3_03")
    t_04 = TL.start("c3_04")
    t_05 = TL.start("c3_05")
    t_06 = TL.start("c3_06")

    cv = bg("los_altos_garage_1976")
    grade(cv, tint=(1.04, 0.98, 0.90), dark=0.06)
    d = ImageDraw.Draw(cv)
    ground_y = 224

    if t < t_02:
        # c3_01: 1 de abril de 1976 (Día de los Inocentes) y tres firmas en el contrato
        draw_chapter_header(cv, t, t_01, "CAP. 3", "LOS 800 DÓLARES MÁS CAROS",
                            "LOS ALTOS · 1 DE ABRIL DE 1976 · DÍA DE LOS INOCENTES")
        floor_prop(cv, draw_garage_bench_1976, 240, ground_y)

        window(cv, 94, 48, 292, 64, fill=(16, 20, 36), border=GOLD, alpha=0.95)
        draw_text(cv, "1 DE ABRIL DE 1976 · FUNDACIÓN DE APPLE", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "JOBS (45%) · WOZNIAK (45%) · WAYNE (10%)", 240, 76, "silk", 8, CYAN, align="center")
        draw_text(cv, "EL TERCER SOCIO QUE CASI NADIE RECUERDA", 240, 92, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1977", 104, ground_y, t, scale=2, look=1)
        char(cv, "ronald_wayne", 168, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 364, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_03:
        # c3_02: Ronald Wayne (41 años), el contrato y el dibujo de Newton bajo un manzano (manzana entera)
        draw_place_only(cv, "RONALD WAYNE · 41 AÑOS · EL ADULTO EN LA HABITACIÓN", t, t_02, border=GOLD)
        floor_prop(cv, draw_garage_bench_1976, 240, ground_y)

        window(cv, 94, 42, 292, 92, fill=(18, 22, 38), border=GOLD, alpha=0.95)
        # Pergamino con Newton bajo un árbol y una manzana roja ENTERA (sin mordisco)
        draw_paper(cv, 92, 52, 56, 72)
        d.rectangle([116, 62, 122, 98], fill=(112, 72, 38, 255))
        d.ellipse([102, 54, 138, 78], fill=(54, 136, 72, 255), outline=(*INK, 255))
        # Manzana entera roja colgando de la rama
        d.ellipse([108, 72, 114, 78], fill=(218, 48, 44, 255), outline=(*INK, 255))
        # Silueta de Newton sentado leyendo al pie del tronco
        d.ellipse([122, 94, 130, 102], fill=(64, 52, 44, 255))
        d.rectangle([120, 102, 132, 114], fill=(48, 64, 98, 255))

        draw_text(cv, "RONALD WAYNE (10%)", 274, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "REDACTÓ EL PRIMER CONTRATO", 274, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "DIBUJÓ A NEWTON BAJO EL MANZANO", 274, 94, "silk", 8, CYAN, align="center")
        draw_text(cv, "TENÍA EL VOTO DE DESEMPATE", 274, 112, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "ronald_wayne", 118, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "jobs_1977", 382, ground_y, t, scale=2, look=-1)
        person_card(cv, "ronald_wayne", "RONALD WAYNE", "TERCER COFUNDADOR DE APPLE · 1976",
                    t, t_02 + 0.35, dur=3.5)

    elif t < t_04:
        # c3_03: Miedo a las deudas -> vende su 10% a los 12 días por 800 dólares
        draw_place_only(cv, "12 DÍAS DESPUÉS · OFICINA PÚBLICA · RENUNCIA AL 10%", t, t_03, border=CORAL)
        floor_prop(cv, draw_clerk_window_prop, 240, ground_y)

        window(cv, 94, 42, 292, 74, fill=(24, 18, 30), border=CORAL, alpha=0.95)
        draw_text(cv, "«YO TENÍA CASA Y AUTO · ELLOS NADA»", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "DURACIÓN COMO SOCIO: 12 DÍAS", 240, 70, "press", 8, GOLD, align="center")
        draw_text(cv, "VENDIÓ SU 10% POR 800 DÓLARES", 240, 90, "press", 8, CHALK_GREEN, align="center")

        char(cv, "ronald_wayne", 146, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "clerk_1976", 336, ground_y, t, scale=2, look=-1)

    elif t < t_05:
        # c3_04: $800 vs ~350.000 millones de dólares hoy
        draw_place_only(cv, "LOS 800 DÓLARES MÁS CAROS DE LA HISTORIA", t, t_04, border=GOLD)
        floor_prop(cv, draw_clerk_window_prop, 240, ground_y)

        window(cv, 94, 40, 292, 82, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "LO QUE COBRÓ EN ABRIL DE 1976: 800 $", 240, 50, "silk", 8, CYAN, align="center")
        draw_text(cv, "VALOR DE ESE 10% HOY:", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "≈ 350.000 MILLONES DE DÓLARES", 240, 84, "press", 8, GOLD, align="center")
        draw_text(cv, "«EL HOMBRE MÁS RICO DEL CEMENTERIO»", 240, 104, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "ronald_wayne", 156, ground_y, t, scale=2, look=1, smile=True, talk=talk_v(t, True))
        char(cv, "jobs_1977", 336, ground_y, t, scale=2, look=-1)

    elif t < t_06:
        # c3_05: Venta de la camioneta combi de Jobs y la calculadora científica de Wozniak
        draw_place_only(cv, "CAPITAL INICIAL · UNA CAMIONETA Y UNA CALCULADORA", t, t_05, border=CYAN)
        floor_prop(cv, draw_vw_van_prop, 240, ground_y)

        window(cv, 94, 42, 292, 68, fill=(14, 22, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "PRIMER PEDIDO: 50 COMPUTADORAS", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "JOBS VENDIÓ SU CAMIONETA COMBI", 240, 70, "silk", 8, CREAM, align="center")
        draw_text(cv, "WOZ VENDIÓ SU CALCULADORA CIENTÍFICA", 240, 88, "silk", 8, CYAN, align="center")

        char(cv, "jobs_1977", 124, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 356, ground_y, t, scale=2, look=-1, smile=True)

    else:
        # c3_06: El precio de la Apple I: 666,66 dólares porque a Woz le gustaban los números repetidos
        draw_place_only(cv, "APPLE I · LA PLACA VERDE DE 666,66 DÓLARES", t, t_06, border=GOLD)
        floor_prop(cv, draw_garage_bench_1976, 240, ground_y)

        window(cv, 94, 42, 292, 78, fill=(16, 22, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "PRIMERA COMPUTADORA APPLE (SIN TECLADO)", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "PRECIO: 666,66 DÓLARES", 240, 70, "press", 16, GOLD, align="center")
        draw_text(cv, "A WOZ LE GUSTABAN LOS DÍGITOS REPETIDOS", 240, 98, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "wozniak_1977", 148, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "jobs_1977", 332, ground_y, t, scale=2, look=-1, smile=True)

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(3) - 0.15, card_ch3, None),
        (TL.start("c3_01"), scene_ch3_main, lambda t: cam_push(t, TL.start("c3_01"), chapter_end(3), 1.0, 1.03)),
    ]
