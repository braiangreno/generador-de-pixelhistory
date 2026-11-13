"""Capítulo 5: Las películas hablan (El cantante de jazz 1927, La Pizarra del sonido óptico y las 24 imágenes por segundo)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_vitaphone_table(cv, x, feet=248, t=0.0, spinning=True):
    """Mesa de proyección Vitaphone con bandeja giradiscos de vinilo sincronizada al proyector,
    apoyada firmemente sobre el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 38
        shadow_ellipse(canvas, cx, fy, 30, 4, 90)
        # Patas y tablero de la mesa hasta el suelo fy
        d.rectangle([cx - 22, top_y + 4, cx - 18, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx + 18, top_y + 4, cx + 22, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx - 26, top_y, cx + 26, top_y + 5], fill=(128, 82, 44, 255), outline=(*INK, 255))
        # Base del tocadiscos y disco de vinilo negro
        d.rectangle([cx - 18, top_y - 8, cx + 18, top_y], fill=(56, 48, 58, 255), outline=(*INK, 255))
        d.ellipse([cx - 14, top_y - 13, cx + 14, top_y - 5], fill=(22, 20, 28, 255), outline=(*GOLD, 255))
        d.ellipse([cx - 4, top_y - 10, cx + 4, top_y - 8], fill=(214, 52, 48, 255))
        # Brazo fonocaptor dorado
        ang = (t * 6.0) if spinning else 0.0
        gx = cx + int(round(math.cos(ang) * 9))
        d.point((gx, top_y - 9), fill=(255, 240, 180, 255))
        d.line([(cx + 14, top_y - 12), (cx + 4, top_y - 9)], fill=(214, 168, 72, 255), width=2)

    floor_prop(cv, _draw, x, feet)


def c5_s01_jazz_singer(t):
    """c5_01..c5_02: Octubre de 1927, estreno de El cantante de jazz -> fin del cine mudo."""
    t0 = TL.s("c5_01")
    t_cantaba = TL.word("c5_01", "cantaba")
    t_escuchaba = TL.word("c5_01", "escuchaba")
    t_c5_02 = TL.s("c5_02")
    t_termino = TL.word("c5_02", "terminó")

    cv = bg("jazz_singer_theater_1927").copy()
    d = ImageDraw.Draw(cv)
    draw_place_only(cv, "OCTUBRE DE 1927 · EL CANTANTE DE JAZZ", t, t0, border=GOLD)

    is_singing = t >= t_cantaba - 0.25
    char(cv, "jazz_singer", 240, 248, t, scale=2,
         arms="cheer" if is_singing else "down", look=1, mood="happy",
         talk=talk_v(t, is_singing))
    char(cv, "spectator", 124, 248, t, scale=2,
         arms="cheer" if t >= t_escuchaba - 0.2 else "down", look=1, mood="happy")
    char(cv, "spectator_f", 356, 248, t, scale=2,
         arms="cheer" if t >= t_escuchaba - 0.2 else "down", look=-1, mood="happy")

    if t < t_c5_02 - 0.12:
        a, dy = pop(t, t0 + 0.1)
        window(cv, 118, 42 + dy, 244, 96, fill=(20, 18, 34), border=GOLD, alpha=0.96)
        if not is_singing:
            # Cartel de cine mudo clásico con ornamentos
            d.rectangle([134, 52 + dy, 346, 118 + dy], fill=(18, 16, 24, 255), outline=(*CREAM, 255))
            draw_text(cv, "1927 · EL CANTANTE DE JAZZ", 240, 62 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "CASI TODA MUDA, CON CARTELES...", 240, 86 + dy, "silk", 8, CREAM, align="center")
        else:
            draw_text(cv, "¡EL PROTAGONISTA CANTABA", 240, 54 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "Y HABLABA EN PANTALLA!", 240, 72 + dy, "press", 8, TESLA_CYAN, align="center")
            draw_text(cv, "Y EL PÚBLICO LO ESCUCHABA", 240, 96 + dy, "silk", 8, CREAM, align="center")
            # Notas musicales y ondas sonoras saliendo de la pantalla
            for i in range(4):
                nx = 156 + i * 54
                ny = 118 + dy + int(round(math.sin(t * 7.0 + i) * 4))
                d.ellipse([nx - 3, ny - 2, nx + 3, ny + 2], fill=(*GOLD, 255))
                d.line([(nx + 3, ny), (nx + 3, ny - 8)], fill=(*GOLD, 255), width=2)
        return vignette(cv, 0.34)

    # c5_02: Primera película larga con diálogos sincronizados -> fin del cine mudo
    a, dy = pop(t, t_c5_02 - 0.1)
    window(cv, 116, 42 + dy, 248, 96, fill=(22, 18, 36), border=TESLA_CYAN, alpha=0.96)
    draw_text(cv, "PRIMER LARGOMETRAJE SONORO", 240, 52 + dy, "press", 8, TESLA_CYAN, align="center")
    draw_text(cv, "CON DIÁLOGOS SINCRONIZADOS", 240, 72 + dy, "silk", 8, CREAM, align="center")
    if t >= t_termino - 0.45:
        d.rectangle([130, 90 + dy, 350, 122 + dy], fill=(38, 20, 28, 255), outline=(*GOLD, 255))
        draw_text(cv, "EN POCOS AÑOS: FIN DEL CINE MUDO", 240, 102 + dy, "press", 8, GOLD, align="center")

    return vignette(cv, 0.34)


def c5_s02_pizarra_sound_and_24fps(t):
    """c5_03..c5_06: LA PIZARRA 2 — Disco aparte (vinilo) -> Franja óptica en el celuloide -> Luz + celda -> 24 cuadros/seg."""
    t0 = TL.s("c5_03")
    t_c5_04 = TL.s("c5_04")
    t_c5_05 = TL.s("c5_05")
    t_c5_06 = TL.s("c5_06")
    t_24 = TL.word("c5_06", "veinticuatro")

    cv = draw_pizarra_frame(
        t, t0,
        "SONIDO Y 24 POR SEGUNDO",
        summary_es="24 FOTOS/SEG = VOZ SIN DESAFINAR",
        t_summary=t_c5_06 + 0.35,
    )
    d = ImageDraw.Draw(cv)

    if t < t_c5_04 - 0.12:
        # Paso 1 (c5_03): El sonido en un disco aparte (como un vinilo) girando con el proyector
        window(cv, 118, 42, 244, 152, fill=(14, 38, 26), border=CHALK_YELLOW, alpha=0.95)
        draw_text(cv, "1. AL PRINCIPIO: DISCO APARTE", 240, 50, "press", 8, CHALK_YELLOW, align="center")
        # Disco de vinilo girando a la izquierda + rollo de proyector a la derecha unidos por correa
        ang = t * 5.0
        for cx_d, lbl_d, col_d in ((184, "VINILO", CHALK_CYAN), (296, "PROYECTOR", CHALK_YELLOW)):
            d.ellipse([cx_d - 28, 82, cx_d + 28, 138], fill=(18, 28, 22, 255), outline=(*col_d, 255), width=2)
            d.ellipse([cx_d - 8, 102, cx_d + 8, 118], fill=(*col_d, 255))
            rx = cx_d + int(round(math.cos(ang) * 20))
            ry = 110 + int(round(math.sin(ang) * 20))
            d.line([(cx_d, 110), (rx, ry)], fill=(*CHALK_WHITE, 255), width=2)
            draw_text(cv, lbl_d, cx_d, 146, "silk", 8, col_d, align="center")
        # Eje de sincronización
        d.line([(212, 110), (268, 110)], fill=(*CHALK_GREEN, 255), width=2)
        draw_text(cv, "GIRABAN AL MISMO TIEMPO", 240, 168, "silk", 8, CHALK_WHITE, align="center")
        draw_chalk_hand(cv, 268, 110, t)
        return vignette(cv, 0.26)

    if t < t_c5_06 - 0.12:
        # Paso 2 (c5_04 y c5_05): Sonido óptico en la misma película (sombra variable + luz + celda)
        window(cv, 118, 40, 244, 156, fill=(14, 38, 26), border=CHALK_CYAN, alpha=0.95)
        draw_text(cv, "2. SONIDO EN LA MISMA PELÍCULA", 240, 48, "press", 8, CHALK_CYAN, align="center")
        # Cinta de 35 mm con pista óptica resaltada
        draw_filmstrip(cv, 130, 66, 220, 44, t, speed=42.0, sepia=True, optical_track=True, alpha=0.95)
        # Zoom a la franja de sombra variable
        d.rectangle([134, 118, 346, 150], fill=(12, 28, 20, 255), outline=(*CHALK_YELLOW, 255))
        pts_w = []
        for wx in range(140, 340, 3):
            wy = 134 + int(round(math.sin(wx * 0.18 + t * 12.0) * 9 * math.sin(wx * 0.05 + t * 3.0)))
            pts_w.append((wx, wy))
        if len(pts_w) >= 2:
            d.line(pts_w, fill=(*CHALK_CYAN, 255), width=2)

        if t < t_c5_05 - 0.1:
            draw_text(cv, "EL SONIDO ES UNA SOMBRA", 240, 158, "silk", 8, CHALK_YELLOW, align="center")
            draw_text(cv, "QUE CAMBIA DE FORMA AL COSTADO", 240, 174, "silk", 8, CHALK_WHITE, align="center")
        else:
            # Haz de luz + celda fotoeléctrica leyendo la franja
            glow(cv, 240, 134, 18, CHALK_YELLOW, 0.65)
            d.rectangle([126, 126, 134, 142], fill=(*CHALK_YELLOW, 255), outline=(*INK, 255))
            d.rectangle([346, 126, 354, 142], fill=(*CHALK_GREEN, 255), outline=(*INK, 255))
            draw_text(cv, "LUZ -> CELDA LA LEE -> ¡SONIDO!", 240, 162, "press", 8, CHALK_GREEN, align="center")
        return vignette(cv, 0.26)

    # Paso 3 (c5_06): Velocidad constante de 24 imágenes por segundo
    window(cv, 118, 40, 244, 156, fill=(14, 38, 26), border=CHALK_GREEN, alpha=0.95)
    draw_text(cv, "3. SIEMPRE A LA MISMA VELOCIDAD", 240, 48, "press", 8, CHALK_GREEN, align="center")
    draw_filmstrip(cv, 130, 66, 220, 38, t, speed=48.0, sepia=False, optical_track=True, alpha=0.95)
    if t >= t_24 - 0.35:
        draw_text(cv, "24", 240, 112, "press", 24, CHALK_YELLOW, align="center")
        draw_text(cv, "IMÁGENES POR SEGUNDO", 240, 142, "press", 8, CHALK_WHITE, align="center")
        draw_text(cv, "TODAVÍA LAS USAMOS HOY", 240, 160, "silk", 8, CHALK_CYAN, align="center")
    else:
        draw_text(cv, "SI VARÍA LA VELOCIDAD, SUENA RARO", 240, 126, "silk", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.26)


def c5_s03_24fps_punchline(t):
    """c5_07: Remate — 'Las veinticuatro imágenes por segundo se eligieron para que la voz no desafinara.'"""
    t0 = TL.s("c5_07")
    t_voz = TL.word("c5_07", "voz")

    cv = bg("jazz_singer_theater_1927").copy()
    draw_place_only(cv, "EL ESTÁNDAR DEL CINE · 24 FPS", t, t0, border=GOLD)

    draw_vitaphone_table(cv, 152, 248, t, spinning=True)
    char(cv, "jazz_singer", 240, 248, t, scale=2, arms="cheer", look=1, mood="happy",
         talk=talk_v(t, t >= t_voz - 0.2))
    draw_cinematograph_tripod(cv, 328, 248, t, beam=True, crank=True, facing=-1)

    a, dy = pop(t, t0 - 0.08)
    window(cv, 116, 44 + dy, 248, 102, fill=(20, 18, 36), border=GOLD, alpha=0.96)
    draw_text(cv, "24 IMÁGENES POR SEGUNDO", 240, 56 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "SE ELIGIERON PARA QUE", 240, 80 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "LA VOZ NO DESAFINARA.", 240, 102 + dy, "press", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.34)


def scenes():
    return [
        (TL.s("c5_00") - 0.15, make_card(5, ["LAS PELÍCULAS", "HABLAN"], "1927 · EL SONIDO Y LOS 24 CUADROS"),
         None, "ch05"),
        (TL.s("c5_01") - 0.15, c5_s01_jazz_singer,
         lambda t: cam_push(t, TL.s("c5_01"), TL.s("c5_03"), 1.0, 1.03, (240, 135)), "ch05"),
        (TL.s("c5_03") - 0.15, c5_s02_pizarra_sound_and_24fps,
         None, "ch05"),
        (TL.s("c5_07") - 0.15, c5_s03_24fps_punchline,
         lambda t: cam_push(t, TL.s("c5_07"), TL.s("c6_00"), 1.0, 1.03, (240, 135)), "ch05"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_sparkle(TL.word("c5_01", "cantaba"), 0.10)
    A.fx_pop(TL.s("c5_03"), 0.08)
    A.fx_chime(TL.word("c5_06", "veinticuatro"), 0.11)
    A.fx_chime(TL.s("c5_07"), 0.11)
