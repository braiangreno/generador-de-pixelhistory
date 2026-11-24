"""Capítulo 5: Piratas y un Cuaderno de Dos Dólares con Cincuenta (1983–1984)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch5 = make_card(5, ["PIRATAS Y UN CUADERNO"], "CUPERTINO · 1983–1984")


def scene_pizarra_32x32(t):
    """La Pizarra 2: 32 por 32 y el cuaderno de $2,50 de Susan Kare (c5_05..c5_07)."""
    t0 = TL.start("c5_05")
    t_06 = TL.start("c5_06")
    t_07 = TL.start("c5_07")

    cv = draw_pizarra_frame(t, t0, "32 POR 32 (EL CUADERNO DE 2,50 $)",
                            summary_es="MIL CUADRADITOS, UNA IDEA", t_summary=t_07 + 2.4)
    d = ImageDraw.Draw(cv)

    window(cv, 94, 42, 292, 154, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.94)

    if t < t_06:
        # c5_05: Comandos crípticos de texto vs el nacimiento de los dibujitos (Susan Kare)
        draw_text(cv, "ANTES DE 1984: SOLO TEXTO CRÍPTICO", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        d.rectangle([118, 72, 224, 136], fill=(10, 26, 18, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "C:\\> DEL *.*", 171, 84, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "SYNTAX ERROR", 171, 102, "silk", 8, CORAL, align="center")
        draw_text(cv, "?", 171, 118, "press", 8, CHALK_WHITE, align="center")

        d.rectangle([254, 72, 362, 136], fill=(228, 236, 244, 255), outline=(*CHALK_CYAN, 255))
        draw_text(cv, "DIBUJOS CLAROS", 308, 86, "silk", 8, INK, align="center")
        draw_text(cv, "PAPELERA · RELOJ", 308, 106, "silk", 8, INK, align="center")
        draw_text(cv, "ARTISTA: SUSAN KARE (ESCULTORA)", 240, 156, "press", 8, CHALK_CYAN, align="center")
        person_card(cv, "susan_kare", "SUSAN KARE", "DISEÑADORA DE LOS ÍCONOS DE MACINTOSH",
                    t, t0 + 0.4, dur=3.4)

    elif t < t_07:
        # c5_06: Cuaderno cuadriculado de $2,50 -> grilla de 32x32 = 1.024 cuadraditos
        draw_text(cv, "CUADERNO DE 2,50 $ · GRILLA 32 × 32", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        gx0, gy0 = 132, 72
        cell = 7
        for r in range(10):
            for c in range(10):
                x0 = gx0 + c * cell
                y0 = gy0 + r * cell
                # Dibujar carita sonriente pixelada en la cuadrícula
                is_on = (
                    (r in (0, 9) and 2 <= c <= 7) or
                    (c in (0, 9) and 1 <= r <= 8) or
                    (r == 3 and c in (3, 6)) or
                    (r == 6 and c in (2, 7)) or
                    (r == 7 and 3 <= c <= 6)
                )
                col_cell = CHALK_YELLOW if is_on else (22, 54, 38)
                d.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1],
                            fill=(*col_cell, 255), outline=(44, 88, 62, 255))
        draw_text(cv, "32 × 32 =", 292, 82, "press", 8, CHALK_WHITE, align="center")
        draw_text(cv, "1.024", 292, 100, "press", 16, CHALK_YELLOW, align="center")
        draw_text(cv, "CUADRADITOS", 292, 122, "press", 8, CHALK_CYAN, align="center")
        draw_text(cv, "1 CUADRADITO PINTADO = 1 PÍXEL EN PANTALLA", 240, 164, "silk", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, gx0 + 56, gy0 + 48, t)

    else:
        # c5_07: Los 3 íconos universales: tijera (cortar), tacho (borrar), compu feliz (bienvenida)
        draw_text(cv, "TRES DIBUJOS QUE CAMBIARON EL MUNDO", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        boxes = [
            (136, "TIJERA", "CORTAR"),
            (240, "TACHO", "BORRAR"),
            (344, "SONRISA", "HOLA"),
        ]
        for idx_b, (cx_b, top_l, bot_l) in enumerate(boxes):
            d.rectangle([cx_b - 32, 74, cx_b + 32, 134], fill=(18, 46, 32, 255), outline=(*CHALK_CYAN, 255))
            if idx_b == 0:
                d.ellipse([cx_b - 12, 98, cx_b - 4, 106], outline=(*CHALK_WHITE, 255), width=2)
                d.ellipse([cx_b + 4, 98, cx_b + 12, 106], outline=(*CHALK_WHITE, 255), width=2)
                d.line([(cx_b - 6, 98), (cx_b + 10, 82)], fill=(*CHALK_YELLOW, 255), width=2)
                d.line([(cx_b + 6, 98), (cx_b - 10, 82)], fill=(*CHALK_YELLOW, 255), width=2)
            elif idx_b == 1:
                d.rectangle([cx_b - 10, 88, cx_b + 10, 112], outline=(*CHALK_WHITE, 255), width=2)
                d.line([(cx_b - 12, 85), (cx_b + 12, 85)], fill=(*CHALK_YELLOW, 255), width=2)
            else:
                d.rectangle([cx_b - 12, 84, cx_b + 12, 112], outline=(*CHALK_YELLOW, 255), width=2)
                d.point((cx_b - 4, 92), fill=(*CHALK_WHITE, 255))
                d.point((cx_b + 4, 92), fill=(*CHALK_WHITE, 255))
                d.line([(cx_b - 5, 102), (cx_b + 5, 102)], fill=(*CHALK_GREEN, 255), width=2)
            draw_text(cv, top_l, cx_b, 118, "silk", 8, CHALK_WHITE, align="center")
            draw_text(cv, bot_l, cx_b, 142, "press", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.28)


def scene_ch5_main(t):
    t_01 = TL.start("c5_01")
    t_02 = TL.start("c5_02")
    t_03 = TL.start("c5_03")
    t_04 = TL.start("c5_04")
    t_05 = TL.start("c5_05")

    if t >= t_05:
        return scene_pizarra_32x32(t)

    ground_y = 224

    if t < t_04:
        cv = bg("mac_pirate_building_1983")
        grade(cv, tint=(0.96, 0.98, 1.06), dark=0.07)
        floor_prop(cv, draw_pirate_flag_prop, 240, ground_y)

        if t < t_02:
            # c5_01: "Es mejor ser pirata que alistarse en la marina"
            draw_chapter_header(cv, t, t_01, "CAP. 5", "PIRATAS Y UN CUADERNO",
                                "CUPERTINO · 1983 · EL GRUPO REBELDE MACINTOSH")
            window(cv, 94, 48, 292, 62, fill=(16, 20, 38), border=GOLD, alpha=0.95)
            draw_text(cv, "EL LEMA DE JOBS PARA SU EQUIPO:", 240, 58, "silk", 8, CYAN, align="center")
            draw_text(cv, "«ES MEJOR SER PIRATA", 240, 74, "press", 8, GOLD, align="center")
            draw_text(cv, "QUE ALISTARSE EN LA MARINA»", 240, 90, "press", 8, CREAM, align="center")

            char(cv, "jobs_1977", 142, ground_y, t, scale=2, look=1, r_arm="up", talk=talk_v(t, True))
            char(cv, "mac_coder", 338, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

        elif t < t_03:
            # c5_02: Bandera pirata cosida a mano izada en el techo del edificio
            draw_place_only(cv, "UNA BANDERA PIRATA REAL EN EL TECHO DE APPLE", t, t_02, border=CYAN)
            window(cv, 94, 42, 292, 66, fill=(16, 20, 38), border=CYAN, alpha=0.95)
            draw_text(cv, "BANDERA NEGRA PINTADA A MANO", 240, 52, "press", 8, CYAN, align="center")
            draw_text(cv, "CALAVERA Y PARCHE EN EL OJO", 240, 70, "silk", 8, CREAM, align="center")
            draw_text(cv, "FLAMEANDO SOBRE EL EDIFICIO DE MACINTOSH", 240, 88, "silk", 8, GOLD, align="center")

            char(cv, "mac_coder", 148, ground_y, t, scale=2, look=1, smile=True, r_arm="point", talk=talk_v(t, True))
            char(cv, "susan_kare", 336, ground_y, t, scale=2, look=-1, smile=True)

        else:
            # c5_03: El equipo vecino roba la bandera y pide rescate -> asalto pirata para recuperarla
            draw_place_only(cv, "NOTA DE RESCATE Y OPERACIÓN DE RECUPERACIÓN", t, t_03, border=CORAL)
            window(cv, 94, 42, 292, 70, fill=(24, 16, 28), border=CORAL, alpha=0.95)
            draw_text(cv, "EL EQUIPO VECINO ROBÓ LA BANDERA", 240, 52, "press", 8, CORAL, align="center")
            draw_text(cv, "MANDARON UNA NOTA PIDIENDO RESCATE", 240, 70, "silk", 8, CREAM, align="center")
            draw_text(cv, "¡ASALTARON LA OFICINA Y LA RECUPERARON!", 240, 88, "silk", 8, GOLD, align="center")

            cx_p, cw_p, clook = pace(t, t_03, 118, 184, period=1.9, pause=0.2)
            char(cv, "mac_coder", cx_p, ground_y, t, scale=2, walk=cw_p, look=clook, r_arm="up", talk=talk_v(t, True))
            char(cv, "jobs_1977", 342, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")

    else:
        # c5_04: Enero de 1984 · La Macintosh sale de un bolso y habla sola en el escenario
        cv = bg("mac_stage_1984")
        grade(cv, tint=(0.94, 0.98, 1.08), dark=0.06)
        draw_place_only(cv, "ENERO DE 1984 · LA COMPUTADORA QUE HABLÓ SOLA", t, t_04, border=GOLD)
        floor_prop(cv, draw_mac_1984_podium_prop, 240, ground_y)

        window(cv, 94, 40, 292, 78, fill=(14, 20, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "«HOLA, SOY MACINTOSH»", 240, 50, "press", 8, GOLD, align="center")
        draw_text(cv, "«NUNCA CONFÍES EN UNA COMPUTADORA", 240, 68, "silk", 8, CYAN, align="center")
        draw_text(cv, "QUE NO PUEDAS LEVANTAR»", 240, 84, "silk", 8, CYAN, align="center")
        draw_text(cv, "EL TEATRO ENTERO APLAUDIÓ DE PIE", 240, 100, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1977", 142, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "susan_kare", 346, ground_y, t, scale=2, look=-1, smile=True)

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(5) - 0.15, card_ch5, None),
        (TL.start("c5_01"), scene_ch5_main, lambda t: cam_push(t, TL.start("c5_01"), chapter_end(5), 1.0, 1.03)),
    ]
