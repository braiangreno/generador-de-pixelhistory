"""Capítulo 2: La cabeza del muñeco (John Logie Baird, Stooky Bill y William Taynton, 1925-1926)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_baird_rig_prop(cv, x, feet=248, t=0.0, show_dummy=True):
    """Mesa de trabajo del altillo de Baird apoyada en el suelo (feet=248) con el disco Televisor,
    lámparas incandescentes y el soporte con la cabeza del muñeco Stooky Bill."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 44, 5, 85)
        # Patas de madera hasta fy y tapa de la mesa
        d.rectangle([cx - 32, top_y + 5, cx - 26, fy], fill=(74, 46, 26, 255), outline=(*INK, 255))
        d.rectangle([cx + 26, top_y + 5, cx + 32, fy], fill=(74, 46, 26, 255), outline=(*INK, 255))
        d.rectangle([cx - 36, top_y, cx + 36, top_y + 6], fill=(118, 76, 42, 255), outline=(*INK, 255))

        # Disco giratorio de Baird a la izquierda sobre la mesa
        dx_c, dy_c, r_d = cx - 14, top_y - 18, 15
        d.rectangle([dx_c - 3, top_y - 6, dx_c + 3, top_y], fill=(58, 62, 74, 255), outline=(*INK, 255))
        d.ellipse([dx_c - r_d, dy_c - r_d, dx_c + r_d, dy_c + r_d], fill=(158, 92, 54, 255), outline=(*INK, 255))
        for i in range(6):
            ang = t * 4.2 + i * (math.pi / 3)
            hx = int(round(dx_c + math.cos(ang) * 9))
            hy = int(round(dy_c + math.sin(ang) * 9))
            d.rectangle([hx - 1, hy - 1, hx + 1, hy + 1], fill=(255, 224, 132, 255))

        # Lámpara caliente en el centro de la mesa
        glow(canvas, cx + 4, top_y - 14, 18, AMBER, 0.5)
        d.rectangle([cx + 2, top_y - 8, cx + 6, top_y], fill=(92, 96, 108, 255), outline=(*INK, 255))
        d.ellipse([cx, top_y - 16, cx + 8, top_y - 8], fill=(255, 234, 142, 255), outline=(*INK, 255))

        # Cabeza del muñeco de ventrílocuo Stooky Bill en su pedestal sobre la mesa
        if show_dummy:
            mx = cx + 20
            d.rectangle([mx - 4, top_y - 6, mx + 4, top_y], fill=(82, 52, 32, 255), outline=(*INK, 255))
            d.ellipse([mx - 7, top_y - 20, mx + 7, top_y - 5], fill=(238, 182, 138, 255), outline=(*INK, 255))
            d.arc([mx - 7, top_y - 21, mx + 7, top_y - 11], 180, 360, fill=(168, 72, 42, 255), width=3)
            d.point((mx - 3, top_y - 14), fill=(18, 16, 24, 255))
            d.point((mx + 3, top_y - 14), fill=(18, 16, 24, 255))
            d.line([(mx - 3, top_y - 9), (mx + 3, top_y - 9)], fill=(168, 44, 44, 255))
    floor_prop(cv, _draw, x, feet)


def c2_s01_stooky_bill(t):
    """c2_01..c2_03: Altillo en Londres, John Logie Baird y el muñeco Stooky Bill."""
    t0 = TL.s("c2_01")
    t_c2_02 = TL.s("c2_02")
    t_calor = TL.word("c2_02", "calor")
    t_c2_03 = TL.s("c2_03")
    t_cor = TL.word("c2_03", "corriendo")

    cv = bg("london_attic_1926").copy()
    draw_place_only(cv, "LONDRES · 1925", t, t0, border=AMBER)
    d = ImageDraw.Draw(cv)

    # Ventana central (x=118..362, w=244)
    window(cv, 118, 44, 244, 102, fill=(22, 18, 28), border=AMBER, alpha=0.94)
    if t < t_c2_02 - 0.1:
        draw_text(cv, "JOHN LOGIE BAIRD · LONDRES", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "DISCOS QUE GIRAN + LÁMPARAS", 240, 74, "silk", 8, CREAM, align="center")
        draw_scanline_beam(cv, 152, 92, 176, 42, t, rows=5, speed=1.4, color=AMBER)
    elif t < t_c2_03 - 0.1:
        draw_text(cv, "PRIMER ACTOR: STOOKY BILL", 240, 52, "press", 8, AMBER, align="center")
        # Retrato del muñeco bajo el calor de las lámparas
        d.ellipse([222, 70, 258, 106], fill=(238, 182, 138, 255), outline=(*GOLD, 255))
        d.point((234, 84), fill=(*INK, 255))
        d.point((246, 84), fill=(*INK, 255))
        d.rectangle([234, 93, 246, 97], fill=(168, 48, 48, 255))
        if t >= t_calor - 0.2:
            glow(cv, 240, 88, 28, AMBER, 0.45)
        draw_text(cv, "NO SE QUEJABA DEL CALOR", 240, 118, "silk", 8, CHALK_YELLOW, align="center")
    else:
        draw_text(cv, "¡LA CARA APARECIÓ EN PANTALLA!", 240, 54, "press", 8, CHALK_GREEN, align="center")
        # Pequeña pantalla anaranjada de 30 líneas con la cara del muñeco
        d.rectangle([204, 72, 276, 118], fill=(48, 20, 12, 255), outline=(*AMBER, 255))
        for ry in range(75, 116, 3):
            d.line([(206, ry), (274, ry)], fill=(218, 104, 42, 210))
        d.ellipse([228, 80, 252, 108], fill=(248, 148, 68, 230))
        draw_text(cv, "BAJÓ CORRIENDO LAS ESCALERAS", 240, 126, "silk", 8, CREAM, align="center")

    # Baird trabajando o saliendo corriendo hacia las escaleras
    bx, bw = (walk(t, t_cor - 0.1, TL.e("c2_03"), 162, 86) if t >= t_cor - 0.1 else (162, None))
    char(cv, "baird", bx, 248, t, scale=2, walk=bw,
         arms="cheer" if t >= t_c2_03 else "work",
         look=-1 if t >= t_cor - 0.1 else 1,
         mood="happy" if t >= t_c2_03 else "neutral")
    draw_baird_rig_prop(cv, 298, 248, t, show_dummy=True)

    return vignette(cv, 0.36)


def c2_s02_taynton_and_1926(t):
    """c2_04..c2_06: William Taynton (primera persona televisada) y demostración de enero de 1926."""
    t0 = TL.s("c2_04")
    t_prim = TL.word("c2_04", "primera")
    t_c2_05 = TL.s("c2_05")
    t_treinta = TL.word("c2_05", "treinta")
    t_c2_06 = TL.s("c2_06")

    cv = bg("london_attic_1926").copy()
    draw_place_only(cv, "LONDRES · ENERO DE 1926", t, t0, border=GOLD)
    d = ImageDraw.Draw(cv)

    window(cv, 118, 44, 244, 104, fill=(24, 18, 28), border=GOLD, alpha=0.95)
    if t < t_c2_05 - 0.1:
        draw_text(cv, "WILLIAM TAYNTON (20 AÑOS)", 240, 52, "press", 8, GOLD, align="center")
        # Pantalla naranja mostrando el rostro de Taynton en vivo
        d.rectangle([198, 70, 282, 120], fill=(52, 22, 14, 255), outline=(*AMBER, 255))
        for ry in range(73, 118, 3):
            d.line([(200, ry), (280, ry)], fill=(228, 112, 48, 215))
        d.ellipse([226, 78, 254, 110], fill=(252, 162, 82, 240))
        d.point((235, 92), fill=(48, 20, 12, 255))
        d.point((245, 92), fill=(48, 20, 12, 255))
        lbl_t = "1.ª PERSONA TELEVISADA" if t >= t_prim - 0.2 else "EMPLEADO DE LA OFICINA DE ABAJO"
        draw_text(cv, lbl_t, 240, 128, "silk", 8, CHALK_GREEN if t >= t_prim - 0.2 else CREAM, align="center")

        char(cv, "baird", 142, 248, t, scale=2, arms="point", look=1, mood="happy")
        draw_baird_rig_prop(cv, 248, 248, t, show_dummy=False)
        char(cv, "taynton", 342, 248, t, scale=2, arms="wave", look=-1, mood="happy")
    else:
        # Enero de 1926: demostración ante 40 científicos; imagen chiquita, anaranjada y de 30 renglones
        draw_text(cv, "DEMOSTRACIÓN · ENERO DE 1926", 240, 52, "press", 8, GOLD, align="center")
        d.rectangle([144, 70, 232, 122], fill=(48, 18, 12, 255), outline=(*AMBER, 255))
        for ry in range(73, 120, 3):
            d.line([(146, ry), (230, ry)], fill=(238, 118, 48, 220))
        d.ellipse([174, 80, 202, 112], fill=(255, 164, 84, 240))
        draw_text(cv, "40 CIENTÍFICOS", 296, 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "IMAGEN ANARANJADA", 296, 92, "silk", 8, AMBER, align="center")
        if t >= t_treinta - 0.2:
            draw_text(cv, "APENAS 30 RENGLONES", 296, 108, "press", 8, CHALK_YELLOW, align="center")
        if t >= t_c2_06 - 0.1:
            draw_text(cv, "UN DISCO QUE GIRA TENÍA LÍMITE", 240, 130, "silk", 8, CHALK_RED, align="center")

        char(cv, "baird", 148, 248, t, scale=2, arms="offer", look=1, mood="happy")
        draw_baird_rig_prop(cv, 244, 248, t, show_dummy=True)
        char(cv, "tolman", 342, 248, t, scale=2, arms="think", look=-1, mood="neutral")

    return vignette(cv, 0.36)


SCENES = [
    (TL.s("c2_00") - 0.15, TL.s("c2_01"), make_card(2, ["LA CABEZA DEL", "MUÑECO"], "1925 – 1926 · LONDRES")),
    (TL.s("c2_01") - 0.15, TL.s("c2_04"), c2_s01_stooky_bill),
    (TL.s("c2_04") - 0.15, TL.s("c3_00"), c2_s02_taynton_and_1926),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    A.add_pad(TL.s("c2_00"), TL.e("c2_06") - TL.s("c2_00"), (196.0, 246.94, 293.66), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c2_02"), 0.08)
    A.fx_chime(TL.s("c2_03"), 0.10)
    A.fx_sparkle(TL.word("c2_04", "primera"), 0.10)
    A.fx_pop(TL.s("c2_05"), 0.08)
