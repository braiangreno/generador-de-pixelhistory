"""Capítulo 7: Lo que vale una empresa (LA PIZARRA 3: billón vs trillion, acciones, valor de mercado y por qué puede caer sin que se rompa una sola máquina)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c7_card = make_card(7, ["LO QUE VALE", "UNA EMPRESA"], "LA PIZARRA · VALOR DE MERCADO")


def c7_s01_pizarra_valuation(t):
    """c7_01..c7_06: LA PIZARRA · LO QUE VALE UNA EMPRESA."""
    t0 = TL.s("c7_01")
    t_c7_02 = TL.s("c7_02")
    t_c7_03 = TL.s("c7_03")
    t_c7_04 = TL.s("c7_04")
    t_c7_05 = TL.s("c7_05")
    t_c7_06 = TL.s("c7_06")

    cv = draw_pizarra_frame(
        t, t0, "LO QUE VALE UNA EMPRESA",
        summary_es="VALE LO QUE SE CREE QUE VA A TENER",
        t_summary=t_c7_06,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c7_03 - 0.12:
        # c7_01..c7_02: Número gigante 6.000.000.000.000 + Billón (ES) = Trillion (EN)
        window(cv, 98, 42, 284, 62, fill=(14, 34, 24), border=CHALK_YELLOW, alpha=0.95)
        draw_text(cv, "¿QUÉ SIGNIFICA VALER US$ 6 BILLONES?", 240, 50, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "US$ 6.000.000.000.000", 240, 68, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "UN SEIS SEGUIDO DE DOCE CEROS", 240, 86, "silk", 8, CHALK_CYAN, align="center")

        if t >= t_c7_02 - 0.1:
            window(cv, 98, 114, 284, 72, fill=(14, 34, 24), border=CHALK_CYAN, alpha=0.95)
            draw_text(cv, "EN ESPAÑOL: UN BILLÓN", 240, 124, "press", 8, CHALK_CYAN, align="center")
            draw_text(cv, "UN MILLÓN DE MILLONES (10^12)", 240, 144, "silk", 8, CHALK_WHITE, align="center")
            draw_text(cv, "EN INGLÉS SE DICE «ONE TRILLION»", 240, 164, "silk", 8, CHALK_YELLOW, align="center")
        draw_chalk_hand(cv, 326, 92, t)
        return vignette(cv, 0.28)

    if t < t_c7_05 - 0.12:
        # c7_03..c7_04: Torta cortada en porciones (Acciones: Precio x Cantidad) y mirada hacia el futuro
        window(cv, 98, 40, 284, 66, fill=(14, 34, 24), border=CHALK_WHITE, alpha=0.95)
        draw_text(cv, "UNA EMPRESA EN BOLSA SE DIVIDE EN:", 240, 48, "silk", 8, CHALK_WHITE, align="center")
        draw_text(cv, "MILLONES DE PARTES = ACCIONES", 240, 66, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "PRECIO DE 1 ACCIÓN × TOTAL = VALOR", 240, 86, "silk", 8, CHALK_CYAN, align="center")

        # Gráfico circular (torta de acciones) en el centro
        cx_p, cy_p, r_p = 152, 148, 24
        d.ellipse([cx_p - r_p, cy_p - r_p, cx_p + r_p, cy_p + r_p], fill=(22, 56, 38, 255), outline=(*CHALK_YELLOW, 255), width=2)
        for ang_d in range(0, 360, 45):
            ar = math.radians(ang_d)
            d.line([(cx_p, cy_p), (int(cx_p + math.cos(ar) * r_p), int(cy_p + math.sin(ar) * r_p))], fill=(*CHALK_WHITE, 220))

        if t >= t_c7_04 - 0.1:
            window(cv, 186, 114, 196, 68, fill=(14, 34, 24), border=CHALK_GREEN, alpha=0.95)
            draw_text(cv, "NO ES PLATA GUARDADA", 284, 124, "press", 8, CHALK_RED, align="center")
            draw_text(cv, "ES LO QUE LA GENTE CREE", 284, 144, "silk", 8, CHALK_WHITE, align="center")
            draw_text(cv, "QUE GANARÁ EN EL FUTURO", 284, 162, "silk", 8, CHALK_GREEN, align="center")
        return vignette(cv, 0.28)

    # c7_05..c7_06: Fábrica intacta a la izquierda mientras el número cae a la derecha + EN UNA FRASE
    window(cv, 98, 40, 284, 76, fill=(14, 34, 24), border=CHALK_YELLOW, alpha=0.95)
    draw_text(cv, "SI MAÑANA DUDAN DEL FUTURO:", 240, 48, "silk", 8, CHALK_WHITE, align="center")
    draw_text(cv, "EL PRECIO CAE EN HORAS", 240, 66, "press", 8, CHALK_RED, align="center")
    draw_text(cv, "SIN QUE SE ROMPA UNA SOLA MÁQUINA", 240, 86, "silk", 8, CHALK_GREEN, align="center")

    # Pequeño centro de datos intacto en tiza verde vs flecha roja de cotización
    d.rectangle([122, 126, 214, 182], fill=(16, 42, 28, 255), outline=(*CHALK_GREEN, 255))
    draw_text(cv, "FÁBRICA INTACTA", 168, 148, "silk", 8, CHALK_GREEN, align="center")
    d.rectangle([246, 126, 358, 182], fill=(28, 22, 24, 255), outline=(*CHALK_RED, 255))
    draw_text(cv, "COTIZACIÓN ↓", 302, 148, "press", 8, CHALK_RED, align="center")
    return vignette(cv, 0.28)


def scenes():
    return [
        (TL.s("c7_00") - 0.15, c7_card),
        (TL.s("c7_01"), c7_s01_pizarra_valuation,
         lambda t: cam_push(t, TL.s("c7_01"), TL.s("c8_00"), 1.0, 1.025, (240, 135), (240, 135))),
    ]


def music(A):
    A.add_pad(TL.s("c7_00"), TL.e("c7_06") - TL.s("c7_00"), (146.83, 174.61, 220.0), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c7_01") + 0.15, 0.05)
    A.fx_chime(TL.s("c7_03") + 0.2, 0.05)
    A.fx_thud(TL.s("c7_05") + 0.25, 0.06)
    A.fx_chime(TL.s("c7_06") + 0.2, 0.06)
