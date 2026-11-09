"""Capítulo 6: La jugada 37 (2016)."""
from common import *  # noqa
import numpy as np

CH = 6

# --------------------------------------------------------------------------- reparto local
REDMOND = dict(name="Comentarista 1", skin=S.SKIN["light"], hair=S.hexc("7a5434"), hair_style="side",
               top="suit", top_color=S.hexc("2a3046"), shirt=S.hexc("eef0f4"), tie=S.hexc("9a2a2a"),
               pants=S.hexc("22263a"))
GARLOCK = dict(name="Comentarista 2", skin=S.SKIN["fair"], hair=S.hexc("b0aca4"), hair_style="short",
               glasses="black", top="suit", top_color=S.hexc("4e4e58"), shirt=S.hexc("e8eaf0"),
               tie=S.hexc("2a4a7a"), pants=S.hexc("33333c"))

WOOD = (214, 164, 92)
WOOD_D = (186, 136, 70)
LINE = (70, 44, 22)
BLACK_ST = (26, 24, 32)
WHITE_ST = (238, 236, 226)


# --------------------------------------------------------------------------- utilidades
def pow10(cv, exp, cx, y, size=32, ramp=GOLD_RAMP, alpha=1.0, approx=True):
    """'~10' grande con exponente chico (~10^170)."""
    w0 = text_size("~", "press", size // 2)[0] + 4 if approx else 0
    w1, _ = text_size("10", "press", size)
    w2, _ = text_size(exp, "press", size // 2)
    x0 = cx - (w0 + w1 + 3 + w2) // 2
    if approx:
        draw_text(cv, "~", x0, y + size // 4, "press", size // 2, gradient=ramp, outline_w=1, alpha=alpha)
    x0 += w0
    draw_text(cv, "10", x0, y, "press", size, gradient=ramp, outline_w=2, alpha=alpha)
    draw_text(cv, exp, x0 + w1 + 3, y - size // 4, "press", size // 2, gradient=ramp, outline_w=1, alpha=alpha)


def stamp(cv, text, cx, cy, t, t0, color=(226, 58, 50), angle=8, size=16):
    """Sello rotado que cae con golpe."""
    if t < t0:
        return
    tw, th = text_size(text, "press", size)
    w, h = tw + 20, th + 18
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.rectangle([1, 1, w - 2, h - 2], outline=(*color, 255), width=2)
    d.rectangle([4, 4, w - 5, h - 5], outline=(*color, 255))
    draw_text(tmp, text, w // 2, 9, "press", size, color, align="center", outline=None, shadow=False)
    tmp = tmp.rotate(angle, Image.NEAREST, expand=True)
    p = prog(t, t0, t0 + 0.16)
    k = 2.2 - 1.2 * p
    if k > 1.01:
        tmp = tmp.resize((int(tmp.size[0] * k), int(tmp.size[1] * k)), Image.NEAREST)
    paste(cv, tmp, cx - tmp.size[0] // 2, cy - tmp.size[1] // 2, min(1.0, 0.4 + p))


def stone(cv, x, y, r, col, glow=None, alpha=255):
    d = ImageDraw.Draw(cv)
    x, y, r = int(x), int(y), max(1, int(r))
    if glow:
        gc, ga = glow
        for rr, aa in ((r + 5, 50), (r + 3, 90)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*gc, int(aa * ga)))
    d.ellipse([x - r + 1, y - r + 2, x + r + 1, y + r + 2], fill=(0, 0, 0, 90))
    if col == "b":
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*BLACK_ST, alpha), outline=(8, 8, 12, alpha))
        if r >= 3:
            d.point((x - r // 2, y - r // 2), fill=(110, 110, 130, alpha))
            d.point((x - r // 2 + 1, y - r // 2), fill=(70, 70, 86, alpha))
    else:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(*WHITE_ST, alpha), outline=(120, 116, 104, alpha))
        if r >= 3:
            d.arc([x - r + 1, y - r + 1, x + r - 1, y + r - 1], 20, 150, fill=(196, 192, 178, alpha))
            d.point((x - r // 2, y - r // 2), fill=(255, 255, 255, alpha))


# --- tablero visto desde arriba
B_BLACK = [(15, 3), (16, 5), (13, 2), (3, 15), (2, 13), (5, 16), (15, 15), (16, 13), (13, 16), (3, 3), (5, 2),
           (2, 5), (9, 3), (10, 15), (16, 8), (6, 9), (12, 12), (7, 14)]
B_WHITE = [(15, 10), (15, 12), (16, 11), (16, 3), (14, 3), (3, 2), (2, 3), (4, 4), (3, 14), (4, 15), (14, 15),
           (15, 16), (16, 16), (9, 15), (4, 9), (2, 9), (11, 3), (16, 6)]
M37 = (14, 9)  # quinta línea desde el borde derecho


def board_td(cv, x0, y0, cell, n=19):
    """Tablero 19x19 visto desde arriba. Devuelve función (i,j)->(x,y)."""
    d = ImageDraw.Draw(cv)
    g = cell * (n - 1)
    m = cell
    d.rectangle([x0 - m - 2, y0 - m + 2, x0 + g + m + 2, y0 + g + m + 6], fill=(60, 34, 16, 255))
    d.rectangle([x0 - m, y0 - m, x0 + g + m, y0 + g + m], fill=(*WOOD, 255), outline=(*INK, 255))
    for k in range(0, g + 2 * m, 7):
        yy = y0 - m + k
        d.line([(x0 - m + 1, yy), (x0 + g + m - 1, yy + 2)], fill=(*WOOD_D, 255))
    for i in range(n):
        d.line([(x0 + i * cell, y0), (x0 + i * cell, y0 + g)], fill=(*LINE, 255))
        d.line([(x0, y0 + i * cell), (x0 + g, y0 + i * cell)], fill=(*LINE, 255))
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            d.rectangle([x0 + i * cell - 1, y0 + j * cell - 1, x0 + i * cell + 1, y0 + j * cell + 1],
                        fill=(*LINE, 255))
    return lambda i, j: (x0 + i * cell, y0 + j * cell)


# --- tablero en perspectiva (infinito)
HZ = 96        # horizonte
FH = 1380.0    # foco * altura de cámara
FX = 70.0 * 7.8


def proj(X, Z):
    return 240 + X * FX / Z, HZ + FH / Z


def _h(i, j, s=0):
    v = (i * 73856093) ^ (j * 19349663) ^ (s * 83492791)
    return ((v * 2654435761) & 0xFFFFFFFF) / 0xFFFFFFFF


def infinite_board(cv, t, cam_z, density):
    """Plano de go infinito con piedras que aparecen. density 0..1."""
    a = np.array(cv)
    top = HZ + 2
    for y in range(top, H):
        Z = FH / (y - HZ)
        fog = clamp01((Z - 8) / 70)
        band = int(fog * 6) / 6
        c = np.array(WOOD) * (1 - band) + np.array((22, 18, 34)) * band
        a[y, :, :3] = c.astype(np.uint8)
    cv = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(cv)
    near, far = 7.6, 90.0
    z0 = math.ceil(near + cam_z)
    for zi in range(z0, int(far + cam_z)):
        Z = zi - cam_z
        if Z <= near:
            continue
        fog = clamp01((Z - 8) / 60)
        if fog >= 0.98:
            continue
        col = tuple(int(LINE[k] * (1 - fog) + 30 * fog) for k in range(3))
        y = int(HZ + FH / Z)
        d.line([(0, y), (W, y)], fill=(*col, 255))
    for xi in range(-60, 61):
        xa, ya = proj(xi, near)
        xb, yb = proj(xi, 40)
        d.line([(int(xa), int(ya)), (int(xb), int(yb))], fill=(*LINE, 255))
        xc, yc = proj(xi, 90)
        d.line([(int(xb), int(yb)), (int(xc), int(yc))], fill=(60, 40, 34, 255))
    # piedras (de atrás hacia adelante)
    for zi in range(int(far + cam_z), z0 - 1, -1):
        Z = zi - cam_z
        if Z <= near - 0.5 or Z > 30:
            continue
        for xi in range(-14, 15):
            hv = _h(xi, zi)
            if hv > density * 0.42:
                continue
            ta = hv / 0.42
            x, y = proj(xi, Z)
            if not (-10 < x < W + 10):
                continue
            rx = 0.42 * FX / Z
            ry = 0.5 * (FH / (Z - 0.42) - FH / (Z + 0.42))
            col = "b" if _h(xi, zi, 1) < 0.5 else "w"
            fill = BLACK_ST if col == "b" else WHITE_ST
            fog = clamp01((Z - 10) / 22)
            fill = tuple(int(fill[k] * (1 - fog) + 30 * fog) for k in range(3))
            pop_k = clamp01((density - ta) * 6)
            rxx, ryy = rx * pop_k, ry * pop_k
            if rxx < 0.6:
                continue
            d.ellipse([x - rxx + 1, y - ryy + 1, x + rxx + 1, y + ryy + 2], fill=(0, 0, 0, 80))
            d.ellipse([x - rxx, y - ryy - ryy * 0.5, x + rxx, y + ryy - ryy * 0.5], fill=(*fill, 255),
                      outline=(*shade(fill, 0.55), 255))
            if rxx > 4 and col == "w":
                d.point((int(x - rxx * 0.4), int(y - ryy)), fill=(255, 255, 255, 255))
            if rxx > 4 and col == "b":
                d.point((int(x - rxx * 0.4), int(y - ryy)), fill=(100, 100, 120, 255))
    return cv


def sky(seed_t):
    cv = vgradient((4, 4, 12), (24, 20, 44), 8)
    STARS.draw(cv, seed_t, alpha=0.7)
    return cv


# =========================================================================== escenas

def sc_board(t):
    """El go: más posiciones que átomos. Ninguna máquina podría vencer a un maestro."""
    w = TL.word
    t_go = w("c6_01", "go")
    t_chino = w("c6_01", "chino")
    t_pos = w("c6_01", "posiciones")
    t_atom = w("c6_01", "atomos")
    t_obs = w("c6_01", "observable")
    t_dur = w("c6_01", "Durante")
    t_maq = w("c6_01", "maquina")
    t_venc = w("c6_01", "vencer")
    t_mae = w("c6_01", "maestro")
    t0 = TL.s("c6_01") - 0.2
    cv = sky(t)
    density = 0.15 + 0.85 * ease_out(prog(t, t0, t_dur))
    cv = infinite_board(cv, t, (t - t0) * 0.9, density)
    # título GO
    if t < t_pos:
        a_out = 1 - prog(t, t_pos - 0.3, t_pos - 0.05)
        a, dy = pop(t, t_go - 0.05, 0.4)
        if a > 0:
            draw_text(cv, "GO", 240, 18 + dy, "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2,
                      alpha=min(a, a_out))
        draw_text(cv, "UN JUEGO CHINO MILENARIO", 240, 74, "press", 8, CREAM, align="center",
                  reveal=(t - t_chino + 0.1) * 40, alpha=a_out)
    # paneles: posiciones vs átomos
    up = int(ease_in_out(prog(t, t_dur - 0.1, t_dur + 0.4)) * -120)
    if t > t_pos - 0.05:
        a, dy = pop(t, t_pos - 0.05)
        x0, y0 = 14, 14 + dy + up
        window(cv, x0, y0, 196, 80)
        draw_text(cv, "POSICIONES POSIBLES", x0 + 98, y0 + 10, "press", 8, CREAM, align="center")
        e = int(1 + 169 * ease_out(prog(t, t_pos, t_pos + 1.0)))
        pow10(cv, str(e), x0 + 98, y0 + 36, 32, GOLD_RAMP)
    if t > t_atom - 0.1:
        a, dy = pop(t, t_atom - 0.1)
        x0, y0 = 270, 14 + dy + up
        window(cv, x0, y0, 196, 80)
        draw_text(cv, "ÁTOMOS EN EL UNIVERSO", x0 + 98, y0 + 8, "press", 8, CREAM, align="center")
        draw_text(cv, "OBSERVABLE", x0 + 98, y0 + 19, "press", 8, CREAM, align="center",
                  reveal=(t - t_obs + 0.1) * 30)
        e = int(1 + 79 * ease_out(prog(t, t_atom, t_atom + 0.8)))
        pow10(cv, str(e), x0 + 98, y0 + 40, 32, CYAN_RAMP)
    if t > t_obs - 0.2:
        a, dy = pop(t, t_obs - 0.2)
        draw_text(cv, ">", 240, 40 + dy + up, "press", 32, (255, 110, 90), align="center", outline_w=2)
    # la máquina, confundida
    if t > t_dur:
        x, _ = walk(t, t_dur, t_dur + 0.9, W + 60, 330)
        face = "question" if t > t_maq else "think"
        if t > t_mae + 0.2:
            face = "sad"
        robot(cv, x, 262, t, face=face, scale=3)
        if t > t_maq:
            a, dy = pop(t, t_maq)
            draw_text(cv, "?", 330 + 52 + int(math.sin(t * 5) * 2), 136 + dy, "press", 24, align="center",
                      gradient=CYAN_RAMP)
        # cita
        a, dy = pop(t, t_dur + 0.3)
        if a > 0:
            window(cv, 40, 22 + dy, 400, 46)
            draw_text(cv, "«NINGUNA MÁQUINA PODRÁ", 240, 32 + dy, "press", 8, CREAM, align="center",
                      reveal=(t - t_dur - 0.4) * 22)
            draw_text(cv, "VENCER A UN MAESTRO»", 240, 48 + dy, "press", 8, CREAM, align="center",
                      reveal=(t - t_venc + 0.1) * 30)
        stamp(cv, "IMPOSIBLE", 150, 150, t, t_mae + 0.1, angle=10)
    dx, dy = shake(t, w("c6_01", "maestro") + 0.26, amp=3)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


def sc_seoul(t):
    """Seúl, marzo de 2016: AlphaGo (DeepMind) contra Lee Sedol."""
    w = TL.word
    t_mar = w("c6_02", "marzo")
    t_2016 = w("c6_02", "dos")
    t_alpha = w("c6_02", "AlphaGo")
    t_dm = w("c6_02", "DeepMind")
    t_enf = w("c6_02", "enfrenta")
    t_lee = w("c6_02", "Lee")
    t_mej = w("c6_02", "mejores")
    cv = bg("bg_seoul_match_2016").copy()
    # Lee Sedol (izq.) y Aja Huang colocando las piedras de AlphaGo (der.)
    lee_arms = "think" if t < t_lee else ("hold" if t < t_mej else "cross")
    char(cv, "leesedol", 140, 262, t, sit=True, look=1, arms=lee_arms,
         mood="neutral", scale=3)
    placing = any(tp < t < tp + 0.5 for tp in (t_alpha + 0.4, t_lee + 1.6))
    char(cv, "ajahuang", 340, 262, t, sit=True, look=-1, arms="point_l" if placing else "down", scale=3)
    bigyear(cv, "2016", 240, 22, t, t_2016) if t < t_enf - 0.1 else None
    # ventana de AlphaGo
    if t > t_alpha - 0.1:
        a, dy = pop(t, t_alpha - 0.1)
        x0, y0 = 356, 14 + dy
        window(cv, x0, y0, 112, 46, fill=(10, 20, 44), border=CYAN, inner=(40, 90, 140))
        d = ImageDraw.Draw(cv)
        # logo: cerebro/ojo pixel
        lit = int(t * 4) % 2
        d.rectangle([x0 + 8, y0 + 9, x0 + 21, y0 + 22], fill=(20, 60, 110, 255), outline=(*CYAN, 255))
        d.rectangle([x0 + 12, y0 + 13, x0 + 17, y0 + 18], fill=(*((140, 240, 255) if lit else CYAN), 255))
        draw_text(cv, "ALPHAGO", x0 + 28, y0 + 10, "press", 8, CYAN)
        draw_text(cv, "DEEPMIND", x0 + 28, y0 + 26, "silk", 8, GREY, reveal=(t - t_dm + 0.1) * 30)
    # etiqueta de Aja Huang (coloca las piedras de AlphaGo)
    if t > t_alpha + 0.3:
        a, dy = pop(t, t_alpha + 0.3)
        tw, _ = text_size("AJA HUANG", "silk", 8)
        window(cv, 340 - tw // 2 - 7, 92 + dy, tw + 14, 16, alpha=0.85)
        draw_text(cv, "AJA HUANG", 340, 96 + dy, "silk", 8, CREAM, align="center")
    # VS
    if t > t_enf - 0.05:
        a, dy = pop(t, t_enf - 0.05)
        draw_text(cv, "VS", 240, 64 + dy, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
        for i in range(3):
            sparkle(cv, 208 + i * 32, 60 + (i % 2) * 40, t + i, 3, GOLD)
    lower_third(cv, "SEÚL · MARZO DE 2016", "GOOGLE DEEPMIND CHALLENGE MATCH", t, t_mar - 0.25, t_lee - 0.25)
    # tarjeta de Lee Sedol
    if t > t_lee - 0.15:
        a = prog(t, t_lee - 0.15, t_lee + 0.25)
        off = int((1 - ease_out(a)) * -150)
        portrait_card(cv, "lee_sedol", 14 + off, 180)
        window(cv, 86 + off, 192, 230, 46)
        draw_text(cv, "LEE SEDOL", 96 + off, 202, "press", 16, CREAM)
        draw_text(cv, "UNO DE LOS MEJORES DEL MUNDO", 96 + off, 222, "silk", 8, GREY)
        if t > t_mej:
            for i in range(3):
                sparkle(cv, 100 + off + i * 60, 196 + (i % 2) * 36, t + i * 0.5, 3, GOLD)
    return vignette(cv, 0.35)


def sc_move37(t):
    """Segunda partida: la jugada 37. Los comentaristas creen que es un error. No lo es."""
    w = TL.word
    t_seg = w("c6_03", "segunda")
    t_jug = w("c6_03", "jugada")
    t_37 = w("c6_03", "siete")
    t_lugar = w("c6_03", "lugar")
    t_prof = w("c6_03", "profesional")
    t_com = w("c6_04", "comentaristas")
    t_err = w("c6_04", "error")
    t_no = w("c6_04", "No")
    t_def = w("c6_04", "define")
    cv = vgradient((10, 8, 20), (34, 24, 30), 8)
    d = ImageDraw.Draw(cv)
    # mesa
    d.rectangle([0, 200, W, H], fill=(46, 28, 18, 255))
    cell = 10
    x0, y0 = 150, 54
    P = board_td(cv, x0, y0, cell)
    for (i, j) in B_BLACK:
        stone(cv, *P(i, j), 4, "b")
    for (i, j) in B_WHITE:
        stone(cv, *P(i, j), 4, "w")
    sx, sy = P(*M37)
    lit = prog(t, t_no, t_no + 0.3)
    # la luz: onda cian y territorio
    if lit > 0:
        R = ease_out(prog(t, t_no, t_def + 1.0)) * 220
        for i in range(19):
            for j in range(19):
                if (i, j) in B_BLACK or (i, j) in B_WHITE or (i, j) == M37:
                    continue
                px, py = P(i, j)
                dd = math.hypot(px - sx, py - sy)
                if dd < R and (i >= 10 or dd < R * 0.45) and t > t_def - 0.2:
                    k = (i + j + int(t * 6)) % 5 == 0
                    d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=((150, 240, 255, 255) if k else (*CYAN, 200)))
        ring = (t - t_no) * 240
        if 0 < ring < 260:
            d.ellipse([sx - ring, sy - ring, sx + ring, sy + ring], outline=(*CYAN, 255), width=2)
        for (i, j) in B_BLACK:
            if math.hypot(P(i, j)[0] - sx, P(i, j)[1] - sy) < R:
                stone(cv, *P(i, j), 4, "b", glow=(CYAN, 0.6))
    # la piedra 37
    t_drop0 = t_jug + 0.05
    if t > t_drop0:
        p = prog(t, t_drop0, t_37)
        if p < 1:
            r = 4 * (1 + 3.5 * (1 - p) ** 2)
            yy = sy - (1 - p) ** 2 * 40
            d.ellipse([sx - 4 * p - 1, sy - 2 * p, sx + 4 * p + 1, sy + 2 * p + 1], fill=(0, 0, 0, int(120 * p)))
            stone(cv, sx, yy, r, "b", glow=(CYAN, 0.4 + 0.6 * p))
        else:
            pulse = 0.6 + 0.4 * math.sin(t * 6)
            stone(cv, sx, sy, 4, "b", glow=(CYAN, pulse))
            imp = prog(t, t_37, t_37 + 0.5)
            if imp < 1:
                rr = 6 + imp * 40
                d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], outline=(200, 250, 255, 255), width=2)
            d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], outline=(*CYAN, 255))
    # quinta línea
    if t > t_lugar and t < t_com:
        a = prog(t, t_lugar, t_lugar + 0.4)
        ll = int(ease_out(a) * 180)
        for yy in range(y0, y0 + ll, 4):
            d.line([(sx, yy), (sx, yy + 1)], fill=(*CYAN, 255))
        for k in range(1, 6):
            xx = P(19 - k, 0)[0]
            draw_text(cv, str(k), xx, y0 + 194, "silk", 8, CYAN if k == 5 else GREY, align="center")
        draw_text(cv, "5ª LÍNEA", 410, 126, "press", 8, CYAN, align="center", alpha=a)
    # etiquetas de jugadores (se ocultan durante el acercamiento)
    a, dy = pop(t, t_seg - 0.1)
    vis = (1 - prog(t, t_jug - 0.2, t_jug)) + prog(t, t_com - 0.3, t_com)
    if a > 0 and vis > 0:
        a = min(a, vis)
        window(cv, 8, 12 + dy, 128, 30)
        draw_text(cv, "PARTIDA 2", 72, 18 + dy, "press", 8, GOLD, align="center", alpha=a)
        draw_text(cv, "10 · MARZO · 2016", 72, 30 + dy, "silk", 8, GREY, align="center", alpha=a)
        window(cv, 8, 50 + dy, 128, 44)
        stone(cv, 22, 64 + dy, 4, "b")
        draw_text(cv, "ALPHAGO", 32, 60 + dy, "press", 8, CYAN, alpha=a)
        stone(cv, 22, 80 + dy, 4, "w")
        draw_text(cv, "LEE SEDOL", 32, 76 + dy, "press", 8, CREAM, alpha=a)
    # JUGADA 37: a la derecha durante el acercamiento, arriba cuando llegan los comentaristas
    if t > t_37:
        if t < t_com - 0.3:
            a, dy = pop(t, t_37, 0.3)
            draw_text(cv, "JUGADA", 410, 54 + dy, "press", 16, align="center", gradient=CYAN_RAMP, outline_w=2)
            draw_text(cv, "37", 410, 76 + dy, "press", 32, align="center", gradient=CYAN_RAMP, outline_w=2)
        else:
            a, dy = pop(t, t_com - 0.3, 0.3)
            draw_text(cv, "JUGADA 37", 240, 12 + dy, "press", 24, align="center", gradient=CYAN_RAMP,
                      outline_w=2)
    if t_prof - 0.2 < t < t_com:
        a, dy = pop(t, t_prof - 0.2)
        x1, y1 = 348, 150 + dy
        window(cv, x1, y1, 124, 46, fill=(40, 14, 20), border=(226, 90, 80))
        draw_text(cv, "¿UN HUMANO?", x1 + 62, y1 + 10, "press", 8, CREAM, align="center")
        draw_text(cv, "¡JAMÁS!", x1 + 62, y1 + 26, "press", 8, (255, 120, 100), align="center")
    # comentaristas (abajo en las esquinas)
    if t > t_com - 0.2:
        up = ease_out(prog(t, t_com - 0.2, t_com + 0.3))
        feet = int(320 - up * 22)
        surprised = t > t_no
        for k, (spec, x) in enumerate(((REDMOND, 62), (GARLOCK, 418))):
            talking = (t_err - 0.6 < t < t_no) and k == 0
            char(cv, spec, x, feet, t, scale=3, look=1 if x < 240 else -1,
                 mood="worried" if (t > t_err - 0.3 and not surprised) else ("happy" if t > t_def else "neutral"),
                 arms="shrug" if (t_err < t < t_no and k == 1) else ("cheer" if t > t_def + 0.4 else "down"),
                 talk=talk_v(t, talking))
        if t_err - 0.35 < t < t_no:
            bubble(cv, "¿UN ERROR?", 62, feet - 156, reveal=(t - t_err + 0.35) * 24)
            if t > t_err + 0.2:
                bubble(cv, "¿?", 418, feet - 156)
        if t > t_no:
            a, dy = pop(t, t_no)
            draw_text(cv, "!", 62, feet - 182 + dy, "press", 16, GOLD, align="center")
            draw_text(cv, "!", 418, feet - 182 + dy, "press", 16, GOLD, align="center")
    if t > t_no:
        a, dy = pop(t, t_no + 0.05)
        window(cv, 158, 238 + dy, 164, 24, fill=(8, 36, 50), border=CYAN, inner=(40, 110, 140))
        txt = "NO ERA UN ERROR" if t < t_def - 0.1 else "JUGADA DECISIVA"
        draw_text(cv, txt, 240, 246 + dy, "press", 8, CYAN if t < t_def - 0.1 else GOLD, align="center")
    dx, dy = shake(t, t_37, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    if t_37 <= t < t_37 + 0.12:
        cv = fade_to(cv, (220, 250, 255), 0.4 * (1 - (t - t_37) / 0.12))
    return vignette(cv, 0.4)


def sc_score(t):
    """AlphaGo gana la serie 4 a 1. Pero en la cuarta partida..."""
    w = TL.word
    t_ag = w("c6_04", "AlphaGo")
    t_4 = w("c6_04", "cuatro")
    t_1 = w("c6_04", "uno")
    t_cuarta = w("c6_05", "cuarta")
    cv = grade(bg("bg_seoul_match_2016"), mul=(0.45, 0.42, 0.5), sat=0.6)
    a, dy = pop(t, t_ag - 0.1, 0.4)
    x0, y0 = 24, 26 + dy
    window(cv, x0, y0, 432, 196)
    draw_text(cv, "SERIE · SEÚL 2016", 240, y0 + 10, "press", 8, GOLD, align="center")
    portrait_card(cv, "la_maquina", x0 + 22, y0 + 34, frame=CYAN)
    portrait_card(cv, "lee_sedol", x0 + 432 - 86, y0 + 34)
    draw_text(cv, "ALPHAGO", x0 + 54, y0 + 108, "press", 8, CYAN, align="center")
    draw_text(cv, "LEE SEDOL", x0 + 432 - 54, y0 + 108, "press", 8, CREAM, align="center")
    if t > t_4:
        a, dy2 = pop(t, t_4, 0.3)
        draw_text(cv, "4", 190, y0 + 46 + dy2, "press", 48, align="center", gradient=CYAN_RAMP, outline_w=2)
    draw_text(cv, "–", 240, y0 + 46, "press", 48, CREAM, align="center", alpha=prog(t, t_4, t_4 + 0.2))
    if t > t_1:
        a, dy2 = pop(t, t_1, 0.3)
        draw_text(cv, "1", 290, y0 + 46 + dy2, "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2)
    # partidas
    winners = ["A", "A", "A", "L", "A"]
    for i in range(5):
        ti = t_ag + 0.25 + i * 0.3
        if t < ti:
            continue
        aa, dyy = pop(t, ti, 0.3)
        bx = 240 + (i - 2) * 46 - 19
        by = y0 + 124 + dyy
        hl = t > t_cuarta - 0.1
        isL = winners[i] == "L"
        col = GOLD if isL else CYAN
        if hl and not isL:
            fill, border = (20, 22, 40), (70, 80, 110)
        elif hl and isL:
            fill, border = (90, 60, 20), (GOLD if int(t * 6) % 2 else (255, 250, 220))
        else:
            fill, border = (14, 30, 54) if not isL else (54, 40, 18), col
        window(cv, bx, by, 38, 44, fill=fill, border=border)
        draw_text(cv, f"P{i + 1}", bx + 19, by + 6, "silk", 8, GREY, align="center")
        dd = ImageDraw.Draw(cv)
        tok = col if not (hl and not isL) else (60, 90, 120)
        cx_, cy_ = bx + 19, by + 28
        if isL and hl:
            dd.ellipse([cx_ - 10, cy_ - 10, cx_ + 10, cy_ + 10], fill=(*GOLD, 70))
        dd.ellipse([cx_ - 6, cy_ - 6, cx_ + 6, cy_ + 6], fill=(*tok, 255), outline=(*INK, 255))
        dd.point((cx_ - 3, cy_ - 3), fill=(255, 255, 255, 255))
    if t > t_cuarta - 0.1:
        a, dyy = pop(t, t_cuarta - 0.1)
        draw_text(cv, "¡GANA LEE SEDOL!", 240, y0 + 174 + dyy, "press", 8, GOLD, align="center")
    # leyenda
    if t > t_ag + 1.6 and t < t_cuarta - 0.1:
        dd = ImageDraw.Draw(cv)
        dd.ellipse([150, y0 + 174, 158, y0 + 182], fill=(*CYAN, 255), outline=(*INK, 255))
        draw_text(cv, "ALPHAGO", 162, y0 + 175, "silk", 8, CYAN)
        dd.ellipse([250, y0 + 174, 258, y0 + 182], fill=(*GOLD, 255), outline=(*INK, 255))
        draw_text(cv, "LEE SEDOL", 262, y0 + 175, "silk", 8, GOLD)
    return vignette(cv, 0.4)


def persp_board(cv, t, x_bl, x_br, x_tl, x_tr, y_t, y_b, n=19):
    """Tablero en perspectiva (en primer plano). Devuelve función (i,j)->(x,y,escala)."""
    d = ImageDraw.Draw(cv)
    d.polygon([(x_tl, y_t), (x_tr, y_t), (x_br, y_b), (x_bl, y_b)], fill=(*WOOD, 255), outline=(*INK, 255))
    d.rectangle([x_tl, y_t - 3, x_tr, y_t - 1], fill=(*shade(WOOD, 1.15), 255))

    def pt(i, j):
        v = (j + 1) / (n + 1)
        yy = y_t + (y_b - y_t) * v
        xl = x_tl + (x_bl - x_tl) * v
        xr = x_tr + (x_br - x_tr) * v
        u = (i + 1) / (n + 1)
        return xl + (xr - xl) * u, yy, (xr - xl) / (x_tr - x_tl)
    for k in range(n):
        a1, b1 = pt(k, 0), pt(k, n - 1)
        d.line([(int(a1[0]), int(a1[1])), (int(b1[0]), int(b1[1]))], fill=(*LINE, 255))
        a2, b2 = pt(0, k), pt(n - 1, k)
        d.line([(int(a2[0]), int(a2[1])), (int(b2[0]), int(b2[1]))], fill=(*LINE, 255))
    return pt


L_BLACK = [(3, 3), (15, 3), (9, 6), (12, 8), (4, 12), (8, 10), (13, 14), (2, 16), (16, 12), (10, 4), (6, 7)]
L_WHITE = [(15, 15), (3, 15), (16, 4), (11, 9), (5, 10), (14, 6), (7, 13), (17, 9), (2, 8), (12, 16)]
M78 = (10, 10)


def sc_lee78(t):
    """Lee Sedol responde con su propia jugada imposible, la 78: la única derrota de la máquina."""
    w = TL.word
    t0 = w("c6_05", "Lee") - 0.15
    t_resp = w("c6_05", "responde")
    t_imp = w("c6_05", "imposible")
    t_78 = w("c6_05", "setenta")
    t_arr = w("c6_05", "arranca")
    t_maq = w("c6_05", "maquina")
    t_unica = w("c6_05", "unica")
    cv = grade(bg("bg_seoul_match_2016"), mul=(0.7, 0.66, 0.72), sat=0.8)
    if t > t_78:
        cv = spotlight(cv, 140, 0, 220, 30, 120, color=(255, 220, 120), strength=0.22)
    win = t > t_unica - 0.1
    lee_arms = "think"
    if t > t_resp - 0.2:
        lee_arms = "point" if t < t_78 + 0.8 else "hold"
    if win:
        lee_arms = "cheer"
    hop = int(abs(math.sin(t * 7)) * 8) if win else 0
    char(cv, "leesedol", 140, 262 - hop, t, scale=3, arms=lee_arms, look=1,
         mood="happy" if (win or t > t_78 + 0.3) else "neutral")
    rx, ry = shake(t, t_arr + 0.1, 0.4, 3)
    face = "think"
    if t > t_imp:
        face = "question"
    if t > t_maq:
        face = "sad"
    robot(cv, 352 + rx, 250 + ry, t, face=face, scale=3)
    if t_imp < t < t_maq:
        a, dy = pop(t, t_imp)
        draw_text(cv, "?!", 352 + 34, 120 + dy, "press", 16, (255, 120, 100), align="center")
    pt = persp_board(cv, t, 30, 450, 112, 368, 214, 270)
    for (i, j) in L_BLACK:
        x, y, s = pt(i, j)
        stone(cv, x, y, 4 * s, "b")
    for (i, j) in L_WHITE:
        x, y, s = pt(i, j)
        stone(cv, x, y, 4 * s, "w")
    if t > t_78 - 0.35:
        p = prog(t, t_78 - 0.35, t_78)
        x, y, s = pt(*M78)
        yy = y - (1 - p) ** 2 * 50
        stone(cv, x, yy, 4 * s * (1 + 1.5 * (1 - p)), "w", glow=(GOLD, 0.5 + 0.5 * math.sin(t * 6) if p >= 1 else p))
        if p >= 1:
            imp = prog(t, t_78, t_78 + 0.5)
            if imp < 1:
                rr = 6 + imp * 46
                ImageDraw.Draw(cv).ellipse([x - rr, y - rr * 0.5, x + rr, y + rr * 0.5], outline=(255, 230, 140, 255),
                                           width=2)
    # títulos
    a, dy = pop(t, t0)
    window(cv, 8, 10 + dy, 128, 30)
    draw_text(cv, "PARTIDA 4", 72, 16 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "13 · MARZO · 2016", 72, 28 + dy, "silk", 8, GREY, align="center")
    if t > t_78:
        a, dy = pop(t, t_78, 0.3)
        draw_text(cv, "JUGADA 78", 300, 12 + dy, "press", 24, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, "«LA JUGADA DIVINA»", 300, 44, "press", 8, CREAM, align="center",
                  reveal=(t - t_78 - 0.3) * 30)
    if win:
        a, dy = pop(t, t_unica - 0.1)
        window(cv, 150, 62 + dy, 300, 24, fill=(60, 36, 14), border=GOLD)
        draw_text(cv, "LA ÚNICA DERROTA DE ALPHAGO", 300, 70 + dy, "press", 8, GOLD, align="center")
        for i in range(5):
            sparkle(cv, 70 + i * 34, 100 + (i % 2) * 30, t + i * 0.6, 3, GOLD)
    return vignette(cv, 0.35)


def sc_intuition(t):
    """Por primera vez, una IA no solo calculaba. Parecía tener intuición."""
    w = TL.word
    t0 = TL.s("c6_06")
    t_calc = w("c6_06", "solo")
    t_par = w("c6_06", "Parecia")
    t_int = w("c6_06", "intuicion")
    cv = vgradient((4, 6, 16), (16, 22, 46), 10)
    d = ImageDraw.Draw(cv)
    # rejilla de go tenue
    for x in range(0, W, 18):
        d.line([(x, 0), (x, H)], fill=(24, 32, 60, 255))
    for y in range(0, H, 18):
        d.line([(0, y), (W, y)], fill=(24, 32, 60, 255))
    STARS.draw(cv, t, alpha=0.4)
    intu = prog(t, t_par, t_par + 0.4)
    # columnas de cálculo
    calc_a = prog(t, t0 + 0.2, t0 + 0.6) * (1 - intu)
    if calc_a > 0:
        for c in range(14):
            cx = 20 + c * 34
            if 170 < cx < 310:
                continue
            for r in range(12):
                yy = int((r * 22 + t * (60 + c * 7) + c * 31) % (H + 22)) - 22
                v = int((_h(c, r + int(t * 8)) * 10))
                col = (90, 200, 120) if r % 3 else (160, 255, 180)
                draw_text(cv, str(v), cx, yy, "silk", 8, col, alpha=calc_a * (0.5 + 0.5 * (r % 2)))
    # la máquina
    face = "think" if t < t_par else "heart"
    robot(cv, 240, 236, t, face=face, scale=3)
    if t > t_calc - 0.1 and t < t_par + 0.3:
        a, dy = pop(t, t_calc - 0.1)
        window(cv, 168, 44 + dy, 144, 26, fill=(14, 40, 26), border=(110, 230, 140))
        draw_text(cv, "CALCULAR", 240, 53 + dy, "press", 8, (140, 255, 170), align="center")
    if intu > 0:
        # bombilla y corazón brillante
        cv = spotlight(cv, 240, 0, 236, 20, 160, color=(255, 210, 120), strength=0.2 * intu)
        bulb(cv, 240, 98 - int(abs(math.sin(t * 3)) * 3), t, intu)
        for i in range(8):
            ang = i * math.pi / 4 + t * 0.8
            sparkle(cv, int(240 + math.cos(ang) * 74), int(170 + math.sin(ang) * 56), t + i * 0.4, 3,
                    GOLD if i % 2 else CYAN)
    if t > t_int - 0.1:
        a, dy = pop(t, t_int - 0.1, 0.4)
        draw_text(cv, "¿INTUICIÓN?", 240, 26 + dy, "press", 24, align="center", gradient=CYAN_RAMP, outline_w=2)
    draw_text(cv, "POR PRIMERA VEZ...", 240, 18, "press", 16, CREAM, align="center",
              reveal=(t - t0) * 24, alpha=1 - prog(t, t_par - 0.3, t_par))
    return vignette(cv, 0.4)


# =========================================================================== montaje

def scenes():
    w = TL.word
    st = TL.chapter_start(CH)
    t37 = w("c6_03", "siete")
    return [
        (st - 0.3, make_card(CH, ["LA JUGADA 37"], "2016"), None),
        (TL.s("c6_01") - 0.2, sc_board,
         lambda t: (1.0 + cam_punch(t, [w("c6_01", "posiciones"), w("c6_01", "atomos"),
                                        w("c6_01", "observable")], 0.05)
                    + cam_punch(t, [w("c6_01", "maestro") + 0.26], 0.08), 240, 135)),
        (TL.s("c6_02") - 0.2, sc_seoul,
         lambda t: (1.0 + cam_punch(t, [w("c6_02", "enfrenta")], 0.06) + cam_punch(t, [w("c6_02", "Lee")], 0.03),
                    240, 140)),
        (TL.s("c6_03") - 0.2, sc_move37,
         lambda t: (cam_push(t, w("c6_03", "jugada"), t37, 1.0, 1.18, (240, 140), (290, 150))[0]
                    * (1 - prog(t, w("c6_04", "comentaristas") - 0.4, w("c6_04", "comentaristas")))
                    + 1.0 * prog(t, w("c6_04", "comentaristas") - 0.4, w("c6_04", "comentaristas"))
                    + cam_punch(t, [t37], 0.12) + cam_punch(t, [w("c6_04", "No")], 0.06),
                    290 - 50 * prog(t, w("c6_04", "comentaristas") - 0.4, w("c6_04", "comentaristas")),
                    150 - 15 * prog(t, w("c6_04", "comentaristas") - 0.4, w("c6_04", "comentaristas")))),
        (w("c6_04", "AlphaGo") - 0.2, sc_score,
         lambda t: (1.0 + cam_punch(t, [w("c6_04", "cuatro"), w("c6_04", "uno")], 0.07), 240, 135)),
        (w("c6_05", "Lee") - 0.15, sc_lee78,
         lambda t: (1.0 + cam_punch(t, [w("c6_05", "setenta")], 0.1)
                    + cam_punch(t, [w("c6_05", "unica")], 0.05), 240, 135)),
        (TL.s("c6_06") - 0.15, sc_intuition,
         lambda t: cam_push(t, TL.s("c6_06"), TL.e("c6_06"), 1.0, 1.12, (240, 135), (240, 130))),
    ]


# =========================================================================== audio

def _clack(A, t, vol=0.07):
    n = int(0.03 * A.SR)
    sig = A.noise(0.03, 2) * np.exp(-np.arange(n) / A.SR * 160)
    A.sfx.add(t, sig, vol)
    A.blip(t, 340, 0.025, vol * 0.6, 0.5)


def music(A):
    w = TL.word
    st = TL.chapter_start(CH)
    end = chapter_end(CH)
    t37 = w("c6_03", "siete")
    t_jug = w("c6_03", "jugada")
    t_no = w("c6_04", "No")
    t_78 = w("c6_05", "setenta")
    Em = [("E", "min"), ("C", "maj"), ("A", "min"), ("B", "maj")]
    A.section(st + 1.6, TL.s("c6_02") - 0.2, 92, Em, A.st_puzzle)
    A.section(TL.s("c6_02") - 0.2, t_jug, 96, [("D", "min"), ("Bb", "maj"), ("G", "min"), ("A", "maj")], A.st_build)
    # riser hacia la jugada 37
    n = int((t37 - t_jug) * A.SR)
    A.music.add(t_jug, A.noise(t37 - t_jug, 3) * np.linspace(0, 1, n) ** 2, 0.06)
    tt = t_jug
    k = 0
    while tt < t37 - 0.05:
        A.note(A.music, tt, A.midi_hz(57 + k), 0.07, duty=0.125, vol=0.05, s=0.4)
        tt += 0.09
        k += 1
    # golpe
    A.kick(A.music, t37, 0.55)
    A.crash(A.music, t37, 0.2)
    A.sting(t37, [50, 57, 62, 66, 69], vol=0.06, step=0.07, hold=1.8)
    A.note(A.music, t37, A.midi_hz(38), 2.4, "tri", vol=0.3, s=0.9, r=0.8)
    # desconcierto
    A.section(t37 + 1.2, t_no, 80, [("D", "min"), ("E", "min")], A.st_mystery)
    # no lo es -> triunfo de la máquina
    A.kick(A.music, t_no, 0.4)
    A.crash(A.music, t_no, 0.12)
    A.section(t_no, w("c6_05", "Pero"), 108, [("D", "maj"), ("A", "maj"), ("B", "min"), ("G", "maj")], A.st_triumph)
    # cuarta partida: tensión -> respuesta humana
    A.section(w("c6_05", "Pero"), t_78, 96, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "maj")], A.st_build)
    A.sting(t_78, [60, 64, 67, 72, 76], vol=0.06, step=0.08, hold=1.4)
    A.crash(A.music, t_78, 0.12)
    A.section(t_78 + 0.6, TL.s("c6_06") - 0.1, 112, [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")],
              A.st_bright)
    # intuición: asombro
    A.section(TL.s("c6_06") - 0.1, end - 0.2, 80, [("F", "maj7"), ("C", "maj7"), ("F", "maj7"), ("G", "sus")],
              A.st_mystery)
    t_int = w("c6_06", "intuicion")
    A.sting(t_int, [72, 76, 79, 83, 84], vol=0.05, step=0.1, hold=1.4)


def sfx(A):
    w = TL.word
    # tablero infinito
    t0 = TL.s("c6_01") - 0.2
    for i in range(12):
        _clack(A, t0 + 0.3 + i * 0.47 + (i % 3) * 0.08, 0.045)
    A.pop_sfx(w("c6_01", "go") - 0.05, 420)
    A.text_blips(w("c6_01", "chino") - 0.1, 24, 40, 0.015)
    for name, n in (("posiciones", 14), ("atomos", 11)):
        tp = w("c6_01", name)
        A.pop_sfx(tp - 0.1, 520)
        for k in range(n):
            A.blip(tp + k * 0.07, 900 + k * 40, 0.02, 0.025)
    A.coin(w("c6_01", "observable") - 0.2, 0.05)
    A.whoosh(w("c6_01", "Durante"), 0.5, 0.05)
    A.text_blips(w("c6_01", "maquina") - 0.4, 22, 30, 0.015)
    A.text_blips(w("c6_01", "vencer") - 0.1, 20, 30, 0.015)
    A.kick(A.sfx, w("c6_01", "maestro") + 0.26, 0.35)
    # Seúl
    A.whoosh(w("c6_02", "marzo") - 0.3, 0.4, 0.05)
    A.pop_sfx(w("c6_02", "AlphaGo") - 0.1, 600)
    A.robot_beep(w("c6_02", "AlphaGo") + 0.1, 0.035)
    _clack(A, w("c6_02", "AlphaGo") + 0.6)
    _clack(A, w("c6_02", "Lee") + 1.8)
    A.kick(A.sfx, w("c6_02", "enfrenta"), 0.3)
    A.whoosh(w("c6_02", "Lee") - 0.2, 0.3, 0.05)
    A.join_jingle(w("c6_02", "Lee") - 0.05)
    # jugada 37
    A.pop_sfx(w("c6_03", "segunda") - 0.1, 480)
    for i, dt in enumerate((0.25, 0.9, 1.5)):
        _clack(A, TL.s("c6_03") + dt, 0.05)
    t37 = w("c6_03", "siete")
    _clack(A, t37, 0.12)
    A.whoosh(w("c6_03", "jugada"), 0.8, 0.04)
    A.text_blips(w("c6_03", "lugar"), 8, 20, 0.02, 1300)
    A.pop_sfx(w("c6_03", "profesional") - 0.2, 380)
    A.whoosh(w("c6_04", "comentaristas") - 0.2, 0.4, 0.04)
    A.text_blips(w("c6_04", "error") - 0.35, 10, 24, 0.025, 900)
    A.pop_sfx(w("c6_04", "error") + 0.2, 700)
    A.coin(w("c6_04", "No") + 0.05, 0.05)
    for i in range(6):
        A.blip(w("c6_04", "define") + i * 0.08, 700 + i * 110, 0.05, 0.03, 0.25)
    # marcador
    A.whoosh(w("c6_04", "AlphaGo") - 0.2, 0.3, 0.05)
    for i in range(5):
        A.pop_sfx(w("c6_04", "AlphaGo") + 0.25 + i * 0.3, 500 + i * 60, 0.05)
    A.kick(A.sfx, w("c6_04", "cuatro"), 0.3)
    A.kick(A.sfx, w("c6_04", "uno"), 0.3)
    A.coin(w("c6_05", "cuarta") - 0.1, 0.05)
    # jugada 78
    _clack(A, w("c6_05", "setenta"), 0.12)
    A.coin(w("c6_05", "setenta") + 0.1, 0.06)
    A.pop_sfx(w("c6_05", "imposible"), 650)
    for i in range(4):  # robot triste
        A.blip(w("c6_05", "maquina") + i * 0.12, 700 - i * 120, 0.09, 0.035, 0.5)
    A.join_jingle(w("c6_05", "unica") - 0.1, 0.06)
    # intuición
    A.typewriter(TL.s("c6_06") + 0.2, w("c6_06", "Parecia"), 16, 0.015)
    A.pop_sfx(w("c6_06", "solo") - 0.1, 500)
    A.coin(w("c6_06", "Parecia") + 0.05, 0.05)
    A.whoosh(w("c6_06", "intuicion") - 0.2, 0.4, 0.04)
