"""Capítulo 5: Una pantalla que siente (San Francisco 9 de enero de 2007, 3 aparatos en 1, pellizco multi-touch y La Pizarra 2: Pantalla Capacitiva)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c5_s01_keynote_2007(t):
    """c5_01..c5_04: Teléfonos de oficina con teclado -> 9 de enero de 2007 en San Francisco: todo pantalla, 3 en 1 y pellizco con dos dedos."""
    t0 = TL.s("c5_01")
    t_c5_02 = TL.s("c5_02")
    t_c5_03 = TL.s("c5_03")
    t_c5_04 = TL.s("c5_04")

    cv = bg("sf_keynote_stage_2007").copy()
    draw_place_only(cv, "SAN FRANCISCO · 9 DE ENERO DE 2007", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    # Atril de demostración apoyado sobre el escenario
    def _draw_keynote_table(canvas, cx, fy):
        d_t = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 30, 4, 90)
        d_t.rectangle([cx - 14, top_y + 5, cx + 14, fy], fill=(32, 38, 56, 255), outline=(*INK, 255))
        d_t.rectangle([cx - 24, fy - 5, cx + 24, fy], fill=(48, 56, 78, 255), outline=(*INK, 255))
        d_t.rectangle([cx - 24, top_y, cx + 24, top_y + 5], fill=(72, 148, 224, 255), outline=(*INK, 255))
        # Smartphone todo pantalla brillante sobre el pedestal
        if t >= t_c5_02 - 0.2:
            glow(canvas, cx, top_y - 14, 18, TESLA_CYAN, 0.5)
            d_t.rectangle([cx - 7, top_y - 24, cx + 7, top_y], fill=(22, 26, 36, 255), outline=(*INK, 255))
            d_t.rectangle([cx - 5, top_y - 21, cx + 5, top_y - 3], fill=(96, 214, 255, 255))
    floor_prop(cv, _draw_keynote_table, 272, 248)

    char(cv, "keynote_speaker", 178, 248, t, scale=2,
         arms="point" if t >= t_c5_02 else "hold", look=1, mood="happy",
         talk=talk_v(t, True))

    window(cv, 118, 40, 244, 108, fill=(12, 20, 40), border=GOLD if t >= t_c5_02 else SOFT_GRAY)
    if t < t_c5_02:
        draw_text(cv, "ANTES DE 2007 · OFICINA:", 240, 48, "silk", 8, SOFT_GRAY, align="center")
        # Teléfono con pantallita arriba y muchos botones abajo
        d.rectangle([222, 64, 258, 120], fill=(54, 60, 74, 255), outline=(*INK, 255))
        d.rectangle([226, 68, 254, 86], fill=(138, 178, 142, 255))
        for ky in range(90, 116, 5):
            for kx in range(226, 254, 5):
                d.rectangle([kx, ky, kx + 3, ky + 3], fill=(196, 202, 214, 255))
        draw_text(cv, "PANTALLITA + TECLADO DE BOTONES", 240, 128, "silk", 8, CREAM, align="center")
    elif t < t_c5_03:
        draw_text(cv, "9 DE ENERO DE 2007 · APPLE:", 240, 48, "silk", 8, TESLA_CYAN, align="center")
        d.rectangle([220, 64, 260, 122], fill=(28, 32, 44, 255), outline=(*TESLA_CYAN, 255))
        d.rectangle([223, 68, 257, 116], fill=(64, 168, 238, 255))
        d.ellipse([238, 117, 242, 121], outline=(188, 196, 212, 255))
        draw_text(cv, "SIN TECLADO · TODO PANTALLA", 240, 128, "press", 8, GOLD, align="center")
    elif t < t_c5_04:
        draw_text(cv, "TRES APARATOS EN UNO:", 240, 48, "silk", 8, GOLD, align="center")
        items = [("MÚSICA", 156, CHALK_GREEN), ("TELÉFONO", 240, TESLA_CYAN), ("INTERNET", 324, GOLD)]
        for lbl, ix, col in items:
            d.rectangle([ix - 32, 68, ix + 32, 108], fill=(22, 34, 58, 255), outline=(*col, 255))
            draw_text(cv, lbl, ix, 84, "silk", 8, col, align="center")
        draw_text(cv, "JUNIO 2007: FILAS EN LAS TIENDAS", 240, 122, "silk", 8, CREAM, align="center")
    else:
        draw_text(cv, "DOS DEDOS -> AGRANDAR FOTO", 240, 48, "silk", 8, TESLA_CYAN, align="center")
        z_p = 0.5 + 0.5 * math.sin(t * 3.5)
        rw = int(22 + 24 * z_p)
        rh = int(14 + 14 * z_p)
        d.rectangle([240 - rw, 90 - rh, 240 + rw, 90 + rh], fill=(42, 118, 186, 255), outline=(*GOLD, 255), width=2)
        draw_text(cv, "NO SENTÍA PRESIÓN · SENTÍA OTRA COSA", 240, 126, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.32)


def c5_s02_pizarra_capacitive(t):
    """c5_05..c5_09: LA PIZARRA 2 — Pantalla Capacitiva (electricidad del cuerpo, cuadrícula de carga, guantes y remate)."""
    t0 = TL.s("c5_05")
    t_c5_06 = TL.s("c5_06")
    t_c5_07 = TL.s("c5_07")
    t_c5_08 = TL.s("c5_08")
    t_c5_09 = TL.s("c5_09")

    cv = draw_pizarra_frame(
        t, t0, "PANTALLA QUE SIENTE",
        summary_es="NO SIENTE TU DEDO: SIENTE TU ELECTRICIDAD",
        t_summary=t_c5_08 + 0.3,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c5_06:
        # Paso 1: Tu cuerpo conduce la electricidad
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_YELLOW, alpha=0.92)
        draw_text(cv, "TU CUERPO CONDUCE ELECTRICIDAD", 240, 56, "silk", 8, CHALK_YELLOW, align="center")
        # Mano con pequeños destellos cian en la yema del dedo
        d.rectangle([222, 92, 258, 134], fill=(234, 184, 142, 255), outline=(*INK, 255))
        d.rectangle([234, 74, 246, 94], fill=(234, 184, 142, 255), outline=(*INK, 255))
        draw_phosphor_dot(cv, 240, 74, r=3, color=CHALK_CYAN)
        draw_text(cv, "MUY POQUITO, PERO CONDUCE", 240, 156, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, 286, 128, t)
    elif t < t_c5_07:
        # Paso 2: Cuadrícula transparente con pequeña carga eléctrica debajo del vidrio
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_CYAN, alpha=0.92)
        draw_text(cv, "CUADRÍCULA DE LÍNEAS TRANSPARENTES", 240, 54, "silk", 8, CHALK_CYAN, align="center")
        for gx in range(168, 316, 24):
            d.line([(gx, 74), (gx, 154)], fill=(*CHALK_CYAN, 190), width=1)
        for gy in range(78, 158, 22):
            d.line([(160, gy), (320, gy)], fill=(*CHALK_CYAN, 190), width=1)
        for gx in range(168, 316, 24):
            for gy in range(78, 158, 22):
                d.rectangle([gx - 2, gy - 2, gx + 2, gy + 2], fill=(*CHALK_YELLOW, 255))
        draw_text(cv, "CADA CRUCE ES UN SENSOR CON CARGA", 240, 166, "silk", 8, CHALK_WHITE, align="center")
    elif t < t_c5_08:
        # Paso 3: Al apoyar varios dedos cambias la carga de esos cruces
        window(cv, 118, 46, 244, 142, fill=BOARD_DARK, border=CHALK_GREEN, alpha=0.92)
        draw_text(cv, "EL TELÉFONO MIDE DÓNDE CAMBIÓ", 240, 54, "silk", 8, CHALK_GREEN, align="center")
        for gx in range(168, 316, 24):
            d.line([(gx, 74), (gx, 154)], fill=(*CHALK_CYAN, 170), width=1)
        for gy in range(78, 158, 22):
            d.line([(160, gy), (320, gy)], fill=(*CHALK_CYAN, 170), width=1)
        # Dos puntos de contacto (multi-touch) iluminados
        for tx_p, ty_p in ((216, 100), (264, 122)):
            glow(cv, tx_p, ty_p, 16, CHALK_YELLOW, 0.65)
            d.ellipse([tx_p - 6, ty_p - 6, tx_p + 6, ty_p + 6], fill=(*CHALK_YELLOW, 255), outline=(*INK, 255))
        draw_text(cv, "PUEDE SEGUIR VARIOS DEDOS A LA VEZ", 240, 166, "silk", 8, CHALK_YELLOW, align="center")
    else:
        # Paso 4 (c5_08..c5_09): Con guantes gruesos no funciona -> Siente tu electricidad
        window(cv, 118, 42, 244, 152, fill=BOARD_DARK, border=CHALK_WHITE, alpha=0.92)
        if t < t_c5_09 - 0.1:
            draw_text(cv, "GUANTE GRUESO: LA TELA NO CONDUCE", 240, 52, "silk", 8, CHALK_RED, align="center")
            d.rectangle([216, 78, 264, 126], fill=(148, 72, 64, 255), outline=(*CHALK_RED, 255), width=2)
            draw_text(cv, "SIN CAMBIO DE CARGA = NO RESPONDE", 240, 142, "silk", 8, CHALK_WHITE, align="center")
        else:
            draw_text(cv, "EL SECRETO DEL TOUCH:", 240, 54, "silk", 8, CHALK_CYAN, align="center")
            draw_text(cv, "LA PANTALLA NO SIENTE TU DEDO.", 240, 82, "press", 8, CHALK_WHITE, align="center")
            draw_text(cv, "SIENTE TU ELECTRICIDAD.", 240, 110, "press", 8, CHALK_YELLOW, align="center")

    return cv


def scenes():
    return [
        (TL.s("c5_00") - 0.15, make_card(5, ["UNA PANTALLA", "QUE SIENTE"], "2007 · SAN FRANCISCO"),
         None, "ch05"),
        (TL.s("c5_01") - 0.15, c5_s01_keynote_2007,
         lambda t: cam_push(t, TL.s("c5_01"), TL.s("c5_05"), 1.0, 1.03, (240, 135)), "ch05"),
        (TL.s("c5_05") - 0.15, c5_s02_pizarra_capacitive,
         None, "ch05"),
    ]


def music(A):
    t0 = TL.s("c5_00")
    t_end = TL.s("c6_00")
    A.add_pad(t0, t_end - t0, [130.81, 196.0, 261.63, 329.63], amp=0.038)


def sfx(A):
    A.fx_chime(TL.s("c5_02"), 0.10)
    A.fx_sweep(TL.s("c5_05"), 0.4, 220, 440, 0.06)
    A.fx_sparkle(TL.s("c5_09"), 0.10)
