"""Capítulo 4: Reglas, expertos y el segundo invierno (1980 – 1993)."""
from common import *  # noqa

WD = TL.word
RED = (230, 70, 60)
GREEN = (110, 230, 120)
PAPER = (246, 240, 222)


# =========================================================================== helpers

def darken(cv, box, k, col=(0, 0, 0)):
    """Oscurece (mezcla con col) una región rectangular. Devuelve imagen nueva."""
    if k <= 0:
        return cv
    x0, y0, x1, y1 = [int(v) for v in box]
    a = np.array(cv)
    reg = a[y0:y1, x0:x1, :3].astype(np.float32)
    a[y0:y1, x0:x1, :3] = (reg * (1 - k) + np.array(col, dtype=np.float32) * k).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def arrow_r(d, x, y, col):
    d.line([(x, y + 2), (x + 6, y + 2)], fill=(*col, 255))
    d.line([(x + 4, y), (x + 6, y + 2), (x + 4, y + 4)], fill=(*col, 255))


def check(d, x, y, col=GREEN, s=2):
    pts = [(x, y + 3 * s), (x + 2 * s, y + 5 * s), (x + 6 * s, y)]
    d.line(pts, fill=(*INK, 255), width=s + 2)
    d.line(pts, fill=(*col, 255), width=s)


def cross_mark(d, x, y, col=RED, s=2):
    for pts in (((x, y), (x + 5 * s, y + 5 * s)), ((x + 5 * s, y), (x, y + 5 * s))):
        d.line(pts, fill=(*INK, 255), width=s + 2)
    for pts in (((x, y), (x + 5 * s, y + 5 * s)), ((x + 5 * s, y), (x, y + 5 * s))):
        d.line(pts, fill=(*col, 255), width=s)


def rule_card(cv, x, y, cond, res):
    """Tarjeta de regla «SI cond → res» sobre papel. Devuelve el ancho."""
    sw, _ = text_size("SI", "silkb", 8)
    cw, _ = text_size(cond, "silk", 8)
    rw, _ = text_size(res, "silkb", 8)
    wd = 6 + sw + 4 + cw + 5 + 8 + 4 + rw + 6
    draw_paper(cv, x, y, wd, 14)
    d = ImageDraw.Draw(cv)
    d.rectangle([x + 1, y + 1, x + 2, y + 13], fill=(200, 70, 60, 255))
    xx = x + 6
    draw_text(cv, "SI", xx, y + 3, "silkb", 8, (180, 40, 40), outline=None, shadow=False)
    xx += sw + 4
    draw_text(cv, cond, xx, y + 3, "silk", 8, INK, outline=None, shadow=False)
    xx += cw + 5
    arrow_r(d, xx, y + 5, (90, 90, 110))
    xx += 8 + 4
    draw_text(cv, res, xx, y + 3, "silkb", 8, (20, 90, 160), outline=None, shadow=False)
    return wd


def mini_card(d, x, y, w=9, h=5):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214, 255), outline=(110, 100, 86, 255))
    d.line([(x + 2, y + 2), (x + w - 2, y + 2)], fill=(170, 160, 150, 255))
    d.point((x + 1, y + 1), fill=(200, 70, 60, 255))


def coin_px(d, cx, cy, t, ph=0.0):
    k = abs(math.cos(t * 6 + ph))
    rw = max(1, int(4 * k))
    d.ellipse([cx - rw, cy - 4, cx + rw, cy + 4], fill=(240, 200, 80, 255), outline=(120, 70, 20, 255))
    if rw > 2:
        d.line([(cx, cy - 2), (cx, cy + 2)], fill=(180, 120, 40, 255))


def poly_rot(d, cx, cy, w, h, ang, fill, outline):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for (px, py) in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((int(cx + px * ca - py * sa), int(cy + px * sa + py * ca)))
    d.polygon(pts, fill=fill, outline=outline)


def net_layers(xs, sizes, cy, gap):
    return [[(x, int(cy + (i - (n - 1) / 2) * gap)) for i in range(n)] for x, n in zip(xs, sizes)]


def draw_net(cv, layers, glow=1.0, edge=(50, 110, 140), node=(120, 230, 255), r=3, node_glow=None):
    d = ImageDraw.Draw(cv)
    ec = tuple(int(c * (0.4 + 0.6 * glow)) for c in edge)
    for la, lb in zip(layers, layers[1:]):
        for p in la:
            for q in lb:
                d.line([p, q], fill=(*ec, 255))
    for li, L in enumerate(layers):
        for ni, (x, y) in enumerate(L):
            g = glow if node_glow is None else node_glow(li, ni)
            nc = tuple(int(30 + (c - 30) * (0.25 + 0.75 * g)) for c in node)
            if g > 0.5:
                d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=(*node, int(70 * g)))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(*nc, 255), outline=(*INK, 255))
            if g > 0.5:
                d.point((x - 1, y - 1), fill=(240, 255, 255, 255))


def net_pulses(cv, layers, s, color, backward=False, size=1):
    """Pulsos sobre las aristas. s = posición de la onda en «capas» (0 .. len-1)."""
    d = ImageDraw.Draw(cv)
    L = len(layers)
    for l in range(L - 1):
        u = (s - l) if not backward else (s - (L - 2 - l))
        if not (0 <= u <= 1):
            continue
        for p in layers[l]:
            for q in layers[l + 1]:
                a, b = (p, q) if not backward else (q, p)
                x = int(a[0] + (b[0] - a[0]) * u)
                y = int(a[1] + (b[1] - a[1]) * u)
                d.rectangle([x - size, y - size, x + size, y + size], fill=(*color, 255))


def glow_disc(cv, cx, cy, r, k, color=(90, 220, 255)):
    """Halo circular con dithering Bayer (más denso en el centro)."""
    if k <= 0:
        return cv
    a = np.array(cv)
    x0, x1 = max(0, cx - r), min(W, cx + r)
    y0, y1 = max(0, cy - r), min(H, cy + r)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dist = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 0.8)) ** 2)
    dens = np.clip(1 - dist, 0, 1) ** 1.5 * 0.55 * k
    th = bayer_tile(W, H)[y0:y1, x0:x1]
    m = th < dens
    reg = a[y0:y1, x0:x1, :3].astype(np.float32)
    reg[m] = reg[m] * 0.45 + np.array(color, dtype=np.float32) * 0.55
    a[y0:y1, x0:x1, :3] = reg.astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def snow_floor(cv, top, seed=0.0, col=(226, 236, 248)):
    a = np.array(cv)
    for x in range(W):
        e = int(top + math.sin(x * 0.19 + seed) * 2 + math.sin(x * 0.05 + 1 + seed) * 3)
        e = max(0, min(H, e))
        a[e:, x, :3] = col
        if e < H:
            a[e, x, :3] = (255, 255, 255)
        if e + 3 < H:
            a[e + 3:, x, :3] = (208, 222, 240) if (x + e) % 7 else (190, 206, 232)
    return Image.fromarray(a, "RGBA")


def tag(cv, txt, cx, y, t, t0, fill=(20, 24, 52), col=CREAM, border=GOLD):
    a, dy = pop(t, t0)
    if a <= 0:
        return
    tw, _ = text_size(txt, "press", 8)
    window(cv, cx - tw // 2 - 6, y + dy, tw + 12, 16, fill=fill, border=border)
    draw_text(cv, txt, cx, y + 4 + dy, "press", 8, col, align="center")


def intro_card(cv, pname, title, sub, t, t_in, t_out, x=14, y=176):
    """Patrón de presentación (retrato + ventana con nombre), entra y sale por la izquierda."""
    if t < t_in - 0.2 or t > t_out + 0.4:
        return
    a = prog(t, t_in - 0.2, t_in + 0.2)
    off = int((1 - ease_out(a)) * -380) + int(ease_in_out(prog(t, t_out, t_out + 0.4)) * -420)
    portrait_card(cv, pname, x + off, y)
    tw = max(text_size(title, "press", 16)[0], text_size(sub, "silk", 8)[0]) + 22
    window(cv, x + 72 + off, y + 14, tw, 46)
    draw_text(cv, title, x + 82 + off, y + 24, "press", 16, CREAM)
    draw_text(cv, sub, x + 82 + off, y + 44, "silk", 8, GREY)


# =========================================================================== escenas

RULES = [("FIEBRE Y TOS", "INFECCIÓN"), ("INFECCIÓN", "ANTIBIÓTICO"), ("ALERGIA", "NO PENICILINA"),
         ("CPU = VAX", "GABINETE B"), ("MEMORIA < 4 MB", "AGREGAR PLACA"), ("DISCO LLENO", "2DO DISCO")]

_rng = np.random.default_rng(3)
WALL_COLS, WALL_ROWS = 30, 24
WALL_ORDER = _rng.permutation(WALL_COLS * WALL_ROWS)


def sc_experts(t):
    """En los ochenta... los sistemas expertos. Miles de reglas escritas a mano."""
    cv = bg("bg_corporate_1985").copy()
    t0 = TL.s("c4_01")
    t_vuelve = WD("c4_01", "vuelve")
    t_sis = WD("c4_01", "sistemas")
    t_exp = WD("c4_01", "expertos")
    t_sig = WD("c4_02", "siguen")
    t_miles = WD("c4_02", "miles")
    t_mano = WD("c4_02", "escritas")
    t_end = TL.e("c4_02")
    # pantallas de las terminales encendidas (parpadeo de texto)
    d = ImageDraw.Draw(cv)
    for (x0, y0) in ((122, 117), (242, 117)):
        for i in range(3):
            ll = 4 + ((i * 5 + int(t * 4)) % 16)
            d.line([(x0, y0 + i * 4), (x0 + ll, y0 + i * 4)], fill=(120, 250, 160, 255))
    # muro de reglas que se llena
    fill = ease_in_out(prog(t, t_miles, t_end + 0.2)) ** 1.3
    n = int(fill * len(WALL_ORDER))
    if n > 0:
        for idx in WALL_ORDER[:n]:
            r, c = divmod(int(idx), WALL_COLS)
            mini_card(d, 12 + c * 11, 50 + r * 7)
    # años 80
    if t < t_sis:
        a_out = 1 - prog(t, t_sis - 0.4, t_sis)
        if a_out > 0:
            p = prog(t, t0, t0 + 0.55)
            yy = 40 - (1 - ease_out_back(p, 2.2)) * 50
            draw_text(cv, "AÑOS 80", 240, int(yy), "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2,
                      alpha=min(p * 3, a_out))
    # título
    if t > t_sis - 0.1:
        a, dy = pop(t, t_sis - 0.1)
        window(cv, 40, 8 + dy, 400, 30)
        draw_text(cv, "LOS SISTEMAS EXPERTOS", 240, 16 + dy, "press", 16, align="center", gradient=GOLD_RAMP,
                  reveal=(t - t_sis + 0.1) * 30)
    # tarjetas legibles
    for i, (cnd, res) in enumerate(RULES):
        ti = t_sig + i * 0.3
        if t > ti:
            a, dy = pop(t, ti)
            rule_card(cv, 16, 50 + i * 20 + dy, cnd, res)
    # el ingeniero del conocimiento
    x, ph = walk(t, t_vuelve - 0.6, t_vuelve + 0.7, W + 40, 404)
    writing = t_mano - 0.1 < t < t_end + 0.3
    arms = "down"
    if ph is None and t_exp < t < t_sig:
        arms = "point_l"
    if writing:
        arms = "write"
    if t > t_end + 0.3:
        arms = "point_l"
    char(cv, "kengineer", x, 266, t, scale=3, walk=ph, facing=-1 if ph is not None else 1, arms=arms,
         mood="happy" if t > t_exp else "neutral", look=-1 if writing else 0)
    if writing:
        dd = ImageDraw.Draw(cv)
        bx, by = int(x) - 16, 196
        dd.rectangle([bx, by, bx + 22, by + 28], fill=(150, 104, 60, 255), outline=(*INK, 255))
        dd.rectangle([bx + 3, by + 4, bx + 19, by + 26], fill=(*PAPER, 255))
        k = int((t - t_mano) * 8) % 6
        for j in range(min(5, k + 1)):
            dd.line([(bx + 5, by + 8 + j * 4), (bx + 15 - (j % 2) * 4, by + 8 + j * 4)], fill=(60, 60, 90, 255))
        dd.rectangle([bx + 8, by - 2, bx + 14, by + 2], fill=(160, 160, 170, 255), outline=(*INK, 255))
    # contador de reglas
    if t > t_miles - 0.1:
        a, dy = pop(t, t_miles - 0.1)
        window(cv, 12, 224 + dy, 236, 34)
        draw_text(cv, "REGLAS:", 22, 236 + dy, "press", 8, CREAM)
        v = int(fill * 10000)
        draw_text(cv, f"{v:,}".replace(",", "."), 84, 232 + dy, "press", 16, align="left", gradient=GOLD_RAMP)
        if fill > 0.98:
            draw_text(cv, "¡MILES!", 236, 236 + dy, "press", 8, (255, 120, 90), align="right")
    # presentación del ingeniero
    intro_card(cv, "expert_engineer_1985", "EL INGENIERO", "DEL CONOCIMIENTO · TRADUCE A EXPERTOS EN REGLAS",
               t, t_exp, t_sig - 0.3)
    return vignette(cv, 0.35)


def med_icon(cv, x, y):
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + 36, y + 36], fill=(246, 244, 238, 255), outline=(*INK, 255))
    d.rectangle([x + 13, y + 5, x + 23, y + 31], fill=(214, 52, 56, 255), outline=(120, 20, 30, 255))
    d.rectangle([x + 5, y + 13, x + 31, y + 23], fill=(214, 52, 56, 255), outline=(120, 20, 30, 255))
    d.rectangle([x + 14, y + 14, x + 22, y + 22], fill=(214, 52, 56, 255))
    # píldora
    d.rounded_rectangle([x + 24, y + 28, x + 44, y + 36], 4, fill=(240, 230, 220, 255), outline=(*INK, 255))
    d.rectangle([x + 34, y + 29, x + 43, y + 35], fill=(90, 160, 230, 255))


def pc_icon(cv, x, y, t):
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + 40, y + 28], fill=(214, 204, 178, 255), outline=(*INK, 255))
    d.rectangle([x + 4, y + 4, x + 36, y + 22], fill=(14, 40, 26, 255))
    for i in range(3):
        ll = 6 + ((i * 7 + int(t * 4)) % 20)
        d.line([(x + 7, y + 8 + i * 4), (x + 7 + ll, y + 8 + i * 4)], fill=(100, 250, 150, 255))
    d.rectangle([x + 14, y + 29, x + 26, y + 32], fill=(150, 140, 120, 255), outline=(*INK, 255))
    d.rectangle([x - 2, y + 33, x + 42, y + 38], fill=(200, 190, 166, 255), outline=(*INK, 255))


def stage_bg(top=(10, 14, 34), bottom=(30, 40, 80), floor_y=206):
    cv = vgradient(top, bottom, 14)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, floor_y, W, H], fill=(20, 22, 44, 255))
    for y in (floor_y, floor_y + 8, floor_y + 20, floor_y + 36, floor_y + 56):
        d.line([(0, y), (W, y)], fill=(40, 46, 86, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, floor_y), (x, H)], fill=(30, 34, 66, 255))
    return cv


_crng = np.random.default_rng(11)
COINS = [(_crng.uniform(0, W), _crng.uniform(-260, 0), _crng.uniform(90, 150), i * 0.7) for i in range(40)]


def sc_boom(t):
    """Diagnostican infecciones, configuran computadoras, y las empresas invierten fortunas."""
    cv = stage_bg()
    t_diag = TL.s("c4_03")
    t_conf = WD("c4_03", "configuran")
    t_emp = WD("c4_03", "empresas")
    t_inv = WD("c4_03", "invierten")
    t_fort = WD("c4_03", "fortunas")
    # tarjeta 1: diagnóstico
    if t > t_diag - 0.1:
        a, dy = pop(t, t_diag - 0.1)
        window(cv, 22, 20 + dy, 210, 92)
        med_icon(cv, 36, 44 + dy)
        draw_text(cv, "DIAGNÓSTICO", 96, 34 + dy, "press", 8, GOLD)
        draw_text(cv, "MYCIN", 96, 52 + dy, "press", 16, CREAM)
        draw_text(cv, "INFECCIONES", 96, 76 + dy, "silk", 8, GREY)
        draw_text(cv, "EN LA SANGRE", 96, 88 + dy, "silk", 8, GREY)
        if t > WD("c4_03", "infecciones") + 0.3:
            check(ImageDraw.Draw(cv), 204, 88 + dy)
    if t > t_conf - 0.1:
        a, dy = pop(t, t_conf - 0.1)
        window(cv, 248, 20 + dy, 210, 92)
        pc_icon(cv, 260, 44 + dy, t)
        draw_text(cv, "CONFIGURACIÓN", 312, 34 + dy, "press", 8, GOLD)
        draw_text(cv, "XCON", 312, 52 + dy, "press", 16, CREAM)
        draw_text(cv, "ARMA PEDIDOS DE", 312, 76 + dy, "silk", 8, GREY)
        draw_text(cv, "COMPUTADORAS VAX", 312, 88 + dy, "silk", 8, GREY)
        if t > WD("c4_03", "computadoras") + 0.4:
            check(ImageDraw.Draw(cv), 432, 88 + dy)
    # gráfico de inversión
    if t > t_emp - 0.1:
        a, dy = pop(t, t_emp - 0.1)
        x0, y0 = 132, 124 + dy
        window(cv, x0, y0, 216, 132)
        draw_text(cv, "INVERSIÓN EN IA", x0 + 12, y0 + 10, "press", 8, CREAM)
        d = ImageDraw.Draw(cv)
        px0, py0, px1, py1 = x0 + 14, y0 + 26, x0 + 202, y0 + 120
        for gy in range(py0, py1 + 1, 16):
            d.line([(px0, gy), (px1, gy)], fill=(40, 50, 96, 255))
        d.line([(px0, py0), (px0, py1)], fill=(*GREY, 255))
        d.line([(px0, py1), (px1, py1)], fill=(*GREY, 255))
        rv = ease_out(prog(t, t_emp, t_fort + 0.9))
        pts = []
        npts = 24
        for i in range(int(npts * rv) + 1):
            u = i / npts
            v = 0.08 + 0.85 * u ** 1.6 + (math.sin(i * 2.1) * 0.03 if i % 3 else -0.04)
            pts.append((int(px0 + u * (px1 - px0 - 10)), int(py1 - v * (py1 - py0))))
        if len(pts) > 1:
            d.line(pts, fill=(*INK, 255), width=4)
            d.line(pts, fill=(*GREEN, 255), width=2)
            ex, ey = pts[-1]
            d.polygon([(ex - 4, ey + 1), (ex + 4, ey + 1), (ex, ey - 6)], fill=(*GREEN, 255), outline=(*INK, 255))
        if t > t_fort + 0.3:
            a2, dy2 = pop(t, t_fort + 0.3)
            draw_text(cv, "US$ MILES DE", x0 + 22, y0 + 32 + dy2, "press", 8, GOLD)
            draw_text(cv, "MILLONES", x0 + 22, y0 + 44 + dy2, "press", 8, GOLD)
    # lluvia de monedas
    if t > t_inv:
        d = ImageDraw.Draw(cv)
        tt = t - t_inv
        for i, (cx, cy, sp, ph) in enumerate(COINS):
            yy = cy + tt * sp
            if -6 < yy < H + 6:
                coin_px(d, int(cx), int(yy), t, ph)
    # personajes
    cheer = t > t_inv
    hop = int(abs(math.sin(t * 7)) * 8) if cheer else 0
    char(cv, "kengineer", 66, 262 - hop, t, scale=2, arms="cheer" if cheer else ("point" if t > t_conf else "down"),
         mood="happy")
    robot(cv, 420, 262 - (int(abs(math.sin(t * 7 + 1)) * 8) if cheer else 0), t,
          face="heart" if t > t_fort else "happy", scale=2)
    return vignette(cv, 0.3)


def sc_japan(t):
    """Japón lanza su ambicioso proyecto de Quinta Generación."""
    cv = new_canvas((240, 228, 204))
    d = ImageDraw.Draw(cv)
    t_jap = WD("c4_03", "Japon")
    t_pro = WD("c4_03", "proyecto")
    t_q = WD("c4_03", "Quinta")
    t_gen = WD("c4_03", "Generacion")
    cx, cy = 240, 96
    # rayos del sol naciente
    ang0 = t * 0.15
    for i in range(16):
        if i % 2:
            continue
        a0 = ang0 + i * math.pi / 8
        a1 = a0 + math.pi / 8
        d.polygon([(cx, cy), (cx + math.cos(a0) * 600, cy + math.sin(a0) * 600),
                   (cx + math.cos(a1) * 600, cy + math.sin(a1) * 600)], fill=(236, 150, 136, 255))
    p = prog(t, t_jap - 0.2, t_jap + 0.35)
    r = int(56 * ease_out_back(p))
    if r > 0:
        d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(*INK, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 30, 45, 255))
        if r > 12:
            d.ellipse([cx - r + 6, cy - r + 6, cx - r // 3, cy - r // 3], fill=(222, 60, 70, 255))
    # contador de generaciones dentro del sol
    if t > t_pro and r > 40:
        k = min(5, 1 + int((t - t_pro) / max(0.05, (t_q - t_pro)) * 4))
        if k < 5:
            draw_text(cv, str(k), cx, cy - 12, "press", 24, CREAM, align="center")
        else:
            a, dy = pop(t, t_q)
            draw_text(cv, "5", cx, cy - 26 + dy, "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2)
            for i in range(4):
                sparkle(cv, cx - 40 + i * 26, cy - 30 + (i % 2) * 56, t + i, 3, CREAM)
    # ventana del título
    if t > t_jap:
        a, dy = pop(t, t_jap)
        window(cv, 72, 166 + dy, 336, 72)
        draw_text(cv, "PROYECTO", 240, 176 + dy, "press", 8, GOLD, align="center", reveal=(t - t_pro) * 24)
        draw_text(cv, "QUINTA GENERACIÓN", 240, 192 + dy, "press", 16, align="center", gradient=GOLD_RAMP,
                  reveal=(t - t_q + 0.1) * 26)
        draw_text(cv, "JAPÓN · 1982", 240, 218 + dy, "press", 8, CYAN, align="center")
    face = "happy" if t > t_q else "question"
    robot(cv, 442, 262, t, face=face, scale=2)
    if t > t_gen + 0.5:
        bulb(cv, 442, 172 - int(abs(math.sin(t * 3)) * 2), t, prog(t, t_gen + 0.5, t_gen + 0.8))
    return vignette(cv, 0.3)


TOWER = []  # (fila, col, x, y)
for _r in range(7):
    _n = 7 - _r
    for _c in range(_n):
        TOWER.append((_r, _c, 172 - _n * 21 + _c * 42 + 1, 218 - _r * 15))
_trng = np.random.default_rng(21)
TOWER_FALL = [(_trng.uniform(-60, 60), _trng.uniform(-80, -10), _trng.uniform(-9, 9), 232 + int(_trng.integers(0, 4)) * 4)
              for _ in TOWER]


def sc_fragile(t):
    """Pero las reglas son frágiles... Mantenerlas cuesta más de lo que valen."""
    cv = bg("bg_corporate_1985").copy()
    cv = grade(cv, mul=(0.45, 0.5, 0.65), add=(4, 4, 14), sat=0.6)
    t_reg = WD("c4_04", "reglas")
    t_frag = WD("c4_04", "fragiles")
    t_fun = WD("c4_04", "funcionan")
    t_esc = WD("c4_04", "escritas")
    t_fall = WD("c4_04", "fallan")
    t_dem = WD("c4_04", "demas")
    t_man = WD("c4_04", "Mantenerlas")
    t_cue = WD("c4_04", "cuesta")
    t_val = WD("c4_04", "valen")
    t_col = t_dem + 0.1
    d = ImageDraw.Draw(cv)
    # torre de reglas
    wob = prog(t, t_fall, t_col) * 3.0
    for k, (r, c, x, y) in enumerate(TOWER):
        if t < t_col:
            dx = int(math.sin(t * 24 + r * 0.7) * wob * (r + 1) / 3)
            d.rectangle([x + dx, y, x + dx + 39, y + 12], fill=(*PAPER, 255), outline=(*INK, 255))
            d.rectangle([x + dx + 1, y + 1, x + dx + 2, y + 11], fill=(200, 70, 60, 255))
            d.line([(x + dx + 5, y + 4), (x + dx + 30, y + 4)], fill=(150, 140, 130, 255))
            d.line([(x + dx + 5, y + 8), (x + dx + 22, y + 8)], fill=(80, 120, 180, 255))
        else:
            vx, vy, spin, floor = TOWER_FALL[k]
            dt = t - t_col - r * 0.03
            dt = max(0.0, dt)
            cx0, cy0 = x + 20, y + 6
            yy = cy0 + vy * dt + 0.5 * 700 * dt * dt
            tland = None
            if yy >= floor:
                # tiempo de aterrizaje
                A_, B_, C_ = 350, vy, cy0 - floor
                disc = max(0.0, B_ * B_ - 4 * A_ * C_)
                tland = (-B_ + math.sqrt(disc)) / (2 * A_)
                yy = floor
            dte = tland if tland is not None else dt
            xx = cx0 + vx * dte
            ang = spin * dte * 0.4 + (0.0 if tland is None else 0.0)
            if tland is not None:
                ang = (0.12 if k % 2 else -0.1) + ((k % 3) - 1) * 0.18
            poly_rot(d, xx, yy, 40, 12, ang, (*PAPER, 255), (*INK, 255))
    # título
    if t > t_reg - 0.1:
        a, dy = pop(t, t_reg - 0.1)
        window(cv, 44, 8 + dy, 392, 30)
        draw_text(cv, "LAS REGLAS SON", 56, 16 + dy, "press", 16, CREAM)
        if t > t_frag:
            sx, sy = shake(t, t_frag + 0.05, 0.3, 2)
            draw_text(cv, "FRÁGILES", 296 + sx, 16 + dy + sy, "press", 16, gradient=ICE_RAMP)
    # casos
    def case_card(txt, y, t_in, t_res, ok):
        p = ease_out(prog(t, t_in, t_in + 0.4))
        if p <= 0 or t > t_man - 0.2:
            return
        x0 = int(-260 + p * 300)
        tw, _ = text_size(txt, "press", 8)
        window(cv, x0, y, tw + 20, 22)
        draw_text(cv, txt, x0 + 10, y + 7, "press", 8, CREAM)
        if t > t_res:
            dd = ImageDraw.Draw(cv)
            if ok:
                check(dd, x0 + tw + 28, y + 3, GREEN, 3)
            else:
                cross_mark(dd, x0 + tw + 28, y + 3, RED, 3)
    case_card("CASO: FIEBRE Y TOS", 48, t_fun - 0.1, t_esc, True)
    case_card("CASO: ¿TOS, VIAJE Y SARPULLIDO?", 76, t_esc + 0.3, t_fall + 0.1, False)
    if t_fall + 0.1 < t < t_man - 0.2:
        a, dy = pop(t, t_fall + 0.1)
        draw_text(cv, "¡NO HAY REGLA!", 172, 106 + dy, "press", 8, (255, 120, 90), align="center")
    # costo vs valor
    if t > t_man - 0.1:
        a, dy = pop(t, t_man - 0.1)
        x0, y0 = 24, 48 + dy
        window(cv, x0, y0, 296, 74)
        dd = ImageDraw.Draw(cv)
        draw_text(cv, "VALOR", x0 + 10, y0 + 14, "press", 8, CREAM)
        draw_text(cv, "COSTO", x0 + 10, y0 + 40, "press", 8, CREAM)
        vl = 120
        dd.rectangle([x0 + 66, y0 + 10, x0 + 66 + vl, y0 + 24], fill=(*GREEN, 255), outline=(*INK, 255))
        cl = int(30 + 186 * ease_in_out(prog(t, t_cue, t_val + 0.2)))
        over = cl > vl
        col = RED if not over or int(t * 8) % 2 else (255, 150, 120)
        dd.rectangle([x0 + 66, y0 + 36, x0 + 66 + cl, y0 + 50], fill=(*col, 255), outline=(*INK, 255))
        dd.line([(x0 + 66 + vl, y0 + 6), (x0 + 66 + vl, y0 + 56)], fill=(*GOLD, 255))
        if t > t_val:
            draw_text(cv, "COSTO > VALOR", x0 + 148, y0 + 60, "press", 8, (255, 120, 90), align="center")
    # ingeniero
    if t < t_fun:
        arms, mood = "down", "neutral"
    elif t < t_fall:
        arms, mood = "point_l", "happy"
    elif t < t_col:
        arms, mood = "shrug", "worried"
    elif t < t_man:
        arms, mood = "cheer", "worried"
    else:
        arms, mood = "think", "worried"
    jit = 2 * int(math.sin(t * 40) > 0.4) if t_col < t < t_man else 0
    char(cv, "kengineer", 404 + jit, 266, t, scale=3, arms=arms, mood=mood, look=-1)
    if t_col < t < t_man + 0.3:
        a, dy = pop(t, t_col)
        draw_text(cv, "!!", 404, 96 + dy, "press", 16, (255, 120, 90), align="center")
    dx, dy = shake(t, t_col, 0.4, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


LISP_CABS = [(35, 80, 106, 210), (175, 80, 229, 210)]
LISP_PANELS = [(66, 84, 92, 140), (181, 84, 225, 144)]
MONITORS = [(35, 115, 50, 138), (120, 114, 151, 138), (240, 114, 271, 138)]


def chart_crash_value(u):
    if u < 0.84:
        return 0.25 + 0.6 * u + math.sin(u * 40) * 0.03
    return max(0.03, 0.75 - (u - 0.84) * 6)


def sc_crash(t):
    """1987: el mercado de las máquinas especializadas se derrumba. Segundo invierno."""
    cv = bg("bg_corporate_1985").copy()
    t0 = TL.s("c4_05")
    t_merc = WD("c4_05", "mercado")
    t_maq = WD("c4_05", "maquinas")
    t_der = WD("c4_05", "derrumba")
    t_seg = WD("c4_05", "segundo")
    t_inv = WD("c4_05", "invierno")
    t_off0 = t_der - 1.25
    # LEDs de las máquinas Lisp y apagado uno por uno
    order = [("mon", 0), ("cab", 0), ("mon", 1), ("cab", 1), ("mon", 2)]
    d = ImageDraw.Draw(cv)
    for kind, i in order:
        pass
    offs = {}
    for k, key in enumerate(order):
        offs[key] = t_off0 + k * 0.25
    for i, (x0, y0, x1, y1) in enumerate(LISP_PANELS):
        if t < offs[("cab", i)]:
            for j in range(18):
                lx = x0 + 3 + (j % 6) * ((x1 - x0 - 6) // 6)
                ly = y0 + 6 + (j // 6) * 16
                on = (int(t * 6) + j * 7 + i) % 5 != 0
                c = [(90, 250, 140), (255, 190, 70), (255, 90, 70)][(j + i) % 3]
                d.rectangle([lx, ly, lx + 1, ly + 1], fill=(*(c if on else shade(c, 0.3)), 255))
    for i, box in enumerate(LISP_CABS):
        k = prog(t, offs[("cab", i)], offs[("cab", i)] + 0.12)
        cv = darken(cv, box, 0.55 * k)
    for i, (x0, y0, x1, y1) in enumerate(MONITORS):
        to = offs[("mon", i)]
        if t >= to:
            cv = darken(cv, (x0, y0, x1, y1), 0.9, (8, 14, 10))
            if t < to + 0.15:
                p = (t - to) / 0.15
                cxm, cym = (x0 + x1) // 2, (y0 + y1) // 2
                hw = int((x1 - x0) / 2 * (1 - p))
                ImageDraw.Draw(cv).line([(cxm - hw, cym), (cxm + hw, cym)], fill=(230, 255, 240, 255))
    # etiquetas
    if t < t_der + 0.4:
        tag(cv, "MÁQUINA LISP", 70, 64, t, t_maq)
        tag(cv, "MÁQUINA LISP", 202, 64, t, t_maq + 0.15)
    # gráfico del mercado
    if t > t_merc - 0.1:
        a, dy = pop(t, t_merc - 0.1)
        x0, y0 = 336, 62 + dy
        window(cv, x0, y0, 136, 82)
        draw_text(cv, "MERCADO", x0 + 10, y0 + 8, "press", 8, CREAM)
        dd = ImageDraw.Draw(cv)
        px0, py0, px1, py1 = x0 + 10, y0 + 22, x0 + 126, y0 + 74
        dd.line([(px0, py1), (px1, py1)], fill=(*GREY, 255))
        dd.line([(px0, py0), (px0, py1)], fill=(*GREY, 255))
        umax = prog(t, t_merc, t_der + 0.45)
        pts = []
        for i in range(int(40 * umax) + 1):
            u = i / 40
            pts.append((int(px0 + u * (px1 - px0)), int(py1 - chart_crash_value(u) * (py1 - py0))))
        if len(pts) > 1:
            split = [p for p in pts if p[0] <= px0 + 0.84 * (px1 - px0)]
            rest = pts[len(split) - 1:] if split else pts
            dd.line(pts, fill=(*INK, 255), width=4)
            if len(split) > 1:
                dd.line(split, fill=(*GREEN, 255), width=2)
            if len(rest) > 1 and umax > 0.84:
                dd.line(rest, fill=(*RED, 255), width=2)
                ex, ey = rest[-1]
                dd.polygon([(ex - 4, ey - 2), (ex + 4, ey - 2), (ex, ey + 5)], fill=(*RED, 255), outline=(*INK, 255))
    # ingeniero
    if t < t_der:
        arms, mood, look = "down", "neutral", -1
    elif t < t_inv:
        arms, mood, look = "shrug", "worried", 0
    else:
        arms, mood, look = "cross", "worried", 0
    jit = 2 * int(math.sin(t * 40) > 0.5) if t > t_inv + 0.4 else 0
    char(cv, "kengineer", 290 + jit, 266, t, scale=3, arms=arms, mood=mood, look=look)
    # invierno
    wk = ease_in_out(prog(t, t_seg - 0.2, t_inv + 0.8))
    if wk > 0:
        cv = grade(cv, mul=(0.72, 0.82, 1.08), add=(22, 32, 54), sat=0.3, k=wk)
        SNOW.draw(cv, t, density=wk)
        acc = ease_in_out(prog(t, t_inv, t_inv + 1.6))
        if acc > 0:
            cv = snow_floor(cv, int(H - acc * 16))
    # textos superiores
    if t < t_der - 0.1:
        a_out = 1 - prog(t, t_der - 0.4, t_der - 0.1)
        p = prog(t, t0, t0 + 0.55)
        yy = 8 - (1 - ease_out_back(p, 2.2)) * 50
        draw_text(cv, "1987", 240, int(yy), "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2,
                  alpha=min(p * 3, a_out))
    elif t < t_seg - 0.1:
        a, dy = pop(t, t_der)
        window(cv, 68, 10 + dy, 344, 32, fill=(120, 24, 30), border=(255, 140, 120))
        draw_text(cv, "COLAPSA EL MERCADO", 240, 18 + dy, "press", 16, CREAM, align="center")
    else:
        a, dy = pop(t, t_seg - 0.1)
        window(cv, 80, 10 + dy, 320, 32, fill=(10, 16, 36), border=(160, 210, 240))
        draw_text(cv, "SEGUNDO INVIERNO", 240, 18 + dy, "press", 16, align="center", gradient=ICE_RAMP, outline_w=2,
                  reveal=(t - t_seg + 0.1) * 45)
    dx, dy = shake(t, t_der, 0.45, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


def skyline(cv, base, col, seed=5):
    d = ImageDraw.Draw(cv)
    rnd = np.random.default_rng(seed)
    x = 0
    while x < W:
        bw = int(rnd.integers(18, 40))
        bh = int(rnd.integers(30, 90))
        d.rectangle([x, base - bh, x + bw, base], fill=(*col, 255))
        x += bw + int(rnd.integers(0, 6))


COLD_NET = net_layers([372, 404, 436], [3, 4, 2], 200, 13)


def sc_cold(t):
    """Sin embargo, en medio del frío, pasa algo que casi nadie celebra."""
    cv = vgradient((6, 8, 22), (30, 44, 74), 12)
    STARS.draw(cv, t * 0.4, alpha=0.4)
    skyline(cv, 222, (18, 24, 44))
    d = ImageDraw.Draw(cv)
    # ventanas apagadas en los edificios
    t_pasa = WD("c4_06", "pasa")
    t_algo = WD("c4_06", "algo")
    t_nad = WD("c4_06", "nadie")
    cv = snow_floor(cv, 222, 0.7)
    SNOW.draw(cv, t, density=1.0)
    robot(cv, 170, 252, t, face="off", frozen=True, scale=3)
    draw_text(cv, "1987 – 1993", 16, 14, "press", 8, (190, 220, 245))
    # la red que sigue brillando
    g = 0.25 + 0.15 * math.sin(t * 3)
    g = g + (1 - g) * ease_out(prog(t, t_pasa, t_algo + 0.4))
    cv = glow_disc(cv, 404, 200, 64, g)
    draw_net(cv, COLD_NET, glow=g, r=3)
    if t > t_pasa:
        s = ((t - t_pasa) * 2.2) % 2.6
        net_pulses(cv, COLD_NET, s, (255, 240, 160))
        for i in range(4):
            sparkle(cv, 380 + i * 18, 176 + (i % 2) * 44, t + i * 0.8, 2, CYAN)
    if t > t_algo + 0.3:
        draw_text(cv, "ALGO SE MUEVE...", 404, 156, "press", 8, CYAN, align="center",
                  reveal=(t - t_algo - 0.3) * 22)
    if t > t_nad + 0.2:
        a = prog(t, t_nad + 0.2, t_nad + 0.5)
        draw_text(cv, "CASI NADIE LO NOTA", 404, 244, "press", 8, (170, 200, 230), align="center", alpha=a)
    return vignette(cv, 0.45)


UCSD_NET = [[(314, 73), (314, 95), (314, 117)],
            [(361, 62), (361, 85), (361, 108), (361, 131)],
            [(406, 80), (406, 108)]]


def nature_cover(cv, x, y):
    w, h = 104, 104
    draw_paper(cv, x, y, w, h, (248, 246, 240))
    d = ImageDraw.Draw(cv)
    d.rectangle([x + 1, y + 1, x + w - 1, y + 20], fill=(196, 30, 40, 255))
    draw_text(cv, "NATURE", x + w // 2, y + 6, "press", 8, CREAM, align="center", outline=None, shadow=False)
    draw_text(cv, "VOL 323 · 1986", x + w // 2, y + 23, "silk", 8, (120, 110, 100), align="center",
              outline=None, shadow=False)
    # mini red
    L = net_layers([x + 28, x + 52, x + 76], [3, 4, 2], y + 50, 7)
    for la, lb in zip(L, L[1:]):
        for p in la:
            for q in lb:
                d.line([p, q], fill=(150, 150, 170, 255))
    for la in L:
        for (px, py) in la:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(40, 120, 200, 255), outline=(*INK, 255))
    for i, ln in enumerate(["LEARNING BY", "BACK-PROPAGATING", "ERRORS"]):
        draw_text(cv, ln, x + w // 2, y + 70 + i * 10, "silk", 8, INK, align="center", outline=None, shadow=False)


def sc_backprop(t):
    """1986: Rumelhart, Hinton y Williams publican en Nature... la retropropagación."""
    cv = bg("bg_ucsd_office_1986").copy()
    t0 = TL.s("c4_07")
    names = ["Rumelhart", "Hinton", "Williams"]
    t_names = [WD("c4_07", "David"), WD("c4_07", "Geoffrey"), WD("c4_07", "Ronald")]
    t_nat = WD("c4_07", "Nature")
    t_red = WD("c4_07", "redes")
    t_cap = WD("c4_07", "capas")
    t_ret = WD("c4_07", "retropropagacion")
    keys = ["rumelhart", "hinton86", "williams"]
    portraits = ["david_rumelhart", "geoffrey_hinton_1986", "ronald_williams"]
    first = ["DAVID", "GEOFFREY", "RONALD"]
    last = ["RUMELHART", "HINTON", "WILLIAMS"]
    xs = [74, 154, 234]
    # red del pizarrón
    if t > t_red - 0.2:
        g = prog(t, t_red - 0.2, t_red + 0.3)
        if t < t_ret:
            s = ((t - t_red) * 2.4) % 2.5
            draw_net(cv, UCSD_NET, glow=g, edge=(120, 100, 60), node=(255, 214, 110), r=5)
            net_pulses(cv, UCSD_NET, s, (230, 160, 40), size=1)
        else:
            s = ((t - t_ret - 0.3) * 2.4) % 2.5
            p_back = s if t > t_ret + 0.3 else -1

            def ng(li, ni):
                return 1.0 if (t > t_ret + 0.3 and abs((2 - li) - s) < 0.35) else 0.45
            draw_net(cv, UCSD_NET, glow=1.0, edge=(40, 120, 150), node=(90, 220, 255), r=5, node_glow=ng)
            if p_back >= 0:
                net_pulses(cv, UCSD_NET, s, (90, 230, 255), backward=True, size=1)
            # error en la salida
            for (ox, oy) in UCSD_NET[2]:
                if int(t * 6) % 2:
                    ImageDraw.Draw(cv).ellipse([ox - 7, oy - 7, ox + 7, oy + 7], outline=(255, 80, 70, 255))
            draw_text(cv, "ERROR", 438, 90, "press", 8, (255, 100, 80), align="center")
    if t > t_cap:
        a, dy = pop(t, t_cap)
        tag(cv, "VARIAS CAPAS", 360, 158, t, t_cap)
    # personajes (aparecen con un salto al decir su nombre)
    for i, k in enumerate(keys):
        tn = t_names[i]
        if t < tn - 0.15:
            continue
        a, dy = pop(t, tn - 0.15, 0.4)
        arms, mood = "down", "neutral"
        if tn < t < tn + 0.9:
            arms, mood = "wave", "happy"
        if t > t_nat + 0.2:
            arms, mood = ("hold" if i != 1 else "down"), "happy"
        if t > t_ret:
            arms, mood = ("point" if i == 1 else "cheer"), "happy"
        char(cv, k, xs[i], 266 + dy, t, alpha=a, arms=arms, mood=mood, scale=3, look=1 if t > t_red else 0)
        if t < tn + 0.5:
            for j in range(3):
                sparkle(cv, xs[i] - 30 + j * 30, 130 + (j % 2) * 40, t + j, 3, GOLD)
    # tarjetas con retrato
    up = int(ease_in_out(prog(t, t_nat - 0.3, t_nat + 0.2)) * -150)
    for i in range(3):
        tn = t_names[i]
        if t > tn - 0.1 and up > -149:
            a, dy = pop(t, tn - 0.1, 0.4)
            cx = xs[i] - 32
            portrait_card(cv, portraits[i], cx, 10 + dy + up)
            window(cv, cx - 7, 80 + dy + up, 78, 26)
            draw_text(cv, first[i], cx + 32, 84 + dy + up, "silk", 8, GREY, align="center")
            draw_text(cv, last[i], cx + 32, 95 + dy + up, "press", 8, CREAM, align="center")
    # año
    if t < t_nat:
        a_out = 1 - prog(t, t_nat - 0.4, t_nat)
        p = prog(t, t0, t0 + 0.55)
        yy = 2 - (1 - ease_out_back(p, 2.2)) * 50
        draw_text(cv, "1986", 372, int(yy), "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2,
                  alpha=min(p * 3, a_out))
    # portada de Nature
    if t > t_nat - 0.1:
        p = prog(t, t_nat - 0.1, t_nat + 0.35)
        yy = int(6 - (1 - ease_out_back(p, 1.6)) * 130)
        nature_cover(cv, 98, yy)
    # título
    if t > t_ret - 0.1:
        a, dy = pop(t, t_ret - 0.1)
        window(cv, 206, 4 + dy, 272, 30)
        draw_text(cv, "RETROPROPAGACIÓN", 342, 12 + dy, "press", 16, align="center", gradient=CYAN_RAMP,
                  reveal=(t - t_ret + 0.1) * 26)
    return vignette(cv, 0.35)


def heartbeat(ph):
    """Forma del latido (fase 0..1) -> desplazamiento vertical (positivo = arriba)."""
    if 0.10 < ph < 0.16:
        return 3 * math.sin((ph - 0.10) / 0.06 * math.pi)
    if 0.22 < ph < 0.25:
        return -5 * (ph - 0.22) / 0.03
    if 0.25 <= ph < 0.29:
        return -5 + 33 * (ph - 0.25) / 0.04
    if 0.29 <= ph < 0.33:
        return 28 - 38 * (ph - 0.29) / 0.04
    if 0.33 <= ph < 0.36:
        return -10 + 10 * (ph - 0.33) / 0.03
    if 0.48 < ph < 0.60:
        return 6 * math.sin((ph - 0.48) / 0.12 * math.pi)
    return 0.0


PULSE_NET = net_layers([300, 330, 360], [3, 4, 2], 128, 12)


def sc_pulse(t):
    """La idea que Minsky había enterrado tenía, otra vez, pulso."""
    cv = vgradient((6, 8, 22), (26, 34, 64), 12)
    STARS.draw(cv, t * 0.4, alpha=0.5)
    t_min = WD("c4_08", "Minsky")
    t_ent = WD("c4_08", "enterrado")
    t_ten = WD("c4_08", "tenia")
    t_pul = WD("c4_08", "pulso")
    t_beat = t_ten
    warm = ease_out(prog(t, t_pul, t_pul + 0.6))
    if warm > 0:
        cv = grade(cv, mul=(1.0, 1.0, 1.0), add=(14, 8, 2), k=warm)
    cv = snow_floor(cv, 226, 1.3)
    SNOW.draw(cv, t, density=1.0 - 0.7 * warm)
    d = ImageDraw.Draw(cv)
    # lápida
    gx, gy = 112, 150
    d.rectangle([gx - 40, gy, gx + 40, 234], fill=(110, 112, 126, 255), outline=(*INK, 255))
    d.pieslice([gx - 40, gy - 34, gx + 40, gy + 34], 180, 360, fill=(110, 112, 126, 255), outline=(*INK, 255))
    d.line([(gx - 39, gy), (gx + 39, gy)], fill=(110, 112, 126, 255))
    d.line([(gx + 36, gy - 10), (gx + 36, 232)], fill=(80, 82, 96, 255))
    draw_text(cv, "R.I.P.", gx, gy - 16, "press", 8, (40, 40, 52), align="center", outline=None, shadow=False)
    draw_text(cv, "REDES", gx, gy + 4, "press", 8, (40, 40, 52), align="center", outline=None, shadow=False)
    draw_text(cv, "NEURONALES", gx, gy + 16, "silkb", 8, (40, 40, 52), align="center", outline=None, shadow=False)
    draw_text(cv, "1969", gx, gy + 30, "press", 8, (40, 40, 52), align="center", outline=None, shadow=False)
    d.rectangle([gx - 44, 222, gx + 44, 232], fill=(230, 238, 250, 255))
    if t > t_ent:
        a = prog(t, t_ent, t_ent + 0.3)
        draw_text(cv, "ENTERRADA POR MINSKY", gx, 240, "silk", 8, (190, 210, 235), align="center", alpha=a)
    if t > t_pul:
        # grieta y luz
        crack = [(gx - 6, gy - 30), (gx + 2, gy - 14), (gx - 4, gy), (gx + 4, gy + 20), (gx - 2, gy + 44)]
        k = int(len(crack) * prog(t, t_pul, t_pul + 0.3))
        if k > 1:
            d.line(crack[:k], fill=(120, 240, 255, 255), width=2)
    # monitor ECG
    x0, y0, ww, hh = 172, 24, 288, 70
    window(cv, x0, y0, ww, hh, fill=(8, 20, 14), border=(120, 140, 130))
    d = ImageDraw.Draw(cv)
    sx0, sx1, base = x0 + 8, x0 + ww - 10, y0 + 46
    for gx_ in range(sx0, sx1, 12):
        d.line([(gx_, y0 + 6), (gx_, y0 + hh - 6)], fill=(16, 44, 30, 255))
    v = 140.0
    span = sx1 - sx0
    pen = sx0 + ((t * v) % span)
    pts = []
    beat_on = t > t_beat
    col = (90, 255, 140) if beat_on else (70, 170, 110)
    for x in range(sx0, sx1):
        back = (pen - x) % span
        if back < 6:
            if pts:
                d.line(pts, fill=(*col, 255)) if len(pts) > 1 else None
            pts = []
            continue
        tau = t - back / v
        yv = 0.0
        if tau > t_beat:
            per = 0.62 if tau > t_pul else 0.8
            ref = t_beat if tau <= t_pul else t_pul
            yv = heartbeat(((tau - ref) / per) % 1.0) * (0.6 if tau <= t_pul else 1.0)
        pts.append((x, int(base - yv)))
    if len(pts) > 1:
        d.line(pts, fill=(*col, 255))
    d.rectangle([int(pen) - 1, base - 1, int(pen) + 1, base + 1], fill=(220, 255, 230, 255))
    draw_text(cv, "PULSO", x0 + 10, y0 + 8, "press", 8, col)
    bpm = "---" if not beat_on else ("72" if t < t_pul else "96")
    draw_text(cv, bpm, x0 + ww - 12, y0 + 8, "press", 8, col, align="right")
    # red y robot
    g = 0.2 + 0.8 * ease_out(prog(t, t_ten, t_pul + 0.3))
    if t > t_pul:
        g = 0.75 + 0.25 * abs(math.sin((t - t_pul) / 0.62 * math.pi))
    draw_net(cv, PULSE_NET, glow=g, r=3)
    if t > t_ten:
        net_pulses(cv, PULSE_NET, ((t - t_ten) * 2.5) % 2.6, (255, 240, 160))
    frozen = t < t_pul
    face = "off" if t < t_ten else ("sad" if t < t_pul else "heart")
    hop = int(abs(math.sin((t - t_pul) * 6)) * 8) if t > t_pul + 0.2 else 0
    robot(cv, 400, 252 - hop, t, face=face, frozen=frozen, scale=3)
    if t_pul <= t < t_pul + 0.5:
        # esquirlas de hielo
        p = (t - t_pul) / 0.5
        dd = ImageDraw.Draw(cv)
        for i in range(14):
            ang = i / 14 * 2 * math.pi
            rr = 20 + p * 60
            px_, py_ = 400 + math.cos(ang) * rr, 190 + math.sin(ang) * rr * 0.8 + p * p * 30
            dd.rectangle([int(px_), int(py_), int(px_) + 2, int(py_) + 2], fill=(220, 240, 255, 255))
    if t > t_pul + 0.1:
        for i in range(5):
            sparkle(cv, 300 + i * 40, 110 + (i % 2) * 40, t + i * 0.6, 3, GOLD)
    return vignette(cv, 0.4)


# =========================================================================== montaje

def scenes():
    c4s = TL.chapter_start(4)
    return [
        (c4s - 0.3, make_card(4, ["REGLAS, EXPERTOS Y", "EL SEGUNDO INVIERNO"], "1980 – 1993", snow=True), None),
        (TL.s("c4_01") - 0.2, sc_experts,
         lambda t: (cam_push(t, WD("c4_02", "miles"), TL.e("c4_02"), 1.0, 1.08, (240, 135), (200, 125))[0]
                    + cam_punch(t, [WD("c4_01", "sistemas")], 0.06),
                    *cam_push(t, WD("c4_02", "miles"), TL.e("c4_02"), 1.0, 1.08, (240, 135), (200, 125))[1:])),
        (TL.s("c4_03") - 0.15, sc_boom,
         lambda t: (1.0 + cam_punch(t, [TL.s("c4_03"), WD("c4_03", "configuran"), WD("c4_03", "fortunas")], 0.05),
                    240, 135)),
        (WD("c4_03", "Japon") - 0.35, sc_japan,
         lambda t: (cam_push(t, WD("c4_03", "Japon"), TL.e("c4_03"), 1.0, 1.1, (240, 120))[0]
                    + cam_punch(t, [WD("c4_03", "Quinta")], 0.08), 240, 125)),
        (TL.s("c4_04") - 0.15, sc_fragile,
         lambda t: (1.0 + cam_punch(t, [WD("c4_04", "demas") + 0.1], 0.1)
                    + cam_punch(t, [WD("c4_04", "valen")], 0.05), 220, 150)),
        (TL.s("c4_05") - 0.15, sc_crash,
         lambda t: (1.0 + cam_punch(t, [WD("c4_05", "derrumba")], 0.1), 240, 135)),
        (TL.s("c4_06") - 0.15, sc_cold,
         lambda t: cam_push(t, WD("c4_06", "frio"), TL.e("c4_06") + 0.1, 1.0, 1.3, (240, 135), (380, 180))),
        (TL.s("c4_07") - 0.15, sc_backprop,
         lambda t: cam_push(t, WD("c4_07", "redes") - 0.3, TL.e("c4_07"), 1.0, 1.18, (240, 135), (350, 110))),
        (TL.s("c4_08") - 0.15, sc_pulse,
         lambda t: (1.0 + cam_punch(t, [WD("c4_08", "pulso")], 0.1), 240, 135)),
    ]


# =========================================================================== audio

def music(A):
    s, e = TL.s, TL.e
    t_start = TL.chapter_start(4) + 1.6
    t_end = chapter_end(4)
    C = [("C", "maj"), ("A", "min"), ("F", "maj"), ("G", "maj")]
    A.section(t_start, s("c4_03") - 0.15, 120, C, A.st_bright)
    A.section(s("c4_03") - 0.15, WD("c4_03", "Japon") - 0.35, 124, [("F", "maj"), ("G", "maj"), ("C", "maj"), ("A", "min")],
              A.st_triumph)
    # Japón: pentatónica
    tj = WD("c4_03", "Japon") - 0.35
    A.section(tj, s("c4_04") - 0.15, 124, [("D", "min"), ("A", "min")], A.st_bright)
    A.sting(WD("c4_03", "Quinta"), [69, 72, 74, 76, 81], vol=0.045, step=0.08, hold=0.9)
    # frágiles: inestable
    tf = s("c4_04") - 0.15
    A.section(tf, WD("c4_04", "demas") + 0.1, 112, [("A", "min"), ("D", "min"), ("E", "maj"), ("A", "min")], A.st_puzzle)
    A.kick(A.music, WD("c4_04", "demas") + 0.1, 0.5)
    A.section(WD("c4_04", "demas") + 0.4, s("c4_05") - 0.15, 100, [("D", "min"), ("E", "maj")], A.st_puzzle)
    # 1987: brillo corporativo que se corta
    tc = s("c4_05") - 0.15
    A.section(tc, WD("c4_05", "derrumba"), 120, [("C", "maj"), ("G", "maj")], A.st_bright)
    td = WD("c4_05", "derrumba")
    A.kick(A.music, td, 0.5)
    A.crash(A.music, td, 0.12)
    n = int(1.4 * A.SR)
    tt = np.arange(n) / A.SR
    f = 660 * np.exp(-tt * 2.0)
    ph = np.cumsum(f) / A.SR
    A.music.add(td + 0.05, np.where((ph % 1) < 0.5, 1.0, -1.0) * np.exp(-tt * 1.6), 0.045)
    A.section(td + 0.8, s("c4_07") - 0.15, 70, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "min")], A.st_winter)
    # 1986: esperanza (retropropagación)
    tb = s("c4_07") - 0.15
    A.section(tb, WD("c4_07", "retropropagacion"), 96, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")],
              A.st_build)
    tr = WD("c4_07", "retropropagacion")
    A.section(tr, s("c4_08") - 0.15, 104, [("F", "maj"), ("G", "maj")], A.st_build)
    A.sting(tr, [64, 67, 72, 76], vol=0.04, step=0.1, hold=1.0)
    # pulso
    A.section(s("c4_08") - 0.15, WD("c4_08", "pulso"), 80, [("A", "min"), ("F", "maj")], A.st_mystery)
    tp = WD("c4_08", "pulso")
    A.section(tp, t_end, 104, [("C", "maj"), ("G", "maj")], A.st_build)
    A.sting(tp, [72, 76, 79, 84], vol=0.05, step=0.09, hold=1.0)


def sfx(A):
    s, e = TL.s, TL.e
    # expertos
    A.whoosh(s("c4_01") - 0.1, 0.3)
    A.text_blips(WD("c4_01", "sistemas") - 0.1, 21, 30)
    A.join_jingle(WD("c4_01", "expertos"))
    for k in range(4):
        sig = A.noise(0.03, 3) * np.exp(-np.arange(int(0.03 * A.SR)) / A.SR * 120)
        A.sfx.add(WD("c4_01", "vuelve") - 0.6 + k * 0.33, sig, 0.03)
    for i in range(len(RULES)):
        A.pop_sfx(WD("c4_02", "siguen") + i * 0.3, 500 + i * 70, 0.06)
    tm = WD("c4_02", "miles")
    for i in range(22):
        A.blip(tm + i * 0.13, 900 + (i % 5) * 120, 0.02, 0.025)
    A.typewriter(WD("c4_02", "escritas"), e("c4_02") + 0.2, 13, 0.03)
    # boom
    A.pop_sfx(s("c4_03") - 0.1, 520)
    A.pop_sfx(WD("c4_03", "configuran") - 0.1, 600)
    A.coin(WD("c4_03", "infecciones") + 0.3, 0.05)
    A.coin(WD("c4_03", "computadoras") + 0.4, 0.05)
    A.pop_sfx(WD("c4_03", "empresas") - 0.1, 450)
    ti = WD("c4_03", "invierten")
    for i in range(9):
        A.coin(ti + i * 0.17, 0.04)
    # Japón
    A.whoosh(WD("c4_03", "Japon") - 0.3, 0.35)
    A.pop_sfx(WD("c4_03", "Quinta"), 700, 0.07)
    A.robot_beep(WD("c4_03", "Generacion") + 0.5, 0.035)
    # frágiles
    A.text_blips(WD("c4_04", "reglas") - 0.1, 14, 26)
    A.freeze(WD("c4_04", "fragiles"), 0.05)
    A.whoosh(WD("c4_04", "funcionan") - 0.1, 0.3, 0.04)
    A.coin(WD("c4_04", "escritas"), 0.05)
    A.whoosh(WD("c4_04", "escritas") + 0.3, 0.3, 0.04)
    for i in range(3):
        A.blip(WD("c4_04", "fallan") + 0.1 + i * 0.12, 220, 0.08, 0.05, 0.5)
    tcol = WD("c4_04", "demas") + 0.1
    A.whoosh(tcol - 0.1, 0.6, 0.08)
    A.kick(A.sfx, tcol, 0.4)
    for i in range(8):
        A.pop_sfx(tcol + 0.25 + i * 0.05, 300 + (i % 3) * 80, 0.03)
    A.pop_sfx(WD("c4_04", "Mantenerlas") - 0.1, 500)
    for i in range(6):
        A.blip(WD("c4_04", "cuesta") + i * 0.18, 400 + i * 60, 0.05, 0.03, 0.25)
    for i in range(3):
        A.blip(WD("c4_04", "valen") + i * 0.12, 1400, 0.05, 0.035)
    # 1987
    A.whoosh(s("c4_05") - 0.1, 0.35)
    A.pop_sfx(WD("c4_05", "mercado") - 0.1, 500)
    A.pop_sfx(WD("c4_05", "maquinas"), 650, 0.05)
    A.pop_sfx(WD("c4_05", "maquinas") + 0.15, 700, 0.05)
    t_off0 = WD("c4_05", "derrumba") - 1.25
    for k in range(5):
        A.blip(t_off0 + k * 0.25, 180 - k * 15, 0.06, 0.06, 0.5)
    A.whoosh(WD("c4_05", "derrumba") - 0.1, 0.5, 0.08)
    A.kick(A.sfx, WD("c4_05", "derrumba"), 0.45)
    A.freeze(WD("c4_05", "invierno"))
    A.wind(WD("c4_05", "segundo") - 0.3, s("c4_07") - 0.1)
    # frío: la red que brilla
    for i in range(4):
        A.blip(WD("c4_06", "pasa") + i * 0.45, 1600 + i * 200, 0.04, 0.025, 0.125)
    A.text_blips(WD("c4_06", "algo") + 0.3, 16, 22, 0.015, 1700)
    # 1986
    A.whoosh(s("c4_07") - 0.1, 0.35)
    for n in ("David", "Geoffrey", "Ronald"):
        A.join_jingle(WD("c4_07", n) - 0.1)
    A.whoosh(WD("c4_07", "Nature") - 0.15, 0.3, 0.06)
    A.pop_sfx(WD("c4_07", "Nature") + 0.3, 380, 0.07)
    A.pop_sfx(WD("c4_07", "capas"), 620)
    A.text_blips(WD("c4_07", "retropropagacion") - 0.1, 16, 26)
    tr = WD("c4_07", "retropropagacion") + 0.3
    for i in range(6):
        A.blip(tr + i * 0.21, 1800 - i * 150, 0.03, 0.025, 0.25)
    # pulso
    t_ten = WD("c4_08", "tenia")
    t_pul = WD("c4_08", "pulso")
    tb = t_ten + 0.8 * 0.27
    while tb < t_pul:
        A.blip(tb, 1000, 0.06, 0.03)
        tb += 0.8
    tb = t_pul + 0.62 * 0.27
    while tb < chapter_end(4) - 0.3:
        A.blip(tb, 1000, 0.07, 0.035)
        A.kick(A.sfx, tb, 0.15)
        tb += 0.62
    A.freeze(t_pul, 0.05)
    A.robot_beep(t_pul + 0.35, 0.05)
