"""Capítulo 5: Dos placas en un dormitorio (Toronto 2012, Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton, AlexNet + LA PIZARRA 2: Inteligencia Artificial)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

c5_card = make_card(5, ["DOS PLACAS EN", "UN DORMITORIO"], "2012 · TORONTO Y ALEXNET")


def c5_s01_toronto_alexnet(t):
    """c5_01..c5_03: Cuarto de estudiante en Toronto (2012) con dos placas de juegos, 6 días entrenando fotos y victoria aplastante de AlexNet."""
    t0 = TL.s("c5_01")
    t_c5_02 = TL.s("c5_02")
    t_c5_03 = TL.s("c5_03")

    cv = bg("toronto_dorm_2012").copy()
    d = ImageDraw.Draw(cv)
    draw_place_only(cv, "TORONTO, CANADÁ · 2012 · DOS PLACAS DE JUEGOS", t, t0, border=GPU_GREEN)

    # Dos placas de video brillando sobre el escritorio de trabajo
    draw_nvidia_prop(cv, 240, 248, kind="gpu_pedestal", t=t, state=1.5)
    char(cv, "krizhevsky", 138, 248, t, scale=2, arms="type" if t < t_c5_03 else "cheer", look=1, mood="happy")
    if t >= t_c5_02 - 0.1:
        char(cv, "sutskever", 322, 248, t, scale=2, arms="work" if t < t_c5_03 else "cheer", look=-1, mood="happy")
        char(cv, "hinton12", 368, 248, t, scale=2, arms="point" if t < t_c5_03 else "cheer", look=-1, mood="happy")

    if t < t_c5_02 - 0.12:
        a, dy = pop(t, t0 + 0.1)
        window(cv, 98, 42 + dy, 284, 92, fill=(12, 26, 20), border=GPU_GREEN, alpha=0.95)
        draw_text(cv, "ALEX KRIZHEVSKY · TORONTO (2012)", 240, 52 + dy, "press", 8, GPU_GREEN, align="center")
        draw_text(cv, "EN EL CUARTO DE LA CASA DE SUS PADRES", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PUSO DOS PLACAS DE JUEGOS EN SU PC", 240, 94 + dy, "silk", 8, GOLD, align="center")
    elif t < t_c5_03 - 0.12:
        a, dy = pop(t, t_c5_02 - 0.1)
        window(cv, 98, 42 + dy, 284, 92, fill=(14, 24, 34), border=TESLA_CYAN, alpha=0.95)
        draw_text(cv, "SUTSKEVER Y GEOFFREY HINTON", 240, 52 + dy, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "ENTRENARON UNA RED PARA RECONOCER FOTOS", 240, 74 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "PERROS · AUTOS · FLORES (6 DÍAS)", 240, 94 + dy, "silk", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c5_03 - 0.1)
        window(cv, 98, 40 + dy, 284, 102, fill=(14, 28, 22), border=GOLD, alpha=0.96)
        draw_text(cv, "GANADOR POR PALIZA: ALEXNET", 240, 48 + dy, "press", 8, GOLD, align="center")
        # Barras comparativas de acierto en el concurso de reconocimiento de imágenes
        bars = [("OTROS", 92, (98, 108, 128)), ("ALEXNET (2 GPUS)", 210, GPU_GREEN)]
        for i, (lbl, bw, bcol) in enumerate(bars):
            by = 68 + i * 24 + dy
            draw_text(cv, lbl, 112, by + 2, "silk", 8, CREAM)
            w_cur = int(bw * clamp01((t - t_c5_03) / 1.0))
            d.rectangle([216, by, 216 + max(6, w_cur // 2), by + 12], fill=(*bcol, 255), outline=(*INK, 255))
        draw_text(cv, "VENTAJA HISTÓRICA EN IMAGENET 2012", 240, 120 + dy, "silk", 8, CHALK_YELLOW, align="center")

    return vignette(cv, 0.32)


def c5_s02_pizarra_ai(t):
    """c5_04..c5_07: LA PIZARRA 2 — ¿Por qué una placa de juegos sirve para Inteligencia Artificial?
    - c5_04: Red neuronal que aprende multiplicando tablas enormes de números.
    - c5_05: Millones de multiplicaciones simples a la vez (igual que mover triángulos).
    - c5_06: Vuelve el aula de miles de alumnos + CUDA.
    - c5_07: EN UNA FRASE: EL CHIP DE JUEGOS ERA EL DE LA IA."""
    t0 = TL.s("c5_04")
    t_c5_05 = TL.s("c5_05")
    t_c5_06 = TL.s("c5_06")
    t_c5_07 = TL.s("c5_07")

    cv = draw_pizarra_frame(t, t0, "INTELIGENCIA ARTIFICIAL",
                            summary_es="EL CHIP DE JUEGOS ERA EL CHIP DE LA IA",
                            t_summary=t_c5_07)
    d = ImageDraw.Draw(cv)

    window(cv, 98, 40, 284, 156, fill=(14, 36, 26), border=CHALK_WHITE, alpha=0.95)
    if t < t_c5_05 - 0.1:
        draw_text(cv, "UNA RED NEURONAL APRENDE ASÍ:", 240, 48, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "MULTIPLICANDO TABLAS ENORMES DE NÚMEROS", 240, 66, "silk", 8, CREAM, align="center")
        # Red de nodos conectada a dos matrices de números
        nodes_l = [(134, 96), (134, 126), (134, 156)]
        nodes_r = [(214, 106), (214, 146)]
        for x1, y1 in nodes_l:
            for x2, y2 in nodes_r:
                d.line([(x1, y1), (x2, y2)], fill=(*CHALK_CYAN, 180))
        for nx, ny in nodes_l + nodes_r:
            d.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(24, 68, 48, 255), outline=(*CHALK_WHITE, 255))
        # Matriz A x Matriz B
        d.rectangle([252, 92, 304, 156], outline=(*CHALK_YELLOW, 255))
        d.rectangle([318, 92, 368, 156], outline=(*CHALK_GREEN, 255))
        draw_text(cv, "[A] × [B]", 310, 170, "press", 8, CHALK_YELLOW, align="center")
    elif t < t_c5_06 - 0.1:
        draw_text(cv, "LA MISMA MATEMÁTICA", 240, 48, "press", 8, CHALK_GREEN, align="center")
        draw_text(cv, "MILLONES DE MULTIPLICACIONES A LA VEZ", 240, 66, "silk", 8, CREAM, align="center")
        # Izquierda: triángulo 3D de un juego; Derecha: matriz de IA
        d.polygon([(168, 92), (136, 152), (200, 152)], outline=(*CHALK_CYAN, 255), fill=(22, 58, 44, 255))
        draw_text(cv, "JUEGO 3D", 168, 162, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, "=", 240, 118, "press", 16, CHALK_YELLOW, align="center")
        d.rectangle([278, 92, 348, 152], fill=(22, 58, 44, 255), outline=(*CHALK_GREEN, 255))
        for r in range(3):
            for c in range(3):
                draw_text(cv, f"{(r + c + int(t * 4)) % 9}", 290 + c * 20, 98 + r * 18, "silk", 8, CHALK_WHITE)
        draw_text(cv, "RED NEURONAL", 313, 162, "silk", 8, CHALK_GREEN, align="center")
    else:
        draw_text(cv, "VUELVE EL AULA DE MILES DE ALUMNOS", 240, 48, "press", 8, CHALK_YELLOW, align="center")
        draw_text(cv, "Y GRACIAS A CUDA, CUALQUIERA PUEDE USARLA", 240, 66, "silk", 8, CREAM, align="center")
        gx0, gy0 = 136, 86
        for r in range(5):
            for c in range(12):
                px = gx0 + c * 17
                py = gy0 + r * 16
                on = ((r * 5 + c + int(t * 14)) % 3 == 0)
                col_c = CHALK_GREEN if on else (36, 78, 56)
                d.rectangle([px, py, px + 12, py + 11], fill=(*col_c, 255), outline=(*CHALK_WHITE, 150))

    return vignette(cv, 0.26)


def scenes():
    return [
        (TL.s("c5_00") - 0.15, c5_card),
        (TL.s("c5_01"), c5_s01_toronto_alexnet,
         lambda t: cam_push(t, TL.s("c5_01"), TL.s("c5_04"), 1.0, 1.03, (240, 135), (240, 134))),
        (TL.s("c5_04"), c5_s02_pizarra_ai,
         lambda t: cam_push(t, TL.s("c5_04"), TL.s("c6_00"), 1.0, 1.025, (240, 135), (240, 134))),
    ]


def music(A):
    A.add_pad(TL.s("c5_00"), TL.e("c5_07") - TL.s("c5_00"), (220.0, 277.18, 329.63), amp=0.016)


def sfx(A):
    A.fx_pop(TL.s("c5_01") + 0.15, 0.05)
    A.fx_chime(TL.s("c5_03") + 0.2, 0.06)
    A.fx_pop(TL.s("c5_04") + 0.15, 0.05)
    A.fx_sparkle(TL.s("c5_07") + 0.2, 0.06)
