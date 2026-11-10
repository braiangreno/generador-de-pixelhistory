"""Apertura (s01..s07) + Capítulo 1: El artículo que nunca terminó (c1_00..c1_05)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa

# Cast de sprites para Dune
HERBERT = {
    "name": "Frank Herbert",
    "skin": (235, 192, 152), "hair": (110, 74, 46), "hair_style": "parted",
    "beard": (105, 70, 42), "glasses": True,
    "shirt": (236, 226, 200), "jacket": (132, 96, 62),
    "tie": (158, 62, 44), "pants": (68, 56, 46),
}
USDA_WORKER_1 = {
    "name": "USDA Worker 1",
    "skin": (228, 182, 144), "hair": (70, 52, 38), "hair_style": "short",
    "shirt": (196, 178, 132), "jacket": (76, 112, 68),
    "pants": (62, 78, 54),
}
USDA_WORKER_2 = {
    "name": "USDA Worker 2",
    "skin": (214, 166, 128), "hair": (50, 40, 32), "hair_style": "short",
    "shirt": (210, 194, 150), "jacket": (88, 124, 76),
    "pants": (58, 74, 52),
}
READER_1 = {
    "name": "Reader 1",
    "skin": (236, 194, 158), "hair": (64, 44, 32), "hair_style": "parted",
    "shirt": (220, 230, 245), "jacket": (54, 82, 134),
    "pants": (46, 54, 76),
}
READER_2 = {
    "name": "Reader 2",
    "skin": (224, 178, 142), "hair": (148, 72, 42), "hair_style": "long",
    "shirt": (244, 214, 168), "jacket": (164, 88, 52),
    "pants": (64, 52, 48),
}


def _draw_biplane(cv, cx, cy, t):
    """Avioneta de los años 50 sobrevolando las dunas de Oregón con estela de aire."""
    d = ImageDraw.Draw(cv)
    by = cy + int(round(math.sin(t * 5.2) * 3))
    # Estela de viento detrás de la avioneta
    for k in range(3):
        sx = cx - 28 - k * 14 - int((t * 45) % 12)
        sy = by - 2 + (k - 1) * 4
        d.line([(sx, sy), (sx + 8, sy)], fill=(255, 244, 210, 150 - k * 40), width=1)
    # Fuselaje amarillo/crema con franja roja
    d.rectangle([cx - 22, by - 4, cx + 16, by + 4], fill=(242, 202, 78, 255), outline=(*INK, 255))
    d.line([(cx - 20, by + 1), (cx + 14, by + 1)], fill=(208, 62, 48, 255), width=2)
    # Cola
    d.polygon([(cx - 22, by - 4), (cx - 30, by - 12), (cx - 16, by - 4)], fill=(208, 62, 48, 255), outline=(*INK, 255))
    # Ala superior
    d.rectangle([cx - 12, by - 8, cx + 10, by - 5], fill=(248, 232, 170, 255), outline=(*INK, 255))
    # Cabina
    d.rectangle([cx - 4, by - 4, cx + 6, by - 1], fill=(130, 205, 245, 255), outline=(*INK, 255))
    # Hélice girando rápido
    ph = int(t * 30) % 2
    if ph == 0:
        d.line([(cx + 18, by - 8), (cx + 18, by + 8)], fill=(220, 230, 240, 235), width=2)
    else:
        d.line([(cx + 18, by - 4), (cx + 18, by + 4)], fill=(180, 195, 210, 210), width=2)


# ===========================================================================
# ESCENA 1 (s01, s02): 1957. Florence, Oregón — Vuelo sobre las dunas
# ===========================================================================
def scene_oregon_flight(t):
    t0 = TL.s("s01")
    t2 = TL.s("s02")
    dt = max(0.0, t - t0)

    cv = bg("bg_oregon_dunes_1957").copy()
    d = ImageDraw.Draw(cv)
    draw_sand_wind(cv, t, density=46, color=(236, 210, 155), y_min=85, y_max=262)

    # Avioneta cruzando el cielo con banqueo dinámico y cámara aérea
    u_flight = clamp01((t - t0) / max(1.0, TL.e("s02") - t0))
    px = int(60 + u_flight * 340)
    py = 66 + int(round(math.sin(t * 2.8) * 6))
    _draw_biplane(cv, px, py, t)

    # Líneas de avance de las dunas hacia el bosque (flechas tácticas animadas)
    for idx, ay in enumerate((198, 218, 238)):
        ax = 160 + idx * 45 + int((t * 36) % 28)
        d.line([(ax, ay), (ax + 22, ay)], fill=(*GOLD, 210), width=2)
        d.polygon([(ax + 22, ay - 3), (ax + 28, ay), (ax + 22, ay + 3)], fill=(*GOLD, 230))

    # Encabezado superior con reveal progresivo
    a_top, dy_top = pop(t, t0 + 0.05)
    window(cv, 20, 10 + dy_top, 440, 36, fill=(14, 22, 36), border=GOLD, alpha=0.94 * a_top)
    draw_text(cv, "1957 · FLORENCE, OREGÓN", 240, 16 + dy_top, "press", 8, GOLD, align="center", reveal=(t - t0) * 28)
    draw_text(cv, "DUNAS QUE AVANZAN SOBRE RUTAS, BOSQUES Y CASAS", 240, 30 + dy_top, "silk", 8, CYAN, align="center",
              reveal=(t - t0 - 0.35) * 36)

    # En el suelo: dos trabajadores observan las dunas; señalan cuando el audio dice "rutas, bosques y casas"
    t_rutas = TL.word("s02", "rutas")
    t_casas = TL.word("s02", "casas")
    w1_arms = "point" if t >= t_rutas else "hips"
    w2_arms = "shrug" if t >= t_casas else ("point" if t >= t_rutas else "hold")
    char(cv, USDA_WORKER_1, 316, 258, t, scale=2, arms=w1_arms, look=1, mood="worried")
    char(cv, USDA_WORKER_2, 388, 258, t, scale=2, arms=w2_arms, look=-1, mood="focused")

    # Recuadro inferior: Frank Herbert tomando notas desde el avión (con entrada pop)
    if t >= t2 - 0.15:
        a_box, dy_box = pop(t, t2 - 0.15)
        window(cv, 18, 184 + dy_box, 236, 72, fill=(16, 22, 36), border=CREAM, alpha=0.95 * a_box)
        portrait(cv, "herbert", 26, 192 + dy_box, 56)
        draw_text(cv, "FRANK HERBERT", 92, 194 + dy_box, "press", 8, GOLD)
        draw_text(cv, "PERIODISTA EN VUELO", 92, 208 + dy_box, "silk", 8, CYAN)
        draw_text(cv, "«UN MAR DE ARENA EN", 92, 224 + dy_box, "silk", 8, CREAM, reveal=(t - t2) * 26)
        draw_text(cv, "MOVIMIENTO...»", 92, 236 + dy_box, "silk", 8, CREAM, reveal=(t - t2 - 0.4) * 26)

    return cv


# ===========================================================================
# ESCENA 2 (s03): Hombres plantando pasto en la arena (Oregón, 1957)
# ===========================================================================
def scene_planting_grass(t):
    t0 = TL.s("s03")
    cv = bg("bg_grass_planting_1957").copy()
    d = ImageDraw.Draw(cv)
    draw_sand_wind(cv, t, density=42, color=(238, 212, 158), y_min=110, y_max=262)

    u = clamp01((t - t0) / max(1.0, TL.e("s03") - t0))

    t_hombres = TL.word("s03", "hombres")
    t_frenar = TL.word("s03", "frenarlas")
    t_pasto = TL.word("s03", "pasto")

    # Hileras de pasto europeo que brotan cuando el narrador menciona "frenarlas... con pasto"
    u_grass = clamp01((t - t_hombres) / max(0.6, TL.e("s03") - t_hombres))
    n_tufts = int(2 + u_grass * 11)
    for i in range(n_tufts):
        gx = 48 + i * 24
        gy = 252 + (i % 2) * 5
        for blade in (-4, -1, 2, 5):
            sway = int(round(math.sin(t * 4.2 + i) * 2.0))
            d.line([(gx, gy), (gx + blade + sway, gy - 12)], fill=(68, 166, 78, 255), width=2)

    # Los trabajadores avanzan un paso al decir "hombres" y plantan pasto al decir "frenarlas... con pasto"
    w1_x, w1_ph = walk(t, t_hombres - 0.1, t_hombres + 0.75, 92, 132)
    w2_x, w2_ph = walk(t, t_hombres, t_hombres + 0.85, 188, 232)
    char(cv, USDA_WORKER_1, w1_x, 258, t, scale=2, walk=w1_ph,
         arms="work" if t >= t_frenar else "hold", look=1, mood="focused")
    char(cv, USDA_WORKER_2, w2_x, 258, t, scale=2, walk=w2_ph,
         arms="point" if t >= t_pasto else ("work" if t >= t_hombres else "hips"), look=1, mood="happy")

    # Frank Herbert entra al inicio ("Vino a escribir un artículo") y toma notas en su libreta
    hx, hph = walk(t, t0, t0 + 0.95, 436, 378)
    char(cv, HERBERT, hx, 258, t, scale=2, walk=hph,
         arms="note" if hph is None else "hold", look=-1)

    # Placa superior con pop
    a_w, dy_w = pop(t, t0)
    window(cv, 20, 10 + dy_w, 440, 36, fill=(14, 24, 34), border=GOLD, alpha=0.94 * a_w)
    draw_text(cv, "FLORENCE, OREGÓN · PROYECTO DEL DEPTO. DE AGRICULTURA", 240, 16 + dy_w, "silk", 8, CYAN, align="center")
    draw_text(cv, "FRENAR LAS DUNAS PLANTANDO PASTO", 240, 30 + dy_w, "press", 8, GOLD, align="center",
              reveal=(t - t0 - 0.15) * 28)

    return cv


# ===========================================================================
# ESCENA 3 (s04, s05): La máquina de escribir y las notas que se vuelven novela
# ===========================================================================
def scene_typewriter_notes(t):
    t0 = TL.s("s04")
    t5 = TL.s("s05")
    dx, dy = shake(t, t0 + 1.1, dur=0.28, amp=3)
    cv = bg("bg_herbert_study_1960").copy()
    d = ImageDraw.Draw(cv)

    # Encabezado superior
    window(cv, 20, 10, 440, 36, fill=(24, 18, 12), border=GOLD, alpha=0.95)
    if t < t5:
        draw_text(cv, "EL ARTÍCULO PERIODÍSTICO: «STOPPING THE MOVING SANDS»", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "NUNCA LO TERMINÓ", 240, 30, "press", 8, RED, align="center", reveal=(t - t0 - 0.4) * 26)
    else:
        draw_text(cv, "DE UN ARTÍCULO INCONCLUSO A UNA OBRA MONUMENTAL", 240, 16, "silk", 8, CYAN, align="center")
        draw_text(cv, "LA NOVELA DE CIENCIA FICCIÓN MÁS VENDIDA", 240, 30, "press", 8, GOLD, align="center",
                  reveal=(t - t5) * 30)

    # Frank Herbert en su estudio: se detiene al decir "Nunca lo terminó", toma notas en "Las notas siguieron creciendo" y señala la novela en "novelas"
    t_termino = TL.word("s04", "termino")
    t_novelas = TL.word("s05", "novelas")
    t_vendidas = TL.word("s05", "vendidas")
    if t < t5:
        h_arms = "shrug" if t >= t_termino else "type"
        char(cv, HERBERT, 96, 260, t, scale=2, arms=h_arms, look=1, mood="worried" if t >= t_termino else "focused")
    else:
        h_arms = "cheer" if t >= t_vendidas else ("point" if t >= t_novelas else "note")
        char(cv, HERBERT, 96, 260, t, scale=2, arms=h_arms, look=1, mood="happy")

    # Tarjeta central: Hoja de máquina de escribir (s04) -> Pila de notas y novela Dune (s05)
    window(cv, 168, 56, 290, 162, fill=(28, 22, 16), border=GOLD, alpha=0.95)
    draw_paper(cv, 182, 68, 122, 136, color=(244, 236, 212))
    draw_text(cv, "OREGON DUNES", 243, 78, "press", 8, INK, align="center", outline=False)

    # Líneas tipeándose en vivo
    u_type = clamp01((t - t0) / 1.1)
    n_lines = int(1 + u_type * 4)
    for row in range(n_lines):
        d.line([(192, 96 + row * 10), (290 - (row % 2) * 18, 96 + row * 10)], fill=(70, 62, 52, 255), width=2)

    # Sello rojo INCOMPLETO que cae con golpe
    if t >= t0 + 1.0:
        a_st, dy_st = pop(t, t0 + 1.0, dur=0.25)
        window(cv, 190, 154 + dy_st, 106, 24, fill=(140, 28, 28), border=RED, alpha=0.96 * a_st)
        draw_text(cv, "SIN TERMINAR", 243, 162 + dy_st, "press", 8, CREAM, align="center")

    if t >= t5:
        u5 = clamp01((t - t5) / max(1.0, TL.e("s05") - t5))
        # Carpetas amarillas apilándose rápidamente y libro dorado DUNE brillando a la derecha
        n_folders = int(2 + u5 * 10)
        for k in range(n_folders):
            fy = 196 - k * 6
            d.rectangle([318, fy, 442, fy + 5], fill=(238, 198, 96, 255), outline=(*INK, 255))
        a_bk, dy_bk = pop(t, t5 + 0.25)
        window(cv, 318, 68 + dy_bk, 126, 66, fill=(44, 26, 12), border=GOLD, alpha=0.98 * a_bk)
        draw_text(cv, "DUNE", 381, 78 + dy_bk, "press", 16, GOLD, align="center", outline_w=2)
        draw_text(cv, "Nº 1 EN VENTAS", 381, 102 + dy_bk, "silk", 8, CREAM, align="center")
        draw_text(cv, "CIENCIA FICCIÓN", 381, 116 + dy_bk, "silk", 8, CYAN, align="center")
        sparkle(cv, 330, 76 + dy_bk, t, 3)
        sparkle(cv, 432, 82 + dy_bk, t + 1.1, 3)

    return offset_canvas(cv, dx, dy)


# ===========================================================================
# ESCENA 4 (s06, s07): Split 1957 / 2026 + Placa de Título Principal
# ===========================================================================
def scene_title_card(t):
    t6 = TL.s("s06")
    t7 = TL.s("s07")

    if t < t7 - 0.15:
        # Pantalla dividida dinámica: Oregón 1957 (izquierda) vs Sala de cine IMAX 2026 (derecha)
        bg_left = bg("bg_oregon_dunes_1957").copy()
        bg_right = bg("bg_imax_2026").copy()
        cv = new_canvas(INK)
        cv.paste(bg_left.crop((0, 0, 240, H)), (0, 0))
        cv.paste(bg_right.crop((240, 0, W, H)), (240, 0))
        d = ImageDraw.Draw(cv)
        d.line([(240, 0), (240, H)], fill=(*GOLD, 255), width=3)

        # Izquierda: Herbert en Oregón 1957 tomando notas
        hx, hph = walk(t, t6, t6 + 1.2, 40, 110)
        char(cv, HERBERT, hx, 252, t, scale=2, walk=hph, arms="note", look=1, talk=talk_v(t, True))
        # Derecha: Espectadores de 2026 entrando a la sala IMAX
        r1x, r1ph = walk(t, t6 + 0.3, t6 + 1.5, 430, 330)
        r2x, r2ph = walk(t, t6 + 0.5, t6 + 1.7, 460, 390)
        char(cv, READER_1, r1x, 252, t, scale=2, walk=r1ph, arms="cheer", look=-1, mood="happy")
        char(cv, READER_2, r2x, 252, t, scale=2, walk=r2ph, arms="point_l", look=-1, mood="happy")

        a1, dy1 = pop(t, t6 + 0.05)
        window(cv, 16, 14 + dy1, 208, 34, fill=(14, 24, 34), border=CYAN, alpha=0.94 * a1)
        draw_text(cv, "1957 · OREGÓN", 120, 20 + dy1, "press", 8, CYAN, align="center")
        draw_text(cv, "UN ARTÍCULO SIN TERMINAR", 120, 34 + dy1, "silk", 8, CREAM, align="center")

        a2, dy2 = pop(t, t6 + 0.35)
        window(cv, 256, 14 + dy2, 208, 34, fill=(32, 18, 10), border=GOLD, alpha=0.94 * a2)
        draw_text(cv, "2026 · EN CINES", 360, 20 + dy2, "press", 8, GOLD, align="center")
        draw_text(cv, "EL MESÍAS DE DUNE", 360, 34 + dy2, "silk", 8, CREAM, align="center")

        a3, dy3 = pop(t, t6 + 0.75)
        window(cv, 44, 206 + dy3, 392, 46, fill=(16, 14, 28), border=GOLD, alpha=0.95 * a3)
        draw_text(cv, "CASI 70 AÑOS DESPUÉS", 240, 214 + dy3, "press", 8, GOLD, align="center")
        draw_text(cv, "EL CAPÍTULO QUE SUS LECTORES NO QUISIERON VER", 240, 232 + dy3, "silk", 8, CREAM, align="center",
                  reveal=(t - t6 - 0.85) * 32)
        return cv

    # Tarjeta de Título Principal (s07: "Esta es la historia de Dune.")
    cv = bg("bg_wadi_rum_2019").copy()
    cv = grade(cv, mul=(0.85, 0.78, 0.68), add=(12, 6, 0), sat=1.1, k=0.85)
    draw_sand_wind(cv, t, density=52, color=(248, 214, 142))

    a_t, dy_t = pop(t, t7 - 0.1)
    window(cv, 24, 42 + dy_t, 432, 168, fill=(20, 14, 10), border=GOLD, alpha=0.95 * a_t)
    draw_text(cv, "PIXELOIDE STUDIOS PRESENTA", 240, 56 + dy_t, "silk", 8, CYAN, align="center")
    draw_text(cv, "LA ARENA QUE NUNCA", 240, 78 + dy_t, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2,
              reveal=(t - t7 + 0.1) * 24)
    draw_text(cv, "SE DETUVO", 240, 102 + dy_t, "press", 16, align="center", gradient=GOLD_RAMP, outline_w=2,
              reveal=(t - t7 - 0.25) * 24)
    draw_text(cv, "LA HISTORIA DE DUNE", 240, 134 + dy_t, "press", 8, CREAM, align="center")
    draw_text(cv, "1957 → 2026", 240, 154 + dy_t, "press", 16, GOLD, align="center", outline_w=2)
    sparkle(cv, 104, 86 + dy_t, t, 3)
    sparkle(cv, 376, 108 + dy_t, t + 1.4, 3)
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
        draw_text(cv, "LA ARENA SE MOVÍA COMO UN MAR MUY LENTO", 240, 29, "silk", 8, CYAN, align="center",
                  reveal=(t - t1) * 30)
    elif t < t3:
        draw_text(cv, "6 AÑOS DE INVESTIGACIÓN Y ESCRITURA (1959 - 1965)", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DESIERTOS · ECOLOGÍA · RELIGIÓN · PODER", 240, 29, "silk", 8, CYAN, align="center",
                  reveal=(t - t2) * 30)
    else:
        draw_text(cv, "NACE UN PLANETA DESIERTO: ARRAKIS", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "DONDE EL AGUA VALE MÁS QUE CUALQUIER RIQUEZA", 240, 29, "silk", 8, CYAN, align="center",
                  reveal=(t - t3) * 30)

    # Frank Herbert en su estudio: escribe en "escribía cuentos", piensa en "vio algo", lee en "Empezó a leer", tipea en "Pasó seis años escribiendo" y señala el planeta en c1_03
    t_vio = TL.word("c1_01", "vio")
    t_escribiendo = TL.word("c1_02", "escribiendo")
    hx, hph = walk(t, t1, t1 + 0.9, 48, 96)
    if t < t2:
        h_arms = "think" if t >= t_vio else "write"
    elif t < t3:
        h_arms = "type" if t >= t_escribiendo else "note"
    else:
        h_arms = "point"
    char(cv, HERBERT, hx, 260, t, scale=2, walk=hph,
         arms=h_arms, look=1, mood="happy" if t >= t3 else "focused")

    if t < t3:
        # Los 4 pilares temáticos aparecen sincronizados con cada palabra del audio
        pillars = [
            ("DESIERTOS", (238, 186, 92), TL.word("c1_02", "desiertos")),
            ("ECOLOGÍA", (98, 214, 132), TL.word("c1_02", "ecologia")),
            ("RELIGIÓN", (196, 148, 245), TL.word("c1_02", "religion")),
            ("PODER", (245, 112, 102), TL.word("c1_02", "poder")),
        ]
        for idx, (label, col, t_appear) in enumerate(pillars):
            if t >= t_appear:
                ap, dyp = pop(t, t_appear)
                px = 164 + (idx % 2) * 150
                py = 62 + (idx // 2) * 58 + dyp
                window(cv, px, py, 140, 46, fill=(28, 22, 18), border=col, alpha=0.95 * ap)
                draw_text(cv, f"PILAR {idx + 1}", px + 70, py + 10, "silk", 8, col, align="center")
                draw_text(cv, label, px + 70, py + 24, "press", 8, CREAM, align="center")

        if t >= t_escribiendo - 0.1:
            ab, dyb = pop(t, t_escribiendo - 0.1)
            window(cv, 164, 182 + dyb, 290, 32, fill=(36, 26, 16), border=GOLD, alpha=0.95 * ab)
            draw_text(cv, "6 AÑOS ESCRIBIENDO · 1959 → 1965", 309, 194 + dyb, "press", 8, GOLD, align="center")
    else:
        # Proyección animada del planeta desierto rotando y la gota de agua
        ap, dyp = pop(t, t3)
        window(cv, 164, 56 + dyp, 292, 160, fill=(20, 16, 24), border=GOLD, alpha=0.95 * ap)
        pcx, pcy, pr = 236, 134 + dyp, 42
        d.ellipse([pcx - pr - 4, pcy - pr - 4, pcx + pr + 4, pcy + pr + 4], fill=(240, 175, 75, 55))
        d.ellipse([pcx - pr, pcy - pr, pcx + pr, pcy + pr], fill=(214, 138, 54, 255), outline=(*GOLD, 255), width=2)
        for band in (-18, -6, 8, 20):
            shift = int(round(math.sin(t * 2.5 + band) * 4))
            d.line([(pcx - pr + 8 + shift, pcy + band), (pcx + pr - 8 + shift, pcy + band)], fill=(176, 98, 34, 255), width=2)
        # Dos lunas orbitando suavemente
        m1_ang = t * 1.4
        m1x = pcx + int(math.cos(m1_ang) * 52)
        m1y = pcy - int(math.sin(m1_ang) * 36)
        d.ellipse([m1x - 5, m1y - 5, m1x + 5, m1y + 5], fill=(242, 232, 200, 255))
        d.ellipse([pcx - 54, pcy + 22, pcx - 46, pcy + 30], fill=(210, 220, 235, 255))

        # Gota de agua azul brillante pulsando a la derecha del panel
        wcx = 376
        wcy = 118 + dyp + int(round(math.sin(t * 4.0) * 3))
        d.polygon([(wcx, wcy - 22), (wcx - 16, wcy + 4), (wcx + 16, wcy + 4)], fill=(72, 195, 255, 255))
        d.ellipse([wcx - 16, wcy - 6, wcx + 16, wcy + 22], fill=(72, 195, 255, 255), outline=(210, 245, 255, 255))
        draw_text(cv, "EL AGUA", 376, 152 + dyp, "press", 8, CYAN, align="center")
        draw_text(cv, "TESORO SUPREMO", 376, 168 + dyp, "silk", 8, CREAM, align="center")
        draw_text(cv, "PLANETA DESIERTO", 236, 188 + dyp, "silk", 8, GOLD, align="center")

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
        draw_text(cv, "PUBLICADA PRIMERO POR ENTREGAS DE CIENCIA FICCIÓN", 240, 30, "silk", 8, CYAN, align="center",
                  reveal=(t - t4) * 30)
    else:
        draw_text(cv, "1965 · EL GRAN DESAFÍO EDITORIAL", 240, 16, "press", 8, GOLD, align="center")
        draw_text(cv, "FALTABA LO DIFÍCIL: CONVERTIRLA EN LIBRO", 240, 30, "silk", 8, CREAM, align="center",
                  reveal=(t - t5) * 30)

    # Tres ejemplares de revista que aparecen sincronizados con la narración
    years_mag = [
        ("1963", "PARTE 1", TL.word("c1_04", "entregas")),
        ("1964", "PARTE 2", TL.word("c1_04", "revista")),
        ("1965", "PARTE 3", TL.word("c1_04", "sesenta")),
    ]
    for idx, (yr, pt_lbl, t_mag) in enumerate(years_mag):
        if t >= t_mag:
            am, dym = pop(t, t_mag)
            mx = 136 + idx * 74
            my = 60 + dym
            window(cv, mx, my, 64, 84, fill=(196, 88, 34), border=GOLD, alpha=0.96 * am)
            draw_text(cv, "ANALOG", mx + 32, my + 8, "silk", 8, CREAM, align="center")
            d.polygon([(mx + 6, my + 54), (mx + 26, my + 34), (mx + 58, my + 54)], fill=(238, 182, 82, 255))
            draw_text(cv, yr, mx + 32, my + 58, "press", 8, GOLD, align="center")
            draw_text(cv, pt_lbl, mx + 32, my + 70, "silk", 8, CYAN, align="center")

    # Herbert presenta las entregas y en c1_05 sostiene el manuscrito ("Faltaba lo difícil: convertirla en libro")
    r1x, r1ph = walk(t, t4 + 0.2, t4 + 1.1, 438, 376)
    char(cv, HERBERT, 82, 260, t, scale=2,
         arms="point" if t < t5 else "shrug", look=1, mood="worried" if t >= t5 else "focused")
    char(cv, READER_1, r1x, 260, t, scale=2, walk=r1ph,
         arms="note" if r1ph is None else "down", look=-1, mood="happy")
    char(cv, READER_2, 428, 260, t, scale=2,
         arms="point_l" if t >= TL.word("c1_04", "revista") else "hips", look=-1, mood="happy")

    if t >= t5:
        ab, dyb = pop(t, t5)
        window(cv, 136, 154 + dyb, 212, 54, fill=(32, 22, 16), border=RED, alpha=0.96 * ab)
        draw_text(cv, "MANUSCRITO COMPLETO", 242, 164 + dyb, "silk", 8, CYAN, align="center")
        draw_text(cv, "¿QUIÉN PUBLICA ESTO?", 242, 180 + dyb, "press", 8, GOLD, align="center",
                  reveal=(t - t5 - 0.15) * 26)

    return cv


def scenes():
    return [
        (0.0, scene_oregon_flight, lambda t: cam_push(t, 0.0, TL.s("s03"), 1.0, 1.10, (240, 135), (225, 145))),
        (TL.s("s03") - 0.15, scene_planting_grass, lambda t: cam_push(t, TL.s("s03"), TL.s("s04"), 1.0, 1.08, (240, 145), (255, 155))),
        (TL.s("s04") - 0.15, scene_typewriter_notes, lambda t: (1.0 + cam_punch(t, [TL.s("s04") + 1.0, TL.s("s05") + 0.25], 0.06), 240, 140)),
        (TL.s("s06") - 0.15, scene_title_card, lambda t: (1.0 + cam_punch(t, [TL.s("s07")], 0.07), 240, 135)),
        (TL.chapter_start(1) - 0.3, make_card(1, ["EL ARTÍCULO QUE", "NUNCA TERMINÓ"], "1957 - 1965 · DE OREGÓN A LA REVISTA"), None),
        (TL.s("c1_01") - 0.15, scene_six_years_study, lambda t: cam_push(t, TL.s("c1_01"), TL.s("c1_04"), 1.0, 1.09, (240, 140), (260, 140))),
        (TL.s("c1_04") - 0.15, scene_newsstand_serial, lambda t: (1.0 + cam_punch(t, [TL.s("c1_05")], 0.06), 240, 145)),
    ]
