"""Capítulo 6: Quinientas aplicaciones (App Store julio 2008, 10 millones en un fin de semana y llegada de Android)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c6_s01_app_store_2008(t):
    """c6_01..c6_03: Julio de 2008 abre la tienda con 500 aplicaciones, 10 millones de descargas, linterna/juego/mapa."""
    t0 = TL.s("c6_01")
    t_c6_02 = TL.s("c6_02")
    t_diez = TL.word("c6_02", "diez")
    t_c6_03 = TL.s("c6_03")

    cv = bg("indie_dev_room_2008").copy()
    draw_place_only(cv, "JULIO DE 2008 · TIENDA DE APLICACIONES", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    # Escritorio con laptop del programador indie apoyado en el suelo
    def _draw_dev_desk(canvas, cx, fy):
        d_k = ImageDraw.Draw(canvas)
        top_y = fy - 40
        shadow_ellipse(canvas, cx, fy, 36, 4, 85)
        d_k.rectangle([cx - 30, top_y + 5, cx - 24, fy], fill=(64, 44, 30, 255), outline=(*INK, 255))
        d_k.rectangle([cx + 24, top_y + 5, cx + 30, fy], fill=(64, 44, 30, 255), outline=(*INK, 255))
        d_k.rectangle([cx - 34, top_y, cx + 34, top_y + 5], fill=(118, 80, 52, 255), outline=(*INK, 255))
        terminal(canvas, cx - 15, top_y - 26, t, on=True)
    floor_prop(cv, _draw_dev_desk, 240, 248)

    char(cv, "indie_dev", 152, 248, t, scale=2,
         arms="type" if t < t_c6_03 else "cheer", look=1, mood="happy")

    window(cv, 118, 42, 244, 104, fill=(14, 24, 44), border=GOLD if t >= t_c6_02 else TESLA_CYAN)
    if t < t_c6_02:
        draw_text(cv, "2007: CERRADO A OTROS PROGRAMAS", 240, 56, "silk", 8, CHALK_RED, align="center")
        draw_text(cv, "2008: SE ABRE LA PUERTA", 240, 82, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CUALQUIERA PUEDE CREAR APPS", 240, 108, "silk", 8, CREAM, align="center")
    elif t < t_c6_03:
        draw_text(cv, "JULIO DE 2008 · ESTRENO:", 240, 50, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "500 APLICACIONES", 240, 68, "press", 8, GOLD, align="center")
        if t >= t_diez - 0.3:
            draw_text(cv, "PRIMER FIN DE SEMANA:", 240, 92, "silk", 8, CREAM, align="center")
            draw_text(cv, "10.000.000 DE DESCARGAS", 240, 110, "press", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "DE UNA HABITACIÓN AL MUNDO ENTERO", 240, 50, "silk", 8, GOLD, align="center")
        apps = [("LINTERNA", 156, GOLD), ("JUEGO", 240, PX_MAGENTA if "PX_MAGENTA" in globals() else TESLA_VIOLET), ("MAPA", 324, CHALK_GREEN)]
        for lbl, ax, col in apps:
            d.rectangle([ax - 30, 68, ax + 30, 106], fill=(24, 36, 62, 255), outline=(*col, 255), width=2)
            draw_text(cv, lbl, ax, 84, "silk", 8, col, align="center")
        draw_text(cv, "NUEVA ECONOMÍA DE BOLSILLO", 240, 118, "silk", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.35)


def c6_s02_android_and_ecosystem(t):
    """c6_04..c6_07: Sale el primer teléfono con Android (teclado deslizable), abierto a fabricantes, 2 de cada 3 hoy."""
    t0 = TL.s("c6_04")
    t_c6_05 = TL.s("c6_05")
    t_c6_06 = TL.s("c6_06")
    t_c6_07 = TL.s("c6_07")

    cv = bg("indie_dev_room_2008").copy()
    draw_place_only(cv, "OCTUBRE DE 2008 · ANDROID (GOOGLE)", t, t0, border=CHALK_GREEN)
    d = ImageDraw.Draw(cv)

    char(cv, "indie_dev", 148, 248, t, scale=2, arms="point", look=1, mood="happy")
    char(cv, "pedestrian_modern", 332, 248, t, scale=2, arms="hold", facing=-1, look=-1, mood="happy")
    draw_held_smartphone(cv, 332, 248, t, glow_col=CHALK_GREEN, facing=-1)

    window(cv, 116, 42, 248, 106, fill=(14, 26, 38), border=CHALK_GREEN if t < t_c6_07 else GOLD)
    if t < t_c6_05:
        draw_text(cv, "PRIMER TELÉFONO CON ANDROID (2008)", 240, 50, "silk", 8, CHALK_GREEN, align="center")
        # Teléfono con pantalla que se desliza mostrando teclado físico debajo
        slide = int(round(6 * (0.5 + 0.5 * math.sin(t * 3.0))))
        d.rectangle([206, 86, 274, 114], fill=(64, 70, 82, 255), outline=(*INK, 255))
        d.rectangle([206, 68 - slide, 274, 96 - slide], fill=(32, 128, 92, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "TECLADO DESLIZABLE DEBAJO", 240, 124, "silk", 8, CREAM, align="center")
    elif t < t_c6_06:
        draw_text(cv, "LA DIFERENCIA CLAVE:", 240, 52, "silk", 8, GOLD, align="center")
        draw_text(cv, "ABIERTO A CUALQUIER FABRICANTE", 240, 76, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "DECENAS DE MARCAS EN TODO EL MUNDO", 240, 104, "silk", 8, CREAM, align="center")
    elif t < t_c6_07 - 0.1:
        draw_text(cv, "EL MUNDO HOY (CADA 3 SMARTPHONES):", 240, 50, "silk", 8, CREAM, align="center")
        # 3 íconos de teléfono: 2 verdes (Android) y 1 cian (iPhone)
        phones = [(176, CHALK_GREEN, "ANDROID"), (240, CHALK_GREEN, "ANDROID"), (304, TESLA_CYAN, "IPHONE")]
        for px, col, lbl in phones:
            d.rectangle([px - 14, 68, px + 14, 110], fill=(22, 30, 44, 255), outline=(*col, 255), width=2)
            d.rectangle([px - 11, 73, px + 11, 103], fill=(*col, 200))
            draw_text(cv, lbl, px, 116, "silk", 8, col, align="center")
    else:
        draw_text(cv, "LA REGLA MODERNA:", 240, 56, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "TU TELÉFONO ES", 240, 78, "press", 8, CREAM, align="center")
        draw_text(cv, "LO QUE LE INSTALAS.", 240, 102, "press", 8, GOLD, align="center")

    return vignette(cv, 0.35)


def scenes():
    return [
        (TL.s("c6_00") - 0.15, make_card(6, ["QUINIENTAS", "APLICACIONES"], "2008 · APP STORE Y ANDROID"),
         None, "ch06"),
        (TL.s("c6_01") - 0.15, c6_s01_app_store_2008,
         lambda t: cam_push(t, TL.s("c6_01"), TL.s("c6_04"), 1.0, 1.03, (240, 135)), "ch06"),
        (TL.s("c6_04") - 0.15, c6_s02_android_and_ecosystem,
         lambda t: cam_push(t, TL.s("c6_04"), TL.s("c7_00"), 1.0, 1.03, (240, 135)), "ch06"),
    ]


def music(A):
    t0 = TL.s("c6_00")
    t_end = TL.s("c7_00")
    A.add_pad(t0, t_end - t0, [146.83, 220.0, 293.66], amp=0.036)


def sfx(A):
    A.fx_pop(TL.s("c6_02"), 0.09)
    A.fx_sparkle(TL.word("c6_02", "diez"), 0.10)
    A.fx_pop(TL.s("c6_04"), 0.08)
    A.fx_chime(TL.s("c6_07"), 0.10)
