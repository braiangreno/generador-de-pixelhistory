"""Capítulo 6: El mago (Mark Twain en el laboratorio, LA PIZARRA: Resonancia y el barco radiocontrolado de 1898)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c6_s01_twain_and_coil(t):
    """6:34 - 6:56: Laboratorio de Nueva York con Mark Twain, la plataforma vibratoria y la Bobina de Tesla."""
    cv = bg("bg_tesla_lab_ny_1894").copy()
    t0 = TL.s("c6_01")
    t_twain = TL.word("c6_01", "Tuein")
    t_c6_02 = TL.s("c6_02")
    t_vib = TL.word("c6_02", "vibraba")
    t_bano = TL.word("c6_02", "baño")
    t_c6_03 = TL.s("c6_03")
    t_bob = TL.word("c6_03", "bobina")

    draw_place_only(cv, "LABORATORIO DE NUEVA YORK · 1894", t, t0, border=TESLA_VIOLET)
    d = ImageDraw.Draw(cv)

    if t < t_c6_02:
        # Mark Twain sosteniendo un aro luminoso frente a la cámara; Tesla sonríe detrás
        char(cv, "inventor", 174, 248, t, scale=2, arms="offer", look=1, mood="happy")
        char(cv, "writer_twain", 284, 248, t, scale=2, arms="hold", look=-1, mood="happy")

        # Aro luminoso sostenido en las manos de Twain
        def _draw_twain_ring(target_cv, fx, fy):
            d_r = ImageDraw.Draw(target_cv)
            glow(target_cv, fx - 18, fy - 36, 22, TESLA_CYAN, 0.65)
            d_r.ellipse([fx - 28, fy - 46, fx - 8, fy - 26], outline=(*TESLA_SPARK, 255), width=2)

        floor_prop(cv, _draw_twain_ring, 284, 248)
        if t >= t_twain - 0.3:
            a, dy = pop(t, t_twain - 0.3)
            window(cv, 128, 56 + dy, 224, 42, fill=(18, 24, 38), border=GOLD)
            draw_text(cv, "INVITADO: MARK TWAIN", 240, 64 + dy, "silk", 8, GOLD, align="center")
            draw_text(cv, "EL ESCRITOR Y EL INVENTOR", 240, 80 + dy, "silk", 8, CREAM, align="center")
    elif t < t_c6_03:
        # Plataforma vibratoria sobre el suelo: Twain vibra y luego sale corriendo hacia la derecha
        def _draw_vib_platform(target_cv, fx, fy):
            d_p = ImageDraw.Draw(target_cv)
            d_p.rectangle([fx - 36, fy - 6, fx + 36, fy + 4], fill=(82, 64, 44, 255), outline=(*GOLD, 255))

        floor_prop(cv, _draw_vib_platform, 280, 248)
        char(cv, "inventor", 164, 248, t, scale=2, arms="point", look=1, mood="happy")
        if t < t_bano - 0.35:
            vib_dy = int(3 * math.sin(t * 58)) if t >= t_vib - 0.2 else 0
            char(cv, "writer_twain", 280, 242 + vib_dy, t, scale=2, arms="up", look=-1, mood="surprised")
            if t >= t_vib - 0.2:
                bubble(cv, "¡BZZZ!", 280, 134)
        else:
            x_run, w_run = walk(t, t_bano - 0.35, t_c6_03 - 0.1, 280, 430)
            char(cv, "writer_twain", x_run, 248, t, scale=2,
                 walk=(w_run * 1.8 if w_run is not None else None), arms="up", look=1, mood="surprised")
            bubble(cv, "¡AL BAÑO!", min(350, int(x_run)), 134)
    else:
        # Bobina de Tesla central apoyada sobre su base en el suelo lanzando arcos violetas y celestes
        def _draw_tesla_coil(target_cv, fx, fy):
            d_c = ImageDraw.Draw(target_cv)
            d_c.ellipse([fx - 26, fy - 4, fx + 26, fy + 4], fill=(0, 0, 0, 110))
            d_c.rectangle([fx - 22, fy - 8, fx + 22, fy], fill=(74, 48, 28, 255), outline=(*INK, 255))
            d_c.rectangle([fx - 14, fy - 92, fx + 14, fy - 8], fill=(116, 68, 38, 255), outline=(*GOLD, 255))
            for ry in range(fy - 86, fy - 10, 6):
                d_c.line([(fx - 12, ry), (fx + 12, ry)], fill=(214, 146, 74, 255), width=1)
            d_c.ellipse([fx - 26, fy - 106, fx + 26, fy - 88], fill=(186, 198, 214, 255), outline=(*TESLA_CYAN, 255))
            glow(target_cv, fx, fy - 100, 56, TESLA_VIOLET, 0.55)
            draw_tesla_sparks(target_cv, fx, fy - 100, t, radius=58, count=6, color=TESLA_CYAN)

        floor_prop(cv, _draw_tesla_coil, 240, 248)
        window(cv, 124, 52, 232, 42, fill=(18, 22, 38), border=TESLA_CYAN)
        draw_text(cv, "LA BOBINA DE TESLA", 240, 60, "press", 8, TESLA_CYAN, align="center")
        draw_text(cv, "CORRIENTE DE ALTA FRECUENCIA", 240, 76, "silk", 8, CREAM, align="center")
        char(cv, "inventor", 142, 248, t, scale=2, arms="point", look=1, mood="happy")

    return vignette(cv, 0.34)


def c6_s02_pizarra_resonancia(t):
    """6:56 - 7:12: LA PIZARRA · RESONANCIA (el columpio empujado a tiempo y las dos bobinas en sintonía)."""
    cv = Image.new("RGBA", (W, H), (14, 28, 22, 255))
    t0 = TL.s("c6_04")
    t_res = TL.word("c6_04", "resonancia")
    t_c6_05 = TL.s("c6_05")
    t_chis = TL.word("c6_05", "chispas")

    draw_pizarra_frame(cv, "LA PIZARRA · RESONANCIA", t, t0)
    d = ImageDraw.Draw(cv)

    if t < t_c6_05:
        # Paso 1 (c6_04): El columpio de tiza que sube cada vez más alto con empujoncitos a tiempo
        window(cv, 118, 44, 244, 156, fill=(18, 36, 28), border=CHALK_YELLOW)
        draw_text(cv, "COMO EMPUJAR UN COLUMPIO:", 240, 52, "silk", 8, CHALK_YELLOW, align="center")

        # Soporte superior del columpio
        px, py = 240, 76
        d.line([(204, py), (276, py)], fill=(*CHALK_WHITE, 255), width=2)
        # Amplitud creciente con el tiempo
        prog = clamp01((t - t0) / 5.0)
        max_ang = 0.28 + 0.62 * prog
        ang = math.sin((t - t0) * 3.4) * max_ang
        rope_l = 68
        sx = int(px + math.sin(ang) * rope_l)
        sy = int(py + math.cos(ang) * rope_l)
        d.line([(px, py), (sx, sy)], fill=(*CHALK_WHITE, 255), width=2)
        d.rectangle([sx - 8, sy - 3, sx + 8, sy + 3], fill=(*CHALK_YELLOW, 255))
        # Arco punteado mostrando que llega más alto
        d.arc([px - rope_l, py - rope_l, px + rope_l, py + rope_l], 25, 155, fill=(*CHALK_CYAN, 180))

        # Flecha de empujón justo en el extremo izquierdo
        draw_text(cv, "EMPUJÓN ->", 160, 118, "silk", 8, CHALK_GREEN, align="center")
        if t >= t_res - 0.3:
            draw_text(cv, "ESO ES RESONANCIA", 240, 174, "press", 8, CHALK_CYAN, align="center")
        draw_chalk_hand(cv, sx + 10, sy + 6, t)
    else:
        # Paso 2 (c6_05): Dos bobinas en resonancia + Sello EN UNA FRASE: EMPUJAR EN EL MOMENTO JUSTO
        window(cv, 118, 42, 244, 114, fill=(18, 36, 28), border=CHALK_CYAN)
        draw_text(cv, "LA BOBINA EMPUJA LA ELECTRICIDAD", 240, 50, "silk", 8, CHALK_CYAN, align="center")

        # Bobina 1 (pulsos pequeños a tiempo)
        d.rectangle([144, 84, 168, 132], fill=(28, 56, 44, 255), outline=(*CHALK_YELLOW, 255))
        draw_text(cv, "PULSOS", 156, 136, "silk", 8, CHALK_YELLOW, align="center")

        # Ondas resonantes creciendo hacia la Bobina 2
        for k in range(3):
            wx = 178 + k * 24
            wh = 8 + k * 10
            d.arc([wx, 108 - wh, wx + 18, 108 + wh], -70, 70, fill=(*CHALK_CYAN, 255))

        # Bobina 2 (alta, acumula voltaje enorme y lanza chispas)
        d.rectangle([264, 72, 292, 132], fill=(28, 56, 44, 255), outline=(*CHALK_WHITE, 255))
        d.ellipse([256, 64, 300, 76], fill=(*CHALK_CYAN, 255))
        if t >= t_chis - 0.6:
            draw_tesla_sparks(cv, 278, 68, t, radius=32, count=5, color=CHALK_YELLOW)
        draw_text(cv, "¡VOLTAJE ENORME!", 284, 136, "silk", 8, CHALK_GREEN, align="center")

        # Sello en una frase
        a, dy = pop(t, t_c6_05 + 0.6)
        window(cv, 118, 162 + dy, 244, 46, fill=(22, 48, 36), border=CHALK_GREEN)
        draw_text(cv, "EN UNA FRASE:", 240, 169 + dy, "silk", 8, CHALK_GREEN, align="center")
        draw_text(cv, "EMPUJAR EN EL MOMENTO JUSTO", 240, 185 + dy, "silk", 8, CHALK_WHITE, align="center")

    return vignette(cv, 0.24)


def c6_s03_radio_boat(t):
    """7:12 - 7:45: Madison Square Garden 1898; el barquito de hierro radiocontrolado y el control remoto."""
    cv = bg("bg_madison_pond_1898").copy()
    t0 = TL.s("c6_06")
    t_c6_07 = TL.s("c6_07")
    t_luc = TL.word("c6_07", "luces")
    t_c6_08 = TL.s("c6_08")
    t_ond = TL.word("c6_08", "ondas")
    t_c6_09 = TL.s("c6_09")

    draw_place_only(cv, "MADISON SQUARE GARDEN · 1898", t, t0, border=TESLA_CYAN)
    d = ImageDraw.Draw(cv)

    # Estanque de agua enmarcado en piedra + barquito de hierro navegando sobre el agua
    d.rectangle([166, 194, 314, 218], fill=(22, 58, 92, 255), outline=(140, 150, 168, 255))
    bx = int(240 + 42 * math.sin((t - t0) * 1.15))
    by = 198 + int(2 * math.sin(t * 4.2))
    # Olas de agua alrededor del casco
    d.line([(bx - 26, by + 10), (bx + 26, by + 10)], fill=(*TESLA_CYAN, 220), width=1)
    # Casco de hierro + antena
    d.polygon([(bx - 24, by), (bx + 24, by), (bx + 18, by + 10), (bx - 18, by + 10)],
              fill=(72, 82, 98, 255), outline=(*CREAM, 255))
    d.rectangle([bx - 8, by - 6, bx + 8, by], fill=(104, 116, 134, 255), outline=(*INK, 255))
    d.line([(bx, by - 6), (bx, by - 22)], fill=(*GOLD, 255), width=2)
    d.ellipse([bx - 2, by - 24, bx + 2, by - 20], fill=(*TESLA_CYAN, 255))

    # Luces del barco parpadeando en respuesta al público (c6_07)
    lights_on = (t >= t_c6_07 and int(t * 6) % 2 == 0)
    if lights_on:
        glow(cv, bx - 14, by - 2, 12, GOLD, 0.8)
        glow(cv, bx + 14, by - 2, 12, GOLD, 0.8)
        d.ellipse([bx - 16, by - 4, bx - 12, by], fill=(*GOLD, 255))
        d.ellipse([bx + 12, by - 4, bx + 16, by], fill=(*GOLD, 255))

    # Tesla a la izquierda operando su cajita de radio con palanca en las manos
    char(cv, "inventor", 122, 248, t, scale=2, arms="hold", look=1, mood="happy")

    def _draw_radio_box(target_cv, fx, fy):
        d_b = ImageDraw.Draw(target_cv)
        d_b.rectangle([fx + 12, fy - 36, fx + 30, fy - 24], fill=(116, 68, 36, 255), outline=(*GOLD, 255))
        d_b.line([(fx + 21, fy - 36), (fx + 21, fy - 46)], fill=(*TESLA_CYAN, 255), width=2)

    floor_prop(cv, _draw_radio_box, 122, 248)

    # Ondas de radio invisibles (arcos de puntitos celestes desde la cajita hasta la antena del barco)
    if t >= t_c6_08 - 0.2:
        for k in range(4):
            prog = ((t * 1.6 + k * 0.25) % 1.0)
            wx = int(146 + (bx - 146) * prog)
            wy = int(202 + (by - 22 - 202) * prog - 12 * math.sin(prog * math.pi))
            d.ellipse([wx - 3, wy - 3, wx + 3, wy + 3], fill=(*TESLA_CYAN, 255))

    # Público asombrado a la derecha
    char(cv, "investor_a", 364, 248, t, scale=2,
         arms="point" if t_c6_07 <= t < t_c6_08 else "down", look=-1, mood="surprised")
    if t_c6_07 <= t < t_c6_08:
        bubble(cv, "¿CON LA MENTE?", 352, 134)

    # Ventana informativa superior (dentro de x=120..360)
    if t >= t_c6_09:
        a, dy = pop(t, t_c6_09)
        window(cv, 120, 52 + dy, 240, 54, fill=(16, 24, 42), border=GOLD)
        draw_text(cv, "PRIMER RADIO-CONTROL (1898)", 240, 60 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "CONTROL REMOTO", 240, 78 + dy, "press", 8, GOLD, align="center")
    elif t >= t_c6_08:
        window(cv, 120, 52, 240, 44, fill=(16, 24, 42), border=TESLA_CYAN)
        draw_text(cv, "ONDAS DE RADIO DESDE UNA CAJITA", 240, 60, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, "SIN UN SOLO CABLE", 240, 76, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.32)


SCENES = [
    (TL.s("c6_00") - 0.15, TL.s("c6_01"), make_card(6, ["EL MAGO"], "1894 – 1898 · NUEVA YORK")),
    (TL.s("c6_01") - 0.15, TL.s("c6_04"), c6_s01_twain_and_coil),
    (TL.s("c6_04"), TL.s("c6_06"), c6_s02_pizarra_resonancia),
    (TL.s("c6_06"), TL.s("c7_00"), c6_s03_radio_boat),
]


def scenes():
    return [(s[0], s[2], None) for s in SCENES]


def music(A):
    """Acto 2/3: El Mago de Nueva York + La Pizarra 3 (Resonancia) + El barco radiocontrolado."""
    t0 = TL.s("c6_00")
    t_piz = TL.s("c6_04")
    t_boat = TL.s("c6_06")
    t_end = TL.s("c7_00")
    A.add_pad(t0, t_piz - t0, [146.83, 220.0, 277.18, 329.63], amp=0.04)
    piz_beat = 60.0 / 112.0
    piz_arp = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46]
    t = t_piz
    step = 0
    while t < t_boat:
        f_n = piz_arp[step % len(piz_arp)]
        A.add_note(t, piz_beat * 0.42, f_n, wave="pulse25", amp=0.042)
        t += piz_beat * 0.5
        step += 1
    A.add_pad(t_boat, t_end - t_boat, [130.81, 196.0, 261.63, 329.63], amp=0.042)


def sfx(A):
    A.fx_pop(TL.word("c6_01", "Tuein"), 0.08)
    A.fx_sweep(TL.word("c6_02", "vibraba"), 0.6, 90, 260, 0.08)
    A.fx_sparkle(TL.word("c6_03", "bobina"), 0.11)
    A.fx_chime(TL.word("c6_04", "resonancia"), 0.11)
    A.fx_pop(TL.s("c6_08"), 0.09)
    A.fx_chime(TL.s("c6_09"), 0.11)

