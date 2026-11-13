"""Capítulo 3: Escribir y mirar (Redes digitales 2G, primer SMS en Inglaterra 1992 y primera foto en California 1997)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c3_s01_digital_and_first_sms(t):
    """c3_01..c3_05: El teléfono entra en el bolsillo, voz en 0 y 1, primer SMS 'MERRY CHRISTMAS' (1992) y límite de 160 caracteres."""
    t0 = TL.s("c3_01")
    t_c3_02 = TL.s("c3_02")
    t_c3_03 = TL.s("c3_03")
    t_c3_04 = TL.s("c3_04")
    t_c3_05 = TL.s("c3_05")

    cv = bg("uk_sms_office_1992").copy()
    draw_place_only(cv, "INGLATERRA · DICIEMBRE DE 1992", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    # Escritorio con computadora desde donde el ingeniero de 22 años envía el primer SMS
    def _draw_sms_desk(canvas, cx, fy):
        d_k = ImageDraw.Draw(canvas)
        top_y = fy - 40
        shadow_ellipse(canvas, cx, fy, 36, 4, 85)
        d_k.rectangle([cx - 30, top_y + 5, cx - 24, fy], fill=(74, 82, 98, 255), outline=(*INK, 255))
        d_k.rectangle([cx + 24, top_y + 5, cx + 30, fy], fill=(74, 82, 98, 255), outline=(*INK, 255))
        d_k.rectangle([cx - 34, top_y, cx + 34, top_y + 5], fill=(138, 102, 68, 255), outline=(*INK, 255))
        terminal(canvas, cx - 15, top_y - 26, t, on=True)
    floor_prop(cv, _draw_sms_desk, 178, 248)

    char(cv, "sms_engineer", 142, 248, t, scale=2,
         arms="type" if t >= t_c3_03 else "point", look=1, mood="happy")
    char(cv, "director_92", 336, 248, t, scale=2,
         arms="hold" if t >= t_c3_04 else "down", facing=-1, look=-1,
         mood="surprised" if t >= t_c3_04 else "neutral")

    if t < t_c3_03:
        window(cv, 118, 44, 244, 92, fill=(16, 26, 44), border=TESLA_CYAN)
        draw_text(cv, "AÑOS 90 · REDES DIGITALES (2G)", 240, 52, "silk", 8, TESLA_CYAN, align="center")
        bits = "01001101 01010011" if int(t * 4) % 2 == 0 else "10110010 01000001"
        draw_text(cv, bits, 240, 74, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "SI VIAJAN NÚMEROS -> VIAJAN LETRAS" if t >= t_c3_02 else "LA VOZ CONVERTIDA EN CEROS Y UNOS",
                  240, 104, "silk", 8, GOLD, align="center")
    elif t < t_c3_05:
        window(cv, 118, 44, 244, 96, fill=(18, 28, 48), border=GOLD)
        draw_text(cv, "PRIMER SMS DE LA HISTORIA (1992)", 240, 52, "silk", 8, GOLD, align="center")
        d.rectangle([136, 68, 344, 98], fill=(32, 64, 44, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "MERRY CHRISTMAS", 240, 79, "press", 8, CHALK_GREEN, align="center",
                  reveal=max(1, int((t - t_c3_03) * 14)))
        draw_text(cv, "DESDE UNA PC · SIN PODER CONTESTAR" if t >= t_c3_04 else "ESCRITO EN UNA COMPUTADORA",
                  240, 114, "silk", 8, CREAM, align="center")
    else:
        window(cv, 118, 44, 244, 96, fill=(18, 24, 42), border=TESLA_CYAN)
        draw_text(cv, "LÍMITE: 160 CARACTERES", 240, 54, "press", 8, TESLA_CYAN, align="center")
        d.rectangle([142, 74, 338, 102], fill=(124, 178, 118, 255), outline=(*INK, 255))
        draw_text(cv, "TKM · XQ · MSJ · SALU2", 240, 84, "press", 8, INK, align="center", outline=None, shadow=False)
        draw_text(cv, "NACIÓ LA COSTUMBRE DE ABREVIAR", 240, 114, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.35)


def c3_s02_first_camera_phone_1997(t):
    """c3_06..c3_08: Philippe Kahn en una maternidad de California (1997) une cámara + teléfono + laptop y comparte la primera foto."""
    t0 = TL.s("c3_06")
    t_cables = TL.word("c3_06", "cables")
    t_c3_07 = TL.s("c3_07")
    t_c3_08 = TL.s("c3_08")

    cv = bg("maternity_ward_1997").copy()
    draw_place_only(cv, "CALIFORNIA · 11 DE JUNIO DE 1997", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    # Mesa en la sala de espera con la cámara digital, el teléfono plegable y la laptop unidos con cables
    def _draw_kahn_rig(canvas, cx, fy):
        d_r = ImageDraw.Draw(canvas)
        top_y = fy - 40
        shadow_ellipse(canvas, cx, fy, 44, 4, 85)
        d_r.rectangle([cx - 38, top_y + 5, cx - 32, fy], fill=(82, 92, 108, 255), outline=(*INK, 255))
        d_r.rectangle([cx + 32, top_y + 5, cx + 38, fy], fill=(82, 92, 108, 255), outline=(*INK, 255))
        d_r.rectangle([cx - 42, top_y, cx + 42, top_y + 5], fill=(148, 112, 74, 255), outline=(*INK, 255))
        # 1. Cámara digital a la izquierda
        d_r.rectangle([cx - 34, top_y - 14, cx - 18, top_y], fill=(64, 68, 78, 255), outline=(*INK, 255))
        d_r.ellipse([cx - 29, top_y - 11, cx - 21, top_y - 3], fill=(28, 36, 52, 255), outline=(*TESLA_CYAN, 255))
        # 2. Teléfono celular en el medio
        d_r.rectangle([cx - 5, top_y - 18, cx + 5, top_y], fill=(42, 46, 58, 255), outline=(*INK, 255))
        d_r.line([(cx + 3, top_y - 25), (cx + 3, top_y - 18)], fill=(42, 46, 58, 255), width=2)
        # 3. Laptop a la derecha
        d_r.rectangle([cx + 16, top_y - 18, cx + 36, top_y - 3], fill=(52, 58, 72, 255), outline=(*INK, 255))
        d_r.rectangle([cx + 18, top_y - 16, cx + 34, top_y - 5], fill=(96, 198, 238, 255))
        d_r.rectangle([cx + 14, top_y - 3, cx + 38, top_y], fill=(72, 78, 92, 255), outline=(*INK, 255))
        # Cables brillantes uniéndolos
        if t >= t_cables - 0.3:
            d_r.line([(cx - 18, top_y - 7), (cx - 5, top_y - 7)], fill=(*GOLD, 255), width=2)
            d_r.line([(cx + 5, top_y - 7), (cx + 16, top_y - 7)], fill=(*TESLA_CYAN, 255), width=2)
    floor_prop(cv, _draw_kahn_rig, 240, 248)

    char(cv, "kahn_1997", 142, 248, t, scale=2,
         arms="work" if t < t_c3_07 else "cheer", look=1, mood="happy")

    window(cv, 118, 42, 244, 102, fill=(16, 26, 42), border=GOLD if t >= t_c3_07 else TESLA_CYAN)
    if t < t_c3_07:
        draw_text(cv, "MATERNIDAD DE CALIFORNIA (1997)", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CÁMARA + TELÉFONO + COMPUTADORA", 240, 72, "press", 8, GOLD, align="center")
        draw_text(cv, "UNIDOS CON CABLES EN LA SALA", 240, 96, "silk", 8, CREAM, align="center")
        draw_text(cv, "PHILIPPE KAHN ESPERA A SU HIJA", 240, 116, "silk", 8, SOFT_GRAY, align="center")
    elif t < t_c3_08 - 0.1:
        draw_text(cv, "PRIMERA FOTO AL INSTANTE (1997)", 240, 50, "silk", 8, GOLD, align="center")
        # Retrato pixel-art de la bebé recién nacida transmitiéndose a 2.000 personas
        d.rectangle([216, 64, 264, 102], fill=(244, 232, 218, 255), outline=(*GOLD, 255))
        d.ellipse([230, 72, 250, 92], fill=(242, 196, 160, 255), outline=(*INK, 255))
        draw_text(cv, "ENVIADA A 2.000 PERSONAS", 240, 112, "press", 8, TESLA_CYAN, align="center")
    else:
        draw_text(cv, "EL TELÉFONO EN 1997:", 240, 52, "silk", 8, CREAM, align="center")
        draw_text(cv, "[OK] ESCRIBIR (SMS)", 240, 72, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "[OK] MIRAR (CÁMARA)", 240, 92, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "LE FALTABA PENSAR.", 240, 116, "press", 8, GOLD, align="center")

    return vignette(cv, 0.35)


def scenes():
    return [
        (TL.s("c3_00") - 0.15, make_card(3, ["ESCRIBIR", "Y MIRAR"], "1992 – 1997 · INGLATERRA Y CALIFORNIA", snow=True),
         None, "ch03"),
        (TL.s("c3_01") - 0.15, c3_s01_digital_and_first_sms,
         lambda t: cam_push(t, TL.s("c3_01"), TL.s("c3_06"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_06") - 0.15, c3_s02_first_camera_phone_1997,
         lambda t: cam_push(t, TL.s("c3_06"), TL.s("c4_00"), 1.0, 1.03, (240, 135)), "ch03"),
    ]


def music(A):
    t0 = TL.s("c3_00")
    t_end = TL.s("c4_00")
    A.add_pad(t0, t_end - t0, [146.83, 220.0, 293.66], amp=0.036)


def sfx(A):
    A.fx_pop(TL.s("c3_03"), 0.08)
    A.fx_chime(TL.word("c3_04", "Navidad"), 0.09)
    A.fx_sparkle(TL.s("c3_07"), 0.10)
    A.fx_chime(TL.s("c3_08"), 0.10)
