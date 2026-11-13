"""Capítulo 6: Color y pantalla gigante (pintado a mano, La Pizarra de Technicolor, El mago de Oz, TV vs pantalla ancha/3D y los blockbusters de los 70)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_painting_desk(cv, x, feet=248, t=0.0):
    """Mesa de coloreado manual de películas (c6_01) con tira de celuloide y frasquitos de anilina,
    apoyada firmemente sobre el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 36
        shadow_ellipse(canvas, cx, fy, 30, 4, 88)
        # Patas y tapa de madera hasta el suelo fy
        d.rectangle([cx - 22, top_y + 4, cx - 18, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx + 18, top_y + 4, cx + 22, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx - 26, top_y, cx + 26, top_y + 5], fill=(128, 82, 44, 255), outline=(*INK, 255))
        # Frasquitos de pintura de colores sobre la mesa
        for idx_p, (px_p, col_p) in enumerate(((-16, (238, 68, 68)), (-6, (72, 214, 112)), (4, (78, 158, 248)))):
            d.rectangle([cx + px_p, top_y - 8, cx + px_p + 7, top_y], fill=(*col_p, 255), outline=(*INK, 255))
        # Tira de película sobre atril luminoso
        d.rectangle([cx + 12, top_y - 10, cx + 22, top_y], fill=(244, 224, 148, 255), outline=(*INK, 255))

    floor_prop(cv, _draw, x, feet)


def draw_tv_1950s(cv, x, feet=248, t=0.0):
    """Televisor de los años 50 con gabinete de madera, patas hasta el suelo (feet=248) y antenas 'orejas de conejo'."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 44
        shadow_ellipse(canvas, cx, fy, 26, 4, 90)
        # Patas cónicas de madera de los años 50 hasta el suelo fy
        d.line([(cx - 14, top_y + 28), (cx - 18, fy)], fill=(*INK, 255), width=3)
        d.line([(cx + 14, top_y + 28), (cx + 18, fy)], fill=(*INK, 255), width=3)
        d.line([(cx - 14, top_y + 28), (cx - 18, fy)], fill=(112, 68, 36, 255), width=2)
        d.line([(cx + 14, top_y + 28), (cx + 18, fy)], fill=(112, 68, 36, 255), width=2)
        # Caja de madera del televisor
        d.rectangle([cx - 20, top_y, cx + 20, top_y + 28], fill=(134, 82, 42, 255), outline=(*INK, 255))
        # Pantalla CRT gris/azulada en blanco y negro
        flick = int(round(math.sin(t * 16.0) * 12))
        scr_c = (158 + flick, 168 + flick, 182 + flick, 255)
        d.rectangle([cx - 16, top_y + 4, cx + 8, top_y + 24], fill=scr_c, outline=(*INK, 255))
        # Perillas sintonizadoras a la derecha
        d.ellipse([cx + 11, top_y + 6, cx + 17, top_y + 12], fill=(218, 178, 84, 255), outline=(*INK, 255))
        d.ellipse([cx + 11, top_y + 15, cx + 17, top_y + 21], fill=(218, 178, 84, 255), outline=(*INK, 255))
        # Antenas en V arriba
        d.line([(cx, top_y), (cx - 12, top_y - 12)], fill=(196, 204, 218, 255), width=1)
        d.line([(cx, top_y), (cx + 12, top_y - 12)], fill=(196, 204, 218, 255), width=1)

    floor_prop(cv, _draw, x, feet)


def c6_s01_hand_painted_and_pizarra_rgb(t):
    """c6_01..c6_03: Méliès pintando cuadro por cuadro -> LA PIZARRA 3 (Rojo, Verde y Azul + cámara Technicolor)."""
    t0 = TL.s("c6_01")
    t_c6_02 = TL.s("c6_02")
    t_c6_03 = TL.s("c6_03")
    t_tech = TL.word("c6_03", "Technicolor")

    if t < t_c6_02 - 0.12:
        cv = bg("melies_glass_studio").copy()
        draw_place_only(cv, "LOS PRIMEROS COLORES · PINTADO A MANO", t, t0, border=GOLD)
        char(cv, "melies", 168, 248, t, scale=2, arms="work", look=1, mood="happy")
        draw_painting_desk(cv, 248, 248, t)

        a, dy = pop(t, t0 + 0.1)
        window(cv, 118, 42 + dy, 244, 102, fill=(22, 18, 36), border=GOLD, alpha=0.96)
        draw_text(cv, "PINTADO A MANO, CUADRO A CUADRO", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_filmstrip(cv, 132, 68 + dy, 216, 40, t, speed=18.0, color_frames=True, alpha=0.95)
        draw_text(cv, "MÉLIÈS COLOREABA CON PINCEL", 240, 118 + dy, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    # c6_02..c6_03: LA PIZARRA 3 — Tres colores (Rojo, Verde, Azul) y la cámara Technicolor
    cv = draw_pizarra_frame(
        t, t_c6_02,
        "TRES COLORES · TECHNICOLOR",
        summary_es="ROJO + VERDE + AZUL = TODO COLOR",
        t_summary=t_c6_03 + 0.45,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c6_03 - 0.12:
        # Paso 1 (c6_02): Rojo, verde y azul (mezcla aditiva de luces)
        window(cv, 118, 40, 244, 156, fill=(14, 38, 26), border=CHALK_YELLOW, alpha=0.95)
        draw_text(cv, "1. TRES LUCES: ROJO, VERDE Y AZUL", 240, 48, "press", 8, CHALK_YELLOW, align="center")
        # Tres círculos de luz RGB superpuestos en el centro
        r_c = 28
        circles = [
            (222, 104, (242, 72, 72), "R"),
            (258, 104, (72, 224, 112), "G"),
            (240, 132, (78, 156, 252), "B"),
        ]
        for cx_c, cy_c, col_c, lbl_c in circles:
            glow(cv, cx_c, cy_c, r_c + 4, col_c, 0.55)
            d.ellipse([cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c], outline=(*col_c, 255), width=2)
            draw_text(cv, lbl_c, cx_c, cy_c - 4, "press", 8, col_c, align="center")
        # Centro blanco brillante donde se cruzan las 3 luces
        d.ellipse([231, 107, 249, 125], fill=(255, 252, 240, 255), outline=(*GOLD, 255))
        draw_text(cv, "MEZCLÁNDOLAS SE ARMA TODO COLOR", 240, 172, "silk", 8, CHALK_WHITE, align="center")
        return vignette(cv, 0.26)

    # Paso 2 (c6_03): Cámara de los años 30 filmando 3 películas distintas -> Technicolor
    window(cv, 118, 40, 244, 156, fill=(14, 38, 26), border=CHALK_CYAN, alpha=0.95)
    draw_text(cv, "2. AÑOS 30: TRES TIRAS EN UNA CÁMARA", 240, 48, "press", 8, CHALK_CYAN, align="center")
    # Esquema de prisma dividiendo la luz en 3 rollos (R, G, B) y uniéndolos
    strips = [
        (70, (242, 72, 72), " TIRA ROJA"),
        (98, (72, 224, 112), " TIRA VERDE"),
        (126, (78, 156, 252), " TIRA AZUL"),
    ]
    for sy_s, col_s, txt_s in strips:
        d.rectangle([134, sy_s, 252, sy_s + 20], fill=(18, 28, 22, 255), outline=(*col_s, 255))
        draw_text(cv, txt_s, 193, sy_s + 6, "silk", 8, col_s, align="center")
        d.line([(252, sy_s + 10), (288, 108)], fill=(*col_s, 255), width=2)
    # Cuadro final combinado a todo color
    d.rectangle([288, 86, 348, 130], fill=(248, 204, 88, 255), outline=(*CHALK_WHITE, 255), width=2)
    draw_text(cv, "COLOR", 318, 104, "press", 8, INK, align="center")
    if t >= t_tech - 0.35:
        draw_text(cv, "¡TECHNICOLOR!", 240, 162, "press", 16, CHALK_YELLOW, align="center")

    return vignette(cv, 0.26)


def c6_s02_oz_and_tv_rivalry(t):
    """c6_04..c6_06: 1939 El mago de Oz (sepia -> estalla en color al abrir la puerta) -> Años 50 TV vs Pantalla Ancha y 3D."""
    t_c6_04 = TL.s("c6_04")
    t_puerta = TL.word("c6_04", "puerta")
    t_c6_05 = TL.s("c6_05")
    t_c6_06 = TL.s("c6_06")
    t_anchas = TL.word("c6_06", "anchas")

    base_bg = bg("technicolor_widescreen_1950s").copy()

    if t < t_c6_05 - 0.12:
        # c6_04: 1939 El mago de Oz — empieza en sepia, y cuando se abre la puerta estalla en color
        in_color = t >= t_puerta - 0.15
        if not in_color:
            # Tono sepia cálido antes de abrir la puerta
            cv = grade(base_bg, mul=(0.92, 0.76, 0.52), add=(18, 10, 0))
            border_c = AMBER
            hdr_txt = "1939 · EL MAGO DE OZ (SEPIA)"
        else:
            cv = base_bg
            border_c = GOLD
            hdr_txt = "1939 · ¡EL MUNDO ESTALLA EN COLOR!"

        d = ImageDraw.Draw(cv)
        draw_place_only(cv, hdr_txt, t, t_c6_04, border=border_c)
        char(cv, "spectator_f", 156, 248, t, scale=2,
             arms="cheer" if in_color else "down", look=1, mood="happy")
        char(cv, "spectator", 324, 248, t, scale=2,
             arms="cheer" if in_color else "down", look=-1, mood="happy")

        window(cv, 118, 42, 244, 110, fill=(24, 18, 32), border=border_c, alpha=0.96)
        if not in_color:
            # Puerta cerrada en sepia
            d.rectangle([216, 56, 264, 122], fill=(128, 94, 58, 255), outline=(*INK, 255))
            d.ellipse([252, 88, 258, 94], fill=(*GOLD, 255))
            draw_text(cv, "EMPEZABA EN SEPIA...", 240, 130, "press", 8, AMBER, align="center")
        else:
            # Puerta abierta de par en par con arcoíris Technicolor y camino amarillo
            rainbow_cols = [(242, 68, 68), (248, 198, 68), (72, 224, 112), (78, 168, 252)]
            for idx_r, r_col in enumerate(rainbow_cols):
                d.rectangle([132 + idx_r * 54, 54, 132 + (idx_r + 1) * 54, 114],
                            fill=(*r_col, 255), outline=(*INK, 255))
            draw_text(cv, "¡PUERTA AL TECHNICOLOR!", 240, 80, "press", 8, CREAM, align="center")
            draw_text(cv, "EL MUNDO ESTALLABA EN COLOR", 240, 126, "press", 8, GOLD, align="center")
            sparkle(cv, 148, 66, t * 5.0, 4, CREAM)
            sparkle(cv, 332, 66, t * 5.0 + 1.2, 4, CREAM)
        return vignette(cv, 0.32)

    if t < t_c6_06 - 0.12:
        # c6_05: En los años 50 la televisión llenó las casas y las salas se empezaron a vaciar
        cv = grade(base_bg, mul=(0.76, 0.78, 0.88))
        draw_place_only(cv, "AÑOS 1950 · LA TELEVISIÓN EN CASA", t, t_c6_05, border=SOFT_GRAY)
        draw_tv_1950s(cv, 214, 248, t)
        char(cv, "spectator", 282, 248, t, scale=2, arms="down", look=-1, mood="neutral")

        a, dy = pop(t, t_c6_05 - 0.1)
        window(cv, 118, 44 + dy, 244, 86, fill=(20, 22, 36), border=SOFT_GRAY, alpha=0.95)
        draw_text(cv, "LA RIVAL DE LOS AÑOS 50", 240, 54 + dy, "press", 8, SOFT_GRAY, align="center")
        draw_text(cv, "LA TELEVISIÓN LLENÓ LAS CASAS", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "Y LAS SALAS SE EMPEZARON A VACIAR", 240, 94 + dy, "silk", 8, CHALK_RED, align="center")
        return vignette(cv, 0.36)

    # c6_06: El cine respondió con pantallas más anchas, sonido rodeando la sala y anteojos 3D
    cv = base_bg
    d = ImageDraw.Draw(cv)
    draw_place_only(cv, "AÑOS 50 · PANTALLA ANCHA, SONIDO Y 3D", t, t_c6_06, border=TESLA_CYAN)
    char(cv, "spectator", 152, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    char(cv, "spectator_f", 328, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

    a, dy = pop(t, t_c6_06 - 0.1)
    window(cv, 116, 42 + dy, 248, 112, fill=(18, 22, 40), border=TESLA_CYAN, alpha=0.96)
    draw_text(cv, "LA RESPUESTA DEL CINE:", 240, 50 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "1. PANTALLAS MÁS ANCHAS", 240, 68 + dy, "silk", 8, TESLA_CYAN, align="center")
    draw_text(cv, "2. SONIDO RODEANDO LA SALA", 240, 84 + dy, "silk", 8, CREAM, align="center")
    # Anteojos 3D clásicos (lente rojo y lente cian)
    gx0, gy0 = 204, 102 + dy
    d.rectangle([gx0, gy0, gx0 + 72, gy0 + 22], fill=(242, 238, 228, 255), outline=(*INK, 255))
    d.rectangle([gx0 + 6, gy0 + 4, gx0 + 32, gy0 + 18], fill=(238, 62, 62, 255), outline=(*INK, 255))
    d.rectangle([gx0 + 40, gy0 + 4, gx0 + 66, gy0 + 18], fill=(64, 214, 245, 255), outline=(*INK, 255))
    draw_text(cv, "3. ANTEOJOS 3D", 240, 130 + dy, "press", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.32)


def c6_s03_blockbusters_and_punchline(t):
    """c6_07..c6_08: Años 70 Tiburón y La guerra de las galaxias -> 'Cada vez que apareció una pantalla rival, el cine se hizo más grande.'"""
    t_c6_07 = TL.s("c6_07")
    t_galaxias = TL.word("c6_07", "galaxias")
    t_c6_08 = TL.s("c6_08")
    t_grande = TL.word("c6_08", "grande")

    cv = bg("technicolor_widescreen_1950s").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c6_08 - 0.12:
        draw_place_only(cv, "AÑOS 1970 · EL ESTRENO GIGANTE DE VERANO", t, t_c6_07, border=GOLD)
        # Fila de espectadores dando la vuelta a la manzana
        for idx_p, (key_p, px_p) in enumerate((("spectator", 104), ("spectator_f", 156), ("spectator", 324), ("spectator_f", 376))):
            char(cv, key_p, px_p, 248, t, scale=2, arms="cheer" if idx_p % 2 == 0 else "down",
                 look=1 if px_p < 240 else -1, mood="happy")

        a, dy = pop(t, t_c6_07 - 0.1)
        window(cv, 116, 40 + dy, 248, 114, fill=(16, 20, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "LOS AÑOS 70 · ÉXITOS DE VERANO", 240, 48 + dy, "press", 8, GOLD, align="center")
        # Dos marquesinas: TIBURÓN (1975) y LA GUERRA DE LAS GALAXIAS (1977)
        d.rectangle([126, 66 + dy, 354, 92 + dy], fill=(18, 48, 78, 255), outline=(*TESLA_CYAN, 255))
        draw_text(cv, "1975 · TIBURÓN", 240, 75 + dy, "press", 8, TESLA_CYAN, align="center")
        if t >= t_galaxias - 0.45:
            d.rectangle([126, 98 + dy, 354, 124 + dy], fill=(18, 16, 32, 255), outline=(*GOLD, 255))
            draw_text(cv, "1977 · LA GUERRA DE LAS GALAXIAS", 240, 107 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "FILAS DANDO VUELTA A LA MANZANA", 240, 134 + dy, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.32)

    # c6_08: Remate — "Cada vez que apareció una pantalla rival, el cine se hizo más grande."
    draw_place_only(cv, "LA LEY DE LA PANTALLA GRANDE", t, t_c6_08, border=GOLD)
    draw_tv_1950s(cv, 148, 248, t)
    char(cv, "spectator", 240, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    char(cv, "spectator_f", 332, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

    a, dy = pop(t, t_c6_08 - 0.1)
    window(cv, 116, 44 + dy, 248, 102, fill=(18, 18, 36), border=GOLD, alpha=0.96)
    draw_text(cv, "CADA VEZ QUE APARECIÓ", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "UNA PANTALLA RIVAL,", 240, 74 + dy, "press", 8, TESLA_CYAN, align="center")
    if t >= t_grande - 0.45:
        draw_text(cv, "EL CINE SE HIZO MÁS GRANDE.", 240, 102 + dy, "press", 8, GOLD, align="center")

    return vignette(cv, 0.32)


def scenes():
    return [
        (TL.s("c6_00") - 0.15, make_card(6, ["COLOR Y PANTALLA", "GIGANTE"], "1930 – 1977 · TECHNICOLOR Y BLOCKBUSTERS"),
         None, "ch06"),
        (TL.s("c6_01") - 0.15, c6_s01_hand_painted_and_pizarra_rgb,
         None, "ch06"),
        (TL.s("c6_04") - 0.15, c6_s02_oz_and_tv_rivalry,
         lambda t: cam_push(t, TL.s("c6_04"), TL.s("c6_07"), 1.0, 1.03, (240, 135)), "ch06"),
        (TL.s("c6_07") - 0.15, c6_s03_blockbusters_and_punchline,
         lambda t: cam_push(t, TL.s("c6_07"), TL.s("c7_00"), 1.0, 1.03, (240, 135)), "ch06"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_pop(TL.s("c6_02"), 0.08)
    A.fx_sparkle(TL.word("c6_04", "color"), 0.11)
    A.fx_chime(TL.word("c6_07", "galaxias"), 0.10)
    A.fx_chime(TL.word("c6_08", "grande"), 0.12)
