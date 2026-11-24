"""Capítulo 7: El Auto Sin Patente y el Enemigo en Pantalla Gigante (1996–2000)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch7 = make_card(7, ["EL AUTO SIN PATENTE"], "CUPERTINO Y BOSTON · 1996–2000")


def scene_ch7_main(t):
    t_01 = TL.start("c7_01")
    t_02 = TL.start("c7_02")
    t_03 = TL.start("c7_03")
    t_04 = TL.start("c7_04")
    t_05 = TL.start("c7_05")
    t_06 = TL.start("c7_06")

    ground_y = 224

    if t < t_02:
        # c7_01: Mediados de los 90 · Apple a 90 días de la quiebra
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(0.90, 0.92, 1.02), dark=0.14)
        draw_chapter_header(cv, t, t_01, "CAP. 7", "EL AUTO SIN PATENTE",
                            "MEDIADOS DE LOS 90 · APPLE AL BORDE DE LA QUIEBRA")
        floor_prop(cv, draw_office_desk_1977, 240, ground_y)

        window(cv, 94, 48, 292, 66, fill=(26, 16, 24), border=CORAL, alpha=0.95)
        draw_text(cv, "1996 · FALTABAN 90 DÍAS PARA QUEBRAR", 240, 58, "press", 8, CORAL, align="center")
        draw_text(cv, "4 JEFES DISTINTOS · MIL PRODUCTOS CONFUSOS", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "PÉRDIDAS DE CIENTOS DE MILLONES", 240, 94, "silk", 8, GOLD, align="center")

        char(cv, "mike_scott", 142, ground_y, t, scale=2, look=1, brows="sad", frown=True)
        char(cv, "atari_tech", 342, ground_y, t, scale=2, look=-1, brows="sad", frown=True)

    elif t < t_03:
        # c7_02: Diciembre de 1996 · Apple compra NeXT y vuelve el Empleado Número Cero por 1 dólar
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(0.98, 1.0, 1.06), dark=0.06)
        draw_place_only(cv, "DICIEMBRE DE 1996 · EL REGRESO DEL EMPLEADO Nº 0", t, t_02, border=GOLD)
        floor_prop(cv, draw_next_cube_prop, 240, ground_y)

        window(cv, 94, 40, 292, 86, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_employee_badge(cv, 136, 82, num_str="0", flip_p=math.cos(t * 2.2), scale=1)
        draw_text(cv, "APPLE COMPRA LA EMPRESA DE JOBS", 264, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "REGRESA EL EMPLEADO NÚMERO CERO", 264, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "SUELDO ANUAL: 1 DÓLAR", 264, 90, "press", 8, CHALK_GREEN, align="center")

        char(cv, "jobs_1997", 146, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "mac_coder", 338, ground_y, t, scale=2, look=-1, smile=True)
        person_card(cv, "steve_jobs_2007", "STEVE JOBS (1997)", "REGRESA A APPLE · SUELDO DE 1 DÓLAR",
                    t, t_02 + 0.35, dur=3.5)

    elif t < t_04:
        # c7_03: Agosto de 1997 en Boston · Bill Gates en pantalla gigante e inversión de 150 millones
        cv = bg("boston_macworld_1997")
        grade(cv, tint=(0.94, 0.98, 1.08), dark=0.06)
        draw_place_only(cv, "BOSTON · AGOSTO DE 1997 · EL RIVAL EN PANTALLA GIGANTE", t, t_03, border=CYAN)
        d = ImageDraw.Draw(cv)

        window(cv, 94, 38, 292, 92, fill=(14, 24, 42), border=CYAN, alpha=0.96)
        # Retrato de Bill Gates dentro de la pantalla gigante del teatro
        p_gates = portrait("bill_gates_1997").resize((48, 48), Image.NEAREST)
        paste(cv, p_gates, 110, 56)
        d.rectangle([109, 55, 159, 105], outline=(*CYAN, 255), width=1)
        draw_text(cv, "EN VIVO VÍA SATÉLITE:", 272, 52, "silk", 8, CYAN, align="center")
        draw_text(cv, "BILL GATES", 272, 68, "press", 8, GOLD, align="center")
        draw_text(cv, "RESCATE: 150 MILLONES DE DÓLARES", 272, 88, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "Y PROGRAMAS PARA LAS COMPUTADORAS MAC", 272, 106, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1997", 148, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "fair_visitor", 342, ground_y, t, scale=2, look=-1, brows="angry", frown=True, l_arm="up")
        person_card(cv, "bill_gates_1997", "BILL GATES", "FUNDADOR DE MICROSOFT · INVERSOR EN 1997",
                    t, t_03 + 0.4, dur=3.5)

    elif t < t_05:
        # c7_04: Abucheos del público y la frase de Jobs que salvó a Apple
        cv = bg("boston_macworld_1997")
        grade(cv, tint=(0.94, 0.98, 1.08), dark=0.06)
        draw_place_only(cv, "FIN DE LA GUERRA · EL DISCURSO QUE SALVÓ A APPLE", t, t_04, border=GOLD)

        window(cv, 94, 42, 292, 78, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "EL PÚBLICO ABUCHEÓ LA PANTALLA", 240, 52, "press", 8, CORAL, align="center")
        draw_text(cv, "JOBS CALMÓ A LA SALA:", 240, 70, "silk", 8, CYAN, align="center")
        draw_text(cv, "«PARA QUE APPLE GANE, NO HACE FALTA", 240, 86, "silk", 8, GOLD, align="center")
        draw_text(cv, "QUE EL OTRO TENGA QUE PERDER»", 240, 100, "silk", 8, GOLD, align="center")

        char(cv, "jobs_1997", 156, ground_y, t, scale=2, look=1, r_arm="up", talk=talk_v(t, True))
        char(cv, "fair_visitor", 336, ground_y, t, scale=2, look=-1)

    elif t < t_06:
        # c7_05: El auto deportivo plateado sin patente estacionado en el campus
        cv = bg("mac_pirate_building_1983")
        grade(cv, tint=(0.98, 1.0, 1.04), dark=0.06)
        draw_place_only(cv, "ESTACIONAMIENTO DE CUPERTINO · EL AUTO SIN PATENTE", t, t_05, border=CYAN)
        floor_prop(cv, draw_silver_car_prop, 240, ground_y)

        window(cv, 94, 42, 292, 72, fill=(16, 22, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "EL MISTERIO DEL DEPORTIVO PLATEADO", 240, 52, "press", 8, CYAN, align="center")
        draw_text(cv, "NUNCA LLEVÓ PATENTE · NI UN SOLO DÍA", 240, 70, "press", 8, CORAL, align="center")
        draw_text(cv, "¿PAGABA MULTAS? ¿TENÍA PERMISO ESPECIAL?", 240, 90, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1997", 132, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "security_chief", 348, ground_y, t, scale=2, look=-1, r_arm="point", talk=talk_v(t, True))

    else:
        # c7_06: El hueco en la ley de tránsito de California: un auto idéntico nuevo cada 6 meses
        cv = bg("mac_pirate_building_1983")
        grade(cv, tint=(1.0, 1.02, 1.04), dark=0.06)
        draw_place_only(cv, "EL TRUCO LEGAL · UNO NUEVO CADA 180 DÍAS", t, t_06, border=GOLD)
        floor_prop(cv, draw_silver_car_prop, 240, ground_y)

        window(cv, 94, 40, 292, 82, fill=(16, 22, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "LEY DE TRÁNSITO DE CALIFORNIA:", 240, 50, "silk", 8, CYAN, align="center")
        draw_text(cv, "6 MESES DE PLAZO PARA PONER LA CHAPA", 240, 66, "press", 8, GOLD, align="center")
        draw_text(cv, "AL DÍA 180 LO CAMBIABA POR OTRO IGUAL", 240, 86, "silk", 8, CREAM, align="center")
        draw_text(cv, "100% LEGAL · 0 PATENTE EN TODA SU VIDA", 240, 102, "press", 8, CHALK_GREEN, align="center")

        char(cv, "jobs_1997", 136, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "security_chief", 346, ground_y, t, scale=2, look=-1, smile=True)

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(7) - 0.15, card_ch7, None),
        (TL.start("c7_01"), scene_ch7_main, lambda t: cam_push(t, TL.start("c7_01"), chapter_end(7), 1.0, 1.03)),
    ]
