"""Capítulo 7: Veinticuatro por segundo (CGI de los 90, cine digital, el regreso al caballo en el aire y llamado a comentar)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa
from i18n import tr as i18n_tr


def draw_cgi_workstation(cv, x, feet=248, t=0.0):
    """Estación de trabajo de animación 3D de los años 90 (Silicon Graphics / Pixar) sobre escritorio
    con patas firmes hasta el suelo (feet=248), envuelta en floor_prop."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 36
        shadow_ellipse(canvas, cx, fy, 34, 4, 90)
        # Patas y tapa del escritorio hasta el suelo fy
        d.rectangle([cx - 26, top_y + 4, cx - 22, fy], fill=(64, 68, 82, 255), outline=(*INK, 255))
        d.rectangle([cx + 22, top_y + 4, cx + 26, fy], fill=(64, 68, 82, 255), outline=(*INK, 255))
        d.rectangle([cx - 30, top_y, cx + 30, top_y + 5], fill=(118, 82, 48, 255), outline=(*INK, 255))
        # Monitor CRT grande en el escritorio
        d.rectangle([cx - 18, top_y - 24, cx + 10, top_y], fill=(212, 206, 192, 255), outline=(*INK, 255))
        d.rectangle([cx - 15, top_y - 21, cx + 7, top_y - 4], fill=(16, 32, 48, 255))
        # Malla 3D (wireframe) girando en la pantalla del monitor
        ox = int(round(math.cos(t * 4.0) * 4))
        d.polygon([(cx - 4 + ox, top_y - 19), (cx - 11, top_y - 7), (cx + 3, top_y - 7)],
                  outline=(*TESLA_CYAN, 255))
        # Gabinete torre SGI índigo al costado sobre el escritorio
        d.rectangle([cx + 13, top_y - 20, cx + 24, top_y], fill=(58, 72, 142, 255), outline=(*INK, 255))
        d.point((cx + 18, top_y - 16), fill=(108, 248, 154, 255))

    floor_prop(cv, _draw, x, feet)


def draw_digital_projector_pedestal(cv, x, feet=248, t=0.0, beam=True):
    """Proyector de cine digital moderno sobre pedestal metálico apoyado en el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 28, 4, 90)
        # Columna y base del pedestal hasta fy
        d.rectangle([cx - 18, fy - 5, cx + 18, fy], fill=(52, 58, 72, 255), outline=(*INK, 255))
        d.rectangle([cx - 8, top_y + 14, cx + 8, fy - 5], fill=(74, 82, 98, 255), outline=(*INK, 255))
        # Cuerpo del proyector digital láser/DLP
        d.rectangle([cx - 16, top_y, cx + 16, top_y + 15], fill=(38, 42, 54, 255), outline=(*TESLA_CYAN, 255))
        d.rectangle([cx + 16, top_y + 4, cx + 21, top_y + 11], fill=(108, 236, 255, 255), outline=(*INK, 255))
        if beam:
            pts_b = [(cx + 21, top_y + 5), (cx + 78, top_y - 16), (cx + 78, top_y + 24), (cx + 21, top_y + 10)]
            ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).polygon(pts_b, fill=(138, 234, 245, 76))
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), ov), (0, 0))

    floor_prop(cv, _draw, x, feet)


def c7_s01_cgi_and_digital(t):
    """c7_01..c7_03: 1993 Jurassic Park y 1995 Toy Story -> cámaras y proyectores digitales -> casi 3.000 millones."""
    t0 = TL.s("c7_01")
    t_toy = TL.word("c7_01", "Story")
    t_c7_02 = TL.s("c7_02")
    t_c7_03 = TL.s("c7_03")
    t_millones = TL.word("c7_03", "millones")

    cv = bg("modern_cinema_1995").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c7_02 - 0.12:
        draw_place_only(cv, "AÑOS 1990 · LA ERA DE LA COMPUTADORA", t, t0, border=TESLA_CYAN)
        char(cv, "animator_90s", 148, 248, t, scale=2, arms="work", look=1, mood="happy")
        draw_cgi_workstation(cv, 224, 248, t)
        char(cv, "spectator", 332, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

        a, dy = pop(t, t0 + 0.1)
        window(cv, 116, 40 + dy, 248, 114, fill=(16, 22, 40), border=TESLA_CYAN, alpha=0.96)
        draw_text(cv, "COMPUTADORAS EN LA PANTALLA", 240, 48 + dy, "press", 8, TESLA_CYAN, align="center")
        # 1993: Jurassic Park (dinosaurios)
        d.rectangle([126, 66 + dy, 354, 92 + dy], fill=(22, 42, 34, 255), outline=(*CHALK_GREEN, 255))
        draw_text(cv, "1993 · JURASSIC PARK (DINOSAURIOS)", 240, 75 + dy, "silk", 8, CHALK_GREEN, align="center")
        if t >= t_toy - 0.5:
            d.rectangle([126, 98 + dy, 354, 126 + dy], fill=(38, 28, 52, 255), outline=(*GOLD, 255))
            draw_text(cv, "1995 · TOY STORY", 240, 103 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "100% HECHA POR COMPUTADORA", 240, 115 + dy, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.32)

    if t < t_c7_03 - 0.12:
        # c7_02: Cámaras y proyectores digitales; el rollo de película casi desapareció
        draw_place_only(cv, "SIGLO XXI · DEL CELULOIDE AL DIGITAL", t, t_c7_02, border=GOLD)
        draw_digital_projector_pedestal(cv, 176, 248, t, beam=True)
        char(cv, "animator_90s", 312, 248, t, scale=2, arms="point", look=-1, mood="happy")

        a, dy = pop(t, t_c7_02 - 0.1)
        window(cv, 118, 42 + dy, 244, 96, fill=(18, 22, 38), border=GOLD, alpha=0.96)
        draw_text(cv, "CÁMARAS Y PROYECTORES DIGITALES", 240, 52 + dy, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "DE LOS ROLLOS DE CELULOIDE", 240, 74 + dy, "silk", 8, SOFT_GRAY, align="center")
        draw_text(cv, "A LOS ARCHIVOS Y PÍXELES", 240, 92 + dy, "silk", 8, GOLD, align="center")
        draw_text(cv, "EL ROLLO CASI DESAPARECIÓ", 240, 112 + dy, "press", 8, CREAM, align="center")
        return vignette(cv, 0.32)

    # c7_03: Las películas más vistas recaudaron casi 3.000 millones de dólares
    draw_place_only(cv, "TAQUILLA MUNDIAL · RÉCORDS HISTÓRICOS", t, t_c7_03, border=GOLD)
    for idx_s, (key_s, sx_s) in enumerate((("spectator", 128), ("spectator_f", 184), ("spectator", 296), ("spectator_f", 352))):
        char(cv, key_s, sx_s, 248, t, scale=2, arms="cheer", look=1 if sx_s < 240 else -1, mood="happy")

    a, dy = pop(t, t_c7_03 - 0.1)
    window(cv, 116, 42 + dy, 248, 104, fill=(18, 20, 38), border=GOLD, alpha=0.96)
    draw_text(cv, "LAS PELÍCULAS MÁS VISTAS", 240, 52 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "LLEGARON A RECAUDAR CASI:", 240, 72 + dy, "silk", 8, CREAM, align="center")
    if t >= t_millones - 0.55:
        draw_text(cv, "US$ 3.000 MILLONES", 240, 94 + dy, "press", 16, CHALK_GREEN, align="center")

    return vignette(cv, 0.32)


def c7_s02_24fps_everywhere(t):
    """c7_04..c7_05: Cine, tele o teléfono = 24 imágenes quietas por segundo -> tu cerebro hace el resto y sala a oscuras."""
    t_c7_04 = TL.s("c7_04")
    t_24 = TL.word("c7_04", "veinticuatro")
    t_c7_05 = TL.s("c7_05")
    t_oscuras = TL.word("c7_05", "oscuras")

    if t < t_c7_05 - 0.12:
        cv = bg("modern_cinema_1995").copy()
        d = ImageDraw.Draw(cv)
        draw_place_only(cv, "CINE, TELE O TELÉFONO · EL MISMO SECRETO", t, t_c7_04, border=TESLA_CYAN)
        char(cv, "spectator", 156, 248, t, scale=2, arms="down", look=1, mood="happy")
        char(cv, "spectator_f", 324, 248, t, scale=2, arms="read", look=-1, mood="happy")

        a, dy = pop(t, t_c7_04 - 0.1)
        window(cv, 116, 40 + dy, 248, 116, fill=(16, 20, 38), border=TESLA_CYAN, alpha=0.96)
        # Tres íconos de pantalla: CINE, TELE, TELÉFONO
        screens = [
            (132, 72, "CINE", GOLD),
            (214, 52, "TELE", TESLA_CYAN),
            (282, 58, "MÓVIL", CHALK_GREEN),
        ]
        for sx0, sw0, s_lbl, s_col in screens:
            d.rectangle([sx0, 50 + dy, sx0 + sw0, 82 + dy], fill=(22, 28, 48, 255), outline=(*s_col, 255))
            draw_text(cv, s_lbl, sx0 + sw0 // 2, 62 + dy, "silk", 8, s_col, align="center")
        draw_text(cv, "ADENTRO PASA LO MISMO:", 240, 92 + dy, "silk", 8, CREAM, align="center")
        if t >= t_24 - 0.45:
            draw_text(cv, "24 IMÁGENES QUIETAS / SEG", 240, 112 + dy, "press", 8, GOLD, align="center")
        return vignette(cv, 0.32)

    # c7_05: Tu cerebro hace el resto, igual que con aquel caballo. Y en una sala a oscuras, desconocidos siguen mirando juntos la misma luz.
    cv = bg("paris_salon_indien_1895").copy()
    draw_place_only(cv, "DESDE 1895 HASTA HOY · LA MISMA LUZ", t, t_c7_05, border=GOLD)
    draw_cinematograph_tripod(cv, 118, 248, t, beam=True, crank=True, facing=1)
    for idx_v, (key_v, vx_v) in enumerate((("spectator", 196), ("spectator_f", 248), ("melies", 302), ("animator_90s", 356))):
        char(cv, key_v, vx_v, 248, t, scale=2, arms="down", look=1, mood="happy")

    a, dy = pop(t, t_c7_05 - 0.1)
    window(cv, 116, 40 + dy, 248, 112, fill=(18, 16, 32), border=GOLD, alpha=0.96)
    draw_text(cv, "TU CEREBRO HACE EL RESTO,", 240, 50 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "IGUAL QUE CON AQUEL CABALLO", 240, 66 + dy, "press", 8, GOLD, align="center")
    draw_galloping_horse(cv, 240, 94 + dy, t * 1.1, scale=1, rider=True)
    if t >= t_oscuras - 0.35:
        draw_text(cv, "MIRANDO JUNTOS LA MISMA LUZ", 240, 126 + dy, "press", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.35)


def c7_s03_horse_flies_finale(t):
    """c7_06: Match cut final — 'El cine sigue siendo un caballo que, por un instante, vuela.'"""
    t0 = TL.s("c7_06")
    t_vuela = TL.word("c7_06", "vuela")

    cv = bg("palo_alto_track_1878").copy()
    d = ImageDraw.Draw(cv)
    draw_place_only(cv, "UN CABALLO EN EL AIRE · 1878 – HOY", t, t0, border=GOLD)

    # Muybridge y los pioneros mirando el fotograma eterno
    char(cv, "muybridge", 122, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    draw_wooden_camera(cv, 178, 248, t, scale=1, flash=True, facing=1)
    char(cv, "melies", 358, 248, t, scale=2, arms="wave", look=-1, mood="happy")

    # Placa dorada central con Sallie Gardner suspendida en el aire (cuadro 3: las 4 patas recogidas)
    a, dy = pop(t, t0 - 0.08)
    window(cv, 116, 40 + dy, 248, 122, fill=(18, 16, 30), border=GOLD, alpha=0.96)
    d.rectangle([132, 50 + dy, 348, 108 + dy], fill=(236, 224, 192, 255), outline=(*GOLD, 255), width=2)
    # Si todavía no dijo "vuela", galopa a 12 fps; en "vuela", queda suspendida en el aire con destello dorado
    freeze_air = t >= t_vuela - 0.25
    if freeze_air:
        glow(cv, 240, 80 + dy, 34, GOLD, 0.65)
        draw_galloping_horse(cv, 240, 82 + dy, frame=2, scale=2, rider=True, highlight_air=True)
    else:
        draw_galloping_horse(cv, 240, 82 + dy, phase=t * 1.1, scale=2, rider=True)

    draw_text(cv, "EL CINE SIGUE SIENDO UN CABALLO", 240, 116 + dy, "press", 8, CREAM, align="center")
    draw_text(cv, "QUE, POR UN INSTANTE, VUELA.", 240, 134 + dy, "press", 8, GOLD, align="center")

    return vignette(cv, 0.32)


def c7_s04_comment_cta(t):
    """c7_07: Llamado a la acción final antes del cierre de Pixeloide Studios: invita a comentar el próximo episodio."""
    t0 = TL.s("c7_07") - 0.20
    t_vo = TL.s("c7_07")
    t_end_vo = TL.e("c7_07")

    cv = bg("paris_salon_indien_1895").copy()
    d = ImageDraw.Draw(cv)

    # Ventana RPG principal (x=118..362, w=244 -> cabe 1:1 en 16:9 y en 9:16 sin escalar)
    a, dy = pop(t, t0, dur=0.32)
    window(cv, 118, 28 + dy, 244, 122, fill=(14, 20, 38), border=GOLD, alpha=0.96)

    # Etiqueta superior dorada
    d.rectangle([144, 35 + dy, 336, 49 + dy], fill=(32, 44, 72, 255), outline=(*TESLA_CYAN, 255))
    draw_text(cv, "PRÓXIMO EPISODIO · TU IDEA", 240, 38 + dy, "silk", 8, GOLD, align="center")

    # Pregunta principal
    draw_text(cv, "¿QUÉ HISTORIA TE GUSTARÍA VER", 240, 56 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "EN EL PRÓXIMO EPISODIO?", 240, 70 + dy, "press", 8, TESLA_CYAN, align="center")

    # Caja interactiva de comentario con efecto de escritura y cursor titilante
    d.rectangle([126, 86 + dy, 354, 108 + dy], fill=(8, 12, 24, 255), outline=(*GOLD, 255))
    d.rectangle([132, 91 + dy, 144, 100 + dy], fill=(*TESLA_CYAN, 255))
    d.polygon([(135, 100 + dy), (139, 100 + dy), (135, 104 + dy)], fill=(*TESLA_CYAN, 255))

    full_msg = i18n_tr("DEJALO EN LOS COMENTARIOS...")
    typed_p = clamp01((t - t_vo) / 2.2)
    n_chars = max(1, int(len(full_msg) * typed_p))
    cur = "|" if int(t * 4) % 2 == 0 else " "
    draw_text(cv, full_msg[:n_chars] + cur, 150, 93 + dy, "silk", 8, GOLD, align="left")

    # Sugerencias de temas + llamado abajo
    draw_text(cv, "¿CIENCIA? · ¿VIDEOJUEGOS? · ¿HISTORIA?", 240, 115 + dy, "silk", 8, SOFT_GRAY, align="center")
    draw_text(cv, "¡TE LEEMOS ABAJO!", 240, 132 + dy, "press", 8, CHALK_GREEN, align="center")

    # Muybridge saludando en el piso junto al Zoopraxiscopio sobre su mesa (floor_prop en feet=248)
    char(cv, "muybridge", 168, 248, t, scale=2, arms="wave", look=1, mood="happy",
         talk=talk_v(t, t_vo <= t <= t_end_vo))
    draw_zoopraxiscope_table(cv, 308, 248, t, spin=True, beam=True)

    cv = vignette(cv, 0.32)
    if t > t_end_vo + 0.8:
        k_black = clamp01((t - (t_end_vo + 0.8)) / 1.4)
        cv = fade_to(cv, (7, 10, 31), k_black)
    return cv


T_END = TL.e("c7_07") + 2.2


def scenes():
    return [
        (TL.s("c7_00") - 0.15, make_card(7, ["VEINTICUATRO", "POR SEGUNDO"], "1993 – HOY · DEL DIGITAL AL CABALLO"),
         None, "ch07"),
        (TL.s("c7_01") - 0.15, c7_s01_cgi_and_digital,
         lambda t: cam_push(t, TL.s("c7_01"), TL.s("c7_04"), 1.0, 1.03, (240, 135)), "ch07"),
        (TL.s("c7_04") - 0.15, c7_s02_24fps_everywhere,
         lambda t: cam_push(t, TL.s("c7_04"), TL.s("c7_06"), 1.0, 1.03, (240, 135)), "ch07"),
        (TL.s("c7_06") - 0.15, c7_s03_horse_flies_finale,
         None, "ch07"),
        (TL.s("c7_07") - 0.20, c7_s04_comment_cta,
         None, "ch07"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_sparkle(TL.word("c7_01", "Story"), 0.10)
    A.fx_chime(TL.word("c7_03", "millones"), 0.11)
    A.fx_chime(TL.word("c7_06", "vuela"), 0.13)
    A.fx_pop(TL.s("c7_07"), 0.10)
    A.fx_sparkle(TL.s("c7_07") + 0.35, 0.10)
