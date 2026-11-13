"""Capítulo 3: El mago (Georges Méliès, el truco de sustitución, Viaje a la Luna y la Legión de Honor)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def draw_toy_kiosk(cv, x, feet=248, t=0.0):
    """Puesto de juguetes y caramelos de Georges Méliès en la estación Montparnasse de París,
    apoyado firmemente sobre el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 42
        shadow_ellipse(canvas, cx, fy, 42, 5, 90)
        # Mostrador de madera hasta el suelo
        d.rectangle([cx - 32, top_y, cx + 32, fy], fill=(116, 74, 42, 255), outline=(*INK, 255))
        d.rectangle([cx - 28, top_y + 6, cx + 28, fy - 4], fill=(88, 54, 30, 255), outline=(168, 118, 62, 255))
        # Toldo rayado rojo y crema sostenido por dos parantes de madera unidos al mostrador
        d.rectangle([cx - 30, top_y - 28, cx - 27, top_y], fill=(92, 58, 32, 255), outline=(*INK, 255))
        d.rectangle([cx + 27, top_y - 28, cx + 30, top_y], fill=(92, 58, 32, 255), outline=(*INK, 255))
        for i, sx in enumerate(range(cx - 34, cx + 30, 8)):
            col_s = (188, 42, 48, 255) if i % 2 == 0 else (242, 234, 212, 255)
            d.rectangle([sx, top_y - 36, sx + 8, top_y - 26], fill=col_s, outline=(*INK, 255))
        # Frascos de caramelos y juguetitos apoyados sobre el mostrador (top_y)
        d.rectangle([cx - 22, top_y - 10, cx - 12, top_y], fill=(238, 128, 168, 255), outline=(*INK, 255))
        d.rectangle([cx - 6, top_y - 12, cx + 6, top_y], fill=(108, 224, 245, 255), outline=(*INK, 255))
        # Caballito/cohete de juguete sobre el mostrador
        d.polygon([(cx + 14, top_y), (cx + 18, top_y - 11), (cx + 24, top_y)],
                  fill=(244, 196, 84, 255), outline=(*INK, 255))

    floor_prop(cv, _draw, x, feet)


def c3_s01_melies_and_camera(t):
    """c3_01..c3_03: Georges Méliès en la primera función -> negativa de los Lumière -> su propia cámara."""
    t0 = TL.s("c3_01")
    t_c3_02 = TL.s("c3_02")
    t_futuro = TL.word("c3_02", "futuro")
    t_c3_03 = TL.s("c3_03")

    if t < t_c3_03 - 0.12:
        cv = bg("paris_salon_indien_1895").copy()
        draw_place_only(cv, "PARÍS · 1895 · GEORGES MÉLIÈS", t, t0, border=GOLD)

        char(cv, "antoine_lumiere", 156, 248, t, scale=2,
             arms="cross" if t >= t_c3_02 else "down", look=1, mood="neutral",
             talk=talk_v(t, t_c3_02 + 0.8 <= t < t_c3_03 - 0.2))
        draw_cinematograph_tripod(cv, 232, 248, t, beam=False, crank=False, facing=1)
        char(cv, "melies", 316, 248, t, scale=2,
             arms="offer" if t >= t_c3_02 else "cheer", look=-1, mood="happy",
             talk=talk_v(t, t0 <= t < t_c3_02 + 0.7))

        if t < t_c3_02 - 0.1:
            a, dy = pop(t, t0 + 0.1)
            window(cv, 118, 44 + dy, 244, 78, fill=(24, 18, 34), border=GOLD, alpha=0.95)
            draw_text(cv, "GEORGES MÉLIÈS", 240, 54 + dy, "press", 8, GOLD, align="center")
            draw_text(cv, "ILUSIONISTA Y MAGO DE TEATRO", 240, 72 + dy, "silk", 8, CREAM, align="center")
            draw_text(cv, "ESTABA ENTRE LOS 33 ESPECTADORES", 240, 90 + dy, "silk", 8, TESLA_CYAN, align="center")
        else:
            a, dy = pop(t, t_c3_02 - 0.1)
            window(cv, 118, 44 + dy, 244, 88, fill=(28, 18, 32), border=CHALK_RED, alpha=0.95)
            draw_text(cv, "QUISO COMPRAR EL CINEMATÓGRAFO", 240, 52 + dy, "silk", 8, CREAM, align="center")
            draw_text(cv, "LOS LUMIÈRE LE DIJERON QUE NO", 240, 70 + dy, "press", 8, CHALK_RED, align="center")
            if t >= t_futuro - 0.35:
                draw_text(cv, "LEYENDA: «ES UN INVENTO SIN FUTURO»", 240, 94 + dy, "silk", 8, GOLD, align="center")
                bubble(cv, "«NO ESTÁ EN VENTA»", 156, 138)
        return vignette(cv, 0.36)

    # c3_03: Consiguió un proyector inglés y lo convirtió en su propia cámara
    cv = bg("melies_glass_studio").copy()
    draw_place_only(cv, "ESTUDIO DE MONTREUIL · PARÍS", t, t_c3_03, border=TESLA_CYAN)
    char(cv, "melies", 184, 248, t, scale=2, arms="work", look=1, mood="happy")
    draw_wooden_camera(cv, 272, 248, t, scale=2, flash=True, facing=1, label="PROYECTOR -> CÁMARA")

    a, dy = pop(t, t_c3_03 - 0.1)
    window(cv, 118, 46 + dy, 244, 82, fill=(18, 24, 42), border=TESLA_CYAN, alpha=0.95)
    draw_text(cv, "EL TALLER DE MÉLIÈS", 240, 56 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "CONSIGUIÓ UN PROYECTOR INGLÉS", 240, 76 + dy, "silk", 8, CREAM, align="center")
    draw_text(cv, "Y LO CONVIRTIÓ EN SU CÁMARA", 240, 96 + dy, "silk", 8, TESLA_CYAN, align="center")

    return vignette(cv, 0.35)


def c3_s02_stop_trick_and_moon(t):
    """c3_04..c3_06: El ómnibus que se convierte en coche fúnebre -> el truco de parar la cámara -> Viaje a la Luna (1902)."""
    t_c3_04 = TL.s("c3_04")
    t_fun = TL.word("c3_04", "fúnebre")
    t_c3_05 = TL.s("c3_05")
    t_c3_06 = TL.s("c3_06")
    t_luna = TL.word("c3_06", "Luna")
    t_ojo = TL.word("c3_06", "ojo")

    cv = bg("melies_glass_studio").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c3_06 - 0.12:
        draw_place_only(cv, "PARÍS · EL TRUCO POR ACCIDENTE", t, t_c3_04, border=GOLD)
        char(cv, "melies", 136, 248, t, scale=2,
             arms="point" if t >= t_c3_05 else "work", look=1, mood="happy")
        draw_wooden_camera(cv, 206, 248, t, scale=1, flash=(t >= t_fun - 0.15), facing=1)

        window(cv, 118, 42, 244, 124, fill=(20, 18, 36), border=GOLD, alpha=0.96)
        if t < t_c3_05 - 0.1:
            is_hearse = t >= t_fun - 0.25
            draw_text(cv, "LA CÁMARA SE TRABÓ UN MINUTO", 240, 50, "silk", 8, CREAM, align="center")
            # Calle parisina dentro de la pantalla de proyección
            d.rectangle([138, 66, 342, 128], fill=(214, 206, 188, 255), outline=(*INK, 255))
            if not is_hearse:
                # Ómnibus alegre tirado por caballos
                d.rectangle([186, 82, 294, 114], fill=(186, 62, 48, 255), outline=(*INK, 255))
                draw_text(cv, "ÓMNIBUS", 240, 94, "press", 8, CREAM, align="center")
            else:
                # De golpe: coche fúnebre negro con penachos
                d.rectangle([186, 80, 294, 114], fill=(24, 22, 32, 255), outline=(*GOLD, 255))
                draw_text(cv, "¡COCHE FÚNEBRE!", 240, 94, "press", 8, GOLD, align="center")
                sparkle(cv, 182, 82, t * 5.0, 4, TESLA_CYAN)
                sparkle(cv, 298, 82, t * 5.0 + 1.0, 4, TESLA_CYAN)
            for wx_w in (202, 278):
                d.ellipse([wx_w - 8, 108, wx_w + 8, 124], fill=(42, 32, 24, 255), outline=(*GOLD, 255))
            draw_text(cv, "ÓMNIBUS -> COCHE FÚNEBRE", 240, 138, "press", 8, TESLA_CYAN, align="center")
        else:
            # c3_05: El truco de sustitución explicado paso a paso
            draw_text(cv, "EL TRUCO DE SUSTITUCIÓN", 240, 50, "press", 8, GOLD, align="center")
            steps = [
                ("1. PARAS LA CÁMARA", CHALK_YELLOW),
                ("2. CAMBIAS ALGO EN ESCENA", TESLA_CYAN),
                ("3. SIGUES FILMANDO = ¡MAGIA!", CHALK_GREEN),
            ]
            for idx_s, (s_txt, s_col) in enumerate(steps):
                sy_r = 72 + idx_s * 26
                d.rectangle([130, sy_r, 350, sy_r + 20], fill=(28, 24, 48, 255), outline=(*s_col, 255))
                draw_text(cv, s_txt, 240, sy_r + 6, "silk", 8, s_col, align="center")
        return vignette(cv, 0.35)

    # c3_06: 1902 — Viaje a la Luna (la nave se clava en su ojo)
    draw_place_only(cv, "1902 · VIAJE A LA LUNA (MÉLIÈS)", t, t_c3_06, border=GOLD)
    char(cv, "melies", 118, 248, t, scale=2, arms="cheer", look=1, mood="happy")
    draw_wooden_camera(cv, 362, 248, t, scale=1, flash=True, facing=-1)

    window(cv, 118, 40, 244, 132, fill=(14, 18, 38), border=GOLD, alpha=0.96)
    STARS.draw(cv, t, alpha=0.6)
    draw_text(cv, "1902 · VIAJE A LA LUNA", 240, 48, "press", 8, GOLD, align="center")
    rk_prog = clamp01((t - (t_luna - 0.4)) / max(0.35, (t_ojo - t_luna + 0.4)))
    draw_melies_moon(cv, 240, 104, r=30, rocket_p=rk_prog, t=t)
    lbl_m = "¡SE CLAVA EN SU OJO!" if t >= t_ojo - 0.25 else "DESAPARICIONES · CABEZAS · COHETE"
    draw_text(cv, lbl_m, 240, 148, "silk", 8, TESLA_CYAN if t >= t_ojo - 0.25 else CREAM, align="center")

    return vignette(cv, 0.35)


def c3_s03_piracy_kiosk_and_honor(t):
    """c3_07..c3_10: Copias piratas en EE. UU. -> puesto de juguetes en París -> Legión de Honor 1931 -> Remate."""
    t_c3_07 = TL.s("c3_07")
    t_propia = TL.word("c3_07", "propia")
    t_c3_08 = TL.s("c3_08")
    t_c3_09 = TL.s("c3_09")
    t_honor = TL.word("c3_09", "Honor")
    t_c3_10 = TL.s("c3_10")

    cv = bg("melies_glass_studio").copy()
    d = ImageDraw.Draw(cv)

    if t < t_c3_08 - 0.12:
        # c3_07: En EE. UU. la copiaron sin permiso y le ofrecieron su propia película
        draw_place_only(cv, "COPIAS SIN PERMISO EN EE. UU.", t, t_c3_07, border=CHALK_RED)
        char(cv, "investor_a", 158, 248, t, scale=2, arms="offer", look=1, mood="happy",
             talk=talk_v(t, t >= t_propia - 0.5))
        char(cv, "melies", 318, 248, t, scale=2, arms="shrug" if t >= t_propia - 0.3 else "hips",
             look=-1, mood="worried")

        # Mesa con latas de película copiadas apoyada en el suelo (feet=248)
        def _draw_film_cans_table(canvas, cx, fy):
            d_t = ImageDraw.Draw(canvas)
            top_y = fy - 34
            shadow_ellipse(canvas, cx, fy, 28, 4, 85)
            d_t.rectangle([cx - 20, top_y + 4, cx - 16, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
            d_t.rectangle([cx + 16, top_y + 4, cx + 20, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
            d_t.rectangle([cx - 24, top_y, cx + 24, top_y + 5], fill=(124, 78, 42, 255), outline=(*INK, 255))
            for i_c in range(3):
                cy_c = top_y - 4 - i_c * 4
                d_t.rectangle([cx - 12, cy_c, cx + 12, cy_c + 4], fill=(176, 184, 198, 255), outline=(*INK, 255))
        floor_prop(cv, _draw_film_cans_table, 238, 248)

        a, dy = pop(t, t_c3_07 - 0.1)
        window(cv, 118, 44 + dy, 244, 88, fill=(28, 18, 28), border=CHALK_RED, alpha=0.95)
        draw_text(cv, "PIRATERÍA EN ESTADOS UNIDOS", 240, 54 + dy, "press", 8, CHALK_RED, align="center")
        draw_text(cv, "COPIARON «VIAJE A LA LUNA»", 240, 74 + dy, "silk", 8, CREAM, align="center")
        if t >= t_propia - 0.4:
            draw_text(cv, "LE OFRECIERON COMPRAR...", 240, 92 + dy, "silk", 8, GOLD, align="center")
            draw_text(cv, "¡SU PROPIA PELÍCULA!", 240, 108 + dy, "press", 8, TESLA_CYAN, align="center")
        return vignette(cv, 0.36)

    if t < t_c3_09 - 0.12:
        # c3_08: Arruinado tras la guerra, vendiendo juguetes y caramelos en la estación Montparnasse
        cv = grade(cv, mul=(0.72, 0.74, 0.84))
        draw_place_only(cv, "AÑOS 1920 · ESTACIÓN MONTPARNASSE, PARÍS", t, t_c3_08, border=SOFT_GRAY)
        draw_toy_kiosk(cv, 214, 248, t)
        char(cv, "melies_old", 282, 248, t, scale=2, arms="down", look=-1, mood="sad")

        a, dy = pop(t, t_c3_08 - 0.1)
        window(cv, 118, 46 + dy, 244, 82, fill=(20, 22, 34), border=SOFT_GRAY, alpha=0.95)
        draw_text(cv, "OLVIDADO TRAS LA GUERRA", 240, 56 + dy, "press", 8, SOFT_GRAY, align="center")
        draw_text(cv, "TERMINÓ VENDIENDO JUGUETES", 240, 76 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "Y CARAMELOS EN UNA ESTACIÓN", 240, 94 + dy, "silk", 8, GOLD, align="center")
        return vignette(cv, 0.40)

    if t < t_c3_10 - 0.12:
        # c3_09: Redescubierto por periodistas; en 1931 recibe la Legión de Honor de manos de Louis Lumière
        draw_place_only(cv, "PARÍS · 1931 · LEGIÓN DE HONOR", t, t_c3_09, border=GOLD)
        char(cv, "reporter", 112, 248, t, scale=2, arms="note", look=1, mood="happy")
        char(cv, "louis_lumiere", 216, 248, t, scale=2, arms="offer", look=1, mood="happy",
             talk=talk_v(t, t >= t_honor - 0.3))
        char(cv, "melies_old", 296, 248, t, scale=2, arms="cheer" if t >= t_honor else "down",
             look=-1, mood="happy")

        a, dy = pop(t, t_c3_09 - 0.1)
        window(cv, 118, 44 + dy, 244, 92, fill=(22, 18, 36), border=GOLD, alpha=0.96)
        draw_text(cv, "1931 · REDESCUBIERTO", 240, 54 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "RECIBIÓ LA LEGIÓN DE HONOR", 240, 74 + dy, "silk", 8, CREAM, align="center")
        # Medalla roja y dorada de la Legión de Honor
        d.polygon([(236, 88 + dy), (244, 88 + dy), (242, 100 + dy), (238, 100 + dy)], fill=(214, 42, 48, 255))
        d.ellipse([234, 98 + dy, 246, 110 + dy], fill=(*GOLD, 255), outline=(*CREAM, 255))
        draw_text(cv, "ENTREGADA POR LOUIS LUMIÈRE", 240, 116 + dy, "silk", 8, TESLA_CYAN, align="center")
        return vignette(cv, 0.34)

    # c3_10: Remate — "Los Lumière filmaron la realidad. Méliès filmó los sueños. El cine necesitó a los dos."
    draw_place_only(cv, "LA REALIDAD Y LOS SUEÑOS", t, t_c3_10, border=GOLD)
    char(cv, "louis_lumiere", 148, 248, t, scale=2, arms="hips", look=1, mood="happy")
    char(cv, "melies", 332, 248, t, scale=2, arms="wave", look=-1, mood="happy")

    a, dy = pop(t, t_c3_10 - 0.1)
    window(cv, 116, 44 + dy, 248, 112, fill=(18, 16, 32), border=GOLD, alpha=0.96)
    d.rectangle([126, 54 + dy, 354, 78 + dy], fill=(26, 36, 54, 255), outline=(*TESLA_CYAN, 255))
    draw_text(cv, "LUMIÈRE: LA REALIDAD", 240, 62 + dy, "press", 8, TESLA_CYAN, align="center")
    d.rectangle([126, 84 + dy, 354, 108 + dy], fill=(42, 24, 48, 255), outline=(*GOLD, 255))
    draw_text(cv, "MÉLIÈS: LOS SUEÑOS", 240, 92 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "EL CINE NECESITÓ A LOS DOS.", 240, 124 + dy, "press", 8, CREAM, align="center")

    return vignette(cv, 0.36)


def scenes():
    return [
        (TL.s("c3_00") - 0.15, make_card(3, ["EL", "MAGO"], "1895 – 1931 · PARÍS"),
         None, "ch03"),
        (TL.s("c3_01") - 0.15, c3_s01_melies_and_camera,
         lambda t: cam_push(t, TL.s("c3_01"), TL.s("c3_04"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_04") - 0.15, c3_s02_stop_trick_and_moon,
         lambda t: cam_push(t, TL.s("c3_04"), TL.s("c3_07"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_07") - 0.15, c3_s03_piracy_kiosk_and_honor,
         lambda t: cam_push(t, TL.s("c3_07"), TL.s("c4_00"), 1.0, 1.03, (240, 135)), "ch03"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_pop(TL.s("c3_02"), 0.08)
    A.fx_sparkle(TL.word("c3_04", "fúnebre"), 0.10)
    A.fx_pop(TL.word("c3_06", "ojo"), 0.11)
    A.fx_chime(TL.word("c3_09", "Honor"), 0.11)
    A.fx_chime(TL.s("c3_10"), 0.11)
