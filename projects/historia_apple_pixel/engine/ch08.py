"""Capítulo 8: El Teléfono Roto, la Petaca de Whisky y los Cuatro Mil Cafés (2007)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL

card_ch8 = make_card(8, ["EL TELÉFONO ROTO Y 4.000 CAFÉS"], "SAN FRANCISCO · 9 DE ENERO DE 2007")


def scene_pizarra_golden_path(t):
    """La Pizarra 3: El Camino Dorado y el vaso de memoria del primer iPhone (c8_03..c8_06)."""
    t0 = TL.start("c8_03")
    t_04 = TL.start("c8_04")
    t_05 = TL.start("c8_05")
    t_06 = TL.start("c8_06")

    cv = draw_pizarra_frame(t, t0, "EL CAMINO DORADO (ENERO 2007)",
                            summary_es="EL ORDEN IMPORTABA", t_summary=t_06 + 2.2)
    d = ImageDraw.Draw(cv)

    window(cv, 94, 42, 292, 154, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.94)

    if t < t_04:
        # c8_03: La memoria del teléfono explicada como un vaso de agua pequeño
        draw_text(cv, "LA MEMORIA = UN VASO DE AGUA PEQUEÑO", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        # Vaso en el centro
        vx0, vy0, vx1, vy1 = 212, 76, 268, 146
        fill_h = max(4, int(38 * clamp01((t - t0) / 3.0)))
        d.rectangle([vx0 + 2, vy1 - fill_h, vx1 - 2, vy1 - 2], fill=(64, 178, 224, 210))
        d.line([(vx0, vy0), (vx0, vy1), (vx1, vy1), (vx1, vy0)], fill=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "CADA PROGRAMA ECHABA AGUA AL VASO", 240, 156, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "AL CERRARLO, EL VASO DEBÍA VACIARSE", 240, 172, "silk", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, 268, 110, t)

    elif t < t_05:
        # c8_04: Los programas perdían memoria, el vaso no se vaciaba y rebalsaba -> pantalla negra
        draw_text(cv, "EL PROBLEMA: EL VASO NO SE VACIABA", 240, 52, "press", 8, CORAL, align="center")
        vx0, vy0, vx1, vy1 = 212, 78, 268, 144
        d.rectangle([vx0 + 2, vy0 + 2, vx1 - 2, vy1 - 2], fill=(224, 88, 78, 220))
        d.line([(vx0, vy0), (vx0, vy1), (vx1, vy1), (vx1, vy0)], fill=(*CHALK_WHITE, 255), width=2)
        # Gotas rebalsando a los costados
        d.rectangle([vx0 - 10, vy1 - 6, vx0 - 2, vy1], fill=(64, 178, 224, 255))
        d.rectangle([vx1 + 2, vy1 - 6, vx1 + 10, vy1], fill=(64, 178, 224, 255))
        draw_text(cv, "¡REBALSÓ!", 240, 98, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "SI ABRÍAS 3 COSAS: PANTALLA NEGRA", 240, 156, "press", 8, CORAL, align="center")
        draw_text(cv, "EL TELÉFONO SE APAGABA EN VIVO", 240, 172, "silk", 8, CHALK_WHITE, align="center")

    elif t < t_06:
        # c8_05: El Camino Dorado (Correo -> Internet = OK | Internet -> Correo = CRASH)
        draw_text(cv, "LA RUTA ÚNICA: «EL CAMINO DORADO»", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        # Ruta 1: Correo -> Internet (Verde OK)
        d.rectangle([112, 74, 368, 110], fill=(18, 52, 34, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "1. CORREO -> 2. INTERNET = ¡AGUANTA!", 240, 88, "press", 8, CHALK_GREEN, align="center")
        # Ruta 2: Internet -> Correo (Rojo CRASH)
        d.rectangle([112, 120, 368, 156], fill=(48, 22, 26, 255), outline=(*CORAL, 255))
        draw_text(cv, "1. INTERNET -> 2. CORREO = ¡SE CUELGA!", 240, 134, "press", 8, CORAL, align="center")
        draw_text(cv, "SI JOBS CAMBIABA EL ORDEN, FALLABA TODO", 240, 170, "silk", 8, CHALK_WHITE, align="center")

    else:
        # c8_06: Tres teléfonos idénticos en la mesa para ir cambiándolos sin que nadie lo note
        draw_text(cv, "EL TRUCO EN LA MESA: 3 TELÉFONOS IGUALES", 240, 52, "press", 8, CHALK_CYAN, align="center")
        for idx_p, (px, lbl) in enumerate(((148, "TEL. 1"), (240, "TEL. 2"), (332, "TEL. 3"))):
            d.rectangle([px - 24, 74, px + 24, 132], fill=(20, 32, 44, 255), outline=(*CHALK_YELLOW, 255))
            draw_text(cv, lbl, px, 96, "press", 8, CHALK_WHITE, align="center")
            draw_text(cv, "LISTO", px, 114, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "CUANDO UNO SE LLENABA, AGARRABA EL OTRO", 240, 152, "silk", 8, CHALK_WHITE, align="center")

    return vignette(cv, 0.28)


def scene_ch8_main(t):
    t_01 = TL.start("c8_01")
    t_02 = TL.start("c8_02")
    t_03 = TL.start("c8_03")
    t_07 = TL.start("c8_07")
    t_08 = TL.start("c8_08")

    if t_03 <= t < t_07:
        return scene_pizarra_golden_path(t)

    cv = bg("iphone_stage_backstage_2007")
    grade(cv, tint=(0.94, 0.98, 1.08), dark=0.06)
    ground_y = 224
    floor_prop(cv, draw_iphone_podium_prop, 240, ground_y)

    if t < t_02:
        # c8_01: 9 de enero de 2007 · San Francisco · Presentación del primer iPhone
        draw_chapter_header(cv, t, t_01, "CAP. 8", "EL TELÉFONO ROTO Y 4.000 CAFÉS",
                            "SAN FRANCISCO · 9 DE ENERO DE 2007")
        window(cv, 94, 48, 292, 62, fill=(14, 20, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "9 DE ENERO DE 2007 · EL PRIMER iPHONE", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "EN EL ESCENARIO PARECÍA TERMINADO", 240, 76, "silk", 8, CYAN, align="center")
        draw_text(cv, "DETRÁS DEL TELÓN: PÁNICO TOTAL", 240, 92, "silk", 8, CORAL, align="center")

        char(cv, "jobs_1997", 142, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "iphone_eng", 346, ground_y, t, scale=2, look=-1, brows="sad", frown=True)

    elif t < t_03:
        # c8_02: Cinco barras de señal trucadas y la petaca de whisky en la quinta fila
        draw_place_only(cv, "5 BARRAS DE SEÑAL TRUCADAS Y UNA PETACA DE WHISKY", t, t_02, border=CORAL)
        d = ImageDraw.Draw(cv)
        window(cv, 94, 40, 292, 82, fill=(24, 16, 28), border=CORAL, alpha=0.95)
        # 5 barras de señal dibujadas fijas
        for b_i in range(5):
            bh = 4 + b_i * 3
            bx = 122 + b_i * 6
            d.rectangle([bx, 68 - bh, bx + 4, 68], fill=(*CHALK_GREEN, 255))
        draw_text(cv, "SEÑAL TRUCADA: SIEMPRE 5 BARRAS", 254, 54, "press", 8, GOLD, align="center")
        draw_text(cv, "EN LA FILA 5: INGENIEROS CON WHISKY", 240, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "UN TRAGO POR CADA PRUEBA QUE NO FALLABA", 240, 96, "silk", 8, CYAN, align="center")

        char(cv, "jobs_1997", 136, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "iphone_eng", 344, ground_y, t, scale=2, look=-1, l_arm="up")

    elif t < t_08:
        # c8_07: La llamada en vivo desde el mapa: "¡Quería pedir 4.000 cafés con leche para llevar!"
        draw_place_only(cv, "LLAMADA EN VIVO · «4.000 CAFÉS CON LECHE PARA LLEVAR»", t, t_07, border=GOLD)
        window(cv, 94, 40, 292, 82, fill=(16, 22, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "LLAMADA EN VIVO A UNA CAFETERÍA REAL:", 240, 50, "silk", 8, CYAN, align="center")
        draw_text(cv, "«¡BUENOS DÍAS! ¿EN QUÉ PUEDO AYUDARLO?»", 240, 68, "silk", 8, CREAM, align="center")
        draw_text(cv, "«QUERÍA 4.000 CAFÉS CON LECHE", 240, 86, "press", 8, GOLD, align="center")
        draw_text(cv, "PARA LLEVAR, POR FAVOR»", 240, 102, "press", 8, GOLD, align="center")

        char(cv, "jobs_1997", 148, ground_y, t, scale=2, look=1, smile=True, r_arm="up", talk=talk_v(t, True))
        char(cv, "iphone_eng", 342, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")
        bubble(cv, "¡4.000 CAFÉS!", 148, ground_y - 104, align="center")

    else:
        # c8_08: "¡No, es una broma! Número equivocado" -> eco de la broma al Papa en 1971
        draw_place_only(cv, "1971 — 2007 · LA PRIMERA BROMA EN UN TELÉFONO MODERNO", t, t_08, border=CYAN)
        window(cv, 94, 40, 292, 84, fill=(14, 22, 38), border=CYAN, alpha=0.96)
        draw_text(cv, "«¡NO, ES UNA BROMA! ¡ADIÓS!»", 240, 50, "press", 8, GOLD, align="center")
        draw_text(cv, "1971: BROMA AL PAPA DESDE UNA CABINA", 240, 72, "silk", 8, CYAN, align="center")
        draw_text(cv, "2007: BROMA EN VIVO FRENTE AL MUNDO", 240, 90, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "EL MISMO ESPÍRITU TRES DÉCADAS DESPUÉS", 240, 106, "silk", 8, CREAM, align="center")

        char(cv, "jobs_1997", 152, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "iphone_eng", 338, ground_y, t, scale=2, look=-1, smile=True)

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.chapter_start(8) - 0.15, card_ch8, None),
        (TL.start("c8_01"), scene_ch8_main, lambda t: cam_push(t, TL.start("c8_01"), chapter_end(8), 1.0, 1.03)),
    ]
