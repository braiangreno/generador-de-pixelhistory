"""Capítulo 3: Dos dólares por día (Nueva York, Edison, las zanjas y el Huevo de Colón)."""
import math
from PIL import Image, ImageDraw
from common import *  # noqa


def c3_s01_ny_harbor(t):
    """2:48 - 2:56: Barco de vapor entra al puerto de Nueva York; el joven baja con su valija."""
    cv = bg("bg_ny_harbor_1884").copy()
    t0 = TL.s("c3_01")
    t_ny = TL.word("c3_01", "Nueva")
    t_edi = TL.word("c3_01", "Edison")

    draw_chapter_header(cv, t, t0, 3, "DOS DÓLARES POR DÍA", "NUEVA YORK · 1884", border=AMBER)

    x_inv, w_inv = walk(t, t0, t_edi, 92, 216)
    char(cv, "inventor_hat", x_inv, 250, t, scale=2, walk=w_inv, arms="hold", look=1, mood="happy")
    # Pequeña valija de cuero en su mano
    d = ImageDraw.Draw(cv)
    vx = int(x_inv) + 14
    d.rectangle([vx, 216, vx + 16, 228], fill=(122, 74, 36, 255), outline=(*INK, 255))
    d.rectangle([vx + 5, 213, vx + 11, 216], fill=(82, 48, 22, 255))

    if t >= t_edi - 0.35:
        a, dy = pop(t, t_edi - 0.35)
        window(cv, 248, 72 + dy, 198, 52, fill=(22, 18, 28), border=GOLD)
        draw_text(cv, "THOMAS EDISON", 347, 82 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "EL INVENTOR MÁS FAMOSO", 347, 98 + dy, "silk", 8, CREAM, align="center")
        char(cv, "edison_gen", 364, 250, t, alpha=a, scale=2, arms="down", look=-1)

    return vignette(cv, 0.35)


def c3_s02_edison_workshop(t):
    """2:56 - 3:16: Taller con generadores de continua, contador de US$50.000, promesa rota y renuncia."""
    cv = bg("bg_edison_workshop_1884").copy()
    t0 = TL.s("c3_02")
    t_50k = TL.word("c3_02", "cincuenta")
    t_c3_03 = TL.s("c3_03")
    t_cob = TL.word("c3_03", "cobrar")
    t_bro = TL.word("c3_03", "broma")
    t_ren = TL.word("c3_03", "Renuncio")

    draw_place_only(cv, "TALLER DE EDISON · NUEVA YORK", t, t0, border=GOLD)

    # Lámparas colgantes cálidas (dentro de x=136..344 para escala 1:1 en 9:16)
    for lx in (144, 240, 336):
        bulb(cv, lx, 48, t, on=1.0 if t < t_bro else 0.45)

    # Contador US$50.000 en pizarra de oficina
    if t >= t_50k - 0.35:
        a, dy = pop(t, t_50k - 0.35)
        cnt_p = clamp01((t - (t_50k - 0.2)) / 1.1)
        val_num = 0 if t >= t_bro else int(round(50000 * cnt_p))
        val_str = f"US${val_num:,}".replace(",", ".")
        border_c = CHALK_RED if t >= t_bro else GOLD
        window(cv, 122, 64 + dy, 236, 56, fill=(18, 22, 34), border=border_c)
        draw_text(cv, "PROMESA POR MEJORAR DÍNAMOS:", 240, 72 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, val_str, 240, 88 + dy, "press", 16, border_c, align="center", outline_w=2)

    # Personajes: el joven trabajando de madrugada -> broma -> se pone el sombrero y sale
    if t < t_cob:
        char(cv, "edison_gen", 136, 250, t, scale=2,
             arms="point" if t >= t_50k else "down", look=1,
             talk=talk_v(t, t_50k - 0.2 <= t < t_c3_03))
        char(cv, "inventor", 322, 250, t, scale=2,
             arms="work" if t >= t_c3_03 else "down", look=-1, mood="neutral")
    else:
        char(cv, "edison_gen", 148, 250, t, scale=2,
             arms="shrug" if t >= t_bro else "down", look=1,
             mood="happy" if t >= t_bro else "neutral",
             talk=talk_v(t, t_cob <= t < t_ren))
        if t_bro - 0.1 <= t < t_ren:
            bubble(cv, "¡ERA UNA BROMA!", 148, 138)
        x_exit, w_exit = walk(t, t_ren - 0.1, t_ren + 1.1, 296, 412)
        char(cv, "inventor_hat" if t >= t_ren - 0.15 else "inventor",
             x_exit, 250, t, scale=2, walk=w_exit,
             arms="down", look=1 if t >= t_ren else -1, mood="sad")

    return vignette(cv, 0.36)


def c3_s03_winter_ditch(t):
    """3:16 - 3:35: Calle de Nueva York en invierno cavando zanjas por US$2 al día; el capataz lo escucha."""
    cv = bg("bg_ny_winter_ditch_1886").copy()
    SNOW.draw(cv, t, density=0.45)
    t0 = TL.s("c3_04")
    t_zanja = TL.word("c3_04", "zanjas")
    t_dos = TL.word("c3_04", "dos")
    t_c3_05 = TL.s("c3_05")
    t_inv = TL.word("c3_05", "inversores")

    draw_place_only(cv, "NUEVA YORK · INVIERNO", t, t0, border=TESLA_CYAN)

    # Cartel contador US$2 POR DÍA
    if t >= t_dos - 0.25 and t < t_c3_05 + 0.4:
        a, dy = pop(t, t_dos - 0.25)
        window(cv, 128, 52 + dy, 224, 52, fill=(18, 24, 38), border=AMBER)
        draw_text(cv, "CAVANDO ZANJAS EN LA CALLE", 240, 60 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "US$2 POR DÍA", 240, 76 + dy, "press", 16, AMBER, align="center", outline_w=2)

    # Obreros en la zanja
    char(cv, "worker_a", 104, 252, t, scale=2, arms="work" if t < t_c3_05 else "down", look=1)
    inv_arms = "work" if t < t_c3_05 else "point"
    char(cv, "inventor_ditch", 212, 252, t, scale=2, arms=inv_arms, look=1,
         mood="sad" if t < t_c3_05 else "happy",
         talk=talk_v(t, t >= t_c3_05))

    if t >= t_c3_05 - 0.15:
        # A la hora del almuerzo dibuja las 4 flechas en la tierra y el jefe de obra se acerca
        x_fm, w_fm = walk(t, t_c3_05 - 0.1, t_inv, 368, 296)
        char(cv, "foreman", x_fm, 250, t, scale=2, walk=w_fm,
             arms="point_l" if t >= t_inv - 0.2 else "down", look=-1, mood="happy")
        a, dy = pop(t, t_c3_05)
        window(cv, 146, 52 + dy, 188, 66, fill=(58, 42, 26), border=GOLD)
        draw_text(cv, "DIBUJO EN LA TIERRA", 240, 60 + dy, "silk", 8, CREAM, align="center")
        draw_rotating_arrows(cv, 240, 92 + dy, 18, t, speed=2.4, color=GOLD, sand_groove=True)
        if t >= t_inv - 0.2:
            bubble(cv, "TE PRESENTARÉ INVERSORES", int(x_fm), 136)

    return vignette(cv, 0.38)


def c3_s04_egg_of_columbus(t):
    """3:35 - 4:05: Sala de inversores, el Huevo de Colón en cobre que gira y se para solo sobre el imán invisible."""
    cv = bg("bg_investors_room_1887").copy()
    t0 = TL.s("c3_06")
    t_c3_07 = TL.s("c3_07")
    t_enc = TL.word("c3_07", "encendio")
    t_par = TL.word("c3_07", "parado")
    t_c3_08 = TL.s("c3_08")
    t_din = TL.word("c3_08", "dinero")
    t_c3_09 = TL.s("c3_09")

    if t >= t_c3_09 - 0.1:
        cv = grade(cv, mul=(0.55, 0.58, 0.68))

    draw_place_only(cv, "EL HUEVO DE COLÓN · 1887", t, t0, border=GOLD)

    # Mesa de madera central (x=156..324, y=188..248)
    d = ImageDraw.Draw(cv)
    d.rectangle([156, 188, 324, 198], fill=(118, 68, 34, 255), outline=(*INK, 255))
    d.rectangle([168, 198, 312, 248], fill=(78, 44, 22, 255), outline=(*INK, 255))

    # Estado del huevo de cobre sobre la mesa
    if t < t_enc:
        spin_spd = 0.0
        upright = 0.0
    else:
        spin_spd = 4.0 + 10.0 * clamp01((t - t_enc) / 1.5)
        upright = ease_out(clamp01((t - (t_par - 0.5)) / 0.8))

    draw_copper_egg(cv, 240, 186, t, spin_speed=spin_spd, upright=upright, scale=2)

    # En c3_08: debajo de la mesa, en transparencia, las cuatro flechas giran
    if t >= t_c3_08 - 0.15:
        d.rectangle([182, 202, 298, 244], fill=(16, 28, 46, 215), outline=(*TESLA_CYAN, 255))
        draw_rotating_arrows(cv, 240, 223, 17, t, speed=4.2, color=TESLA_CYAN, glow=GOLD)

    # Tarjeta superior explicativa / remate
    if t < t_c3_07:
        window(cv, 118, 48, 244, 48, fill=(24, 18, 28), border=AMBER)
        draw_text(cv, "LEYENDA DE COLÓN:", 240, 56, "silk", 8, AMBER, align="center")
        draw_text(cv, "PARÓ EL HUEVO APLASTÁNDOLO", 240, 72, "press", 8, CREAM, align="center")
    elif t < t_c3_09 - 0.1:
        window(cv, 116, 48, 248, 52, fill=(18, 24, 38), border=GOLD)
        lbl_top = "IMÁN INVISIBLE BAJO LA MESA" if t >= t_c3_08 else "HUEVO DE COBRE + ALTERNA"
        lbl_bot = "¡PUSIERON EL DINERO!" if t >= t_din else "GIRA HASTA QUEDAR PARADO"
        draw_text(cv, lbl_top, 240, 56, "silk", 8, TESLA_CYAN, align="center")
        draw_text(cv, lbl_bot, 240, 74, "press", 8, GOLD, align="center")
    else:
        a, dy = pop(t, t_c3_09 - 0.1)
        window(cv, 108, 52 + dy, 264, 58, fill=(16, 14, 26), border=GOLD)
        draw_text(cv, "COLÓN TUVO QUE ROMPERLO", 240, 62 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "TESLA LO HIZO BAILAR", 240, 80 + dy, "press", 8, GOLD, align="center")

    # Personajes: Tesla a la izquierda de la mesa y 3 inversores a la derecha
    char(cv, "inventor", 112, 250, t, scale=2,
         arms="point" if t >= t_c3_07 else "wave", look=1,
         mood="happy", talk=talk_v(t, t < t_c3_07))

    inv_mood = "happy" if t >= t_par else "worried"
    inv_arms = "cheer" if t >= t_din else "down"
    char(cv, "investor_a", 356, 250, t, scale=2, arms=inv_arms, look=-1, mood=inv_mood)
    char(cv, "investor_b", 398, 252, t, scale=2, arms=inv_arms, look=-1, mood=inv_mood)
    char(cv, "investor_c", 438, 250, t, scale=2, arms="down", look=-1, mood=inv_mood)

    return vignette(cv, 0.38)


def scenes():
    return [
        (TL.s("c3_01") - 0.15, c3_s01_ny_harbor,
         lambda t: cam_push(t, TL.s("c3_01"), TL.s("c3_02"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_02") - 0.15, c3_s02_edison_workshop,
         lambda t: cam_push(t, TL.s("c3_02"), TL.s("c3_04"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_04") - 0.15, c3_s03_winter_ditch,
         lambda t: cam_push(t, TL.s("c3_04"), TL.s("c3_06"), 1.0, 1.03, (240, 135)), "ch03"),
        (TL.s("c3_06") - 0.15, c3_s04_egg_of_columbus,
         lambda t: cam_push(t, TL.s("c3_06"), TL.s("c4_01"), 1.0, 1.035, (240, 145)), "ch03"),
    ]


def music(A):
    """Acto 1 final: de la dureza del invierno en Nueva York al asombro mágico del Huevo de Colón."""
    t0 = TL.s("c3_01")
    t_egg = TL.s("c3_06")
    t_end = TL.s("c4_01")
    beat = 60.0 / 96.0
    chords = [[196.0, 233.08, 293.66], [174.61, 220.0, 261.63], [146.83, 174.61, 220.0], [164.81, 207.65, 246.94]]
    mel = [392.0, 466.16, 440.0, 392.0, 349.23, 329.63, 293.66, 329.63]
    t = t0
    idx = 0
    while t < t_egg:
        ch = chords[idx % len(chords)]
        A.add_pad(t, min(beat * 4, t_egg - t), ch, amp=0.038)
        for b in range(4):
            nt = t + b * beat
            if nt >= t_egg:
                break
            A.add_note(nt, beat * 0.8, mel[(idx * 4 + b) % len(mel)], wave="triangle", amp=0.05)
            A.add_bass(nt, beat * 0.9, ch[0] * 0.5, amp=0.048)
        t += beat * 4
        idx += 1

    # En la escena del Huevo de Colón: zumbido creciente + arpegio brillante
    A.add_pad(t_egg, t_end - t_egg, [110.0, 220.0, 329.63], amp=0.046)
    arp_egg = [440.0, 554.37, 659.25, 880.0]
    t = t_egg
    step = 0
    while t < t_end:
        A.add_note(t, 0.28, arp_egg[step % 4], wave="triangle", amp=0.045)
        t += 0.32
        step += 1


def sfx(A):
    A.fx_thud(TL.s("c3_01"), 0.09)
    A.fx_pop(TL.word("c3_02", "cincuenta"), 0.09)
    A.fx_thud(TL.word("c3_03", "Renuncio"), 0.10)
    A.fx_pop(TL.word("c3_04", "dos"), 0.08)
    A.fx_sweep(TL.word("c3_07", "encendio"), 0.9, 110, 440, 0.08)
    A.fx_chime(TL.word("c3_07", "parado"), 0.12)
