"""Capítulo 5: Placas de videojuegos (1997 – 2012)."""
from common import *  # noqa

WD = TL.word
RED = (230, 70, 60)
GREEN = (110, 230, 120)
PAPER = (246, 240, 222)


# =========================================================================== helpers

def net_layers(xs, sizes, cy, gap):
    return [[(x, int(cy + (i - (n - 1) / 2) * gap)) for i in range(n)] for x, n in zip(xs, sizes)]


def draw_net(cv, layers, glow=1.0, edge=(50, 110, 140), node=(120, 230, 255), r=3):
    d = ImageDraw.Draw(cv)
    ec = tuple(int(c * (0.4 + 0.6 * glow)) for c in edge)
    for la, lb in zip(layers, layers[1:]):
        for p in la:
            for q in lb:
                d.line([p, q], fill=(*ec, 255))
    for L in layers:
        for (x, y) in L:
            nc = tuple(int(30 + (c - 30) * (0.25 + 0.75 * glow)) for c in node)
            if glow > 0.5:
                d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=(*node, int(70 * glow)))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(*nc, 255), outline=(*INK, 255))
            if glow > 0.5:
                d.point((x - 1, y - 1), fill=(240, 255, 255, 255))


def net_pulses(cv, layers, s, color, size=1):
    d = ImageDraw.Draw(cv)
    for l in range(len(layers) - 1):
        u = s - l
        if not (0 <= u <= 1):
            continue
        for p in layers[l]:
            for q in layers[l + 1]:
                x = int(p[0] + (q[0] - p[0]) * u)
                y = int(p[1] + (q[1] - p[1]) * u)
                d.rectangle([x - size, y - size, x + size, y + size], fill=(*color, 255))


def tag(cv, txt, cx, y, t, t0, fill=(20, 24, 52), col=CREAM, border=GOLD):
    a, dy = pop(t, t0)
    if a <= 0:
        return
    tw, _ = text_size(txt, "press", 8)
    window(cv, cx - tw // 2 - 6, y + dy, tw + 12, 16, fill=fill, border=border)
    draw_text(cv, txt, cx, y + 4 + dy, "press", 8, col, align="center")


def intro_card(cv, pname, title, sub, t, t_in, t_out, x=14, y=176):
    if t < t_in - 0.2 or t > t_out + 0.4:
        return
    a = prog(t, t_in - 0.2, t_in + 0.2)
    off = int((1 - ease_out(a)) * -380) + int(ease_in_out(prog(t, t_out, t_out + 0.4)) * -420)
    portrait_card(cv, pname, x + off, y)
    tw = max(text_size(title, "press", 16)[0], text_size(sub, "silk", 8)[0]) + 22
    window(cv, x + 72 + off, y + 14, tw, 46)
    draw_text(cv, title, x + 82 + off, y + 24, "press", 16, CREAM)
    draw_text(cv, sub, x + 82 + off, y + 44, "silk", 8, GREY)


def year_drop(cv, text, cx, y, t, t0, t_out, size=48):
    if t >= t_out:
        return
    a_out = 1 - prog(t, t_out - 0.35, t_out)
    p = prog(t, t0, t0 + 0.55)
    if p <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=GOLD_RAMP, outline_w=2,
              alpha=min(p * 3, a_out))
    if p >= 1 and a_out > 0.5:
        tw, _ = text_size(text, "press", size)
        for i, ph in enumerate((0.0, 1.7, 3.1)):
            sparkle(cv, cx - tw // 2 + int((i + 0.5) * tw / 3), y + 4 + (i * 13) % size, t + ph, 3)


def stage_bg(top=(10, 14, 34), bottom=(30, 40, 80), floor_y=206):
    cv = vgradient(top, bottom, 14)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, floor_y, W, H], fill=(20, 22, 44, 255))
    for y in (floor_y, floor_y + 8, floor_y + 20, floor_y + 36, floor_y + 56):
        d.line([(0, y), (W, y)], fill=(40, 46, 86, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, floor_y), (x, H)], fill=(30, 34, 66, 255))
    return cv


def deep_blue(cv, x, y, w, h, t, on=1.0):
    """Gabinete negro de Deep Blue con LEDs azules."""
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 30, 255), outline=(*INK, 255))
    d.rectangle([x + 2, y + 2, x + w - 2, y + 5], fill=(40, 44, 64, 255))
    d.line([(x + w - 3, y + 6), (x + w - 3, y + h - 2)], fill=(10, 10, 16, 255))
    rows = (h - 30) // 8
    cols = max(1, (w - 12) // 6)
    for r in range(rows):
        for c in range(cols):
            lit = on > 0 and (int(t * 9) + r * 5 + c * 3 + (r * c) % 7) % 4 != 0
            col = (90, 170, 255) if (r + c) % 5 else (120, 255, 200)
            d.rectangle([x + 6 + c * 6, y + 12 + r * 8, x + 8 + c * 6, y + 13 + r * 8],
                        fill=(*(col if lit else (30, 40, 70)), 255))
    d.rectangle([x + w // 2 - 12, y + h - 14, x + w // 2 + 12, y + h - 6], fill=(31, 79, 160, 255), outline=(*INK, 255))
    draw_text(cv, "IBM", x + w // 2, y + h - 13, "silkb", 8, CREAM, align="center", outline=None, shadow=False)


# --------------------------------------------------------------------------- rey de ajedrez

def _king_img(k=1.5):
    """Rey negro dibujado a resolución nativa (k = escala de las coordenadas)."""
    def P(*pts):
        return [(int(round(x * k)), int(round(y * k))) for x, y in pts]
    im = Image.new("RGBA", (int(24 * k) + 2, int(46 * k) + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    body, hi, ol = (34, 34, 46, 255), (96, 96, 122, 255), (220, 214, 200, 255)
    d.rectangle(P((1, 39), (22, 44)), fill=body, outline=ol)
    d.polygon(P((5, 39), (18, 39), (15, 25), (8, 25)), fill=body, outline=ol)
    d.rectangle(P((4, 21), (19, 25)), fill=body, outline=ol)
    d.ellipse(P((6, 10), (17, 22)), fill=body, outline=ol)
    d.rectangle(P((10, 1), (13, 10)), fill=body, outline=ol)
    d.rectangle(P((7, 4), (16, 6)), fill=body, outline=ol)
    d.line(P((8.5, 27), (8.5, 37)), fill=hi, width=2)
    d.line(P((3, 41), (12, 41)), fill=hi)
    d.point(P((8.5, 14))[0], fill=hi)
    return im


KING = _king_img(1.5)


def draw_king(cv, px, py, ang_deg):
    """Rey con pivote en la base (px, py); ang_deg > 0 cae hacia la derecha."""
    kw, kh = KING.size
    S = kh * 2 + 8
    tmp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    tmp.paste(KING, (S // 2 - kw // 2, S // 2 - kh), KING)
    if ang_deg:
        tmp = tmp.rotate(-ang_deg, resample=Image.NEAREST, center=(S // 2 + kw // 2, S // 2))
    paste(cv, tmp, px - S // 2, py - S // 2)


# =========================================================================== escenas

def sc_chess(t):
    """Mayo de 1997. Deep Blue, de IBM, derrota al campeón mundial Garry Kasparov."""
    cv = bg("bg_chess_stage_1997").copy()
    t0 = TL.s("c5_01")
    t_comp = WD("c5_01", "computadora")
    t_deep = WD("c5_01", "Deep")
    t_ibm = WD("c5_01", "IBM")
    t_der = WD("c5_01", "derrota")
    t_camp = WD("c5_01", "campeon")
    t_garry = WD("c5_01", "Garry")
    # Deep Blue: gabinete y monitor
    deep_blue(cv, 4, 112, 46, 104, t)
    d = ImageDraw.Draw(cv)
    if t > t_comp:
        d.rectangle([72, 102, 106, 132], fill=(10, 30, 60, 255))
        if int(t * 4) % 2 or t > t_der:
            draw_text(cv, "DEEP", 89, 108, "silkb", 8, (120, 200, 255), align="center", outline=None, shadow=False)
            draw_text(cv, "BLUE", 89, 118, "silkb", 8, (120, 200, 255), align="center", outline=None, shadow=False)
    # año
    year_drop(cv, "1997", 240, 8, t, t0, t_deep - 0.1)
    if t < t_deep - 0.1:
        a = prog(t, t0 - 0.1, t0 + 0.3) * (1 - prog(t, t_deep - 0.45, t_deep - 0.1))
        draw_text(cv, "MAYO", 240, 64, "press", 16, CREAM, align="center", alpha=a)
    else:
        a, dy = pop(t, t_deep - 0.1)
        window(cv, 104, 8 + dy, 272, 30)
        draw_text(cv, "DEEP BLUE", 120, 16 + dy, "press", 16, gradient=CYAN_RAMP)
        if t > t_ibm:
            draw_text(cv, "· IBM", 280, 16 + dy, "press", 16, CREAM)
    # el rey cae
    if t > t_ibm - 0.1:
        a, dy = pop(t, t_ibm - 0.1)
        p = prog(t, t_der, t_der + 0.45)
        ang = 90 * p * p
        if p >= 1:
            ang = 90 - 8 * abs(math.sin((t - t_der - 0.45) * 12)) * math.exp(-(t - t_der - 0.45) * 5)
        draw_king(cv, 240, 150 + dy, ang)
        if t_der + 0.45 <= t < t_der + 0.8:
            for i in range(6):
                sparkle(cv, 250 + i * 12, 144 - (i % 2) * 6, t + i, 3, CREAM)
    if t > t_der + 0.5:
        a, dy = pop(t, t_der + 0.5)
        draw_text(cv, "JAQUE MATE", 240, 52 + dy, "press", 8, (255, 120, 90), align="center")
    # personajes
    if t < t_comp:
        k_arms, k_mood = "think", "neutral"
    elif t < t_der:
        k_arms, k_mood = "think", "worried"
    elif t < t_camp:
        k_arms, k_mood = "shrug", "worried"
    else:
        k_arms, k_mood = ("think" if int((t - t_camp) / 0.9) % 2 else "cross"), "sad"
    jit = int(math.sin(t * 30) * 1.5) if t_der < t < t_camp + 1 else 0
    char(cv, "kasparov", 130 + jit, 266, t, scale=3, arms=k_arms, mood=k_mood, look=1 if t < t_der else 0)
    char(cv, "ibm_op", 360, 266, t, scale=3, arms="hold" if t < t_der else "down",
         mood="neutral" if t < t_der else "happy", look=-1)
    if t > t_der + 0.2:
        a, dy = pop(t, t_der + 0.2)
        draw_text(cv, "!?", 130, 90 + dy, "press", 16, (255, 120, 90), align="center")
    intro_card(cv, "garry_kasparov", "GARRY KASPAROV", "CAMPEÓN MUNDIAL DE AJEDREZ", t, t_garry - 0.1, 99999)
    dx, dy = shake(t, t_der + 0.45, 0.3, 3)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


_mrng = np.random.default_rng(17)
MOVES = [(_mrng.uniform(0, 1), _mrng.uniform(0, 1), _mrng.uniform(0, 6.28), _mrng.uniform(10, 26)) for _ in range(90)]


def chess_floor(cv, top=170, t=0.0):
    """Tablero gigante en perspectiva."""
    a = np.array(cv)
    hzn = top
    for y in range(hzn, H):
        depth = (y - hzn + 4) / (H - hzn + 4)
        sq = 0.02 / depth
        for x in range(W):
            u = (x - W / 2) * depth / 60.0
            v = 1.0 / depth + t * 0.0
            c = (int(math.floor(u)) + int(math.floor(v * 1.0))) % 2
            if c:
                a[y, x, :3] = (52, 56, 92)
            else:
                a[y, x, :3] = (22, 24, 46)
    return Image.fromarray(a, "RGBA")


_FLOOR_CACHE = {}


def floor_img():
    if "f" not in _FLOOR_CACHE:
        base = vgradient((6, 8, 22), (24, 30, 64), 12)
        _FLOOR_CACHE["f"] = chess_floor(base, 168)
    return _FLOOR_CACHE["f"]


def sc_brute(t):
    """Es un hito, pero no aprende: calcula millones de jugadas por fuerza bruta."""
    cv = floor_img().copy()
    STARS.draw(cv, t * 0.5, alpha=0.5)
    t_hito = WD("c5_02", "hito")
    t_apr = WD("c5_02", "aprende")
    t_calc = WD("c5_02", "calcula")
    t_mill = WD("c5_02", "millones")
    t_fue = WD("c5_02", "fuerza")
    # ráfaga de jugadas que salen del gabinete
    d = ImageDraw.Draw(cv)
    burst = prog(t, t_calc - 0.2, t_calc + 0.6)
    if burst > 0:
        n = int(len(MOVES) * burst)
        for i, (u, v, ang, ln) in enumerate(MOVES[:n]):
            ph = (t * (1.5 + u) + v) % 1.0
            r = 30 + ph * 260
            ang2 = -math.pi * (0.05 + 0.9 * v)
            x0 = 110 + math.cos(ang2) * r
            y0 = 150 + math.sin(ang2) * r * 0.6 + ph * 60
            x1 = x0 + math.cos(ang) * ln * 0.5
            y1 = y0 + math.sin(ang) * ln * 0.3
            if not (0 <= x0 < W and 0 <= y0 < H):
                continue
            col = (90, 220, 255) if i % 3 else (255, 214, 110)
            d.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=(*col, 255))
            d.rectangle([int(x1) - 1, int(y1) - 1, int(x1) + 1, int(y1) + 1], fill=(*col, 255))
    # gabinete gigante
    hot = prog(t, t_fue, t_fue + 0.4)
    deep_blue(cv, 66, 64, 88, 150, t * (1 + 3 * burst))
    if hot > 0:
        for i in range(5):
            ph = (t * 1.2 + i * 0.21) % 1.0
            sx = 80 + i * 16 + int(math.sin(t * 6 + i) * 3)
            sy = int(60 - ph * 40)
            d.rectangle([sx, sy, sx + 3, sy + 2], fill=(200, 200, 210, int(200 * (1 - ph))))
    # título hito
    if t > t_hito - 0.1:
        a, dy = pop(t, t_hito - 0.1)
        window(cv, 196, 12 + dy, 268, 30)
        draw_text(cv, "UN HITO", 214, 20 + dy, "press", 16, align="left", gradient=GOLD_RAMP)
        for i in range(3):
            sparkle(cv, 344 + i * 30, 26 + dy, t + i, 3, GOLD)
    # no aprende: calcula
    if t > t_apr - 0.15:
        a, dy = pop(t, t_apr - 0.15)
        window(cv, 196, 52 + dy, 268, 58)
        draw_text(cv, "NO APRENDE", 214, 62 + dy, "press", 16, CREAM)
        if t > t_calc + 0.3:
            dd = ImageDraw.Draw(cv)
            dd.line([(212, 70 + dy), (376, 70 + dy)], fill=(*RED, 255), width=2)
        if t > t_calc - 0.1:
            draw_text(cv, "CALCULA", 214, 84 + dy, "press", 16, gradient=CYAN_RAMP,
                      reveal=(t - t_calc + 0.1) * 24)
    # contador
    if t > t_mill - 0.1:
        a, dy = pop(t, t_mill - 0.1)
        window(cv, 196, 118 + dy, 268, 46)
        v = int(round(200 * ease_out(prog(t, t_mill, t_fue))))
        draw_text(cv, f"~{v} MILLONES", 330, 126 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
        draw_text(cv, "DE POSICIONES POR SEGUNDO", 330, 148 + dy, "press", 8, GREY, align="center")
    # sello fuerza bruta
    if t > t_fue:
        p = prog(t, t_fue, t_fue + 0.18)
        sc = 1.0
        a = min(1.0, p * 2)
        window(cv, 168, 182, 302, 40, fill=(120, 24, 30), border=(255, 140, 120))
        draw_text(cv, "FUERZA BRUTA", 319, 190, "press", 24, CREAM, align="center", alpha=a)
    # la máquina mira, pensativa
    robot(cv, 36, 262, t, face="think" if t < t_fue else "question", scale=2)
    dx, dy = shake(t, t_fue + 0.1, 0.35, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


# --------------------------------------------------------------------------- ImageNet

def _make_mosaic():
    rng = np.random.default_rng(9)
    a = np.zeros((H, W, 4), np.uint8)
    a[..., 3] = 255
    cw, ch = 8, 6
    palette_sky = [(120, 180, 230), (200, 220, 240), (110, 150, 90), (230, 200, 150), (60, 70, 90), (180, 140, 100),
                   (240, 240, 230), (90, 120, 160)]
    for cy in range(0, H, ch):
        for cx in range(0, W, cw):
            sky = np.array(palette_sky[rng.integers(0, len(palette_sky))]) + rng.integers(-20, 20, 3)
            obj = rng.integers(20, 255, 3)
            a[cy:cy + ch, cx:cx + cw, :3] = np.clip(sky, 0, 255)
            ox, oy = int(rng.integers(1, 3)), int(rng.integers(1, 2))
            a[cy + oy + 1:cy + oy + 4, cx + ox:cx + ox + 4, :3] = obj
            a[cy + ch - 1, cx:cx + cw, :3] = (16, 16, 24)
            a[cy:cy + ch, cx + cw - 1, :3] = (16, 16, 24)
    return a


MOSAIC = _make_mosaic()
_cy, _cx = np.mgrid[0:H // 6 + 1, 0:W // 8 + 1]
CELL_D = np.sqrt(((_cx * 8 + 4) - 364) ** 2 + (((_cy * 6 + 3) - 142) * 1.4) ** 2)
CELL_J = np.random.default_rng(4).uniform(0, 40, CELL_D.shape)

IMG_TAGS = [("GATO", 7, 14), ("PERRO", 16, 26), ("AUTO", 44, 13), ("AVIÓN", 52, 22), ("FLOR", 4, 33),
            ("MANZANA", 36, 31)]


def sc_imagenet(t):
    """2009: Fei-Fei Li lanza ImageNet, millones de imágenes etiquetadas."""
    cv = bg("bg_stanford_office_2009").copy()
    t_ver = WD("c5_03", "verdadero")
    t_year = WD("c5_03", "nueve")
    t_fei = WD("c5_03", "Fei-Fei")
    t_lan = WD("c5_03", "lanzan")
    t_img = WD("c5_03", "ImageNet")
    t_mill = WD("c5_03", "millones")
    t_et = WD("c5_03", "etiquetadas")
    # miniaturas en los monitores del fondo
    a = np.array(cv)
    for (x0, y0) in ((321, 125), (367, 125)):
        k = int(t * 3)
        sub = MOSAIC[(k * 6) % 120:(k * 6) % 120 + 30, (k * 8) % 200:(k * 8) % 200 + 40]
        a[y0:y0 + 30, x0:x0 + 40] = sub
    # mosaico que se expande
    R = 0
    if t > t_img - 0.2:
        R = 600 * ease_in_out(prog(t, t_img - 0.2, t_mill + 0.4)) ** 1.2
    if R > 0:
        cells = (CELL_D + CELL_J) < R
        m = np.repeat(np.repeat(cells, 6, 0), 8, 1)[:H, :W]
        mos = (MOSAIC[..., :3].astype(np.float32) * 0.72).astype(np.uint8)
        a[m, :3] = mos[m]
    cv = Image.fromarray(a, "RGBA")
    # la máquina llega
    rx, _ = walk(t, t_ver - 0.2, t_ver + 1.6, W + 40, 428)
    face = "question" if t < t_img else ("happy" if t < t_et else "heart")
    robot(cv, rx, 262, t, face=face, scale=2)
    # Fei-Fei
    if t > t_fei - 0.8:
        x, ph = walk(t, t_fei - 0.8, t_fei - 0.05, -40, 222)
        arms = "down"
        if ph is None:
            arms = "wave" if t < t_lan else ("point" if t < t_mill else "cheer")
        char(cv, "feifei", x, 266, t, scale=3, walk=ph, arms=arms, mood="happy" if t > t_lan else "neutral")
    # etiquetas
    if t > t_et - 0.1:
        for i, (lab, cx, cy) in enumerate(IMG_TAGS):
            ti = t_et - 0.1 + i * 0.12
            if t < ti:
                continue
            a_, dy = pop(t, ti)
            x0, y0 = cx * 8, cy * 6
            dd = ImageDraw.Draw(cv)
            dd.rectangle([x0 - 1, y0 - 1, x0 + 16, y0 + 12], outline=(*GOLD, 255))
            dd.rectangle([x0 - 2, y0 - 2, x0 + 17, y0 + 13], outline=(*INK, 255))
            tw, _ = text_size(lab, "press", 8)
            window(cv, x0 + 8 - tw // 2 - 4, y0 - 17 + dy, tw + 8, 14)
            draw_text(cv, lab, x0 + 8, y0 - 14 + dy, "press", 8, CREAM, align="center")
    # año / título
    year_drop(cv, "2009", 240, 8, t, t_year - 0.15, t_img - 0.1)
    if t > t_img - 0.1:
        a_, dy = pop(t, t_img - 0.1)
        window(cv, 104, 4 + dy, 272, 44)
        draw_text(cv, "IMAGENET", 240, 10 + dy, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
    if t > t_mill - 0.1:
        a_, dy = pop(t, t_mill - 0.1)
        window(cv, 100, 54 + dy, 280, 26)
        draw_text(cv, "MILLONES DE IMÁGENES", 112, 62 + dy, "press", 8, CREAM, reveal=(t - t_mill + 0.1) * 30)
        if t > t_et - 0.05:
            draw_text(cv, "ETIQUETADAS", 280, 62 + dy, "press", 8, CYAN,
                      reveal=(t - t_et + 0.05) * 26)
    intro_card(cv, "fei_fei_li", "FEI-FEI LI", "STANFORD · VISIÓN POR COMPUTADORA", t, t_fei, t_img - 0.3)
    return vignette(cv, 0.3)


# --------------------------------------------------------------------------- Toronto

def toronto_bg():
    cv = vgradient((8, 10, 30), (40, 40, 84), 12)
    STARS.draw(cv, 0.0, alpha=0.5)
    d = ImageDraw.Draw(cv)
    rnd = np.random.default_rng(23)
    x = 0
    while x < W:
        bw = int(rnd.integers(16, 36))
        bh = int(rnd.integers(30, 100))
        d.rectangle([x, 196 - bh, x + bw, 196], fill=(34, 40, 76, 255))
        for wy in range(196 - bh + 6, 194, 8):
            for wx in range(x + 3, x + bw - 3, 6):
                if rnd.random() < 0.35:
                    d.rectangle([wx, wy, wx + 1, wy + 2], fill=(220, 190, 110, 255))
        x += bw + int(rnd.integers(0, 5))
    # CN Tower
    cx = 412
    TC = (52, 60, 104, 255)
    d.polygon([(cx - 6, 196), (cx + 6, 196), (cx + 2, 70), (cx - 2, 70)], fill=TC)
    d.ellipse([cx - 11, 92, cx + 11, 104], fill=TC)
    d.rectangle([cx - 8, 104, cx + 8, 108], fill=TC)
    d.line([(cx, 70), (cx, 30)], fill=TC, width=2)
    d.point((cx, 30), fill=(255, 80, 70, 255))
    d.rectangle([0, 196, W, H], fill=(26, 24, 40, 255))
    for y in (196, 204, 216, 232, 252):
        d.line([(0, y), (W, y)], fill=(44, 40, 66, 255))
    return cv


TOR_BG = None


def sc_toronto(t):
    """2012: tres investigadores de Toronto presentan AlexNet."""
    global TOR_BG
    if TOR_BG is None:
        TOR_BG = toronto_bg()
    cv = TOR_BG.copy()
    d = ImageDraw.Draw(cv)
    # luz roja de la torre
    if int(t * 2) % 2:
        d.rectangle([411, 29, 413, 31], fill=(255, 90, 80, 255))
    t_year = WD("c5_04", "dos")
    t_uni = WD("c5_04", "Universidad")
    t_names = [WD("c5_04", "Alex"), WD("c5_04", "Ilya"), WD("c5_04", "Geoffrey")]
    t_pres = WD("c5_04", "presentan")
    t_anet = WD("c5_04", "AlexNet")
    t_comp = WD("c5_04", "competencia")
    keys = ["krizhevsky", "sutskever", "hinton12"]
    portraits = ["alex_krizhevsky", "ilya_sutskever", "geoffrey_hinton_2012"]
    first = ["ALEX", "ILYA", "GEOFFREY"]
    last = ["KRIZHEVSKY", "SUTSKEVER", "HINTON"]
    xs = [110, 240, 370]
    for i, k in enumerate(keys):
        tn = t_names[i]
        if t < tn - 0.15:
            continue
        a, dy = pop(t, tn - 0.15, 0.4)
        arms, mood = ("wave", "happy") if tn < t < tn + 0.9 else ("down", "neutral")
        if t > t_anet:
            arms, mood = ("point" if i == 0 else ("hold" if i == 1 else "think")), "happy"
        char(cv, k, xs[i], 266 + dy, t, alpha=a, arms=arms, mood=mood, scale=3)
        if t < tn + 0.5:
            for j in range(3):
                sparkle(cv, xs[i] - 30 + j * 30, 130 + (j % 2) * 40, t + j, 3, GOLD)
    up = int(ease_in_out(prog(t, t_anet - 0.35, t_anet + 0.1)) * -150)
    for i in range(3):
        tn = t_names[i]
        if t > tn - 0.1 and up > -149:
            a, dy = pop(t, tn - 0.1, 0.4)
            cx = xs[i] - 32
            portrait_card(cv, portraits[i], cx, 10 + dy + up)
            window(cv, cx - 13, 80 + dy + up, 90, 26)
            draw_text(cv, first[i], cx + 32, 84 + dy + up, "silk", 8, GREY, align="center")
            draw_text(cv, last[i], cx + 32, 95 + dy + up, "press", 8, CREAM, align="center")
    year_drop(cv, "2012", 240, 10, t, t_year - 0.1, t_names[0] - 0.15)
    if t_uni - 0.1 < t < t_names[0] - 0.15:
        tag(cv, "UNIVERSIDAD DE TORONTO", 240, 70, t, t_uni - 0.1)
    if t > t_anet - 0.1:
        a, dy = pop(t, t_anet - 0.1)
        window(cv, 112, 6 + dy, 256, 44)
        draw_text(cv, "ALEXNET", 240, 12 + dy, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
        for i in range(3):
            sparkle(cv, 130 + i * 110, 20 + (i % 2) * 20, t + i, 3, GOLD)
    if t > t_comp - 0.1:
        tag(cv, "COMPETENCIA IMAGENET 2012", 240, 58, t, t_comp - 0.1, fill=(30, 50, 90), border=CYAN)
    return vignette(cv, 0.35)


# --------------------------------------------------------------------------- GPUs

GPUS = [(24, 141, 92, 166), (24, 168, 92, 194)]
FANS = [(39, 154), (75, 154), (39, 181), (75, 181)]
BED_NET = net_layers([306, 336, 366, 396, 426, 452], [3, 5, 5, 5, 4, 2], 82, 11)


def sc_gpus(t):
    """Entrenada con dos placas de video para gamers en la casa de los padres de Krizhevsky."""
    cv = bg("bg_bedroom_2012").copy()
    t_red = WD("c5_05", "red")
    t_prof = WD("c5_05", "profunda")
    t_dos = WD("c5_05", "placas") - 0.25
    t_gam = WD("c5_05", "gamers")
    t_casa = WD("c5_05", "casa")
    t_kri = WD("c5_05", "Krizhevsky")
    heat = prog(t, t_dos, t_dos + 1.5)
    # brillo de las GPUs
    a = np.array(cv)
    if t > t_dos:
        pulse = 0.5 + 0.5 * math.sin(t * 8)
        for (x0, y0, x1, y1) in GPUS:
            reg = a[y0:y1, x0:x1, :3].astype(np.float32)
            a[y0:y1, x0:x1, :3] = np.clip(reg * (1.0 + 0.35 * pulse) + np.array([10, 30, 20]) * pulse, 0, 255)
    # calor: desplazamiento ondulante sobre el gabinete
    if heat > 0:
        for y in range(56, 100):
            sh = int(round(math.sin(y * 0.6 + t * 14) * 1.5 * heat))
            if sh:
                a[y, 10:112] = np.roll(a[y, 10:112], sh, axis=0)
    cv = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(cv)
    # ventiladores girando
    spd = 10 + 30 * heat
    for (fx, fy) in FANS:
        for k in range(3):
            ang = t * spd + k * 2 * math.pi / 3
            d.line([(fx, fy), (int(fx + math.cos(ang) * 8), int(fy + math.sin(ang) * 8))], fill=(150, 255, 210, 255),
                   width=2)
        d.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=(40, 70, 60, 255))
    if t > t_dos:
        on = int(t * 6) % 2
        for i, (x0, y0, x1, y1) in enumerate(GPUS):
            if t > t_dos + i * 0.25:
                col = GOLD if on else (255, 250, 200)
                d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(*col, 255))
                d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], outline=(*INK, 255))
    # vapor de calor
    if heat > 0.3:
        for i in range(6):
            ph = (t * 0.9 + i * 0.17) % 1.0
            sx = 22 + i * 15 + int(math.sin(t * 5 + i) * 3)
            sy = int(98 - ph * 50)
            d.rectangle([sx, sy, sx + 2, sy + 1], fill=(255, 170, 90, int(255 * (1 - ph))))
    # Krizhevsky en la PC
    char(cv, "krizhevsky", 256, 266, t, scale=3, arms="type", facing=-1, look=-1,
         mood="happy" if t > t_casa else "neutral")
    # red profunda en la pared
    if t > t_red - 0.1:
        a_, dy = pop(t, t_red - 0.1)
        window(cv, 290, 22 + dy, 182, 116, fill=(10, 16, 36))
        draw_text(cv, "RED NEURONAL", 381, 30 + dy, "press", 8, CREAM, align="center")
        g = prog(t, t_red, t_prof + 0.3)
        L = [[(x, y + dy) for (x, y) in col] for col in BED_NET]
        draw_net(cv, L, glow=g, r=2)
        if t > t_prof:
            net_pulses(cv, L, ((t - t_prof) * 3.0) % 5.4, (255, 220, 120))
            draw_text(cv, "PROFUNDA", 381, 124 + dy, "press", 8, align="center", gradient=CYAN_RAMP)
    # etiqueta GPUs
    if t > t_dos:
        a_, dy = pop(t, t_dos)
        window(cv, 10, 40 + dy, 124, 44)
        draw_text(cv, "GTX 580  X2", 72, 48 + dy, "press", 8, GOLD, align="center")
        if t > t_gam - 0.1:
            draw_text(cv, "PLACAS PARA", 72, 60 + dy, "silk", 8, CREAM, align="center")
            draw_text(cv, "GAMERS", 72, 70 + dy, "silkb", 8, CYAN, align="center")
    # casa de los padres
    if t > t_casa - 0.1:
        a_, dy = pop(t, t_casa - 0.1)
        window(cv, 286, 150 + dy, 174, 22)
        dd = ImageDraw.Draw(cv)
        hx, hy = 294, 155 + dy
        dd.polygon([(hx, hy + 5), (hx + 6, hy), (hx + 12, hy + 5)], fill=(220, 90, 70, 255), outline=(*INK, 255))
        dd.rectangle([hx + 2, hy + 5, hx + 10, hy + 12], fill=(240, 220, 180, 255), outline=(*INK, 255))
        draw_text(cv, "CASA DE SUS PADRES", 310, 157 + dy, "press", 8, CREAM)
    return vignette(cv, 0.3)


# --------------------------------------------------------------------------- resultados

def crowd(cv, t, y=226, quiet=False):
    d = ImageDraw.Draw(cv)
    for i in range(12):
        x = 20 + i * 40
        bob = 0 if quiet else int(abs(math.sin(t * 6 + i)) * 3)
        hy = y - bob + (i % 2) * 6
        d.ellipse([x - 12, hy - 12, x + 12, hy + 12], fill=(8, 8, 18, 255))
        d.rectangle([x - 18, hy + 8, x + 18, H], fill=(8, 8, 18, 255))
        d.ellipse([x - 18, hy + 4, x + 18, hy + 20], fill=(8, 8, 18, 255))


def sc_results(t):
    """El resultado deja mudo al campo: 15,3 % contra 26,2 %."""
    cv = stage_bg((8, 10, 28), (26, 32, 70), 190)
    for xx in (120, 240, 360):
        cv = spotlight(cv, xx, 0, 190, 8, 70, strength=0.12)
    t_res = WD("c5_06", "resultado")
    t_mudo = WD("c5_06", "mudo")
    t_err = WD("c5_06", "error")
    t_15 = WD("c5_06", "quince")
    t_c = WD("c5_06", "contra")
    t_26 = WD("c5_06", "veintiseis")
    t_seg = WD("c5_06", "segundo")
    # título
    a, dy = pop(t, t_res - 0.1)
    window(cv, 60, 8 + dy, 360, 30)
    draw_text(cv, "TASA DE ERROR", 240, 16 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
    # tabla
    x0, y0 = 30, 48
    window(cv, x0, y0, 420, 112)
    draw_text(cv, "COMPETENCIA IMAGENET 2012", x0 + 12, y0 + 10, "press", 8, CYAN)
    draw_text(cv, "(MENOS ES MEJOR)", x0 + 408, y0 + 10, "silk", 8, GREY, align="right")
    d = ImageDraw.Draw(cv)
    bx = x0 + 120
    scale = 230 / 26.2
    rows = [("ALEXNET", 15.3, t_15, GOLD), ("SEGUNDO", 26.2, t_26, (150, 156, 176))]
    for i, (lab, val, tv, col) in enumerate(rows):
        yy = y0 + 32 + i * 38
        draw_text(cv, lab, x0 + 12, yy + 8, "press", 8, CREAM if i == 0 else GREY)
        d.rectangle([bx, yy, bx + 230, yy + 24], fill=(14, 16, 36, 255), outline=(40, 46, 86, 255))
        p = ease_out(prog(t, tv - 0.15, tv + 0.6))
        if p > 0:
            ln = int(val * scale * p)
            c = col
            if i == 0 and t > t_seg + 0.3 and int(t * 6) % 2:
                c = (255, 250, 210)
            d.rectangle([bx, yy, bx + ln, yy + 24], fill=(*c, 255), outline=(*INK, 255))
            d.line([(bx + 1, yy + 1), (bx + ln - 1, yy + 1)], fill=(*shade(c, 1.2), 255))
            num = f"{val * p:.1f}".replace(".", ",") + " %"
            draw_text(cv, num, bx + ln + 6, yy + 4, "press", 16, CREAM if i == 0 else GREY)
    if t > t_seg + 0.2:
        a2, dy2 = pop(t, t_seg + 0.2)
        window(cv, 120, 166 + dy2, 240, 20, fill=(30, 80, 50), border=GREEN)
        draw_text(cv, "¡CASI 11 PUNTOS MENOS!", 240, 172 + dy2, "press", 8, CREAM, align="center")
    # el público, mudo
    crowd(cv, t, quiet=True)
    if t_mudo - 0.1 < t < t_15:
        for i, x in enumerate((60, 180, 300, 420)):
            a3, dy3 = pop(t, t_mudo - 0.1 + i * 0.1)
            if a3 > 0:
                bubble(cv, "...", x, 206 + dy3)
    if t > t_15 + 0.3:
        for i, x in enumerate((100, 260, 380)):
            a3, dy3 = pop(t, t_15 + 0.3 + i * 0.12)
            if a3 > 0:
                draw_text(cv, "!", x, 186 + dy3, "press", 16, GOLD, align="center")
    return vignette(cv, 0.35)


def trophy(cv, cx, top, t, alpha=1.0):
    im = Image.new("RGBA", (40, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    g, gd, gl = (240, 196, 80, 255), (176, 120, 40, 255), (255, 240, 170, 255)
    d.ellipse([1, 4, 10, 18], outline=(*INK, 255), width=3)
    d.ellipse([29, 4, 38, 18], outline=(*INK, 255), width=3)
    d.ellipse([2, 5, 9, 17], outline=gd, width=1)
    d.ellipse([30, 5, 37, 17], outline=gd, width=1)
    d.polygon([(7, 1), (32, 1), (29, 20), (22, 27), (17, 27), (10, 20)], fill=g, outline=(*INK, 255))
    d.line([(11, 4), (13, 18)], fill=gl, width=2)
    d.rectangle([17, 27, 22, 35], fill=gd, outline=(*INK, 255))
    d.rectangle([11, 35, 28, 39], fill=g, outline=(*INK, 255))
    d.rectangle([8, 39, 31, 47], fill=(90, 56, 34, 255), outline=(*INK, 255))
    d.rectangle([14, 41, 25, 44], fill=gl)
    big = Image.fromarray(np.repeat(np.repeat(np.array(im), 3, 0), 3, 1), "RGBA")
    paste(cv, big, cx - 60, top, alpha)


def sc_win(t):
    """Las redes neuronales, las mismas que habían dado por muertas, acababan de ganar."""
    cv = stage_bg((8, 10, 28), (30, 30, 70), 200)
    t_red = WD("c5_07", "redes")
    t_muer = WD("c5_07", "muertas")
    t_aca = WD("c5_07", "acababan")
    t_gan = WD("c5_07", "ganar")
    won = t > t_gan
    if won:
        for xx in (100, 240, 380):
            cv = spotlight(cv, xx, 0, 200, 10, 90, color=(255, 220, 140), strength=0.18)
    # red gigante de fondo
    L = net_layers([60, 130, 200, 280, 350, 420], [4, 6, 6, 6, 5, 3], 98, 14)
    g = 0.35 + 0.65 * ease_out(prog(t, t_red, t_red + 0.6))
    if t_muer < t < t_gan:
        g *= 0.5 + 0.5 * (int(t * 10) % 2)
    draw_net(cv, L, glow=g, r=3)
    net_pulses(cv, L, ((t - t_red) * 3.0) % 5.5, (255, 230, 140))
    # lápida que estalla
    if t < t_aca + 0.3:
        d = ImageDraw.Draw(cv)
        gx, gy = 240, 132
        p = prog(t, t_muer - 0.2, t_muer + 0.2)
        if p > 0:
            shk = int(math.sin(t * 50) * 2) if t > t_aca - 0.2 else 0
            yoff = int((1 - ease_out(p)) * 60)
            gx += shk
            d.rectangle([gx - 36, gy + yoff, gx + 36, 206], fill=(110, 112, 126, 255), outline=(*INK, 255))
            d.pieslice([gx - 36, gy - 30 + yoff, gx + 36, gy + 30 + yoff], 180, 360, fill=(110, 112, 126, 255),
                       outline=(*INK, 255))
            d.line([(gx - 35, gy + yoff), (gx + 35, gy + yoff)], fill=(110, 112, 126, 255))
            draw_text(cv, "R.I.P.", gx, gy - 14 + yoff, "press", 8, (40, 40, 52), align="center", outline=None,
                      shadow=False)
            draw_text(cv, "REDES", gx, gy + 4 + yoff, "press", 8, (40, 40, 52), align="center", outline=None,
                      shadow=False)
            draw_text(cv, "NEURONALES", gx, gy + 16 + yoff, "silkb", 8, (40, 40, 52), align="center", outline=None,
                      shadow=False)
            if t > t_aca - 0.2:
                k = prog(t, t_aca - 0.2, t_aca + 0.2)
                crack = [(gx - 4, gy - 26), (gx + 4, gy - 8), (gx - 6, gy + 10), (gx + 5, gy + 30), (gx - 2, gy + 60)]
                n = max(2, int(len(crack) * k))
                d.line(crack[:n], fill=(255, 230, 140, 255), width=2)
    if t_aca + 0.3 <= t < t_gan + 0.5:
        p = (t - t_aca - 0.3) / (t_gan + 0.2 - t_aca - 0.3)
        d = ImageDraw.Draw(cv)
        for i in range(16):
            ang = i / 16 * 2 * math.pi
            rr = 10 + p * 120
            x = 240 + math.cos(ang) * rr
            y = 160 + math.sin(ang) * rr * 0.7 + p * p * 60
            d.rectangle([int(x), int(y), int(x) + 4, int(y) + 3], fill=(110, 112, 126, 255), outline=(*INK, 255))
    # trofeo
    if t > t_aca + 0.3:
        p = prog(t, t_aca + 0.3, t_aca + 0.7)
        top = int(54 + (1 - ease_out_back(p)) * 40)
        trophy(cv, 240, top + (int(abs(math.sin(t * 4)) * 3) if won else 0), t, alpha=min(1, p * 2))
        if won:
            for i in range(6):
                sparkle(cv, 190 + i * 20, 60 + (i % 3) * 30, t + i * 0.5, 4, GOLD)
    # personajes
    hop = lambda i: int(abs(math.sin(t * 8 + i)) * 12) if won else 0
    for i, (k, x) in enumerate((("krizhevsky", 56), ("sutskever", 130), ("hinton12", 424))):
        char(cv, k, x, 266 - hop(i), t, scale=3, arms="cheer" if won else "down",
             mood="happy" if won or t < t_muer else "worried", look=1 if x < 240 else -1)
    robot(cv, 340, 266 - hop(3), t, face="heart" if won else ("think" if t < t_aca else "question"), scale=3)
    # textos
    if t < t_gan:
        draw_text(cv, "LAS REDES NEURONALES", 240, 12, "press", 16, CREAM, align="center",
                  reveal=(t - t_red + 0.1) * 26)
        if t > t_muer - 0.3:
            draw_text(cv, "¿DADAS POR MUERTAS?", 240, 34, "press", 8, GREY, align="center",
                      reveal=(t - t_muer + 0.3) * 30)
    else:
        a, dy = pop(t, t_gan)
        draw_text(cv, "¡GANARON!", 240, 8 + dy, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
        CONF.draw(cv, t - t_gan)
        CONF.draw(cv, t - t_gan + 2.0)
    for t0 in (t_gan,):
        if t0 <= t < t0 + 0.15:
            cv = fade_to(cv, (255, 250, 230), 0.35 * (1 - (t - t0) / 0.15))
    dx, dy = shake(t, t_gan, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.3)


# =========================================================================== montaje

def scenes():
    c5s = TL.chapter_start(5)
    return [
        (c5s - 0.3, make_card(5, ["PLACAS DE", "VIDEOJUEGOS"], "1997 – 2012"), None),
        (TL.s("c5_01") - 0.2, sc_chess,
         lambda t: (cam_push(t, WD("c5_01", "derrota") - 0.5, TL.e("c5_01"), 1.0, 1.1, (240, 135), (220, 125))[0]
                    + cam_punch(t, [WD("c5_01", "derrota") + 0.45], 0.08),
                    *cam_push(t, WD("c5_01", "derrota") - 0.5, TL.e("c5_01"), 1.0, 1.1, (240, 135), (220, 125))[1:])),
        (TL.s("c5_02") - 0.15, sc_brute,
         lambda t: (1.0 + cam_punch(t, [WD("c5_02", "aprende"), WD("c5_02", "calcula"), WD("c5_02", "fuerza") + 0.1],
                                    0.06), 240, 135)),
        (TL.s("c5_03") - 0.15, sc_imagenet,
         lambda t: (1.0 + cam_punch(t, [WD("c5_03", "ImageNet")], 0.08), 240, 135)),
        (TL.s("c5_04") - 0.15, sc_toronto,
         lambda t: (1.0 + cam_punch(t, [WD("c5_04", n) for n in ("Alex", "Ilya", "Geoffrey")], 0.04)
                    + cam_punch(t, [WD("c5_04", "AlexNet")], 0.08), 240, 135)),
        (TL.s("c5_05") - 0.15, sc_gpus,
         lambda t: (1.0 + cam_punch(t, [WD("c5_05", "placas"), WD("c5_05", "casa")], 0.04), 240, 135)),
        (TL.s("c5_06") - 0.15, sc_results,
         lambda t: (1.0 + cam_punch(t, [WD("c5_06", "quince"), WD("c5_06", "veintiseis")], 0.08), 240, 120)),
        (TL.s("c5_07") - 0.15, sc_win,
         lambda t: (1.0 + cam_punch(t, [WD("c5_07", "ganar")], 0.12), 240, 135)),
    ]


# =========================================================================== audio

def music(A):
    s, e = TL.s, TL.e
    t_start = TL.chapter_start(5) + 1.6
    t_end = chapter_end(5)
    Em = [("E", "min"), ("C", "maj"), ("A", "min"), ("B", "maj")]
    A.section(t_start, s("c5_02") - 0.15, 112, Em, A.st_puzzle)
    A.kick(A.music, WD("c5_01", "derrota") + 0.45, 0.4)
    A.section(s("c5_02") - 0.15, s("c5_03") - 0.15, 132, [("E", "min"), ("D", "maj")], A.st_puzzle)
    A.crash(A.music, WD("c5_02", "fuerza") + 0.1, 0.08)
    A.section(s("c5_03") - 0.15, s("c5_04") - 0.15, 92, [("D", "maj"), ("A", "maj"), ("B", "min"), ("G", "maj")],
              A.st_mystery)
    A.sting(WD("c5_03", "ImageNet"), [74, 78, 81, 86], vol=0.04, step=0.09, hold=1.0)
    A.section(s("c5_04") - 0.15, s("c5_06") - 0.15, 112, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")],
              A.st_build)
    A.sting(WD("c5_04", "AlexNet"), [69, 72, 76, 81], vol=0.04, step=0.08, hold=0.8)
    # silencio tenso: deja mudo al campo
    tr = s("c5_06") - 0.15
    t15 = WD("c5_06", "quince")
    A.note(A.music, tr, A.midi_hz(40), t15 - tr, "tri", vol=0.2, a=0.2, s=0.9, r=0.4)
    A.section(t15, s("c5_07") - 0.15, 120, [("F", "maj"), ("G", "maj"), ("A", "min"), ("G", "maj")], A.st_build)
    A.kick(A.music, t15, 0.4)
    A.kick(A.music, WD("c5_06", "veintiseis"), 0.4)
    # triunfo
    tw = s("c5_07") - 0.15
    tg = WD("c5_07", "ganar")
    A.section(tw, tg, 132, [("F", "maj"), ("G", "maj")], A.st_build)
    A.section(tg, t_end, 132, [("C", "maj"), ("F", "maj"), ("G", "maj"), ("C", "maj")], A.st_triumph)
    A.kick(A.music, tg, 0.5)
    A.crash(A.music, tg, 0.18)
    for m in (60, 64, 67, 72):
        A.note(A.music, tg, A.midi_hz(m + 12), 1.4, duty=0.5, vol=0.04, s=0.7, r=0.5)
    A.note(A.music, tg, A.midi_hz(48), 1.6, "tri", vol=0.3, s=0.9, r=0.5)


def sfx(A):
    s, e = TL.s, TL.e
    # ajedrez
    A.whoosh(s("c5_01") - 0.1, 0.35)
    A.robot_beep(WD("c5_01", "computadora"), 0.035)
    A.text_blips(WD("c5_01", "Deep") - 0.1, 9, 24)
    A.pop_sfx(WD("c5_01", "IBM") - 0.1, 450)
    td = WD("c5_01", "derrota")
    A.whoosh(td, 0.45, 0.06)
    A.kick(A.sfx, td + 0.45, 0.35)
    A.pop_sfx(td + 0.5, 300, 0.06)
    A.join_jingle(WD("c5_01", "Garry") - 0.1)
    # fuerza bruta
    A.coin(WD("c5_02", "hito"), 0.05)
    A.pop_sfx(WD("c5_02", "aprende") - 0.15, 500)
    A.text_blips(WD("c5_02", "calcula") - 0.1, 7, 24)
    tc = WD("c5_02", "calcula")
    for i in range(30):
        A.blip(tc + i * 0.06, 700 + (i * 137) % 900, 0.015, 0.02)
    tm = WD("c5_02", "millones")
    for i in range(14):
        A.blip(tm + i * 0.08, 1200 + (i % 4) * 100, 0.02, 0.025)
    A.whoosh(WD("c5_02", "fuerza") - 0.1, 0.3, 0.07)
    A.kick(A.sfx, WD("c5_02", "fuerza") + 0.05, 0.4)
    # ImageNet
    A.robot_beep(WD("c5_03", "verdadero") + 0.8, 0.03)
    A.whoosh(WD("c5_03", "nueve") - 0.2, 0.3)
    A.join_jingle(WD("c5_03", "Fei-Fei"))
    A.pop_sfx(WD("c5_03", "ImageNet") - 0.1, 600)
    ti = WD("c5_03", "ImageNet")
    for i in range(24):
        A.blip(ti + i * 0.08, 1500 + (i * 91) % 700, 0.012, 0.018)
    for i in range(6):
        A.pop_sfx(WD("c5_03", "etiquetadas") - 0.1 + i * 0.12, 700 + i * 60, 0.04)
    # Toronto
    A.whoosh(WD("c5_04", "dos") - 0.15, 0.3)
    A.pop_sfx(WD("c5_04", "Universidad") - 0.1, 500, 0.05)
    for n in ("Alex", "Ilya", "Geoffrey"):
        A.join_jingle(WD("c5_04", n) - 0.1)
    A.whoosh(WD("c5_04", "AlexNet") - 0.15, 0.3, 0.06)
    A.coin(WD("c5_04", "AlexNet") + 0.1, 0.05)
    A.pop_sfx(WD("c5_04", "competencia") - 0.1, 650, 0.05)
    # GPUs
    A.pop_sfx(WD("c5_05", "red") - 0.1, 550)
    tp = WD("c5_05", "placas") - 0.25
    A.pop_sfx(tp, 400, 0.06)
    A.pop_sfx(tp + 0.25, 480, 0.06)
    # zumbido de ventiladores
    n = int(3.0 * A.SR)
    x = A.noise(3.0, 6)
    env = np.minimum(1, np.minimum(np.arange(n) / (0.8 * A.SR), (n - np.arange(n)) / (0.6 * A.SR)))
    A.sfx.add(tp, x * env, 0.02)
    A.pop_sfx(WD("c5_05", "gamers") - 0.1, 620, 0.04)
    A.pop_sfx(WD("c5_05", "casa") - 0.1, 520, 0.05)
    # resultados
    A.pop_sfx(WD("c5_06", "resultado") - 0.1, 500, 0.05)
    for i in range(4):
        A.blip(WD("c5_06", "mudo") - 0.1 + i * 0.1, 300, 0.03, 0.02)
    t15 = WD("c5_06", "quince")
    A.whoosh(t15 - 0.15, 0.4, 0.06)
    A.text_blips(t15, 12, 20, 0.02, 1200)
    t26 = WD("c5_06", "veintiseis")
    A.whoosh(t26 - 0.15, 0.4, 0.05)
    A.text_blips(t26, 12, 20, 0.02, 900)
    A.coin(WD("c5_06", "segundo") + 0.2, 0.06)
    # victoria
    A.robot_beep(WD("c5_07", "redes"), 0.03)
    A.freeze(WD("c5_07", "muertas"), 0.04)
    ta = WD("c5_07", "acababan")
    for i in range(5):
        A.blip(ta - 0.2 + i * 0.08, 200 + i * 40, 0.04, 0.04, 0.5)
    A.whoosh(ta + 0.3, 0.5, 0.07)
    tg = WD("c5_07", "ganar")
    A.kick(A.sfx, tg, 0.4)
    A.join_jingle(tg + 0.05, 0.07)
    for i in range(10):
        A.pop_sfx(tg + 0.1 + i * 0.07, 600 + (i % 4) * 150, 0.04)
    # aplausos (ráfagas de ruido cortas)
    tt = tg + 0.2
    k = 0
    while tt < chapter_end(5) - 0.2:
        sig = A.noise(0.02, 1) * np.exp(-np.arange(int(0.02 * A.SR)) / A.SR * 160)
        A.sfx.add(tt, sig, 0.03)
        tt += 0.025 + ((k * 37) % 11) / 400
        k += 1
