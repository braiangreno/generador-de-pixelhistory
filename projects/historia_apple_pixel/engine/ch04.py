"""Capítulo 4: La Computadora Falsa y la que Había que Tirar Contra la Mesa (1977–1980)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch4 = make_card(4, ["LA COMPUTADORA FALSA"], "FERIA DE SAN FRANCISCO · 1977–1980")


def scene_ch4_main(t):
    t_01 = TL.start("c4_01")
    t_02 = TL.start("c4_02")
    t_03 = TL.start("c4_03")
    t_04 = TL.start("c4_04")
    t_05 = TL.start("c4_05")
    t_06 = TL.start("c4_06")

    cv = bg("sf_computer_fair_1977")
    grade(cv, tint=(1.02, 0.98, 0.92), dark=0.06)
    d = ImageDraw.Draw(cv)
    ground_y = 224

    if t < t_02:
        # c4_01: Feria de San Francisco (1977) · Apple II con carcasa plástica beige
        draw_chapter_header(cv, t, t_01, "CAP. 4", "LA COMPUTADORA FALSA",
                            "FERIA DE SAN FRANCISCO · ABRIL DE 1977")
        floor_prop(cv, draw_fair_booth_prop, 240, ground_y)

        window(cv, 94, 48, 292, 56, fill=(16, 22, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "APPLE II · CARCASA DE PLÁSTICO BEIGE", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "TECLADO Y COLOR · LISTA PARA EL HOGAR", 240, 76, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1977", 142, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 338, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_03:
        # c4_02: Los 8.000 folletos falsos de Wozniak para la computadora "ZALTAIR"
        draw_place_only(cv, "LA BROMA SECRETA DE WOZNIAK · 8.000 FOLLETOS «ZALTAIR»", t, t_02, border=CYAN)
        floor_prop(cv, draw_fair_booth_prop, 240, ground_y)

        window(cv, 94, 40, 292, 80, fill=(14, 24, 38), border=CYAN, alpha=0.95)
        draw_text(cv, "FOLLETO FALSO: «LA NUEVA ZALTAIR»", 240, 50, "press", 8, CYAN, align="center")
        draw_text(cv, "«IMAGINA UN AUTO CON CINCO RUEDAS»", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "1º PUESTO: ZALTAIR (INVENTADA)", 240, 86, "silk", 8, GOLD, align="center")
        draw_text(cv, "2º PUESTO: APPLE II", 240, 102, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "wozniak_1977", 144, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "fair_visitor", 344, ground_y, t, scale=2, look=-1)

    elif t < t_04:
        # c4_03: Jobs se cree el folleto falso y festeja el segundo puesto
        draw_place_only(cv, "JOBS CAYÓ EN LA TRAMPA · «¡QUEDAMOS SEGUNDOS!»", t, t_03, border=GOLD)
        floor_prop(cv, draw_fair_booth_prop, 240, ground_y)

        window(cv, 94, 42, 292, 70, fill=(16, 20, 36), border=GOLD, alpha=0.95)
        draw_text(cv, "JOBS NO SABÍA QUE ERA UNA BROMA", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "MOSTRABA ORGULLOSO LA TABLA FALSA:", 240, 70, "silk", 8, CREAM, align="center")
        draw_text(cv, "«¡NO ESTÁ NADA MAL QUEDAR SEGUNDOS!»", 240, 88, "silk", 8, CYAN, align="center")

        char(cv, "jobs_1977", 152, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 336, ground_y, t, scale=2, look=-1, smile=True)
        bubble(cv, "¡SOMOS SEGUNDOS!", 152, ground_y - 104, align="center")

    elif t < t_05:
        # c4_04: 1980 · Apple III sin ventilador, calentándose y expulsando chips
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(1.08, 0.92, 0.88), dark=0.08)
        draw_place_only(cv, "CUPERTINO · 1980 · LA COMPUTADORA SIN VENTILADOR", t, t_04, border=CORAL)
        floor_prop(cv, draw_office_desk_1977, 240, ground_y)

        window(cv, 94, 40, 292, 86, fill=(28, 16, 22), border=CORAL, alpha=0.95)
        draw_text(cv, "1980 · JOBS PROHIBIÓ EL VENTILADOR", 240, 50, "press", 8, CORAL, align="center")
        draw_text(cv, "«HACEN RUIDO Y SON POCO ELEGANTES»", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "LA PLACA HERVÍA Y LOS CHIPS SE SALÍAN", 240, 86, "silk", 8, GOLD, align="center")
        # Olas de calor rojas en el panel
        for wx_i in range(140, 340, 32):
            wy_i = 108 + int(round(math.sin(t * 8 + wx_i) * 3))
            d.line([(wx_i, wy_i), (wx_i + 16, wy_i)], fill=(*CORAL, 255), width=2)

        char(cv, "jobs_1977", 136, ground_y, t, scale=2, look=1, brows="angry", frown=True)
        char(cv, "atari_tech", 344, ground_y, t, scale=2, look=-1, brows="sad", l_arm="up", talk=talk_v(t, True))

    elif t < t_06:
        # c4_05: Instrucción oficial de soporte técnico: levantarla 8 centímetros
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(1.04, 0.96, 0.90), dark=0.06)
        draw_place_only(cv, "MANUAL OFICIAL DE SOPORTE TÉCNICO · 1980", t, t_05, border=GOLD)
        floor_prop(cv, draw_office_desk_1977, 240, ground_y)

        lift_p = ease_in_out(clamp01((t - t_05) / 2.2))
        comp_y = int(round(98 - lift_p * 14))
        window(cv, 94, 40, 292, 92, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "SOLUCIÓN OFICIAL POR TELÉFONO:", 240, 50, "press", 8, GOLD, align="center")
        draw_text(cv, "1. APAGUE LA COMPUTADORA", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "2. LEVÁNTELA UNOS CENTÍMETROS...", 240, 84, "silk", 8, CYAN, align="center")
        # Mini computadora beige levantándose dentro del panel
        d.rectangle([216, comp_y, 264, comp_y + 18], fill=(230, 220, 194, 255), outline=(*INK, 255))
        d.line([(190, 118), (290, 118)], fill=(*GOLD, 255), width=2)

        char(cv, "atari_tech", 142, ground_y, t, scale=2, look=1, r_arm="up", talk=talk_v(t, True))
        char(cv, "fair_visitor", 338, ground_y, t, scale=2, look=-1, l_arm="up")

    else:
        # c4_06: "...y suéltala" -> golpe seco contra la mesa con rebote del fotograma
        cv = bg("cupertino_office_1977")
        grade(cv, tint=(1.04, 0.98, 0.92), dark=0.06)
        draw_place_only(cv, "«...Y SUÉLTALA CONTRA EL ESCRITORIO»", t, t_06, border=CHALK_GREEN)
        floor_prop(cv, draw_office_desk_1977, 240, ground_y)

        dt = t - t_06
        drop_t = 0.55
        window(cv, 94, 40, 292, 92, fill=(16, 24, 34), border=CHALK_GREEN, alpha=0.96)
        draw_text(cv, "3. «...Y SUÉLTALA»", 240, 52, "press", 16, GOLD, align="center")
        draw_text(cv, "EL GOLPE SECO METÍA LOS CHIPS EN SU LUGAR", 240, 78, "silk", 8, CREAM, align="center")
        draw_text(cv, "Y LA MÁQUINA VOLVÍA A ARRANCAR", 240, 96, "silk", 8, CHALK_GREEN, align="center")

        char(cv, "atari_tech", 142, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "fair_visitor", 338, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")
        bubble(cv, "¡FUNCIONÓ!", 338, ground_y - 104, align="center")

        # Rebote del fotograma entero cuando cae contra el escritorio
        _, dy_sh = shake(t, t_06 + drop_t, dur=0.45, amp=4)
        cv = offset_canvas(cv, 0, dy_sh)

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(4) - 0.15, card_ch4, None),
        (TL.start("c4_01"), scene_ch4_main, lambda t: cam_push(t, TL.start("c4_01"), chapter_end(4), 1.0, 1.03)),
    ]
