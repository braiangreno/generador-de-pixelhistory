"""Capítulo 8: Trece años (2017 – 2026) + cierre del documental."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *  # noqa

w = TL.word
CH = 8
T_CARD = TL.chapter_start(CH)
T_END = TL.e("c8_09") + 2.8

S1 = TL.s("c8_01") - 0.2     # 2017: Switch en el tren (casa y portátil)
S2 = TL.s("c8_02") - 0.2     # 157 M vs 160 M (Switch vs PS2)
S3 = TL.s("c8_03") - 0.2     # 2025: Switch 2 al amanecer (3,5 M en 4 días)
S4 = TL.s("c8_04") - 0.2     # 2025: Globo terráqueo US$ 201.600 millones
S5 = TL.s("c8_05") - 0.2     # GTA V +230 M (dither_mix de ciudad 2001 a costa neón 2026)
S6 = TL.s("c8_06") - 0.2     # Calendario con dos sellos rojos "POSTERGADO"
S7 = TL.s("c8_07") - 0.2     # 19 · 11 · 2026 / TRECE AÑOS DESPUÉS sobre el horizonte neón
S8 = TL.s("c8_08") - 0.2     # Match Cut: el sol neón se encoge hasta el punto de fósforo de 1958
S9 = TL.s("c8_09") - 0.2     # Pantalla negra, un único rebote ("plic") y título final

C = S.hexc

CAST_CH8 = {
    "viajera": dict(
        name="Viajera Switch", skin=S.SKIN["fair"], hair=C("5a3222"), hair_style="long",
        top="hoodie", top_color=C("386898"), pants=C("262a3a"),
    ),
    "fila_1": dict(
        name="Comprador 1", skin=S.SKIN["light"], hair=C("2c201a"), hair_style="fringe",
        top="hoodie", top_color=C("d8463e"), pants=C("283044"),
    ),
    "fila_2": dict(
        name="Compradora 2", skin=S.SKIN["tan"], hair=C("181416"), hair_style="bangs",
        top="sweater", top_color=C("28a8c8"), pants=C("242836"),
    ),
    "fila_3": dict(
        name="Comprador 3", skin=S.SKIN["olive"], hair=C("362820"), hair_style="short",
        glasses="black", top="tshirt", top_color=C("e8a838"), pants=C("2c3242"),
    ),
    "fila_4": dict(
        name="Compradora 4", skin=S.SKIN["brown"], hair=C("141012"), hair_style="curly",
        top="hoodie", top_color=C("6a4c9c"), pants=C("222634"),
    ),
}

SW_CYAN = (0, 195, 227)
SW_RED = (255, 69, 84)
PS2_BLUE = (46, 128, 255)
PHOSPHOR = (100, 255, 140)


# =========================================================================== helpers

def _draw_switch_handheld(cv, cx, cy, scale=1, glow=True):
    """Consola híbrida con controles laterales azul cian (izq) y rojo neón (der)."""
    d = ImageDraw.Draw(cv)
    w_scr = 7 * scale
    h_scr = 4 * scale
    w_pad = max(2, 2 * scale)
    # Control izquierdo (Cian)
    d.rectangle([cx - w_scr - w_pad, cy - h_scr, cx - w_scr, cy + h_scr],
                fill=(*SW_CYAN, 255), outline=(*INK, 255))
    # Control derecho (Rojo)
    d.rectangle([cx + w_scr, cy - h_scr, cx + w_scr + w_pad, cy + h_scr],
                fill=(*SW_RED, 255), outline=(*INK, 255))
    # Pantalla central encendida
    d.rectangle([cx - w_scr, cy - h_scr, cx + w_scr, cy + h_scr],
                fill=(22, 28, 38, 255), outline=(*INK, 255))
    d.rectangle([cx - w_scr + 1, cy - h_scr + 1, cx + w_scr - 1, cy + h_scr - 1],
                fill=(95, 215, 250, 255))
    if glow:
        d.ellipse([cx - w_scr - 4, cy - h_scr - 8, cx + w_scr + 4, cy + 2],
                  fill=(130, 235, 255, 48))


def _draw_dock_diagram(cv, x, y, t, t_split):
    """Diagrama visual del paso de TV de casa a consola portátil con Joy-Cons encastrando."""
    window(cv, x, y, 186, 66, border=CYAN, alpha=0.92)
    d = ImageDraw.Draw(cv)
    p = ease_out(prog(t, t_split - 0.2, t_split + 0.45))
    # Ícono izquierdo: TV + Dock (Casa)
    tx, ty = x + 44, y + 32
    d.rectangle([tx - 24, ty - 16, tx + 24, ty + 8], fill=(16, 24, 42, 255), outline=(*CREAM, 255))
    if p < 0.5:
        d.rectangle([tx - 21, ty - 13, tx + 21, ty + 5], fill=(60, 175, 235, 255))
        d.rectangle([tx - 8, ty - 4, tx + 8, ty + 5], fill=(110, 220, 130, 255))
    d.rectangle([tx - 8, ty + 9, tx + 8, ty + 16], fill=(42, 46, 58, 255), outline=(*INK, 255))
    draw_text(cv, "CASA", tx, y + 52, "silk", 8, GOLD if p < 0.5 else GREY, align="center")

    # Flecha central
    ax = x + 93
    d.line([(ax - 10, ty), (ax + 10, ty)], fill=(*GOLD, 255), width=2)
    d.polygon([(ax + 10, ty - 4), (ax + 15, ty), (ax + 10, ty + 4)], fill=(*GOLD, 255))

    # Ícono derecho: Consola portátil con controles cian y rojo acoplándose
    hx, hy = x + 142, y + 32
    off_pad = int((1.0 - p) * -8)
    d.rectangle([hx - 16, hy - 10, hx + 16, hy + 10], fill=(20, 26, 38, 255), outline=(*INK, 255))
    d.rectangle([hx - 14, hy - 8, hx + 14, hy + 8], fill=(70, 195, 245, 255) if p >= 0.3 else (30, 40, 56, 255))
    d.rectangle([hx - 23, hy - 10 + off_pad, hx - 16, hy + 10 + off_pad],
                fill=(*SW_CYAN, 255), outline=(*INK, 255))
    d.rectangle([hx + 16, hy - 10 + off_pad, hx + 23, hy + 10 + off_pad],
                fill=(*SW_RED, 255), outline=(*INK, 255))
    draw_text(cv, "PORTÁTIL", hx, y + 52, "silk", 8, CYAN if p >= 0.5 else GREY, align="center")


def _draw_globe(cv, cx, cy, r, t, p_nodes=1.0):
    """Globo terráqueo pixel art con continentes, grilla de meridianos y arcos luminosos."""
    d = ImageDraw.Draw(cv)
    # Halo exterior atmosférico
    for gr, ga in ((r + 8, 25), (r + 4, 55)):
        d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(40, 170, 235, ga))
    # Océano profundo
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 42, 88, 255), outline=(*CYAN, 255))

    # Continentes estilizados en grilla de píxeles (bloques de 3x3 dentro del círculo)
    rot = int(t * 6) % 24
    continents = [
        # América del Norte y del Sur
        (-36, -24, 18, 16), (-28, -8, 12, 10), (-22, 4, 16, 26),
        # Europa y África
        (-2, -28, 18, 14), (0, -10, 20, 28),
        # Asia y Oceanía
        (16, -26, 26, 20), (26, 12, 14, 10),
    ]
    for (ox, oy, cw, ch) in continents:
        for yy in range(oy, oy + ch, 3):
            for xx in range(ox, ox + cw, 3):
                px = cx + ((xx + rot + r) % (2 * r)) - r
                py = cy + yy
                if (px - cx) ** 2 + (py - cy) ** 2 < (r - 3) ** 2:
                    col = (46, 142, 96) if (xx + yy) % 6 == 0 else (34, 114, 82)
                    d.rectangle([px, py, px + 2, py + 2], fill=(*col, 255))

    # Paralelos y meridianos sutiles
    for dy_lat in (-r // 2, 0, r // 2):
        hw = int(math.sqrt(max(0, r * r - dy_lat * dy_lat)))
        d.line([(cx - hw + 2, cy + dy_lat), (cx + hw - 2, cy + dy_lat)], fill=(28, 82, 142, 160))
    for mw in (-r // 2, 0, r // 2):
        d.arc([cx - abs(mw) - 12, cy - r + 2, cx + abs(mw) + 12, cy + r - 2], 0, 360, fill=(28, 82, 142, 140))

    # Nodos luminosos y arcos de conexión intercontinental
    nodes = [
        (cx - 28, cy - 16),  # Norteamérica
        (cx - 16, cy + 16),  # Sudamérica
        (cx + 4, cy - 18),   # Europa
        (cx + 8, cy + 6),    # África
        (cx + 28, cy - 10),  # Asia Oriental
        (cx + 32, cy + 18),  # Oceanía
    ]
    arcs = [(0, 2), (0, 1), (2, 4), (2, 3), (4, 5), (1, 3), (0, 4)]
    n_active = int(round(len(arcs) * clamp01(p_nodes)))
    for idx in range(n_active):
        p0, p1 = nodes[arcs[idx][0]], nodes[arcs[idx][1]]
        mx = (p0[0] + p1[0]) // 2
        my = min(p0[1], p1[1]) - 14
        prev = p0
        for step in range(1, 9):
            u = step / 8.0
            qx = int((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u ** 2 * p1[0])
            qy = int((1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u ** 2 * p1[1])
            d.line([prev, (qx, qy)], fill=(120, 240, 255, 210), width=1)
            prev = (qx, qy)
        # Pulso viajando por el arco
        uf = (t * 1.4 + idx * 0.23) % 1.0
        px = int((1 - uf) ** 2 * p0[0] + 2 * (1 - uf) * uf * mx + uf ** 2 * p1[0])
        py = int((1 - uf) ** 2 * p0[1] + 2 * (1 - uf) * uf * my + uf ** 2 * p1[1])
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(*GOLD, 255))

    for idx, (nx, ny) in enumerate(nodes):
        if p_nodes > idx * 0.12:
            orb(cv, nx, ny, t + idx, 1.0)


def _draw_stamp(cv, cx, cy, text, t, t0):
    """Sello rojo pesado ('POSTERGADO') que cae de golpe sobre el calendario."""
    p = prog(t, t0, t0 + 0.18)
    if p <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    sw, sh = 112, 26
    x0, y0 = cx - sw // 2, cy - sh // 2
    # Marco doble de sello de goma rojo
    red_ink = (218, 38, 46)
    d.rectangle([x0, y0, x0 + sw, y0 + sh], fill=(248, 224, 220, 240), outline=(*red_ink, 255), width=2)
    d.rectangle([x0 + 3, y0 + 3, x0 + sw - 3, y0 + sh - 3], outline=(*red_ink, 255), width=1)
    draw_text(lay, text, cx, cy - 4, "press", 8, red_ink, align="center", outline=None, shadow=False)
    paste(cv, lay, 0, 0, min(1.0, p * 3))


# =========================================================================== escenas

def sc_switch_train(t):
    """c8_01: En 2017, la Nintendo Switch borra la línea entre la consola de casa y la portátil."""
    base = bg("bg_commuter_train_2017").copy()
    sway_y = int(round(math.sin(t * 3.2) * 1))
    cv = offset_canvas(base, 0, sway_y, fill=(24, 18, 28))

    t_sw = w("c8_01", "Switch")
    t_por = w("c8_01", "portatil")

    # Pasajera sentada en la butaca del tren jugando con la consola híbrida (controles rojo y azul)
    px, py = 148, 246 + sway_y
    char(cv, CAST_CH8["viajera"], px, py, t, scale=3, sit=True, arms="hold", mood="happy", look=1)
    _draw_switch_handheld(cv, px, py - 24 * 3, scale=2, glow=True)

    # Diagrama interactivo de Casa -> Portátil a la derecha
    if t >= t_sw - 0.2:
        a_d, dy_d = pop(t, t_sw - 0.2, 0.35)
        if a_d > 0:
            _draw_dock_diagram(cv, 266, 66 + dy_d, t, t_por - 0.3)

    # La Máquina mira por la ventana del tren maravillada
    robot(cv, 326, 258 + sway_y, t, face="happy", scale=2)

    # Placa superior: SWITCH · 2017 · CASA Y PORTÁTIL
    a_top, dy_top = pop(t, S1 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 72, 12 + dy_top, 336, 42, border=CYAN, alpha=0.94)
        draw_text(cv, "SWITCH · 2017 · CASA Y PORTÁTIL", 240, 20 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        draw_text(cv, "LA CONSOLA QUE VIAJA CON VOS", 240, 36 + dy_top, "silk", 8,
                  CYAN, align="center", alpha=a_top)

    return vignette(cv, 0.3)


def sc_switch_vs_ps2(t):
    """c8_02: Dos barras horizontales en tablero limpio: SWITCH 157 MILLONES vs PS2 160 MILLONES."""
    cv = vgradient((8, 12, 28), (18, 26, 54), 14)
    STARS.draw(cv, t * 0.3, alpha=0.45)
    d = ImageDraw.Draw(cv)

    t_157 = w("c8_02", "ciento")
    t_tres = w("c8_02", "tres")
    t_ps2 = w("c8_02", "PlayStation")

    # Cabecera superior: SWITCH 157 M · PS2 160 M
    a_hd, dy_hd = pop(t, S2 + 0.08, 0.35)
    window(cv, 56, 14 + dy_hd, 368, 42, border=GOLD, alpha=0.95)
    draw_text(cv, "SWITCH 157 M · PS2 160 M", 240, 22 + dy_hd, "press", 8,
              GOLD, align="center", alpha=a_hd)
    draw_text(cv, "LA CARRERA POR EL RÉCORD HISTÓRICO", 240, 38 + dy_hd, "silk", 8,
              CREAM, align="center", alpha=a_hd)

    # Panel principal con las dos barras horizontales creciendo
    window(cv, 28, 66, 424, 134, alpha=0.92)
    p_sw = ease_out(prog(t, S2 + 0.2, t_157 + 0.7))
    p_ps = ease_out(prog(t, S2 + 0.35, t_157 + 0.95))

    max_w = 376
    bx0 = 52

    # Barra 1 (Cyan / Red): SWITCH · 157 MILLONES
    by1 = 84
    n_sw = int(round(157 * p_sw))
    draw_text(cv, f"SWITCH · {n_sw} MILLONES" if p_sw < 0.98 else "SWITCH · 157 MILLONES",
              bx0, by1, "press", 8, CYAN)
    d.rectangle([bx0, by1 + 14, bx0 + max_w, by1 + 36], fill=(12, 18, 34, 255), outline=(*INK, 255))
    w1 = int(round(max_w * (157.0 / 160.0) * p_sw))
    if w1 > 4:
        # Mitad izquierda cian, mitad derecha rojo neón (colores de Switch)
        half = w1 // 2
        d.rectangle([bx0 + 2, by1 + 16, bx0 + 2 + half, by1 + 34], fill=(*SW_CYAN, 255))
        d.rectangle([bx0 + 2 + half, by1 + 16, bx0 + w1, by1 + 34], fill=(*SW_RED, 255))
        d.rectangle([bx0 + 2, by1 + 16, bx0 + w1, by1 + 20], fill=(255, 220, 225, 140))

    # Barra 2 (Azul eléctrico): PS2 · 160 MILLONES
    by2 = 138
    n_ps = int(round(160 * p_ps))
    draw_text(cv, f"PS2 · {n_ps} MILLONES" if p_ps < 0.98 else "PS2 · 160 MILLONES",
              bx0, by2, "press", 8, (120, 185, 255))
    d.rectangle([bx0, by2 + 14, bx0 + max_w, by2 + 36], fill=(12, 18, 34, 255), outline=(*INK, 255))
    w2 = int(round(max_w * 1.0 * p_ps))
    if w2 > 4:
        d.rectangle([bx0 + 2, by2 + 16, bx0 + w2, by2 + 34], fill=(*PS2_BLUE, 255))
        d.rectangle([bx0 + 2, by2 + 16, bx0 + w2, by2 + 20], fill=(160, 215, 255, 160))

    # Indicador de la brecha de menos de 3 millones
    if t >= t_tres - 0.1:
        a_g, dy_g = pop(t, t_tres - 0.1, 0.35)
        # Franja dorada resaltando la pequeña diferencia en el extremo derecho de la barra 1
        x_gap = bx0 + int(max_w * (157.0 / 160.0))
        d.rectangle([x_gap, by1 + 14, bx0 + max_w, by2 + 36], outline=(*GOLD, 255), width=2)
        window(cv, 76, 210 + dy_g, 328, 38, border=GOLD, alpha=0.95)
        draw_text(cv, "DIFERENCIA: MENOS DE 3 MILLONES", 240, 218 + dy_g, "press", 8,
                  GOLD, align="center", alpha=a_g)
        draw_text(cv, "DOS DÉCADAS DE HISTORIA FRENTE A FRENTE", 240, 233 + dy_g, "silk", 8,
                  CREAM, align="center", alpha=a_g)

    return vignette(cv, 0.35)


def sc_switch2_dawn(t):
    """c8_03: 2025 · Fila al amanecer frente a la tienda para Switch 2 (3,5 millones en 4 días)."""
    # Gradación de amanecer azul/rosado temprano sobre la tienda
    base = bg("bg_midnight_launch_2013").copy()
    cv = grade(base, mul=(1.15, 0.92, 1.18), add=(38, 18, 42), sat=0.95, k=0.85)
    d = ImageDraw.Draw(cv)
    # Resplandor rosado/dorado del amanecer en el cielo izquierdo (x < 160, y < 110)
    lay_sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(lay_sky)
    for r_sun, a_sun in ((70, 35), (45, 55), (24, 80)):
        ds.ellipse([110 - r_sun, 72 - r_sun, 110 + r_sun, 72 + r_sun], fill=(255, 150, 185, a_sun))
    paste(cv, lay_sky, 0, 0)

    t_sw2 = w("c8_03", "Switch")
    t_tres = w("c8_03", "tres")
    t_nin = w("c8_03", "Nintendo")

    # Fila de compradores al amanecer llevando cajas rojas/cian de la nueva consola
    buyers = [
        ("fila_1", 108, 256, 0.0),
        ("fila_2", 188, 258, 0.1),
        ("fila_3", 268, 258, 0.2),
        ("fila_4", 356, 256, 0.3),
    ]
    for idx, (bk, bx, by, delay) in enumerate(buyers):
        a_b, dy_b = pop(t, S3 + delay, 0.32)
        if a_b <= 0:
            continue
        arms = "cheer" if t >= t_nin else "hold"
        char(cv, CAST_CH8[bk], bx, by + dy_b, t + idx * 0.2, scale=3 if idx in (0, 3) else 2,
             alpha=a_b, arms=arms, mood="happy", look=1 if bx < 280 else -1)
        # Caja de consola Switch 2 en las manos cuando están en pose 'hold'
        if arms == "hold":
            sc = 3 if idx in (0, 3) else 2
            hy = by + dy_b - 24 * sc
            d.rectangle([bx - 4 * sc, hy - 3 * sc, bx + 4 * sc, hy + 2 * sc],
                        fill=(230, 45, 58, 255), outline=(*INK, 255))
            d.rectangle([bx - 2 * sc, hy - 2 * sc, bx + 2 * sc, hy + 1 * sc],
                        fill=(248, 248, 252, 255))

    robot(cv, 44, 256, t, face="happy" if t < t_nin else "heart", scale=2)

    # Placa superior: SWITCH 2 · 3,5 MILLONES EN 4 DÍAS
    a_top, dy_top = pop(t, S3 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 48, 12 + dy_top, 384, 46, border=GOLD if t >= t_tres else CYAN, alpha=0.94)
        draw_text(cv, "SWITCH 2 · 3,5 MILLONES EN 4 DÍAS", 240, 20 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        sub = "EL MEJOR ARRANQUE EN LA HISTORIA DE NINTENDO" if t >= t_nin - 0.2 else "2025 · RÉCORD DE LANZAMIENTO"
        draw_text(cv, sub, 240, 38 + dy_top, "silk", 8, CREAM, align="center", alpha=a_top)

    return vignette(cv, 0.3)


def sc_globe_2025(t):
    """c8_04: En 2025, la industria supera por primera vez los US$ 200.000 millones (201.600 M)."""
    cv = vgradient((4, 8, 22), (12, 24, 52), 16)
    STARS.draw(cv, t * 0.45, alpha=0.8)

    t_2025 = w("c8_04", "veinticinco")
    t_sup = w("c8_04", "supero")
    t_200 = w("c8_04", "doscientos")

    # Globo terráqueo central con continentes y arcos intercontinentales
    p_nodes = ease_out(prog(t, S4 + 0.15, t_200 + 0.3))
    _draw_globe(cv, 240, 134, 56, t, p_nodes=p_nodes)

    # Placa superior: 2025 · US$ 201.600 MILLONES
    a_top, dy_top = pop(t, S4 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 56, 10 + dy_top, 368, 44, border=GOLD, alpha=0.95)
        draw_text(cv, "2025 · US$ 201.600 MILLONES", 240, 18 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        draw_text(cv, "MÁS DE US$ 200.000 MILLONES AL AÑO", 240, 34 + dy_top, "silk", 8,
                  CYAN, align="center", alpha=a_top)

    # Placa inferior con desglose global al llegar a "doscientos mil millones"
    if t >= t_sup - 0.1:
        a_b, dy_b = pop(t, t_sup - 0.1, 0.35)
        window(cv, 68, 208 + dy_b, 344, 44, border=CYAN, alpha=0.93)
        draw_text(cv, "UN PLANETA ENTERO JUGANDO CONECTADO", 240, 217 + dy_b, "press", 8,
                  CREAM, align="center", alpha=a_b)
        draw_text(cv, "CONSOLAS · PC · MÓVILES EN TODOS LOS CONTINENTES", 240, 234 + dy_b, "silk", 8,
                  GOLD, align="center", alpha=a_b)
        for i in range(4):
            sparkle(cv, 88 + i * 100, 198 + (i % 2) * 8, t + i * 0.5, 3, GOLD)

    return vignette(cv, 0.35)


def sc_gtav_230m(t):
    """c8_05: Transición con dithering de bg_open_city_2001 a bg_neon_coast_2026 (+230 M de copias)."""
    t_gta = w("c8_05", "cinco")
    t_230 = w("c8_05", "doscientos")
    # Dither mix progresivo desde la ciudad lluviosa de 2001 hacia la costa synthwave de 2026
    k_mix = ease_in_out(prog(t, S5 + 0.3, t_230 + 0.2))
    cv = dither_mix(bg("bg_open_city_2001"), bg("bg_neon_coast_2026"), k_mix).copy()

    # Placa superior: GTA V · +230 MILLONES DE COPIAS
    a_top, dy_top = pop(t, S5 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 52, 12 + dy_top, 376, 46, border=GOLD, alpha=0.94)
        draw_text(cv, "GTA V · +230 MILLONES DE COPIAS", 240, 20 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        draw_text(cv, "TRES GENERACIONES DE CONSOLAS SIN DEJAR DE VENDERSE", 240, 38 + dy_top,
                  "silk", 8, CYAN, align="center", alpha=a_top)

    # Contador gigante en el centro-abajo cuando dice "más de doscientos treinta millones"
    if t >= t_230 - 0.25:
        a_c, dy_c = pop(t, t_230 - 0.25, 0.35)
        p_c = ease_out(prog(t, t_230 - 0.15, t_230 + 0.45))
        n_cop = int(round(230 * p_c))
        window(cv, 84, 196 + dy_c, 312, 52, border=GOLD, alpha=0.95)
        draw_text(cv, f"+{n_cop} MILLONES", 240, 205 + dy_c, "press", 16,
                  align="center", gradient=GOLD_RAMP, outline_w=2, alpha=a_c)
        draw_text(cv, "2013 - 2026 · FENÓMENO CONTINUO", 240, 231 + dy_c, "silk", 8,
                  CREAM, align="center", alpha=a_c)

    return vignette(cv, 0.3)


def sc_calendar_delays(t):
    """c8_06: Hoja de calendario con dos fechas previas y dos sellos rojos ('POSTERGADO') con shake."""
    base = grade(bg("bg_neon_coast_2026").copy(), mul=(0.38, 0.35, 0.52), add=(8, 6, 18), sat=0.55, k=0.85)
    t_vez = w("c8_06", "vez")
    t_otra = w("c8_06", "otra")

    # Hoja grande de calendario en el centro de la pantalla
    a_cal, dy_cal = pop(t, S6 + 0.08, 0.35)
    cx, cy = 240, 134 + dy_cal
    cw, ch = 296, 168
    x0, y0 = cx - cw // 2, cy - ch // 2

    draw_paper(base, x0, y0, cw, ch, color=(244, 238, 224))
    d = ImageDraw.Draw(base)
    # Encabezado rojo del calendario y anillos metálicos
    d.rectangle([x0 + 1, y0 + 1, x0 + cw - 1, y0 + 28], fill=(196, 48, 56, 255), outline=(*INK, 255))
    for rx in range(x0 + 36, x0 + cw - 24, 44):
        d.rectangle([rx - 3, y0 - 5, rx + 3, y0 + 6], fill=(180, 186, 198, 255), outline=(*INK, 255))
    draw_text(base, "CALENDARIO DE LANZAMIENTO", cx, y0 + 10, "press", 8, CREAM, align="center")

    # Dos bloques de fecha objetivo previos dentro de la hoja
    # Fila 1: OTOÑO 2025
    r1_y = y0 + 42
    d.rectangle([x0 + 18, r1_y, x0 + cw - 18, r1_y + 48], fill=(230, 222, 206, 255), outline=(160, 150, 135, 255))
    draw_text(base, "FECHA OBJETIVO 1", x0 + 26, r1_y + 8, "silk", 8, (90, 84, 76), outline=None, shadow=False)
    draw_text(base, "OTOÑO 2025", x0 + 26, r1_y + 24, "press", 8, INK, outline=None, shadow=False)

    # Fila 2: MAYO 2026
    r2_y = y0 + 102
    d.rectangle([x0 + 18, r2_y, x0 + cw - 18, r2_y + 48], fill=(230, 222, 206, 255), outline=(160, 150, 135, 255))
    draw_text(base, "FECHA OBJETIVO 2", x0 + 26, r2_y + 8, "silk", 8, (90, 84, 76), outline=None, shadow=False)
    draw_text(base, "MAYO 2026", x0 + 26, r2_y + 24, "press", 8, INK, outline=None, shadow=False)

    # Sello 1: "POSTERGADO" en "vez"
    if t >= t_vez - 0.04:
        _draw_stamp(base, x0 + cw - 78, r1_y + 24, "POSTERGADO", t, t_vez - 0.04)

    # Sello 2: "POSTERGADO" en "otra"
    if t >= t_otra - 0.04:
        _draw_stamp(base, x0 + cw - 78, r2_y + 24, "POSTERGADO", t, t_otra - 0.04)

    # Sacudida de cámara (shake) al golpear cada sello
    dx1, dy1 = shake(t, t_vez - 0.02, dur=0.28, amp=5)
    dx2, dy2 = shake(t, t_otra - 0.02, dur=0.32, amp=6)
    cv = offset_canvas(base, dx1 + dx2, dy1 + dy2, fill=(10, 8, 20))
    return vignette(cv, 0.35)


def sc_neon_date(t):
    """c8_07: En bg_neon_coast_2026 se eleva el cartel neón '19 · 11 · 2026' / 'TRECE AÑOS DESPUÉS'."""
    cv = bg("bg_neon_coast_2026").copy()
    t_19 = w("c8_07", "diecinueve")
    t_trece = w("c8_07", "Trece")

    # Destellos synthwave sobre el mar y las luces de neón de la avenida
    d = ImageDraw.Draw(cv)
    for i in range(6):
        wy = 166 + i * 8
        wx = 98 + int(math.sin(t * 3.0 + i) * 16)
        d.line([(wx - 18, wy), (wx + 18, wy)], fill=(255, 190, 120, 150))

    # Gran cartel neón que se eleva sobre el horizonte al decir la fecha
    p_rise = ease_out(prog(t, S7 + 0.15, t_19 + 0.45))
    if p_rise > 0:
        y_box = int(62 - p_rise * 42)
        window(cv, 44, y_box, 392, 86, fill=(16, 10, 38), border=(255, 70, 190), alpha=0.92)
        draw_text(cv, "NUEVA FECHA OFICIAL · GTA VI", 240, y_box + 10, "silk", 8,
                  CYAN, align="center")
        draw_text(cv, "19 · 11 · 2026", 240, y_box + 26, "press", 24,
                  align="center", gradient=GOLD_RAMP, outline_w=2)
        if t >= t_trece - 0.2:
            a_tr = prog(t, t_trece - 0.2, t_trece + 0.25)
            draw_text(cv, "TRECE AÑOS DESPUÉS", 240, y_box + 60, "press", 16,
                      align="center", gradient=CYAN_RAMP, outline_w=2, alpha=a_tr)
            for i in range(4):
                sparkle(cv, 66 + i * 116, y_box + 34 + (i % 2) * 24, t * 1.5 + i, 3, GOLD)

    return vignette(cv, 0.28)


def sc_match_cut(t):
    """c8_08: El Match Cut — El sol neón de 2026 se encoge paso a paso hasta convertirse en el
    punto verde de fósforo de Tennis for Two (1958) sobre la línea de cancha del osciloscopio."""
    t_punto = w("c8_08", "punto")
    t_cinco = w("c8_08", "cinco")
    t_vis = w("c8_08", "visitas")
    t_hoy = w("c8_08", "Hoy")
    t_end8 = TL.e("c8_08")

    # Progreso de la transformación del sol neón (en x=102, y=132, r=52) hacia el punto de fósforo (240, 135, r=3)
    p_shrink = ease_in_out(prog(t, S8 + 0.35, t_vis + 0.2))

    # Fondo 1: Costa neón que se apaga gradualmente hacia el negro verdoso del osciloscopio de 1958
    neon_bg = bg("bg_neon_coast_2026").copy()
    osc_bg = new_canvas((4, 12, 8))
    d_osc = ImageDraw.Draw(osc_bg)
    # Retícula circular sutil de osciloscopio de 5 pulgadas y cancha + red de Tennis for Two
    d_osc.ellipse([240 - 96, 135 - 96, 240 + 96, 135 + 96], fill=(6, 20, 12, 255), outline=(28, 76, 42, 255), width=2)
    for gx in range(160, 321, 32):
        d_osc.line([(gx, 46), (gx, 224)], fill=(12, 38, 20, 255))
    for gy in range(60, 216, 32):
        d_osc.line([(152, gy), (328, gy)], fill=(12, 38, 20, 255))
    # Línea horizontal de la cancha (y=170) y red central (x=240, y=148..170)
    d_osc.line([(164, 170), (316, 170)], fill=(*PHOSPHOR, 255), width=2)
    d_osc.line([(240, 146), (240, 170)], fill=(*PHOSPHOR, 255), width=2)

    cv = dither_mix(neon_bg, osc_bg, p_shrink).copy()
    d = ImageDraw.Draw(cv)

    # El sol neón se desplaza desde (102, 132) hasta el centro de la cancha (240, 135) y reduce su radio de 52 a 3
    sun_x = int(round(102 + (240 - 102) * p_shrink))
    sun_y = int(round(132 + (135 - 132) * p_shrink))
    sun_r = max(3, int(round(52 * (1.0 - p_shrink) + 3 * p_shrink)))

    if p_shrink < 0.88:
        # Sol synthwave encogiéndose con franjas magenta/naranja que viran al verde fósforo
        c_top = (
            int(255 * (1 - p_shrink) + PHOSPHOR[0] * p_shrink),
            int(165 * (1 - p_shrink) + PHOSPHOR[1] * p_shrink),
            int(70 * (1 - p_shrink) + PHOSPHOR[2] * p_shrink),
        )
        c_bot = (
            int(235 * (1 - p_shrink) + PHOSPHOR[0] * p_shrink),
            int(45 * (1 - p_shrink) + PHOSPHOR[1] * p_shrink),
            int(165 * (1 - p_shrink) + PHOSPHOR[2] * p_shrink),
        )
        d.ellipse([sun_x - sun_r - 4, sun_y - sun_r - 4, sun_x + sun_r + 4, sun_y + sun_r + 4],
                  fill=(*c_top, 75))
        d.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r],
                  fill=(*c_top, 255), outline=(*c_bot, 255))
    else:
        # El punto de luz verde de fósforo rebotando sobre la cancha de 1958
        dt_b = max(0.0, t - (t_cinco - 0.2))
        bx = 240 + int(math.sin(dt_b * 3.4) * 52)
        by = 166 - int(abs(math.cos(dt_b * 3.4)) * 34)
        trail = []
        for k in range(5, 0, -1):
            tk = max(0.0, dt_b - k * 0.04)
            tx = 240 + int(math.sin(tk * 3.4) * 52)
            ty = 166 - int(abs(math.cos(tk * 3.4)) * 34)
            trail.append((tx, ty))
        draw_phosphor_dot(cv, bx, by, r=3, trail=trail)

    # Placa comparativa superior: 1958 · UN PUNTO DE LUZ -> 2026 · UNA CIUDAD ENTERA
    window(cv, 52, 12, 376, 40, border=GOLD if t >= t_hoy else CYAN, alpha=0.92)
    if t < t_hoy - 0.1:
        draw_text(cv, "1958 · UN PUNTO DE LUZ EN 5 PULGADAS", 240, 20, "press", 8,
                  PHOSPHOR, align="center")
        draw_text(cv, "PARA QUE LAS VISITAS NO SE ABURRAN", 240, 35, "silk", 8,
                  CREAM, align="center")
    else:
        draw_text(cv, "1958 → 2026 · HOY ES UNA CIUDAD ENTERA", 240, 20, "press", 8,
                  GOLD, align="center")
        draw_text(cv, "SESENTA Y OCHO AÑOS DEL MISMO PUNTO DE LUZ", 240, 35, "silk", 8,
                  CYAN, align="center")

    # Corte abrupto a negro al terminar c8_08
    if t >= t_end8 - 0.12:
        cv = fade_to(cv, (0, 0, 0), prog(t, t_end8 - 0.12, t_end8 + 0.05))
    return vignette(cv, 0.35)


def sc_epilogue(t):
    """c8_09: Pantalla negra pura; el punto verde de fósforo rebota UNA sola vez en el centro
    y aparece el cielo estrellado con el título 'PARA QUE NO SE ABURRIERAN' antes de fundir a negro."""
    cv = new_canvas((0, 0, 0))
    t_bounce = TL.s("c8_09") - 0.1
    t_prox = w("c8_09", "proximo")
    t_emp = w("c8_09", "empezar")
    t_e9 = TL.e("c8_09")

    # Aparición suave de las estrellas tras el único rebote
    star_a = ease_in_out(prog(t, t_prox - 0.2, t_emp + 0.4))
    if star_a > 0:
        STARS.draw(cv, t * 0.25, alpha=0.65 * star_a)

    # El punto verde de fósforo cae, rebota UNA sola vez en (240, 146) en t_bounce y queda brillando en el centro
    dt = t - (S9 + 0.02)
    t_hit = t_bounce - (S9 + 0.02)
    if dt <= t_hit:
        # Caída hacia el centro para el único bote
        u = clamp01(dt / max(0.05, t_hit))
        by = int(68 + (146 - 68) * (u ** 2))
    else:
        # Un único arco tras el bote que se asienta suavemente en (240, 118)
        u2 = clamp01((dt - t_hit) / 0.85)
        by = int(146 - 28 * ease_out(u2) - math.sin(u2 * math.pi) * 24)

    trail = []
    if dt < t_hit + 0.85:
        for k in range(5, 0, -1):
            dk = max(0.0, dt - k * 0.035)
            if dk <= t_hit:
                uk = clamp01(dk / max(0.05, t_hit))
                ty = int(68 + (146 - 68) * (uk ** 2))
            else:
                uk2 = clamp01((dk - t_hit) / 0.85)
                ty = int(146 - 28 * ease_out(uk2) - math.sin(uk2 * math.pi) * 24)
            trail.append((240, ty))

    # Ondas concéntricas sutiles en el instante del único bote
    if 0 <= t - t_bounce < 0.55:
        p_ring = (t - t_bounce) / 0.55
        r_ring = int(6 + p_ring * 28)
        a_ring = int(160 * (1.0 - p_ring))
        ImageDraw.Draw(cv).ellipse([240 - r_ring, 146 - r_ring // 2, 240 + r_ring, 146 + r_ring // 2],
                                   outline=(*PHOSPHOR, a_ring))

    draw_phosphor_dot(cv, 240, by, r=3, trail=trail)

    # Título final: "PARA QUE NO SE ABURRAN"
    if t >= t_prox - 0.15:
        a_tit = ease_in_out(prog(t, t_prox - 0.15, t_emp + 0.2))
        draw_text(cv, "PARA QUE NO SE ABURRAN", 240, 162, "press", 16,
                  align="center", gradient=GOLD_RAMP, outline_w=2, alpha=a_tit)
        draw_text(cv, "LA HISTORIA DE LOS VIDEOJUEGOS · 1958 – 2026", 240, 188, "silk", 8,
                  CYAN, align="center", alpha=a_tit)
        if t >= t_emp - 0.1:
            a_sub = prog(t, t_emp - 0.1, t_e9 + 0.3)
            draw_text(cv, "EL PRÓXIMO CAPÍTULO ESTÁ POR EMPEZAR", 240, 206, "press", 8,
                      CREAM, align="center", alpha=a_sub)

    # Fundido limpio a negro antes de T_END (donde entra outro.py con Pixeloide Studios)
    fade_black = ease_in_out(prog(t, T_END - 0.85, T_END - 0.08))
    if fade_black > 0:
        cv = fade_to(cv, (0, 0, 0), fade_black)
    return cv


# =========================================================================== montaje

def scenes():
    return [
        (T_CARD - 0.3, make_card(CH, ["TRECE AÑOS"], "2017 – 2026", robot_face="happy"), None),
        (S1, sc_switch_train, lambda t: (
            cam_push(t, S1, S2, 1.0, 1.05, (240, 135), (230, 140))[0]
            + cam_punch(t, [w("c8_01", "Switch"), w("c8_01", "portatil")], 0.05),
            235, 138
        )),
        (S2, sc_switch_vs_ps2, lambda t: (
            1.0 + cam_punch(t, [w("c8_02", "ciento"), w("c8_02", "tres"), w("c8_02", "PlayStation")], 0.05),
            240, 135
        )),
        (S3, sc_switch2_dawn, lambda t: (
            cam_push(t, S3, S4, 1.0, 1.06, (240, 135), (240, 142))[0]
            + cam_punch(t, [w("c8_03", "Switch"), w("c8_03", "tres")], 0.05),
            240, 138
        )),
        (S4, sc_globe_2025, lambda t: (
            cam_push(t, S4, S5, 1.0, 1.07, (240, 135), (240, 134))[0]
            + cam_punch(t, [w("c8_04", "doscientos")], 0.06),
            240, 134
        )),
        (S5, sc_gtav_230m, lambda t: (
            cam_push(t, S5, S6, 1.0, 1.06, (240, 135), (240, 135))[0]
            + cam_punch(t, [w("c8_05", "doscientos")], 0.06),
            240, 135
        )),
        (S6, sc_calendar_delays, lambda t: (
            1.0 + cam_punch(t, [w("c8_06", "vez"), w("c8_06", "otra")], 0.08),
            240, 135
        )),
        (S7, sc_neon_date, lambda t: (
            cam_push(t, S7, S8, 1.0, 1.08, (240, 145), (240, 118))[0]
            + cam_punch(t, [w("c8_07", "diecinueve"), w("c8_07", "Trece")], 0.07),
            240, 128
        )),
        (S8, sc_match_cut, lambda t: cam_push(t, S8, S9, 1.0, 1.08, (200, 135), (240, 135))),
        (S9, sc_epilogue, None),
    ]


# =========================================================================== música y efectos

def music(A):
    t_end8 = TL.e("c8_08")
    # 2017 Switch y récord frente a PS2: ritmo moderno y brillante
    A.section(T_CARD + 1.6, S3, 118, [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_bright)
    # 2025 Switch 2 y globo terráqueo de US$ 201.600 millones: ascenso épico
    A.section(S3, S6, 122, [("F", "maj"), ("G", "maj"), ("E", "min"), ("A", "min")], A.st_triumph)
    A.sting(w("c8_04", "doscientos"), [69, 72, 76, 81], vol=0.045, step=0.10, hold=1.0)
    # Calendario de postergaciones: tensión expectante
    A.section(S6, S7, 100, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "maj")], A.st_build)
    # 19/11/2026 y Match Cut: clímax synthwave que se corta abruptamente al final de c8_08
    A.section(S7, t_end8, 124, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_summer_lead)
    t_trece = w("c8_07", "Trece")
    A.kick(A.music, t_trece, 0.42)
    A.crash(A.music, t_trece, 0.16)
    A.sting(t_trece, [69, 72, 76, 81, 84], vol=0.05, step=0.10, hold=1.2)
    # Nota: la música se detiene exactamente en TL.e("c8_08") para dejar silencio puro en c8_09


def sfx(A):
    # Escena 1: Switch 2017
    A.whoosh(S1 + 0.05, 0.35, 0.05)
    A.pop_sfx(w("c8_01", "Switch"), 680, 0.055)
    A.pop_sfx(w("c8_01", "portatil"), 820, 0.055)

    # Escena 2: Switch 157 M vs PS2 160 M
    A.whoosh(S2 + 0.05, 0.35, 0.05)
    for i in range(6):
        A.blip(S2 + 0.25 + i * 0.14, 640 + i * 70, vol=0.025)
    A.coin(w("c8_02", "tres"), 0.06)

    # Escena 3: Switch 2 (3,5 M en 4 días)
    A.whoosh(S3 + 0.05, 0.35, 0.05)
    A.join_jingle(w("c8_03", "Switch"), 0.055)
    A.coin(w("c8_03", "tres") + 0.15, 0.06)

    # Escena 4: Globo 2025 (US$ 201.600 millones)
    A.whoosh(S4 + 0.05, 0.4, 0.05)
    for i in range(7):
        A.blip(S4 + 0.25 + i * 0.16, 780 + i * 90, vol=0.025)
    A.coin(w("c8_04", "doscientos"), 0.065)

    # Escena 5: GTA V +230 millones
    A.whoosh(S5 + 0.05, 0.45, 0.05)
    A.coin(w("c8_05", "doscientos") + 0.2, 0.065)

    # Escena 6: Dos sellos pesados ("POSTERGADO") sobre el calendario
    A.whoosh(S6 + 0.05, 0.3, 0.045)
    A.stamp_hit(w("c8_06", "vez"))
    A.stamp_hit(w("c8_06", "otra"))

    # Escena 7: 19 · 11 · 2026 / TRECE AÑOS DESPUÉS
    A.whoosh(S7 + 0.1, 0.45, 0.055)
    A.pop_sfx(w("c8_07", "diecinueve"), 620, 0.06)
    A.coin(w("c8_07", "Trece"), 0.065)

    # Escena 8: Match Cut al osciloscopio de 1958
    A.whoosh(S8 + 0.2, 0.55, 0.05)
    A.hum_1958(w("c8_08", "cinco") - 0.2, TL.e("c8_08"), vol=0.020)
    A.plic(w("c8_08", "punto"), 980, 0.075)
    A.plic(w("c8_08", "visitas"), 1120, 0.065)

    # Escena 9: Silencio negro y el único rebote final ("plic") antes del título
    A.plic(TL.s("c8_09") - 0.1)
    A.text_blips(w("c8_09", "proximo") - 0.1, 24, 28, vol=0.016)
