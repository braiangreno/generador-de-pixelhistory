"""Capítulo 4: Hollywood (el Trust de Edison, la mudanza a California por el sol, el mito de los abogados y el piano en vivo)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_upright_piano(cv, x, feet=248, t=0.0, playing=True):
    """Piano vertical de sala de cine mudo apoyado firmemente sobre el suelo (feet=248),
    con notas musicales flotando cuando suena en vivo."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 48
        shadow_ellipse(canvas, cx, fy, 34, 4, 90)
        # Caja de caoba oscura del piano vertical hasta el suelo fy
        d.rectangle([cx - 24, top_y, cx + 24, fy], fill=(76, 42, 24, 255), outline=(*INK, 255))
        d.rectangle([cx - 20, top_y + 4, cx + 20, top_y + 18], fill=(56, 30, 18, 255), outline=(168, 118, 62, 255))
        # Atril con partitura blanca
        d.rectangle([cx - 8, top_y + 6, cx + 8, top_y + 16], fill=(242, 236, 218, 255), outline=(*INK, 255))
        # Teclado de marfil sobresaliendo a mitad de altura
        kb_y = top_y + 22
        d.rectangle([cx - 26, kb_y, cx + 26, kb_y + 7], fill=(246, 242, 230, 255), outline=(*INK, 255))
        for kx in range(cx - 22, cx + 22, 4):
            d.line([(kx, kb_y), (kx, kb_y + 6)], fill=(*INK, 255))
            if (kx // 4) % 3 != 0:
                d.rectangle([kx - 1, kb_y, kx + 1, kb_y + 4], fill=(20, 18, 26, 255))
        # Pedales dorados abajo en fy
        d.rectangle([cx - 4, fy - 4, cx + 4, fy - 1], fill=(214, 168, 72, 255), outline=(*INK, 255))
        if playing:
            for i in range(3):
                ny = top_y - 6 - int(((t * 18 + i * 9) % 18))
                nx = cx - 12 + i * 12 + int(round(math.sin(t * 5 + i) * 3))
                col_n = GOLD if i % 2 == 0 else TESLA_CYAN
                d.ellipse([nx - 2, ny - 2, nx + 2, ny + 1], fill=(*col_n, 255))
                d.line([(nx + 2, ny), (nx + 2, ny - 6)], fill=(*col_n, 255))

    floor_prop(cv, _draw, x, feet)


def c4_s01_trust_and_west(t):
    """c4_01..c4_02: El Trust de Edison en el Este -> mudanza al oeste, a un pueblito llamado Hollywood."""
    t0 = TL.s("c4_01")
    t_trust = TL.word("c4_01", "trust")
    t_c4_02 = TL.s("c4_02")
    t_holly = TL.word("c4_02", "Hollywood")

    cv = bg("hollywood_hills_1915").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c4_02 - 0.12:
        # c4_01: Edison y el Trust controlando cámaras, películas y salas
        cv = grade(cv, mul=(0.78, 0.80, 0.90))
        draw_place_only(cv, "ESTADOS UNIDOS · 1908 · EL TRUST", t, t0, border=CHALK_RED)
        char(cv, "edison", 148, 248, t, scale=2, arms="cross", look=1, mood="angry",
             talk=talk_v(t, t0 <= t < t_c4_02 - 0.3))
        char(cv, "investor_a", 332, 248, t, scale=2, arms="hips", look=-1, mood="neutral")
        draw_wooden_camera(cv, 240, 248, t, scale=1, flash=False, facing=1, label="PATENTE CONTROLADA")

        a, dy = pop(t, t0 + 0.1)
        window(cv, 118, 42 + dy, 244, 92, fill=(28, 18, 28), border=CHALK_RED, alpha=0.95)
        draw_text(cv, "EL MONOPOLIO DEL ESTE", 240, 52 + dy, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "EDISON Y OTRAS EMPRESAS", 240, 72 + dy, "silk", 8, CREAM, align="center")
        if t >= t_trust - 0.3:
            draw_text(cv, "CONTROLARON CÁMARAS, PELÍCULAS", 240, 90 + dy, "silk", 8, GOLD, align="center")
            draw_text(cv, "Y SALAS DE CINE", 240, 108 + dy, "press", 8, TESLA_CYAN, align="center")
        return vignette(cv, 0.38)

    # c4_02: Muchos productores se mudaron al oeste, a un pueblito de California llamado Hollywood
    draw_place_only(cv, "CALIFORNIA · UN PUEBLITO LLAMADO HOLLYWOOD", t, t_c4_02, border=GOLD)
    dx_dir, wph = walk(t, t_c4_02, t_c4_02 + 2.4, 108, 174)
    char(cv, "director_hollywood", dx_dir, 248, t, scale=2, walk_phase=wph,
         arms="point" if wph is None else "down", look=1, mood="happy")
    draw_wooden_camera(cv, 256, 248, t, scale=2, flash=(t >= t_holly - 0.2), facing=1)

    a, dy = pop(t, t_c4_02 - 0.1)
    window(cv, 118, 42 + dy, 244, 86, fill=(22, 20, 36), border=GOLD, alpha=0.95)
    draw_text(cv, "RUMBO AL OESTE", 240, 52 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "MUCHOS PRODUCTORES SE MUDARON", 240, 72 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "A HOLLYWOOD, CALIFORNIA", 240, 92 + dy, "press", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.32)


def c4_s02_sun_landscapes_and_myth(t):
    """c4_03..c4_04: ¿Por qué ahí? El sol + mar, montañas y desierto -> el mito de los abogados y México."""
    t_c4_03 = TL.s("c4_03")
    t_mar = TL.word("c4_03", "mar")
    t_c4_04 = TL.s("c4_04")
    t_mito = TL.word("c4_04", "mito")

    cv = bg("hollywood_hills_1915").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c4_04 - 0.12:
        draw_place_only(cv, "CALIFORNIA · SOL Y PAISAJES TODO EL AÑO", t, t_c4_03, border=GOLD)
        draw_sun(cv, 412, 54, 18, t, face=False)
        char(cv, "director_hollywood", 148, 248, t, scale=2, arms="cheer", look=1, mood="happy")
        draw_wooden_camera(cv, 224, 248, t, scale=1, flash=True, facing=1)

        a, dy = pop(t, t_c4_03 - 0.1)
        window(cv, 118, 42 + dy, 244, 114, fill=(20, 22, 38), border=GOLD, alpha=0.95)
        draw_text(cv, "¿POR QUÉ HOLLYWOOD?", 240, 50 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "1. SOL CASI TODO EL AÑO", 240, 68 + dy, "silk", 8, CHALK_YELLOW, align="center")
        if t >= t_mar - 0.35:
            # Tres tarjetitas de paisaje: MAR, MONTAÑAS, DESIERTO
            badges = [
                ("MAR", (54, 148, 224), 132),
                ("MONTAÑA", (118, 178, 98), 206),
                ("DESIERTO", (232, 178, 84), 282),
            ]
            for b_txt, b_col, bx0 in badges:
                d.rectangle([bx0, 88 + dy, bx0 + 66, 114 + dy], fill=(24, 28, 44, 255), outline=(*b_col, 255))
                draw_text(cv, b_txt, bx0 + 33, 97 + dy, "silk", 8, b_col, align="center")
            draw_text(cv, "TODO A POCA DISTANCIA", 240, 128 + dy, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.32)

    # c4_04: Mito vs realidad de huir de los abogados de Edison a México
    draw_place_only(cv, "MITO VS. HISTORIA · CALIFORNIA", t, t_c4_04, border=TESLA_CYAN)
    char(cv, "director_hollywood", 142, 248, t, scale=2, arms="hips", look=1, mood="happy")
    char(cv, "edison", 338, 248, t, scale=2, arms="work", look=-1, mood="neutral")
    draw_wooden_camera(cv, 282, 248, t, scale=1, flash=True, facing=-1, label="TRUST EN CA")

    a, dy = pop(t, t_c4_04 - 0.1)
    window(cv, 116, 42 + dy, 248, 112, fill=(20, 22, 38), border=TESLA_CYAN, alpha=0.96)
    d.rectangle([126, 52 + dy, 354, 82 + dy], fill=(38, 22, 32, 255), outline=(*CHALK_RED, 255))
    draw_text(cv, "LEYENDA: HUÍAN A MÉXICO", 240, 58 + dy, "silk", 8, CHALK_RED, align="center")
    draw_text(cv, "DE LOS ABOGADOS DE EDISON", 240, 70 + dy, "silk", 8, CREAM, align="center")
    if t >= t_mito - 0.35:
        d.rectangle([126, 88 + dy, 354, 120 + dy], fill=(18, 38, 34, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "HISTORIADORES: MÁS MITO QUE REALIDAD", 240, 94 + dy, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "HASTA EL TRUST FILMABA EN CALIFORNIA", 240, 106 + dy, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.34)


def c4_s03_live_piano_and_punchline(t):
    """c4_05..c4_06: Películas mudas pero nunca silenciosas (pianista en vivo) -> 'Nació por la luz'."""
    t_c4_05 = TL.s("c4_05")
    t_c4_06 = TL.s("c4_06")
    t_luz = TL.word("c4_06", "luz")

    if t < t_c4_06 - 0.12:
        cv = bg("jazz_singer_theater_1927").copy()
        draw_place_only(cv, "SALAS DE CINE MUDO · MÚSICA EN VIVO", t, t_c4_05, border=GOLD)
        draw_upright_piano(cv, 152, 248, t, playing=True)
        char(cv, "pianist", 196, 248, t, scale=2, arms="work", look=-1, mood="happy")
        char(cv, "spectator", 296, 248, t, scale=2, arms="down", look=-1, mood="happy")
        char(cv, "spectator_f", 348, 248, t, scale=2, arms="down", look=-1, mood="happy")

        a, dy = pop(t, t_c4_05 - 0.1)
        window(cv, 118, 42 + dy, 244, 88, fill=(22, 18, 36), border=GOLD, alpha=0.95)
        draw_text(cv, "CINE MUDO ≠ CINE SILENCIOSO", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "EN LAS SALAS HABÍA UN PIANISTA", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "O UNA ORQUESTA TOCANDO EN VIVO", 240, 94 + dy, "silk", 8, TESLA_CYAN, align="center")
        return vignette(cv, 0.35)

    # c4_06: Remate — "Hollywood no nació por los abogados. Nació por la luz."
    cv = bg("hollywood_hills_1915").copy()
    draw_sun(cv, 240, 52, 22, t, face=False)
    glow(cv, 240, 52, 46, GOLD, 0.55)
    draw_place_only(cv, "EL ORIGEN DE HOLLYWOOD", t, t_c4_06, border=GOLD)

    char(cv, "director_hollywood", 168, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    draw_wooden_camera(cv, 304, 248, t, scale=2, flash=(t >= t_luz - 0.2), facing=-1)

    a, dy = pop(t, t_c4_06 - 0.1)
    window(cv, 116, 62 + dy, 248, 92, fill=(20, 18, 34), border=GOLD, alpha=0.96)
    draw_text(cv, "HOLLYWOOD NO NACIÓ", 240, 74 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "POR LOS ABOGADOS.", 240, 92 + dy, "press", 8, CHALK_RED, align="center")
    if t >= t_luz - 0.35:
        draw_text(cv, "NACIÓ POR LA LUZ.", 240, 118 + dy, "press", 16, GOLD, align="center")

    return vignette(cv, 0.32)


def scenes():
    return [
        (TL.s("c4_00") - 0.15, make_card(4, ["HOLLYWOOD"], "1908 – 1920 · CALIFORNIA"),
         None, "ch04"),
        (TL.s("c4_01") - 0.15, c4_s01_trust_and_west,
         lambda t: cam_push(t, TL.s("c4_01"), TL.s("c4_03"), 1.0, 1.03, (240, 135)), "ch04"),
        (TL.s("c4_03") - 0.15, c4_s02_sun_landscapes_and_myth,
         lambda t: cam_push(t, TL.s("c4_03"), TL.s("c4_05"), 1.0, 1.03, (240, 135)), "ch04"),
        (TL.s("c4_05") - 0.15, c4_s03_live_piano_and_punchline,
         lambda t: cam_push(t, TL.s("c4_05"), TL.s("c5_00"), 1.0, 1.03, (240, 135)), "ch04"),
    ]


def music(A):
    A.add_pad(TL.s("c4_00"), TL.e("c4_06") - TL.s("c4_00"), (164.81, 207.65, 246.94), amp=0.015)


def sfx(A):
    A.fx_pop(TL.s("c4_01"), 0.08)
    A.fx_sparkle(TL.word("c4_02", "Hollywood"), 0.10)
    A.fx_chime(TL.word("c4_03", "sol"), 0.10)
    A.fx_chime(TL.word("c4_06", "luz"), 0.12)
