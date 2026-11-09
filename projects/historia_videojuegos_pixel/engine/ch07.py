"""Capítulo 7: Todos juegan (2006 – 2016)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *  # noqa

w = TL.word
CH = 7
T_CARD = TL.chapter_start(CH)
T_END = chapter_end(CH)

S1 = TL.s("c7_01") - 0.2     # 2006: Wii en el living (abuela, padre, nieto + bolos)
S2 = TL.s("c7_03") - 0.2     # Teléfonos móviles en el subte (56 % de la industria)
S3 = TL.s("c7_04") - 0.2     # 2011: Minecraft (+350 millones, construcción por bloques)
S4 = TL.s("c7_05") - 0.2     # 17/09/2013: Lanzamiento de medianoche de GTA V
S5 = TL.s("c7_06") - 0.15    # US$ 1.000 millones en 3 días (récord histórico en 72 h)

C = S.hexc

# Reparto local de jugadores diversos para el Capítulo 7
CAST_CH7 = {
    "abuela": dict(
        name="Abuela", skin=S.SKIN["fair"], hair=C("d8d6d2"), hair_style="bun",
        glasses="wire", top="sweater", top_color=C("b85a7c"), shirt=C("f4eee6"),
        skirt=True, skirt_color=C("484a62"), pants=C("484a62"),
    ),
    "padre": dict(
        name="Padre", skin=S.SKIN["light"], hair=C("4a3424"), hair_style="side",
        top="shirt", top_color=C("4a88b8"), pants=C("383c48"),
    ),
    "nieto": dict(
        name="Nieto", skin=S.SKIN["fair"], hair=C("6a4426"), hair_style="fringe",
        top="hoodie", top_color=C("e0543c"), pants=C("2c3e66"),
    ),
    "sub_1": dict(
        name="Pasajera 1", skin=S.SKIN["tan"], hair=C("1c1618"), hair_style="long",
        top="hoodie", top_color=C("9c4268"), pants=C("262a38"),
    ),
    "sub_2": dict(
        name="Pasajero 2", skin=S.SKIN["brown"], hair=C("161214"), hair_style="crew",
        glasses="black", top="trench", top_color=C("4a5a68"), shirt=C("e6e4dc"),
        tie=C("883038"), pants=C("242830"),
    ),
    "sub_3": dict(
        name="Pasajera 3", skin=S.SKIN["asian"], hair=C("141016"), hair_style="bangs",
        top="sweater", top_color=C("38887a"), pants=C("2a2c38"),
    ),
    "sub_4": dict(
        name="Pasajero 4", skin=S.SKIN["fair"], hair=C("b88648"), hair_style="wavy",
        top="tshirt", top_color=C("c87a28"), pants=C("343846"),
    ),
    "sub_5": dict(
        name="Pasajero 5", skin=S.SKIN["light"], hair=C("c4c2be"), hair_style="recede",
        glasses="round", top="blazer", top_color=C("52483e"), shirt=C("e8e2d4"),
        pants=C("36322e"),
    ),
    "builder": dict(
        name="Constructor", skin=S.SKIN["tan"], hair=C("3c2618"), hair_style="short",
        top="tshirt", top_color=C("289aa8"), pants=C("343472"),
    ),
    "fan_1": dict(
        name="Fan 1", skin=S.SKIN["light"], hair=C("261c18"), hair_style="short",
        beard="stubble", top="hoodie", top_color=C("2c6844"), pants=C("262c3a"),
    ),
    "fan_2": dict(
        name="Fan 2", skin=S.SKIN["fair"], hair=C("8a3c28"), hair_style="long",
        top="sweater", top_color=C("823c64"), pants=C("242634"),
    ),
    "fan_3": dict(
        name="Fan 3", skin=S.SKIN["brown"], hair=C("141012"), hair_style="curly",
        top="tshirt", top_color=C("d4882a"), pants=C("2a3040"),
    ),
    "fan_4": dict(
        name="Fan 4", skin=S.SKIN["olive"], hair=C("1e1818"), hair_style="fringe",
        glasses="black", top="hoodie", top_color=C("3a5a8c"), pants=C("222630"),
    ),
}


# =========================================================================== helpers

def _draw_wiimote(cv, x, y, t, facing=1, swinging=True):
    """Control blanco por movimiento con correa y estela cian en la mano del jugador."""
    d = ImageDraw.Draw(cv)
    ang = math.sin(t * 10.0 + x * 0.1) * 0.55 if swinging else 0.15
    dx = int(round(math.cos(ang) * 9 * facing))
    dy = int(round(-abs(math.sin(ang)) * 9 - 4))
    # Estela de movimiento cian/blanca
    if swinging:
        for k in range(1, 5):
            ak = ang - k * 0.22
            sx = x + int(round(math.cos(ak) * (8 + k * 2) * facing))
            sy = y - int(round(abs(math.sin(ak)) * (8 + k * 2)))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(120, 235, 255, max(20, 150 - k * 32)))
    # Cuerpo blanco del control
    x1, y1 = x + dx, y + dy
    d.line([(x, y), (x1, y1)], fill=(*INK, 255), width=5)
    d.line([(x, y), (x1, y1)], fill=(246, 248, 252, 255), width=3)
    # Botón celeste encendido
    d.point((x + dx // 2, y + dy // 2), fill=(80, 220, 255, 255))
    # Correa de muñeca
    d.line([(x, y + 2), (x - 3 * facing, y + 7)], fill=(190, 198, 210, 220), width=1)


def _draw_bowling_tv(cv, t, t_strike):
    """Pista de bolos en pixel art dentro del marco interior del televisor plano (211, 70)..(309, 129)."""
    x0, y0, x1, y1 = 211, 70, 309, 129
    w_tv, h_tv = x1 - x0, y1 - y0
    tv = Image.new("RGBA", (w_tv, h_tv), (18, 32, 68, 255))
    d = ImageDraw.Draw(tv)
    # Cielo/fondo del salón de bolos y marcador superior
    d.rectangle([0, 0, w_tv, 19], fill=(26, 48, 98, 255))
    d.rectangle([4, 2, w_tv - 5, 13], fill=(12, 24, 52, 255), outline=(80, 200, 255, 255))
    # Pista de madera en perspectiva (trapecio)
    cx = w_tv // 2
    d.polygon([(cx - 16, 20), (cx + 16, 20), (cx + 42, h_tv), (cx - 42, h_tv)],
              fill=(218, 162, 92, 255))
    # Canaletas laterales
    d.polygon([(cx - 20, 20), (cx - 16, 20), (cx - 42, h_tv), (cx - 48, h_tv)],
              fill=(70, 76, 92, 255))
    d.polygon([(cx + 16, 20), (cx + 20, 20), (cx + 48, h_tv), (cx + 42, h_tv)],
              fill=(70, 76, 92, 255))
    # Tablones de madera de la pista
    for i in (-10, -5, 0, 5, 10):
        d.line([(cx + i, 20), (cx + i * 3, h_tv)], fill=(192, 136, 70, 255))
    # Ciclo del lanzamiento de la bola y los bolos volando
    cyc = (t - S1) % 3.2
    ball_p = clamp01(cyc / 1.35)
    hit = cyc >= 1.35
    # Bolos al fondo (10 pinos en formación triangular)
    pin_offsets = [(-10, -2), (-4, -2), (4, -2), (10, -2), (-6, 0), (0, 0), (6, 0), (-3, 2), (3, 2), (0, 4)]
    for idx, (px_off, py_off) in enumerate(pin_offsets):
        px = cx + px_off
        py = 22 + py_off
        if hit:
            dt_h = cyc - 1.35
            vx = (px_off * 2.4 + ((idx % 3) - 1) * 7) * dt_h
            vy = -24 * dt_h + 38 * (dt_h ** 2)
            px = int(px + vx)
            py = int(py + vy)
        if 2 <= px < w_tv - 2 and 2 <= py < h_tv - 2:
            d.rectangle([px - 1, py - 4, px + 1, py + 1], fill=(248, 248, 252, 255), outline=(30, 24, 38, 255))
            d.line([(px - 1, py - 2), (px + 1, py - 2)], fill=(220, 50, 50, 255))
    # Bola de bolos azul brillante avanzando hacia los pinos
    if not hit:
        by = int(h_tv - 4 - (h_tv - 28) * ease_in_out(ball_p))
        bx = cx + int(math.sin(ball_p * math.pi) * 3)
        r = max(2, int(5 - 2 * ball_p))
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(45, 150, 255, 255), outline=(16, 40, 96, 255))
        d.point((bx - 1, by - 1), fill=(210, 245, 255, 255))
    else:
        for k in range(4):
            ang = k * math.pi / 2 + t * 4
            sx = cx + int(math.cos(ang) * 12)
            sy = 22 + int(math.sin(ang) * 6)
            d.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=(*GOLD, 255))
    paste(cv, tv, x0, y0)
    if hit and int(t * 8) % 2 == 0:
        draw_text(cv, "¡CHUZA!", x0 + cx, y0 + 3, "silk", 8, GOLD, align="center", outline=INK, shadow=False)
    # Consola blanca vertical sobre el mueble al lado del parlante izquierdo con ranura cian
    d_cv = ImageDraw.Draw(cv)
    d_cv.rectangle([206, 141, 213, 155], fill=(244, 244, 248, 255), outline=(*INK, 255))
    d_cv.line([(208, 143), (208, 152)], fill=(70, 225, 255, 255))


def _draw_phone_glow(cv, x, feet, scale, t, seed=0):
    """Teléfono brillante en las manos del pasajero y haz de luz cian hacia su rostro."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # Posición de las manos en pose 'hold' (aprox 24*scale arriba de los pies)
    hx = int(x)
    hy = int(feet - 24 * scale)
    fy = int(feet - 38 * scale)
    pulse = 0.85 + 0.15 * math.sin(t * 5.0 + seed)
    # Cono de luz suave hacia la cara
    hw_top = 7 * scale
    d.polygon([
        (hx - 2 * scale, hy),
        (hx + 2 * scale, hy),
        (hx + hw_top, fy - 2 * scale),
        (hx - hw_top, fy - 2 * scale),
    ], fill=(110, 235, 255, int(68 * pulse)))
    # Brillo directo en el mentón/rostro
    d.ellipse([hx - 4 * scale, fy - 2 * scale, hx + 4 * scale, fy + 5 * scale],
              fill=(170, 245, 255, int(55 * pulse)))
    # Teléfono inteligente en las manos
    pw, ph = max(3, 3 * scale), max(4, 4 * scale)
    d.rectangle([hx - pw, hy - ph, hx + pw, hy + 1], fill=(24, 28, 38, 255), outline=(*INK, 255))
    d.rectangle([hx - pw + 1, hy - ph + 1, hx + pw - 1, hy], fill=(150, 248, 255, 255))
    # Ícono/partícula de juego flotando sobre la pantalla
    bob = int(math.sin(t * 4.2 + seed * 1.7) * 3)
    col = [GOLD, (110, 245, 160), (255, 120, 175), CYAN][seed % 4]
    d.rectangle([hx - 2, hy - ph - 6 + bob, hx + 2, hy - ph - 2 + bob], fill=(*col, 230), outline=(*INK, 220))
    paste(cv, lay, 0, 0)


def _draw_voxel_block(cv, gx, gy, kind, sz=14, alpha=1.0, dy=0):
    """Bloque estilo voxel 2.5D con textura pixelada (tierra/pasto, madera, piedra, cristal, techo)."""
    if alpha <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if alpha < 1 else cv
    d = ImageDraw.Draw(lay)
    x0, y0 = int(gx), int(gy + dy)
    depth = sz // 2
    palettes = {
        "grass": ((98, 178, 62), (134, 92, 56), (96, 64, 38)),
        "wood": ((188, 146, 86), (156, 114, 62), (118, 84, 44)),
        "log": ((124, 94, 58), (94, 66, 38), (68, 46, 26)),
        "stone": ((148, 152, 160), (118, 122, 130), (88, 92, 100)),
        "glass": ((190, 242, 255), (130, 212, 240), (96, 178, 212)),
        "gold": ((255, 230, 96), (232, 182, 52), (178, 128, 28)),
    }
    top_c, front_c, side_c = palettes.get(kind, palettes["wood"])
    # Cara frontal (x0..x0+sz, y0..y0+sz)
    d.rectangle([x0, y0, x0 + sz, y0 + sz], fill=(*front_c, 255), outline=(*INK, 255))
    if kind == "grass":
        # Borde de pasto verde arriba de la tierra
        d.rectangle([x0 + 1, y0 + 1, x0 + sz - 1, y0 + 4], fill=(*top_c, 255))
        for px in range(x0 + 2, x0 + sz - 1, 3):
            d.point((px, y0 + 5), fill=(*top_c, 255))
    elif kind == "glass":
        d.line([(x0 + 3, y0 + 3), (x0 + sz - 3, y0 + sz - 3)], fill=(245, 255, 255, 255))
    elif kind == "wood":
        d.line([(x0 + 1, y0 + sz // 2), (x0 + sz - 1, y0 + sz // 2)], fill=(*side_c, 255))
    else:
        d.point((x0 + 3, y0 + 4), fill=(*side_c, 255))
        d.point((x0 + sz - 4, y0 + sz - 4), fill=(*top_c, 255))
    # Cara superior (paralelogramo isométrico)
    d.polygon([
        (x0, y0),
        (x0 + depth, y0 - depth // 2),
        (x0 + sz + depth, y0 - depth // 2),
        (x0 + sz, y0),
    ], fill=(*top_c, 255), outline=(*INK, 255))
    # Cara lateral derecha
    d.polygon([
        (x0 + sz, y0),
        (x0 + sz + depth, y0 - depth // 2),
        (x0 + sz + depth, y0 + sz - depth // 2),
        (x0 + sz, y0 + sz),
    ], fill=(*side_c, 255), outline=(*INK, 255))
    if alpha < 1:
        paste(cv, lay, 0, 0, alpha)


# Lista ordenada de bloques para construir automáticamente un refugio/torre sobre el paisaje
VOXEL_BUILD = [
    # Base de pasto y piedra (fila inferior y=194)
    (186, 194, "grass"), (200, 194, "grass"), (214, 194, "stone"), (228, 194, "stone"),
    (242, 194, "stone"), (256, 194, "grass"), (270, 194, "grass"),
    # Piso de madera y columnas de tronco (y=180)
    (200, 180, "log"), (214, 180, "wood"), (228, 180, "wood"), (242, 180, "wood"), (256, 180, "log"),
    # Paredes con ventanas de cristal (y=166)
    (200, 166, "log"), (214, 166, "glass"), (228, 166, "wood"), (242, 166, "glass"), (256, 166, "log"),
    # Dintel superior (y=152)
    (200, 152, "log"), (214, 152, "wood"), (228, 152, "wood"), (242, 152, "wood"), (256, 152, "log"),
    # Techo escalonado y coronamiento dorado (y=138, 124)
    (193, 138, "wood"), (207, 138, "wood"), (221, 138, "wood"), (235, 138, "wood"),
    (249, 138, "wood"), (263, 138, "wood"),
    (207, 124, "wood"), (221, 124, "gold"), (235, 124, "gold"), (249, 124, "wood"),
]


# =========================================================================== escenas

def sc_wii(t):
    """2006: La Wii pone a jugar a abuelos, padres y chicos frente al televisor (+101 M)."""
    cv = bg("bg_living_wii_2006").copy()
    t_2006 = w("c7_01", "seis")
    t_abu = w("c7_01", "Abuelos")
    t_pad = w("c7_01", "Padres")
    t_chi = w("c7_01", "Chicos")
    t_mov = w("c7_01", "moviendo")
    t_c7_02 = TL.s("c7_02")

    # Pista de bolos animada en la pantalla del televisor
    _draw_bowling_tv(cv, t, t_mov)

    # Abuela en el piso de madera a la izquierda del sillón (aparece desde el inicio y saluda/juega)
    abu_swing = t >= t_abu - 0.15
    abu_arms = "cheer" if t >= t_c7_02 else ("wave" if abu_swing else "down")
    char(cv, CAST_CH7["abuela"], 114, 260, t, scale=3, arms=abu_arms, mood="happy", look=1)
    if abu_swing:
        _draw_wiimote(cv, 114 + 34, 260 - 115, t, facing=1, swinging=True)

    # Padre en el piso de madera a la derecha del sillón (entra en "Padres", escala adulta 3x apoyado en el suelo)
    if t >= t_pad - 0.2:
        a_p, dy_p = pop(t, t_pad - 0.2, 0.32)
        pad_arms = "cheer" if t >= t_c7_02 else "wave"
        char(cv, CAST_CH7["padre"], 354, 260 + dy_p, t, scale=3, alpha=a_p,
             arms=pad_arms, mood="happy", look=-1, facing=-1)
        if a_p > 0.6:
            _draw_wiimote(cv, 354 - 34, 260 + dy_p - 115, t + 0.4, facing=-1, swinging=True)

    # Nieto (chico, escala infantil 2x) parado sobre la alfombra/piso de madera adelante a la derecha (pies en y=264)
    chi_jump = int(abs(math.sin((t - t_chi) * 9.0)) * -6) if t_chi <= t < t_chi + 0.8 else 0
    chi_arms = "cheer" if (t >= t_c7_02 or t_chi <= t < t_chi + 0.9) else "wave"
    char(cv, CAST_CH7["nieto"], 396, 264 + chi_jump, t + 0.3, scale=2,
         arms=chi_arms, mood="happy", look=-1, facing=-1)
    _draw_wiimote(cv, 396 - 22, 264 + chi_jump - 76, t + 0.7, facing=-1, swinging=True)

    # La Máquina acompaña en el rincón izquierdo sobre el piso
    robot(cv, 44, 258, t, face="heart" if t >= t_c7_02 else "happy", scale=2)

    # Placa superior: WII · 2006 · CONTROL POR MOVIMIENTO
    a_top, dy_top = pop(t, S1 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 76, 10 + dy_top, 328, 40, alpha=0.92)
        draw_text(cv, "WII · 2006 · CONTROL POR MOVIMIENTO", 240, 17 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        sub_txt = "ABUELOS · PADRES · CHICOS JUGANDO JUNTOS" if t >= t_abu else "LA CONSOLA PARA TODA LA FAMILIA"
        draw_text(cv, sub_txt, 240, 33 + dy_top, "silk", 8, CYAN, align="center", alpha=a_top)

    # Durante c7_02: ventana contador que sube a "+101 MILLONES DE CONSOLAS"
    if t >= t_c7_02 - 0.15:
        a_cnt, dy_cnt = pop(t, t_c7_02 - 0.15, 0.35)
        cnt_p = ease_out(prog(t, t_c7_02 - 0.05, t_c7_02 + 1.15))
        n_val = int(round(101 * cnt_p))
        window(cv, 64, 152 + dy_cnt, 352, 54, border=GOLD, alpha=0.95)
        draw_text(cv, f"+{n_val} MILLONES", 240, 161 + dy_cnt, "press", 16,
                  align="center", gradient=GOLD_RAMP, outline_w=2, alpha=a_cnt)
        draw_text(cv, "+101 MILLONES DE CONSOLAS", 240, 187 + dy_cnt, "press", 8,
                  CREAM, align="center", alpha=a_cnt)
        if cnt_p >= 0.95:
            for i in range(4):
                sparkle(cv, 84 + i * 104, 164 + (i % 2) * 18, t + i * 0.6, 3, GOLD)

    return vignette(cv, 0.3)


def sc_mobile(t):
    """c7_03: Pasajeros en el subte mirando sus teléfonos brillantes (56 % · JUEGO MÓVIL)."""
    base = bg("bg_subway_mobile_2010").copy()
    # Vaivén suave del vagón de subte
    sway_x = int(round(math.sin(t * 2.4) * 2))
    sway_y = int(round(abs(math.cos(t * 4.8)) * 1))
    cv = offset_canvas(base, sway_x, sway_y, fill=(10, 18, 24))

    t_tel = w("c7_03", "telefonos")
    t_mit = w("c7_03", "mitad")
    t_bol = w("c7_03", "bolsillo")

    # Luces de túnel pasando rápido por las ventanillas izquierdas
    d = ImageDraw.Draw(cv)
    tunnel_x = int((t * 260) % 180)
    if tunnel_x < 60:
        d.rectangle([58, 86, 134, 92], fill=(140, 235, 255, 70))
        d.rectangle([160, 92, 206, 97], fill=(140, 235, 255, 55))

    # Pasajeros en segunda fila (scale=2) y primer plano (scale=3) con teléfonos iluminando sus caras
    back_passengers = [
        ("sub_5", 220 + sway_x, 226 + sway_y, 0.0),
        ("sub_3", 282 + sway_x, 230 + sway_y, 0.2),
        ("sub_4", 338 + sway_x, 234 + sway_y, 0.35),
    ]
    for idx, (ck, px, py, delay) in enumerate(back_passengers):
        a_p, dy_p = pop(t, S2 + delay, 0.3)
        if a_p > 0:
            char(cv, CAST_CH7[ck], px, py + dy_p, t + idx, scale=2, alpha=a_p,
                 arms="hold", mood="happy", look=0)
            _draw_phone_glow(cv, px, py + dy_p, 2, t, seed=idx + 2)

    front_passengers = [
        ("sub_1", 104 + sway_x, 264 + sway_y, 0.05),
        ("sub_2", 392 + sway_x, 264 + sway_y, 0.15),
    ]
    for idx, (ck, px, py, delay) in enumerate(front_passengers):
        a_p, dy_p = pop(t, S2 + delay, 0.35)
        if a_p > 0:
            char(cv, CAST_CH7[ck], px, py + dy_p, t + idx * 0.5, scale=3, alpha=a_p,
                 arms="hold", mood="happy", look=0)
            _draw_phone_glow(cv, px, py + dy_p, 3, t, seed=idx)

    # La Máquina en el pasillo mirando también una pantallita brillante
    robot(cv, 248 + sway_x, 260 + sway_y, t, face="happy", scale=2)

    # Gran placa de estadística y barra: "56 % · JUEGO MÓVIL"
    a_bar, dy_bar = pop(t, S2 + 0.15, 0.4)
    if a_bar > 0:
        window(cv, 52, 10 + dy_bar, 376, 68, border=CYAN, alpha=0.94)
        bar_p = ease_out(prog(t, S2 + 0.25, t_mit + 0.4))
        pct = int(round(56 * bar_p))
        draw_text(cv, f"{pct} % · JUEGO MÓVIL" if bar_p < 0.98 else "56 % · JUEGO MÓVIL",
                  240, 18 + dy_bar, "press", 16, align="center", gradient=CYAN_RAMP, alpha=a_bar)
        # Barra de progreso segmentada (56 % del total de la industria)
        bx0, by0, bw, bh = 74, 42 + dy_bar, 332, 14
        d.rectangle([bx0, by0, bx0 + bw, by0 + bh], fill=(14, 22, 42, 255), outline=(*INK, 255))
        fill_w = int(round(bw * (0.56 * bar_p)))
        if fill_w > 2:
            d.rectangle([bx0 + 2, by0 + 2, bx0 + fill_w, by0 + bh - 2], fill=(*CYAN, 255))
            d.rectangle([bx0 + 2, by0 + 2, bx0 + fill_w, by0 + 5], fill=(195, 252, 255, 255))
        # Línea divisoria del 50 %
        x_half = bx0 + bw // 2
        d.line([(x_half, by0 - 2), (x_half, by0 + bh + 2)], fill=(*GOLD, 255))
        draw_text(cv, "MÁS DE LA MITAD DE LA INDUSTRIA EN EL BOLSILLO",
                  240, 62 + dy_bar, "silk", 8, CREAM, align="center", alpha=a_bar)

    return vignette(cv, 0.35)


def sc_minecraft(t):
    """c7_04: 2011 · Minecraft (+350 millones, el juego más vendido de la historia)."""
    cv = bg("bg_voxel_world_2011").copy()
    t_blo = w("c7_04", "bloques")
    t_mc = w("c7_04", "Minecraft")
    t_350 = w("c7_04", "trescientos")
    t_ven = w("c7_04", "vendido")

    # Construcción procedural por bloques sobre el paisaje voxel
    build_span = (t_350 + 0.4) - (S3 + 0.25)
    n_blocks = len(VOXEL_BUILD)
    for idx, (bx, by, bkind) in enumerate(VOXEL_BUILD):
        tb0 = S3 + 0.2 + (idx / n_blocks) * build_span
        a_b, dy_b = pop(t, tb0, 0.25)
        if a_b > 0:
            _draw_voxel_block(cv, bx, by, bkind, sz=14, alpha=a_b, dy=dy_b)
            if 0 < t - tb0 < 0.18:
                sparkle(cv, bx + 7, by + 4, t * 2 + idx, 2, GOLD)

    # Personaje constructor a la izquierda colocando bloques y La Máquina a la derecha
    building_now = t < t_350 + 0.5
    char(cv, CAST_CH7["builder"], 124, 254, t, scale=3,
         arms="wave" if building_now else "cheer", mood="happy", look=1)
    robot(cv, 372, 254, t, face="heart" if t >= t_mc else "happy", scale=2)

    # Placa superior: MINECRAFT · 2011 · +350 MILLONES
    a_top, dy_top = pop(t, S3 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 54, 10 + dy_top, 372, 44, border=GOLD if t >= t_mc else None, alpha=0.93)
        title_str = "MINECRAFT · 2011 · +350 MILLONES" if t >= t_mc - 0.1 else "2011 · UN MUNDO HECHO DE BLOQUES"
        draw_text(cv, title_str, 240, 18 + dy_top, "press", 8, GOLD, align="center", alpha=a_top)
        draw_text(cv, "EL JUEGO MÁS VENDIDO DE LA HISTORIA", 240, 34 + dy_top, "press", 8,
                  CYAN, align="center", alpha=a_top)

    # Contador de +350 millones en la parte inferior cuando se menciona la cifra
    if t >= t_350 - 0.2:
        a_c, dy_c = pop(t, t_350 - 0.2, 0.35)
        p_c = ease_out(prog(t, t_350 - 0.1, t_350 + 0.85))
        n_m = int(round(350 * p_c))
        window(cv, 84, 210 + dy_c, 312, 46, border=GOLD, alpha=0.95)
        draw_text(cv, f"+{n_m} MILLONES DE COPIAS", 240, 218 + dy_c, "press", 8,
                  GOLD, align="center", alpha=a_c)
        draw_text(cv, "RÉCORD MUNDIAL · +350 MILLONES", 240, 236 + dy_c, "silk", 8,
                  CREAM, align="center", alpha=a_c)
        if p_c >= 0.95:
            sparkle(cv, 102, 224, t, 3, GOLD)
            sparkle(cv, 378, 224, t + 1.1, 3, GOLD)

    return vignette(cv, 0.3)


def sc_gtav_launch(t):
    """c7_05: 17 · 09 · 2013 · GTA V — Fila nocturna frente a la tienda iluminada y festejo."""
    cv = bg("bg_midnight_launch_2013").copy()
    t_nom = w("c7_05", "nombre")
    t_gta = w("c7_05", "cinco") - 0.35

    # La puerta de la tienda (x≈276..304, y≈98..184) proyecta luz cálida al abrirse
    open_p = ease_out(prog(t, t_nom - 0.2, t_gta + 0.2))
    if open_p > 0:
        cv = spotlight(cv, 290, 96, 260, 26, 150, color=(255, 220, 120), strength=0.28 * open_p)

    # Fila de fanáticos esperando en la vereda nocturna; festejan cuando se menciona GTA V
    cheering = t >= t_gta - 0.1
    fans = [
        ("fan_1", 118, 254, 0.0),
        ("fan_2", 184, 256, 0.08),
        ("fan_3", 252, 258, 0.16),
        ("fan_4", 352, 256, 0.24),
    ]
    for idx, (fk, fx, fy, delay) in enumerate(fans):
        a_f, dy_f = pop(t, S4 + delay, 0.3)
        if a_f <= 0:
            continue
        arms = "cheer" if cheering else ("wave" if idx % 2 == 0 else "down")
        look = 1 if fx < 285 else -1
        char(cv, CAST_CH7[fk], fx, fy + dy_f, t + idx * 0.3, scale=3 if idx in (0, 3) else 2,
             alpha=a_f, arms=arms, mood="happy", look=look)

    robot(cv, 54, 254, t, face="heart" if cheering else "happy", scale=2)

    # Confeti y destellos al abrir las puertas de medianoche
    if cheering:
        CONF.draw(cv, t)

    # Placa superior: 17 · 09 · 2013 · GTA V
    a_top, dy_top = pop(t, S4 + 0.1, 0.35)
    if a_top > 0:
        window(cv, 88, 12 + dy_top, 304, 48, border=GOLD if cheering else CYAN, alpha=0.94)
        draw_text(cv, "17 · 09 · 2013 · GTA V", 240, 20 + dy_top, "press", 8,
                  GOLD, align="center", alpha=a_top)
        sub = "EL REGRESO DE GRAND THEFT AUTO" if cheering else "MEDIANOCHE · LANZAMIENTO MUNDIAL"
        draw_text(cv, sub, 240, 38 + dy_top, "silk", 8, CREAM, align="center", alpha=a_top)

    return vignette(cv, 0.35)


def sc_gtav_billion(t):
    """c7_06: Tablero explosivo de recaudación sobre la noche de estreno: US$ 1.000 MILLONES · 3 DÍAS."""
    cv = grade(bg("bg_midnight_launch_2013").copy(), mul=(0.55, 0.58, 0.72), add=(6, 8, 18), sat=0.75, k=0.8)
    t_mil = w("c7_06", "mil")
    t_pel = w("c7_06", "pelicula")
    t_dis = w("c7_06", "disco")
    t_rap = w("c7_06", "rapido")

    # Multitud festejando abajo y lluvia de confeti dorado
    CONF.draw(cv, t)
    for idx, (fk, fx) in enumerate((("fan_1", 72), ("fan_2", 156), ("fan_3", 324), ("fan_4", 408))):
        char(cv, CAST_CH7[fk], fx, 264, t + idx * 0.25, scale=2, arms="cheer", mood="happy")
    robot(cv, 240, 264, t, face="heart", scale=2)

    # Tablero central de recaudación que sube a toda velocidad hasta US$ 1.000 MILLONES · 3 DÍAS
    a_db, dy_db = pop(t, S5 + 0.05, 0.35)
    cnt_p = ease_out(prog(t, S5 + 0.1, t_mil + 0.35))
    val = int(round(1000 * cnt_p))
    val_str = "1.000" if val >= 1000 else f"{val}"

    window(cv, 36, 12 + dy_db, 408, 96, border=GOLD, alpha=0.95)
    draw_text(cv, "GTA V · RECAUDACIÓN EN 72 HORAS", 240, 20 + dy_db, "silk", 8,
              CYAN, align="center", alpha=a_db)
    draw_text(cv, f"US$ {val_str} MILLONES", 240, 36 + dy_db, "press", 16,
              align="center", gradient=GOLD_RAMP, outline_w=2, alpha=a_db)
    draw_text(cv, "US$ 1.000 MILLONES · 3 DÍAS", 240, 60 + dy_db, "press", 8,
              CREAM, align="center", alpha=a_db)

    # Insignia dorada de récord histórico
    d = ImageDraw.Draw(cv)
    d.rectangle([76, 76 + dy_db, 404, 98 + dy_db], fill=(28, 22, 48, 255), outline=(*GOLD, 255))
    draw_text(cv, "RÉCORD HISTÓRICO EN 72 HORAS", 240, 83 + dy_db, "press", 8,
              GOLD, align="center", alpha=a_db)

    if cnt_p >= 0.95:
        for i in range(6):
            sparkle(cv, 56 + i * 72, 28 + (i % 2) * 52, t * 1.4 + i, 3, GOLD)

    # Comparación con Cine y Música cuando dice "Ninguna película, ningún disco..."
    comp_items = [
        ("NINGUNA PELÍCULA", t_pel - 0.1, 44),
        ("NINGÚN DISCO", t_dis - 0.1, 246),
    ]
    for label, t0_c, x_box in comp_items:
        if t >= t0_c:
            a_c, dy_c = pop(t, t0_c, 0.3)
            window(cv, x_box, 118 + dy_c, 190, 34, border=CYAN, alpha=0.92)
            draw_text(cv, label, x_box + 95, 126 + dy_c, "press", 8, GREY, align="center", alpha=a_c)
            draw_text(cv, "SUPERADO EN 3 DÍAS", x_box + 95, 139 + dy_c, "silk", 8, GOLD, align="center", alpha=a_c)

    if t >= t_rap - 0.25:
        a_r, dy_r = pop(t, t_rap - 0.25, 0.35)
        window(cv, 72, 160 + dy_r, 336, 28, border=GOLD, alpha=0.94)
        draw_text(cv, "EL ESTRENO MÁS RÁPIDO DE LA HISTORIA", 240, 170 + dy_r, "press", 8,
                  CYAN, align="center", alpha=a_r)

    return vignette(cv, 0.35)


# =========================================================================== montaje

def scenes():
    return [
        (T_CARD - 0.3, make_card(CH, ["TODOS JUEGAN"], "2006 – 2016", robot_face="happy"), None),
        (S1, sc_wii, lambda t: (
            cam_push(t, S1, S2, 1.0, 1.05, (240, 135), (240, 140))[0]
            + cam_punch(t, [w("c7_01", "Abuelos"), w("c7_01", "Padres"), w("c7_01", "Chicos"), TL.s("c7_02")], 0.05),
            240, 138
        )),
        (S2, sc_mobile, lambda t: (
            cam_push(t, S2, S3, 1.0, 1.06, (240, 135), (240, 130))[0]
            + cam_punch(t, [w("c7_03", "mitad"), w("c7_03", "bolsillo")], 0.05),
            240, 135
        )),
        (S3, sc_minecraft, lambda t: (
            cam_push(t, S3, S4, 1.0, 1.06, (240, 135), (235, 145))[0]
            + cam_punch(t, [w("c7_04", "Minecraft"), w("c7_04", "trescientos")], 0.06),
            240, 140
        )),
        (S4, sc_gtav_launch, lambda t: (
            cam_push(t, S4, S5, 1.0, 1.07, (240, 135), (255, 142))[0]
            + cam_punch(t, [w("c7_05", "cinco") - 0.3], 0.07),
            245, 138
        )),
        (S5, sc_gtav_billion, lambda t: (
            1.0 + cam_punch(t, [w("c7_06", "mil"), w("c7_06", "pelicula"), w("c7_06", "disco"), w("c7_06", "rapido")], 0.06),
            240, 135
        )),
    ]


# =========================================================================== música y efectos

def music(A):
    # Wii + Móviles: melodía brillante y alegre ("Todos juegan")
    A.section(T_CARD + 1.6, S3, 118, [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_bright)
    A.sting(TL.s("c7_02"), [72, 76, 79, 84], vol=0.045, step=0.10, hold=0.9)
    # Minecraft: pulso creativo de construcción
    A.section(S3, S4, 112, [("F", "maj"), ("C", "maj"), ("G", "maj"), ("A", "min")], A.st_summer_lead)
    A.sting(w("c7_04", "Minecraft"), [69, 72, 76, 81], vol=0.045, step=0.11, hold=1.0)
    # GTA V lanzamiento y récord de mil millones: triunfo enérgico
    A.section(S4, T_END, 124, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_triumph)
    t_mil = w("c7_06", "mil")
    A.kick(A.music, t_mil, 0.42)
    A.crash(A.music, t_mil, 0.16)
    A.sting(t_mil, [60, 64, 67, 72, 76, 79, 84], vol=0.05, step=0.09, hold=1.4)


def sfx(A):
    # Escena 1: Wii
    A.whoosh(S1 + 0.1, 0.35, 0.05)
    for k in ("Abuelos", "Padres", "Chicos"):
        A.pop_sfx(w("c7_01", k), 520, 0.06)
    A.whoosh(w("c7_01", "moviendo"), 0.35, 0.055)
    A.coin(TL.s("c7_02") + 0.25, 0.065)
    for i in range(6):
        A.blip(TL.s("c7_02") + i * 0.14, 700 + i * 90, vol=0.025)

    # Escena 2: Juego móvil en el subte
    A.whoosh(S2 + 0.05, 0.4, 0.05)
    A.pop_sfx(w("c7_03", "telefonos"), 640, 0.055)
    for i in range(5):
        A.blip(w("c7_03", "mitad") + i * 0.12, 820 + i * 80, vol=0.028)
    A.coin(w("c7_03", "bolsillo"), 0.06)

    # Escena 3: Minecraft (bloques que se colocan uno por uno)
    A.whoosh(S3 + 0.05, 0.35, 0.05)
    for i in range(10):
        A.pop_sfx(S3 + 0.35 + i * 0.42, 420 + (i % 4) * 80, 0.035)
    A.join_jingle(w("c7_04", "Minecraft"), 0.055)
    A.coin(w("c7_04", "trescientos") + 0.3, 0.065)

    # Escena 4: Lanzamiento de medianoche GTA V
    A.whoosh(S4 + 0.05, 0.4, 0.05)
    A.pop_sfx(w("c7_05", "diecisiete"), 520, 0.05)
    A.join_jingle(w("c7_05", "cinco") - 0.3, 0.06)

    # Escena 5: US$ 1.000 millones en 3 días
    A.whoosh(S5 + 0.05, 0.4, 0.055)
    A.coin_cascade(S5 + 0.15, dur=1.4, count=16, vol=0.045)
    A.pop_sfx(w("c7_06", "pelicula"), 600, 0.055)
    A.pop_sfx(w("c7_06", "disco"), 680, 0.055)
    A.coin(w("c7_06", "rapido"), 0.065)
