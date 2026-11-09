"""Apertura + Capitulo 1 (La pregunta)."""
from common import *  # noqa
# =========================================================================== escenas
# Cada escena: función (t_global) -> Image RGBA 480x270



def sc_office(t):
    """En 1955, cuatro científicos pidieron dinero para un plan audaz."""
    cv = bg("bg_office_1955").copy()
    # lámpara titilando
    if int(t * 7) % 23 == 0:
        cv = grade(cv, mul=(0.93, 0.93, 0.93))
    bigyear(cv, "1955", 240, 30, t, TL.s("s01") + 0.05)
    t_cuatro = TL.word("s01", "cuatro")
    t_dinero = TL.word("s01", "dinero")
    t_audaz = TL.word("s01", "audaz")
    xs = [56, 118, 180, 242]
    for i, k in enumerate(FOUR):
        t0 = t_cuatro - 0.9 + i * 0.22
        x, ph = walk(t, t0, t0 + 1.3, -50 - i * 40, xs[i])
        speaking = (ph is None and t > t0 + 1.3 and int((t - t0) / 0.9) % 4 == i and t < t_audaz)
        arms = "down"
        mood = "neutral"
        if t > t_audaz:
            arms, mood = ("cheer" if i % 2 == 0 else "point"), "happy"
        char(cv, k, x, 266, t, walk=ph, talk=talk_v(t, speaking), arms=arms, mood=mood, scale=3)
        if t > t_audaz + i * 0.07:
            a, dy = pop(t, t_audaz + i * 0.07)
            draw_text(cv, "!", int(x) - 6, 92 + dy, "press", 16, GOLD, alpha=a)
    # solicitud de fondos
    if t > t_dinero - 0.1:
        a, dy = pop(t, t_dinero - 0.1, 0.4)
        x0, y0 = 296, 92 + dy
        window(cv, x0, y0, 176, 46)
        draw_text(cv, "SOLICITUD DE FONDOS", x0 + 10, y0 + 10, "silkb", 8, GOLD, alpha=a)
        draw_text(cv, "FUNDACIÓN ROCKEFELLER", x0 + 10, y0 + 24, "silk", 8, CREAM, alpha=a)
        # monedas
        for j in range(3):
            cx = x0 + 156 + (j % 2) * 8
            cy = y0 + 30 - j * 5 - int(abs(math.sin(t * 5 + j)) * 2)
            d = ImageDraw.Draw(cv)
            d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=(240, 200, 80, 255), outline=(120, 70, 20, 255))
            d.line([(cx - 2, cy), (cx + 2, cy)], fill=(180, 120, 40, 255))
    return vignette(cv, 0.4)


def sc_ten(t):
    """Dos meses de verano, y diez personas, para enseñarle a una máquina a pensar."""
    cv = vgradient((8, 10, 26), (34, 40, 78), 14)
    d = ImageDraw.Draw(cv)
    # piso del escenario
    d.rectangle([0, 206, W, H], fill=(20, 22, 44, 255))
    for i, y in enumerate((206, 214, 226, 242, 262)):
        d.line([(0, y), (W, y)], fill=(40, 46, 86, 255))
    for x in range(-200, W + 200, 40):
        d.line([(W // 2 + (x - W // 2) * 0.35, 206), (x, H)], fill=(30, 34, 66, 255))
    t_dos = TL.s("s02")
    t_diez = TL.word("s02", "diez")
    t_maq = TL.word("s02", "maquina")
    t_pensar = TL.word("s02", "pensar")
    # títulos
    draw_text(cv, "DOS MESES", 240 - 100, 18, "press", 16, CREAM, align="center",
              reveal=(t - t_dos) * 22)
    if t > t_diez:
        draw_text(cv, "·", 240, 18, "press", 16, GOLD, align="center")
        draw_text(cv, "DIEZ PERSONAS", 240 + 118, 18, "press", 16, CREAM, align="center",
                  reveal=(t - t_diez) * 26)
    # calendario de verano
    a, dy = pop(t, t_dos + 0.2, 0.4)
    if a > 0:
        x0, y0 = 22, 46 + dy
        draw_paper(cv, x0, y0, 62, 58)
        d = ImageDraw.Draw(cv)
        d.rectangle([x0 + 1, y0 + 1, x0 + 61, y0 + 13], fill=(200, 70, 60, 255))
        draw_text(cv, "VERANO", x0 + 31, y0 + 4, "silk", 8, CREAM, align="center", outline=None, shadow=False)
        draw_text(cv, "1956", x0 + 31, y0 + 16, "silk", 8, INK, align="center", outline=None, shadow=False)
        weeks = int(prog(t, t_dos + 0.4, t_diez + 0.8) * 8)
        for wk in range(8):
            r, c = wk // 4, wk % 4
            bx, by = x0 + 8 + c * 12, y0 + 30 + r * 12
            d.rectangle([bx, by, bx + 8, by + 8], outline=(120, 110, 100, 255))
            if wk < weeks:
                d.line([(bx + 1, by + 1), (bx + 7, by + 7)], fill=(200, 60, 50, 255))
                d.line([(bx + 7, by + 1), (bx + 1, by + 7)], fill=(200, 60, 50, 255))
        draw_sun(cv, x0 + 62, y0 + 2, 6, t, face=False)
    # diez personas con sus orbes cian
    for i, k in enumerate(S.DARTMOUTH_TEN):
        t0 = t_diez + 0.05 + i * 0.11
        a, dy = pop(t, t0)
        if a <= 0:
            continue
        x = 48 + i * 43
        cv = spotlight(cv, x, 40, 206, 4, 34, strength=0.18 * a)
        char(cv, k, x, 204 + dy, t, alpha=a, mood="happy" if t > t_pensar else "neutral",
             look=(1 if x < 240 else -1) if t > t_maq + 0.3 else 0)
        orb(cv, x, 132 + dy, t, a)
    # la máquina
    if t > t_maq - 0.6:
        x, _ = walk(t, t_maq - 0.6, t_maq + 0.5, W + 30, 240)
        face = "question" if t > t_pensar - 0.1 else "happy"
        robot(cv, x, 256, t, face=face)
        if t > t_pensar + 0.2:
            on = prog(t, t_pensar + 0.2, t_pensar + 0.5)
            bulb(cv, int(x), 196 - int(abs(math.sin(t * 3)) * 2), t, on)
    return vignette(cv, 0.3)


def sc_summer(t):
    """Creían que un verano alcanzaba. Ya pasaron setenta años. Y la historia todavía no terminó."""
    t3 = TL.s("s03")
    t4 = TL.s("s04")
    t_end = TL.word("s04", "termino", end=True)
    p = ease_in_out(prog(t, t4 + 0.2, TL.word("s04", "historia")))
    years = p * 70
    night = sky_cycle(years / 14.0) if p > 0 else 0.0
    base = bg("bg_dartmouth_summer").copy()
    if night > 0.01:
        base = grade(base, mul=(0.35, 0.4, 0.75), add=(4, 6, 24), sat=0.6, k=night)
    cv = base
    # sol / luna en arco
    if p <= 0:
        draw_sun(cv, 62, 44, 14, t)
    else:
        ang = (years / 14.0) % 1.0
        sx = int(-20 + ang * (W + 40))
        sy = int(110 - math.sin(ang * math.pi) * 90)
        if night < 0.6:
            draw_sun(cv, sx, sy, 12, t, face=False)
        else:
            draw_moon(cv, (sx + W // 2) % W, sy)
    # los diez sentados en el pasto
    seat = [(60, 236), (150, 236), (240, 236), (330, 236), (420, 236),
            (30, 264), (105, 264), (195, 264), (285, 264), (375, 264)]
    for i, k in enumerate(S.DARTMOUTH_TEN):
        fade = 1 - prog(t, t4 + 0.2 + i * 0.08, t4 + 0.6 + i * 0.08)
        if fade <= 0:
            continue
        x, feet = seat[i]
        speaking = int(t / 0.7) % 10 == i and t < t4
        char(cv, k, x, feet, t, alpha=fade, sit=True, talk=talk_v(t, speaking), mood="happy",
             arms="think" if i == 3 else "down", scale=2)
    # misión
    if t < t4 + 0.2:
        quest_window(cv, [("MISIÓN:", GOLD), ("ENSEÑAR A PENSAR", CREAM), ("A UNA MÁQUINA", CREAM),
                          ("PLAZO: 1 VERANO", CYAN)], 250, 22, t, t3 + 0.1, w=196)
    else:
        quest_window(cv, [("MISIÓN:", GOLD), ("ENSEÑAR A PENSAR", CREAM), ("A UNA MÁQUINA", CREAM),
                          ("PLAZO: " + ("70 AÑOS..." if p > 0.98 else f"{int(years) + 1} VERANOS"), CYAN)],
                     250, 22, t, t3 + 0.1, w=196)
        if p < 0.15:
            d = ImageDraw.Draw(cv)
            d.line([(258, 66), (380, 66)], fill=(230, 70, 60, 255), width=2)
    # contador de años
    if p > 0:
        year = 1956 + int(round(years))
        draw_text(cv, str(year), 240, 96, "press", 32, align="center", gradient=GOLD_RAMP, outline_w=2)
        bars70(cv, years, t)
    if t > t_end - 0.4:
        a = prog(t, t_end - 0.4, t_end)
        draw_text(cv, "SETENTA AÑOS DESPUÉS", 240, 148, "press", 8, GOLD, align="center", alpha=a)
    return vignette(cv, 0.35)




def sc_title(t):
    """Esta es la historia de la inteligencia artificial."""
    cv = vgradient((4, 4, 12), (22, 26, 58), 12)
    STARS.draw(cv, t)
    bars70(cv, 70, t, y=246, cur_glow=False, alpha=0.8)
    # resplandor del horizonte
    d = ImageDraw.Draw(cv)
    t_hist = TL.word("s05", "historia")
    t_ia = TL.word("s05", "inteligencia")
    t_art = TL.word("s05", "artificial")
    t_end = TL.e("s05")
    draw_text(cv, "LA HISTORIA DE LA", 240, 62, "press", 16, CREAM, align="center",
              reveal=(t - t_hist + 0.2) * 24)
    dx, dy = 0, 0
    if t > t_ia:
        p = prog(t, t_ia, t_ia + 0.25)
        draw_text(cv, "INTELIGENCIA", 240, int(92 - (1 - p) * 30), "press", 32, align="center",
                  gradient=GOLD_RAMP, outline_w=2, alpha=p)
    if t > t_art:
        p = prog(t, t_art, t_art + 0.25)
        draw_text(cv, "ARTIFICIAL", 240, int(134 + (1 - p) * 30), "press", 32, align="center",
                  gradient=GOLD_RAMP, outline_w=2, alpha=p)
        for i in range(6):
            sparkle(cv, 70 + i * 68, 100 + (i % 2) * 52, t + i, 3)
    draw_text(cv, "UN VERANO QUE DURÓ 70 AÑOS", 240, 186, "press", 8, CYAN, align="center",
              reveal=(t - t_end - 0.2) * 30)
    if t > t_end + 0.5:
        robot(cv, 448, 238, t, face="happy", alpha=prog(t, t_end + 0.5, t_end + 0.8))
    for t0 in (t_ia, t_art):
        sx, sy = shake(t, t0 + 0.22)
        dx += sx; dy += sy
    cv = offset_canvas(cv, dx, dy)
    # destello
    for t0 in (t_ia + 0.22, t_art + 0.22):
        if t0 <= t < t0 + 0.15:
            cv = fade_to(cv, (255, 250, 230), 0.35 * (1 - (t - t0) / 0.15))
    return cv


def sc_ch1(t):
    cv = vgradient((2, 2, 8), (14, 16, 36), 10)
    STARS.draw(cv, t * 0.5, alpha=0.6)
    t0 = TL.s("s06") - 0.35
    chapter_card(cv, t, t0, 1, ["LA PREGUNTA"], "1950 – 1956")
    # signo de pregunta flotante
    if t > t0 + 0.6:
        a = prog(t, t0 + 0.6, t0 + 0.9)
        draw_text(cv, "?", 240, 34 + int(math.sin(t * 3) * 3), "press", 24, align="center", gradient=CYAN_RAMP,
                  alpha=a)
    return cv




def sc_turing(t):
    """Turing y la pregunta."""
    cv = bg("bg_turing_study").copy()
    RAIN.draw(cv, t, 200)
    t0 = TL.s("s07")
    t_alan = TL.word("s07", "Alan")
    t_art = TL.word("s07", "articulo")
    t_preg = TL.word("s07", "pregunta")
    t_pue = TL.word("s07", "pueden")
    t_maq = TL.word("s07", "maquinas")
    # 1950 gigante (sale antes de la pregunta)
    if t < t_preg:
        a_out = 1 - prog(t, t_preg - 0.5, t_preg)
        if a_out > 0:
            p = prog(t, t0, t0 + 0.55)
            yy = 26 - (1 - ease_out_back(p, 2.2)) * 50
            draw_text(cv, "1950", 310, int(yy), "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2,
                      alpha=min(p * 3, a_out))
    # Turing
    pose = dict(arms="think", mood="neutral")
    if t > t_art:
        pose = dict(arms="hold", mood="neutral")
    if t > t_preg:
        pose = dict(arms="think", mood="neutral", look=0)
    if t > t_pue:
        pose = dict(arms="point_l", mood="happy")
    char(cv, "turing", 404, 268, t, scale=3, **pose)
    # hoja de papel en la mano
    if t_art < t < t_preg:
        draw_paper(cv, 392, 184, 24, 30)
        for i in range(5):
            ImageDraw.Draw(cv).line([(396, 190 + i * 5), (411, 190 + i * 5)], fill=(120, 120, 140, 255))
    # pregunta en cian
    if t > t_preg + 0.2:
        a, dy = pop(t, t_preg + 0.2)
        bubble(cv, "?", 404, 114 + dy, size=16)
    if t > t_pue - 0.1:
        rv = (t - t_pue + 0.1) * 18
        draw_text(cv, "¿PUEDEN PENSAR", 210, 40, "press", 16, align="center", gradient=CYAN_RAMP, reveal=rv)
        draw_text(cv, "LAS MÁQUINAS?", 210, 64, "press", 16, align="center", gradient=CYAN_RAMP,
                  reveal=(t - t_maq + 0.3) * 18)
    # tarjeta con retrato
    if t > t_alan - 0.2:
        a = prog(t, t_alan - 0.2, t_alan + 0.2)
        off = int((1 - ease_out(a)) * -120)
        portrait_card(cv, "alan_turing", 14 + off, 176)
        tw = 270
        window(cv, 86 + off, 190, tw, 46)
        draw_text(cv, "ALAN TURING", 96 + off, 200, "press", 16, CREAM)
        draw_text(cv, "«COMPUTING MACHINERY AND INTELLIGENCE» · 1950", 96 + off, 220, "silk", 8, GREY)
    return vignette(cv, 0.4)


def booth_bg():
    cv = vgradient((34, 28, 52), (18, 16, 30), 10)
    d = ImageDraw.Draw(cv)
    for x in range(0, W, 16):
        d.line([(x, 0), (x, 236)], fill=(40, 34, 60, 255))
    d.rectangle([0, 236, W, H], fill=(70, 48, 34, 255))
    for y in (242, 252, 266):
        d.line([(0, y), (W, y)], fill=(54, 36, 26, 255))
    # muro divisor de ladrillos
    d.rectangle([160, 0, 178, 238], fill=(96, 48, 40, 255), outline=(*INK, 255))
    for y in range(0, 238, 8):
        off = 0 if (y // 8) % 2 else 4
        d.line([(161, y), (177, y)], fill=(64, 30, 26, 255))
        d.line([(161 + off + 4, y), (161 + off + 4, y + 7)], fill=(64, 30, 26, 255))
    # tabique entre cabinas
    d.rectangle([326, 40, 331, 238], fill=(60, 52, 80, 255), outline=(*INK, 255))
    return cv


def sc_imitation(t):
    """El juego de la imitación."""
    cv = booth_bg()
    t_juego = TL.word("s08", "juego")
    t_si = TL.word("s08", "conversas")
    t_maq = TL.word("s08", "maquina")
    t_dist = TL.word("s08", "distinguirla")
    t_imp = TL.word("s08", "importa")
    reveal = prog(t, t_imp, t_imp + 0.6)
    judge_talk = t_si - 0.2 < t < t_si + 1.2
    look = 0
    if t > t_dist:
        look = 1 if int((t - t_dist) * 2) % 2 == 0 else -1
    char(cv, "judge", 62, 262, t, talk=talk_v(t, judge_talk), look=look, scale=3,
         arms="type" if t_si - 1.0 < t < t_si - 0.2 else "down",
         mood="worried" if t > t_dist else "neutral")
    for label, cx in (("A", 252), ("B", 404)):
        window(cv, cx - 12, 46, 24, 20)
        draw_text(cv, label, cx, 52, "press", 8, GOLD, align="center")
    if reveal < 1:
        silhouette(cv, "human_b", 290, 262, t, scale=3)
        robot(cv, 430, 262, t, sil=True, scale=3)
    if reveal > 0:
        char(cv, "human_b", 290, 262, t, alpha=reveal, mood="happy", talk=0, scale=3)
        robot(cv, 430, 262, t, face="happy", alpha=reveal, scale=3)
    if reveal < 1:
        draw_text(cv, "?", 290, 128, "press", 16, CYAN, align="center")
        draw_text(cv, "?", 430, 156, "press", 16, CYAN, align="center")
    # escritorios delante de los personajes (cubren las piernas)
    desk(cv, 4, 156, 202, 266)
    desk(cv, 182, 322, 202, 266)
    desk(cv, 336, 476, 202, 266)
    scaled(cv, lambda im: terminal(im, 0, 0, t), 31, 27, 96, 148)
    scaled(cv, lambda im: terminal(im, 0, 0, t), 31, 27, 186, 148)
    scaled(cv, lambda im: terminal(im, 0, 0, t), 31, 27, 338, 148)
    if t > t_juego - 0.1:
        a, dy = pop(t, t_juego - 0.1)
        window(cv, 40, 8 + dy, 400, 30)
        draw_text(cv, "EL JUEGO DE LA IMITACIÓN", 240, 16 + dy, "press", 16, align="center", gradient=GOLD_RAMP)
    if t_si - 0.2 < t < t_imp + 0.4:
        bubble(cv, "¿ERES HUMANO?", 66, 104, reveal=(t - t_si + 0.2) * 22)
    if t_maq - 0.1 < t < t_imp + 2.5:
        r = (t - t_maq + 0.1) * 20
        bubble(cv, "SÍ, CLARO.", 270, 104, reveal=r)
        bubble(cv, "SÍ, CLARO.", 420, 104, reveal=r)
    if t > t_dist + 0.3 and t < t_imp + 0.4:
        a, dy = pop(t, t_dist + 0.3)
        draw_text(cv, "?", 62 + int(math.sin(t * 6) * 2), 60 + dy, "press", 16, CYAN, align="center")
    if t > t_imp:
        a = prog(t, t_imp, t_imp + 0.4)
        draw_text(cv, "¿HUMANO O MÁQUINA?", 240, 244, "press", 8, CREAM, align="center", alpha=a)
    return vignette(cv, 0.35)


def sc_dartmouth(t):
    """Cinco años después... firman la propuesta para un taller de verano en Dartmouth."""
    cv = bg("bg_dartmouth_summer").copy()
    draw_sun(cv, 52, 36, 12, t)
    t0 = TL.s("s09")
    names = ["McCarthy", "Minsky", "Shannon", "Rochester"]
    times = [TL.word("s09", n) for n in names]
    t_firman = TL.word("s09", "firman")
    t_dart = TL.word("s09", "Dartmouth")
    t_nombre = TL.word("s10", "nombre", end=True)
    t_doc = TL.word("s10", "documento")
    t_primera = TL.word("s10", "primera")
    bigyear(cv, "1955", 240, 8, t, t0 - 0.1, size=24) if t < times[0] - 0.2 else None
    portraits = ["john_mccarthy", "marvin_minsky", "claude_shannon", "nathaniel_rochester"]
    first = ["JOHN", "MARVIN", "CLAUDE", "NATHANIEL"]
    last = ["McCARTHY", "MINSKY", "SHANNON", "ROCHESTER"]
    xs = [226, 290, 354, 418]
    doc_p = prog(t, t_firman - 0.2, t_firman + 0.4)
    for i, k in enumerate(FOUR):
        tn = times[i]
        x, ph = walk(t, tn - 0.9, tn - 0.05, W + 40, xs[i])
        mood = "happy" if t > tn else "neutral"
        arms = "wave" if tn < t < tn + 0.9 else ("hold" if t > t_firman + 0.3 else "down")
        char(cv, k, x, 266, t, walk=ph, mood=mood, arms=arms, scale=2, facing=-1 if ph is not None else 1)
        # tarjeta con retrato
        if t > tn - 0.1:
            a, dy = pop(t, tn - 0.1, 0.4)
            up = int(ease_in_out(doc_p) * -170)
            cx = 36 + i * 108
            portrait_card(cv, portraits[i], cx, 26 + dy + up)
            draw_text(cv, first[i], cx + 32, 98 + dy + up, "silk", 8, GREY, align="center")
            draw_text(cv, last[i], cx + 32, 108 + dy + up, "press", 8, CREAM, align="center")
    # documento de la propuesta
    if doc_p > 0:
        yoff = int((1 - ease_out(doc_p)) * 160)
        x0, y0 = 128, 8 + yoff
        draw_paper(cv, x0, y0, 224, 150)
        lines = ["A PROPOSAL FOR THE", "DARTMOUTH SUMMER", "RESEARCH PROJECT ON"]
        for i, ln in enumerate(lines):
            draw_text(cv, ln, x0 + 112, y0 + 12 + i * 12, "silk", 8, INK, align="center", outline=None, shadow=False)
        hl = prog(t, t_doc, t_doc + 0.5)
        col = INK if hl <= 0 else (200, 120, 20)
        if hl > 0:
            d = ImageDraw.Draw(cv)
            ww = int(196 * ease_out(hl))
            d.rectangle([x0 + 14, y0 + 46, x0 + 14 + ww, y0 + 60], fill=(255, 226, 120, 255))
        draw_text(cv, "ARTIFICIAL INTELLIGENCE", x0 + 112, y0 + 49, "silkb", 8, col, align="center",
                  outline=None, shadow=False)
        draw_text(cv, "AUGUST 31, 1955", x0 + 112, y0 + 68, "silk", 8, (90, 90, 100), align="center",
                  outline=None, shadow=False)
        sig_names = ["J. McCARTHY", "M. L. MINSKY", "N. ROCHESTER", "C. E. SHANNON"]
        for i in range(4):
            sx, sy = x0 + 16 + (i % 2) * 106, y0 + 94 + (i // 2) * 26
            p = prog(t, t_firman + 0.3 + i * 0.45, t_firman + 0.8 + i * 0.45)
            scribble(cv, sx, sy, 80, p, seed=i * 2.3)
            d = ImageDraw.Draw(cv)
            d.line([(sx, sy + 6), (sx + 84, sy + 6)], fill=(150, 140, 120, 255))
            draw_text(cv, sig_names[i], sx, sy + 9, "silk", 8, (110, 104, 96), outline=None, shadow=False)
        if t > t_primera:
            a, dy = pop(t, t_primera)
            window(cv, x0 + 176, y0 - 8 + dy, 80, 18, fill=(150, 40, 40), border=GOLD)
            draw_text(cv, "¡1ª VEZ!", x0 + 216, y0 - 3 + dy, "press", 8, CREAM, align="center")
            for i in range(4):
                sparkle(cv, x0 + 20 + i * 60, y0 + 44 + (i % 2) * 18, t + i, 3, GOLD)
    lower_third(cv, "DARTMOUTH COLLEGE", "PROPUESTA DE 1955 · TALLER DE VERANO DE 1956", t, t_dart - 0.3,
                t_nombre + 0.6, x=16, y=232)
    return vignette(cv, 0.3)


def sc_board(t):
    """... un nombre: inteligencia artificial."""
    cv = bg("bg_classroom_1956").copy()
    d = ImageDraw.Draw(cv)
    # banderín verde de Dartmouth sobre el escudo de la pared
    d.rectangle([434, 50, 479, 110], fill=(232, 210, 170, 255))
    d.polygon([(440, 58), (474, 58), (474, 100), (457, 108), (440, 100)], fill=(0, 105, 62, 255),
              outline=(*INK, 255))
    draw_text(cv, "D", 457, 70, "press", 16, CREAM, align="center")
    t_ia = TL.word("s10", "inteligencia")
    t_art = TL.word("s10", "artificial")
    t_end = TL.e("s10")
    # tiza
    def chalk(text, y, t0, t1):
        n = len(text)
        rv = prog(t, t0, t1) * n
        draw_text(cv, text, 309, y, "press", 16, (236, 240, 230), align="center", outline=None,
                  shadow=False, reveal=rv)
    chalk("INTELIGENCIA", 54, t_ia - 0.05, t_art - 0.05)
    chalk("ARTIFICIAL", 86, t_art - 0.05, t_end + 0.1)
    glow = prog(t, t_end + 0.15, t_end + 0.6)
    if glow > 0:
        draw_text(cv, "INTELIGENCIA", 309, 54, "press", 16, align="center", gradient=GOLD_RAMP, alpha=glow,
                  outline=None, shadow=False)
        draw_text(cv, "ARTIFICIAL", 309, 86, "press", 16, align="center", gradient=GOLD_RAMP, alpha=glow,
                  outline=None, shadow=False)
        for i in range(5):
            sparkle(cv, 220 + i * 44, 50 + (i % 2) * 52, t + i * 0.7, 3, GOLD)
    # personajes
    writing = t_ia - 0.1 < t < t_end + 0.1
    char(cv, "mccarthy", 424, 268, t, arms="point_l" if writing else ("cheer" if glow > 0.5 else "down"),
         mood="happy" if glow > 0 else "neutral", scale=3)
    for i, (k, x) in enumerate((("minsky", 46), ("shannon", 116), ("rochester", 186))):
        cheer = glow > 0.3
        char(cv, k, x, 268 - (int(abs(math.sin(t * 7 + i)) * 10) if cheer else 0), t,
             arms="cheer" if cheer else "down", mood="happy" if cheer else "neutral", look=1, scale=3)
    return vignette(cv, 0.35)




def sc_winter(t):
    """Eran optimistas. Demasiado optimistas. Y lo que vino después..."""
    t11 = TL.s("s11")
    t_dem = TL.word("s11", "Demasiado")
    t12 = TL.s("s12")
    t_ent = TL.word("s12", "enterrar")
    t_siempre = TL.word("s12", "siempre")
    w = ease_in_out(prog(t, t12 - 0.1, t12 + 2.2))  # 0 verano -> 1 invierno
    cv = bg("bg_dartmouth_summer").copy()
    if w > 0:
        cv = grade(cv, mul=(0.78, 0.9, 1.12), add=(36, 46, 70), sat=0.25, k=w)
    if w < 1:
        draw_sun(cv, 60, 40, 14, t, alpha=int(255 * (1 - w)))
    # los diez (dos filas, escala x2)
    pos = [(50, 238), (126, 238), (202, 238), (278, 238), (354, 238), (430, 238),
           (40, 266), (120, 266), (360, 266), (440, 266)]
    for i, k in enumerate(S.DARTMOUTH_TEN):
        leave = prog(t, t_ent - 0.6 + i * 0.08, t_ent - 0.1 + i * 0.08)
        if leave >= 1:
            continue
        hop = 0
        arms, mood = "down", "neutral"
        if t11 - 0.2 < t < t12:
            arms, mood = "cheer", "happy"
            hop = int(abs(math.sin(t * 7 + i * 0.8)) * 10)
        elif t >= t12:
            arms, mood = ("cross", "worried")
            hop = 2 * int(math.sin(t * 40 + i) > 0.6)  # tiritan
        x, feet = pos[i]
        char(cv, k, x + (hop if t >= t12 else 0), feet - (hop if t < t12 else 0), t,
             alpha=1 - leave, arms=arms, mood=mood, scale=2)
    if t11 - 0.2 < t < t12 + 0.4:
        CONF.draw(cv, t - t11 + 0.2)
    # medidor de optimismo
    fill = 0.55 + 0.45 * ease_out(prog(t, t11, t11 + 0.8))
    fill += 0.75 * ease_out(prog(t, t_dem, t_dem + 1.0))
    fill *= 1 - ease_in_out(prog(t, t12 + 0.5, t_ent))
    window(cv, 12, 12, 156, 34)
    draw_text(cv, "OPTIMISMO", 20, 18, "press", 8, CREAM if w < 0.5 else (190, 220, 245))
    d = ImageDraw.Draw(cv)
    d.rectangle([20, 30, 160, 38], fill=(10, 10, 20, 255), outline=(*INK, 255))
    bw = int(140 * fill)
    over = fill > 1.0
    col = GOLD if not over else ((255, 90, 70) if int(t * 8) % 2 else GOLD)
    if w > 0.5:
        col = (120, 180, 230)
    d.rectangle([21, 31, 21 + max(0, bw - 1), 37], fill=(*col, 255), outline=(*INK, 255) if over else None)
    if over and w < 0.5:
        draw_text(cv, "!!", 26 + bw, 26, "press", 8, (255, 90, 70))
    # la idea: texto que se congela y se hunde
    if t > t12 + 0.6:
        a = prog(t, t12 + 0.6, t12 + 1.0)
        sink = ease_in_out(prog(t, t_ent, t_siempre + 0.6)) * 70
        ice = prog(t, t12 + 1.2, t_ent)
        ramp = GOLD_RAMP if ice < 0.5 else ICE_RAMP
        draw_text(cv, "INTELIGENCIA ARTIFICIAL", 240, int(150 + sink), "press", 16, align="center",
                  gradient=ramp, alpha=a)
    # la máquina se congela
    if t > t12 + 0.3:
        a = prog(t, t12 + 0.3, t12 + 0.7)
        frozen = t > t_ent
        robot(cv, 240, 266, t, face="sad" if not frozen else "off", frozen=frozen, alpha=a, scale=2)
    # nieve que cae y se acumula
    if w > 0:
        SNOW.draw(cv, t, density=w)
        acc = ease_in_out(prog(t, t12 + 0.5, t_siempre + 0.8))
        top = int(H - acc * 52)
        a = np.array(cv)
        xs_ = np.arange(W)
        edge = top + (np.sin(xs_ * 0.21) * 2 + np.sin(xs_ * 0.07 + 1) * 3).astype(int)
        for x in range(W):
            e = max(0, edge[x])
            a[e:, x, :3] = (232, 240, 250)
            if e < H:
                a[e, x, :3] = (255, 255, 255)
                if e + 3 < H:
                    a[e + 3:, x, :3] = (214, 226, 242) if (x + e) % 7 else (196, 212, 236)
        cv = Image.fromarray(a, "RGBA")
    return vignette(cv, 0.4)


# =========================================================================== montaje

def scenes():
    """Lista de (inicio, función, cámara) de la apertura y el capítulo 1."""
    w = TL.word
    c = [
        (0.0, sc_office, lambda t: cam_push(t, 0.0, TL.s("s02"), 1.0, 1.12, (240, 150), (170, 170))),
        (TL.s("s02") - 0.2, sc_ten, lambda t: (1.0 + cam_punch(t, [w("s02", "diez") + 0.05 + i * 0.11 for i in range(10)], 0.02)
                                               + cam_punch(t, [w("s02", "pensar") + 0.2], 0.08), 240, 160)),
        (TL.s("s03") - 0.2, sc_summer, lambda t: cam_push(t, TL.s("s03"), TL.s("s04") + 0.3, 1.1, 1.0, (240, 150))),
        (TL.s("s05") - 0.25, sc_title, lambda t: (1.0 + cam_punch(t, [w("s05", "inteligencia") + 0.22,
                                                                   w("s05", "artificial") + 0.22], 0.1), 240, 120)),
        (TL.s("s06") - 0.35, make_card(1, ["LA PREGUNTA"], "1950 – 1956"), None),
        (TL.s("s07") - 0.2, sc_turing, lambda t: cam_push(t, TL.s("s07"), TL.e("s07"), 1.0, 1.08, (240, 135), (232, 145))),
        (TL.s("s08") - 0.2, sc_imitation, lambda t: (1.0 + cam_punch(t, [w("s08", "importa")], 0.1), 240, 150)),
        (TL.s("s09") - 0.2, sc_dartmouth, lambda t: (1.0 + cam_punch(t, [w("s09", n) for n in
                                                                      ("McCarthy", "Minsky", "Shannon", "Rochester")], 0.04), 240, 135)),
        (w("s10", "nombre", end=True) + 0.05, sc_board, lambda t: cam_push(t, w("s10", "nombre"), TL.e("s10") + 0.6,
                                                                         1.0, 1.22, (240, 135), (300, 80))),
        (TL.s("s11") - 0.3, sc_winter, lambda t: cam_push(t, TL.s("s12"), TL.e("s12"), 1.0, 1.15, (240, 135), (240, 190))),
    ]
    return c
