"""Capítulo 3: El primer invierno (1966 – 1980)."""
from common import *  # noqa

RED = (232, 72, 60)
GREEN_T = (100, 250, 150)
FIRE_RAMP = [(255, 244, 190), (255, 206, 100), (246, 140, 60), (210, 70, 44)]

# =========================================================================== helpers locales


def year_big(cv, text, cx, y, t, t0, t_out=None, size=48, ramp=GOLD_RAMP):
    a_out = 1.0 if t_out is None else 1 - prog(t, t_out, t_out + 0.4)
    p = prog(t, t0, t0 + 0.55)
    if p <= 0 or a_out <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=ramp, outline_w=2,
              alpha=min(p * 3, a_out))
    if p >= 1 and a_out >= 1:
        tw, _ = text_size(text, "press", size)
        for i, ph in enumerate((0.0, 1.7, 3.1)):
            sx = cx - tw // 2 + int((i + 0.5) * tw / 3)
            sparkle(cv, sx + (i * 7) % 11, y + 4 + (i * 13) % size, t + ph, 3)


def name_card(cv, t, t0, t1, pname, title, sub, x=14, y=12):
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


def mark_cross(cv, cx, cy, s=10, color=RED):
    d = ImageDraw.Draw(cv)
    segs = (((cx - s, cy - s), (cx + s, cy + s)), ((cx + s, cy - s), (cx - s, cy + s)))
    for a, b in segs:
        d.line([a, b], fill=(*INK, 255), width=6)
    for a, b in segs:
        d.line([a, b], fill=(*color, 255), width=3)


_GRUNGE = np.random.default_rng(5).random((240, 480))


def stamp(cv, text, cx, cy, t, t0, color=(214, 44, 44), size=16, angle=-8):
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
    a[..., 3] = np.where(_GRUNGE[:h, :w] < 0.13, 0, a[..., 3])
    im = Image.fromarray(a, "RGBA").rotate(angle, resample=Image.NEAREST, expand=True)
    sc = 1 + (1 - p) * 0.8
    if sc > 1.01:
        im = im.resize((int(im.size[0] * sc), int(im.size[1] * sc)), Image.NEAREST)
    paste(cv, im, cx - im.size[0] // 2, cy - im.size[1] // 2, min(1.0, 0.4 + p))


def flash(cv, t, t0, color=(255, 255, 255), k=0.45, dur=0.16):
    if t0 <= t < t0 + dur:
        return fade_to(cv, color, k * (1 - (t - t0) / dur))
    return cv


def union_jack(cv, x, y, w=60, h=34):
    im = Image.new("RGBA", (w, h), (20, 40, 110, 255))
    d = ImageDraw.Draw(im)
    d.line([(0, 0), (w, h)], fill=(240, 240, 240, 255), width=7)
    d.line([(0, h), (w, 0)], fill=(240, 240, 240, 255), width=7)
    d.line([(0, 0), (w, h)], fill=(200, 30, 40, 255), width=2)
    d.line([(0, h), (w, 0)], fill=(200, 30, 40, 255), width=2)
    d.rectangle([w // 2 - 6, 0, w // 2 + 5, h], fill=(240, 240, 240, 255))
    d.rectangle([0, h // 2 - 6, w, h // 2 + 5], fill=(240, 240, 240, 255))
    d.rectangle([w // 2 - 3, 0, w // 2 + 2, h], fill=(200, 30, 40, 255))
    d.rectangle([0, h // 2 - 3, w, h // 2 + 2], fill=(200, 30, 40, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(*INK, 255))
    paste(cv, im, x, y)


def us_flag(cv, x, y, w=24, h=15):
    d = ImageDraw.Draw(cv)
    for i in range(7):
        y0 = y + int(i * h / 7)
        y1 = y + int((i + 1) * h / 7) - 1
        d.rectangle([x, y0, x + w, max(y0, y1)], fill=(200, 40, 50, 255) if i % 2 == 0 else (240, 240, 240, 255))
    d.rectangle([x, y, x + w // 2, y + h // 2], fill=(30, 50, 120, 255))
    for i in range(3):
        for j in range(2):
            d.point((x + 2 + i * 3, y + 2 + j * 3), fill=(255, 255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(*INK, 255))


# =========================================================================== escenas


def stage_bg(t):
    cv = vgradient((12, 16, 40), (30, 40, 86), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 14):
        d.line([(x, 0), (x, 206)], fill=(18, 22, 52, 255))
        d.line([(x + 7, 0), (x + 7, 206)], fill=(44, 56, 110, 255))
    d.rectangle([0, 0, W, 12], fill=(140, 40, 56, 255))
    for x in range(0, W, 24):
        d.pieslice([x, 2, x + 24, 22], 0, 180, fill=(140, 40, 56, 255), outline=(*INK, 255))
    d.rectangle([0, 206, W, H], fill=(84, 56, 38, 255))
    for i, y in enumerate((206, 214, 226, 242, 262)):
        d.line([(0, y), (W, y)], fill=(60, 40, 28, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, 206), (x, H)], fill=(70, 46, 32, 255))
    return cv


def calendar(cv, x0, y0, year, t, red=False):
    draw_paper(cv, x0, y0, 80, 72)
    d = ImageDraw.Draw(cv)
    d.rectangle([x0 + 1, y0 + 1, x0 + 79, y0 + 15], fill=(190, 60, 50, 255))
    for k in (16, 64):
        d.rectangle([x0 + k - 2, y0 - 4, x0 + k + 2, y0 + 4], fill=(90, 90, 100, 255), outline=(*INK, 255))
    draw_text(cv, "AÑO", x0 + 40, y0 + 5, "silk", 8, CREAM, align="center", outline=None, shadow=False)
    draw_text(cv, str(year), x0 + 40, y0 + 32, "press", 16, (180, 40, 40) if red else INK, align="center",
              outline=None, shadow=False)


def sc_promise(t):
    """Las promesas seguían creciendo. En 1970, Minsky predice que en tres a ocho años..."""
    cv = stage_bg(t)
    w = TL.word
    t0 = TL.s("c3_01")
    t_prom = w("c3_01", "promesas")
    t_mil = w("c3_01", "mil")
    t_min = w("c3_01", "Minsky")
    t_tres = w("c3_01", "tres")
    t_ocho = w("c3_01", "ocho")
    t_anos = w("c3_01", "años")
    t_int = w("c3_01", "inteligencia")
    t_hum = w("c3_01", "humano")
    t_prom2 = w("c3_01", "promedio")
    t_pero = TL.s("c3_02")
    t_res = w("c3_02", "resultados")
    t_lleg = w("c3_02", "llegan")
    cv = spotlight(cv, 390, 0, 266, 24, 130, color=(255, 240, 200), strength=0.2)
    # Minsky (1970)
    if t < t_min:
        arms = "cheer" if t_prom < t < t_mil else "down"
    elif t < t_tres:
        arms = "wave"
    elif t < t_pero:
        arms = "point_l"
    else:
        arms = "shrug" if t > t_res else "down"
    mood = "worried" if t > t_pero + 0.2 else "happy"
    talking = t_min - 0.2 < t < t_prom2 + 0.4 or t_prom - 0.2 < t < t_mil
    char(cv, "minsky70", 392, 264, t, scale=3, arms=arms, mood=mood, talk=talk_v(t, talking and t < t_pero),
         look=-1 if t > t_tres else 0)
    # medidor de promesas + globos
    if t < t_mil + 0.6:
        a_out = 1 - prog(t, t_mil, t_mil + 0.4)
        fill = 0.4 + 0.9 * ease_out(prog(t, t_prom - 0.3, t_mil - 0.2))
        x0 = 14 + int(-220 * (1 - a_out))
        window(cv, x0, 14, 196, 34)
        draw_text(cv, "PROMESAS", x0 + 8, 20, "press", 8, CREAM)
        d = ImageDraw.Draw(cv)
        d.rectangle([x0 + 8, 32, x0 + 186, 40], fill=(10, 10, 20, 255), outline=(*INK, 255))
        bw = int(178 * min(1.0, fill))
        over = fill > 1.0
        col = GOLD if not over else ((255, 90, 70) if int(t * 8) % 2 else GOLD)
        d.rectangle([x0 + 9, 33, x0 + 8 + bw, 39], fill=(*col, 255))
        if over:
            draw_text(cv, "!!", x0 + 192, 28, "press", 8, (255, 90, 70))
        promises = [("¡PRONTO!", 100, 118), ("¡YA CASI!", 254, 92), ("¡GARANTIZADO!", 150, 172),
                    ("¡EN POCOS AÑOS!", 270, 152)]
        for i, (txt, bx, by) in enumerate(promises):
            tp = t_prom + 0.05 + i * 0.4
            if t > tp:
                a, dy = pop(t, tp)
                if a_out > 0.5:
                    bubble(cv, txt, bx, by + dy)
    # 1970
    year_big(cv, "1970", 186, 24, t, t_mil - 0.05, t_tres - 0.45)
    name_card(cv, t, t_min, t_int - 0.4, "marvin_minsky_1970", "MARVIN MINSKY", "PREDICCIÓN · 1970", x=14, y=176)
    # la predicción
    if t > t_tres - 0.05:
        n = 4 if t < t_ocho - 0.05 else (8 if t < t_anos - 0.05 else 13)
        draw_text(cv, "DE 3 A 8 AÑOS", 30, 60, "press", 24, gradient=GOLD_RAMP, outline_w=2, reveal=n)
        if t > t_pero:
            p = prog(t, t_res - 0.2, t_res + 0.4)
            d = ImageDraw.Draw(cv)
            if p > 0:
                d.line([(26, 72), (26 + int(320 * p), 70)], fill=(*INK, 255), width=6)
                d.line([(26, 72), (26 + int(320 * p), 70)], fill=(*RED, 255), width=3)
        # calendario
        flip = prog(t, t_ocho, t_anos + 0.9)
        year = 1970 + int(ease_out(flip) * 8)
        late = 0
        if t > t_pero:
            late = int(prog(t, t_pero + 0.1, t_lleg + 0.3) * 5)
        a, dy = pop(t, t_tres + 0.1)
        calendar(cv, 146, 98 + dy, year + late, t, red=late > 0)
        if t > t_anos + 0.9 and t < t_pero:
            draw_text(cv, "PLAZO", 186, 176, "press", 8, CYAN, align="center")
        stamp(cv, "VENCIDO", 186, 150, t, t_lleg, size=8, angle=-12)
    # inteligencia humana
    if t > t_int - 0.1:
        draw_text(cv, "INTELIGENCIA GENERAL", 186, 186, "press", 16, CREAM, align="center",
                  reveal=(t - t_int + 0.1) * 26)
        draw_text(cv, "DE UN HUMANO PROMEDIO", 186, 208, "press", 8, CYAN, align="center",
                  reveal=(t - t_hum + 0.5) * 30)
    if t > t_prom2 - 0.2:
        draw_text(cv, "— MARVIN MINSKY, 1970", 186, 226, "silk", 8, GREY, align="center",
                  reveal=(t - t_prom2 + 0.2) * 30)
    return vignette(cv, 0.35)


def sc_alpac(t):
    """1966: el informe ALPAC. La traducción automática no estaba ni cerca."""
    cv = bg("bg_perceptron_lab").copy()
    cv = grade(cv, mul=(0.62, 0.72, 0.95), add=(0, 4, 14), sat=0.5)
    w = TL.word
    t_mil = w("c3_02", "mil novecientos")
    t_inf = w("c3_02", "informe")
    t_alp = w("c3_02", "ALPAC")
    t_conc = w("c3_02", "concluido")
    t_trad = w("c3_02", "traduccion")
    t_auto = w("c3_02", "automatica")
    t_no = w("c3_02", "no estaba")
    t_ig = w("c3_02", "igualar")
    t_hum = w("c3_02", "traductor")
    in_t0 = t_conc - 0.5
    proc0, proc1 = t_trad - 0.1, t_auto + 0.3
    out_t0 = proc1
    # pantalla
    sx, sy, sw, sh = 158, 60, 310, 150
    window(cv, sx, sy, sw, sh, fill=(8, 28, 18), border=(150, 160, 172), inner=(70, 80, 96))
    d = ImageDraw.Draw(cv)
    for y in range(sy + 4, sy + sh - 4, 2):
        d.line([(sx + 3, y), (sx + sw - 4, y)], fill=(12, 36, 24, 255))
    tx = sx + 12
    if t > in_t0 - 0.3:
        draw_text(cv, "ENTRADA:", tx, sy + 10, "silk", 8, (90, 170, 120))
        draw_text(cv, "EL GATO ESTÁ SOBRE LA MESA.", tx, sy + 24, "press", 8, GREEN_T,
                  reveal=(t - in_t0) * 40)
    if t > proc0:
        p = prog(t, proc0, proc1)
        draw_text(cv, "TRADUCIENDO...", tx, sy + 44, "silk", 8, (90, 170, 120))
        d.rectangle([tx, sy + 56, tx + 200, sy + 62], outline=(60, 140, 90, 255))
        d.rectangle([tx + 1, sy + 57, tx + 1 + int(198 * p), sy + 61], fill=(*GREEN_T, 255))
    if t > out_t0:
        draw_text(cv, "SALIDA:", tx, sy + 76, "silk", 8, (190, 150, 80))
        draw_text(cv, "GATO EL MESA ¿¿SOBRE?? LA", tx, sy + 90, "press", 8, (255, 196, 90), reveal=(t - out_t0) * 40)
        draw_text(cv, "ESTÁ #%& ??? MESA GATO", tx, sy + 102, "press", 8, (255, 196, 90),
                  reveal=(t - out_t0 - 0.6) * 40)
        if int(t * 3) % 2 and t > out_t0 + 1.2:
            draw_text(cv, "? ? ?", tx, sy + 120, "press", 8, (255, 120, 90))
    if t > t_no:
        a, dy = pop(t, t_no, 0.2)
        mark_cross(cv, 404, sy + 96 + dy, 26)
    # el robot traductor
    face = "happy"
    if t > in_t0:
        face = "talk" if t < proc0 else "think"
    if t > out_t0:
        face = "question"
    if t > t_no:
        face = "sad"
    robot(cv, 80, 262, t, face=face, scale=3)
    if proc0 < t < proc1:
        for i in range(3):
            sparkle(cv, 50 + i * 30, 132 - (i % 2) * 8, t * 2 + i, 2, GREEN_T)
    # títulos
    year_big(cv, "1966", 313, 10, t, t_mil - 0.05, t_alp - 0.5)
    if t > t_alp - 0.15:
        a, dy = pop(t, t_alp - 0.15)
        window(cv, 112, 10 + dy, 362, 42)
        draw_text(cv, "INFORME ALPAC · 1966", 293, 16 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
        draw_text(cv, "TRADUCCIÓN AUTOMÁTICA: LEJOS DEL HUMANO", 293, 36 + dy, "silk", 8, GREY, align="center")
    if t > t_ig - 0.1:
        draw_text(cv, "¿IGUAL A UN TRADUCTOR HUMANO?", sx + sw // 2 - 12, 222, "press", 8, CREAM, align="center",
                  reveal=(t - t_ig + 0.1) * 30)
        if t > t_hum + 0.4:
            mark_cross(cv, 450, 225, 7)
    dx, dy = shake(t, t_no, 0.25, 3)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


def lighthill_report(cv, x0, y0, t):
    bw, bh = 110, 92
    d = ImageDraw.Draw(cv)
    d.rectangle([x0 + 5, y0 + 5, x0 + bw + 6, y0 + bh + 6], fill=(0, 0, 0, 120))
    for k in range(5, 0, -1):  # hojas (grosor)
        d.rectangle([x0 + k, y0 + k, x0 + bw + k, y0 + bh + k], fill=(220, 214, 196, 255), outline=(150, 140, 120, 255))
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(236, 230, 212, 255), outline=(*INK, 255))
    d.rectangle([x0 + 1, y0 + 1, x0 + bw - 1, y0 + 14], fill=(30, 40, 80, 255))
    draw_text(cv, "INFORME · 1973", x0 + bw // 2, y0 + 4, "silk", 8, CREAM, align="center", outline=None,
              shadow=False)
    draw_text(cv, "INFORME", x0 + bw // 2, y0 + 22, "press", 8, INK, align="center", outline=None, shadow=False)
    draw_text(cv, "LIGHTHILL", x0 + bw // 2, y0 + 34, "press", 8, (150, 30, 30), align="center", outline=None,
              shadow=False)
    draw_text(cv, "ARTIFICIAL", x0 + bw // 2, y0 + 50, "silk", 8, (70, 70, 80), align="center", outline=None,
              shadow=False)
    draw_text(cv, "INTELLIGENCE", x0 + bw // 2, y0 + 60, "silk", 8, (70, 70, 80), align="center", outline=None,
              shadow=False)
    draw_text(cv, "1973", x0 + bw // 2, y0 + 76, "press", 8, INK, align="center", outline=None, shadow=False)


def sc_lighthill(t):
    """1973: James Lighthill entrega al gobierno británico un informe demoledor."""
    cv = bg("bg_british_office_1973").copy()
    w = TL.word
    t0 = TL.s("c3_03")
    t_mat = w("c3_03", "matematico")
    t_james = w("c3_03", "James")
    t_ent = w("c3_03", "entrega")
    t_gob = w("c3_03", "gobierno")
    t_inf = w("c3_03", "informe")
    t_dem = w("c3_03", "demoledor")
    land = t_dem
    # banderita del gobierno británico
    if t > t_gob - 0.1:
        a, dy = pop(t, t_gob - 0.1)
        window(cv, 262, 200 + dy, 204, 30)
        union_jack(cv, 270, 206 + dy, 30, 18)
        draw_text(cv, "GOBIERNO BRITÁNICO", 306, 212 + dy, "press", 8, CREAM)
    # Lighthill
    if t < t_ent:
        arms = "down"
    elif t < land:
        arms = "hold"
    else:
        arms = "point"
    char(cv, "lighthill", 214, 266, t, scale=3, arms=arms, mood="neutral",
         talk=talk_v(t, t_ent - 0.1 < t < land), look=1 if t > t_ent else 0)
    if t_ent <= t < land:
        # lleva el informe en las manos
        d = ImageDraw.Draw(cv)
        d.rectangle([196, 184, 232, 206], fill=(236, 230, 212, 255), outline=(*INK, 255))
        d.rectangle([197, 185, 231, 190], fill=(30, 40, 80, 255))
    if t > land - 0.35:
        p = prog(t, land - 0.35, land)
        yy = int(60 - (1 - p * p) * 200)
        lighthill_report(cv, 344, yy, t)
        if t > land:
            k = prog(t, land, land + 0.5)
            if k < 1:
                d = ImageDraw.Draw(cv)
                for s in (-1, 1):
                    for j in range(3):
                        px_ = 400 + s * int(62 + k * 30 + j * 8)
                        py_ = 158 - int(k * 10) - j * 3
                        d.rectangle([px_, py_, px_ + 2, py_ + 2], fill=(230, 220, 200, int(220 * (1 - k))))
            a = prog(t, land + 0.1, land + 0.3)
            draw_text(cv, "¡DEMOLEDOR!", 400, 38, "press", 8, (255, 110, 90), align="center", alpha=a)
    year_big(cv, "1973", 240, 14, t, t0 + 0.02, t_james - 0.5)
    name_card(cv, t, t_james, t_inf - 0.1, "james_lighthill", "JAMES LIGHTHILL", "MATEMÁTICO · REINO UNIDO")
    dx, dy = shake(t, land, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.4)


# --------------------------------------------------------------------------- explosión combinatoria

def _tree_levels():
    lv = []
    for L in range(7):
        n = 3 ** L
        width = 0 if L == 0 else min(1400, 104 * 3 * (2.05 ** (L - 1)))
        sp = width / max(1, n - 1) if n > 1 else 0
        y = 22 + L * 34
        xs = [240 + (i - (n - 1) / 2) * sp for i in range(n)]
        lv.append((y, xs))
    return lv


TREE = _tree_levels()


def fmt_num(n):
    s = f"{int(n):,}".replace(",", ".")
    return s


def sc_explosion(t):
    """La IA no cumplió sus objetivos... explosión combinatoria."""
    cv = vgradient((4, 8, 20), (16, 24, 52), 12)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 24):
        d.line([(x, 0), (x, H)], fill=(18, 28, 56, 255))
    for y in range(0, H, 24):
        d.line([(0, y), (W, y)], fill=(18, 28, 56, 255))
    w = TL.word
    t0 = TL.s("c3_04")
    t_no = w("c3_04", "no cumplio")
    t_obj = w("c3_04", "objetivos")
    t_prog = w("c3_04", "programas")
    t_aho = w("c3_04", "ahogan")
    t_exp = w("c3_04", "explosion")
    t_comb = w("c3_04", "combinatoria")
    slide = ease_in_out(prog(t, t_prog - 0.5, t_prog - 0.1))
    # árbol que explota
    t_l = [t_prog - 0.2 + L * 0.42 for L in range(7)]
    if t > t_l[1] - 0.05:
        burst = t > t_exp
        for L in range(1, 7):
            p = prog(t, t_l[L] - 0.05, t_l[L] + 0.3)
            if p <= 0:
                continue
            yp, xsp = TREE[L - 1]
            yc, xsc = TREE[L]
            heat = L / 6
            col = _mix((90, 200, 255), (255, 120, 60), heat)
            for i, xc in enumerate(xsc):
                if xc < -60 or xc > W + 60:
                    continue
                xp = xsp[i // 3]
                c = col
                if burst and (i * 7 + int(t * 12)) % 9 == 0:
                    c = (255, 240, 200)
                ex = xp + (xc - xp) * p
                ey = yp + (yc - yp) * p
                d.line([(int(xp), yp), (int(ex), int(ey))], fill=(*c, 255))
            for i, xc in enumerate(xsc):
                if p >= 1 and -4 < xc < W + 4:
                    r = max(1, 5 - L)
                    d.rectangle([int(xc) - r, yc - r, int(xc) + r, yc + r], fill=(*col, 255))
        d.ellipse([234, 16, 246, 28], fill=(*CYAN, 255), outline=(*INK, 255))
    # contador de posibilidades
    if t > t_l[1]:
        lc = prog(t, t_l[1] - 0.42, t_l[6]) * 6
        n = 3 ** lc
        if t > t_exp:
            n = 729 * 10 ** (prog(t, t_exp, t_comb + 0.8) * 12)
        window(cv, 10, 222, 210, 40, alpha=0.95)
        draw_text(cv, "POSIBILIDADES", 20, 230, "press", 8, GREY)
        draw_text(cv, fmt_num(n), 20, 244, "press", 8, GOLD if t < t_exp else (255, 110, 80))
    # la máquina se ahoga
    if t > t_prog - 0.4:
        face = "think"
        if t > t_aho:
            face = "sad"
        jit = int(math.sin(t * 40) * 2) if t > t_exp else 0
        robot(cv, 430 + jit, 262, t, face=face, scale=2)
        if t > t_aho:
            d2 = ImageDraw.Draw(cv)
            for k in range(2):
                yy = 190 + int(((t * 30 + k * 9) % 18))
                d2.rectangle([458, yy, 459, yy + 2], fill=(140, 200, 255, 255))
    # el informe: objetivos incumplidos
    if slide < 1:
        oy = int(slide * 280)
        x0, y0 = 96, 26 + oy
        draw_paper(cv, x0, y0, 288, 182)
        draw_text(cv, "INFORME LIGHTHILL", x0 + 144, y0 + 10, "press", 8, (150, 30, 30), align="center", outline=None,
                  shadow=False)
        draw_text(cv, "OBJETIVOS DE LA IA", x0 + 144, y0 + 26, "press", 8, INK, align="center", outline=None,
                  shadow=False)
        dd = ImageDraw.Draw(cv)
        dd.line([(x0 + 20, y0 + 38), (x0 + 268, y0 + 38)], fill=(150, 140, 120, 255))
        tx = [t0 + 0.6, t_no, t_no + 0.45, t_obj]
        for i in range(4):
            yy = y0 + 50 + i * 26
            q = prog(t, t0 + i * 0.25, t0 + i * 0.25 + 0.3)
            if q > 0:
                draw_text(cv, f"{i + 1}.", x0 + 26, yy, "press", 8, INK, outline=None, shadow=False)
                ln = [180, 140, 196, 120][i]
                dd.rectangle([x0 + 50, yy + 1, x0 + 50 + int(ln * q), yy + 6], fill=(150, 146, 136, 255))
            if t > tx[i]:
                mark_cross(cv, x0 + 252, yy + 3, 7)
        if t > t_obj + 0.3:
            draw_text(cv, "NO CUMPLIDOS", x0 + 144, y0 + 160, "press", 8, (190, 30, 30), align="center",
                      outline=None, shadow=False)
    # EXPLOSIÓN
    if t > t_exp:
        a = prog(t, t_exp, t_exp + 0.15)
        band = Image.new("RGBA", (W, 64), (6, 4, 12, 210))
        paste(cv, band, 0, 96, a)
        draw_text(cv, "EXPLOSIÓN", 240, 102, "press", 24, align="center", gradient=FIRE_RAMP, outline_w=2, alpha=a)
        if t > t_comb - 0.1:
            draw_text(cv, "COMBINATORIA", 240, 130, "press", 24, align="center", gradient=FIRE_RAMP, outline_w=2,
                      reveal=(t - t_comb + 0.1) * 30)
    dx, dy = shake(t, t_exp, 0.4, 5)
    cv = offset_canvas(cv, dx, dy)
    cv = flash(cv, t, t_exp, (255, 230, 200), 0.5)
    return vignette(cv, 0.35)


def _mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def gov_bg():
    cv = vgradient((44, 48, 62), (26, 28, 40), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 40):
        d.rectangle([x + 4, 20, x + 36, 200], outline=(52, 56, 72, 255))
    d.rectangle([0, 210, W, H], fill=(56, 44, 36, 255))
    for y in (216, 230, 250):
        d.line([(0, y), (W, y)], fill=(44, 34, 28, 255))
    return cv


def sc_cuts(t):
    """El Reino Unido recorta los fondos. Al año siguiente, DARPA también reduce su apoyo."""
    cv = gov_bg()
    w = TL.word
    t0 = TL.s("c3_05")
    t_rec = w("c3_05", "recorta")
    t_al = w("c3_05", "Al")
    t_eeuu = w("c3_05", "Estados")
    t_darpa = w("c3_05", "DARPA")
    t_tam = w("c3_05", "tambien")
    t_red = w("c3_05", "reduce")
    t_apoyo = w("c3_05", "apoyo")
    d = ImageDraw.Draw(cv)
    # Reino Unido
    a, dy = pop(t, t0 - 0.05)
    window(cv, 14, 14 + dy, 152, 200)
    union_jack(cv, 60, 24 + dy)
    draw_text(cv, "REINO UNIDO", 90, 66 + dy, "press", 8, CREAM, align="center")
    bx0, by0, bx1, by1 = 62, 82 + dy, 118, 204 + dy
    d.rectangle([bx0 - 2, by0 - 2, bx1 + 2, by1 + 2], fill=(10, 10, 20, 255), outline=(*INK, 255))
    full = by1 - by0
    level = 1.0 if t < t_rec + 0.05 else 0.25
    top = by1 - int(full * level)
    stripes = [(200, 30, 40), (240, 240, 240), (20, 40, 110)]
    for y in range(top, by1 + 1):
        d.line([(bx0, y), (bx1, y)], fill=(*stripes[((y - by0) // 6) % 3], 255))
    # pedazo cortado que cae
    if t > t_rec + 0.05:
        k = prog(t, t_rec + 0.05, t_rec + 0.9)
        if k < 1:
            piece_h = int(full * 0.75)
            off = int(k * k * 160)
            for y in range(by0, by0 + piece_h):
                yy = y + off
                if yy < H:
                    d.line([(bx0 + int(k * 20), yy), (bx1 + int(k * 20), yy)],
                           fill=(*stripes[((y - by0) // 6) % 3], int(255 * (1 - k))))
    # tijeras
    if t_rec - 0.35 < t < t_rec + 0.35:
        sx = int(30 + 110 * prog(t, t_rec - 0.35, t_rec + 0.1))
        sy = by1 - int(full * 0.25)
        open_ = int(t * 16) % 2
        d.line([(sx - 12, sy - 6 - open_ * 3), (sx + 8, sy)], fill=(210, 214, 224, 255), width=3)
        d.line([(sx - 12, sy + 6 + open_ * 3), (sx + 8, sy)], fill=(210, 214, 224, 255), width=3)
        d.ellipse([sx - 20, sy - 12 - open_ * 3, sx - 12, sy - 4 - open_ * 3], outline=(220, 60, 60, 255), width=2)
        d.ellipse([sx - 20, sy + 4 + open_ * 3, sx - 12, sy + 12 + open_ * 3], outline=(220, 60, 60, 255), width=2)
    # 1974
    year_big(cv, "1974", 232, 18, t, t_al - 0.05, size=24)
    # Estados Unidos: medidor
    if t > t_eeuu - 0.1:
        a, dy = pop(t, t_eeuu - 0.1)
        window(cv, 296, 14 + dy, 170, 40)
        us_flag(cv, 306, 22 + dy)
        draw_text(cv, "EE.UU. · DARPA", 338, 25 + dy, "press", 8, CREAM)
        fill = 1 - ease_in_out(prog(t, t_red, t_apoyo + 0.3))
        d.rectangle([306, 40 + dy, 456, 47 + dy], fill=(10, 10, 20, 255), outline=(*INK, 255))
        col = GOLD if fill > 0.4 else ((255, 90, 70) if int(t * 8) % 2 else (150, 50, 40))
        if fill > 0.01:
            d.rectangle([307, 41 + dy, 307 + int(148 * fill), 46 + dy], fill=(*col, 255))
        else:
            draw_text(cv, "0", 446, 30 + dy, "press", 8, (255, 90, 70))
    # sello de DARPA en la pared
    if t > t_darpa - 0.1:
        a, dy = pop(t, t_darpa - 0.1)
        cx, cy = 440, 106 + dy
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(26, 40, 90, 255), outline=(*GOLD, 255), width=2)
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(*GOLD, 255))
        draw_text(cv, "DARPA", cx, cy - 4, "press", 8, CREAM, align="center")
    # funcionario de DARPA
    if t > t_eeuu - 0.4:
        x, ph = walk(t, t_eeuu - 0.4, t_darpa, 540, 362)
        stamping = t_red - 0.25 < t < t_red + 0.1
        char(cv, "darpa", x, 266, t, walk=ph, scale=3, facing=-1 if ph is not None else 1,
             arms="cheer" if stamping else ("hold" if t > t_darpa else "down"),
             mood="neutral", talk=0, look=-1 if t > t_tam else 0)
    desk(cv, 230, 478, 214, 268, color=(70, 50, 40))
    # presupuesto
    if t > t_tam - 0.2:
        a, dy = pop(t, t_tam - 0.2)
        px0, py0 = 214, 118 + dy
        draw_paper(cv, px0, py0, 112, 86)
        draw_text(cv, "PRESUPUESTO", px0 + 56, py0 + 8, "press", 8, INK, align="center", outline=None, shadow=False)
        draw_text(cv, "INVESTIGACIÓN IA", px0 + 56, py0 + 22, "silk", 8, (80, 80, 90), align="center", outline=None,
                  shadow=False)
        dd = ImageDraw.Draw(cv)
        for i in range(4):
            yy = py0 + 38 + i * 10
            dd.line([(px0 + 10, yy), (px0 + 70, yy)], fill=(150, 150, 160, 255))
            draw_text(cv, "$$$", px0 + 78, yy - 4, "silk", 8, (60, 120, 60), outline=None, shadow=False)
        stamp(cv, "RECORTADO", px0 + 56, py0 + 48, t, t_red, size=8, angle=-10)
    dx, dy2 = shake(t, t_red, 0.3, 4)
    sx_, sy_ = shake(t, t_rec + 0.05, 0.2, 2)
    cv = offset_canvas(cv, dx + sx_, dy2 + sy_)
    return vignette(cv, 0.4)


RESEARCHERS = [
    dict(name="Investigador A", skin=S.SKIN["fair"], hair=(60, 40, 30), hair_style="side", glasses="black",
         top="labcoat", top_color=(232, 232, 226), shirt=(160, 190, 220), tie=(90, 40, 40), pants=(70, 70, 80)),
    dict(name="Investigadora B", skin=S.SKIN["tan"], hair=(40, 26, 20), hair_style="bun", top="sweater",
         top_color=(120, 70, 90), pants=(60, 60, 80), skirt=True, skirt_color=(70, 70, 90)),
    dict(name="Investigador C", skin=S.SKIN["light"], hair=(150, 90, 50), hair_style="curly", beard="short",
         top="shirt", top_color=(150, 170, 120), pants=(80, 66, 50)),
]


def carry_box(cv, x, feet, label="IA"):
    d = ImageDraw.Draw(cv)
    x0, y0, x1, y1 = int(x) - 26, feet - 92, int(x) + 26, feet - 54
    d.rectangle([x0, y0, x1, y1], fill=(176, 136, 90, 255), outline=(*INK, 255))
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 6], fill=(196, 156, 106, 255))
    d.line([(x0 + 1, y0 + 6), (x1 - 1, y0 + 6)], fill=(120, 90, 60, 255))
    d.rectangle([int(x) - 4, y0, int(x) + 4, y0 + 16], fill=(214, 200, 150, 255))
    draw_text(cv, label, int(x), y0 + 20, "press", 8, (90, 60, 30), align="center", outline=None, shadow=False)


def plate(cv, t, t_cross, t_flip):
    x0, y0, pw, ph = 156, 18, 144, 52
    flip = prog(t, t_flip, t_flip + 0.3)
    sy = abs(math.cos(flip * math.pi))
    hh = max(2, int(ph * sy))
    yy = y0 + (ph - hh) // 2
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, pw - 1, ph - 1], fill=(196, 168, 92, 255), outline=(*INK, 255))
    d.rectangle([2, 2, pw - 3, ph - 3], outline=(150, 120, 60, 255))
    new = flip >= 0.5
    draw_text(im, "LABORATORIO DE", pw // 2, 7, "silk", 8, (70, 50, 20), align="center", outline=None, shadow=False)
    if not new:
        draw_text(im, "INTELIGENCIA", pw // 2, 21, "press", 8, INK, align="center", outline=None, shadow=False)
        draw_text(im, "ARTIFICIAL", pw // 2, 33, "press", 8, INK, align="center", outline=None, shadow=False)
        p = prog(t, t_cross, t_cross + 0.3)
        if p > 0:
            d.line([(14, 25), (14 + int(116 * p), 25)], fill=(200, 40, 40, 255), width=2)
            d.line([(24, 37), (24 + int(96 * p), 37)], fill=(200, 40, 40, 255), width=2)
    else:
        draw_text(im, "INFORMÁTICA", pw // 2, 27, "press", 8, (30, 40, 90), align="center", outline=None,
                  shadow=False)
    if hh != ph:
        im = im.resize((pw, hh), Image.NEAREST)
    paste(cv, im, x0, yy)
    if t > t_flip + 0.3:
        for i in range(3):
            sparkle(cv, x0 + 10 + i * 52, y0 + 6 + (i % 2) * 36, t + i, 3, GOLD)


def sc_empty(t):
    """Los laboratorios se vacían. Cambian de campo, o cambian el nombre de lo que hacen."""
    cv = bg("bg_lab_1970s_empty").copy()
    w = TL.word
    t0 = TL.s("c3_06")
    t_vac = w("c3_06", "vacian")
    t_inv = w("c3_06", "investigadores")
    t_campo = w("c3_06", "campo")
    t_c2 = w("c3_06", "cambian", occurrence=2)
    t_nom = w("c3_06", "nombre")
    # nieve en la ventana
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    SNOW.draw(tmp, t, density=0.9)
    win = tmp.crop((294, 10, 440, 146))
    cv.alpha_composite(win, (294, 10))
    # cartel de SALIDA
    window(cv, 10, 12, 62, 18, fill=(20, 90, 50), border=(140, 230, 160))
    draw_text(cv, "SALIDA", 41, 17, "press", 8, (200, 255, 210), align="center")
    d = ImageDraw.Draw(cv)
    d.polygon([(14, 40), (24, 34), (24, 46)], fill=(140, 230, 160, 255), outline=(*INK, 255))
    plate(cv, t, t_c2 - 0.05, t_nom)
    # se van con sus cajas
    walkers = [(0, t0 - 0.2, t0 + 2.6, 520, -70, "IA"), (1, t0 + 0.6, t0 + 3.6, 540, -70, "IA")]
    for idx, a0, a1, x0, x1, lab in walkers:
        if a0 < t < a1:
            x, ph = walk(t, a0, a1, x0, x1)
            char(cv, RESEARCHERS[idx], x, 266, t, walk=ph, scale=3, facing=-1, arms="hold", mood="sad")
            carry_box(cv, x, 266, lab)
            if idx == 1 and t_campo - 0.5 < t < t_campo + 0.7:
                bubble(cv, "OTRO CAMPO...", int(x), 108)
    # el que cambia el nombre
    if t > t_campo - 0.6:
        x, ph = walk(t, t_campo - 0.6, t_c2 - 0.1, 520, 228)
        if ph is not None:
            arms, mood = "down", "neutral"
        elif t < t_nom + 0.4:
            arms, mood = "wave", "neutral"
        else:
            arms, mood = "shrug", "happy"
        char(cv, RESEARCHERS[2], x, 266, t, walk=ph, scale=3, facing=-1 if ph is not None else 1, arms=arms,
             mood=mood, look=0)
        if t > t_nom + 0.5:
            a, dy = pop(t, t_nom + 0.5)
            bubble(cv, "¡NUEVO NOMBRE!", 250, 108 + dy)
    # las luces se apagan
    dark = ease_in_out(prog(t, t_vac + 0.3, t_inv))
    if t_vac - 0.2 < t < t_vac + 0.3 and int(t * 20) % 3 == 0:
        dark = 0.6
    if dark > 0:
        cv = grade(cv, mul=(0.72, 0.76, 0.86), k=dark)
    return vignette(cv, 0.4)


_rng = np.random.default_rng(11)
_FROST_N = _rng.random((H, W)).astype(np.float32)
_yy, _xx = np.mgrid[0:H, 0:W]
_EDGE = (np.minimum(np.minimum(_xx, W - 1 - _xx) / (W / 2), np.minimum(_yy, H - 1 - _yy) / (H / 2))).astype(np.float32)
_FROST_M = _EDGE + (_FROST_N - 0.5) * 0.16 + np.sin(_xx * 0.21) * 0.02 + np.sin(_yy * 0.17 + 1) * 0.02


def frost(cv, level):
    if level <= 0:
        return cv
    a = np.array(cv)
    m = _FROST_M < level
    edge = (_FROST_M < level + 0.02) & ~m
    a[m, :3] = (a[m, :3] * 0.35 + np.array([214, 232, 248]) * 0.65).astype(np.uint8)
    a[edge, :3] = (240, 250, 255)
    return Image.fromarray(a, "RGBA")


def sc_freeze(t):
    """Había llegado el primer invierno de la inteligencia artificial."""
    w = TL.word
    t0 = TL.s("c3_07")
    t_pri = w("c3_07", "primer")
    t_inv = w("c3_07", "invierno")
    t_ia = w("c3_07", "inteligencia")
    t_end = TL.e("c3_07")
    cold = ease_in_out(prog(t, t0 - 0.2, t_inv + 0.3))
    cv = bg("bg_lab_1970s_empty").copy()
    cv = grade(cv, mul=(0.72, 0.76, 0.86))
    cv = grade(cv, mul=(0.75, 0.9, 1.12), add=(28, 40, 64), sat=0.2, k=0.4 + 0.6 * cold)
    SNOW.draw(cv, t, density=0.4 + 0.6 * cold)
    frozen = t > t_inv
    robot(cv, 240, 258, t, face="sad" if not frozen else "off", frozen=frozen, scale=3)
    if frozen:
        for i in range(4):
            sparkle(cv, 200 + i * 26, 150 + (i % 2) * 40, t + i * 0.7, 3, (230, 246, 255))
    # nieve acumulada
    acc = ease_in_out(prog(t, t0, t_end + 0.5))
    if acc > 0:
        a = np.array(cv)
        top = int(H - acc * 22)
        xs_ = np.arange(W)
        edge = top + (np.sin(xs_ * 0.19) * 2 + np.sin(xs_ * 0.05 + 2) * 3).astype(int)
        for x in range(W):
            e = max(0, min(H, edge[x]))
            a[e:, x, :3] = (226, 238, 250)
            if e < H:
                a[e, x, :3] = (255, 255, 255)
        cv = Image.fromarray(a, "RGBA")
    cv = frost(cv, 0.06 + 0.22 * ease_in_out(prog(t, t_pri - 0.4, t_end + 0.4)))
    if t > t_pri - 0.05:
        p = prog(t, t_pri - 0.05, t_pri + 0.4)
        yy = int(30 - (1 - ease_out_back(p, 2.0)) * 40)
        draw_text(cv, "PRIMER INVIERNO", 240, yy, "press", 24, align="center", gradient=ICE_RAMP, outline_w=2,
                  alpha=min(1, p * 3))
    if t > t_ia - 0.05:
        a, dy = pop(t, t_ia - 0.05, 0.4)
        draw_text(cv, "DE LA IA", 240, 62 + dy, "press", 24, align="center", gradient=ICE_RAMP, outline_w=2, alpha=a)
    if t > t_end - 0.4:
        for i in range(5):
            sparkle(cv, 90 + i * 75, 34 + (i % 2) * 40, t + i * 0.5, 3, (230, 246, 255))
    dx, dy = shake(t, t_inv, 0.3, 3)
    cv = offset_canvas(cv, dx, dy)
    cv = flash(cv, t, t_inv, (220, 240, 255), 0.5, 0.2)
    return vignette(cv, 0.45)


# =========================================================================== montaje


def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (TL.chapter_start(3) - 0.3, make_card(3, ["EL PRIMER", "INVIERNO"], "1966 – 1980", snow=True, robot_face="sad"),
         None),
        (s("c3_01") - 0.2, sc_promise,
         lambda t: (cam_push(t, w("c3_01", "tres"), e("c3_01"), 1.0, 1.06, (220, 135), (210, 140))[0]
                    + cam_punch(t, [w("c3_01", k) for k in ("tres", "ocho", "años")], 0.04)
                    + cam_punch(t, [w("c3_02", "llegan")], 0.06), 220, 138)),
        (w("c3_02", "llegan") + 0.65, sc_alpac,
         lambda t: (1.0 + cam_punch(t, [w("c3_02", "no estaba")], 0.1), 300, 135)),
        (s("c3_03") - 0.2, sc_lighthill,
         lambda t: (1.0 + cam_punch(t, [w("c3_03", "demoledor")], 0.1), 300, 120)),
        (s("c3_04") - 0.2, sc_explosion,
         lambda t: (cam_push(t, w("c3_04", "programas"), w("c3_04", "explosion"), 1.0, 1.12, (240, 135))[0]
                    + cam_punch(t, [w("c3_04", "explosion")], 0.12), 240, 135)),
        (s("c3_05") - 0.2, sc_cuts,
         lambda t: (1.0 + cam_punch(t, [w("c3_05", "recorta") + 0.05], 0.05)
                    + cam_punch(t, [w("c3_05", "reduce")], 0.1), 240, 135)),
        (s("c3_06") - 0.2, sc_empty,
         lambda t: cam_push(t, s("c3_06"), e("c3_06"), 1.0, 1.08, (240, 120), (240, 120))),
        (s("c3_07") - 0.2, sc_freeze,
         lambda t: (cam_push(t, s("c3_07"), e("c3_07") + 0.4, 1.0, 1.1, (240, 140))[0]
                    + cam_punch(t, [w("c3_07", "invierno")], 0.08), 240, 140)),
    ]


# =========================================================================== audio


def music(A):
    s, e, w = TL.s, TL.e, TL.word
    t0 = TL.chapter_start(3) + 1.6
    t_end = chapter_end(3) - 0.2
    c_alp = w("c3_02", "llegan") + 0.65
    A.section(t0, c_alp, 88, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("A", "min")], A.st_mystery)
    A.section(c_alp, s("c3_04") - 0.2, 76, [("E", "min"), ("C", "maj"), ("A", "min"), ("B", "min")], A.st_winter)
    A.section(s("c3_04") - 0.2, w("c3_04", "explosion"), 96, [("E", "min"), ("C", "maj"), ("D", "maj"), ("B", "min")],
              A.st_build)
    tx = w("c3_04", "explosion")
    A.kick(A.music, tx, 0.5)
    A.crash(A.music, tx, 0.14)
    A.note(A.music, tx, A.midi_hz(40), 1.8, "tri", vol=0.28, s=0.9, r=0.6)
    # riser durante la explosión del árbol
    tt = w("c3_04", "programas") - 0.2
    k = 0
    while tt < tx:
        p = (tt - (w("c3_04", "programas") - 0.2)) / max(0.1, tx - w("c3_04", "programas") + 0.2)
        A.note(A.music, tt, A.midi_hz(64 + [0, 3, 7, 12][k % 4] + int(p * 12)), 0.06, duty=0.125, vol=0.035, s=0.4)
        tt += 0.14 - 0.08 * p
        k += 1
    A.section(tx + 0.9, s("c3_07") - 0.1, 72, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "min")], A.st_winter)
    A.section(s("c3_07") - 0.1, t_end, 60, [("A", "min"), ("F", "maj")], A.st_winter)
    ti = w("c3_07", "invierno")
    A.sting(ti, [88, 84, 81, 76], inst_duty=0.125, vol=0.035, step=0.12, hold=1.6)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    A.wind(TL.chapter_start(3) + 0.2, chapter_end(3) - 0.3, 0.03)
    # promesas
    t_prom = w("c3_01", "promesas")
    for i in range(4):
        A.pop_sfx(t_prom + 0.05 + i * 0.4, 600 + i * 90, 0.045)
    for i in range(8):
        A.blip(t_prom + i * 0.12, 500 + i * 90, 0.05, 0.025, 0.25)
    A.pop_sfx(w("c3_01", "mil") - 0.05, 420, 0.06)
    A.join_jingle(w("c3_01", "Minsky") - 0.1, 0.05)
    for k in ("tres", "ocho", "años"):
        A.pop_sfx(w("c3_01", k), 700, 0.05)
    for i in range(8):
        A.blip(w("c3_01", "ocho") + i * (1.4 / 8), 1100, 0.025, 0.03)
    A.text_blips(w("c3_01", "inteligencia") - 0.1, 20, 26, 0.016)
    A.text_blips(w("c3_01", "promedio") - 0.2, 21, 30, 0.012, 1800)
    for i in range(5):
        A.blip(s("c3_02") + 0.1 + i * 0.3, 900 - i * 80, 0.03, 0.03)
    A.whoosh(w("c3_02", "resultados") - 0.2, 0.3, 0.04)
    A.kick(A.sfx, w("c3_02", "llegan"), 0.35)
    # ALPAC
    A.pop_sfx(w("c3_02", "mil novecientos") - 0.05, 420, 0.06)
    A.pop_sfx(w("c3_02", "ALPAC") - 0.15, 600, 0.05)
    t_in = w("c3_02", "concluido") - 0.5
    A.typewriter(t_in, t_in + 1.25, 16, 0.035)
    A.robot_beep(w("c3_02", "traduccion") - 0.1, 0.035)
    for i in range(8):
        A.blip(w("c3_02", "traduccion") + i * 0.1, 400 + (i * 370) % 900, 0.04, 0.025, 0.125)
    t_out = w("c3_02", "automatica") + 0.3
    A.typewriter(t_out, t_out + 1.2, 16, 0.035)
    A.kick(A.sfx, w("c3_02", "no estaba"), 0.45)
    A.note(A.sfx, w("c3_02", "no estaba"), 120, 0.25, duty=0.5, vol=0.05, s=0.8, r=0.05)
    A.text_blips(w("c3_02", "igualar") - 0.1, 29, 30, 0.014)
    A.note(A.sfx, w("c3_02", "traductor") + 0.4, 160, 0.14, duty=0.5, vol=0.045, s=0.8, r=0.02)
    # Lighthill
    A.pop_sfx(s("c3_03") + 0.02, 420, 0.06)
    A.join_jingle(w("c3_03", "James") - 0.1, 0.05)
    A.pop_sfx(w("c3_03", "gobierno") - 0.1, 650, 0.045)
    A.whoosh(w("c3_03", "demoledor") - 0.35, 0.35, 0.06)
    A.kick(A.sfx, w("c3_03", "demoledor"), 0.5)
    A.snare(A.sfx, w("c3_03", "demoledor"), 0.12)
    # explosión combinatoria
    t0 = s("c3_04")
    for i in range(4):
        A.text_blips(t0 + i * 0.25, 16, 40, 0.012)
    for k in (t0 + 0.6, w("c3_04", "no cumplio"), w("c3_04", "no cumplio") + 0.45, w("c3_04", "objetivos")):
        A.note(A.sfx, k, 150, 0.14, duty=0.5, vol=0.045, s=0.8, r=0.02)
    A.whoosh(w("c3_04", "programas") - 0.5, 0.4, 0.04)
    for L in range(1, 7):
        tl = w("c3_04", "programas") - 0.2 + L * 0.42
        for j in range(min(L * 2, 8)):
            A.blip(tl + j * 0.03, 600 + L * 160 + j * 40, 0.02, 0.02, 0.25)
    tx = w("c3_04", "explosion")
    A.kick(A.sfx, tx, 0.5)
    A.crash(A.sfx, tx, 0.15)
    A.whoosh(tx, 0.8, 0.07)
    # recortes
    t_rec = w("c3_05", "recorta")
    for k in range(3):
        A.blip(t_rec - 0.3 + k * 0.16, 3000, 0.02, 0.04)
    A.pop_sfx(t_rec + 0.05, 300, 0.06)
    A.whoosh(t_rec + 0.1, 0.5, 0.04)
    A.pop_sfx(w("c3_05", "Al") - 0.05, 420, 0.05)
    A.pop_sfx(w("c3_05", "Estados") - 0.1, 600, 0.04)
    A.join_jingle(w("c3_05", "DARPA") - 0.1, 0.04)
    A.pop_sfx(w("c3_05", "tambien") - 0.2, 500, 0.04)
    tr = w("c3_05", "reduce")
    A.kick(A.sfx, tr, 0.5)
    A.snare(A.sfx, tr, 0.1)
    for i in range(8):
        A.blip(tr + 0.1 + i * 0.1, 1200 - i * 120, 0.06, 0.03, 0.25)
    # laboratorio vacío
    t0 = s("c3_06")
    for k in range(12):
        sig_t = t0 - 0.1 + k * 0.33
        A.blip(sig_t, 90, 0.03, 0.03, 0.5)
    for k in range(4):
        A.blip(w("c3_06", "vacian") - 0.2 + k * 0.12, 2000, 0.015, 0.02)
    A.note(A.sfx, w("c3_06", "investigadores"), 140, 0.3, "tri", vol=0.15, s=0.6, r=0.2)
    A.chalk(w("c3_06", "cambian", occurrence=2) - 0.05, w("c3_06", "cambian", occurrence=2) + 0.3)
    A.whoosh(w("c3_06", "nombre"), 0.3, 0.05)
    A.coin(w("c3_06", "nombre") + 0.3, 0.05)
    # invierno
    A.wind(s("c3_07") - 0.3, chapter_end(3) - 0.3, 0.05)
    A.freeze(w("c3_07", "invierno"))
    A.text_blips(e("c3_07") - 0.4, 11, 24, 0.014, 1900)
