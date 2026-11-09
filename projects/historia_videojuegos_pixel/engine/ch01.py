"""Apertura + Capítulo 1: El juego que nadie patentó (1958 – 1962)."""
from common import *  # noqa

PHOS = (100, 255, 140)
PHOS_BRIGHT = (220, 255, 230)
PHOS_MID = (52, 168, 86)
PHOS_DIM = (18, 64, 34)
PHOS_BG = (4, 16, 8)
PHOS_RAMP = [(230, 255, 236), (140, 255, 170), (80, 220, 118), (38, 150, 72)]
NEON_PINK = (255, 76, 168)
NEON_CYAN = (80, 240, 255)
NEON_GOLD = (255, 214, 92)

C = S.hexc
SKIN = S.SKIN

HIGINBOTHAM = dict(
    name="William Higinbotham", skin=SKIN["fair"], hair=C("5a4636"), hair_style="recede",
    glasses="black", top="shirt", top_color=C("f2efe6"), tie=C("284838"), pants=C("383c38"),
)
TECH_1959 = dict(
    name="Técnico Brookhaven", skin=SKIN["light"], hair=C("3a2c22"), hair_style="short",
    glasses="wire", top="labcoat", top_color=C("d8dfd6"), shirt=C("e8ece8"), tie=C("22382c"), pants=C("343a36"),
)
KID_1958 = dict(
    name="Niño visitante", skin=SKIN["fair"], hair=C("8a542e"), hair_style="crew",
    top="sweater", top_color=C("387854"), shirt=C("f0eee4"), pants=C("2e3846"),
)
VISITOR_A = dict(
    name="Visitante A", skin=SKIN["light"], hair=C("4e3222"), hair_style="bun",
    top="shirt", top_color=C("d68c72"), skirt=True, skirt_color=C("3c4c5a"), pants=C("3c4c5a"),
)
VISITOR_B = dict(
    name="Visitante B", skin=SKIN["fair"], hair=C("2c2420"), hair_style="side",
    glasses="round", top="suit", top_color=C("525852"), shirt=C("efece2"), tie=C("78322c"), pants=C("383c38"),
)
VISITOR_C = dict(
    name="Visitante C", skin=SKIN["tan"], hair=C("221c1a"), hair_style="wavy",
    top="blazer", top_color=C("6e5840"), shirt=C("ece6d8"), pants=C("42382e"),
)
VISITOR_D = dict(
    name="Visitante D", skin=SKIN["light"], hair=C("7a4828"), hair_style="bangs",
    top="sweater", top_color=C("486878"), pants=C("303844"),
)
RUSSELL_MIT = dict(
    name="Steve Russell", skin=SKIN["fair"], hair=C("4a3626"), hair_style="side",
    glasses="black", top="shirt", top_color=C("dce8e0"), tie=C("203c30"), pants=C("323836"),
)
MIT_PROG_2 = dict(
    name="Programador MIT 2", skin=SKIN["light"], hair=C("2a221e"), hair_style="short",
    glasses="wire", top="vest", top_color=C("465e52"), shirt=C("eef2ee"), tie=C("1e2c26"), pants=C("2e3432"),
)
MIT_PROG_3 = dict(
    name="Programador MIT 3", skin=SKIN["fair"], hair=C("6e4c30"), hair_style="curly",
    top="sweater", top_color=C("2e4a44"), shirt=C("e8ece8"), pants=C("303438"),
)


# =========================================================================== helpers locales


def draw_phos_grid(cv, x0=0, y0=0, x1=W, y1=H, step=24, col=(8, 30, 16), axis_col=(18, 58, 30)):
    d = ImageDraw.Draw(cv)
    for x in range(x0, x1 + 1, step):
        d.line([(x, y0), (x, y1)], fill=(*col, 255))
    for y in range(y0, y1 + 1, step):
        d.line([(x0, y), (x1, y)], fill=(*col, 255))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(x0, cy), (x1, cy)], fill=(*axis_col, 255))
    d.line([(cx, y0), (cx, y1)], fill=(*axis_col, 255))
    for x in range(x0, x1 + 1, 6):
        d.line([(x, cy - 2), (x, cy + 2)], fill=(*axis_col, 255))
    for y in range(y0, y1 + 1, 6):
        d.line([(cx - 2, y), (cx + 2, y)], fill=(*axis_col, 255))


def phos_window(cv, x, y, w, h, alpha=0.92):
    window(cv, x, y, w, h, fill=(6, 22, 12), border=PHOS, alpha=alpha, inner=(24, 90, 46))


def tennis_ball_pos(t, t0, x_left, x_right, y_court, arc_h, period=1.1):
    """Devuelve (x, y, trail) de la pelota de Tennis for Two rebotando de lado a lado."""
    dt = max(0.0, t - t0)
    u = (dt / period) % 2.0
    going_right = u < 1.0
    p = u if going_right else (2.0 - u)
    bx = x_left + (x_right - x_left) * p
    # Dos rebotes por cruce: toca la cancha de un lado, pasa sobre la red y pica del otro
    sub = (dt / period) % 1.0
    by = y_court - abs(math.sin(sub * math.pi)) * arc_h
    trail = []
    for k in range(7, 0, -1):
        td = max(0.0, dt - k * 0.032)
        uu = (td / period) % 2.0
        pp = uu if uu < 1.0 else (2.0 - uu)
        tx = x_left + (x_right - x_left) * pp
        tsub = (td / period) % 1.0
        ty = y_court - abs(math.sin(tsub * math.pi)) * arc_h
        trail.append((tx, ty))
    return bx, by, trail


def s01_bounces():
    t0 = 0.55
    step = 0.68
    out = []
    tt = t0
    while tt < TL.s("s02") - 0.35:
        out.append(round(tt, 3))
        tt += step
    return out


def draw_controller_box(cv, x, y, w, h, angle_deg, btn_pressed, label_knob="ÁNGULO", label_btn="BOTÓN", show_hand=False):
    """Caja metálica de control de Tennis for Two con perilla rotatoria y botón pulsador."""
    d = ImageDraw.Draw(cv)
    # Sombra y gabinete de aluminio
    d.rectangle([x + 3, y + 3, x + w + 3, y + h + 3], fill=(0, 0, 0, 140))
    d.rectangle([x, y, x + w, y + h], fill=(56, 74, 62, 255), outline=(*INK, 255))
    d.rectangle([x + 2, y + 2, x + w - 2, y + 5], fill=(92, 118, 100, 255))
    d.rectangle([x + 3, y + 6, x + w - 3, y + h - 3], fill=(34, 48, 40, 255), outline=(20, 30, 24, 255))
    # Tornillos en las esquinas
    for sx, sy in ((x + 6, y + 9), (x + w - 6, y + 9), (x + 6, y + h - 6), (x + w - 6, y + h - 6)):
        d.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=(130, 155, 138, 255))

    # Perilla de ángulo (izquierda)
    kx, ky, kr = x + 34, y + 29, 14
    for a_deg in range(-135, 136, 30):
        rad = math.radians(a_deg - 90)
        tx0 = kx + int(math.cos(rad) * (kr + 2))
        ty0 = ky + int(math.sin(rad) * (kr + 2))
        tx1 = kx + int(math.cos(rad) * (kr + 4))
        ty1 = ky + int(math.sin(rad) * (kr + 4))
        d.line([(tx0, ty0), (tx1, ty1)], fill=(*PHOS, 200))
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(24, 34, 28, 255), outline=(140, 175, 150, 255))
    d.ellipse([kx - kr + 3, ky - kr + 3, kx + kr - 3, ky + kr - 3], fill=(44, 60, 50, 255))
    rad = math.radians(angle_deg - 90)
    px = kx + int(math.cos(rad) * (kr - 4))
    py = ky + int(math.sin(rad) * (kr - 4))
    d.line([(kx, ky), (px, py)], fill=(*PHOS_BRIGHT, 255), width=2)
    d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(*PHOS, 255))
    draw_text(cv, label_knob, kx, y + h - 13, "silk", 8, PHOS, align="center")

    # Botón de golpe (derecha)
    bx, by = x + w - 34, y + 28
    d.ellipse([bx - 13, by - 10, bx + 13, by + 10], fill=(22, 30, 24, 255), outline=(130, 160, 140, 255))
    off_y = 3 if btn_pressed else 0
    bcol = (120, 255, 150) if btn_pressed else (210, 64, 58)
    btop = (200, 255, 215) if btn_pressed else (250, 120, 110)
    d.rectangle([bx - 9, by - 8 + off_y, bx + 9, by + 4], fill=(*bcol, 255), outline=(*INK, 255))
    d.rectangle([bx - 7, by - 7 + off_y, bx + 7, by - 4 + off_y], fill=(*btop, 255))
    if btn_pressed:
        for r_glow, a_glow in ((18, 45), (14, 80)):
            d.ellipse([bx - r_glow, by - r_glow, bx + r_glow, by + r_glow], fill=(*PHOS, a_glow))
    draw_text(cv, label_btn, bx, y + h - 13, "silk", 8, CREAM, align="center")

    if show_hand:
        # Mano pixelada girando perilla y dedo presionando el botón
        hx = kx - 14 + int(math.sin(math.radians(angle_deg)) * 4)
        hy = ky + 6
        d.rectangle([hx - 6, hy, hx + 6, hy + 12], fill=(*SKIN["fair"], 255), outline=(*INK, 255))
        d.rectangle([hx - 4, hy - 5, hx + 3, hy + 1], fill=(*SKIN["fair"], 255), outline=(*INK, 255))
        # Dedo sobre el botón
        fy = by - 18 + (4 if btn_pressed else 0)
        d.rectangle([bx - 4, fy - 10, bx + 4, fy + 2], fill=(*SKIN["fair"], 255), outline=(*INK, 255))
        d.rectangle([bx - 6, fy - 16, bx + 6, fy - 8], fill=(220, 230, 220, 255), outline=(*INK, 255))


# =========================================================================== APERTURA (s01 .. s08)


def sc_s01_dot(t):
    """s01: Pantalla negra con grilla sutil, punto de fósforo rebotando y fecha tipeada."""
    cv = new_canvas((2, 8, 4))
    draw_phos_grid(cv, 24, 18, 456, 200, step=24, col=(6, 24, 12), axis_col=(14, 48, 24))
    d = ImageDraw.Draw(cv)
    # Línea de suelo de fósforo sutil donde rebota el punto
    ground_y = 164
    d.line([(84, ground_y + 4), (396, ground_y + 4)], fill=(26, 96, 48, 255), width=1)

    t0 = 0.55
    step = 0.68
    if t >= 0.15:
        dt = max(0.0, t - t0)
        u = dt / step
        cyc = int(u)
        frac = u - cyc
        # Rebote rítmico de izquierda a derecha y vuelta
        waypoints = [150, 210, 270, 330, 270, 210]
        x_a = waypoints[cyc % len(waypoints)]
        x_b = waypoints[(cyc + 1) % len(waypoints)]
        bx = x_a + (x_b - x_a) * frac
        by = ground_y - abs(math.sin(frac * math.pi)) * 68
        trail = []
        for k in range(8, 0, -1):
            td = max(0.0, dt - k * 0.03)
            tu = td / step
            tcyc = int(tu)
            tfrac = tu - tcyc
            xa = waypoints[tcyc % len(waypoints)]
            xb = waypoints[(tcyc + 1) % len(waypoints)]
            tx = xa + (xb - xa) * tfrac
            ty = ground_y - abs(math.sin(tfrac * math.pi)) * 68
            trail.append((tx, ty))
        # Ondas en el punto de impacto cuando rebota
        if frac < 0.18:
            rk = int(4 + frac * 70)
            ak = int(180 * (1 - frac / 0.18))
            d.ellipse([int(x_a) - rk, ground_y + 2 - rk // 3, int(x_a) + rk, ground_y + 2 + rk // 3],
                      outline=(*PHOS, ak))
        draw_phosphor_dot(cv, bx, by, r=4, trail=trail, color=PHOS)

    # Año grande en rampa verde fósforo
    t_year = TL.word("s01", "mil")
    if t >= t_year - 0.1:
        bigyear(cv, "1958", 240, 24, t, t_year - 0.1, size=32, ramp=PHOS_RAMP)

    # Placa inferior con fecha y lugar tipeados con cursor
    txt = "18 · 10 · 1958 · LONG ISLAND, NUEVA YORK"
    n_rev = int(max(0.0, (t - 0.75) * 14.0))
    phos_window(cv, 44, 210, 392, 36)
    shown = txt[:min(len(txt), n_rev)]
    draw_text(cv, txt, 60, 224, "press", 8, PHOS_BRIGHT, align="left", reveal=n_rev)
    if n_rev > 0:
        tw, _ = text_size(shown, "press", 8)
        cx_cur = min(422, 60 + tw + 3)
        if int(t * 6) % 2 == 0 or n_rev < len(txt):
            d.rectangle([cx_cur, 223, cx_cur + 6, 232], fill=(*PHOS, 255))
    return vignette(cv, 0.4)


def sc_s02_brookhaven(t):
    """s02: Laboratorio Brookhaven 1958. Físico dibujando planos bajo la lámpara."""
    cv = bg("bg_brookhaven_lab_1958").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("s02")
    t_bomba = TL.word("s02", "bomba")
    t_visitas = TL.word("s02", "visitas")
    t_aburren = TL.word("s02", "aburren")

    # Onda sinusoidal verde de fósforo estrictamente dentro del CRT del osciloscopio sobre la mesa (x=293..311, y=148..166)
    d.rectangle([293, 148, 311, 166], fill=(6, 26, 14, 235))
    wave_pts = []
    for dx in range(17):
        wy = 157 + int(round(math.sin(t * 7.5 + dx * 0.55) * 5))
        wave_pts.append((294 + dx, max(150, min(164, wy))))
    d.line(wave_pts, fill=(*PHOS_BRIGHT, 245), width=1)

    # Físico dibujando planos en el banco de trabajo bajo la lámpara
    char(cv, HIGINBOTHAM, 118, 266, t, scale=3, arms="write",
         talk=talk_v(t, t0 < t < t_visitas), mood="neutral" if t < t_aburren else "happy", look=1)

    # Trazos oscuros de grafito sobre la hoja de papel del escritorio mientras dibuja
    p_draw = prog(t, t0 + 0.3, t_visitas)
    scribble(cv, 198, 202, int(44 * p_draw), 1.0, seed=1.4, color=(64, 56, 44))

    # Ventana superior derecha: el problema de las visitas aburridas
    if t >= t0 + 1.4:
        a, dy = pop(t, t0 + 1.4)
        phos_window(cv, 214, 16 + dy, 250, 44)
        draw_text(cv, "DÍA DE VISITAS ANUAL", 339, 24 + dy, "press", 8, PHOS, align="center", alpha=a)
        draw_text(cv, "PROBLEMA: ¡SE ABURREN!", 339, 40 + dy, "press", 8, GOLD, align="center",
                  reveal=(t - t0 - 1.8) * 28)

    lower_third(cv, "WILLIAM HIGINBOTHAM", "FÍSICO · LABORATORIO BROOKHAVEN", t, t0, TL.e("s02"), x=24, y=214)
    return vignette(cv, 0.35)


def sc_s03_oscilloscope(t):
    """s03: Primer plano del osciloscopio redondo de 5 pulgadas dibujando cancha, red y pelota."""
    cv = new_canvas((4, 12, 8))
    draw_phos_grid(cv, 0, 0, W, H, step=32, col=(6, 20, 11), axis_col=(10, 32, 18))
    d = ImageDraw.Draw(cv)

    t0 = TL.s("s03")
    t_cinco = TL.word("s03", "cinco")
    t_dibuja = TL.word("s03", "dibuja")

    # Gabinete metálico frontal del osciloscopio redondo (centrado en cx=240, cy=124, r=82)
    cx, cy, r = 240, 124, 82
    d.rectangle([128, 28, 352, 232], fill=(38, 52, 42, 255), outline=(*INK, 255))
    d.rectangle([132, 32, 348, 228], fill=(28, 40, 32, 255), outline=(74, 96, 80, 255))
    # Bisel circular del tubo de 5 pulgadas
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(64, 82, 68, 255), outline=(*INK, 255))
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=(20, 32, 24, 255), outline=(120, 150, 128, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(4, 18, 9, 255), outline=(*PHOS_MID, 255))

    # Grilla interna del CRT redondo
    for gx in range(cx - 60, cx + 61, 20):
        h_chord = int(math.sqrt(max(0, r * r - (gx - cx) ** 2)))
        d.line([(gx, cy - h_chord + 4), (gx, cy + h_chord - 4)], fill=(10, 42, 22, 255))
    for gy in range(cy - 60, cy + 61, 20):
        w_chord = int(math.sqrt(max(0, r * r - (gy - cy) ** 2)))
        d.line([(cx - w_chord + 4, gy), (cx + w_chord - 4, gy)], fill=(10, 42, 22, 255))

    # 1) Línea horizontal de la cancha
    p_court = prog(t, t0 + 0.3, t0 + 1.4)
    court_y = cy + 34
    if p_court > 0:
        x_end = int((cx - 64) + 128 * ease_out(p_court))
        d.line([(cx - 64, court_y), (x_end, court_y)], fill=(*PHOS, 255), width=2)
        d.line([(cx - 64, court_y - 1), (x_end, court_y - 1)], fill=(*PHOS, 90), width=4)

    # 2) Línea vertical de la red
    p_net = prog(t, t0 + 1.2, t0 + 2.1)
    if p_net > 0:
        y_top = int(court_y - 26 * ease_out(p_net))
        d.line([(cx, court_y), (cx, y_top)], fill=(*PHOS, 255), width=2)

    # 3) Pelota de luz rebotando en arco sobre la red
    t_ball_start = t0 + 2.0
    if t >= t_ball_start:
        bx, by, trail = tennis_ball_pos(t, t_ball_start, cx - 56, cx + 56, court_y - 2, 48, period=0.95)
        draw_phosphor_dot(cv, bx, by, r=3, trail=trail, color=PHOS)

    # Manos y controles analógicos a izquierda y derecha en la parte inferior
    ang = math.sin(t * 3.5) * 48
    pressed = int((t - t0) / 0.475) % 2 == 1 and t >= t_ball_start
    draw_controller_box(cv, 12, 182, 126, 68, ang, pressed, "ÁNGULO", "BOTÓN", show_hand=True)
    draw_controller_box(cv, 342, 182, 126, 68, -ang * 0.8, not pressed and t >= t_ball_start, "ÁNGULO", "BOTÓN", show_hand=True)

    # Etiqueta superior
    phos_window(cv, 104, 8, 272, 26)
    draw_text(cv, "OSCILOSCOPIO · 5 PULGADAS", 240, 15, "press", 8, PHOS_BRIGHT, align="center",
              reveal=(t - t0) * 28)
    return vignette(cv, 0.35)


def sc_s04_visitors(t):
    """s04: Sala de visitantes en Brookhaven 1958. Larga fila y niño señalando el osciloscopio."""
    cv = bg("bg_visitors_hall_1958").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("s04")

    # Limpiamos la onda estática del fondo dentro del círculo del CRT (cx=342, cy=105, r=19) y dibujamos cancha, red y pelota adentro
    ox, oy, orad = 342, 105, 19
    d.ellipse([ox - orad, oy - orad, ox + orad, oy + orad], fill=(8, 28, 16, 255))
    for gx in range(ox - 12, ox + 13, 6):
        d.line([(gx, oy - 14), (gx, oy + 14)], fill=(14, 46, 26, 255))
    for gy in range(oy - 12, oy + 13, 6):
        d.line([(ox - 14, gy), (ox + 14, gy)], fill=(14, 46, 26, 255))
    d.line([(ox - 14, oy + 8), (ox + 14, oy + 8)], fill=(*PHOS, 240), width=1)
    d.line([(ox, oy + 8), (ox, oy - 2)], fill=(*PHOS, 240), width=1)
    bx, by, trail = tennis_ball_pos(t, t0 - 0.5, ox - 12, ox + 12, oy + 7, 11, period=0.75)
    draw_phosphor_dot(cv, bx, by, r=2, trail=trail[-4:], color=PHOS)

    # Fila de visitantes de 1958 en primer plano (scale=3, proporcionados con el salón y la mesa)
    queue = [
        (VISITOR_C, 42, 262, 0.0),
        (VISITOR_B, 100, 262, 0.14),
        (VISITOR_A, 158, 262, 0.28),
        (HIGINBOTHAM, 216, 262, 0.42),
    ]
    for spec, qx, qfeet, delay in queue:
        a, dy = pop(t, t0 - 0.15 + delay, 0.3)
        if a > 0:
            char(cv, spec, qx, qfeet + dy, t, scale=3, alpha=a, facing=1, look=1,
                 mood="happy", arms="wave" if delay == 0.28 and t > t0 + 0.8 else "down")

    # Niño adelante (scale=2, altura infantil natural frente a los adultos scale=3) señalando el osciloscopio
    hop = int(abs(math.sin(t * 8)) * 4)
    char(cv, KID_1958, 268, 262 - hop, t, scale=2, facing=1, look=1, arms="point", mood="happy")
    bubble(cv, "¡YO SIGO!", 268, 152 - hop, size=8, reveal=(t - t0 - 0.2) * 24)

    # Placa superior
    phos_window(cv, 20, 12, 264, 30)
    draw_text(cv, "FILAS DE VISITANTES · 1958", 152, 21, "press", 8, PHOS_BRIGHT, align="center",
              reveal=(t - t0 + 0.1) * 28)
    return vignette(cv, 0.3)


def sc_s05_nopatent(t):
    """s05: Corte seco a negro. Placa central en tipografía bold: 'NUNCA LO PATENTÓ'."""
    cv = new_canvas((0, 0, 0))
    t0 = TL.s("s05")
    a, dy = pop(t, t0 - 0.05, 0.3)
    if a > 0:
        phos_window(cv, 40, 96 + dy, 400, 74, alpha=0.95)
        draw_text(cv, "NUNCA LO PATENTÓ", 240, 122 + dy, "press", 16, align="center",
                  gradient=PHOS_RAMP, alpha=a)
        # Pequeño punto de fósforo solitario debajo del texto
        draw_phosphor_dot(cv, 240, 152 + dy, r=2, color=PHOS)
    return cv


def draw_neon_coast_live(t, reveal_bg=1.0):
    """Dibuja bg_neon_coast_2026 con autos animados en la avenida y carteles de neón parpadeando."""
    base = new_canvas((6, 10, 20))
    if reveal_bg > 0:
        coast = bg("bg_neon_coast_2026").copy()
        base = dither_mix(base, coast, reveal_bg)
    d = ImageDraw.Draw(base)
    if reveal_bg > 0.5:
        # Carteles de neón parpadeando en los edificios de la derecha
        neon_signs = [
            (366, 82, 376, 118, NEON_PINK, 0),
            (412, 68, 422, 112, NEON_CYAN, 1),
            (444, 48, 454, 106, NEON_GOLD, 2),
        ]
        for x0, y0, x1, y1, col, idx in neon_signs:
            if (int(t * 4) + idx) % 3 != 0:
                d.rectangle([x0, y0, x1, y1], outline=(*col, 220), width=1)
                d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], outline=(*col, 70), width=1)

        # Autos pixelados circulando por la avenida costera (x=290..465, y=165..265)
        for i in range(3):
            u = ((t * 0.28 + i * 0.33) % 1.0)
            # Perspectiva desde el fondo (292, 164) hacia adelante (445, 258)
            cx = int(292 + u * 150)
            cy = int(164 + u * 92)
            cw = max(6, int(6 + u * 18))
            ch = max(4, int(3 + u * 9))
            car_col = (240, 70, 150) if i % 2 == 0 else (70, 215, 250)
            d.rectangle([cx - cw // 2, cy - ch, cx + cw // 2, cy], fill=(*car_col, 255), outline=(*INK, 255))
            # Luces delanteras / traseras y reflejo en el asfalto húmedo
            d.rectangle([cx - cw // 2 + 1, cy - 2, cx - cw // 2 + 3, cy - 1], fill=(255, 245, 190, 255))
            d.rectangle([cx + cw // 2 - 3, cy - 2, cx + cw // 2 - 1, cy - 1], fill=(255, 80, 100, 255))
            d.line([(cx - cw // 3, cy + 3), (cx + cw // 3, cy + 3)], fill=(*car_col, 130))
    return base


def sc_s06_revenue(t):
    """s06: El punto verde cruza la pantalla y se transforma en el sol neón de 2026; contador 1958->2026 y US$ 201.600 MILLONES."""
    t0 = TL.s("s06") - 0.2
    t_sesenta = TL.s("s06")
    t_punto = TL.word("s06", "punto")
    t_mueve = TL.word("s06", "mueve")
    t_dosc = TL.word("s06", "doscientos")

    # Transición: el punto de fósforo cruza hasta el sol del atardecer (cx=100, cy=128) y revela la costa neón
    p_morph = ease_in_out(prog(t, t0, t0 + 1.15))
    cv = draw_neon_coast_live(t, reveal_bg=prog(t, t0 + 0.55, t0 + 1.35))
    d = ImageDraw.Draw(cv)

    if p_morph < 1.0:
        bx = int(240 + (100 - 240) * p_morph)
        by = int(135 + (128 - 135) * p_morph - math.sin(p_morph * math.pi) * 36)
        r_dot = int(4 + p_morph * 28)
        col_dot = tuple(int(PHOS[i] + (NEON_GOLD[i] - PHOS[i]) * p_morph) for i in range(3))
        trail = []
        for k in range(6, 0, -1):
            pm = max(0.0, p_morph - k * 0.06)
            tx = int(240 + (100 - 240) * pm)
            ty = int(135 + (128 - 135) * pm - math.sin(pm * math.pi) * 36)
            trail.append((tx, ty))
        draw_phosphor_dot(cv, bx, by, r=r_dot, trail=trail, color=col_dot)
    else:
        # Pulso luminoso alrededor del sol del horizonte
        for r_sun, a_sun in ((58, 35), (48, 55)):
            d.ellipse([100 - r_sun, 128 - r_sun, 100 + r_sun, 128 + r_sun], fill=(255, 190, 90, a_sun))

    # Ventana de contadores: AÑO 1958 -> 2026 y FACTURACIÓN ANUAL -> US$ 201.600 MILLONES
    p_yr = ease_out(prog(t, t_sesenta, t_punto + 0.4))
    yr = int(round(1958 + (2026 - 1958) * p_yr))
    window(cv, 22, 14, 436, 78, fill=(18, 14, 38), border=NEON_CYAN, inner=(70, 44, 120))
    draw_text(cv, f"AÑO: {yr}", 40, 26, "press", 16, NEON_CYAN)
    draw_text(cv, "+68 AÑOS", 352, 30, "press", 8, GOLD, align="center")

    if t >= t_mueve - 0.2:
        p_rev = ease_out(prog(t, t_mueve - 0.1, t_dosc + 0.9))
        val = int(round(201600 * p_rev))
        s_val = f"{val:,}".replace(",", ".")
        draw_text(cv, "INDUSTRIA GLOBAL ANUAL:", 40, 50, "silk", 8, CREAM)
        draw_text(cv, f"US$ {s_val} MILLONES", 40, 64, "press", 16, gradient=GOLD_RAMP)
    return vignette(cv, 0.3)


def sc_s07_countdown(t):
    """s07: Costa neón 2026 con cartel luminoso parpadeante 'CUENTA REGRESIVA · 2026'."""
    cv = draw_neon_coast_live(t, reveal_bg=1.0)
    t0 = TL.s("s07")
    a, dy = pop(t, t0 - 0.1, 0.35)
    blink_on = int(t * 5) % 2 == 0
    border_col = NEON_PINK if blink_on else NEON_CYAN

    window(cv, 32, 18 + dy, 416, 76, fill=(22, 12, 42), border=border_col, inner=(90, 40, 130))
    draw_text(cv, "CUENTA REGRESIVA · 2026", 240, 30 + dy, "press", 16,
              NEON_GOLD if blink_on else CREAM, align="center")
    draw_text(cv, "EL MUNDO ENTERO ESPERA UN SOLO JUEGO", 240, 54 + dy, "press", 8,
              NEON_CYAN, align="center", reveal=(t - t0) * 28)

    # Reloj digital de cuenta regresiva en la esquina inferior izquierda
    window(cv, 24, 206, 212, 44, fill=(14, 10, 30), border=GOLD)
    days = max(1, 30 - int((t - t0) * 7) % 30)
    draw_text(cv, "LANZAMIENTO GLOBAL", 130, 214, "silk", 8, GREY, align="center")
    draw_text(cv, f"FALTAN {days:02d} DÍAS", 130, 228, "press", 8, GOLD, align="center")
    return vignette(cv, 0.3)


def sc_s08_title(t):
    """s08: Cielo estrellado nocturno y gran placa de título con la pelota de fósforo rebotando sobre las letras."""
    cv = vgradient((4, 8, 20), (14, 34, 48), 14)
    STARS.draw(cv, t, alpha=0.9)
    draw_phos_grid(cv, 0, 198, W, H, step=20, col=(8, 34, 22), axis_col=(18, 68, 40))

    t0 = TL.s("s08")
    t_hist = TL.word("s08", "historia")
    t_vid = TL.word("s08", "videojuegos")

    phos_window(cv, 24, 44, 432, 142, alpha=0.9)
    draw_text(cv, "LA HISTORIA DE LOS", 240, 66, "press", 16, CREAM, align="center",
              reveal=(t - t_hist + 0.3) * 26)

    if t >= t_vid - 0.25:
        p = prog(t, t_vid - 0.25, t_vid + 0.15)
        yy = int(104 + (1 - ease_out_back(p)) * 24)
        draw_text(cv, "VIDEOJUEGOS", 240, yy, "press", 32, align="center",
                  gradient=GOLD_RAMP, outline_w=2, alpha=min(1.0, p * 2.5))
        draw_text(cv, "1958 · 2026 · PARA QUE NO SE ABURRAN", 240, 156, "press", 8,
                  PHOS, align="center", reveal=(t - t0 - 0.5) * 42)

    # Pelota verde fósforo rebotando sobre las letras de VIDEOJUEGOS
    dt = max(0.0, t - t0)
    u = (dt * 1.45) % 2.0
    p_x = u if u < 1.0 else (2.0 - u)
    bx = int(68 + p_x * 344)
    by = int(96 - abs(math.sin(dt * 7.2)) * 34)
    trail = []
    for k in range(7, 0, -1):
        td = max(0.0, dt - k * 0.03)
        uu = (td * 1.45) % 2.0
        px = uu if uu < 1.0 else (2.0 - uu)
        tx = int(68 + px * 344)
        ty = int(96 - abs(math.sin(td * 7.2)) * 34)
        trail.append((tx, ty))
    draw_phosphor_dot(cv, bx, by, r=4, trail=trail, color=PHOS)
    return vignette(cv, 0.35)


# =========================================================================== CAPÍTULO 1 (c1_00 .. c1_07)


def sc_c1_01_02_tennis(t):
    """c1_01 & c1_02: Vista completa de osciloscopio en fósforo verde + dos controles metálicos en c1_02."""
    cv = new_canvas(PHOS_BG)
    draw_phos_grid(cv, 16, 12, 464, 258, step=24, col=(8, 30, 16), axis_col=(16, 56, 28))
    d = ImageDraw.Draw(cv)

    t0 = TL.s("c1_01")
    t_cancha = TL.word("c1_01", "cancha")
    t_red = TL.word("c1_01", "red")
    t_punto = TL.word("c1_01", "punto")
    t_c2 = TL.s("c1_02")
    t_perilla = TL.word("c1_02", "perilla")
    t_boton = TL.word("c1_02", "boton")

    # Marco de pantalla de osciloscopio
    d.rectangle([28, 42, 452, 182], fill=(4, 18, 9, 255), outline=(*PHOS_MID, 255), width=2)
    draw_phos_grid(cv, 32, 46, 448, 178, step=20, col=(8, 36, 18), axis_col=(18, 68, 34))

    # Título superior
    phos_window(cv, 84, 8, 312, 28)
    draw_text(cv, "TENNIS FOR TWO · 1958", 240, 16, "press", 8, PHOS_BRIGHT, align="center",
              reveal=(t - t0) * 28)

    court_y = 152
    # 1) Línea horizontal: LA CANCHA
    p_c = prog(t, t_cancha - 0.35, t_cancha + 0.25)
    if p_c > 0:
        x1 = int(56 + 368 * ease_out(p_c))
        d.line([(56, court_y), (x1, court_y)], fill=(*PHOS_BRIGHT, 255), width=2)
        d.line([(56, court_y - 1), (x1, court_y - 1)], fill=(*PHOS, 85), width=4)
        draw_text(cv, "CANCHA", 96, court_y + 8, "press", 8, PHOS, align="center", alpha=p_c)

    # 2) Línea vertical: LA RED
    p_n = prog(t, t_red - 0.35, t_red + 0.2)
    if p_n > 0:
        y_top = int(court_y - 36 * ease_out(p_n))
        d.line([(240, court_y), (240, y_top)], fill=(*PHOS_BRIGHT, 255), width=2)
        draw_text(cv, "RED", 240, court_y + 8, "press", 8, PHOS, align="center", alpha=p_n)

    # 3) Punto de luz: LA PELOTA
    if t >= t_red - 0.1:
        bx, by, trail = tennis_ball_pos(t, t_red - 0.1, 72, 408, court_y - 3, 66, period=1.05)
        draw_phosphor_dot(cv, bx, by, r=4, trail=trail, color=PHOS)
        draw_text(cv, "PELOTA", 384, court_y + 8, "press", 8, PHOS_BRIGHT, align="center",
                  alpha=prog(t, t_red, t_red + 0.35))

    # Durante c1_01 (antes de c1_02): leyenda inferior explicativa
    if t < t_c2 - 0.15:
        phos_window(cv, 52, 198, 376, 48)
        draw_text(cv, "COMPUTADORA ANALÓGICA DONNER", 240, 208, "press", 8, PHOS, align="center")
        draw_text(cv, "1 LÍNEA = CANCHA · 1 LÍNEA = RED · 1 PUNTO = PELOTA", 240, 226, "silk", 8, CREAM, align="center")
    else:
        # Durante c1_02: dos cajas metálicas de control en la parte inferior
        a, dy = pop(t, t_c2 - 0.15, 0.3)
        ang1 = math.sin((t - t_perilla) * 4.0) * 55 if t >= t_perilla - 0.2 else -20
        ang2 = -math.sin((t - t_perilla) * 3.5) * 50 if t >= t_perilla - 0.2 else 25
        hit1 = t >= t_boton - 0.2 and (int((t - t_boton) / 0.52) % 2 == 0)
        hit2 = t >= t_boton - 0.2 and (int((t - t_boton) / 0.52) % 2 == 1)
        draw_controller_box(cv, 44, 190 + dy, 168, 68, ang1, hit1, "ÁNGULO", "BOTÓN", show_hand=True)
        draw_controller_box(cv, 268, 190 + dy, 168, 68, ang2, hit2, "ÁNGULO", "BOTÓN", show_hand=True)
    return vignette(cv, 0.35)


def sc_c1_03_gravities(t):
    """c1_03: Tres pantallas de osciloscopio lado a lado comparando LUNA, TIERRA y JÚPITER."""
    cv = new_canvas(PHOS_BG)
    draw_phos_grid(cv, 0, 0, W, H, step=24, col=(6, 24, 12), axis_col=(12, 42, 22))
    d = ImageDraw.Draw(cv)

    t0 = TL.s("c1_03")
    t_luna = TL.word("c1_03", "Luna")
    t_jup = TL.word("c1_03", "Jupiter")

    phos_window(cv, 68, 10, 344, 28)
    draw_text(cv, "GRAVEDAD SIMULADA · 1959", 240, 18, "press", 8, PHOS_BRIGHT, align="center",
              reveal=(t - t0) * 28)

    panels = [
        ("LUNA", "0.16 G · ARCO ALTO", 16, 82, 1.65, t0 + 0.1),
        ("TIERRA", "1.00 G · NORMAL", 168, 48, 1.00, t0 + 0.25),
        ("JÚPITER", "2.50 G · ARCO BAJO", 320, 20, 0.52, t0 + 0.4),
    ]
    for title, sub, x0, arc_h, period, t_appear in panels:
        a, dy = pop(t, t_appear, 0.3)
        if a <= 0:
            continue
        y0, pw, ph = 48 + dy, 144, 198
        highlight = (title == "LUNA" and t_luna - 0.2 <= t < t_jup - 0.1) or (title == "JÚPITER" and t >= t_jup - 0.1)
        window(cv, x0, y0, pw, ph, fill=(6, 22, 12),
               border=PHOS_BRIGHT if highlight else PHOS_MID, inner=(22, 82, 42))
        draw_text(cv, title, x0 + pw // 2, y0 + 10, "press", 8,
                  GOLD if highlight else PHOS_BRIGHT, align="center")
        draw_text(cv, sub, x0 + pw // 2, y0 + 24, "silk", 8, CREAM, align="center")

        # Pantalla circular del osciloscopio dentro de cada tarjeta
        cx, cy, r = x0 + pw // 2, y0 + 112, 54
        d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(22, 38, 28, 255), outline=(*INK, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(4, 16, 8, 255), outline=(*PHOS, 255))
        draw_phos_grid(cv, cx - 38, cy - 38, cx + 38, cy + 38, step=19, col=(8, 34, 18), axis_col=(16, 56, 28))

        court_y = cy + 28
        d.line([(cx - 42, court_y), (cx + 42, court_y)], fill=(*PHOS, 255), width=2)
        d.line([(cx, court_y), (cx, court_y - 16)], fill=(*PHOS, 255), width=2)

        # Curva punteada guía del arco
        pts_arc = []
        for k in range(17):
            u = k / 16.0
            ax = int((cx - 38) + 76 * u)
            ay = int(court_y - 2 - math.sin(u * math.pi) * arc_h)
            pts_arc.append((ax, ay))
        for k in range(0, len(pts_arc) - 1, 2):
            d.line([pts_arc[k], pts_arc[k + 1]], fill=(30, 96, 50, 180))

        bx, by, trail = tennis_ball_pos(t, t0, cx - 38, cx + 38, court_y - 2, arc_h, period=period)
        draw_phosphor_dot(cv, bx, by, r=3, trail=trail[-5:], color=PHOS)
    return vignette(cv, 0.35)


def sc_c1_04_disassemble(t):
    """c1_04: Laboratorio Brookhaven oscurecido; osciloscopio apagado y técnico llevándose caja de piezas."""
    cv = bg("bg_brookhaven_lab_1958").copy()
    cv = grade(cv, mul=(0.48, 0.58, 0.50), add=(2, 8, 4), sat=0.45, k=0.85)
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c1_04")
    t_estantes = TL.word("c1_04", "estantes")

    # Osciloscopio del escritorio apagado (pantalla oscura sin onda)
    d.rectangle([294, 148, 326, 174], fill=(10, 16, 12, 255))

    # Técnico caminando con una caja de válvulas y cables hacia los estantes
    tx, ph = walk(t, t0 - 0.1, t_estantes + 0.6, 150, 340)
    char(cv, TECH_1959, tx, 266, t, scale=3, walk=ph, arms="hold", facing=1, mood="neutral")

    # Caja de madera/cartón con piezas en las manos del técnico
    bx, by = int(tx) + 8, 176 + (int(math.sin(t * 12) * 2) if ph is not None else 0)
    d.rectangle([bx - 22, by - 14, bx + 22, by + 12], fill=(132, 96, 58, 255), outline=(*INK, 255))
    d.line([(bx - 21, by - 2), (bx + 21, by - 2)], fill=(96, 68, 38, 255))
    # Válvulas y cables asomando de la caja
    for vx in (bx - 12, bx, bx + 11):
        d.rectangle([vx - 3, by - 22, vx + 3, by - 14], fill=(160, 190, 175, 255), outline=(*INK, 255))
    draw_text(cv, "PIEZAS", bx, by + 1, "silk", 8, CREAM, align="center", outline=None, shadow=False)

    phos_window(cv, 64, 14, 352, 30)
    draw_text(cv, "DESARMADO · PIEZAS AL ESTANTE", 240, 23, "press", 8, GREY, align="center",
              reveal=(t - t0) * 26)
    return vignette(cv, 0.45)


def sc_c1_05_idea_free(t):
    """c1_05: Corte a negro. Solo el punto de luz verde fósforo sigue rebotando libremente."""
    cv = new_canvas((2, 8, 4))
    t0 = TL.s("c1_05") - 0.15
    dt = max(0.0, t - t0)

    # Trayectoria libre por toda la pantalla oscura
    def pos_at(tt):
        x = 64 + ((tt * 155) % 352)
        if int((tt * 155) // 352) % 2 == 1:
            x = 416 - ((tt * 155) % 352)
        y = 188 - abs(math.sin(tt * 5.2)) * 112
        return x, y

    bx, by = pos_at(dt)
    trail = [pos_at(max(0.0, dt - k * 0.032)) for k in range(10, 0, -1)]
    draw_phosphor_dot(cv, bx, by, r=4, trail=trail, color=PHOS)

    phos_window(cv, 52, 210, 376, 36)
    draw_text(cv, "PERO LA IDEA YA ESTABA SUELTA", 240, 222, "press", 8, PHOS_BRIGHT,
              align="center", reveal=(t - TL.s("c1_05") + 0.1) * 26)
    return vignette(cv, 0.4)


def sc_c1_06_mit_pdp1(t):
    """c1_06: MIT 1962. Dos programadores tipeando en la consola PDP-1 y un tercero observando."""
    cv = bg("bg_mit_pdp1_1962").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c1_06")
    t_sw = TL.word("c1_06", "Spacewar")

    # Resplandor verde fósforo sobre la pantalla circular del PDP-1 (cx=240, cy=135, r=21)
    cx, cy = 240, 135
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(6, 26, 14, 255))
    # Estrella central y dos pequeñas naves girando dentro del monitor del fondo
    d.point((cx, cy), fill=(*PHOS_BRIGHT, 255))
    for i, rad_off in enumerate((0.0, math.pi)):
        ang = t * 2.2 + rad_off
        sx = cx + int(math.cos(ang) * 12)
        sy = cy + int(math.sin(ang) * 10)
        d.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=(*PHOS, 255))

    # Dos programadores en la consola PDP-1 (arms="type") y un tercero con brazos cruzados (arms="cross")
    char(cv, RUSSELL_MIT, 152, 256, t, scale=3, arms="type", facing=1, look=1,
         talk=talk_v(t, t0 < t < t_sw), mood="happy")
    char(cv, MIT_PROG_2, 326, 256, t, scale=3, arms="type", facing=-1, look=-1, mood="happy")
    char(cv, MIT_PROG_3, 74, 262, t, scale=3, arms="cross", facing=1, look=1, mood="happy")

    if t < t_sw - 0.35:
        bigyear(cv, "1962", 240, 18, t, t0 + 0.05, size=32, ramp=PHOS_RAMP)
    else:
        a, dy = pop(t, t_sw - 0.35, 0.35)
        phos_window(cv, 84, 16 + dy, 312, 32)
        draw_text(cv, "SPACEWAR! · MIT · 1962", 240, 26 + dy, "press", 8, PHOS_BRIGHT, align="center")
    lower_third(cv, "STEVE RUSSELL Y EQUIPO", "COMPUTADORA DEC PDP-1 · MIT", t, t0 + 0.4, TL.e("c1_06"), x=16, y=220)
    return vignette(cv, 0.35)


def draw_needle_ship(d, cx, cy, ang, col=PHOS_BRIGHT):
    """Nave 'Aguja' (Needle) de Spacewar! en pixel art."""
    ca, sa = math.cos(ang), math.sin(ang)
    tip = (int(cx + ca * 11), int(cy + sa * 11))
    tail = (int(cx - ca * 9), int(cy - sa * 9))
    wing_l = (int(cx - ca * 7 - sa * 5), int(cy - sa * 7 + ca * 5))
    wing_r = (int(cx - ca * 7 + sa * 5), int(cy - sa * 7 - ca * 5))
    d.line([tail, tip], fill=(*col, 255), width=2)
    d.line([wing_l, tail, wing_r], fill=(*PHOS, 255), width=1)


def draw_wedge_ship(d, cx, cy, ang, col=PHOS_BRIGHT):
    """Nave 'Cuña' (Wedge) de Spacewar! en pixel art."""
    ca, sa = math.cos(ang), math.sin(ang)
    tip = (int(cx + ca * 10), int(cy + sa * 10))
    wing_l = (int(cx - ca * 8 - sa * 7), int(cy - sa * 8 + ca * 7))
    wing_r = (int(cx - ca * 8 + sa * 7), int(cy - sa * 8 - ca * 7))
    back = (int(cx - ca * 5), int(cy - sa * 5))
    d.polygon([tip, wing_l, back, wing_r], outline=(*col, 255), fill=(12, 52, 26, 255))


def sc_c1_07a_spacewar_crt(t):
    """c1_07 (1ra mitad): Primer plano del CRT circular del PDP-1 jugando Spacewar!."""
    cv = new_canvas(PHOS_BG)
    d = ImageDraw.Draw(cv)
    cx, cy, r = 240, 138, 104

    # Bisel circular del monitor CRT Type 30 del PDP-1
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], fill=(42, 58, 48, 255), outline=(*INK, 255))
    d.ellipse([cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5], fill=(20, 32, 24, 255), outline=(96, 126, 104, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(3, 14, 7, 255), outline=(*PHOS, 255))

    # Estrellas de fósforo dentro del CRT
    for i in range(28):
        sx = cx + int(math.cos(i * 2.39) * ((i * 19) % (r - 10)))
        sy = cy + int(math.sin(i * 2.39) * ((i * 19) % (r - 10)))
        d.point((sx, sy), fill=(*PHOS_MID, 220))

    # Estrella central pulsante con pozo gravitatorio
    star_r = 4 + int(abs(math.sin(t * 9)) * 4)
    for gr, ga in ((16, 40), (10, 90)):
        d.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(*PHOS, ga))
    d.line([(cx - star_r - 4, cy), (cx + star_r + 4, cy)], fill=(*PHOS_BRIGHT, 255), width=1)
    d.line([(cx, cy - star_r - 4), (cx, cy + star_r + 4)], fill=(*PHOS_BRIGHT, 255), width=1)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(240, 255, 245, 255))

    # Dos naves (Needle y Wedge) orbitando la estrella central y disparando torpedos
    ang1 = t * 1.65
    x1, y1 = cx + math.cos(ang1) * 64, cy + math.sin(ang1) * 54
    draw_needle_ship(d, x1, y1, ang1 + math.pi * 0.55)

    ang2 = t * 1.65 + math.pi
    x2, y2 = cx + math.cos(ang2) * 68, cy + math.sin(ang2) * 56
    draw_wedge_ship(d, x2, y2, ang2 + math.pi * 0.55)

    # Torpedos de píxeles cruzando el espacio entre las naves
    for k in range(3):
        u = ((t * 2.4 + k * 0.33) % 1.0)
        tx = int(x1 + (x2 - x1) * u)
        ty = int(y1 + (y2 - y1) * u - math.sin(u * math.pi) * 14)
        draw_phosphor_dot(cv, tx, ty, r=2, color=PHOS)

    phos_window(cv, 20, 10, 176, 26)
    draw_text(cv, "CRT PDP-1 · SPACEWAR!", 108, 17, "press", 8, PHOS_BRIGHT, align="center")
    phos_window(cv, 304, 10, 156, 26)
    draw_text(cv, "NO SE VENDÍA", 382, 17, "press", 8, GOLD, align="center")
    return vignette(cv, 0.35)


US_OUTLINE = [
    (58, 72), (124, 68), (196, 74), (274, 78), (336, 86), (394, 70), (424, 82),
    (414, 118), (398, 152), (384, 186), (362, 198), (332, 184), (288, 192),
    (246, 212), (212, 194), (154, 188), (98, 182), (62, 154), (48, 112), (58, 72),
]

US_NODES = [
    (402, 92, "MIT"),
    (386, 114, "NY"),
    (352, 124, "PA"),
    (298, 112, "IL"),
    (242, 134, "TX"),
    (168, 128, "UT"),
    (84, 102, "WA"),
    (74, 146, "STANFORD"),
]


def sc_c1_07b_network(t):
    """c1_07 (2da mitad): Mapa oscuro de EE.UU. donde nodos de fósforo se encienden copiando el juego."""
    cv = new_canvas(PHOS_BG)
    draw_phos_grid(cv, 0, 0, W, H, step=24, col=(6, 24, 12), axis_col=(12, 42, 22))
    d = ImageDraw.Draw(cv)

    t0 = TL.word("c1_07", "computadora") - 0.15
    t_end = TL.e("c1_07")

    # Contorno estilizado de Estados Unidos en verde fósforo
    d.polygon(US_OUTLINE, fill=(6, 26, 14, 230), outline=(*PHOS_MID, 255))
    d.line(US_OUTLINE, fill=(*PHOS, 180), width=2)

    # Nodos que se iluminan uno tras otro conectados por líneas mientras la copia viaja
    span = max(0.8, (t_end - t0) * 0.85)
    for i, (nx, ny, label) in enumerate(US_NODES):
        tn = t0 + (i / len(US_NODES)) * span
        p = prog(t, tn - 0.15, tn + 0.25)
        if i > 0 and p > 0:
            px, py, _ = US_NODES[i - 1]
            lx = int(px + (nx - px) * p)
            ly = int(py + (ny - py) * p)
            d.line([(px, py), (lx, ly)], fill=(*PHOS_BRIGHT, 255), width=2)
            if p < 1.0:
                draw_phosphor_dot(cv, lx, ly, r=3, color=PHOS)
        # Nodo
        if p > 0:
            for gr, ga in ((10, 45), (6, 95)):
                d.ellipse([nx - gr, ny - gr, nx + gr, ny + gr], fill=(*PHOS, int(ga * p)))
            d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(*PHOS_BRIGHT, 255), outline=(*INK, 255))
            draw_text(cv, label, nx, ny - 16, "silk", 8, PHOS_BRIGHT if i in (0, 7) else PHOS, align="center")
        else:
            d.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(18, 52, 28, 255), outline=(*PHOS_MID, 255))

    # Pulso que sigue viajando de nodo en nodo
    idx_f = ((t - t0) * 2.8) % max(1, len(US_NODES) - 1)
    i0 = int(idx_f)
    frac = idx_f - i0
    ax, ay, _ = US_NODES[i0]
    bx, by, _ = US_NODES[i0 + 1]
    draw_phosphor_dot(cv, ax + (bx - ax) * frac, ay + (by - ay) * frac, r=3, color=PHOS)

    phos_window(cv, 44, 12, 392, 28)
    draw_text(cv, "DE COMPUTADORA EN COMPUTADORA", 240, 20, "press", 8, PHOS, align="center",
              reveal=(t - t0) * 28)

    phos_window(cv, 48, 220, 384, 36)
    draw_text(cv, "EL PRIMER JUEGO QUE VIAJÓ", 240, 232, "press", 8, GOLD, align="center",
              reveal=(t - t0 - 0.5) * 32)
    return vignette(cv, 0.35)


# =========================================================================== MONTAJE (scenes, music, sfx)


def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (0.0, sc_s01_dot,
         lambda t: (1.0 + cam_punch(t, s01_bounces(), 0.03), 240, 135)),
        (s("s02") - 0.2, sc_s02_brookhaven,
         lambda t: cam_push(t, s("s02") - 0.2, s("s03") - 0.2, 1.0, 1.06, (195, 150), (225, 150))),
        (s("s03") - 0.2, sc_s03_oscilloscope,
         lambda t: (1.0 + cam_punch(t, [w("s03", "pelota")], 0.06), 240, 135)),
        (s("s04") - 0.2, sc_s04_visitors,
         lambda t: cam_push(t, s("s04") - 0.2, s("s05") - 0.15, 1.0, 1.06, (220, 145), (245, 145))),
        (s("s05") - 0.15, sc_s05_nopatent, None),
        (s("s06") - 0.2, sc_s06_revenue,
         lambda t: (1.0 + cam_punch(t, [w("s06", "doscientos")], 0.06), 240, 135)),
        (s("s07") - 0.15, sc_s07_countdown,
         lambda t: cam_push(t, s("s07") - 0.15, s("s08") - 0.25, 1.0, 1.05, (240, 135), (240, 135))),
        (s("s08") - 0.25, sc_s08_title,
         lambda t: (1.0 + cam_punch(t, [w("s08", "videojuegos")], 0.08), 240, 135)),
        (TL.chapter_start(1) - 0.3, make_card(1, ["EL JUEGO QUE", "NADIE PATENTÓ"], "1958 – 1962"), None),
        (s("c1_01") - 0.2, sc_c1_01_02_tennis,
         lambda t: (1.0 + cam_punch(t, [w("c1_01", "cancha"), w("c1_01", "red"), w("c1_01", "punto")], 0.04), 240, 135)),
        (s("c1_02") - 0.15, sc_c1_01_02_tennis,
         lambda t: (1.0 + cam_punch(t, [w("c1_02", "perilla"), w("c1_02", "boton")], 0.045), 240, 145)),
        (s("c1_03") - 0.2, sc_c1_03_gravities,
         lambda t: (1.0 + cam_punch(t, [w("c1_03", "Luna"), w("c1_03", "Jupiter")], 0.05), 240, 135)),
        (s("c1_04") - 0.2, sc_c1_04_disassemble,
         lambda t: cam_push(t, s("c1_04") - 0.2, s("c1_05") - 0.15, 1.0, 1.06, (230, 145), (250, 145))),
        (s("c1_05") - 0.15, sc_c1_05_idea_free, None),
        (s("c1_06") - 0.2, sc_c1_06_mit_pdp1,
         lambda t: cam_push(t, s("c1_06") - 0.2, s("c1_07") - 0.2, 1.0, 1.08, (240, 145), (240, 140))),
        (s("c1_07") - 0.2, sc_c1_07a_spacewar_crt,
         lambda t: cam_push(t, s("c1_07") - 0.2, w("c1_07", "computadora") - 0.15, 1.0, 1.08, (240, 138), (240, 138))),
        (w("c1_07", "computadora") - 0.15, sc_c1_07b_network,
         lambda t: (1.0 + cam_punch(t, [w("c1_07", "viajo")], 0.06), 240, 135)),
    ]


def music(A):
    s, e, w = TL.s, TL.e, TL.word
    # Apertura: en s04 entra pulso suave; en s05 silencio total ("Nunca lo patentó"); en s06 explota el tema; en s08 acorde principal
    A.section(s("s04") - 0.15, s("s05") - 0.2, 96, [("A", "min"), ("F", "maj")], A.st_mystery)
    # s06 y s07: impulso moderno brillante
    A.kick(A.music, s("s06") - 0.05, 0.45)
    A.crash(A.music, s("s06") - 0.05, 0.14)
    A.section(s("s06"), s("s08") - 0.25, 118, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_summer_lead)
    # s08: acorde principal y fanfarria de título
    t_title = s("s08") - 0.15
    A.kick(A.music, t_title, 0.5)
    A.crash(A.music, t_title, 0.18)
    A.sting(w("s08", "videojuegos") - 0.1, [69, 72, 76, 81, 84], inst_duty=0.5, vol=0.065, step=0.12, hold=1.5)
    A.section(s("s08"), TL.chapter_start(1) - 0.35, 118, [("F", "maj"), ("G", "maj"), ("A", "min")], A.st_triumph)

    # Capítulo 1 (desde fin de placa hasta fin del capítulo, con corte en c1_05)
    t_ch1 = TL.chapter_start(1) + 1.6
    A.section(t_ch1, s("c1_04") - 0.2, 102, [("A", "min"), ("E", "min"), ("F", "maj"), ("G", "maj")], A.st_puzzle)
    A.section(s("c1_04") - 0.2, s("c1_05") - 0.2, 86, [("D", "min"), ("A", "min")], A.st_rain)
    # En c1_05 solo rebota el punto; en c1_06 vuelve con energía en el MIT
    A.section(s("c1_06") - 0.15, chapter_end(1) - 0.25, 110,
              [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_build)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    # Zumbido eléctrico de 1958 durante s01..s03
    A.hum_1958(0.1, e("s03"))
    # Rebotes de la pelota en s01
    for i, bt in enumerate(s01_bounces()):
        A.plic(bt, 980 if i % 2 == 0 else 1120, 0.08)
    A.text_blips(0.75, 28, 14, 0.016, 1450)

    # s02: laboratorio Brookhaven
    A.chalk(s("s02") + 0.3, w("s02", "visitas") - 0.2, 0.025)
    A.pop_sfx(w("s02", "visitas") - 0.1, 620, 0.05)

    # s03: osciloscopio 5 pulgadas
    A.blip(s("s03") + 0.5, 840, 0.06, 0.04)
    A.blip(w("s03", "cinco") + 0.1, 1060, 0.06, 0.04)
    t_b = w("s03", "dibuja") - 0.1
    while t_b < s("s04") - 0.25:
        A.plic(t_b, 980, 0.08)
        t_b += 0.475

    # s04: fila de visitantes
    for i in range(5):
        A.pop_sfx(s("s04") - 0.1 + i * 0.12, 520 + i * 60, 0.045)
        A.plic(s("s04") + 0.15 + i * 0.38, 1040 if i % 2 else 920, 0.06)

    # s05: corte seco ("Él nunca lo patenta")
    A.stamp_hit(s("s05") - 0.05, 0.08)

    # s06 & s07: transición a 2026 y contador
    A.whoosh(s("s06") - 0.15, 0.55, 0.065)
    A.text_blips(w("s06", "mueve"), 18, 22, 0.018, 1650)
    A.coin(w("s06", "doscientos") + 0.3, 0.065)
    A.pop_sfx(s("s07") - 0.1, 740, 0.055)

    # s08: rebotes en el título
    for k in range(5):
        A.plic(s("s08") + 0.2 + k * 0.44, 980 + (k % 2) * 160, 0.065)

    # c1_01 & c1_02: Tennis for Two + perilla y botón
    A.hum_1958(s("c1_01") - 0.1, e("c1_02"))
    A.blip(w("c1_01", "cancha"), 880, 0.06, 0.045)
    A.blip(w("c1_01", "red"), 1100, 0.06, 0.045)
    tt = w("c1_01", "punto") - 0.2
    while tt < s("c1_03") - 0.25:
        A.plic(tt, 960 if int(tt * 2) % 2 == 0 else 1140, 0.075)
        tt += 0.52

    # c1_03: gravedades Luna (lento/estirado) y Júpiter (rápido/acelerado)
    t_luna = w("c1_03", "Luna")
    for k in range(3):
        A.plic(t_luna - 0.4 + k * 0.65, 720, 0.07)
    t_jup = w("c1_03", "Jupiter")
    for k in range(5):
        A.plic(t_jup - 0.2 + k * 0.22, 1380, 0.07)

    # c1_04 & c1_05: desarmado y punto suelto
    A.whoosh(s("c1_04") + 0.2, 0.4, 0.045)
    t_free = s("c1_05") - 0.1
    while t_free < s("c1_06") - 0.2:
        A.plic(t_free, 1020, 0.08)
        t_free += 0.60

    # c1_06 & c1_07: Spacewar! en el MIT y red de computadoras
    A.typewriter(s("c1_06") + 0.2, w("c1_06", "Spacewar") - 0.2, 13, 0.03)
    A.join_jingle(w("c1_06", "Spacewar") - 0.1, 0.055)
    for k in range(4):
        A.blip(w("c1_06", "torpedos") - 0.2 + k * 0.18, 1500 - k * 180, 0.035, 0.04)
    for k in range(5):
        A.blip(s("c1_07") + 0.15 + k * 0.35, 1320 - (k % 3) * 160, 0.03, 0.035)
    t_net = w("c1_07", "computadora")
    for i in range(len(US_NODES)):
        A.plic(t_net + i * 0.38, 880 + i * 70, 0.065)
