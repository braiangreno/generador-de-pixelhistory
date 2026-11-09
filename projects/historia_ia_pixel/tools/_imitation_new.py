def scaled(cv, fn, w, h, x, y, k=2):
    """Dibuja con fn(img) en un lienzo chico (w x h) y lo pega ampliado x k (pixel art)."""
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fn(tmp)
    a = upscale(np.array(tmp), k)
    paste_arr(cv, a, x, y)


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


