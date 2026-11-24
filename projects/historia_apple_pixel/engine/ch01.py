"""Apertura (El Empleado Número Cero, 1977) + Capítulo 1 (El Silbato y el Papa, 1971)."""
import math
from PIL import Image, ImageDraw

from core import *  # noqa
from common import *  # noqa
from timeline import TL


# ===========================================================================
# APERTURA: EL EMPLEADO NÚMERO CERO (s01..s06)
# ===========================================================================

def scene_opening(t):
    t_s01 = TL.start("s01")
    t_s02 = TL.start("s02")
    t_s03 = TL.start("s03")
    t_s04 = TL.start("s04")
    t_s05 = TL.start("s05")
    t_s06 = TL.start("s06")

    # Placa de título principal durante s06
    if t >= t_s06 - 0.1:
        cv = vgradient((8, 12, 24), (18, 30, 52), 12)
        STARS.draw(cv, t, alpha=0.85)
        d = ImageDraw.Draw(cv)
        # Suelo oscuro con trazas electrónicas verdes
        d.rectangle([0, 232, W, H], fill=(12, 22, 18, 255))
        for ry in range(236, H, 6):
            d.line([(0, ry), (W, ry)], fill=(54, 156, 94, 130))

        p_in = ease_out(prog(t, t_s06, t_s06 + 0.6))
        # Credencial #0 girando arriba del título
        flip = math.cos(t * 2.4)
        draw_employee_badge(cv, 240, 44, num_str="0", flip_p=flip, scale=1)

        window(cv, 34, 72, 412, 134, fill=(14, 18, 34), border=GOLD, alpha=0.96)
        draw_text(cv, "DOCUMENTAL PIXELOIDE · 1971 — 2026", 240, 84, "press", 8, CYAN, align="center")
        draw_text(cv, "EL EMPLEADO", 240, 104, "press", 24, align="center", gradient=GOLD_RAMP,
                  reveal=max(1, int((t - t_s06 + 0.2) * 24)))
        draw_text(cv, "NÚMERO CERO", 240, 134, "press", 24, align="center", gradient=CREAM_RAMP,
                  reveal=max(1, int((t - t_s06 - 0.1) * 24)))
        draw_text(cv, "APPLE Y STEVE JOBS EN SUS ANÉCDOTAS MÁS RARAS", 240, 174, "silk", 8, GOLD,
                  align="center", alpha=p_in)
        draw_text(cv, "POR PIXELOIDE STUDIOS", 240, 190, "silk", 8, GREY, align="center", alpha=p_in)
        return vignette(cv, 0.36)

    cv = bg("cupertino_office_1977")
    grade(cv, tint=(1.04, 0.98, 0.90), dark=0.06)
    draw_place_only(cv, "CUARTEL DE APPLE · CUPERTINO · 1977", t, t_s01, border=GOLD)

    ground_y = 224
    floor_prop(cv, draw_office_desk_1977, 240, ground_y)

    if t < t_s02:
        # s01: Mike Scott ordenando la empresa recién nacida con carpeta de credenciales
        window(cv, 94, 48, 292, 54, fill=(16, 20, 36), border=GOLD, alpha=0.94)
        draw_text(cv, "ORDENANDO LA EMPRESA RECIÉN NACIDA", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "CREDENCIALES NUMERADAS PARA EL EQUIPO", 240, 76, "silk", 8, CREAM, align="center")

        char(cv, "mike_scott", 136, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "wozniak_1977", 336, ground_y, t, scale=2, look=-1)
        char(cv, "jobs_1977", 396, ground_y, t, scale=2, look=-1)
        person_card(cv, "mike_scott", "MIKE SCOTT", "PRIMER PRESIDENTE DE APPLE · 1977",
                    t, t_s01 + 0.35, dur=3.2)

    elif t < t_s03:
        # s02: Número 1 para Wozniak, Número 2 para Jobs
        window(cv, 94, 44, 292, 82, fill=(16, 20, 36), border=CYAN, alpha=0.95)
        draw_employee_badge(cv, 152, 84, num_str="1", flip_p=1.0, scale=1)
        draw_text(cv, "Nº 1 · STEVE WOZNIAK", 262, 62, "press", 8, GOLD, align="center")
        draw_text(cv, "ARMÓ LOS CIRCUITOS CON SUS MANOS", 262, 76, "silk", 8, CREAM, align="center")
        draw_employee_badge(cv, 152, 108, num_str="2", flip_p=1.0, scale=1, bar_col=(214, 72, 64))
        draw_text(cv, "Nº 2 · STEVE JOBS", 262, 102, "press", 8, CORAL, align="center")

        char(cv, "mike_scott", 124, ground_y, t, scale=2, look=1)
        char(cv, "wozniak_1977", 316, ground_y, t, scale=2, look=-1, smile=True, l_arm="up")
        char(cv, "jobs_1977", 392, ground_y, t, scale=2, look=-1, frown=True, brows="angry")
        person_card(cv, "steve_wozniak", "STEVE WOZNIAK", "INGENIERO · EMPLEADO NÚMERO 1",
                    t, t_s02 + 0.3, dur=3.2)

    elif t < t_s04:
        # s03: Berrinche de Steve Jobs (22 años): "¡No puedo ser el dos!"
        window(cv, 94, 46, 292, 56, fill=(28, 16, 22), border=CORAL, alpha=0.95)
        draw_text(cv, "STEVE JOBS · 22 AÑOS", 240, 56, "press", 8, CORAL, align="center")
        draw_text(cv, "LLANTOS · GRITOS · GOLPES EN LA MESA", 240, 74, "silk", 8, CREAM, align="center")

        jx, jw, jlook = pace(t, t_s03, 310, 396, period=1.8, pause=0.18)
        char(cv, "mike_scott", 122, ground_y, t, scale=2, look=1, brows="sad")
        char(cv, "wozniak_1977", 184, ground_y, t, scale=2, look=1)
        char(cv, "jobs_1977", jx, ground_y, t, scale=2, walk=jw, look=jlook,
             brows="angry", frown=True, l_arm="up", r_arm="up", talk=talk_v(t, True))
        bubble(cv, "¡NO PUEDO SER EL DOS!", int(jx), ground_y - 104, align="center")
        person_card(cv, "steve_jobs_1977", "STEVE JOBS", "COFUNDADOR DE APPLE · 22 AÑOS",
                    t, t_s03 + 0.25, dur=3.2)

    elif t < t_s05:
        # s04: "¿El cero? ¡Entonces quiero ser el cero!" + Rechazo del sistema bancario
        dt = t - t_s04
        window(cv, 94, 42, 292, 82, fill=(16, 20, 36), border=GOLD, alpha=0.95)
        draw_employee_badge(cv, 138, 82, num_str="0", flip_p=1.0, scale=1)
        draw_text(cv, "CREDENCIAL Nº 0 · APROBADA", 268, 56, "press", 8, GOLD, align="center")
        draw_text(cv, "SISTEMA DE SUELDOS DEL BANCO:", 268, 74, "silk", 8, CREAM, align="center")
        if dt > 2.4:
            draw_text(cv, "RECHAZADO (EMPIEZA EN 1)", 268, 92, "press", 8, CORAL, align="center")
        else:
            draw_text(cv, "PROCESANDO FICHA #000...", 268, 92, "silk", 8, CYAN, align="center")

        char(cv, "mike_scott", 132, ground_y, t, scale=2, look=1, r_arm="point")
        char(cv, "jobs_1977", 356, ground_y, t, scale=2, look=-1, l_arm="up", talk=talk_v(t, dt < 2.4))
        if dt < 2.4:
            bubble(cv, "¡QUIERO SER EL CERO!", 356, ground_y - 104, align="center")

    else:
        # s05: Credencial #0 iluminada en el centro pero cobrando como #2
        cv = spotlight(cv, 240, 34, 224, 52, 160, color=(255, 220, 120), strength=0.28)
        window(cv, 94, 42, 292, 92, fill=(16, 20, 36), border=GOLD, alpha=0.96)
        draw_employee_badge(cv, 146, 88, num_str="0", name_str="JOBS", flip_p=math.cos(t * 2.0), scale=2)
        draw_text(cv, "CREDENCIAL EN EL PECHO: Nº 0", 282, 62, "press", 8, GOLD, align="center")
        draw_text(cv, "RECIBO DEL BANCO: EMPLEADO Nº 2", 282, 82, "silk", 8, CYAN, align="center")
        draw_text(cv, "ASÍ ERA APPLE DESDE EL PRIMER DÍA", 282, 102, "silk", 8, CREAM, align="center")

        char(cv, "mike_scott", 104, ground_y, t, scale=2, look=1)
        char(cv, "jobs_1977", 240, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "wozniak_1977", 376, ground_y, t, scale=2, look=-1, smile=True)

    return vignette(cv, 0.34)


# ===========================================================================
# CAPÍTULO 1: EL SILBATO Y EL PAPA (c1_00..c1_08)
# ===========================================================================

card_ch1 = make_card(1, ["EL SILBATO Y EL PAPA"], "CALIFORNIA Y ROMA · 1971")


def scene_pizarra_whistle(t):
    """La Pizarra 1: El silbato mágico de 2600 Hz y la caja azul (c1_02..c1_05)."""
    t0 = TL.start("c1_02")
    t_03 = TL.start("c1_03")
    t_04 = TL.start("c1_04")
    t_05 = TL.start("c1_05")

    cv = draw_pizarra_frame(t, t0, "EL SILBATO MÁGICO (2600 Hz)",
                            summary_es="EL TELÉFONO OBEDECÍA SONIDOS", t_summary=t_05 + 2.2)
    d = ImageDraw.Draw(cv)

    # Panel central de esquema en tiza
    window(cv, 94, 42, 292, 154, fill=(14, 38, 26), border=CHALK_WHITE, alpha=0.94)

    if t < t_03:
        # c1_02: Teléfono a la izquierda, línea larga y central con operadora dormida a la derecha
        draw_text(cv, "CÓMO FUNCIONABA LA RED EN 1971", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        # Tubo de teléfono a la izquierda
        d.rectangle([118, 92, 148, 134], outline=(*CHALK_WHITE, 255), width=2)
        draw_text(cv, "TU CASA", 133, 142, "silk", 8, CHALK_CYAN, align="center")
        # Línea telefónica
        d.line([(148, 112), (296, 112)], fill=(*CHALK_WHITE, 255), width=2)
        # Central telefónica a la derecha
        d.rectangle([296, 84, 366, 142], outline=(*CHALK_YELLOW, 255), width=2)
        draw_text(cv, "CENTRAL", 331, 96, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "SONIDOS = ÓRDENES", 331, 116, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "LOS SONIDOS VIAJABAN POR EL MISMO CABLE", 240, 172, "silk", 8, CHALK_GREEN, align="center")
        draw_chalk_hand(cv, 260, 112, t)

    elif t < t_04:
        # c1_03: Onda amarilla de 2600 Hz que abre la compuerta de la central
        draw_text(cv, "EL TONO SECRETO: 2600 Hz", 240, 52, "press", 8, CHALK_YELLOW, align="center")
        d.rectangle([114, 92, 144, 132], outline=(*CHALK_WHITE, 255), width=2)
        # Onda sinusoidal amarilla viajando hacia la central
        pts = []
        for x in range(148, 282, 3):
            yy = 112 + int(round(math.sin((x - t * 90) * 0.22) * 12))
            pts.append((x, yy))
        if len(pts) >= 2:
            d.line(pts, fill=(*CHALK_YELLOW, 255), width=2)
        draw_text(cv, "2600 CICLOS/SEG", 214, 78, "press", 8, CHALK_YELLOW, align="center")
        # Compuerta abierta en verde (100px de ancho)
        d.rectangle([284, 82, 384, 142], outline=(*CHALK_GREEN, 255), width=2)
        draw_text(cv, "¡COLGÓ!", 334, 94, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "LÍNEA ABIERTA", 334, 116, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "LA MÁQUINA CREÍA QUE HABÍAS CORTADO", 240, 172, "silk", 8, CHALK_CYAN, align="center")

    elif t < t_05:
        # c1_04: Silbato de plástico de caja de cereales soplando 2600 Hz gratis
        draw_text(cv, "EL REGALO EN LA CAJA DE CEREALES", 240, 52, "press", 8, CHALK_CYAN, align="center")
        # Dibujo del silbato celeste en tiza
        d.rectangle([120, 102, 152, 118], fill=(38, 118, 142, 255), outline=(*CHALK_CYAN, 255))
        d.ellipse([146, 96, 174, 124], fill=(38, 118, 142, 255), outline=(*CHALK_CYAN, 255))
        draw_text(cv, "SILBATO GRATIS", 150, 134, "silk", 8, CHALK_CYAN, align="center")
        # Ondas iguales de 2600 Hz
        for r_w in (12, 22, 32):
            d.arc([172, 110 - r_w, 172 + r_w * 2, 110 + r_w], -45, 45, fill=(*CHALK_YELLOW, 255), width=2)
        draw_text(cv, "= 2600 Hz EXACTOS", 296, 98, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "LLAMADAS GRATIS AL MUNDO", 296, 118, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "SOPLABAS EN EL TUBO Y MARCABAS CUALQUIER PAÍS", 240, 172, "silk", 8, CHALK_WHITE, align="center")

    else:
        # c1_05: La Caja Azul electrónica construida por Wozniak y Jobs
        draw_text(cv, "LA CAJA AZUL DE WOZNIAK Y JOBS", 240, 52, "press", 8, CHALK_CYAN, align="center")
        # Caja azul con teclado de 12 botones
        bx, by = 188, 72
        d.rectangle([bx, by, bx + 104, by + 76], fill=(28, 78, 148, 255), outline=(*CHALK_CYAN, 255), width=2)
        for r in range(3):
            for c in range(4):
                kx = bx + 14 + c * 22
                ky = by + 14 + r * 18
                d.rectangle([kx, ky, kx + 14, ky + 12], fill=(224, 232, 248, 255), outline=(*INK, 255))
        draw_text(cv, "IMITABA TODOS LOS TONOS DE LA RED", 240, 162, "silk", 8, CHALK_WHITE, align="center")

    return vignette(cv, 0.28)


def scene_ch1_main(t):
    """Escenas narrativas del Capítulo 1: garaje 1971, cabina nocturna, broma al Vaticano y venta (c1_01, c1_06..c1_08)."""
    t_01 = TL.start("c1_01")
    t_02 = TL.start("c1_02")
    t_06 = TL.start("c1_06")
    t_07 = TL.start("c1_07")
    t_08 = TL.start("c1_08")

    if t_02 <= t < t_06:
        return scene_pizarra_whistle(t)

    ground_y = 224

    if t < t_02:
        # c1_01: Garaje 1971, Wozniak (21) y Jobs (16) leyendo la revista del hombre ciego
        cv = bg("los_altos_garage_1976")
        grade(cv, tint=(1.04, 0.98, 0.88), dark=0.06)
        draw_chapter_header(cv, t, t_01, "CAP. 1", "EL SILBATO Y EL PAPA", "CALIFORNIA · 1971 · CINCO AÑOS ANTES DE APPLE")
        floor_prop(cv, draw_garage_bench_1976, 240, ground_y)

        window(cv, 94, 48, 292, 54, fill=(16, 20, 36), border=GOLD, alpha=0.94)
        draw_text(cv, "WOZNIAK (21 AÑOS) · JOBS (16 AÑOS)", 240, 58, "press", 8, GOLD, align="center")
        draw_text(cv, "REVISTA: EL HACKER CIEGO DEL OÍDO PERFECTO", 240, 76, "silk", 8, CREAM, align="center")

        char(cv, "wozniak_teen", 156, ground_y, t, scale=2, look=1, r_arm="point", talk=talk_v(t, True))
        char(cv, "jobs_teen", 324, ground_y, t, scale=2, look=-1, smile=True)

    elif t < t_07:
        # c1_06: Cabina telefónica de noche · llamando al Vaticano fingiendo ser Henry Kissinger
        cv = bg("night_payphone_1971")
        grade(cv, tint=(0.90, 0.96, 1.08), dark=0.10)
        draw_place_only(cv, "TELÉFONO PÚBLICO · NOCHE DE 1971 · LLAMANDO A ROMA", t, t_06, border=CYAN)
        floor_prop(cv, draw_payphone_booth_prop, 240, ground_y)

        window(cv, 94, 42, 292, 62, fill=(14, 20, 38), border=CYAN, alpha=0.94)
        draw_text(cv, "DESTINO: EL VATICANO · ROMA", 240, 52, "press", 8, CYAN, align="center")
        draw_text(cv, "WOZNIAK IMITA A HENRY KISSINGER", 240, 70, "silk", 8, GOLD, align="center")
        draw_text(cv, "«NECESITO HABLAR CON EL PAPA PABLO VI»", 240, 86, "silk", 8, CREAM, align="center")

        char(cv, "wozniak_teen", 178, ground_y, t, scale=2, look=1, r_arm="up", talk=talk_v(t, True))
        char(cv, "jobs_teen", 312, ground_y, t, scale=2, look=-1, smile=True)
        person_card(cv, "henry_kissinger", "HENRY KISSINGER", "FUNCIONARIO DE EE.UU. IMITADO POR WOZNIAK",
                    t, t_06 + 1.8, dur=3.4)

    elif t < t_08:
        # c1_07: Pasillo del Vaticano a las 5:30 AM, guardia corriendo con vela en candelabro sobre mesa
        cv = bg("vatican_corridor_night")
        grade(cv, tint=(1.02, 0.96, 0.90), dark=0.08)
        draw_place_only(cv, "CIUDAD DEL VATICANO · 5:30 DE LA MAÑANA", t, t_07, border=GOLD)
        floor_prop(cv, draw_vatican_table_prop, 148, ground_y)

        window(cv, 94, 42, 292, 60, fill=(24, 18, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "5:30 AM EN ROMA · ¡SE LO CREYERON!", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "FUERON A DESPERTAR AL PAPA DE LA CAMA", 240, 70, "silk", 8, CREAM, align="center")
        draw_text(cv, "SE TENTARON DE RISA Y CORTARON ANTES", 240, 86, "silk", 8, CYAN, align="center")

        gx, gw, glook = pace(t, t_07, 290, 396, period=2.0, pause=0.15)
        char(cv, "vatican_guard", gx, ground_y, t, scale=2, walk=gw, look=glook, r_arm="up", talk=talk_v(t, True))
        bubble(cv, "¡DESPIERTEN AL PAPA!", int(gx), ground_y - 104, align="center")

    else:
        # c1_08: Venta de 200 cajas azules a 150 dólares en residencias estudiantiles
        cv = bg("night_payphone_1971")
        grade(cv, tint=(0.95, 1.0, 1.05), dark=0.08)
        draw_place_only(cv, "RESIDENCIAS UNIVERSITARIAS · EL PRIMER NEGOCIO", t, t_08, border=GOLD)
        floor_prop(cv, draw_payphone_booth_prop, 240, ground_y)

        window(cv, 94, 42, 292, 74, fill=(14, 22, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "200 CAJAS AZULES VENDIDAS", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "PRECIO: 150 DÓLARES CADA UNA", 240, 70, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "WOZ PONÍA EL INGENIO · JOBS LO VENDÍA", 240, 90, "silk", 8, CREAM, align="center")

        char(cv, "wozniak_teen", 154, ground_y, t, scale=2, look=1, smile=True)
        char(cv, "jobs_teen", 326, ground_y, t, scale=2, look=-1, smile=True, l_arm="up", talk=talk_v(t, True))

    return vignette(cv, 0.34)


def scenes():
    return [
        (0.0, scene_opening, lambda t: cam_push(t, 0.0, TL.chapter_start(1), 1.0, 1.03)),
        (TL.chapter_start(1) - 0.15, card_ch1, None),
        (TL.start("c1_01"), scene_ch1_main, lambda t: cam_push(t, TL.start("c1_01"), chapter_end(1), 1.0, 1.03)),
    ]
