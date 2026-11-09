"""Apertura (s01..s07) + Capítulo 1: El artículo que nunca terminó (c1_00..c1_05)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

# Cast de sprites para Dune
HERBERT = {
    "skin": (235, 192, 152), "hair": (110, 74, 46), "hair_style": "parted",
    "beard": (105, 70, 42), "glasses": True,
    "shirt": (236, 226, 200), "jacket": (132, 96, 62),
    "tie": (158, 62, 44), "pants": (68, 56, 46),
}
USDA_WORKER_1 = {
    "skin": (228, 182, 144), "hair": (70, 52, 38), "hair_style": "short",
    "shirt": (196, 178, 132), "jacket": (76, 112, 68),
    "pants": (62, 78, 54),
}
USDA_WORKER_2 = {
    "skin": (214, 166, 128), "hair": (50, 40, 32), "hair_style": "short",
    "shirt": (210, 194, 150), "jacket": (88, 124, 76),
    "pants": (58, 74, 52),
}
READER_1 = {
    "skin": (236, 194, 158), "hair": (64, 44, 32), "hair_style": "parted",
    "shirt": (220, 230, 245), "jacket": (54, 82, 134),
    "pants": (46, 54, 76),
}
READER_2 = {
    "skin": (224, 178, 142), "hair": (148, 72, 42), "hair_style": "long",
    "shirt": (244, 214, 168), "jacket": (164, 88, 52),
    "pants": (64, 52, 48),
}


def _draw_biplane(cv, cx, cy, t):
    """Avioneta de los años 50 sobrevolando las dunas de Oregón."""
    d = ImageDraw.Draw(cv)
    by = cy + int(round(math.sin(t * 4.2) * 2))
    # Fuselaje amarillo/crema con franja roja
    d.rectangle([cx - 22, by - 4, cx + 16, by + 4], fill=(242, 202, 78, 255), outline=(*INK, 255))
    d.line([(cx - 20, by + 1), (cx + 14, by + 1)], fill=(208, 62, 48, 255), width=2)
    # Cola
    d.polygon([(cx - 22, by - 4), (cx - 30, by - 12), (cx - 16, by - 4)], fill=(208, 62, 48, 255), outline=(*INK, 255))
    # Ala superior
    d.rectangle([cx - 12, by - 8, cx + 10, by - 5], fill=(248, 232, 170, 255), outline=(*INK, 255))
    # Cabina
    d.rectangle([cx - 4, by - 4, cx + 6, by - 1], fill=(130, 205, 245, 255), outline=(*INK, 255))
    # Hélice girando
    ph = int(t * 28) % 2
    if ph == 0:
        d.line([(cx + 18, by - 8), (cx + 18, by + 8)], fill=(220, 230, 240, 230), width=2)
    else:
        d.line([(cx + 18, by - 4), (cx + 18, by + 4)], fill=(180, 195, 210, 200), width=2)


# ===========================================================================
# ESCENA 1 (s01, s02): 1957. Florence, Oregón — Vuelo sobre las dunas
# ===========================================================================
def scene_oregon_flight(t):
    t0 = TL.s("s01")
    dt = max(0.0, t - t0)

    # Primeros 0.55s: pantalla oscura con la ondulación de arena abriendo el documental
    if dt < 0.55:
        cv = new_canvas((10, 12, 18))
        draw_sand_ripple(cv, t, y_base=145, x_start=30, x_end=450, progress=dt / 0.55)
        draw_text(cv, "1957 · FLORENCE, OREGÓN", 240, 108, "press", 8, GOLD, align="center")
        return cv

    cv = bg("bg_oregon_dunes_1957").copy()
    d = ImageDraw.Draw(cv)
    draw_sand_wind(cv, t, density=34, color=(236, 210, 155), y_min=95, y_max=260)

    # Ondulación bajo la arena avanzando hacia los pinos de la derecha
    u_rip = clamp01((t - t0) / max(1.0, TL.e("s02") - t0))
    draw_sand_ripple(cv, t, y_base=242, x_start=60, x_end=445, progress=u_rip)

    # Avioneta cruzando el cielo de izquierda a derecha
    px = int(90 + u_rip * 290)
    _draw_biplane(cv, px, 64, t)

    # Encabezado superior
    window(cv, 20, 10, 440, 36, fill=(14, 22, 36), border=GOLD, alpha=0.94)
    draw_text(cv, "1957 · FLORENCE, OREGÓN", 240, 16, "press", 8, GOLD, align="center")
    draw_text(cv, "DUNAS QUE AVANZAN SOBRE RUTAS, BOSQUES Y CASAS", 240, 30, "silk", 8, CYAN, align="center")

    # Recuadro inferior: Frank Herbert tomando notas desde el avión
    if t >= TL.s("s02") - 0.1:
        window(cv, 18, 186, 236, 72, fill=(16, 22, 36), border=CREAM, alpha=0.94)
        portrait(cv, "herbert", 26, 194, 56)
        draw_text(cv, "FRANK HERBERT", 92, 196, "press", 8, GOLD)
        draw_text(cv, "PERIODISTA EN VUELO", 92, 210, "silk", 8, CYAN)
        draw_text(cv, "«UN MAR DE ARENA EN", 92, 226, "silk", 8, CREAM)
        draw_text(cv, "MOVIMIENTO...»", 92, 238, "silk", 8, CREAM)

    robot(cv, 436, 258, t, face="surprised", scale=1)
    return cv


# ===========================================================================
# ESCENA 2 (s03): Hombres plantando pasto en la arena (Oregón, 1957)
# ===========================================================================
def scene_planting_grass(t):
    t0 = TL.s("s03")
    cv = bg("bg_grass_planting_1957").copy()
    d = ImageDraw.Draw(cv)
    draw_sand_wind(cv, t, density=38, color=(238, 212, 158), y_min=110, y_max=262)

    # Hileras de pasto europeo plantadas progresivamente en el suelo
    u = clamp01((t - t0) / max(1.0, TL.e("s03") - t0))
    n_tufts = int(3 + u * 9)
    for i in range(n_tufts):
        gx = 56 + i * 24
        gy = 252 + (i % 2) * 5
        for blade in (-4, -1, 2, 5):
            sway = int(round(math.sin(t * 4.0 + i) * 2))
            d.line([(gx, gy), (gx + blade + sway, gy - 11)], fill=(68, 156, 78, 255), width=2)

    # Dos trabajadores del Departamento de Agricultura plantando pasto en el piso (feet=258)
    char(cv, USDA_WORKER_1, 108, 258, t, scale=2, arms="work", look=1, mood="focused")
    char(cv, USDA_WORKER_2, 196, 258, t, scale=2, arms="point", look=1, mood="neutral")

    # Frank Herbert de pie a la derecha tomando apuntes en su libreta (feet=258)
    char(cv, HERBERT, 344, 258, t, scale=2, arms="note", look=-1, talk=talk_v(t, True))
    robot(cv, 424, 258, t, face="question", scale=1)

    # Ondulación bajo la arena debajo de los pies
    draw_sand_ripple(cv, t, y_base=263, x_start=40, x_end=440, progress=u)

    # Placa superior
    window(cv, 20, 10, 440, 36, fill=(14, 24, 34), border=GOLD, alpha=0.94)
    draw_text(cv, "FLORENCE, OREGÓN · PROYECTO DEL DEPTO. DE AGRICULTURA", 240, 16, "silk", 8, CYAN, align="center")
    draw_text(cv, "FRENAR LAS DUNAS PLANTANDO PASTO", 240, 30, "press", 8, GOLD, align="center")

    return cv


# ===========================================================================
# ESCENA 3 (s04, s05): La máquina de escribir y las notas que se vuelven novela
# ===========================================================================
def scene_typewriter_notes(t):
    t0 = TL.s("s04")
    t5 = TL.s("s05")
    cv = bg("bg_herbert_study_1960").copy()
    d = ImageDraw.Draw(cv)

    # Encabezado superior
    window(cv, 20, 10, 440, 36, fill=(24, 18, 12), border=GOLD, alpha=0.95)
    if t < t5:
        draw_text(cv, "EL ARTÍCULO PERIODÍSTICO: «STOPPING THE MOVING SANDS»", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "NUNCA LO TERMINÓ", 240, 30, "press", 8, RED, align="center")
    else:
        draw_text(cv, "DE UN ARTÍCULO INCONCLUSO A UNA OBRA MONUMENTAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA NOVELA DE CIENCIA FICCIÓN MÁS VENDIDA", 240, 30, "press", 8, GOLD, align="center")

    # Frank Herbert en su estudio (feet=260)
    char(cv, HERBERT, 108, 260, t, scale=2, arms="point" if t >= t5 else "cross", look=1, talk=talk_v(t, True))
    robot(cv, 46, 260, t, face="excited" if t >= t5 else "surprised", scale=1)

    # Tarjeta central: Hoja de máquina de escribir (s04) -> Pila de notas y novela Dune (s05)
    window(cv, 168, 56, 290, 162, fill=(28, 22, 16), border=GOLD, alpha=0.95)
    draw_paper(cv, 182, 68, 122, 136, color=(244, 236, 212))
    draw_text(cv, "OREGON DUNES", 243, 78, "press", 8, INK, align="center", outline=False)
    for row in range(5):
        d.line([(192, 96 + row * 10), (290 - (row % 2) * 18, 96 + row * 10)], fill=(70, 62, 52, 255), width=2)
    # Sello rojo INCOMPLETO
    window(cv, 190, 154, 106, 24, fill=(140, 28, 28), border=RED, alpha=0.96)
    draw_text(cv, "SIN TERMINAR", 243, 162, "press", 8, CREAM, align="center")

    if t >= t5:
        u5 = clamp01((t - t5) / max(1.0, TL.e("s05") - t5))
        # Carpetas amarillas creciendo y libro dorado DUNE a la derecha
        n_folders = int(2 + u5 * 8)
        for k in range(n_folders):
            fy = 192 - k * 7
            d.rectangle([318, fy, 442, fy + 6], fill=(238, 198, 96, 255), outline=(*INK, 255))
        window(cv, 318, 68, 126, 66, fill=(44, 26, 12), border=GOLD, alpha=0.98)
        draw_text(cv, "DUNE", 381, 78, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "Nº 1 EN VENTAS", 381, 102, "silk", 8, CREAM, align="center")
        draw_text(cv, "CIENCIA FICCIÓN", 381, 116, "silk", 8, CYAN, align="center")

    # La ondulación bajo la arena cruza la parte inferior del estudio
    draw_sand_ripple(cv, t, y_base=254, x_start=150, x_end=456)
    return cv


# ===========================================================================
# ESCENA 4 (s06, s07): Split 1957 / 2026 + Placa de Título Principal
# ===========================================================================
def scene_title_card(t):
    t6 = TL.s("s06")
    t7 = TL.s("s07")

    if t < t7 - 0.15:
        # Pantalla dividida: Oregón 1957 (izquierda) vs Sala de cine IMAX 2026 (derecha)
        bg_left = bg("bg_oregon_dunes_1957").copy()
        bg_right = bg("bg_imax_2026").copy()
        cv = new_canvas(INK)
        cv.paste(bg_left.crop((0, 0, 240, H)), (0, 0))
        cv.paste(bg_right.crop((240, 0, W, H)), (240, 0))
        d = ImageDraw.Draw(cv)
        d.line([(240, 0), (240, H)], fill=(*GOLD, 255), width=3)

        window(cv, 16, 14, 208, 34, fill=(14, 24, 34), border=CYAN, alpha=0.94)
        draw_text(cv, "1957 · OREGÓN", 120, 20, "press", 8, CYAN, align="center")
        draw_text(cv, "UN ARTÍCULO SIN TERMINAR", 120, 34, "silk", 8, CREAM, align="center")

        window(cv, 256, 14, 208, 34, fill=(32, 18, 10), border=GOLD, alpha=0.94)
        draw_text(cv, "2026 · EN CINES", 360, 20, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MESÍAS DE DUNE", 360, 34, "silk", 8, CREAM, align="center")

        window(cv, 44, 206, 392, 46, fill=(16, 14, 28), border=GOLD, alpha=0.95)
        draw_text(cv, "CASI 70 AÑOS DESPUÉS", 240, 214, "press", 8, GOLD, align="center")
        draw_text(cv, "EL CAPÍTULO QUE SUS LECTORES NO QUISIERON VER", 240, 232, "silk", 8, CREAM, align="center")

        draw_sand_ripple(cv, t, y_base=196, x_start=20, x_end=460)
        return cv

    # Tarjeta de Título Principal (s07: "Esta es la historia de Dune.")
    cv = bg("bg_wadi_rum_2019").copy()
    cv = grade(cv, mul=(0.85, 0.78, 0.68), add=(12, 6, 0), sat=1.1, k=0.85)
    draw_sand_wind(cv, t, density=48, color=(248, 214, 142))

    window(cv, 24, 42, 432, 168, fill=(20, 14, 10), border=GOLD, alpha=0.95)
    draw_text(cv, "PIXELOIDE STUDIOS PRESENTA", 240, 56, "silk", 8, CYAN, align="center")
    draw_text(cv, "LA ARENA QUE NUNCA", 240, 78, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, "SE DETUVO", 240, 102, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2)
    draw_text(cv, "LA HISTORIA DE DUNE", 240, 134, "press", 8, CREAM, align="center")
    draw_text(cv, "1957 → 2026", 240, 154, "press", 16, GOLD, align="center", outline_w=2)

    u_rip = clamp01((t - t7) / max(0.8, TL.e("s07") - t7))
    draw_sand_ripple(cv, t, y_base=192, x_start=44, x_end=436, progress=u_rip)
    robot(cv, 240, 260, t, face="excited", scale=1)
    return cv


# ===========================================================================
# ESCENA 5 (c1_01, c1_02, c1_03): Seis años de investigación y Arrakis
# ===========================================================================
def scene_six_years_study(t):
    t1 = TL.s("c1_01")
    t2 = TL.s("c1_02")
    t3 = TL.s("c1_03")
    cv = bg("bg_herbert_study_1960").copy()
    d = ImageDraw.Draw(cv)

    # Placa superior
    window(cv, 16, 10, 448, 34, fill=(24, 18, 12), border=GOLD, alpha=0.94)
    if t < t2:
        draw_text(cv, "FRANK HERBERT · PERIODISTA Y ESCRITOR", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "LA ARENA SE MOVÍA COMO UN MAR MUY LENTO", 240, 29, "silk", 8, CYAN, align="center")
    elif t < t3:
        draw_text(cv, "6 AÑOS DE INVESTIGACIÓN Y ESCRITURA (1959 - 1965)", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DESIERTOS · ECOLOGÍA · RELIGIÓN · PODER", 240, 29, "silk", 8, CYAN, align="center")
    else:
        draw_text(cv, "NACE UN PLANETA DESIERTO: ARRAKIS", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DONDE EL AGUA VALE MÁS QUE CUALQUIER RIQUEZA", 240, 29, "silk", 8, CYAN, align="center")

    # Frank Herbert en su estudio (feet=260)
    char(cv, HERBERT, 96, 260, t, scale=2, arms="note" if t < t3 else "point", look=1, talk=talk_v(t, True))
    robot(cv, 38, 260, t, face="question" if t < t3 else "surprised", scale=1)

    if t < t3:
        # Los 4 pilares temáticos de Dune en cajas limpias
        pillars = [
            ("DESIERTOS", (238, 186, 92)),
            ("ECOLOGÍA", (98, 214, 132)),
            ("RELIGIÓN", (196, 148, 245)),
            ("PODER", (245, 112, 102)),
        ]
        for idx, (label, col) in enumerate(pillars):
            px = 164 + (idx % 2) * 150
            py = 62 + (idx // 2) * 58
            window(cv, px, py, 140, 46, fill=(28, 22, 18), border=col, alpha=0.94)
            draw_text(cv, f"PILAR {idx + 1}", px + 70, py + 10, "silk", 8, col, align="center")
            draw_text(cv, label, px + 70, py + 24, "press", 8, CREAM, align="center")

        window(cv, 164, 182, 290, 32, fill=(36, 26, 16), border=GOLD, alpha=0.95)
        draw_text(cv, "6 AÑOS ESCRIBIENDO · 1959 → 1965", 309, 194, "press", 8, GOLD, align="center")
    else:
        # Proyección del planeta desierto y una gota de agua preciosa
        window(cv, 164, 56, 292, 160, fill=(20, 16, 24), border=GOLD, alpha=0.95)
        # Planeta ocre a la izquierda del panel
        pcx, pcy, pr = 236, 134, 42
        d.ellipse([pcx - pr - 4, pcy - pr - 4, pcx + pr + 4, pcy + pr + 4], fill=(240, 175, 75, 55))
        d.ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=(214, 138, 54, 255), outline=(*GOLD, 255), width=2)
        for band in (-18, -6, 8, 20):
            d.line([(pcx - pr + 8, pcy + band), (pcx + pr - 8, pcy + band)], fill=(176, 98, 34, 255), width=2)
        # Dos lunas pequeñas
        d.ellipse([pcx + 44, pcy - 38, pcx + 54, pcy - 28], fill=(242, 232, 200, 255))
        d.ellipse([pcx - 54, pcy + 22, pcx - 46, pcy + 30], fill=(210, 220, 235, 255))

        # Gota de agua azul brillante a la derecha del panel
        wcx, wcy = 376, 118
        d.polygon([(wcx, wcy - 22), (wcx - 16, wcy + 4), (wcx + 16, wcy + 4)], fill=(72, 195, 255, 255))
        d.ellipse([wcx - 16, wcy - 6, wcx + 16, wcy + 22], fill=(72, 195, 255, 255), outline=(210, 245, 255, 255))
        draw_text(cv, "EL AGUA", 376, 152, "press", 8, CYAN, align="center")
        draw_text(cv, "TESORO SUPREMO", 376, 168, "silk", 8, CREAM, align="center")
        draw_text(cv, "PLANETA DESIERTO", 236, 188, "silk", 8, GOLD, align="center")

    draw_sand_ripple(cv, t, y_base=255, x_start=150, x_end=456)
    return cv


# ===========================================================================
# ESCENA 6 (c1_04, c1_05): Kiosco de revistas (1963-1965) y el manuscrito
# ===========================================================================
def scene_newsstand_serial(t):
    t4 = TL.s("c1_04")
    t5 = TL.s("c1_05")
    cv = bg("bg_newsstand_1963").copy()
    d = ImageDraw.Draw(cv)

    # Placa superior
    window(cv, 16, 10, 448, 36, fill=(24, 18, 14), border=GOLD, alpha=0.95)
    if t < t5:
        draw_text(cv, "REVISTA ANALOG · 1963 A 1965", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "PUBLICADA PRIMERO POR ENTREGAS DE CIENCIA FICCIÓN", 240, 30, "silk", 8, CYAN, align="center")
    else:
        draw_text(cv, "1965 · EL GRAN DESAFÍO EDITORIAL", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "FALTABA LO DIFÍCIL: CONVERTIRLA EN LIBRO", 240, 30, "silk", 8, CREAM, align="center")

    # Tres ejemplares de revista en exhibición (1963, 1964, 1965)
    years_mag = [("1963", "PARTE 1"), ("1964", "PARTE 2"), ("1965", "PARTE 3")]
    for idx, (yr, pt_lbl) in enumerate(years_mag):
        mx = 136 + idx * 74
        my = 60
        window(cv, mx, my, 64, 84, fill=(196, 88, 34), border=GOLD, alpha=0.96)
        draw_text(cv, "ANALOG", mx + 32, my + 8, "silk", 8, CREAM, align="center")
        # Duna ilustrada en la tapa
        d.polygon([(mx + 6, my + 54), (mx + 26, my + 34), (mx + 58, my + 54)], fill=(238, 182, 82, 255))
        draw_text(cv, yr, mx + 32, my + 58, "press", 8, GOLD, align="center")
        draw_text(cv, pt_lbl, mx + 32, my + 70, "silk", 8, CYAN, align="center")

    # Personajes en la vereda del kiosco (feet=260)
    char(cv, HERBERT, 82, 260, t, scale=2, arms="point", look=1, talk=talk_v(t, True))
    char(cv, READER_1, 376, 260, t, scale=2, arms="note", look=-1, mood="happy")
    char(cv, READER_2, 434, 260, t, scale=2, arms="hips", look=-1, mood="happy")
    robot(cv, 30, 260, t, face="happy" if t < t5 else "question", scale=1)

    if t >= t5:
        # Gran bloque del manuscrito buscando editorial
        window(cv, 136, 154, 212, 54, fill=(32, 22, 16), border=RED, alpha=0.96)
        draw_text(cv, "MANUSCRITO COMPLETO", 242, 164, "silk", 8, CYAN, align="center")
        draw_text(cv, "¿QUIÉN PUBLICA ESTO?", 242, 180, "press", 8, GOLD, align="center")

    draw_sand_ripple(cv, t, y_base=262, x_start=30, x_end=450)
    return cv


def scenes():
    return [
        (0.0, scene_oregon_flight),
        (TL.s("s03") - 0.15, scene_planting_grass),
        (TL.s("s04") - 0.15, scene_typewriter_notes),
        (TL.s("s06") - 0.15, scene_title_card),
        (TL.chapter_start(1) - 0.3, make_card(1, ["EL ARTÍCULO QUE", "NUNCA TERMINÓ"], "1957 - 1965 · DE OREGÓN A LA REVISTA")),
        (TL.s("c1_01") - 0.15, scene_six_years_study),
        (TL.s("c1_04") - 0.15, scene_newsstand_serial),
    ]
