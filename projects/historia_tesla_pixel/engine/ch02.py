"""Capítulo 2: El dibujo en la arena (Budapest + La Pizarra 1: Dos corrientes)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c2_s01_budapest_obsessed(t):
    """1:40 - 1:47: Central telefónica antigua en Budapest; el joven termina enfermo de obsesión."""
    cv = bg("bg_budapest_telegraph_1881").copy()
    t0 = TL.s("c2_01")
    t_obs = TL.word("c2_01", "obsesionado")
    t_enf = TL.word("c2_01", "enfermo")

    draw_place_only(cv, "BUDAPEST, HUNGRÍA · 1881", t, t0, border=AMBER)

    # Escritorio con lámpara y pilas de planos descartados apoyado en el suelo
    def _draw_desk_buda(canvas, cx, fy):
        d_b = ImageDraw.Draw(canvas)
        shadow_ellipse(canvas, cx, fy, 52, 5, 80)
        d_b.rectangle([cx - 52, fy - 46, cx + 52, fy - 38], fill=(116, 76, 42, 255), outline=(*INK, 255))
        d_b.rectangle([cx - 46, fy - 38, cx - 38, fy], fill=(78, 50, 28, 255), outline=(*INK, 255))
        d_b.rectangle([cx + 38, fy - 38, cx + 46, fy], fill=(78, 50, 28, 255), outline=(*INK, 255))
        for i, dx_p in enumerate((-38, -22, 16, 30)):
            draw_paper(canvas, cx + dx_p, fy - 58 - (i % 2) * 3, 14, 11)
    floor_prop(cv, _draw_desk_buda, 240, 248)

    # Ventana superior mostrando los intentos fallidos del motor
    if t >= t_obs - 0.2:
        a, dy = pop(t, t_obs - 0.2)
        window(cv, 120, 56 + dy, 240, 68, fill=(20, 18, 32), border=AMBER)
        draw_text(cv, "OBSESIÓN · MOTOR SIN CHISPAS", 240, 64 + dy, "silk", 8, AMBER, align="center")
        draw_text(cv, "INTENTO #47 · #82 · #119", 240, 82 + dy, "press", 8, CREAM, align="center")
        if t >= t_enf - 0.15:
            draw_text(cv, "AGOTAMIENTO EXTREMO", 240, 102 + dy, "press", 8, CHALK_RED, align="center")

    # Operador al fondo y el joven inventor en el escritorio
    char(cv, "student_b", 92, 248, t, scale=2, arms="type", look=1)
    sick = t >= t_enf - 0.1
    char(cv, "inventor", 240, 248, t, scale=2,
         arms="shrug" if sick else "write",
         mood="sad" if sick else "worried", look=0)
    if sick:
        bubble(cv, "...", 240, 138)

    return vignette(cv, 0.38)


def c2_s02_park_revelation(t):
    """1:47 - 2:06: Paseo por el parque de Budapest recitando a Goethe -> relámpago de inspiración -> dibujo en la arena."""
    cv = bg("bg_budapest_park_sunset").copy()
    t0 = TL.s("c2_02")
    t_fausto = TL.word("c2_02", "Fausto")
    t_c2_03 = TL.s("c2_03")
    t_rel = TL.word("c2_03", "relampago")
    t_pal = TL.word("c2_03", "palito")
    t_are = TL.word("c2_03", "arena")

    # Destello en el instante de "como un relámpago"
    if abs(t - t_rel) < 0.22:
        cv = grade(cv, mul=(1.35, 1.30, 1.15), add=(32, 24, 10))

    draw_place_only(cv, "PARQUE DE BUDAPEST", t, t0, border=AMBER)

    x_inv, w_inv = walk(t, t0, t_c2_03, 92, 188)
    x_fri, w_fri = walk(t, t0, t_c2_03, 46, 132)

    if t < t_c2_03:
        inv_arms = "wave" if t >= t_fausto - 0.2 else "down"
        mood_inv = "neutral"
    elif t < t_pal:
        inv_arms = "cheer"
        mood_inv = "happy"
    else:
        inv_arms = "point"
        mood_inv = "happy"

    char(cv, "friend_budapest", x_fri, 250, t, scale=2, walk=w_fri,
         arms="point" if t >= t_pal + 0.4 else "down", look=1, mood="neutral")
    char(cv, "inventor", x_inv, 250, t, scale=2, walk=w_inv,
         arms=inv_arms, look=1, mood=mood_inv,
         talk=talk_v(t, t_fausto - 0.2 <= t < t_c2_03 - 0.15))

    if t_fausto - 0.2 <= t < t_c2_03 - 0.1:
        bubble(cv, "GOETHE · FAUSTO", int(x_inv), 138)
    elif t_c2_03 <= t < t_pal:
        draw_tesla_sparks(cv, int(x_inv), 152, t, rays=4, max_len=28, color=GOLD, core_col=CREAM)
        bubble(cv, "¡LO VEO GIRAR!", int(x_inv), 134, fill=(255, 248, 205))

    # A partir del palito: ventana de arena mostrando el trazado de las 4 flechas
    if t >= t_pal - 0.15:
        def _draw_stick_c2(canvas, cx, fy):
            d_st = ImageDraw.Draw(canvas)
            d_st.line([(cx + 14, fy - 38), (cx + 30, fy - 12)], fill=(172, 122, 64, 255), width=2)
        floor_prop(cv, _draw_stick_c2, x_inv, 250)
        a, dy = pop(t, t_pal - 0.15)
        window(cv, 236, 56 + dy, 216, 136, fill=(74, 50, 26), border=GOLD)
        draw_text(cv, "EL MOTOR EN LA ARENA", 344, 64 + dy, "press", 8, GOLD, align="center")
        p_draw = clamp01((t - t_pal) / max(0.4, (t_are - t_pal + 0.5)))
        draw_rotating_arrows(cv, 344, 130 + dy, 38, t,
                             speed=2.2 if p_draw >= 0.95 else 0.2,
                             color=GOLD, glow=AMBER, progress=p_draw, sand_groove=True)

    return vignette(cv, 0.35)


def c2_s03_pizarra_corrientes(t):
    """2:06 - 2:40: LA PIZARRA · DOS CORRIENTES (Continua = tubería, Alterna = serrucho, 2 alternas = imán que gira)."""
    t0 = TL.s("c2_04")
    t_c2_05 = TL.s("c2_05")
    t_c2_06 = TL.s("c2_06")
    t_c2_07 = TL.s("c2_07")
    t_c2_08 = TL.s("c2_08")

    cv = draw_pizarra_frame(t, t0, "DOS CORRIENTES",
                            summary_es="UN IMÁN QUE GIRA SOLO", t_summary=t_c2_08)
    d = ImageDraw.Draw(cv)

    if t < t_c2_07 - 0.1:
        # Parte A (2:06 - 2:25): Comparación CONTINUA (tubería) vs ALTERNA (serrucho) en dos paneles apilados de 244px
        if t >= t_c2_05 - 0.25:
            a1, dy1 = pop(t, t_c2_05 - 0.25)
            bx, by, bw, bh = 118, 44 + dy1, 244, 72
            window(cv, bx, by, bw, bh, fill=(16, 42, 30), border=CHALK_CYAN, alpha=0.95)
            draw_text(cv, "CONTINUA · AGUA EN TUBERÍA", 240, by + 8, "press", 8, CHALK_CYAN, align="center")
            # Tubería horizontal en tiza
            py = by + 40
            d.line([(bx + 24, py - 9), (bx + bw - 24, py - 9)], fill=(*CHALK_WHITE, 255), width=2)
            d.line([(bx + 24, py + 9), (bx + bw - 24, py + 9)], fill=(*CHALK_WHITE, 255), width=2)
            # Flujo constante hacia la derecha
            for k in range(5):
                wx = bx + 32 + int(((t * 68 + k * 36) % (bw - 68)))
                d.rectangle([wx, py - 3, wx + 10, py + 3], fill=(*CHALK_CYAN, 255))
                d.polygon([(wx + 14, py), (wx + 9, py - 5), (wx + 9, py + 5)], fill=(*CHALK_YELLOW, 255))
            if t < t_c2_06:
                draw_chalk_hand(cv, bx + bw - 34, py + 6, t)

        if t >= t_c2_06 - 0.15:
            a2, dy2 = pop(t, t_c2_06 - 0.15)
            bx, by, bw, bh = 118, 126 + dy2, 244, 74
            window(cv, bx, by, bw, bh, fill=(16, 42, 30), border=CHALK_YELLOW, alpha=0.95)
            draw_text(cv, "ALTERNA · SERRUCHO (VA Y VIENE)", 240, by + 8, "press", 8, CHALK_YELLOW, align="center")
            # Tronco de madera fijo + serrucho que va y viene
            d.rectangle([216, by + 44, 264, by + 62], fill=(138, 92, 48, 255), outline=(*CHALK_WHITE, 255))
            saw_dx = int(round(math.sin(t * 10.0) * 26))
            sx = 240 + saw_dx
            sy = by + 38
            d.polygon([(sx - 34, sy - 5), (sx + 34, sy - 5), (sx + 28, sy + 4), (sx - 28, sy + 4)],
                      fill=(*CHALK_WHITE, 255), outline=(*INK, 255))
            # Mango del serrucho
            d.rectangle([sx - 42, sy - 8, sx - 32, sy + 5], fill=(176, 114, 56, 255), outline=(*INK, 255))
            draw_chalk_hand(cv, sx + 28, sy, t)
        return vignette(cv, 0.25)

    # Parte B (2:25 - 2:40): Anillo de bobinas que se encienden una tras otra + cilindro metálico que gira sin chispas
    a3, dy3 = pop(t, t_c2_07 - 0.1)
    bx, by, bw, bh = 116, 42 + dy3, 248, 160
    window(cv, bx, by, bw, bh, fill=(16, 42, 30), border=CHALK_YELLOW, alpha=0.95)
    draw_text(cv, "2 ALTERNAS = IMÁN QUE GIRA", 240, by + 8, "press", 8, CHALK_YELLOW, align="center")

    cx, cy = 240, by + 86
    # 4 bobinas en cruz encendiéndose en secuencia tipo marquesina
    active_coil = int(t * 5.0) % 4
    coil_pos = [(cx, cy - 48), (cx + 48, cy), (cx, cy + 48), (cx - 48, cy)]
    for idx_c, (qx, qy) in enumerate(coil_pos):
        lit = (idx_c == active_coil)
        col_c = CHALK_YELLOW if lit else (76, 112, 92)
        if lit:
            glow(cv, qx, qy, 14, CHALK_YELLOW, 0.45)
        d.rectangle([qx - 9, qy - 7, qx + 9, qy + 7], fill=(*col_c, 255), outline=(*CHALK_WHITE, 255))

    # Las 4 flechas girando dentro del anillo
    draw_rotating_arrows(cv, cx, cy, 30, t, speed=3.4, color=CHALK_CYAN, progress=1.0)

    # En c2_08: cilindro metálico en el centro persiguiendo al imán invisible, sin chispas
    if t >= t_c2_08 - 0.15:
        rot_ang = t * 3.4
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(192, 204, 218, 255), outline=(*INK, 255))
        rx_end = int(round(cx + math.cos(rot_ang) * 11))
        ry_end = int(round(cy + math.sin(rot_ang) * 11))
        d.line([(cx, cy), (rx_end, ry_end)], fill=(*INK, 255), width=3)
        draw_text(cv, "GIRA SIN CHISPAS", 240, by + 142, "silk", 8, CHALK_CYAN, align="center")

    return vignette(cv, 0.25)


def c2_s04_sand_remate(t):
    """2:40 - 2:48: Vuelta al dibujo en la arena: el motor imposible ya funcionaba (en su cabeza)."""
    cv = bg("bg_budapest_park_sunset").copy()
    t0 = TL.s("c2_09")
    t_cab = TL.word("c2_09", "cabeza")

    draw_place_only(cv, "BUDAPEST · EL MOTOR IMPOSIBLE", t, t0, border=GOLD)

    # Ventana central con el dibujo en la arena girando y la palabra IMPOSIBLE tachada
    a, dy = pop(t, t0 - 0.1)
    window(cv, 118, 40 + dy, 244, 102, fill=(58, 38, 20), border=GOLD)
    draw_rotating_arrows(cv, 240, 78 + dy, 24, t, speed=3.2, color=GOLD, glow=TESLA_CYAN, sand_groove=True)
    draw_text(cv, "IMPOSIBLE -> YA FUNCIONABA", 240, 112 + dy, "silk", 8, GOLD, align="center")
    if t >= t_cab - 0.2:
        draw_text(cv, "POR AHORA, SOLO EN SU CABEZA", 240, 126 + dy, "silk", 8, CREAM, align="center")

    char(cv, "friend_budapest", 142, 250, t, scale=2, arms="down", look=1, mood="happy")
    char(cv, "inventor", 338, 250, t, scale=2, arms="think", look=-1, mood="happy")

    return vignette(cv, 0.35)


def scenes():
    return [
        (TL.s("c2_00") - 0.15, make_card(2, ["EL DIBUJO EN", "LA ARENA"], "1881 – 1882 · BUDAPEST"),
         None, "ch02"),
        (TL.s("c2_01") - 0.15, c2_s01_budapest_obsessed,
         lambda t: cam_push(t, TL.s("c2_01"), TL.s("c2_02"), 1.0, 1.03, (240, 135)), "ch02"),
        (TL.s("c2_02") - 0.15, c2_s02_park_revelation,
         lambda t: cam_push(t, TL.s("c2_02"), TL.s("c2_04"), 1.0, 1.03, (240, 135)), "ch02"),
        (TL.s("c2_04") - 0.15, c2_s03_pizarra_corrientes,
         lambda t: cam_push(t, TL.s("c2_04"), TL.s("c2_09"), 1.0, 1.02, (240, 135)), "ch02"),
        (TL.s("c2_09") - 0.15, c2_s04_sand_remate,
         lambda t: cam_push(t, TL.s("c2_09"), TL.s("c3_00"), 1.0, 1.03, (240, 135)), "ch02"),
    ]


def music(A):
    """Acto 1 + Pulso liviano y juguetón de sintetizador en La Pizarra."""
    t0 = TL.s("c2_01")
    t_piz = TL.s("c2_04")
    t_rem = TL.s("c2_09")
    t_end = TL.s("c3_00")

    # Parte 1: Budapest (melodía contemplativa)
    beat = 60.0 / 92.0
    chords = [[220.0, 261.63, 329.63], [196.0, 246.94, 293.66], [174.61, 220.0, 261.63], [164.81, 207.65, 246.94]]
    mel = [329.63, 392.0, 440.0, 523.25, 493.88, 440.0, 392.0, 329.63]
    t = t0
    idx = 0
    while t < t_piz:
        ch = chords[idx % len(chords)]
        A.add_pad(t, min(beat * 4, t_piz - t), ch, amp=0.036)
        for b in range(4):
            nt = t + b * beat
            if nt >= t_piz:
                break
            A.add_note(nt, beat * 0.8, mel[(idx * 4 + b) % len(mel)], wave="triangle", amp=0.05)
        t += beat * 4
        idx += 1

    # Parte 2: Tema propio de "La Pizarra" (pulso de sintetizador liviano y juguetón)
    piz_beat = 60.0 / 112.0
    piz_arp = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46]
    t = t_piz
    step = 0
    while t < t_rem:
        f_n = piz_arp[step % len(piz_arp)]
        A.add_note(t, piz_beat * 0.42, f_n, wave="pulse25", amp=0.042)
        if step % 2 == 0:
            A.add_bass(t, piz_beat * 0.8, f_n * 0.25, amp=0.045)
        t += piz_beat * 0.5
        step += 1

    # Parte 3: Remate en la arena + zumbido grave de alterna
    A.add_pad(t_rem, t_end - t_rem, [110.0, 220.0, 277.18, 329.63], amp=0.048)


def sfx(A):
    A.fx_thud(TL.s("c2_01"), 0.09)
    A.fx_sparkle(TL.word("c2_03", "relampago"), 0.12)
    A.fx_pop(TL.s("c2_04"), 0.09)
    A.fx_pop(TL.s("c2_06"), 0.08)
    A.fx_chime(TL.s("c2_08"), 0.11)
