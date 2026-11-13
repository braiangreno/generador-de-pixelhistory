"""Capítulo 2: Treinta y tres espectadores (El kinetoscopio, los hermanos Lumière y el Grand Café de París, 1895)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c2_s01_kinetoscope_and_cinematograph(t):
    """c2_01..c2_03: El Kinetoscopio de Edison (mirar solo en una caja) -> Antoine Lumière -> El Cinematógrafo."""
    t0 = TL.s("c2_01")
    t_moneda = TL.word("c2_01", "moneda")
    t_c2_02 = TL.s("c2_02")
    t_hijos = TL.word("c2_02", "hijos")
    t_c2_03 = TL.s("c2_03")
    t_cine = TL.word("c2_03", "cinematógrafo")

    cv = bg("paris_salon_indien_1895").copy()

    if t < t_c2_02 - 0.12:
        draw_place_only(cv, "ESTADOS UNIDOS · EL KINETOSCOPIO", t, t0, border=AMBER)
        # Edison junto al gabinete del Kinetoscopio apoyado en el suelo (feet=248) y espectador mirando solo
        char(cv, "edison", 142, 248, t, scale=2, arms="hips", look=1, mood="neutral",
             talk=talk_v(t, t0 <= t < t_c2_02 - 0.2))
        draw_kinetoscope_box(cv, 240, 248, t, peep_glow=True)
        char(cv, "spectator", 292, 248, t, scale=2,
             arms="hold" if t >= t_moneda - 0.2 else "down", look=-1, mood="happy")

        a, dy = pop(t, t0 + 0.1)
        window(cv, 118, 42 + dy, 244, 88, fill=(20, 18, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "EL KINETOSCOPIO DE EDISON", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "CAJA CON MIRILLA INDIVIDUAL", 240, 68 + dy, "silk", 8, CREAM, align="center")
        if t >= t_moneda - 0.25:
            draw_text(cv, "1 MONEDA -> MIRABAS SOLO", 240, 88 + dy, "silk", 8, TESLA_CYAN, align="center")
            draw_text(cv, "PELÍCULA DE POCOS SEGUNDOS", 240, 104 + dy, "silk", 8, CHALK_YELLOW, align="center")
        return vignette(cv, 0.36)

    if t < t_c2_03 - 0.12:
        # c2_02: Antoine Lumière ve la caja en París y vuelve a casa con una idea para sus hijos
        draw_place_only(cv, "PARÍS · ANTOINE LUMIÈRE", t, t_c2_02, border=GOLD)
        draw_kinetoscope_box(cv, 148, 248, t, peep_glow=False)
        char(cv, "antoine_lumiere", 224, 248, t, scale=2,
             arms="point" if t >= t_hijos - 0.3 else "think", look=1, mood="happy",
             talk=talk_v(t, t >= t_c2_02))
        char(cv, "auguste_lumiere", 316, 248, t, scale=2, arms="down", look=-1, mood="neutral")
        char(cv, "louis_lumiere", 368, 248, t, scale=2, arms="think", look=-1, mood="happy")

        a, dy = pop(t, t_c2_02 - 0.1)
        window(cv, 118, 44 + dy, 244, 78, fill=(20, 18, 32), border=GOLD, alpha=0.95)
        draw_text(cv, "ANTOINE LUMIÈRE (FOTÓGRAFO)", 240, 54 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "VIO LA CAJA EN PARÍS", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "«¡SAQUEMOS LA IMAGEN A UNA PANTALLA!»", 240, 92 + dy, "silk", 8, TESLA_CYAN, align="center")
        return vignette(cv, 0.36)

    # c2_03: Auguste y Louis Lumière inventan el Cinematógrafo (filma, copia y proyecta)
    draw_place_only(cv, "LYON Y PARÍS · HERMANOS LUMIÈRE", t, t_c2_03, border=TESLA_CYAN)
    char(cv, "auguste_lumiere", 148, 248, t, scale=2, arms="cheer" if t >= t_cine else "point",
         look=1, mood="happy")
    draw_cinematograph_tripod(cv, 240, 248, t, beam=True, crank=True, facing=1)
    char(cv, "louis_lumiere", 332, 248, t, scale=2, arms="work", look=-1, mood="happy")

    a, dy = pop(t, t_c2_03 - 0.1)
    window(cv, 118, 42 + dy, 244, 96, fill=(18, 22, 38), border=TESLA_CYAN, alpha=0.96)
    draw_text(cv, "AUGUSTE Y LOUIS LUMIÈRE", 240, 50 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EL CINEMATÓGRAFO", 240, 68 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "1. FILMABA  ·  2. COPIABA", 240, 90 + dy, "silk", 8, TESLA_CYAN, align="center")
    draw_text(cv, "3. PROYECTABA EN PANTALLA", 240, 108 + dy, "silk", 8, CHALK_GREEN, align="center")

    return vignette(cv, 0.35)


def c2_s02_salon_indien_1895(t):
    """c2_04..c2_06: 28 de diciembre de 1895 en el sótano del Grand Café (100 sillas, 33 personas, 10 películas)."""
    t0 = TL.s("c2_04")
    t_franco = TL.word("c2_04", "franco")
    t_c2_05 = TL.s("c2_05")
    t_treinta = TL.word("c2_05", "treinta")
    t_c2_06 = TL.s("c2_06")
    t_bebe = TL.word("c2_06", "bebé")
    t_jard = TL.word("c2_06", "jardinero")

    cv = bg("paris_salon_indien_1895").copy()
    d = ImageDraw.Draw(cv)
    draw_place_only(cv, "PARÍS · 28 DE DICIEMBRE DE 1895", t, t0, border=GOLD)

    # Cinematógrafo proyectando en el sótano y espectadores sentados/de pie en el suelo
    draw_cinematograph_tripod(cv, 92, 248, t, beam=(t >= t_c2_06 - 0.2), crank=True, facing=1)
    char(cv, "louis_lumiere", 54, 248, t, scale=2, arms="work", look=1, mood="happy")
    char(cv, "spectator", 356, 248, t, scale=2, arms="down", look=-1, mood="happy")
    char(cv, "spectator_f", 406, 248, t, scale=2, arms="down", look=-1, mood="happy")

    if t < t_c2_05 - 0.12:
        a, dy = pop(t, t0 + 0.1)
        window(cv, 120, 46 + dy, 240, 92, fill=(28, 18, 26), border=GOLD, alpha=0.95)
        draw_text(cv, "SÓTANO DEL GRAND CAFÉ", 240, 56 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "SALON INDIEN · PARÍS", 240, 74 + dy, "silk", 8, CREAM, align="center")
        if t >= t_franco - 0.25:
            d.ellipse([226, 90 + dy, 254, 118 + dy], fill=(*GOLD, 255), outline=(*INK, 255))
            draw_text(cv, "1F", 240, 100 + dy, "press", 8, INK, align="center", outline=None, shadow=False)
            draw_text(cv, "ENTRADA: 1 FRANCO", 240, 122 + dy, "silk", 8, CHALK_YELLOW, align="center")
        return vignette(cv, 0.36)

    if t < t_c2_06 - 0.12:
        # c2_05: Había 100 sillas. Llegaron 33 personas. (Grilla visual de 100 butacas con 33 encendidas)
        a, dy = pop(t, t_c2_05 - 0.1)
        window(cv, 118, 42 + dy, 244, 122, fill=(22, 16, 28), border=GOLD, alpha=0.96)
        draw_text(cv, "HABÍA 100 SILLAS", 240, 50 + dy, "silk", 8, CREAM, align="center")
        lit_seats = 33 if t >= t_treinta - 0.2 else int(clamp01((t - t_c2_05) / 1.2) * 33)
        for s_i in range(100):
            r_i = s_i // 20
            c_i = s_i % 20
            sx = 142 + c_i * 10
            sy = 66 + dy + r_i * 11
            col_s = GOLD if s_i < lit_seats else (58, 48, 66)
            d.rectangle([sx, sy, sx + 6, sy + 7], fill=(*col_s, 255), outline=(*INK, 255))
        draw_text(cv, "LLEGARON 33 PERSONAS", 240, 132 + dy, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "67 SILLAS VACÍAS", 240, 148 + dy, "silk", 8, SOFT_GRAY, align="center")
        return vignette(cv, 0.36)

    # c2_06: Vieron diez películas cortitas (fábrica, bebé comiendo, broma al jardinero)
    cv = grade(cv, mul=(0.72, 0.70, 0.78))
    window(cv, 118, 40, 244, 130, fill=(236, 230, 212), border=GOLD, alpha=0.96)
    draw_text(cv, "PROGRAMA: 10 PELÍCULAS CORTITAS", 240, 48, "silk", 8, INK, align="center",
              outline=None, shadow=False)

    # Tres viñetas en blanco y negro/sepia que se iluminan al nombrarlas
    d.rectangle([130, 64, 350, 142], fill=(38, 34, 30, 255), outline=(*INK, 255), width=2)
    if t < t_bebe - 0.15:
        draw_text(cv, "1. SALIDA DE LA FÁBRICA", 240, 74, "press", 8, GOLD, align="center")
        # Portón de fábrica y siluetas de obreros saliendo
        d.rectangle([168, 92, 312, 134], fill=(198, 188, 168, 255), outline=(*INK, 255))
        for wx_o in (194, 224, 254, 284):
            ox_m = wx_o + int(math.sin(t * 5 + wx_o) * 4)
            d.rectangle([ox_m - 4, 108, ox_m + 4, 132], fill=(42, 38, 34, 255))
            d.ellipse([ox_m - 3, 100, ox_m + 3, 107], fill=(42, 38, 34, 255))
    elif t < t_jard - 0.2:
        draw_text(cv, "2. EL DESAYUNO DEL BEBÉ", 240, 74, "press", 8, GOLD, align="center")
        d.rectangle([168, 92, 312, 134], fill=(212, 202, 182, 255), outline=(*INK, 255))
        # Mesa con padres y bebé en el medio
        d.rectangle([196, 118, 284, 132], fill=(92, 68, 46, 255))
        d.ellipse([235, 104, 245, 114], fill=(48, 42, 36, 255))
        d.ellipse([208, 98, 220, 110], fill=(48, 42, 36, 255))
        d.ellipse([260, 98, 272, 110], fill=(48, 42, 36, 255))
    else:
        draw_text(cv, "3. EL REGADOR REGADO", 240, 74, "press", 8, GOLD, align="center")
        d.rectangle([168, 92, 312, 134], fill=(204, 194, 174, 255), outline=(*INK, 255))
        # Manguera y chorro de agua en la cara del jardinero (primera comedia)
        d.line([(186, 128), (232, 128), (242, 114)], fill=(42, 38, 34, 255), width=2)
        d.line([(242, 114), (268, 106)], fill=(90, 210, 255, 255), width=3)
        d.ellipse([266, 100, 278, 112], fill=(42, 38, 34, 255))

    draw_text(cv, "50 SEGUNDOS CADA UNA", 240, 150, "silk", 8, (92, 48, 28), align="center",
              outline=None, shadow=False)

    return vignette(cv, 0.36)


def c2_s03_train_myth_and_latam(t):
    """c2_07..c2_09: El mito del tren que llegaba a la estación -> llegada a América Latina -> 33 espectadores."""
    t_c2_07 = TL.s("c2_07")
    t_prim = TL.word("c2_07", "primera")
    t_c2_08 = TL.s("c2_08")
    t_c2_09 = TL.s("c2_09")

    cv = bg("paris_salon_indien_1895").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c2_08 - 0.12:
        draw_place_only(cv, "LA LEYENDA DEL TREN (1896)", t, t_c2_07, border=CHALK_RED)
        char(cv, "spectator", 136, 248, t, scale=2, arms="down", look=1, mood="neutral")
        char(cv, "spectator_f", 344, 248, t, scale=2, arms="down", look=-1, mood="neutral")

        window(cv, 118, 42, 244, 124, fill=(22, 18, 28), border=CHALK_RED, alpha=0.96)
        draw_text(cv, "EL MITO DEL TREN EN PANTALLA", 240, 50, "press", 8, GOLD, align="center")
        # Locomotora en perspectiva en la pantalla
        d.rectangle([142, 64, 338, 118], fill=(216, 208, 188, 255), outline=(*INK, 255))
        d.polygon([(156, 114), (228, 76), (252, 76), (318, 114)], fill=(78, 72, 64, 255))
        d.ellipse([224, 74, 256, 106], fill=(32, 28, 26, 255), outline=(*GOLD, 255))
        d.ellipse([234, 84, 246, 96], fill=(255, 236, 156, 255))

        if t >= t_prim - 0.3:
            d.rectangle([130, 122, 350, 158], fill=(56, 18, 24, 255), outline=(*CHALK_RED, 255))
            draw_text(cv, "NO ESTABA EN LA 1ª FUNCIÓN", 240, 128, "silk", 8, CHALK_YELLOW, align="center")
            draw_text(cv, "Y NO HAY REGISTRO DE PÁNICO", 240, 142, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.36)

    if t < t_c2_09 - 0.12:
        # c2_08: En pocos meses ya estaba en Buenos Aires, Montevideo y Ciudad de México
        draw_place_only(cv, "1896 · EL CINE CRUZA EL OCÉANO", t, t_c2_08, border=TESLA_CYAN)
        draw_cinematograph_tripod(cv, 240, 248, t, beam=True, crank=True, facing=1)
        char(cv, "auguste_lumiere", 138, 248, t, scale=2, arms="wave", look=1, mood="happy")
        char(cv, "spectator", 346, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

        a, dy = pop(t, t_c2_08 - 0.1)
        window(cv, 118, 44 + dy, 244, 112, fill=(16, 24, 42), border=TESLA_CYAN, alpha=0.96)
        draw_text(cv, "1896 · EN POCOS MESES:", 240, 54 + dy, "press", 8, GOLD, align="center")
        cities = [
            ("BUENOS AIRES", "JULIO DE 1896", CHALK_CYAN),
            ("MONTEVIDEO", "JULIO DE 1896", GOLD),
            ("CIUDAD DE MÉXICO", "AGOSTO DE 1896", CHALK_GREEN),
        ]
        for idx_c, (c_name, c_date, c_col) in enumerate(cities):
            cy_row = 74 + dy + idx_c * 24
            d.rectangle([130, cy_row, 350, cy_row + 19], fill=(24, 36, 58, 255), outline=(*c_col, 255))
            draw_text(cv, f"{c_name} ({c_date})", 240, cy_row + 5, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.35)

    # c2_09: Remate — "Treinta y tres espectadores. El público más chico de la historia del cine… y el primero."
    cv = grade(cv, mul=(0.55, 0.50, 0.62))
    draw_place_only(cv, "PARÍS · 28 DE DICIEMBRE DE 1895", t, t_c2_09, border=GOLD)
    draw_cinematograph_tripod(cv, 148, 248, t, beam=True, crank=True, facing=1)
    char(cv, "spectator", 296, 248, t, scale=2, arms="up", look=-1, mood="happy")
    char(cv, "spectator_f", 348, 248, t, scale=2, arms="up", look=-1, mood="happy")

    a, dy = pop(t, t_c2_09 - 0.1)
    window(cv, 118, 48 + dy, 244, 102, fill=(22, 16, 30), border=GOLD, alpha=0.96)
    draw_text(cv, "33 ESPECTADORES", 240, 60 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, "EL PÚBLICO MÁS CHICO", 240, 92 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "DE LA HISTORIA DEL CINE...", 240, 108 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "¡Y EL PRIMERO!", 240, 128 + dy, "press", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.38)


def scenes():
    return [
        (TL.s("c2_00") - 0.15, make_card(2, ["TREINTA Y TRES", "ESPECTADORES"], "1891 – 1895 · EE. UU. Y PARÍS"),
         None, "ch02"),
        (TL.s("c2_01") - 0.15, c2_s01_kinetoscope_and_cinematograph,
         lambda t: cam_push(t, TL.s("c2_01"), TL.s("c2_04"), 1.0, 1.03, (240, 135)), "ch02"),
        (TL.s("c2_04") - 0.15, c2_s02_salon_indien_1895,
         lambda t: cam_push(t, TL.s("c2_04"), TL.s("c2_07"), 1.0, 1.03, (240, 135)), "ch02"),
        (TL.s("c2_07") - 0.15, c2_s03_train_myth_and_latam,
         lambda t: cam_push(t, TL.s("c2_07"), TL.s("c3_00"), 1.0, 1.03, (240, 135)), "ch02"),
    ]


def music(A):
    A.add_pad(TL.s("c2_00"), TL.e("c2_09") - TL.s("c2_00"), (196.0, 246.94, 293.66), amp=0.015)


def sfx(A):
    A.fx_sparkle(TL.word("c2_01", "moneda"), 0.09)
    A.fx_pop(TL.s("c2_03"), 0.09)
    A.fx_pop(TL.s("c2_05"), 0.09)
    A.fx_chime(TL.s("c2_09"), 0.11)
