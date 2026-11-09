"""Capítulo 8: El verano que no terminó (2024 – hoy) + final del video."""
from common import *  # noqa

w = TL.word
CH = 8
T_CARD = TL.chapter_start(CH)
T_END = TL.e("c8_08") + 2.8

S1 = TL.s("c8_01") - 0.2                    # Nobel de Física
S2 = TL.s("c8_03") - 0.2                    # Nobel de Química
S3 = w("c8_03", "su sistema") - 0.25        # AlphaFold
S4 = TL.s("c8_04") - 0.2                    # las tres edades de Hinton
S5 = TL.s("c8_05") - 0.2                    # hoy, las máquinas...
S6 = TL.s("c8_06") - 0.2                    # setenta años después
S7 = TL.s("c8_07") - 0.3                    # la pregunta sigue abierta
S8 = TL.s("c8_08") - 0.35                   # amanecer + título final

MEDAL_RIM = (150, 96, 44)
MEDAL = (236, 190, 84)
MEDAL_HI = (255, 236, 160)
MEDAL_D = (196, 136, 62)
GLOW = (109, 252, 154)
_CACHE = {}


# =========================================================================== helpers

def medal(cv, cx, cy, r, t, spin=0.8, phase=0.0, alpha=1.0):
    """Medalla Nobel de píxeles: moneda que gira (se achica en X para fingir rotación)."""
    if alpha <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)) if alpha < 1 else cv
    d = ImageDraw.Draw(lay)
    cx, cy, r = int(cx), int(cy), max(3, int(r))
    c = math.cos(t * spin * 2 * math.pi + phase)
    hw = int(round(r * abs(c)))
    if hw <= 2:
        d.rectangle([cx - 1, cy - r, cx + 1, cy + r], fill=(*MEDAL_D, 255), outline=(*INK, 255))
    else:
        rim = max(1, r // 6)
        d.ellipse([cx - hw, cy - r, cx + hw, cy + r], fill=(*MEDAL_RIM, 255), outline=(*INK, 255))
        ih, ir = max(1, hw - rim), r - rim
        d.ellipse([cx - ih, cy - ir, cx + ih, cy + ir], fill=(*MEDAL, 255))
        if c > 0 and r >= 9 and hw > r * 0.45:
            # perfil (cara) en relieve
            k = ih / ir
            d.ellipse([cx + int(-0.32 * ir * k), cy - int(0.55 * ir), cx + int(0.30 * ir * k), cy + int(0.1 * ir)],
                      fill=(*MEDAL_D, 255))
            d.polygon([(cx + int(-0.55 * ir * k), cy + int(0.62 * ir)), (cx + int(0.55 * ir * k), cy + int(0.62 * ir)),
                       (cx + int(0.25 * ir * k), cy + int(0.12 * ir)), (cx + int(-0.25 * ir * k), cy + int(0.12 * ir))],
                      fill=(*MEDAL_D, 255))
        elif c <= 0 and r >= 9 and hw > r * 0.45:
            # reverso: corona de laurel (anillo)
            k = ih / ir
            d.ellipse([cx - int(0.6 * ir * k), cy - int(0.6 * ir), cx + int(0.6 * ir * k), cy + int(0.6 * ir)],
                      outline=(*MEDAL_D, 255))
        # brillo
        if ih >= 4 and ir >= 4:
            x0, y0 = cx - ih + max(1, ih // 4), cy - ir + max(1, ir // 4)
            d.rectangle([x0, y0, x0 + max(1, ih // 4), y0 + max(1, ir // 5)], fill=(*MEDAL_HI, 255))
    if alpha < 1:
        paste(cv, lay, 0, 0, alpha)
    if r >= 10 and abs(c) > 0.8:
        sparkle(cv, cx - hw // 2, cy - r // 2, t * 1.3 + cx, 3)


def medal_on(cv, x, feet, t, phase=0.0, scale=3):
    """Medalla colgada (cinta azul) en el pecho de un personaje."""
    d = ImageDraw.Draw(cv)
    k = scale
    neck = feet - 32 * k
    my = feet - 25 * k
    d.line([(x - 3 * k, neck), (x - 1, my - 8)], fill=(40, 70, 170, 255), width=max(1, k - 1))
    d.line([(x + 3 * k, neck), (x + 1, my - 8)], fill=(40, 70, 170, 255), width=max(1, k - 1))
    medal(cv, x, my, 3 * k + 1, t, spin=0.6, phase=phase)


def fly_medal(cv, t, t0, dur, p0, p1, r0, r1, phase=0.0):
    """Medalla que vuela de p0 a p1 (devuelve True si ya llegó)."""
    p = prog(t, t0, t0 + dur)
    if p <= 0:
        return False
    if p >= 1:
        return True
    e = ease_out(p)
    x = p0[0] + (p1[0] - p0[0]) * e
    y = p0[1] + (p1[1] - p0[1]) * e - math.sin(p * math.pi) * 30
    medal(cv, x, y, r0 + (r1 - r0) * e, t, spin=2.0, phase=phase)
    return False


def robot_face(cv, x, feet, t, scale, face):
    """Dibuja caras extra del robot (wink) sobre una pantalla vacía."""
    ox, oy = int(x) - 15 * scale, int(feet) - 39 * scale
    d = ImageDraw.Draw(cv)

    def px(lx, ly):
        d.rectangle([ox + lx * scale, oy + ly * scale, ox + lx * scale + scale - 1, oy + ly * scale + scale - 1],
                    fill=(*GLOW, 255))
    if face == "wink":
        for yy in (10, 11, 12):
            px(11, yy); px(12, yy)
        px(16, 11); px(17, 10); px(18, 11)
        px(11, 13); px(17, 13)
        for xx in range(12, 17):
            px(xx, 14)


def robot2(cv, x, feet, t, face="happy", scale=3, alpha=1.0):
    if face == "wink":
        robot(cv, x, feet, t, face="off", scale=scale, alpha=alpha)
        if alpha > 0.5:
            robot_face(cv, x, feet, t, scale, "wink")
    else:
        robot(cv, x, feet, t, face=face, scale=scale, alpha=alpha)


def card_pop(cv, name, first, last, cx, y, t, t0, alpha_out=1.0):
    """Retrato + nombre (patrón de presentación)."""
    a, dy = pop(t, t0, 0.4)
    a = min(a, alpha_out)
    if a <= 0:
        return
    if a < 1:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        portrait_card(lay, name, cx - 32, y + dy)
        paste(cv, lay, 0, 0, a)
    else:
        portrait_card(cv, name, cx - 32, y + dy)
    draw_text(cv, first, cx, y + 78 + dy, "silk", 8, GREY, align="center", alpha=a)
    draw_text(cv, last, cx, y + 88 + dy, "press", 8, CREAM, align="center", alpha=a)


def drop_text(cv, text, cx, y, t, t0, size=48, ramp=GOLD_RAMP, alpha_out=1.0):
    p = prog(t, t0, t0 + 0.55)
    if p <= 0 or alpha_out <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=ramp, outline_w=2,
              alpha=min(1, p * 3, alpha_out))


def neural_net(cv, cx, cy, t, p, layers=(3, 4, 3), dx=22, dy=11):
    """Pequeña red neuronal con pulsos que viajan (p = aparición 0..1)."""
    if p <= 0:
        return
    d = ImageDraw.Draw(cv)
    pts = []
    n = len(layers)
    for i, m in enumerate(layers):
        x = cx + int((i - (n - 1) / 2) * dx)
        pts.append([(x, cy + int((j - (m - 1) / 2) * dy)) for j in range(m)])
    for i in range(n - 1):
        for a_ in pts[i]:
            for b_ in pts[i + 1]:
                d.line([a_, b_], fill=(40, 110, 150, int(255 * p)))
    # pulsos
    for i in range(n - 1):
        for j, a_ in enumerate(pts[i]):
            b_ = pts[i + 1][(j * 2 + int(t * 2)) % len(pts[i + 1])]
            f = (t * 1.6 + j * 0.3 + i * 0.5) % 1.0
            x = int(a_[0] + (b_[0] - a_[0]) * f)
            y = int(a_[1] + (b_[1] - a_[1]) * f)
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(220, 255, 255, int(255 * p)))
    for layer in pts:
        for (x, y) in layer:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(*CYAN, int(255 * p)), outline=(*INK, 255))
            d.point((x - 1, y - 1), fill=(240, 255, 255, 255))


def stage_bg(top=(8, 10, 26), bottom=(34, 40, 78)):
    cv = vgradient(top, bottom, 14)
    d = ImageDraw.Draw(cv)
    d.rectangle([0, 206, W, H], fill=(20, 22, 44, 255))
    for y in (206, 214, 226, 242, 262):
        d.line([(0, y), (W, y)], fill=(40, 46, 86, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, 206), (x, H)], fill=(30, 34, 66, 255))
    return cv


def big_orb(cv, cx, cy, t, a=1.0, r=5):
    if a <= 0:
        return
    d = ImageDraw.Draw(cv)
    pulse = 0.5 + 0.5 * math.sin(t * 4 + cx)
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=(90, 220, 255, int(70 * a * pulse)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 230, 255, int(255 * a)), outline=(30, 110, 160, 255))
    d.rectangle([cx - r // 2, cy - r // 2, cx - r // 2 + 1, cy - r // 2 + 1], fill=(240, 255, 255, 255))


# ------------------------------------------------------------------ Dartmouth (noche / amanecer)

def _dart_sky():
    if "sky" not in _CACHE:
        a = np.array(bg("bg_dartmouth_summer")).astype(np.int32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        yy = np.repeat(np.arange(H)[:, None], W, 1)
        xx = np.repeat(np.arange(W)[None, :], H, 0)
        blue = (b > 150) & (b > r + 30) & (yy < 150)
        cloud = (r > 200) & (g > 200) & (b > 200) & (yy < 72) & ((xx < 214) | (xx > 268))
        _CACHE["sky"] = blue | cloud
        grad = np.zeros((H, W, 3), dtype=np.float32)
        for y in range(H):
            k = int(y / 150 * 8) / 8
            grad[y, :] = [6 + 20 * k, 8 + 24 * k, 26 + 46 * k]
        _CACHE["night"] = grad
        dawn = np.zeros((H, W, 3), dtype=np.float32)
        for y in range(H):
            k = min(1.0, int(y / 140 * 8) / 8)
            dawn[y, :] = [60 + 190 * k, 50 + 100 * k, 90 - 20 * k]
        _CACHE["dawn"] = dawn
    return _CACHE["sky"]


def dart_sky_bg(t, night, dawn=0.0, sun=None):
    """Fondo de Dartmouth con cielo nocturno/amanecer. sun=(x, y) dibuja el sol detrás de los edificios."""
    sky = _dart_sky()
    base = bg("bg_dartmouth_summer").copy()
    if night > 0:
        base = grade(base, mul=(0.32, 0.38, 0.7), add=(4, 6, 22), sat=0.55, k=night)
    if dawn > 0:
        base = grade(base, mul=(1.08, 0.86, 0.74), add=(18, 6, 0), sat=1.0, k=dawn * 0.6)
    a = np.array(base)
    rgb = a[..., :3].astype(np.float32)
    if night > 0:
        rgb[sky] = rgb[sky] * (1 - night) + _CACHE["night"][sky] * night
    if dawn > 0:
        rgb[sky] = rgb[sky] * (1 - dawn * 0.75) + _CACHE["dawn"][sky] * dawn * 0.75
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if night > 0.05:
        STARS.draw(lay, t, alpha=night)
    if sun is not None:
        draw_sun(lay, int(sun[0]), int(sun[1]), 13, t, face=False)
    L = np.array(lay)
    m = sky & (L[..., 3] > 0)
    rgb[m] = L[m, :3]
    a[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


# ------------------------------------------------------------------ proteína

PROT_PATH = [(0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 1), (2, 0),
             (3, 0), (4, 0), (5, 0), (5, 1), (4, 1), (3, 1), (3, 2), (4, 2), (5, 2), (5, 3), (5, 4), (5, 5),
             (4, 5), (4, 4), (4, 3), (3, 3), (3, 4), (3, 5), (2, 5), (2, 4), (2, 3), (1, 3), (1, 4), (1, 5)]


def _ham_path(rng, n=6):
    """Camino hamiltoniano aleatorio en una grilla n x n (Warnsdorff con desempate al azar)."""
    for _ in range(400):
        start = (int(rng.integers(0, n)), int(rng.integers(0, n)))
        path, seen = [start], {start}
        while len(path) < n * n:
            x, y = path[-1]
            nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
            if not nb:
                break

            def deg(c):
                return sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                           if 0 <= c[0] + dx < n and 0 <= c[1] + dy < n and (c[0] + dx, c[1] + dy) not in seen)
            m = min(deg(c) for c in nb)
            cand = [c for c in nb if deg(c) == m]
            c = cand[int(rng.integers(0, len(cand)))]
            path.append(c)
            seen.add(c)
        if len(path) == n * n:
            return path
    return PROT_PATH


def _protein():
    """Plegado final: camino compacto e irregular en grilla 6x6 con un leve desorden (aspecto orgánico).
    Devuelve (giros, largos de enlace relativos)."""
    if "prot" in _CACHE:
        return _CACHE["prot"]
    rng = np.random.default_rng(1972)
    best, best_score = PROT_PATH, -1
    for _ in range(60):
        pth = _ham_path(rng)
        # preferimos caminos con muchos giros (menos tramos rectos = menos "letra")
        turns_n = sum(1 for i in range(1, len(pth) - 1)
                      if (pth[i][0] - pth[i - 1][0], pth[i][1] - pth[i - 1][1]) !=
                      (pth[i + 1][0] - pth[i][0], pth[i + 1][1] - pth[i][1]))
        if turns_n > best_score:
            best, best_score = pth, turns_n
    P = np.array(best, dtype=np.float64) + rng.uniform(-0.22, 0.22, (len(best), 2))
    seg = P[1:] - P[:-1]
    lens = np.sqrt((seg ** 2).sum(1))
    dirs = np.arctan2(seg[:, 1], seg[:, 0])
    turns = []
    for i in range(1, len(dirs)):
        dd = dirs[i] - dirs[i - 1]
        while dd > math.pi:
            dd -= 2 * math.pi
        while dd <= -math.pi:
            dd += 2 * math.pi
        turns.append(dd)
    _CACHE["prot"] = (turns, list(lens))
    return _CACHE["prot"]


PROT_COLS = [(40, 80, 220), (50, 140, 240), (70, 210, 240), (90, 230, 160), (240, 220, 80), (250, 150, 60)]


def draw_protein(cv, cx, cy, t, p_fold, t_fold0, t_fold1, clip=(160, 45, 381, 166)):
    turns, lens = _protein()
    n = len(turns) + 2
    pe = ease_in_out(p_fold)
    ang = 0.0
    pts = [(0.0, 0.0)]
    span = t_fold1 - t_fold0
    for i in range(n - 1):
        if i > 0:
            # cada articulación se pliega con un pequeño retraso (el plegado avanza por la cadena)
            a0 = t_fold0 + span * 0.3 * (i / n)
            pi_ = ease_in_out(prog(t, a0, a0 + span * 0.7))
            wig = 0.2 * math.sin(t * 3.0 + i * 0.8) * (1 - pi_)
            ang += turns[i - 1] * pi_ + wig
        bond = 6.0 + (12.0 * lens[i] - 6.0) * pe
        x, y = pts[-1]
        pts.append((x + math.cos(ang) * bond, y + math.sin(ang) * bond))
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    pts = [(int(round(cx + x - mx)), int(round(cy + y - my))) for x, y in pts]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(len(pts) - 1):
        k = i / (len(pts) - 1)
        col = PROT_COLS[min(len(PROT_COLS) - 1, int(k * len(PROT_COLS)))]
        d.line([pts[i], pts[i + 1]], fill=(*shade(col, 0.75), 255), width=3 if p_fold > 0.6 else 2)
    rad = 3
    for i, (x, y) in enumerate(pts):
        k = i / (len(pts) - 1)
        col = PROT_COLS[min(len(PROT_COLS) - 1, int(k * len(PROT_COLS)))]
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(*col, 255), outline=(*INK, 255))
        d.point((x - 1, y - 1), fill=(255, 255, 255, 255))
    x0, y0, x1, y1 = clip
    paste(cv, lay.crop((x0, y0, x1, y1)), x0, y0)


# =========================================================================== escenas

def sc_physics(t):
    """En octubre de 2024 la IA llega a lo más alto de la ciencia: Nobel de Física a Hopfield y Hinton."""
    cv = bg("bg_nobel_stage_2024").copy()
    t_oct = w("c8_01", "octubre")
    t_24 = w("c8_01", "veinticuatro")
    t_ia = w("c8_01", "inteligencia")
    t_alto = w("c8_01", "alto")
    t_hop = w("c8_02", "Hopfield")
    t_hin = w("c8_02", "Hinton")
    t_nob = w("c8_02", "Nobel")
    t_fis = w("c8_02", "Fisica")
    t_red = w("c8_02", "redes")
    # brillos del escenario
    for i in range(4):
        sparkle(cv, 112 + (i % 2) * 254, 44 + (i // 2) * 8, t * 0.7 + i, 2, GOLD)
    # OCTUBRE / 2024
    out = 1 - prog(t, t_alto - 0.75, t_alto - 0.4)
    if out > 0:
        draw_text(cv, "OCTUBRE", 240, 14, "press", 16, CREAM, align="center",
                  reveal=(t - t_oct + 0.1) * 22, alpha=out)
        drop_text(cv, "2024", 240, 40, t, t_24 - 0.1, size=48, alpha_out=out)
    # medalla gigante que baja sobre el disco dorado del escenario
    t_land = t_alto + 0.15
    if t > t_alto - 0.45:
        p = ease_out(prog(t, t_alto - 0.45, t_land))
        if t < t_nob:
            y = int(-50 + (72 + 50) * p)
            medal(cv, 240, y, 34, t, spin=0.5 if t > t_land else 1.4)
            if t > t_land:
                for i in range(5):
                    sparkle(cv, 240 + int(math.cos(i * 1.26 + t) * 46), 72 + int(math.sin(i * 1.26 + t) * 46),
                            t + i, 3, GOLD)
    # robot: llega y mira hacia arriba
    rx, _ = walk(t, t_ia - 0.1, t_ia + 1.0, W + 50, 240)
    face = "happy"
    if t_alto - 0.5 < t < t_land + 0.1:
        face = "question"
    elif t_land + 0.1 <= t < t_hop - 0.2:
        face = "heart"
    elif t > t_nob:
        face = "heart" if t < t_nob + 1.5 else "happy"
    if t > t_ia - 0.1:
        robot(cv, rx, 264, t, face=face, scale=3)
    # laureados
    hx, hph = walk(t, t_hop - 0.85, t_hop - 0.05, -50, 122)
    gx, gph = walk(t, t_hin - 0.85, t_hin - 0.05, W + 50, 358)
    landed = t > t_nob + 0.55
    for key, x, ph, tn, fac, ph0 in (("hopfield", hx, hph, t_hop, 1, 0.0), ("hinton24", gx, gph, t_hin, -1, 1.7)):
        if t < tn - 0.85:
            continue
        if ph is not None:
            arms, mood = "down", "neutral"
        elif t < t_nob:
            arms, mood = ("wave" if t < tn + 0.8 else "down"), "happy"
        elif t < t_nob + 1.6:
            arms, mood = "cheer", "happy"
        else:
            arms, mood = "hold", "happy"
        look = 0 if ph is not None else (1 if x < 240 else -1)
        char(cv, key, x, 264, t, walk=ph, arms=arms, mood=mood, scale=3, look=look,
             facing=fac if ph is not None else 1)
        if landed:
            medal_on(cv, int(x), 264, t, phase=ph0)
    # la medalla se divide en dos y vuela a los laureados
    if t_nob <= t:
        for x1, ph0 in ((122, 0.0), (358, 1.7)):
            fly_medal(cv, t, t_nob, 0.55, (240, 72), (x1, 264 - 75), 34, 10, ph0)
    # tarjetas
    card_pop(cv, "john_hopfield", "JOHN", "HOPFIELD", 58, 14, t, t_hop - 0.1)
    card_pop(cv, "geoffrey_hinton_2024", "GEOFFREY", "HINTON", 422, 14, t, t_hin - 0.1)
    # rótulo central
    if t > t_fis - 0.1:
        a, dy = pop(t, t_fis - 0.1, 0.4)
        window(cv, 100, 16 + dy, 280, 54)
        draw_text(cv, "NOBEL DE FÍSICA", 240, 26 + dy, "press", 16, align="center", gradient=GOLD_RAMP, alpha=a)
        draw_text(cv, "2024 · HOPFIELD Y HINTON", 240, 52 + dy, "press", 8, CREAM, align="center", alpha=a)
    # red neuronal sobre el robot
    neural_net(cv, 240, 112, t, prog(t, t_red - 0.3, t_red + 0.1))
    return vignette(cv, 0.35)


def sc_chemistry(t):
    """Un día después: Nobel de Química para Hassabis, Jumper (DeepMind) y Baker."""
    cv = bg("bg_nobel_stage_2024").copy()
    t_dia = w("c8_03", "dia")
    t_has = w("c8_03", "Hassabis")
    t_jum = w("c8_03", "Jumper")
    t_dm = w("c8_03", "DeepMind")
    t_nob = w("c8_03", "Nobel")
    t_dav = w("c8_03", "David")
    t_bak = w("c8_03", "Baker")
    # calendario que pasa del 8 al 9 de octubre
    cal_out = 1 - prog(t, t_jum - 0.5, t_jum - 0.15)
    if cal_out > 0:
        a, dy = pop(t, S2 + 0.05, 0.35)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x0, y0 = 209, 14 + dy
        draw_paper(lay, x0, y0, 62, 62)
        d = ImageDraw.Draw(lay)
        d.rectangle([x0 + 1, y0 + 1, x0 + 61, y0 + 13], fill=(200, 70, 60, 255))
        draw_text(lay, "OCT 2024", x0 + 31, y0 + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        f = prog(t, t_dia, t_dia + 0.3)
        num = "8" if f < 0.5 else "9"
        sq = abs(1 - 2 * f)
        if sq > 0.15:
            draw_text(lay, num, x0 + 31, y0 + 24, "press", 32, INK, align="center", outline=None, shadow=False)
        if 0 < f < 1:
            yy = y0 + 22 + int((1 - sq) * 18)
            d.rectangle([x0 + 4, yy, x0 + 58, yy + 2], fill=(200, 190, 170, 255))
        paste(cv, lay, 0, 0, min(a, cal_out))
        draw_text(cv, "UN DÍA DESPUÉS", 240, 84 + dy, "press", 8, GOLD, align="center",
                  reveal=(t - t_dia + 0.1) * 26, alpha=cal_out)
    # laureados
    people = [("hassabis", 110, t_has, "demis_hassabis", "DEMIS", "HASSABIS", 0.3),
              ("jumper", 240, t_jum, "john_jumper", "JOHN", "JUMPER", 1.1),
              ("baker", 370, t_bak, "david_baker", "DAVID", "BAKER", 2.2)]
    for key, x, tn, por, first, last, ph0 in people:
        t0 = tn - 0.15 if key != "baker" else t_dav - 0.05
        a, dy = pop(t, t0, 0.35)
        if a <= 0:
            continue
        t_med = t_nob if key != "baker" else t_dav + 0.1
        if t < t_med:
            arms = "wave" if t < t0 + 0.9 else "down"
        elif t < t_med + 1.4:
            arms = "cheer"
        else:
            arms = "hold"
        look = 1 if x < 240 else (-1 if x > 240 else 0)
        char(cv, key, x, 264 + dy, t, alpha=a, arms=arms, mood="happy", scale=3, look=look)
        if fly_medal(cv, t, t_med, 0.5, (x, -30), (x, 264 - 75), 10, 10, ph0):
            medal_on(cv, x, 264, t, phase=ph0)
        card_pop(cv, por, first, last, x, 14, t, t0)
    # etiqueta DeepMind
    if t > t_dm - 0.05:
        a, dy = pop(t, t_dm - 0.05, 0.35)
        window(cv, 137, 110 + dy, 76, 16, fill=(16, 50, 100), border=CYAN)
        draw_text(cv, "DEEPMIND", 175, 114 + dy, "press", 8, CREAM, align="center", alpha=a)
        d = ImageDraw.Draw(cv)
        for i in range(4):
            d.line([(134 - i, 118 + dy - i), (134 - i, 118 + dy + i)], fill=(*CYAN, 255))
            d.line([(216 + i, 118 + dy - i), (216 + i, 118 + dy + i)], fill=(*CYAN, 255))
    lower_third(cv, "NOBEL DE QUÍMICA 2024", "HASSABIS · JUMPER · BAKER", t, w("c8_03", "Quimica") - 0.1,
                S3 + 1.0, x=60, y=226)
    return vignette(cv, 0.35)


def sc_alphafold(t):
    """AlphaFold predice la forma de las proteínas: un problema de medio siglo."""
    cv = bg("bg_protein_lab_2024").copy()
    t_af = w("c8_03", "AlphaFold")
    t_pre = w("c8_03", "predice")
    t_prot = w("c8_03", "proteinas")
    t_prob = w("c8_03", "problema")
    t_medio = w("c8_03", "medio")
    t_fold0, t_fold1 = t_pre - 0.1, t_prot + 0.6
    # pantalla propia sobre el monitor gigante
    on = prog(t, t_af - 0.25, t_af + 0.1)
    if on > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.rectangle([158, 28, 382, 188], fill=(4, 14, 24, 255), outline=(*CYAN, 255))
        for x in range(166, 382, 16):
            d.line([(x, 46), (x, 186)], fill=(10, 34, 48, 255))
        for y in range(54, 188, 16):
            d.line([(160, y), (380, y)], fill=(10, 34, 48, 255))
        d.rectangle([159, 29, 381, 43], fill=(12, 50, 70, 255))
        draw_text(lay, "PLEGAMIENTO DE PROTEÍNAS", 168, 33, "silk", 8, CYAN, reveal=(t - t_af) * 30)
        if int(t * 2) % 2:
            d.rectangle([370, 33, 375, 38], fill=(*GLOW, 255))
        paste(cv, lay, 0, 0, on)
        if on >= 1:
            p_fold = prog(t, t_fold0, t_fold1)
            draw_protein(cv, 270, 110, t, p_fold, t_fold0, t_fold1)
            # estado
            if p_fold < 1:
                txt = "PLEGANDO..." if p_fold > 0 else "SECUENCIA"
                draw_text(cv, txt, 270, 172, "press", 8, GREY, align="center")
            else:
                draw_text(cv, "ESTRUCTURA 3D", 270, 172, "press", 8, GLOW, align="center")
    # gran título ALPHAFOLD
    if t > t_af - 0.1:
        a, dy = pop(t, t_af - 0.1, 0.4)
        draw_text(cv, "ALPHAFOLD", 270, 4 + dy, "press", 16, align="center", gradient=CYAN_RAMP, alpha=a)
    # contador de medio siglo
    if t > t_prob - 0.1:
        a, dy = pop(t, t_prob - 0.1, 0.4)
        window(cv, 148, 198 + dy, 244, 50)
        draw_text(cv, "UN PROBLEMA DE", 270, 206 + dy, "press", 8, GREY, align="center", alpha=a)
        n = int(round(50 * ease_out(prog(t, t_prob + 0.2, t_medio - 0.1))))
        if t < t_medio - 0.05:
            draw_text(cv, f"{n} AÑOS", 270, 222 + dy, "press", 16, align="center", gradient=CREAM_RAMP, alpha=a)
        else:
            pp = prog(t, t_medio - 0.05, t_medio + 0.2)
            draw_text(cv, "MEDIO SIGLO", 270, 222 + dy + int((1 - ease_out_back(pp)) * -6), "press", 16,
                      align="center", gradient=GOLD_RAMP, alpha=a)
            for i in range(3):
                sparkle(cv, 196 + i * 74, 230 + (i % 2) * 8, t + i, 3, GOLD)
    # personajes
    char(cv, "hassabis", 66, 266, t, arms="point" if t_af - 0.2 < t < t_prot + 0.8 else "down",
         mood="happy", look=1, scale=3)
    face = "think" if t < t_fold1 else ("heart" if t < t_prob else "happy")
    robot(cv, 430, 266, t, face=face, scale=3)
    if t > t_fold1:
        bulb(cv, 430, 140 - int(abs(math.sin(t * 3)) * 2), t, prog(t, t_fold1, t_fold1 + 0.3))
    return vignette(cv, 0.35)


def sc_hinton(t):
    """Hinton, el mismo que siguió apostando por las redes neuronales cuando nadie lo hacía."""
    t_h = TL.s("c8_04")
    t_ap = w("c8_04", "apostando")
    t_red = w("c8_04", "redes")
    t_cua = w("c8_04", "cuando")
    t_nad = w("c8_04", "nadie")
    cold = ease_in_out(prog(t, t_cua - 0.1, t_nad + 0.3))
    cv = stage_bg()
    if cold > 0:
        cv = grade(cv, mul=(0.8, 0.95, 1.2), add=(10, 18, 30), sat=0.4, k=cold)
    ages = [("hinton86", "geoffrey_hinton_1986", "1986", 96),
            ("hinton12", "geoffrey_hinton_2012", "2012", 240),
            ("hinton24", "geoffrey_hinton_2024", "2024", 384)]
    t_pops = [t_h, t_h + 0.55, t_h + 1.1]
    for i, (key, por, yr, x) in enumerate(ages):
        t0 = t_pops[i]
        a, dy = pop(t, t0, 0.35)
        if a <= 0:
            continue
        cv = spotlight(cv, x, 0, 262, 10, 90, strength=0.2 * a)
        holding = t > t_ap - 0.2
        char(cv, key, x, 262 + dy, t, alpha=a, arms="hold" if holding else ("wave" if t < t0 + 0.7 else "down"),
             mood="happy" if not (t_cua < t < t_nad + 0.6) else "neutral", scale=3, look=0)
        # retrato + año
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        portrait_card(lay, por, x - 32, 12 + dy)
        paste(cv, lay, 0, 0, a)
        draw_text(cv, yr, x, 90 + dy, "press", 16, align="center", gradient=GOLD_RAMP, alpha=a)
    # el hilo de las redes neuronales que une las tres edades
    p = prog(t, t_ap - 0.2, t_red + 0.6)
    oy = 262 - 74
    if p > 0:
        d = ImageDraw.Draw(cv)
        xe = int(96 + (384 - 96) * ease_in_out(p))
        d.line([(96, oy), (xe, oy)], fill=(40, 150, 210, 255), width=3)
        d.line([(96, oy - 1), (xe, oy - 1)], fill=(150, 240, 255, 255))
        for k in range(6):
            f = (t * 0.7 + k / 6) % 1.0
            x = int(96 + (384 - 96) * f)
            if x < xe:
                d.rectangle([x - 1, oy - 2, x + 2, oy + 1], fill=(240, 255, 255, 255))
    for i, x in enumerate((96, 240, 384)):
        if t > t_ap - 0.2 + i * 0.25:
            big_orb(cv, x, oy, t, prog(t, t_ap - 0.2 + i * 0.25, t_ap + 0.1 + i * 0.25), r=6)
    if cold > 0:
        SNOW.draw(cv, t, density=0.6 * cold)
    return vignette(cv, 0.4)


# ------------------------------------------------------------------ hoy

PANEL_W, PANEL_H, PANEL_Y = 100, 84, 36
PANEL_X = [19, 133, 247, 361]


def _panel_write(im, t, t0):
    iw, ih = im.size
    draw_paper(im, 6, 6, iw - 14, ih - 14)
    d = ImageDraw.Draw(im)
    p = (t - t0) * 1.6
    lens = [56, 62, 48, 60, 36]
    px_, py_ = 12, 16
    for i, L in enumerate(lens):
        k = clamp01(p - i)
        if k <= 0:
            break
        y = 16 + i * 11
        ln = int(L * k)
        d.line([(12, y), (12 + ln, y)], fill=(60, 64, 90, 255), width=2)
        px_, py_ = 12 + ln, y
    # lápiz
    d.line([(px_, py_ - 1), (px_ + 9, py_ - 10)], fill=(240, 200, 60, 255), width=3)
    d.line([(px_ + 7, py_ - 8), (px_ + 10, py_ - 11)], fill=(230, 120, 140, 255), width=3)
    d.point((px_, py_), fill=(*INK, 255))


def _panel_code(im, t, t0):
    iw, ih = im.size
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, iw - 5, ih - 5], fill=(10, 14, 28, 255), outline=(*INK, 255))
    draw_text(im, "</>", iw // 2, 10, "press", 16, align="center", gradient=CYAN_RAMP)
    cols = [(255, 120, 160), (120, 220, 255), (250, 210, 100), (140, 240, 150), (200, 160, 255)]
    lines = [(0, 30), (8, 40), (8, 26), (16, 34), (8, 20), (0, 14)]
    n = (t - t0) * 9
    for i, (ind, L) in enumerate(lines):
        k = clamp01(n - i)
        if k <= 0:
            break
        y = 34 + i * 7
        d.rectangle([10 + ind, y, 10 + ind + int(L * k), y + 2], fill=(*cols[i % len(cols)], 255))
    if int(t * 4) % 2:
        i = min(len(lines) - 1, int(n))
        d.rectangle([12 + lines[i][0] + lines[i][1], 34 + i * 7, 14 + lines[i][0] + lines[i][1], 36 + i * 7],
                    fill=(240, 240, 240, 255))


def _note(d, x, y, col):
    d.ellipse([x, y, x + 6, y + 4], fill=(*col, 255), outline=(*INK, 255))
    d.line([(x + 6, y + 2), (x + 6, y - 12)], fill=(*INK, 255), width=2)
    d.line([(x + 6, y - 12), (x + 10, y - 8)], fill=(*INK, 255), width=2)


def _panel_music(im, t, t0):
    iw, ih = im.size
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, iw - 5, ih - 5], fill=(30, 26, 60, 255), outline=(*INK, 255))
    for i in range(5):
        y = 26 + i * 7
        d.line([(8, y), (iw - 9, y)], fill=(200, 196, 230, 255))
    cols = [GOLD, CYAN, (255, 130, 170), (140, 240, 150)]
    n = (t - t0) * 5
    for i in range(5):
        if n < i:
            break
        x = 12 + i * 16
        base = 44 - [2, 9, 5, 13, 7][i] * 1
        bounce = int(abs(math.sin(t * 6 + i)) * 3)
        _note(d, x, base - bounce, cols[i % 4])


def _landscape(iw, ih, t):
    im = Image.new("RGBA", (iw, ih), (0, 0, 0, 255))
    a = np.zeros((ih, iw, 4), dtype=np.uint8)
    for y in range(ih):
        k = int(y / ih * 6) / 6
        a[y, :, :3] = [int(250 - 80 * k), int(150 + 40 * k), int(110 + 100 * k)]
    a[..., 3] = 255
    im = Image.fromarray(a, "RGBA")
    d = ImageDraw.Draw(im)
    d.ellipse([iw * 0.62, ih * 0.18, iw * 0.62 + ih * 0.22, ih * 0.40], fill=(255, 236, 150, 255))
    d.polygon([(0, ih * 0.75), (iw * 0.25, ih * 0.38), (iw * 0.5, ih * 0.7), (iw * 0.72, ih * 0.45), (iw, ih * 0.75),
               (iw, ih), (0, ih)], fill=(70, 60, 110, 255))
    d.polygon([(iw * 0.18, ih * 0.48), (iw * 0.25, ih * 0.38), (iw * 0.32, ih * 0.48)], fill=(240, 240, 250, 255))
    d.rectangle([0, int(ih * 0.82), iw, ih], fill=(60, 140, 90, 255))
    return im


def _miniature(t):
    """Miniatura de la apertura del propio video (1955)."""
    mini = bg("bg_office_1955").resize((240, 135), Image.NEAREST).copy()
    for i, k in enumerate(FOUR):
        char(mini, k, 34 + i * 34, 131, t, scale=1, mood="happy")
    draw_text(mini, "1955", 120, 10, "press", 24, align="center", gradient=GOLD_RAMP, outline_w=2)
    return mini


def _panel_image(im, t, t0):
    iw, ih = im.size
    land = _landscape(iw - 8, ih - 8, t)
    # "difusión": ruido que se resuelve en imagen
    p = prog(t, t0 + 0.1, t0 + 1.1)
    A = np.array(land)
    if p < 1:
        rnd = np.random.default_rng(int(t * 12))
        noise = rnd.integers(30, 230, size=A.shape[:2] + (3,), dtype=np.uint8)
        th = bayer_tile(A.shape[1], A.shape[0])
        m = th >= p
        A[m, :3] = noise[m]
    paste(im, Image.fromarray(A, "RGBA"), 4, 4)


def sc_today(t):
    """Hoy, las máquinas escriben, programan, componen música y generan imágenes como las de este video."""
    cv = stage_bg((6, 8, 22), (26, 30, 66))
    STARS.draw(cv, t * 0.4, alpha=0.4)
    t_hoy = TL.s("c8_05")
    t_maq = w("c8_05", "maquinas")
    beats = [w("c8_05", "escriben"), w("c8_05", "programan"), w("c8_05", "componen"), w("c8_05", "generan")]
    t_vid = w("c8_05", "este video")
    labels = [("ESCRIBEN", None), ("PROGRAMAN", None), ("COMPONEN", "MÚSICA"), ("GENERAN", "IMÁGENES")]
    drawers = [_panel_write, _panel_code, _panel_music, _panel_image]
    drop_text(cv, "HOY", 240, 6, t, t_hoy - 0.05, size=24)
    grow = ease_in_out(prog(t, t_vid - 0.1, t_vid + 0.35))
    for i in range(4):
        t0 = beats[i] - 0.05
        a, dy = pop(t, t0, 0.35)
        if a <= 0:
            continue
        x, y = PANEL_X[i], PANEL_Y + dy
        if i == 3 and grow > 0:
            continue
        window(cv, x, y, PANEL_W, PANEL_H)
        inner = Image.new("RGBA", (PANEL_W - 8, PANEL_H - 8), (0, 0, 0, 0))
        drawers[i](inner, t, t0)
        paste(cv, inner, x + 4, y + 4, a)
        l1, l2 = labels[i]
        draw_text(cv, l1, x + PANEL_W // 2, PANEL_Y + PANEL_H + 6, "press", 8, GOLD, align="center", alpha=a)
        if l2:
            draw_text(cv, l2, x + PANEL_W // 2, PANEL_Y + PANEL_H + 16, "press", 8, GOLD, align="center", alpha=a)
    # la imagen generada crece y muestra... este mismo video
    if grow > 0:
        x0, y0, w0, h0 = PANEL_X[3], PANEL_Y, PANEL_W, PANEL_H
        x1, y1, w1, h1 = 116, 4, 248, 143
        x = int(x0 + (x1 - x0) * grow); y = int(y0 + (y1 - y0) * grow)
        ww = int(w0 + (w1 - w0) * grow); hh = int(h0 + (h1 - h0) * grow)
        window(cv, x, y, ww, hh, border=GOLD)
        mini = _miniature(t)
        land = _landscape(240, 135, t)
        k = prog(t, t_vid + 0.1, t_vid + 0.45)
        content = dither_mix_any(land, mini, k)
        content = content.resize((ww - 8, hh - 8), Image.NEAREST)
        paste(cv, content, x + 4, y + 4)
        if grow >= 1:
            for i in range(4):
                sparkle(cv, x + 10 + (i % 2) * (ww - 20), y + 10 + (i // 2) * (hh - 20), t + i * 0.7, 3, GOLD)
    # la máquina
    if t > t_maq - 0.1:
        a, dy = pop(t, t_maq - 0.1, 0.4)
        face = "talk" if t < beats[0] else "happy"
        if t > t_vid + 0.45:
            face = "wink" if (t - t_vid - 0.45) % 1.6 < 0.9 else "happy"
        robot2(cv, 240 if grow <= 0 else 240, 268 + dy, t, face=face, scale=3, alpha=a)
    return vignette(cv, 0.35)


def dither_mix_any(a, b, k):
    if k <= 0:
        return a
    if k >= 1:
        return b
    A = np.array(a); B = np.array(b)
    th = bayer_tile(A.shape[1], A.shape[0])
    m = th < k
    A[m] = B[m]
    return Image.fromarray(A, a.mode)


# ------------------------------------------------------------------ Dartmouth, 70 años después

BOTS = [  # (x, feet, kind) kind: g = suelo, f = volando
    (30, 214, "g"), (96, 220, "g"), (162, 212, "g"), (318, 212, "g"), (384, 220, "g"), (450, 214, "g"),
    (84, 244, "g"), (140, 242, "g"), (192, 244, "g"), (288, 244, "g"), (340, 242, "g"), (396, 244, "g"),
    (120, 40, "f"), (196, 26, "f"), (290, 30, "f"), (356, 52, "f"), (60, 70, "f"), (430, 66, "f"),
]


def flying_bot(cv, x, y, t, face="happy"):
    arr = S.render_robot(face, int(t * 30) % 90, False, (t % 3.1) < 0.12)
    yy = int(y + math.sin(t * 4 + x) * 3)
    paste_arr(cv, arr, int(x) - 15, yy - 40)
    d = ImageDraw.Draw(cv)
    span = 9 if int(t * 20 + x) % 2 else 4
    d.line([(int(x) - span, yy - 42), (int(x) + span, yy - 42)], fill=(200, 200, 210, 255))


def _window_mask():
    if "win" not in _CACHE:
        a = np.array(bg("bg_dartmouth_summer")).astype(np.int32)
        dark = (a[..., 0] + a[..., 1] + a[..., 2]) < 150
        yy = np.repeat(np.arange(H)[:, None], W, 1)
        _CACHE["win"] = dark & (yy > 128) & (yy < 196)
    return _CACHE["win"]


def sc_dartmouth70(t):
    """Setenta años después de aquel verano en Dartmouth, la IA está en todas partes."""
    t6 = TL.s("c8_06")
    t_ver = w("c8_06", "verano")
    t_dar = w("c8_06", "Dartmouth")
    t_ia = w("c8_06", "inteligencia")
    t_tod = w("c8_06", "todas")
    cv = bg("bg_dartmouth_summer").copy()
    draw_sun(cv, 62, 40, 14, t)
    # pantallas encendidas en las ventanas
    if t > t_ia:
        a = np.array(cv)
        m = _window_mask()
        bands = [(160, 196), (196, 214), (268, 290), (300, 330)]
        for j, (xa, xb) in enumerate(bands):
            if t > t_ia + 0.15 + j * 0.25:
                mm = m.copy()
                mm[:, :xa] = False
                mm[:, xb:] = False
                fl = 1.0 if int(t * 6 + j) % 7 else 0.8
                a[mm, :3] = (np.array([60, 230, 130]) * fl).astype(np.uint8)
        cv = Image.fromarray(a, "RGBA")
    # 70 lucecitas 1956 -> 2026
    p = ease_in_out(prog(t, t6 + 0.05, t_ver - 0.1))
    years = 70 * p
    bars70(cv, years, t)
    if t > t_ia:
        la = prog(t, t_ia, t_ia + 0.4)
        draw_text(cv, "1956", 24, 236, "press", 8, CREAM, alpha=la)
        draw_text(cv, "2026", 456, 236, "press", 8, CREAM, align="right", alpha=la)
    out_year = 1 - prog(t, t_ia - 0.3, t_ia)
    if out_year > 0:
        draw_text(cv, str(1956 + int(round(years))), 240, 70, "press", 32, align="center", gradient=GOLD_RAMP,
                  outline_w=2, alpha=out_year)
        if p >= 1:
            draw_text(cv, "SETENTA AÑOS DESPUÉS", 240, 110, "press", 8, GOLD, align="center", alpha=out_year)
    # los diez de 1956
    xs = [33 + i * 46 for i in range(10)]
    for i, k in enumerate(S.DARTMOUTH_TEN):
        a, dy = pop(t, t_ver + i * 0.07, 0.35)
        fade = 1 - prog(t, t_ia - 0.1 + i * 0.04, t_ia + 0.35 + i * 0.04)
        a = min(a, fade)
        if a <= 0:
            continue
        char(cv, k, xs[i], 238 + dy, t, alpha=a, mood="happy", arms="wave" if t > t_dar else "down",
             look=1 if xs[i] < 240 else -1, scale=2)
    # robots en todas partes
    for j, (x, feet, kind) in enumerate(BOTS):
        t0 = t_ia + 0.1 + j * 0.11
        a, dy = pop(t, t0, 0.3)
        if a <= 0:
            continue
        face = ["happy", "talk", "heart", "happy"][j % 4]
        if kind == "f":
            flying_bot(cv, x, feet + dy, t + j * 0.37, face)
        else:
            robot(cv, x, feet + dy, t + j * 0.37, face=face, alpha=a, scale=1)
    if t > t_ia + 0.2:
        a, dy = pop(t, t_ia + 0.2, 0.4)
        robot(cv, 240, 246 + dy, t, face="heart" if t > t_tod else "happy", alpha=a, scale=2)
    if t > t_tod - 0.1:
        a, dy = pop(t, t_tod - 0.1, 0.35)
        draw_text(cv, "EN TODAS PARTES", 240, 100 + dy, "press", 16, align="center", gradient=CYAN_RAMP,
                  alpha=a, outline_w=2)
    return vignette(cv, 0.3)


# ------------------------------------------------------------------ la pregunta sigue abierta

def sc_question(t):
    """Y sin embargo, la pregunta de Turing sigue abierta. ¿Pueden pensar las máquinas?"""
    t7 = TL.s("c8_07")
    t_preg = w("c8_07", "pregunta")
    t_tur = w("c8_07", "Turing")
    t_sig = w("c8_07", "sigue")
    t_pue = w("c8_07", "Pueden")
    t_maq = w("c8_07", "maquinas")
    night = ease_in_out(prog(t, S7, t7 + 0.5))
    cv = dart_sky_bg(t, night)
    draw_moon_masked = night > 0.5
    if draw_moon_masked:
        draw_moon(cv, 362, 92, 9)
    # Turing y la máquina, frente a frente
    pose = dict(arms="down", mood="neutral")
    if t > t_preg:
        pose = dict(arms="think", mood="neutral")
    if t > t_pue:
        pose = dict(arms="point", mood="happy")
    char(cv, "turing", 150, 264, t, scale=3, look=1, **pose)
    face = "happy"
    if t > t_sig:
        face = "question"
    if t > t_maq + 0.5:
        face = "think"
    robot(cv, 330, 264, t, face=face, scale=3)
    # globos
    if t > t_preg + 0.1:
        a, dy = pop(t, t_preg + 0.1)
        bubble(cv, "?", 150, 108 + dy, size=16)
    if t > t_sig + 0.1:
        a, dy = pop(t, t_sig + 0.1)
        bubble(cv, "?", 330, 140 + dy, size=16)
    # tarjeta de Turing
    out = 1 - prog(t, t_pue - 0.4, t_pue - 0.1)
    if out > 0:
        card_pop(cv, "alan_turing", "ALAN", "TURING", 46, 14, t, t_tur - 0.1, alpha_out=out)
    # la pregunta
    if t > t_pue - 0.1:
        draw_text(cv, "¿PUEDEN PENSAR", 240, 24, "press", 24, align="center", gradient=CYAN_RAMP, outline_w=2,
                  reveal=(t - t_pue + 0.1) * 18)
        draw_text(cv, "LAS MÁQUINAS?", 240, 56, "press", 24, align="center", gradient=CYAN_RAMP, outline_w=2,
                  reveal=(t - t_maq + 0.15) * 18)
    return vignette(cv, 0.45)


# ------------------------------------------------------------------ final

def sc_finale(t):
    """Tal vez la respuesta llegue en el próximo verano. O tal vez nos lleve otros setenta años."""
    t8 = TL.s("c8_08")
    t_ver = w("c8_08", "verano")
    t_o = w("c8_08", "O tal")
    t_otros = w("c8_08", "otros")
    t_set = w("c8_08", "setenta")
    t_e = TL.e("c8_08")
    p = ease_in_out(prog(t, t8 - 0.2, t_ver + 0.2))     # amanecer
    night = 1 - p
    dawn = math.sin(p * math.pi) * 0.9 + 0.25 * p
    sun_y = 128 - 88 * ease_out(prog(t, t8 - 0.2, t_ver + 0.6))
    cv = dart_sky_bg(t, night, dawn=min(1.0, dawn), sun=(330, sun_y))
    # Turing y la máquina miran el amanecer
    look = 1 if t < t_e + 1.0 else 0
    char(cv, "turing", 186, 236, t, scale=2, look=look, mood="happy",
         arms="wave" if t > t_e + 1.4 else "down")
    rface = "happy"
    if t > t_ver:
        rface = "heart"
    if t > t_e + 1.4:
        rface = "wink" if (t - t_e - 1.4) % 1.8 < 1.0 else "happy"
    robot2(cv, 294, 236, t, face=rface, scale=2)
    # fila de 70 años: llena (1956-2026)... y otros 70 por delante
    if t > t_o - 0.2:
        a = prog(t, t_o - 0.2, t_o + 0.2)
        nxt = t > t_otros
        lit = 0 if nxt else 70
        bars70(cv, lit, t, alpha=a)
        if nxt and int(t * 3) % 2:
            ImageDraw.Draw(cv).rectangle([30, 252, 33, 262], fill=(255, 250, 220, 255))
        l, r = ("2026", "2096?") if nxt else ("1956", "2026")
        draw_text(cv, l, 24, 236, "press", 8, CREAM, alpha=a)
        draw_text(cv, r, 456, 236, "press", 8, CYAN if nxt else CREAM, align="right", alpha=a)
    # título final
    if t > t_ver - 0.1:
        a = prog(t, t_ver - 0.1, t_ver + 0.3)
        wh = int(36 + (112 - 36) * ease_out(prog(t, t_set - 0.3, t_set + 0.1)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        window(lay, 12, 6, 456, wh, alpha=0.88)
        paste(cv, lay, 0, 0, a)
        draw_text(cv, "LE DIERON UN VERANO.", 240, 18, "press", 16, align="center", gradient=GOLD_RAMP,
                  reveal=(t - t_ver + 0.1) * 26)
    if t > t_set - 0.1:
        pp = prog(t, t_set - 0.1, t_set + 0.25)
        sz_70 = 24 if text_size("TARDÓ 70 AÑOS.", "press", 32)[0] > 448 else 32
        y_70 = (48 if sz_70 == 24 else 44) + (1 - ease_out_back(pp, 2.0)) * -20
        draw_text(cv, "TARDÓ 70 AÑOS.", 240, int(y_70), "press", sz_70,
                  align="center", gradient=GOLD_RAMP, outline_w=2, alpha=min(1, pp * 2))
        if pp >= 1:
            for i in range(6):
                sparkle(cv, 40 + i * 80, 46 + (i % 2) * 34, t + i * 0.8, 3, GOLD)
    if t > t_set + 0.35:
        draw_text(cv, "LA HISTORIA DE LA INTELIGENCIA ARTIFICIAL", 240, 88, "press", 8, CYAN, align="center",
                  reveal=(t - t_set - 0.35) * 45)
    if t > t_e + 0.4:
        draw_text(cv, "GRACIAS POR VER", 240, 102, "press", 8, CREAM, align="center",
                  alpha=prog(t, t_e + 0.4, t_e + 0.9))
    # destello al caer el título
    t_fl = t_set + 0.2
    if t_fl <= t < t_fl + 0.15:
        cv = fade_to(cv, (255, 250, 230), 0.3 * (1 - (t - t_fl) / 0.15))
    return vignette(cv, 0.35)


# =========================================================================== montaje

def scenes():
    return [
        (T_CARD - 0.3, make_card(CH, ["EL VERANO QUE", "NO TERMINÓ"], "2024 – HOY", robot_face="happy"), None),
        (S1, sc_physics, lambda t: (cam_push(t, S1, S2, 1.0, 1.03, (240, 140), (240, 150))[0]
                                    + cam_punch(t, [w("c8_01", "alto") + 0.15, w("c8_02", "Nobel") + 0.5], 0.08),
                                    240, 140)),
        (S2, sc_chemistry, lambda t: (1.0 + cam_punch(t, [w("c8_03", n) for n in ("Hassabis", "Jumper", "David")], 0.04)
                                      + cam_punch(t, [w("c8_03", "Nobel") + 0.5], 0.07), 240, 135)),
        (S3, sc_alphafold, lambda t: cam_push(t, S3 + 0.5, TL.s("c8_04"), 1.0, 1.05, (260, 135), (260, 132))),
        (S4, sc_hinton, lambda t: (1.0 + cam_punch(t, [TL.s("c8_04") + i * 0.55 for i in range(3)], 0.05), 240, 135)),
        (S5, sc_today, lambda t: (1.0 + cam_punch(t, [w("c8_05", k) for k in ("escriben", "programan", "componen",
                                                                            "generan")], 0.04)
                                  + cam_punch(t, [w("c8_05", "este video") + 0.35], 0.08), 240, 120)),
        (S6, sc_dartmouth70, lambda t: (1.0 + 0.05 * math.sin(math.pi * prog(t, S6, w("c8_06", "inteligencia")))
                                        + cam_punch(t, [w("c8_06", "todas") - 0.1], 0.06), 240, 150)),
        (S7, sc_question, lambda t: cam_push(t, TL.s("c8_07"), TL.e("c8_07"), 1.0, 1.1, (240, 135), (240, 110))),
        (S8, sc_finale, lambda t: cam_push(t, S8, w("c8_08", "verano"), 1.12, 1.0, (240, 160), (240, 135))),
    ]


# =========================================================================== música y efectos

def music(A):
    s, e = TL.s, TL.e
    t_alto = w("c8_01", "alto") + 0.15
    t_nob = w("c8_02", "Nobel")
    t_nob2 = w("c8_03", "Nobel")
    # majestuoso: Nobel
    A.section(T_CARD + 1.6, S2, 110, [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_triumph)
    A.crash(A.music, t_alto, 0.12)
    A.kick(A.music, t_nob + 0.5, 0.45)
    A.crash(A.music, t_nob + 0.5, 0.2)
    A.section(S2, S3, 110, [("F", "maj"), ("G", "maj"), ("E", "min"), ("A", "min")], A.st_triumph)
    A.kick(A.music, t_nob2 + 0.5, 0.4)
    A.crash(A.music, t_nob2 + 0.5, 0.16)
    # asombro: AlphaFold
    A.section(S3, S4, 96, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_build)
    A.sting(w("c8_03", "proteinas") + 0.4, [69, 72, 76, 81], vol=0.04)
    # Hinton: perseverancia
    A.section(S4, S5, 100, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")], A.st_build)
    # hoy: montaje enérgico
    A.section(S5, S6, 124, [("C", "maj"), ("A", "min"), ("F", "maj"), ("G", "maj")], A.st_bright)
    # Dartmouth: vuelve la melodía del verano
    A.section(S6, S7, 112, [("C", "maj"), ("F", "maj"), ("A", "min"), ("G", "maj")], A.st_summer_lead)
    # la pregunta abierta: misterio cálido
    A.section(S7 + 0.1, S8, 78, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")], A.st_mystery)
    # amanecer
    t_ver = w("c8_08", "verano")
    A.section(S8, w("c8_08", "setenta") - 0.1, 84, [("F", "maj"), ("G", "maj"), ("A", "min"), ("C", "add9")],
              A.st_winter, beats_per_chord=2)
    A.sting(t_ver, [72, 76, 79], vol=0.035, hold=0.8)
    # resolución final: sting + acorde largo sostenido
    t_fin = w("c8_08", "setenta") - 0.05
    A.kick(A.music, t_fin, 0.4)
    A.crash(A.music, t_fin, 0.14)
    A.sting(t_fin, [60, 64, 67, 72, 76, 79, 84], vol=0.05, step=0.11, hold=2.6)
    hold = max(2.0, T_END - t_fin - 0.4)
    for m in (48, 55, 60, 64, 67, 74):
        A.note(A.music, t_fin + 0.1, A.midi_hz(m), hold, duty=0.5, vol=0.022, a=0.3, s=0.8, r=1.2, vib=0.2)
    A.note(A.music, t_fin, A.midi_hz(36), hold, "tri", vol=0.24, a=0.05, s=0.9, r=1.4)
    # arpegio suave que se apaga
    for i in range(10):
        tt = t_fin + 1.6 + i * 0.32
        if tt > T_END - 0.8:
            break
        m = [72, 76, 79, 84, 79, 76][i % 6]
        A.note(A.music, tt, A.midi_hz(m), 0.3, duty=0.125, vol=0.03 * (1 - i / 12), s=0.4, r=0.2)


def sfx(A):
    s = TL.s
    # Física
    A.whoosh(w("c8_01", "octubre") - 0.1)
    A.pop_sfx(w("c8_01", "veinticuatro"), 420)
    A.robot_beep(w("c8_01", "inteligencia") + 0.4)
    A.whoosh(w("c8_01", "alto") - 0.45, 0.5)
    A.coin(w("c8_01", "alto") + 0.15)
    for n in ("Hopfield", "Hinton"):
        A.join_jingle(w("c8_02", n))
    t_nob = w("c8_02", "Nobel")
    A.whoosh(t_nob, 0.5)
    A.coin(t_nob + 0.55)
    A.coin(t_nob + 0.68)
    A.pop_sfx(w("c8_02", "Fisica") - 0.1, 600)
    t_red = w("c8_02", "redes")
    for i in range(5):
        A.blip(t_red - 0.2 + i * 0.07, 900 + i * 150, vol=0.03)
    # Química
    A.whoosh(S2 + 0.05)
    A.pop_sfx(w("c8_03", "dia"), 520)
    for n in ("Hassabis", "Jumper"):
        A.join_jingle(w("c8_03", n) - 0.1)
    A.join_jingle(w("c8_03", "David"))
    A.pop_sfx(w("c8_03", "DeepMind"), 700)
    t_nob2 = w("c8_03", "Nobel")
    A.coin(t_nob2 + 0.5)
    A.coin(t_nob2 + 0.6)
    A.coin(w("c8_03", "Baker") + 0.8)
    # AlphaFold
    t_af = w("c8_03", "AlphaFold")
    A.robot_beep(t_af - 0.2)
    A.text_blips(t_af, 9, 24)
    t0 = w("c8_03", "predice") - 0.1
    for i in range(12):
        A.blip(t0 + i * 0.15, 500 + i * 60, vol=0.025)
    A.pop_sfx(w("c8_03", "problema") - 0.1, 480)
    A.coin(w("c8_03", "medio") + 0.2)
    # Hinton
    for i in range(3):
        A.whoosh(s("c8_04") + i * 0.55 - 0.05, 0.3, 0.045)
        A.pop_sfx(s("c8_04") + i * 0.55, 500 + i * 120)
    A.wind(w("c8_04", "cuando"), TL.e("c8_04") + 0.2, 0.035)
    # Hoy
    A.pop_sfx(s("c8_05"), 400)
    A.robot_beep(w("c8_05", "maquinas"))
    for i, k in enumerate(("escriben", "programan", "componen", "generan")):
        A.pop_sfx(w("c8_05", k) - 0.05, 560 + i * 110)
    A.typewriter(w("c8_05", "escriben"), w("c8_05", "programan") - 0.1, 14, 0.035)
    A.text_blips(w("c8_05", "programan"), 6, 9, vol=0.018)
    t_vid = w("c8_05", "este video")
    A.whoosh(t_vid - 0.1, 0.45)
    A.robot_beep(t_vid + 0.5)
    A.blip(t_vid + 0.6, 1800, vol=0.04)
    # Dartmouth 70
    A.whoosh(S6)
    t6 = s("c8_06")
    for i in range(14):
        A.blip(t6 + 0.05 + i * 0.1, 600 + i * 40, vol=0.02)
    A.join_jingle(w("c8_06", "verano"))
    t_ia = w("c8_06", "inteligencia")
    for j in range(len(BOTS)):
        if j % 2 == 0:
            A.pop_sfx(t_ia + 0.1 + j * 0.11, 600 + (j % 7) * 70, 0.035)
    A.robot_beep(t_ia + 0.3)
    A.pop_sfx(w("c8_06", "todas") - 0.1, 760)
    # pregunta
    A.whoosh(S7 + 0.1, 0.6, 0.05)
    A.pop_sfx(w("c8_07", "pregunta") + 0.1, 600)
    A.join_jingle(w("c8_07", "Turing") - 0.1, 0.045)
    A.robot_beep(w("c8_07", "sigue") + 0.1)
    A.text_blips(w("c8_07", "Pueden") - 0.1, 14, 18)
    A.text_blips(w("c8_07", "maquinas") - 0.15, 13, 18)
    # final
    A.whoosh(S8 + 0.1, 0.7, 0.04)
    A.text_blips(w("c8_08", "verano") - 0.1, 20, 26)
    A.robot_beep(w("c8_08", "verano") + 0.3)
    A.text_blips(TL.e("c8_08") + 0.2, 41, 40, vol=0.015)
    A.robot_beep(TL.e("c8_08") + 1.5)
