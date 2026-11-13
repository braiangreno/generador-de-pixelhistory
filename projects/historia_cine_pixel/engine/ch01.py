"""Apertura: Un caballo en el aire (s01..s05) + Capítulo 1: Doce cámaras (c1_00..c1_08)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def s01_s02_question_and_paintings(t):
    """s01..s02: La discusión del siglo XIX sobre el galope del caballo y los cuadros con patas estiradas."""
    t_s01 = TL.s("s01")
    t_preg = TL.word("s01", "pregunta")
    t_cuatro = TL.word("s01", "cuatro")
    t_s02 = TL.s("s02")
    t_pint = TL.word("s02", "pintores", occurrence=1)

    cv = bg("palo_alto_track_1878").copy()
    draw_place_only(cv, "FINES DEL SIGLO XIX · LA GRAN PREGUNTA", t, t_s01, border=GOLD)

    # Personajes debatiendo sobre el suelo firme (feet=248): criador, científico y pintor
    char(cv, "stanford", 136, 248, t, scale=2,
         arms="point" if t < t_s02 else "cross", look=1, mood="neutral",
         talk=talk_v(t, t_s01 <= t < t_s02 - 0.2))
    char(cv, "prof_graz", 240, 248, t, scale=2,
         arms="think" if t < t_cuatro else "shrug", look=-1 if int(t) % 2 == 0 else 1, mood="neutral")
    char(cv, "painter", 344, 248, t, scale=2,
         arms="wave" if t >= t_s02 else "hips", look=-1, mood="happy" if t >= t_s02 else "neutral",
         talk=talk_v(t, t >= t_s02))

    if t < t_s02 - 0.12:
        # Ventana central: el misterio de las 4 patas en el aire
        a, dy = pop(t, t_s01 + 0.1)
        window(cv, 118, 44 + dy, 244, 108, fill=(22, 18, 32), border=GOLD, alpha=0.94)
        draw_text(cv, "¿DESPEGA LAS 4 PATAS A LA VEZ?", 240, 52 + dy, "silk", 8, GOLD, align="center")
        # Caballo corriendo tan rápido que el ojo no alcanza a distinguir las patas
        fast_ph = t * 2.4
        draw_galloping_horse(cv, 240, 96 + dy, fast_ph, scale=2, rider=True)
        if t >= t_cuatro - 0.2:
            draw_text(cv, "¿SIEMPRE TOCA EL SUELO O VUELA?", 240, 134 + dy, "silk", 8, TESLA_CYAN, align="center")
    else:
        # s02: Cómo lo dibujaban los pintores (patas estiradas hacia adelante y atrás como balancín)
        a, dy = pop(t, t_s02 - 0.1)
        window(cv, 118, 44 + dy, 244, 112, fill=(38, 26, 22), border=GOLD, alpha=0.95)
        draw_text(cv, "EL OJO NO ALCANZABA A VERLO", 240, 52 + dy, "silk", 8, CREAM, align="center")
        # Marco de cuadro clásico
        d = ImageDraw.Draw(cv)
        d.rectangle([144, 66 + dy, 336, 128 + dy], fill=(64, 48, 34, 255), outline=(*GOLD, 255), width=2)
        draw_galloping_horse(cv, 240, 96 + dy, 0.0, scale=2, rider=True, painting_spread=True)
        draw_text(cv, "CUADROS: PATAS ESTIRADAS", 240, 138 + dy, "silk", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.34)


def s03_s05_twelve_cameras_and_title(t):
    """s03..s05: Las 12 cámaras en fila con hilos -> La respuesta fue sí -> Título UN CABALLO EN EL AIRE."""
    t_s03 = TL.s("s03")
    t_hilos = TL.word("s03", "hilos")
    t_s04 = TL.s("s04")
    t_cine = TL.word("s04", "cine")
    t_s05 = TL.s("s05")

    cv = bg("palo_alto_track_1878").copy()
    d = ImageDraw.Draw(cv)

    if t < t_s05 - 0.15:
        draw_place_only(cv, "PALO ALTO · 12 CÁMARAS EN FILA", t, t_s03, border=AMBER)

        # Cámaras de madera sobre trípode apoyadas firmemente en el suelo (feet=248)
        for idx_c, cx_cam in enumerate((96, 168, 312, 384)):
            flashing = (t_s03 + 0.6 + idx_c * 0.45) <= t <= (t_s03 + 0.95 + idx_c * 0.45)
            draw_wooden_camera(cv, cx_cam, 248, t, scale=1, flash=flashing, facing=1,
                               label=f"#{idx_c * 3 + 1}")

        # Muybridge operando las cámaras en el suelo
        char(cv, "muybridge", 58, 248, t, scale=2,
             arms="point" if t < t_s04 else "cheer", look=1, mood="happy")

        if t < t_s04 - 0.1:
            # El caballo galopa cortando los hilos frente al muro blanco
            run_u = clamp01((t - t_s03) / max(0.5, (t_s04 - t_s03 - 0.3)))
            hx = int(110 + 260 * run_u)
            # Hilos verticales que se cortan al paso del caballo
            for tx_thread in range(130, 370, 24):
                if hx < tx_thread:
                    d.line([(tx_thread, 130), (tx_thread, 232)], fill=(245, 242, 230, 210), width=1)
                elif abs(hx - tx_thread) < 18:
                    sparkle(cv, tx_thread, 196, t * 5.0, 3, GOLD)
            floor_prop(cv, lambda c, cx, fy: draw_galloping_horse(c, cx, fy - 24, t * 1.3, scale=2, rider=True),
                       hx, 248)
            window(cv, 122, 44, 236, 38, fill=(18, 22, 36), border=GOLD, alpha=0.92)
            draw_text(cv, "12 CÁMARAS + HILOS EN LA PISTA", 240, 52, "silk", 8, GOLD, align="center")
            draw_text(cv, "EL CABALLO DISPARA LAS FOTOS", 240, 66, "silk", 8, CREAM, align="center")
        else:
            # s04: "¡La respuesta fue sí! Y sin buscarlo, abrió la puerta al cine."
            a, dy = pop(t, t_s04 - 0.1)
            window(cv, 118, 44 + dy, 244, 114, fill=(18, 24, 38), border=TESLA_CYAN, alpha=0.95)
            draw_text(cv, "LA RESPUESTA FUE SÍ:", 240, 52 + dy, "press", 8, GOLD, align="center")
            # Fotograma #3 congelado con las 4 patas en el aire recogidas bajo la panza
            d.rectangle([152, 68 + dy, 328, 126 + dy], fill=(228, 214, 184, 255), outline=(*GOLD, 255), width=2)
            draw_galloping_horse(cv, 240, 96 + dy, 0.0, scale=2, frame=2, rider=True, highlight_air=True)
            lbl_bot = "ABRIÓ LA PUERTA AL CINE" if t >= t_cine - 0.2 else "¡LAS 4 PATAS EN EL AIRE!"
            draw_text(cv, lbl_bot, 240, 136 + dy, "silk", 8, TESLA_CYAN, align="center")

        return vignette(cv, 0.34)

    # s05: Placa de título principal del documental ("UN CABALLO EN EL AIRE — LA HISTORIA DEL CINE")
    cv = grade(cv, mul=(0.55, 0.52, 0.65))
    draw_filmstrip(cv, 0, 14, W, 34, t, speed=42.0, sepia=False, color_frames=(t > t_s05 + 2.2), alpha=0.9)
    draw_filmstrip(cv, 0, 222, W, 34, t, speed=-42.0, sepia=False, color_frames=(t > t_s05 + 2.2), alpha=0.9)

    a, dy = pop(t, t_s05 - 0.1)
    window(cv, 116, 54 + dy, 248, 116, fill=(16, 14, 28), border=GOLD, alpha=0.96)
    draw_text(cv, "UN CABALLO", 240, 66 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(1, int((t - t_s05 + 0.2) * 24)))
    draw_text(cv, "EN EL AIRE", 240, 92 + dy, "press", 16, align="center",
              gradient=GOLD_RAMP, outline_w=2, reveal=max(0, int((t - t_s05 - 0.15) * 24)))
    draw_text(cv, "LA HISTORIA DEL CINE", 240, 120 + dy, "press", 8, TESLA_CYAN, align="center",
              reveal=max(0, int((t - t_s05 - 0.45) * 32)))
    draw_text(cv, "MOVIMIENTO · SONIDO · COLOR", 240, 142 + dy, "silk", 8, CREAM, align="center",
              reveal=max(0, int((t - t_s05 - 0.85) * 32)))

    return vignette(cv, 0.36)


# ===========================================================================
# CAPÍTULO 1: DOCE CÁMARAS (c1_01 .. c1_08)
# ===========================================================================

def c1_s01_stanford_and_muybridge(t):
    """c1_01..c1_02: Leland Stanford (ferrocarriles, caballos y el mito de la apuesta) y Eadweard Muybridge."""
    t0 = TL.s("c1_01")
    t_apuesta = TL.word("c1_01", "apuesta")
    t_c1_02 = TL.s("c1_02")
    t_lent = TL.word("c1_02", "lentísimas")

    cv = bg("palo_alto_track_1878").copy()
    draw_place_only(cv, "PALO ALTO, CALIFORNIA", t, t0, border=GOLD)

    if t < t_c1_02 - 0.12:
        # Leland Stanford junto a su caballo en la pista
        char(cv, "stanford", 164, 248, t, scale=2,
             arms="hips" if t < t_apuesta else "shrug", look=1, mood="happy",
             talk=talk_v(t, t0 <= t < t_c1_02 - 0.2))
        floor_prop(cv, lambda c, cx, fy: draw_galloping_horse(c, cx, fy - 22, 0.0, scale=2, frame=7, rider=False, facing=-1),
                   308, 248)

        a, dy = pop(t, t0 + 0.1)
        window(cv, 118, 44 + dy, 244, 86, fill=(20, 18, 32), border=GOLD, alpha=0.94)
        draw_text(cv, "LELAND STANFORD", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "FERROCARRILES Y CABALLOS", 240, 70 + dy, "silk", 8, CREAM, align="center")
        if t >= t_apuesta - 0.2:
            draw_text(cv, "¿APUESTA? LEYENDA SIN PRUEBAS", 240, 92 + dy, "silk", 8, TESLA_CYAN, align="center")
            draw_text(cv, "NADIE PUDO PROBARLO", 240, 108 + dy, "silk", 8, CHALK_YELLOW, align="center")
    else:
        # Eadweard Muybridge trabajando años con las pesadas cámaras de placas húmedas
        char(cv, "muybridge", 184, 248, t, scale=2,
             arms="work" if t >= t_lent - 0.2 else "point", look=1, mood="neutral",
             talk=talk_v(t, t >= t_c1_02))
        draw_wooden_camera(cv, 268, 248, t, scale=2, flash=False, facing=1, label="1872-1878")

        a, dy = pop(t, t_c1_02 - 0.1)
        window(cv, 118, 44 + dy, 244, 86, fill=(20, 18, 32), border=AMBER, alpha=0.94)
        draw_text(cv, "EADWEARD MUYBRIDGE", 240, 52 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "FOTÓGRAFO DEL EXPERIMENTO", 240, 70 + dy, "silk", 8, CREAM, align="center")
        if t >= t_lent - 0.25:
            draw_text(cv, "CÁMARAS LENTÍSIMAS", 240, 92 + dy, "silk", 8, CHALK_RED, align="center")
            draw_text(cv, "TARDÓ AÑOS EN LOGRARLO", 240, 108 + dy, "silk", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.34)


def c1_s02_sallie_gardner_and_wheel(t):
    """c1_03..c1_05: Sallie Gardner en 1878 frente a periodistas -> 4 patas recogidas -> Zoopraxiscopio en la pared."""
    t_c1_03 = TL.s("c1_03")
    t_c1_04 = TL.s("c1_04")
    t_panza = TL.word("c1_04", "panza")
    t_c1_05 = TL.s("c1_05")
    t_pared = TL.word("c1_05", "pared")

    cv = bg("palo_alto_track_1878").copy()

    if t < t_c1_04 - 0.12:
        # 1878: Sallie Gardner corre frente a los periodistas y las 12 cámaras
        draw_place_only(cv, "PALO ALTO · JUNIO DE 1878", t, t_c1_03, border=GOLD)
        char(cv, "muybridge", 82, 248, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, "reporter", 392, 248, t, scale=2, arms="note", look=-1, mood="happy")
        for idx_c, cx_c in enumerate((142, 206, 270, 334)):
            draw_wooden_camera(cv, cx_c, 248, t, scale=1,
                               flash=abs((t - t_c1_03) - (0.8 + idx_c * 0.45)) < 0.2, facing=1)

        run_p = clamp01((t - t_c1_03 - 0.2) / max(0.8, (t_c1_04 - t_c1_03 - 0.5)))
        hx = int(128 + 216 * run_p)
        floor_prop(cv, lambda c, cx, fy: draw_galloping_horse(c, cx, fy - 24, t * 1.4, scale=2, rider=True),
                   hx, 248)

        window(cv, 120, 44, 240, 40, fill=(18, 22, 36), border=GOLD, alpha=0.94)
        draw_text(cv, "1878 · YEGUA «SALLIE GARDNER»", 240, 52, "press", 8, GOLD, align="center")
        draw_text(cv, "12 FOTOS EN MEDIO SEGUNDO", 240, 68, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    if t < t_c1_05 - 0.12:
        # c1_04: Las cuatro patas en el aire, recogidas bajo la panza vs estiradas en los cuadros
        draw_place_only(cv, "EL DESCUBRIMIENTO DE MUYBRIDGE", t, t_c1_04, border=TESLA_CYAN)
        char(cv, "muybridge", 118, 248, t, scale=2, arms="point", look=1, mood="happy")
        char(cv, "stanford", 362, 248, t, scale=2, arms="cheer", look=-1, mood="happy")

        a, dy = pop(t, t_c1_04 - 0.1)
        window(cv, 116, 42 + dy, 248, 128, fill=(20, 18, 30), border=TESLA_CYAN, alpha=0.96)
        d = ImageDraw.Draw(cv)
        # Arriba: la foto real de Muybridge (recogidas bajo la panza)
        d.rectangle([126, 50 + dy, 354, 104 + dy], fill=(232, 220, 192, 255), outline=(*GOLD, 255))
        draw_galloping_horse(cv, 178, 76 + dy, 0.0, scale=2, frame=2, rider=True, highlight_air=True)
        draw_text(cv, "FOTO REAL:", 282, 62 + dy, "press", 8, INK, align="center", outline=None, shadow=False)
        draw_text(cv, "RECOGIDAS BAJO", 282, 76 + dy, "silk", 8, (148, 32, 28), align="center", outline=None, shadow=False)
        draw_text(cv, "LA PANZA", 282, 88 + dy, "silk", 8, (148, 32, 28), align="center", outline=None, shadow=False)

        # Abajo: comparación con los cuadros antiguos
        if t >= t_panza - 0.2:
            d.rectangle([126, 110 + dy, 354, 160 + dy], fill=(42, 30, 26, 255), outline=(*CHALK_RED, 255))
            draw_galloping_horse(cv, 178, 134 + dy, 0.0, scale=1, painting_spread=True, rider=False)
            draw_text(cv, "NO ESTIRADAS", 282, 122 + dy, "silk", 8, CHALK_RED, align="center")
            draw_text(cv, "COMO EN LOS CUADROS", 282, 138 + dy, "silk", 8, CREAM, align="center")
        return vignette(cv, 0.34)

    # c1_05: Puso las fotos en una rueda (Zoopraxiscopio) y las proyectó en una pared
    cv = grade(cv, mul=(0.45, 0.45, 0.58))
    draw_place_only(cv, "1879 · EL ZOOPRAXISCOPIO", t, t_c1_05, border=GOLD)

    char(cv, "muybridge", 118, 248, t, scale=2, arms="work", look=1, mood="happy")
    draw_zoopraxiscope_table(cv, 182, 248, t, spin=True, beam=True)
    char(cv, "spectator", 376, 248, t, scale=2, arms="up" if t >= t_pared else "down", look=-1, mood="happy")

    # Pared de proyección iluminada en el centro
    window(cv, 122, 46, 236, 108, fill=(242, 234, 206), border=GOLD, alpha=0.96)
    draw_text(cv, "FOTOS EN UNA RUEDA GIRATORIA", 240, 54, "silk", 8, INK, align="center", outline=None, shadow=False)
    draw_galloping_horse(cv, 240, 98, t * 1.1, scale=2, silhouette_col=(28, 22, 18), rider=True)
    draw_text(cv, "¡VOLVIÓ A CORRER EN LA PARED!", 240, 136, "press", 8, (148, 36, 28),
              align="center", outline=None, shadow=False)

    return vignette(cv, 0.38)


def c1_s03_pizarra_persistence(t):
    """c1_06..c1_08: LA PIZARRA 1 (El cerebro rellena los huecos + flipbook a 10-12 fps) y cierre del capítulo."""
    t_c1_06 = TL.s("c1_06")
    t_huecos = TL.word("c1_06", "huecos")
    t_c1_07 = TL.s("c1_07")
    t_cuad = TL.word("c1_07", "cuaderno")
    t_c1_08 = TL.s("c1_08")

    if t < t_c1_08 - 0.15:
        cv = draw_pizarra_frame(
            t, t_c1_06, "EL CEREBRO Y EL MOVIMIENTO",
            summary_es="+10 FOTOS/SEG = MOVIMIENTO",
            t_summary=t_cuad + 0.6,
        )
        d = ImageDraw.Draw(cv)

        if t < t_c1_07 - 0.1:
            # 3 fotos quietas separadas -> el cerebro rellena los huecos
            window(cv, 118, 42, 244, 152, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96)
            draw_text(cv, "3 FOTOS QUIETAS SEPARADAS:", 240, 50, "silk", 8, CHALK_WHITE, align="center")
            for idx_f, (fx, fr_num) in enumerate(((158, 0), (240, 2), (322, 6))):
                d.rectangle([fx - 32, 66, fx + 32, 116], fill=(22, 52, 36, 255), outline=(*CHALK_YELLOW, 255))
                draw_galloping_horse(cv, fx, 90, 0.0, scale=1, frame=fr_num,
                                     silhouette_col=CHALK_WHITE, rider=False)
                draw_text(cv, f"FOTO {idx_f + 1}", fx, 105, "silk", 8, CHALK_YELLOW, align="center")

            if t >= t_huecos - 0.4:
                # Flechas punteadas de tiza mostrando cómo el cerebro une las fotos
                d.line([(192, 90), (206, 90)], fill=(*CHALK_CYAN, 255), width=2)
                d.line([(274, 90), (288, 90)], fill=(*CHALK_CYAN, 255), width=2)
                draw_text(cv, "EL CEREBRO RELLENA LOS HUECOS", 240, 132, "press", 8, CHALK_CYAN, align="center")
                draw_text(cv, "UNE LAS POSES EN UNA SOLA ACCIÓN", 240, 152, "silk", 8, CHALK_GREEN, align="center")
                draw_chalk_hand(cv, 326, 148, t)
        else:
            # c1_07: +10 a 12 imágenes por segundo + cuaderno con dibujitos en las esquinas (flipbook)
            window(cv, 118, 42, 244, 154, fill=(16, 40, 28), border=CHALK_YELLOW, alpha=0.96)
            draw_text(cv, "10 A 12 IMÁGENES POR SEGUNDO", 240, 50, "press", 8, CHALK_YELLOW, align="center")
            draw_text(cv, "YA NO VES FOTOS: VES MOVIMIENTO", 240, 66, "silk", 8, CHALK_WHITE, align="center")

            # Cuaderno / flipbook animado en el centro de la pizarra
            d.rectangle([156, 84, 324, 164], fill=(238, 232, 212, 255), outline=(*INK, 255), width=2)
            # Anillado del cuaderno a la izquierda y hojas pasando en la esquina derecha
            for ry in range(90, 160, 10):
                d.rectangle([152, ry, 160, ry + 4], fill=(90, 96, 110, 255), outline=(*INK, 255))
            page_flip = int(t * 12) % 4
            for p_i in range(3):
                px_r = 320 - p_i * 3 - (page_flip if p_i == 0 else 0)
                d.line([(px_r, 86), (px_r, 162)], fill=(168, 158, 138, 255))
            # Caballito dibujado en la esquina del cuaderno corriendo a 12 fps
            draw_galloping_horse(cv, 252, 122, t * 1.0, scale=2, silhouette_col=(36, 48, 92), rider=False)
            draw_text(cv, "CUADERNO (FLIPBOOK)", 240, 174, "silk", 8, CHALK_CYAN, align="center")

        return vignette(cv, 0.28)

    # c1_08: Remate del Capítulo 1 — "Ya había movimiento. Faltaba mostrarlo a una sala llena."
    cv = bg("palo_alto_track_1878").copy()
    cv = grade(cv, mul=(0.52, 0.50, 0.66))
    draw_place_only(cv, "FIN DEL CAPÍTULO 1 · EL PRÓXIMO PASO", t, t_c1_08, border=GOLD)

    char(cv, "muybridge", 148, 248, t, scale=2, arms="hips", look=1, mood="happy")
    draw_zoopraxiscope_table(cv, 240, 248, t, spin=True, beam=True)

    a, dy = pop(t, t_c1_08 - 0.1)
    window(cv, 118, 52 + dy, 244, 96, fill=(18, 16, 30), border=GOLD, alpha=0.96)
    draw_text(cv, "YA HABÍA MOVIMIENTO.", 240, 68 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "FALTABA MOSTRARLO", 240, 94 + dy, "press", 8, TESLA_CYAN, align="center")
    draw_text(cv, "A UNA SALA LLENA.", 240, 114 + dy, "press", 8, CREAM, align="center")

    return vignette(cv, 0.36)


def scenes():
    return [
        (0.0, s01_s02_question_and_paintings,
         lambda t: cam_push(t, 0.0, TL.s("s03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("s03") - 0.15, s03_s05_twelve_cameras_and_title,
         lambda t: cam_push(t, TL.s("s03"), TL.s("c1_00"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_00") - 0.15, make_card(1, ["DOCE", "CÁMARAS"], "1878 · PALO ALTO, CALIFORNIA"),
         None, "ch01"),
        (TL.s("c1_01") - 0.15, c1_s01_stanford_and_muybridge,
         lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_03"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_03") - 0.15, c1_s02_sallie_gardner_and_wheel,
         lambda t: cam_push(t, TL.s("c1_03"), TL.s("c1_06"), 1.0, 1.03, (240, 135)), "ch01"),
        (TL.s("c1_06") - 0.15, c1_s03_pizarra_persistence,
         lambda t: cam_push(t, TL.s("c1_06"), TL.s("c2_00"), 1.0, 1.03, (240, 135)), "ch01"),
    ]


def music(A):
    return


def sfx(A):
    A.fx_pop(TL.s("s01") + 0.2, 0.08)
    A.fx_pop(TL.s("s03"), 0.08)
    A.fx_sparkle(TL.s("s04"), 0.10)
    A.fx_chime(TL.s("s05"), 0.11)
    A.fx_pop(TL.s("c1_03"), 0.09)
    A.fx_sparkle(TL.s("c1_04"), 0.10)
    A.fx_chime(TL.s("c1_08"), 0.10)
