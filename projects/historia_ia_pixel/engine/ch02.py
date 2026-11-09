"""Capítulo 2: La máquina que iba a ser consciente (1958 – 1969)."""
from common import *  # noqa

RED = (232, 72, 60)
GREEN = (110, 232, 120)
CHALK = (236, 240, 230)
SEPIA_MUL = (1.05, 0.92, 0.72)

# =========================================================================== helpers locales


def flash_white(cv, t, times, dur=0.16, k=0.45, color=(255, 252, 240)):
    for t0 in times:
        if t0 <= t < t0 + dur:
            cv = fade_to(cv, color, k * (1 - (t - t0) / dur))
    return cv


def year_big(cv, text, cx, y, t, t0, t_out=None, size=48):
    """bigyear con salida suave."""
    a_out = 1.0 if t_out is None else 1 - prog(t, t_out, t_out + 0.4)
    p = prog(t, t0, t0 + 0.55)
    if p <= 0 or a_out <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=GOLD_RAMP, outline_w=2,
              alpha=min(p * 3, a_out))
    if p >= 1 and a_out >= 1:
        tw, _ = text_size(text, "press", size)
        for i, ph in enumerate((0.0, 1.7, 3.1)):
            sx = cx - tw // 2 + int((i + 0.5) * tw / 3)
            sparkle(cv, sx + (i * 7) % 11, y + 4 + (i * 13) % size, t + ph, 3)


def name_card(cv, t, t0, t1, pname, title, sub, x=14, y=12):
    """Retrato + ventana con nombre (patrón de sc_turing), entra y sale por la izquierda."""
    a = prog(t, t0 - 0.2, t0 + 0.25)
    out = prog(t, t1 - 0.35, t1)
    if a <= 0 or out >= 1:
        return
    off = int((1 - ease_out(a)) * -150) + int(ease_in_out(out) * -420)
    portrait_card(cv, pname, x + off, y)
    tw = max(text_size(title, "press", 16)[0], text_size(sub, "silk", 8)[0]) + 22
    window(cv, x + 72 + off, y + 14, tw, 46)
    draw_text(cv, title, x + 82 + off, y + 24, "press", 16, CREAM)
    draw_text(cv, sub, x + 82 + off, y + 44, "silk", 8, GREY)


def mark_check(cv, cx, cy, s=10, color=GREEN):
    d = ImageDraw.Draw(cv)
    pts = [(cx - s, cy), (cx - s // 3, cy + s * 2 // 3), (cx + s, cy - s * 2 // 3)]
    d.line(pts, fill=(*INK, 255), width=6)
    d.line(pts, fill=(*color, 255), width=3)


def mark_cross(cv, cx, cy, s=10, color=RED):
    d = ImageDraw.Draw(cv)
    for a, b in (((cx - s, cy - s), (cx + s, cy + s)), ((cx + s, cy - s), (cx - s, cy + s))):
        d.line([a, b], fill=(*INK, 255), width=6)
    for a, b in (((cx - s, cy - s), (cx + s, cy + s)), ((cx + s, cy - s), (cx - s, cy + s))):
        d.line([a, b], fill=(*color, 255), width=3)


_GRUNGE = np.random.default_rng(3).random((200, 400))


def stamp(cv, text, cx, cy, t, t0, color=(214, 44, 44), size=16, angle=-8):
    """Sello de goma que golpea (escala 1.8 -> 1)."""
    if t < t0:
        return
    p = prog(t, t0, t0 + 0.12)
    tw, th = text_size(text, "press", size)
    pad = 8
    w, h = tw + pad * 2 + 4, th + pad * 2 + 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(*color, 255), width=3)
    d.rectangle([5, 5, w - 6, h - 6], outline=(*color, 255), width=1)
    draw_text(im, text, w // 2 + 1, pad + 1, "press", size, color, align="center", outline=None, shadow=False)
    a = np.array(im)
    g = _GRUNGE[:h, :w] if h <= 200 and w <= 400 else np.zeros((h, w))
    a[..., 3] = np.where(g < 0.13, 0, a[..., 3])
    im = Image.fromarray(a, "RGBA").rotate(angle, resample=Image.NEAREST, expand=True)
    sc = 1 + (1 - p) * 0.8
    if sc > 1.01:
        im = im.resize((int(im.size[0] * sc), int(im.size[1] * sc)), Image.NEAREST)
    paste(cv, im, cx - im.size[0] // 2, cy - im.size[1] // 2, min(1.0, 0.4 + p))


def coin_px(d, cx, cy, a=255):
    d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=(240, 200, 80, a), outline=(120, 70, 20, a))
    d.line([(cx - 2, cy), (cx + 2, cy)], fill=(180, 120, 40, a))


def money_bag(cv, cx, by, alpha=1.0):
    im = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([6, 18, 54, 58], fill=(196, 160, 96, 255), outline=(*INK, 255))
    d.ellipse([12, 24, 30, 40], fill=(222, 192, 130, 255))
    d.polygon([(22, 20), (38, 20), (44, 6), (16, 6)], fill=(196, 160, 96, 255), outline=(*INK, 255))
    d.rectangle([20, 17, 40, 21], fill=(120, 60, 40, 255), outline=(*INK, 255))
    draw_text(im, "$", 30, 32, "press", 16, (120, 84, 30), align="center", outline=None, shadow=False)
    paste(cv, im, cx - 30, by - 58, alpha)


def chalk_line(d, a, b, p=1.0, col=CHALK, w=1):
    if p <= 0:
        return
    x = a[0] + (b[0] - a[0]) * p
    y = a[1] + (b[1] - a[1]) * p
    d.line([a, (int(x), int(y))], fill=(*col, 255), width=w)


# --------------------------------------------------------------------------- formas del perceptrón

def _tri():
    s = set()
    for r in range(3, 17):
        half = (r - 3) * 0.62
        for c in range(20):
            if abs(c - 9.5) <= half + 0.01:
                s.add((r, c))
    return s


TRI = _tri()
SQ = {(r, c) for r in range(4, 16) for c in range(4, 16)}


def photo_grid(cv, gx, gy, lit, on=1.0, col=CYAN, cell=7, scan=None, dead=0.0):
    d = ImageDraw.Draw(cv)
    d.rectangle([gx - 3, gy - 3, gx + 20 * cell + 1, gy + 20 * cell + 1], fill=(10, 14, 18, 255),
                outline=(*INK, 255))
    dim = (44, 56, 64)
    if dead:
        dim = tuple(int(v * (1 - 0.45 * dead)) for v in dim)
    for r in range(20):
        for c in range(20):
            x, y = gx + c * cell, gy + r * cell
            if (r, c) in lit and on > 0:
                k = on
                cc = tuple(int(dim[i] + (col[i] - dim[i]) * k) for i in range(3))
            else:
                cc = dim
            if scan is not None and abs(r - scan) < 1:
                cc = tuple(min(255, v + 60) for v in cc)
            d.rectangle([x, y, x + cell - 2, y + cell - 2], fill=(*cc, 255))
            if (r, c) in lit and on > 0.6:
                d.point((x, y), fill=(230, 255, 255, 255))


def mark1_panel(cv, x0, y0, t, lit, on=1.0, out=None, scan=None, dead=0.0, title=True):
    """Panel del Mark I Perceptron: retina de 20x20 + dos lámparas de salida."""
    window(cv, x0, y0, 240, 196, fill=(30, 36, 44), border=(150, 160, 172), inner=(80, 90, 104))
    if title:
        draw_text(cv, "MARK I PERCEPTRÓN", x0 + 120, y0 + 8, "press", 8, GOLD if not dead else GREY,
                  align="center")
    photo_grid(cv, x0 + 22, y0 + 32, lit, on, scan=scan, dead=dead)
    # lámparas de salida
    d = ImageDraw.Draw(cv)
    for i, (cy, lab) in enumerate(((y0 + 74, "tri"), (y0 + 138, "sq"))):
        cx = x0 + 204
        lit_l = out == i and not dead
        if lit_l:
            d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 220, 120, 60))
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 214, 90, 255) if lit_l else (70, 60, 44, 255),
                  outline=(*INK, 255))
        if lit_l:
            d.point((cx - 3, cy - 3), fill=(255, 255, 230, 255))
        yy = cy + 16
        col = (*CREAM, 255) if lit_l else (120, 126, 136, 255)
        if lab == "tri":
            d.polygon([(cx, yy), (cx - 7, yy + 11), (cx + 7, yy + 11)], fill=col, outline=(*INK, 255))
        else:
            d.rectangle([cx - 6, yy, cx + 6, yy + 11], fill=col, outline=(*INK, 255))


# --------------------------------------------------------------------------- red neuronal

NET = [(118, [72, 102, 132, 162, 192, 222]), (240, [80, 114, 148, 182, 216]), (362, [116, 186])]


def _h(i):
    v = math.sin(i * 12.9898 + 4.1) * 43758.5453
    return (v - math.floor(v)) * 2 - 1


EDGES = []
_k = 0
for _L in range(2):
    for _i, _ya in enumerate(NET[_L][1]):
        for _j, _yb in enumerate(NET[_L + 1][1]):
            EDGES.append((_L, _i, _j, (NET[_L][0], _ya), (NET[_L + 1][0], _yb), _h(_k), _h(_k + 300)))
            _k += 1
NODE_IDS = [(L, i) for L in range(3) for i in range(len(NET[L][1]))]


def _lerp(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def draw_net(cv, t, show=(1, 1, 1), adapt=0.0, alive=None, pulse=0.0, crack=0.0, win=None):
    """Red de 3 capas. show: aparición por capa; adapt: pesos que se ajustan; alive(L,i)->0..1."""
    d = ImageDraw.Draw(cv)
    base = (34, 42, 74)
    dead_c = (36, 36, 44)

    def alv(L, i):
        return 1.0 if alive is None else alive(L, i)

    for (L, i, j, a, b, w0, ph) in EDGES:
        sp = show[L + 1]
        if sp <= 0 or show[L] <= 0:
            continue
        wv = w0 + adapt * 0.9 * math.sin(t * 3.2 + ph * 6)
        wv = max(-1.0, min(1.0, wv))
        k = abs(wv)
        tgt = CYAN if wv > 0 else (240, 150, 70)
        col = _lerp(base, tgt, 0.25 + 0.75 * k)
        al = min(alv(L, i), alv(L + 1, j))
        col = _lerp(dead_c, col, al)
        if crack > 0 and int(t * 20 + ph * 9) % 5 == 0 and (ph > 1 - crack * 2):
            col = RED
        chalk_line(d, a, b, sp, col, 2 if (k > 0.72 and al > 0.5) else 1)
        if pulse > 0 and wv > 0.15 and al > 0.5 and sp >= 1:
            u = ((t * 1.4 + ph * 0.5 + L * 0.5) % 1.0)
            px_ = int(a[0] + (b[0] - a[0]) * u)
            py_ = int(a[1] + (b[1] - a[1]) * u)
            d.rectangle([px_ - 1, py_ - 1, px_ + 1, py_ + 1], fill=(220, 255, 255, int(255 * pulse)))
    for L, (x, ys) in enumerate(NET):
        if show[L] <= 0:
            continue
        for i, y in enumerate(ys):
            pp = clamp01(show[L] * len(ys) - i)  # aparición escalonada
            if pp <= 0:
                continue
            al = alv(L, i)
            r = 7
            act = 0.5 + 0.5 * math.sin(t * 4 + i * 1.7 + L)
            if L == 2 and win is not None:
                act = 1.0 if i == win else 0.15
            on_c = _lerp((20, 50, 80), (130, 236, 255), act)
            fill = _lerp((30, 30, 38), on_c, al)
            if al > 0.5 and act > 0.7:
                d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=(90, 220, 255, 50))
            rr = int(r * min(1, pp * 1.4))
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*fill, 255),
                      outline=(*(_lerp((70, 70, 80), (200, 250, 255), al)), 255))
            if al > 0.5:
                d.point((x - 2, y - 2), fill=(240, 255, 255, 255))


# =========================================================================== escenas


def sc_press(t):
    """Julio de 1958. La Marina presenta ante la prensa el invento de Frank Rosenblatt: el perceptrón."""
    cv = bg("bg_press_room_1958").copy()
    w = TL.word
    t0 = TL.s("c2_01")
    t_mar = w("c2_01", "Marina")
    t_pre = w("c2_01", "prensa")
    t_frank = w("c2_01", "Frank")
    t_perc = w("c2_01", "perceptron")
    flashes = flash_times()
    # la Marina
    char(cv, "navy", 176, 264, t, scale=3, talk=talk_v(t, t_mar - 0.1 < t < t_frank - 0.2),
         arms="point" if t > t_perc - 0.1 else ("wave" if t_mar < t < t_mar + 0.9 else "down"),
         mood="happy" if t > t_perc else "neutral")
    if t_mar - 0.05 < t < t_frank - 0.1:
        a, dy = pop(t, t_mar - 0.05)
        window(cv, 112, 82 + dy, 128, 20)
        draw_text(cv, "MARINA DE EE.UU.", 176, 88 + dy, "press", 8, GOLD, align="center", alpha=a)
    # la máquina tapada / revelada
    rp = prog(t, t_perc - 0.05, t_perc + 0.45)
    if rp > 0:
        robot(cv, 258, 262, t, face="happy", scale=2)
        if rp < 1:
            pass
        else:
            for i in range(4):
                sparkle(cv, 232 + i * 18, 186 + (i % 2) * 22, t + i * 0.6, 3, GOLD)
    if rp < 1:
        lift = int(ease_in_out(rp) * 120)
        d = ImageDraw.Draw(cv)
        a = int(255 * (1 - rp))
        top = 176 - lift
        pts = [(226, 262 - lift), (230, top + 30), (244, top + 6), (258, top), (272, top + 6), (286, top + 30),
               (292, 262 - lift)]
        d.polygon(pts, fill=(222, 218, 206, a), outline=(*INK, a))
        for xx in (240, 256, 272):
            d.line([(xx, top + 16), (xx + (xx - 258) // 6, 258 - lift)], fill=(186, 180, 166, a))
        if rp == 0:
            draw_text(cv, "?", 258, 140, "press", 16, CYAN, align="center")
    # Rosenblatt
    if t > t_frank - 0.25:
        a, dy = pop(t, t_frank - 0.25)
        char(cv, "rosenblatt", 336, 264 + dy, t, scale=3, alpha=a,
             arms="wave" if t < t_frank + 1.0 else ("point_l" if t > t_perc - 0.1 else "down"),
             mood="happy", look=-1 if t > t_perc else 0)
    # periodista escribiendo
    char(cv, "reporter", 438, 266, t, scale=3, facing=-1, arms="write" if t > t_pre - 0.1 else "down",
         look=0, mood="happy" if t > t_perc else "neutral")
    # destellos de las cámaras
    for i, ft in enumerate(flashes):
        if ft <= t < ft + 0.18:
            k = 1 - (t - ft) / 0.18
            cx, cy = ((390, 95), (438, 100))[i % 2]
            d = ImageDraw.Draw(cv)
            r = int(6 + 10 * k)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 240, int(200 * k)))
            for ang in range(0, 360, 45):
                ln = r + 8
                d.line([(cx, cy), (cx + int(math.cos(math.radians(ang)) * ln),
                                   cy + int(math.sin(math.radians(ang)) * ln))], fill=(255, 255, 230, int(255 * k)))
    # textos
    year_big(cv, "1958", 240, 14, t, t0 + 0.02, t_frank - 0.6)
    name_card(cv, t, t_frank, t_perc - 0.15, "frank_rosenblatt", "FRANK ROSENBLATT", "PSICÓLOGO · 30 AÑOS · CORNELL")
    if t > t_perc - 0.05:
        a, dy = pop(t, t_perc - 0.05, 0.4)
        window(cv, 58, 10 + dy, 364, 34)
        draw_text(cv, "EL PERCEPTRÓN · 1958", 240, 20 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
    cv = vignette(cv, 0.35)
    return flash_white(cv, t, flashes, 0.12, 0.22)


def flash_times():
    w = TL.word
    t_pre = w("c2_01", "prensa")
    t_perc = w("c2_01", "perceptron")
    return [t_pre + 0.05, t_pre + 0.55, t_pre + 1.2, w("c2_01", "psicologo"), t_perc + 0.35, t_perc + 0.8]


def stage_floor(cv, top=206, col=(20, 22, 44), line=(40, 46, 86)):
    d = ImageDraw.Draw(cv)
    d.rectangle([0, top, W, H], fill=(*col, 255))
    for y in (top, top + 8, top + 20, top + 36, top + 56):
        d.line([(0, y), (W, y)], fill=(*line, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, top), (x, H)], fill=(*_lerp(col, line, 0.5), 255))


def sc_learn(t):
    """Una máquina que no se programa: aprende de sus errores."""
    cv = vgradient((8, 10, 26), (34, 40, 78), 14)
    stage_floor(cv)
    w = TL.word
    t_maq = w("c2_02", "maquina")
    t_no = w("c2_02", "no")
    t_prog = w("c2_02", "programa", end=True)
    t_apr = w("c2_02", "aprende")
    t_err = w("c2_02", "errores")
    tries = [t_apr + 0.05, t_apr + 0.45, t_err + 0.1]
    # programa tachado
    if t > t_maq - 0.2:
        a, dy = pop(t, t_maq - 0.2)
        x0, y0 = 34, 64 + dy
        draw_paper(cv, x0, y0, 116, 112)
        draw_text(cv, "PROGRAMA", x0 + 58, y0 + 8, "press", 8, INK, align="center", outline=None, shadow=False)
        code = ["10 LEER X", "20 SI X>5", "30 IR A 80", "40 SUMAR 1", "50 IMPRIMIR", "60 FIN"]
        for i, ln in enumerate(code):
            draw_text(cv, ln, x0 + 10, y0 + 24 + i * 13, "silk", 8, (60, 70, 110), outline=None, shadow=False)
        if t > t_no:
            p = prog(t, t_no, t_prog)
            d = ImageDraw.Draw(cv)
            chalk_line(d, (x0 + 6, y0 + 6), (x0 + 110, y0 + 106), p, RED, 4)
            chalk_line(d, (x0 + 110, y0 + 6), (x0 + 6, y0 + 106), prog(t, t_prog - 0.2, t_prog + 0.15), RED, 4)
            draw_text(cv, "NO SE PROGRAMA", x0 + 58, 190, "press", 8, CREAM, align="center",
                      reveal=(t - t_no) * 24)
    # tarjeta con la figura a reconocer
    if t > t_apr - 0.3:
        a, dy = pop(t, t_apr - 0.3)
        x0, y0 = 330, 56 + dy
        window(cv, x0, y0, 120, 96)
        d = ImageDraw.Draw(cv)
        d.polygon([(x0 + 60, y0 + 14), (x0 + 30, y0 + 70), (x0 + 90, y0 + 70)], fill=(*CYAN, 255),
                  outline=(*INK, 255))
        draw_text(cv, "¿QUÉ ES?", x0 + 60, y0 + 78, "press", 8, CREAM, align="center")
        # intentos
        shapes = ["sq", "circ", "tri"]
        for k, tt in enumerate(tries):
            if t < tt:
                continue
            bx, by = 316 + k * 50, 176
            window(cv, bx, by, 40, 40, fill=(26, 30, 60))
            col = (*GOLD, 255)
            if shapes[k] == "sq":
                d.rectangle([bx + 11, by + 11, bx + 29, by + 29], fill=col, outline=(*INK, 255))
            elif shapes[k] == "circ":
                d.ellipse([bx + 10, by + 10, bx + 30, by + 30], fill=col, outline=(*INK, 255))
            else:
                d.polygon([(bx + 20, by + 9), (bx + 9, by + 30), (bx + 31, by + 30)], fill=col, outline=(*INK, 255))
            if t > tt + 0.15:
                if k < 2:
                    mark_cross(cv, bx + 20, by + 50, 6)
                else:
                    mark_check(cv, bx + 20, by + 50, 8)
    # la máquina
    face = "happy"
    if t > t_apr - 0.3:
        face = "think"
    for k, tt in enumerate(tries[:2]):
        if tt + 0.15 < t < tt + 0.42:
            face = "sad"
    if t > tries[2] + 0.15:
        face = "happy"
    hop = int(abs(math.sin(t * 9)) * 8) if t > tries[2] + 0.15 else 0
    robot(cv, 236, 250 - hop, t, face=face, scale=3)
    if t > tries[2] + 0.15:
        for i in range(5):
            sparkle(cv, 196 + i * 20, 118 + (i % 2) * 16, t + i * 0.5, 3, GOLD)
    draw_text(cv, "APRENDE DE SUS ERRORES", 240, 16, "press", 16, align="center", gradient=GOLD_RAMP,
              reveal=(t - t_apr + 0.05) * 20)
    return vignette(cv, 0.3)


def newspaper(t):
    """Primera plana (imagen RGBA 320x210)."""
    PW, PH = 316, 206
    im = Image.new("RGBA", (PW + 4, PH + 4), (0, 0, 0, 0))
    draw_paper(im, 0, 0, PW, PH, color=(240, 232, 210))
    w = TL.word
    d = ImageDraw.Draw(im)
    ink = INK
    draw_text(im, "THE NEW YORK TIMES", PW // 2, 8, "press", 16, ink, align="center", outline=None, shadow=False)
    d.line([(6, 28), (PW - 6, 28)], fill=(*ink, 255))
    d.line([(6, 30), (PW - 6, 30)], fill=(*ink, 255))
    draw_text(im, "MARTES 8 DE JULIO DE 1958", 8, 33, "silk", 8, (80, 70, 60), outline=None, shadow=False)
    draw_text(im, "5 CENTAVOS", PW - 8, 33, "silk", 8, (80, 70, 60), align="right", outline=None, shadow=False)
    d.line([(6, 44), (PW - 6, 44)], fill=(*ink, 255))
    t_mar = w("c2_03", "Marina")
    t_que = w("c2_03", "que", occurrence=2)
    draw_text(im, "LA MARINA ESPERA", PW // 2, 52, "press", 16, ink, align="center", outline=None, shadow=False,
              reveal=(t - t_mar + 0.3) * 30)
    draw_text(im, "QUE PUEDA...", PW // 2, 72, "press", 16, ink, align="center", outline=None, shadow=False,
              reveal=(t - t_que + 0.1) * 24)
    d.line([(6, 92), (PW - 6, 92)], fill=(*ink, 255))
    # foto
    d.rectangle([10, 98, 92, 198], fill=(70, 60, 50, 255), outline=(*ink, 255))
    ph = Image.new("RGBA", (80, 100), (0, 0, 0, 0))
    robot(ph, 40, 92, t, face="happy", scale=2)
    ph = grade(ph, mul=SEPIA_MUL, sat=0.0)
    paste(im, ph, 11, 98)
    # lista
    items = [("CAMINAR", "caminar", 118, 104), ("HABLAR", "hablar", 216, 104), ("VER", "ver,", 118, 122),
             ("ESCRIBIR", "escribir", 216, 122)]
    for txt, key, x, y in items:
        tk = w("c2_03", key)
        d.rectangle([x - 14, y - 1, x - 5, y + 8], fill=(250, 246, 232, 255), outline=(*ink, 255))
        if t > tk:
            a, dy = pop(t, tk, 0.25)
            draw_text(im, txt, x, y + dy, "press", 8, ink, outline=None, shadow=False, alpha=a)
            d.line([(x - 12, y + 4), (x - 10, y + 6), (x - 6, y + 1)], fill=(40, 120, 60, 255), width=2)
    t_con = w("c2_03", "consciente")
    t_ser = w("c2_03", "ser")
    if t > t_ser - 0.05:
        draw_text(im, "Y SER", 102, 136, "press", 8, ink, outline=None, shadow=False)
    if t > t_con:
        a, dy = pop(t, t_con, 0.3)
        draw_text(im, "CONSCIENTE", 206, 154 + dy, "press", 16, (190, 30, 30), align="center", outline=None,
                  shadow=False, alpha=a)
        draw_text(im, "DE SU EXISTENCIA", 206, 176, "press", 8, ink, align="center", outline=None, shadow=False,
                  reveal=(t - w("c2_03", "de su")) * 30)
        p = prog(t, t_con + 0.25, t_con + 0.6)
        if p > 0:
            # círculo rojo de marcador
            pts = []
            n = int(48 * p)
            for k in range(n + 1):
                ang = -math.pi / 2 + k / 48 * 2 * math.pi * 1.04
                pts.append((206 + int(math.cos(ang) * 100), 166 + int(math.sin(ang) * 26)))
            if len(pts) > 1:
                d.line(pts, fill=(214, 40, 40, 255), width=2)
    return im


def sc_nyt(t):
    """Al día siguiente, The New York Times escribe..."""
    cv = vgradient((46, 30, 22), (14, 10, 10), 10)
    d = ImageDraw.Draw(cv)
    # pared con tramado de imprenta
    for y in range(0, 214, 6):
        for x in range((y // 6) % 2 * 3, W, 6):
            d.point((x, y), fill=(60, 42, 30, 255))
    d.rectangle([0, 214, W, H], fill=(54, 36, 26, 255))
    for y in (220, 232, 250):
        d.line([(0, y), (W, y)], fill=(40, 26, 20, 255))
    w = TL.word
    t0 = TL.s("c2_03")
    t_nyt = w("c2_03", "New")
    t_con = w("c2_03", "consciente")
    t_ex = w("c2_03", "existencia", end=True)
    land = t0 + 0.6
    p = prog(t, t0, land)
    char(cv, "reporter", 78, 266, t, scale=3, arms="point" if t > land else "down",
         mood="happy", talk=talk_v(t, t_nyt - 0.1 < t < t_nyt + 0.8), look=1 if t > land else 0)
    if p > 0:
        im = newspaper(t)
        if p < 1:
            s = 0.08 + 0.92 * ease_out(p)
            ang = (1 - p) * 720
            im = im.resize((max(2, int(im.size[0] * s)), max(2, int(im.size[1] * s))), Image.NEAREST)
            im = im.rotate(ang, resample=Image.NEAREST, expand=True)
        cx, cy = 312, 126
        paste(cv, im, cx - im.size[0] // 2, cy - im.size[1] // 2)
    if t > t_ex - 0.6:
        draw_text(cv, "— THE NEW YORK TIMES, 1958", 468, 244, "press", 8, CREAM, align="right",
                  reveal=(t - t_ex + 0.6) * 30)
    if t > t_con:
        for i in range(4):
            sparkle(cv, 220 + i * 60, 160 + (i % 2) * 40, t + i * 0.4, 3, GOLD)
    dx, dy = shake(t, land, 0.2, 3)
    sx, sy = shake(t, t_con, 0.25, 3)
    cv = offset_canvas(cv, dx + sx, dy + sy)
    return vignette(cv, 0.35)


def sc_lab(t):
    """La realidad era más modesta: veinte por veinte fotocélulas."""
    cv = bg("bg_perceptron_lab").copy()
    w = TL.word
    t0 = TL.s("c2_04")
    t_mod = w("c2_04", "modesta")
    t_per = w("c2_04", "perceptron")
    t_fig = w("c2_04", "figuras")
    t_sim = w("c2_04", "simples")
    t_cua = w("c2_04", "cuadricula")
    t_v1 = w("c2_04", "veinte")
    t_v2 = w("c2_04", "veinte", occurrence=2)
    t_foto = w("c2_04", "fotocelulas")
    draw_text(cv, "LA REALIDAD ERA MÁS MODESTA", 240, 10, "press", 8, CREAM, align="center",
              reveal=(t - t0) * 22, alpha=1 - prog(t, t_fig - 0.3, t_fig))
    char(cv, "rosenblatt", 86, 266, t, scale=3, arms="point" if t > t_per else "think",
         talk=0, mood="happy" if t > t_sim + 0.4 else "neutral", look=1 if t > t_per else 0)
    if t < t_per:
        a, dy = pop(t, t_mod - 0.1)
        if a > 0:
            bubble(cv, "...", 92, 112 + dy, size=16)
    if t > t_per - 0.1:
        a, dy = pop(t, t_per - 0.1, 0.4)
        x0, y0 = 168, 28 + dy
        lit, out = set(), None
        if t > t_fig:
            lit, out = TRI, (0 if t > t_fig + 0.35 else None)
        if t > t_sim + 0.35:
            lit, out = SQ, (1 if t > t_sim + 0.7 else None)
        if t > t_foto + 0.6:
            ph = int((t - t_foto - 0.6) / 1.1) % 2
            lit, out = (TRI, 0) if ph == 0 else (SQ, 1)
        on = 1.0
        scan = None
        if t_cua - 0.05 < t < t_cua + 0.7:
            scan = (t - t_cua + 0.05) / 0.75 * 20
        # haz de la cámara hacia la retina
        d = ImageDraw.Draw(cv)
        if t > t_fig - 0.2:
            for k in range(0, 8):
                yy = 70 + k * 14
                d.line([(424, 106), (395, yy)], fill=(140, 220, 255, 60))
        mark1_panel(cv, x0, y0, t, lit, on, out, scan)
        gx, gy = x0 + 22, y0 + 32
        # etiquetas 20 x 20
        if t > t_v1:
            a1, d1 = pop(t, t_v1)
            d.line([(gx, gy - 6), (gx + 138, gy - 6)], fill=(*GOLD, 255))
            d.line([(gx, gy - 9), (gx, gy - 3)], fill=(*GOLD, 255))
            d.line([(gx + 138, gy - 9), (gx + 138, gy - 3)], fill=(*GOLD, 255))
            d.rectangle([gx + 56, gy - 14, gx + 82, gy - 1], fill=(30, 36, 44, 255))
            draw_text(cv, "20", gx + 69, gy - 11 + d1, "press", 8, GOLD, align="center", alpha=a1)
        if t > t_v2:
            a2, d2 = pop(t, t_v2)
            d.line([(gx - 8, gy), (gx - 8, gy + 138)], fill=(*GOLD, 255))
            d.line([(gx - 11, gy), (gx - 5, gy)], fill=(*GOLD, 255))
            d.line([(gx - 11, gy + 138), (gx - 5, gy + 138)], fill=(*GOLD, 255))
            d.rectangle([gx - 21, gy + 62, gx - 2, gy + 76], fill=(30, 36, 44, 255))
            draw_text(cv, "20", gx - 11, gy + 65 + d2, "press", 8, GOLD, align="center", alpha=a2)
        if t > t_foto:
            draw_text(cv, "= 400 FOTOCÉLULAS", x0 + 92, y0 + 178, "press", 8, CYAN, align="center",
                      reveal=(t - t_foto) * 30)
    return vignette(cv, 0.35)


def sc_net(t):
    """Pero la idea era enorme: una red de neuronas artificiales que ajusta sus conexiones."""
    cv = vgradient((4, 6, 16), (18, 22, 50), 12)
    STARS.draw(cv, t * 0.5, alpha=0.5)
    w = TL.word
    t_idea = w("c2_05", "idea")
    t_red = w("c2_05", "red")
    t_neu = w("c2_05", "neuronas")
    t_art = w("c2_05", "artificiales")
    t_aj = w("c2_05", "ajusta")
    t_exp = w("c2_05", "experiencia")
    show = (prog(t, t_red - 0.1, t_red + 0.4), prog(t, t_neu - 0.05, t_neu + 0.35), prog(t, t_art, t_art + 0.3))
    adapt = ease_in_out(prog(t, t_aj - 0.1, t_aj + 0.6))
    pulse = prog(t, t_exp - 0.6, t_exp - 0.2)
    win = 0 if t > t_exp + 0.2 else None
    # la idea: una bombita enorme que estalla en la red
    t_eno = w("c2_05", "enorme")
    if t_idea - 0.3 < t < t_red + 0.35:
        k = 2 if t < t_idea + 0.25 else (3 if t < t_eno else 5)
        tmp = Image.new("RGBA", (28, 28), (0, 0, 0, 0))
        bulb(tmp, 14, 15, t, prog(t, t_idea - 0.1, t_idea + 0.3))
        big = Image.fromarray(upscale(np.array(tmp), k), "RGBA")
        a = prog(t, t_idea - 0.3, t_idea) * (1 - prog(t, t_red - 0.1, t_red + 0.35))
        paste(cv, big, 240 - 14 * k, 148 - 15 * k, a)
        if t > t_eno:
            for i in range(8):
                ang = i * math.pi / 4 + t
                sparkle(cv, 240 + int(math.cos(ang) * 92), 148 + int(math.sin(ang) * 72), t + i, 4, GOLD)
    # retina de entrada
    if show[0] > 0:
        d = ImageDraw.Draw(cv)
        a = show[0]
        gx, gy = 30, 122
        d.rectangle([gx - 3, gy - 3, gx + 8 * 6 + 1, gy + 8 * 6 + 1], fill=(10, 14, 18, 255), outline=(*GREY, 255))
        for r in range(8):
            for c in range(8):
                on = r >= 1 and abs(c - 3.5) <= (r - 1) * 0.6
                d.rectangle([gx + c * 6, gy + r * 6, gx + c * 6 + 4, gy + r * 6 + 4],
                            fill=(*(CYAN if on else (44, 56, 64)), 255))
        for y in NET[0][1]:
            chalk_line(d, (gx + 50, gy + 24), (NET[0][0] - 8, y), a, (50, 70, 100))
    draw_net(cv, t, show, adapt=adapt, pulse=pulse, win=win)
    # salidas
    if show[2] >= 1:
        d = ImageDraw.Draw(cv)
        c1 = (*(GOLD if win == 0 else GREY), 255)
        d.polygon([(400, 106), (392, 124), (408, 124)], fill=c1, outline=(*INK, 255))
        d.rectangle([392, 178, 408, 194], fill=(*GREY, 255), outline=(*INK, 255))
        if win == 0:
            mark_check(cv, 432, 114, 9)
            for i in range(3):
                sparkle(cv, 388 + i * 22, 96 + (i % 2) * 34, t + i, 3, GOLD)
    # números de pesos que cambian
    if adapt > 0:
        for k, (L, i, j, a, b, w0, ph) in enumerate(EDGES[::7]):
            wv = max(-1, min(1, w0 + adapt * 0.9 * math.sin(t * 3.2 + ph * 6)))
            mx, my = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
            draw_text(cv, f"{wv:+.1f}", mx, my - 4, "silk", 8, CYAN if wv > 0 else (240, 150, 70), align="center")
    draw_text(cv, "LA IDEA ERA ENORME", 240, 12, "press", 16, align="center", gradient=GOLD_RAMP,
              reveal=(t - t_idea + 0.2) * 24)
    draw_text(cv, "RED DE NEURONAS ARTIFICIALES", 240, 36, "press", 8, CYAN, align="center",
              reveal=(t - t_red) * 26)
    draw_text(cv, "QUE AJUSTA SUS CONEXIONES CON LA EXPERIENCIA", 240, 250, "press", 8, CREAM, align="center",
              reveal=(t - t_aj + 0.2) * 30)
    return vignette(cv, 0.3)


def perceptrons_book(cv, x0, y0, t):
    """Tapa del libro Perceptrons (100x124)."""
    d = ImageDraw.Draw(cv)
    bw, bh = 100, 124
    d.rectangle([x0 + 4, y0 + 4, x0 + bw + 4, y0 + bh + 4], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(176, 40, 36, 255), outline=(*INK, 255))
    d.rectangle([x0 + 1, y0 + 1, x0 + 6, y0 + bh - 1], fill=(130, 26, 26, 255))
    # espiral cuadrada (laberinto de la tapa)
    cx, cy = x0 + 53, y0 + 72
    pts = [(cx, cy)]
    x, y, step = cx, cy, 4
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for k in range(14):
        dx, dy = dirs[k % 4]
        x += dx * step
        y += dy * step
        pts.append((x, y))
        if k % 2 == 1:
            step += 4
    d.line(pts, fill=(20, 12, 12, 255), width=2)
    d.rectangle([x0 + 8, y0 + 8, x0 + bw - 4, y0 + 26], fill=(20, 12, 12, 255))
    draw_text(cv, "PERCEPTRONS", x0 + 53, y0 + 13, "press", 8, CREAM, align="center", outline=None, shadow=False)
    draw_text(cv, "MINSKY · PAPERT", x0 + 53, y0 + bh - 14, "silk", 8, CREAM, align="center", outline=None,
              shadow=False)


def sc_mit(t):
    """1969: Minsky y Papert publican Perceptrons."""
    cv = bg("bg_mit_office_1969").copy()
    w = TL.word
    t0 = TL.s("c2_06")
    t_min = w("c2_06", "Marvin")
    t_pap = w("c2_06", "Seymour")
    t_lib = w("c2_06", "libro")
    t_per = w("c2_06", "Perceptrons")
    land = t_per
    x, ph = walk(t, t_min - 0.7, t_min, -40, 96)
    char(cv, "minsky", x, 266, t, walk=ph, scale=3, arms="point" if t > land else ("wave" if t_min < t < t_min + 0.8 else "down"),
         mood="happy" if t > t_min else "neutral", look=1 if t > t_lib else 0)
    if t > t_pap - 0.8:
        x2, ph2 = walk(t, t_pap - 0.8, t_pap, 330, 210)
        char(cv, "papert", x2, 266, t, walk=ph2, scale=3, facing=-1 if ph2 is not None else 1,
             arms="cross" if t > land else ("wave" if t_pap < t < t_pap + 0.8 else "down"),
             mood="happy", look=1 if t > t_lib else 0)
    # libro que cae sobre el escritorio
    if t > t_lib + 0.1:
        p = prog(t, t_lib + 0.1, land)
        yy = int(40 - (1 - p * p) * 190)
        perceptrons_book(cv, 352, yy, t)
        if t > land:
            for i in range(3):
                sparkle(cv, 360 + i * 40, 50 + (i % 2) * 70, t + i, 3, GOLD)
            # polvo del golpe
            k = prog(t, land, land + 0.5)
            if k < 1:
                d = ImageDraw.Draw(cv)
                for s in (-1, 1):
                    for j in range(3):
                        px_ = 402 + s * int(56 + k * 30 + j * 8)
                        py_ = 164 - int(k * 10) - j * 3
                        d.rectangle([px_, py_, px_ + 2, py_ + 2], fill=(230, 220, 200, int(220 * (1 - k))))
    year_big(cv, "1969", 240, 14, t, t0 + 0.02, t_lib - 0.2)
    lower_third(cv, "MINSKY Y PAPERT", "MIT · 1969", t, t_min - 0.1, TL.e("c2_06") + 0.4, x=26, y=226)
    dx, dy = shake(t, land, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


def sc_xor(t):
    """Una red de una sola capa no puede resolver el o exclusivo."""
    cv = bg("bg_mit_office_1969").copy()
    cv = grade(cv, mul=(0.75, 0.72, 0.7))
    w = TL.word
    t0 = TL.s("c2_07")
    t_una = w("c2_07", "una")
    t_capa = w("c2_07", "capa", end=True)
    t_no = w("c2_07", "no")
    t_prob = w("c2_07", "problemas")
    t_tan = w("c2_07", "tan")
    t_o = w("c2_07", "o exclusivo")
    t_x = TL.e("c2_07") - 0.6
    d = ImageDraw.Draw(cv)
    # pizarrón
    bx0, by0, bx1, by1 = 168, 12, 472, 224
    d.rectangle([bx0 - 5, by0 - 5, bx1 + 5, by1 + 5], fill=(110, 72, 44, 255), outline=(*INK, 255))
    d.rectangle([bx0, by0, bx1, by1], fill=(36, 66, 52, 255), outline=(*INK, 255))
    for i in range(70):
        xx = bx0 + 4 + (i * 97) % (bx1 - bx0 - 8)
        yy = by0 + 4 + (i * 53) % (by1 - by0 - 8)
        d.point((xx, yy), fill=(60, 92, 76, 255))
    d.rectangle([bx0 + 30, by1 + 1, bx1 - 30, by1 + 5], fill=(140, 96, 60, 255), outline=(*INK, 255))
    # red de una sola capa
    p = prog(t, t_una - 0.1, t_capa)
    ins = [(198, 70), (198, 130)]
    out = (266, 100)
    for k, a in enumerate(ins):
        chalk_line(d, a, out, prog(p, 0.2 + k * 0.2, 0.7 + k * 0.2) if p < 1 else 1)
        if p > k * 0.2:
            d.ellipse([a[0] - 7, a[1] - 7, a[0] + 7, a[1] + 7], fill=(36, 66, 52, 255), outline=(*CHALK, 255))
            draw_text(cv, "AB"[k], a[0] - 17, a[1] - 4, "press", 8, CHALK, outline=None, shadow=False)
    if p > 0.6:
        d.ellipse([out[0] - 9, out[1] - 9, out[0] + 9, out[1] + 9], fill=(36, 66, 52, 255), outline=(*CHALK, 255))
        chalk_line(d, (out[0] + 9, out[1]), (out[0] + 30, out[1]), prog(p, 0.7, 1.0))
    if t > t_capa - 0.4:
        draw_text(cv, "1 SOLA CAPA", 230, 150, "press", 8, CHALK, align="center", outline=None, shadow=False,
                  reveal=(t - t_capa + 0.4) * 24)
    if t > t_no:
        draw_text(cv, "NO PUEDE:", 230, 172, "press", 8, (255, 140, 120), align="center", outline=None,
                  shadow=False, reveal=(t - t_no) * 20)
    # gráfico XOR
    ox, oy = 322, 176
    if t > t_prob - 0.3:
        pa = prog(t, t_prob - 0.3, t_prob + 0.1)
        chalk_line(d, (ox, oy), (458, oy), pa)
        chalk_line(d, (ox, oy), (ox, 36), pa)
        draw_text(cv, "0", ox + 18, oy + 4, "silk", 8, CHALK, outline=None, shadow=False)
        draw_text(cv, "1", ox + 114, oy + 4, "silk", 8, CHALK, outline=None, shadow=False)
        draw_text(cv, "1", ox - 10, oy - 120, "silk", 8, CHALK, outline=None, shadow=False)
    pts = [((340, 158), CYAN), ((436, 58), CYAN), ((340, 58), GOLD), ((436, 158), GOLD)]
    for k, ((px_, py_), col) in enumerate(pts):
        tk = t_prob + 0.1 + k * 0.12
        if t > tk:
            a, dy = pop(t, tk, 0.25)
            d.ellipse([px_ - 7, py_ - 7 + dy, px_ + 7, py_ + 7 + dy], fill=(*col, 255), outline=(*INK, 255))
            d.point((px_ - 2, py_ - 3 + dy), fill=(255, 255, 255, 255))
    # la línea que intenta separarlos
    if t_tan < t < t_x + 0.4:
        sp = prog(t, t_tan, t_x - 0.1)
        ang = math.radians(-70 + 250 * ease_in_out(sp))
        cx_, cy_ = 388, 108
        L = 90
        a = (int(cx_ - math.cos(ang) * L), int(cy_ - math.sin(ang) * L))
        b = (int(cx_ + math.cos(ang) * L), int(cy_ + math.sin(ang) * L))
        bad = int(t * 8) % 2 == 0
        d2 = ImageDraw.Draw(cv)
        d2.line([a, b], fill=(*((255, 120, 100) if bad else (255, 230, 140)), 255), width=2)
    if t > t_x:
        mark_cross(cv, 388, 108, 46)
    if t > t_o:
        a, dy = pop(t, t_o)
        draw_text(cv, "O EXCLUSIVO (XOR)", 390, 198 + dy, "press", 8, align="center", gradient=GOLD_RAMP,
                  alpha=a)
    # personajes
    char(cv, "papert", 46, 266, t, scale=3, arms="cross", look=1, mood="neutral")
    talk = t0 < t < t_capa or t_no < t < t_o + 0.6
    char(cv, "minsky", 126, 266, t, scale=3, arms="point", talk=talk_v(t, talk), look=1,
         mood="happy" if t > t_x else "neutral")
    dx, dy = shake(t, t_x, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


def sc_collapse(t):
    """El golpe es devastador. El dinero para redes neuronales se evapora."""
    cv = vgradient((6, 6, 14), (24, 22, 40), 12)
    w = TL.word
    t_gol = w("c2_08", "golpe")
    t_dev = w("c2_08", "devastador")
    t_din = w("c2_08", "dinero")
    t_ev = w("c2_08", "evapora")
    t_end = TL.e("c2_08")
    n = len(NODE_IDS)
    off0, off1 = t_din + 0.2, t_end + 0.1

    def alive(L, i):
        idx = NODE_IDS.index((L, i))
        order = (idx * 7) % n
        return 1 - prog(t, off0 + order * (off1 - off0) / n, off0 + (order + 0.6) * (off1 - off0) / n)

    draw_net(cv, t, (1, 1, 1), adapt=0.2, alive=alive, crack=prog(t, t_dev, t_dev + 0.4) * (1 - prog(t, t_din, t_din + 0.5)))
    # el libro aplasta la red
    if t < t_din + 0.4:
        p = prog(t, t_gol - 0.3, t_gol)
        a_out = 1 - prog(t, t_din - 0.2, t_din + 0.3)
        yy = int(70 - (1 - p * p) * 220)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        perceptrons_book(im, 190, yy, t)
        paste(cv, im, 0, 0, a_out)
    if t > t_dev:
        a = prog(t, t_dev, t_dev + 0.2) * (1 - prog(t, t_din - 0.2, t_din + 0.2))
        draw_text(cv, "¡DEVASTADOR!", 240, 234, "press", 16, RED, align="center", alpha=a)
    # fondos
    if t > t_din - 0.3:
        a, dy = pop(t, t_din - 0.3)
        window(cv, 104, 8 + dy, 272, 38)
        draw_text(cv, "FONDOS · REDES NEURONALES", 240, 14 + dy, "press", 8, CREAM, align="center")
        d = ImageDraw.Draw(cv)
        fill = 1 - ease_in_out(prog(t, t_ev - 0.3, t_end))
        d.rectangle([116, 28 + dy, 364, 37 + dy], fill=(10, 10, 20, 255), outline=(*INK, 255))
        col = GOLD if fill > 0.5 else ((255, 90, 70) if int(t * 8) % 2 else (150, 50, 40))
        if fill > 0.01:
            d.rectangle([117, 29 + dy, 117 + int(246 * fill), 36 + dy], fill=(*col, 255))
        # bolsa de dinero
        bag_a = 1 - prog(t, t_ev + 0.3, t_end + 0.3)
        money_bag(cv, 54, 236, a * max(0.0, bag_a))
        # monedas que se evaporan
        if t > t_ev - 0.4:
            d = ImageDraw.Draw(cv)
            for k in range(9):
                st = t_ev - 0.4 + k * 0.12
                q = prog(t, st, st + 1.2)
                if 0 < q < 1:
                    cx = 54 + int(math.sin(k * 2.1 + q * 6) * 14) + (k % 3 - 1) * 10
                    cy = 180 - int(q * 120)
                    if q < 0.5:
                        coin_px(d, cx, cy, int(255 * (1 - q)))
                    else:
                        for j in range(3):
                            d.point((cx + j * 3 - 3, cy - j * 2), fill=(200, 210, 230, int(255 * (1 - q))))
    # la máquina triste
    if t > t_gol + 0.3:
        a = prog(t, t_gol + 0.3, t_gol + 0.6)
        robot(cv, 428, 254, t, face="sad" if t < t_end else "off", alpha=a, scale=2)
    k = prog(t, t_din, t_end + 0.2)
    if k > 0:
        cv = grade(cv, mul=(0.85, 0.9, 1.05), sat=0.4, k=k * 0.8)
    dx, dy = shake(t, t_gol, 0.35, 5)
    cv = offset_canvas(cv, dx, dy)
    for ft in (t_gol,):
        if ft <= t < ft + 0.18:
            cv = fade_to(cv, (200, 30, 30), 0.4 * (1 - (t - ft) / 0.18))
    return vignette(cv, 0.4)


_DUST = [((i * 73) % 480, (i * 41) % 270, 0.3 + (i * 37 % 10) / 14, i * 0.7) for i in range(60)]


def cobweb(cv, cx, cy, r, sx, sy, p, col=(200, 200, 210)):
    """Telaraña en una esquina (sx, sy = dirección hacia adentro)."""
    if p <= 0:
        return
    d = ImageDraw.Draw(cv)
    rr = r * p
    a = int(170 * min(1, p * 1.5))
    angs = [0, 22, 45, 68, 90]
    spokes = []
    for ag in angs:
        ex = cx + sx * int(math.cos(math.radians(ag)) * rr)
        ey = cy + sy * int(math.sin(math.radians(ag)) * rr)
        spokes.append((ex, ey))
        d.line([(cx, cy), (ex, ey)], fill=(*col, a))
    for ring in (0.35, 0.6, 0.85):
        pts = [(cx + int((ex - cx) * ring), cy + int((ey - cy) * ring)) for ex, ey in spokes]
        d.line(pts, fill=(*col, a))


def sc_dust(t):
    """La idea que hoy mueve todo pasa a ser, durante años, una curiosidad abandonada."""
    w = TL.word
    t0 = TL.s("c2_09")
    t_hoy = w("c2_09", "hoy")
    t_pasa = w("c2_09", "pasa")
    t_dur = w("c2_09", "durante")
    t_cur = w("c2_09", "curiosidad")
    t_ab = w("c2_09", "abandonada")
    old = ease_in_out(prog(t, t_pasa - 0.2, t_dur + 0.6))
    cv = bg("bg_perceptron_lab").copy()
    cv = grade(cv, mul=(0.55, 0.52, 0.5), add=(6, 4, 2), sat=0.35, k=0.5 + 0.5 * old)
    # panel: brilla "hoy" y después se apaga
    glow = 1 - old
    lit = TRI if int(t * 2) % 2 == 0 else SQ
    x0, y0 = 52, 52
    mark1_panel(cv, x0, y0, t, lit, on=glow, out=(0 if lit is TRI else 1) if glow > 0.5 else None, dead=old,
                title=True)
    # polvo acumulado sobre el panel
    if old > 0:
        a = np.array(cv)
        th = bayer_tile(W, H)
        sub = a[y0:y0 + 196, x0:x0 + 240]
        m = th[y0:y0 + 196, x0:x0 + 240] < 0.28 * old
        sub[m, :3] = (sub[m, :3] * 0.5 + np.array([150, 140, 120]) * 0.5).astype(np.uint8)
        a[y0:y0 + 196, x0:x0 + 240] = sub
        cv = Image.fromarray(a, "RGBA")
    cw = prog(t, t_dur - 0.4, t_cur + 0.4)
    cobweb(cv, x0 + 1, y0 + 1, 34, 1, 1, cw)
    cobweb(cv, x0 + 239, y0 + 1, 28, -1, 1, prog(t, t_dur, t_cur + 0.8))
    cobweb(cv, 0, 0, 46, 1, 1, cw)
    cobweb(cv, 479, 0, 40, -1, 1, cw)
    # polvo flotando
    d = ImageDraw.Draw(cv)
    if old > 0:
        for (x, y, s, ph) in _DUST:
            xx = int(x + math.sin(t * 0.7 + ph) * 8) % W
            yy = int(y - t * 6 * s) % H
            d.point((xx, yy), fill=(220, 210, 180, int(200 * old)))
    # calendario que pasa
    if t > t_dur - 0.2:
        a, dy = pop(t, t_dur - 0.2)
        cx0, cy0 = 330, 52 + dy
        draw_paper(cv, cx0, cy0, 64, 58)
        d = ImageDraw.Draw(cv)
        d.rectangle([cx0 + 1, cy0 + 1, cx0 + 63, cy0 + 13], fill=(160, 60, 50, 255))
        draw_text(cv, "AÑO", cx0 + 32, cy0 + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        yr = 1969 + int(ease_in_out(prog(t, t_dur, t_ab + 0.5)) * 13)
        draw_text(cv, str(yr), cx0 + 32, cy0 + 26, "press", 8, INK, align="center", outline=None, shadow=False)
    # la máquina, sola
    robot(cv, 384, 262, t, face="sad" if t > t_pasa else "happy", scale=3)
    if t < t_pasa + 0.3:
        a = 1 - prog(t, t_pasa, t_pasa + 0.3)
        draw_text(cv, "LA IDEA QUE HOY MUEVE TODO", 240, 18, "press", 8, CYAN, align="center", alpha=a,
                  reveal=(t - t0) * 26)
    if t > t_cur - 0.4:
        draw_text(cv, "UNA CURIOSIDAD", 240, 10, "press", 16, CREAM, align="center", reveal=(t - t_cur + 0.4) * 22)
        draw_text(cv, "ABANDONADA", 240, 30, "press", 16, GREY, align="center", reveal=(t - t_ab + 0.1) * 22)
    return vignette(cv, 0.5)


# =========================================================================== montaje


def cam_xor(t):
    w = TL.word
    z, cx, cy = cam_push(t, w("c2_07", "problemas") - 0.3, w("c2_07", "exclusivo"), 1.0, 1.18, (240, 135),
                         (360, 120))
    return z + cam_punch(t, [TL.e("c2_07") - 0.6], 0.08), cx, cy


def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (TL.chapter_start(2) - 0.3, make_card(2, ["LA MÁQUINA QUE", "IBA A SER CONSCIENTE"], "1958 – 1969"), None),
        (s("c2_01") - 0.2, sc_press,
         lambda t: (cam_push(t, s("c2_01"), w("c2_01", "Frank"), 1.06, 1.0, (240, 150))[0]
                    + cam_punch(t, flash_times(), 0.03), 240, 150)),
        (s("c2_02") - 0.2, sc_learn,
         lambda t: (1.0 + cam_punch(t, [w("c2_02", "errores") + 0.25], 0.08), 240, 135)),
        (s("c2_03") - 0.2, sc_nyt,
         lambda t: (1.0 + cam_punch(t, [w("c2_03", k) for k in ("caminar", "hablar", "ver,", "escribir")], 0.025)
                    + cam_punch(t, [w("c2_03", "consciente")], 0.1), 300, 150)),
        (s("c2_04") - 0.2, sc_lab,
         lambda t: cam_push(t, w("c2_04", "perceptron"), w("c2_04", "fotocelulas"), 1.0, 1.15, (240, 135), (280, 130))),
        (s("c2_05") - 0.2, sc_net,
         lambda t: (1.0 + cam_punch(t, [w("c2_05", "enorme")], 0.08)
                    + cam_punch(t, [w("c2_05", k) for k in ("red", "neuronas", "artificiales")], 0.03)
                    + cam_punch(t, [w("c2_05", "experiencia") + 0.2], 0.05), 240, 140)),
        (s("c2_06") - 0.2, sc_mit,
         lambda t: (1.0 + cam_punch(t, [w("c2_06", "Perceptrons")], 0.05), 260, 135)),
        (s("c2_07") - 0.2, sc_xor,
         cam_xor),
        (s("c2_08") - 0.2, sc_collapse,
         lambda t: (1.0 + cam_punch(t, [w("c2_08", "golpe")], 0.12), 240, 135)),
        (s("c2_09") - 0.2, sc_dust,
         lambda t: cam_push(t, s("c2_09"), e("c2_09") + 0.4, 1.0, 1.05, (240, 135), (240, 135))),
    ]


# =========================================================================== audio


def music(A):
    s, e, w = TL.s, TL.e, TL.word
    t0 = TL.chapter_start(2) + 1.6
    t_end = TL.chapter_start(3) - 0.25
    A.section(t0, s("c2_02") - 0.2, 104, [("C", "maj"), ("A", "min"), ("F", "maj"), ("G", "maj")], A.st_build)
    A.section(s("c2_02") - 0.2, s("c2_04") - 0.2, 110, [("F", "maj"), ("G", "maj"), ("E", "min"), ("A", "min")],
              A.st_bright)
    A.section(s("c2_04") - 0.2, s("c2_05") - 0.2, 100, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")],
              A.st_puzzle)
    A.section(s("c2_05") - 0.2, s("c2_06") - 0.2, 108, [("F", "maj7"), ("G", "maj"), ("C", "maj"), ("A", "min")],
              A.st_triumph)
    A.section(s("c2_06") - 0.2, w("c2_08", "golpe"), 92, [("D", "min"), ("Bb", "maj"), ("G", "min"), ("A", "maj")],
              A.st_mystery)
    # golpe devastador
    tg = w("c2_08", "golpe")
    A.kick(A.music, tg, 0.5)
    A.crash(A.music, tg, 0.14)
    for m in A.chord_notes("D", "min", 2):
        A.note(A.music, tg, A.midi_hz(m), 1.6, "tri" if m == A.chord_notes("D", "min", 2)[0] else "pulse",
               vol=0.25 if m == A.chord_notes("D", "min", 2)[0] else 0.035, s=0.8, r=0.6)
    A.section(tg + 0.7, t_end, 70, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "min")], A.st_winter)
    # final melancólico
    A.sting(e("c2_09") - 0.6, [76, 74, 72, 69], inst_duty=0.125, vol=0.035, step=0.22, hold=1.0)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    # prensa
    A.whoosh(s("c2_01") - 0.2, 0.3, 0.04)
    A.pop_sfx(s("c2_01") + 0.05, 420, 0.06)
    A.pop_sfx(w("c2_01", "Marina") - 0.05, 650, 0.04)
    for ft in flash_times():
        A.pop_sfx(ft, 900, 0.05)
        A.blip(ft + 0.02, 2600, 0.04, 0.03)
    A.typewriter(w("c2_01", "prensa") + 0.1, w("c2_01", "Frank") - 0.3, 10, 0.025)
    A.join_jingle(w("c2_01", "Frank") - 0.1)
    A.whoosh(w("c2_01", "perceptron") - 0.1, 0.4, 0.05)
    A.coin(w("c2_01", "perceptron") + 0.3, 0.05)
    A.robot_beep(w("c2_01", "perceptron") + 0.5, 0.04)
    # aprende de sus errores
    A.robot_beep(w("c2_02", "maquina"), 0.035)
    A.pop_sfx(w("c2_02", "maquina") - 0.2, 500, 0.04)
    A.whoosh(w("c2_02", "no"), 0.25, 0.04)
    t_apr, t_err = w("c2_02", "aprende"), w("c2_02", "errores")
    for k, tt in enumerate([t_apr + 0.05, t_apr + 0.45]):
        A.pop_sfx(tt, 600, 0.04)
        A.note(A.sfx, tt + 0.15, 150, 0.16, duty=0.5, vol=0.05, s=0.8, r=0.02)
    A.pop_sfx(t_err + 0.1, 700, 0.04)
    A.coin(t_err + 0.25, 0.06)
    A.text_blips(t_apr, 22, 20, 0.018)
    # New York Times
    t0 = s("c2_03")
    A.whoosh(t0, 0.6, 0.07)
    A.kick(A.sfx, t0 + 0.6, 0.3)
    A.typewriter(w("c2_03", "Marina") - 0.3, w("c2_03", "pueda") + 0.3, 14, 0.035)
    for k in ("caminar", "hablar", "ver,", "escribir"):
        A.pop_sfx(w("c2_03", k), 700, 0.05)
    A.kick(A.sfx, w("c2_03", "consciente"), 0.35)
    A.pop_sfx(w("c2_03", "consciente"), 380, 0.06)
    A.text_blips(e("c2_03") - 0.6, 26, 30, 0.015, 1800)
    # laboratorio
    A.text_blips(s("c2_04"), 27, 22, 0.016)
    A.pop_sfx(w("c2_04", "perceptron") - 0.1, 450, 0.05)
    for k in ("figuras", "simples"):
        tt = w("c2_04", k) + (0.35 if k == "simples" else 0)
        for i in range(5):
            A.blip(tt + i * 0.03, 900 + i * 150, 0.02, 0.025)
    A.blip(w("c2_04", "figuras") + 0.35, 1400, 0.08, 0.04)
    A.blip(w("c2_04", "simples") + 0.7, 1400, 0.08, 0.04)
    for i in range(10):
        A.blip(w("c2_04", "cuadricula") + i * 0.07, 600 + i * 40, 0.02, 0.02, 0.125)
    A.pop_sfx(w("c2_04", "veinte"), 650, 0.05)
    A.pop_sfx(w("c2_04", "veinte", occurrence=2), 750, 0.05)
    A.text_blips(w("c2_04", "fotocelulas"), 17, 30, 0.016)
    # red neuronal
    A.text_blips(w("c2_05", "idea") - 0.2, 18, 24, 0.018)
    for L, key in enumerate(("red", "neuronas", "artificiales")):
        nn = len(NET[L][1])
        for i in range(nn):
            A.blip(w("c2_05", key) + i * 0.06, 700 + L * 300 + i * 60, 0.03, 0.03)
    A.whoosh(w("c2_05", "ajusta"), 0.5, 0.04)
    A.coin(w("c2_05", "experiencia") + 0.25, 0.05)
    # Minsky y Papert
    A.pop_sfx(s("c2_06") + 0.05, 420, 0.06)
    A.join_jingle(w("c2_06", "Marvin") - 0.1, 0.05)
    A.join_jingle(w("c2_06", "Seymour") - 0.1, 0.05)
    A.whoosh(w("c2_06", "libro") + 0.1, 0.5, 0.05)
    A.kick(A.sfx, w("c2_06", "Perceptrons"), 0.45)
    A.snare(A.sfx, w("c2_06", "Perceptrons"), 0.12)
    # XOR
    A.chalk(w("c2_07", "una") - 0.1, w("c2_07", "capa", end=True))
    A.chalk(w("c2_07", "no") + 0.3, w("c2_07", "problemas"))
    for k in range(4):
        A.pop_sfx(w("c2_07", "problemas") + 0.1 + k * 0.12, 600 + k * 70, 0.04)
    tx = e("c2_07") - 0.6
    tt = w("c2_07", "tan")
    while tt < tx:
        A.note(A.sfx, tt, 180, 0.07, duty=0.5, vol=0.03, s=0.7, r=0.01)
        tt += 0.25
    A.kick(A.sfx, tx, 0.4)
    A.note(A.sfx, tx, 110, 0.3, duty=0.5, vol=0.05, s=0.8, r=0.1)
    # el golpe
    tg = w("c2_08", "golpe")
    A.whoosh(tg - 0.3, 0.3, 0.07)
    A.kick(A.sfx, tg, 0.5)
    A.crash(A.sfx, tg, 0.12)
    A.coin(w("c2_08", "dinero") - 0.1, 0.05)
    t_ev = w("c2_08", "evapora")
    for k in range(9):
        A.blip(t_ev - 0.4 + k * 0.12, 1600 - k * 120, 0.05, 0.03, 0.25)
    n = len(NODE_IDS)
    off0, off1 = w("c2_08", "dinero") + 0.2, e("c2_08") + 0.1
    for o in range(n):
        A.blip(off0 + (o + 0.3) * (off1 - off0) / n, 500 - o * 25, 0.04, 0.02, 0.5)
    # polvo
    A.whoosh(s("c2_09") - 0.2, 0.8, 0.03)
    A.text_blips(s("c2_09"), 26, 26, 0.014, 1300)
    for i in range(6):
        A.blip(w("c2_09", "durante") + i * 0.3, 900, 0.02, 0.02)
    A.wind(w("c2_09", "pasa"), TL.chapter_start(3) - 0.2, 0.025)
