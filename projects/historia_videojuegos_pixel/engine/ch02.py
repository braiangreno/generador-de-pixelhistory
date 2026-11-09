"""Capítulo 2: La caja de monedas (1966 – 1975)."""
from common import *  # noqa

WOOD_LIGHT = (196, 138, 76)
WOOD_MID = (148, 96, 48)
WOOD_DARK = (92, 56, 26)
AMBER = (255, 198, 92)
RED_ALERT = (236, 68, 60)
SILVER = (214, 222, 232)
SILVER_DARK = (128, 138, 152)

C = S.hexc
SKIN = S.SKIN

RALPH_BAER = dict(
    name="Ralph Baer", skin=SKIN["fair"], hair=C("4a3a2e"), hair_style="recede",
    glasses="black", top="shirt", top_color=C("f0ece0"), tie=C("6e3428"), pants=C("463c34"),
)
FATHER_1972 = dict(
    name="Padre 1972", skin=SKIN["fair"], hair=C("5a3822"), hair_style="side",
    mustache=True, top="sweater", top_color=C("c87438"), shirt=C("f4efe2"), pants=C("4e3a2c"),
)
MOTHER_1972 = dict(
    name="Madre 1972", skin=SKIN["light"], hair=C("8a4e28"), hair_style="wavy",
    top="shirt", top_color=C("e2a84c"), skirt=True, skirt_color=C("6a442e"), pants=C("6a442e"),
)
KID_1972 = dict(
    name="Hijo 1972", skin=SKIN["fair"], hair=C("6e4426"), hair_style="fringe",
    top="tshirt", top_color=C("d85a3a"), pants=C("384e68"),
)
NOLAN_BUSHNELL = dict(
    name="Nolan Bushnell", skin=SKIN["fair"], hair=C("5c3c24"), hair_style="wavy",
    beard="short", top="blazer", top_color=C("8c5230"), shirt=C("f2e6cf"), pants=C("3e342c"),
)
AL_ALCORN = dict(
    name="Al Alcorn", skin=SKIN["light"], hair=C("443022"), hair_style="side",
    glasses="wire", beard="mustache", top="shirt", top_color=C("e6dec8"), tie=C("844426"), pants=C("423830"),
)
PATRON_1 = dict(
    name="Cliente Bar 1", skin=SKIN["tan"], hair=C("2c2018"), hair_style="curly",
    mustache=True, top="vest", top_color=C("784828"), shirt=C("ecdcb8"), pants=C("38322e"),
)
PATRON_2 = dict(
    name="Cliente Bar 2", skin=SKIN["fair"], hair=C("7a4e2a"), hair_style="long",
    top="tshirt", top_color=C("b84632"), pants=C("2e3c52"),
)
PATRON_3 = dict(
    name="Cliente Bar 3", skin=SKIN["light"], hair=C("3a2a20"), hair_style="short",
    beard="full", top="shirt", top_color=C("687a52"), pants=C("3a342c"),
)


# =========================================================================== helpers locales


def warm_window(cv, x, y, w, h, border=GOLD, alpha=0.92):
    window(cv, x, y, w, h, fill=(32, 22, 16), border=border, alpha=alpha, inner=(96, 64, 38))


def draw_pong_screen(cv, x0, y0, w, h, t, score_l="07", score_r="08", freeze_at=None, glitch=False):
    """Dibuja una pantalla de Pong (cancha negra, red punteada, paletas blancas, pelota cuadrada y tanteador)."""
    d = ImageDraw.Draw(cv)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 12, 14, 255), outline=(*INK, 255))
    tt = freeze_at if freeze_at is not None else t

    # Línea punteada central
    cx = x0 + w // 2
    step = max(4, h // 12)
    for yy in range(y0 + 4, y0 + h - 4, step):
        d.line([(cx, yy), (cx, min(y0 + h - 4, yy + step // 2))], fill=(220, 224, 218, 255), width=max(1, w // 90))

    # Tanteador superior
    if w >= 90:
        sz = 16 if w >= 220 else 8
        draw_text(cv, score_l, cx - w // 5, y0 + 8, "press", sz, CREAM, align="center", outline=None, shadow=False)
        draw_text(cv, score_r, cx + w // 5, y0 + 8, "press", sz, CREAM, align="center", outline=None, shadow=False)

    # Movimiento de pelota y paletas
    period = 0.85
    u = (tt / period) % 2.0
    px_norm = u if u < 1.0 else (2.0 - u)
    by_norm = 0.5 + 0.36 * math.sin(tt * 3.7)

    pad_h = max(8, h // 5)
    pad_w = max(2, w // 45)
    lx = x0 + max(6, w // 14)
    rx = x0 + w - max(6, w // 14) - pad_w

    ly = int(y0 + (h - pad_h) * (0.5 + 0.34 * math.sin(tt * 3.7 - 0.25)))
    ry = int(y0 + (h - pad_h) * (0.5 + 0.34 * math.sin(tt * 3.7 + 0.2)))
    d.rectangle([lx, ly, lx + pad_w, ly + pad_h], fill=(245, 245, 240, 255))
    d.rectangle([rx, ry, rx + pad_w, ry + pad_h], fill=(245, 245, 240, 255))

    bx = int(lx + pad_w + 2 + (rx - lx - pad_w - 6) * px_norm)
    by = int(y0 + 8 + (h - 16) * by_norm)
    br = max(2, w // 70)
    d.rectangle([bx - br, by - br, bx + br, by + br], fill=(255, 255, 245, 255))

    if glitch:
        # Barras horizontales de interferencia / congelamiento
        for k in range(5):
            gy = y0 + 10 + ((k * 29 + int(t * 25) * 7) % max(8, h - 20))
            gx_off = ((k % 2) * 2 - 1) * 8
            d.rectangle([x0 + 4, gy, x0 + w - 4, gy + 3], fill=(220, 210, 180, 200))
            d.line([(x0 + 2, gy + 1), (x0 + w - 2, gy + 1)], fill=(*RED_ALERT, 220))


def draw_quarter(d, cx, cy, r=5, silver=True, alpha=255):
    """Moneda de 25 centavos (quarter) en pixel art dorada/plateada."""
    fill = (218, 226, 236, alpha) if silver else (244, 204, 88, alpha)
    edge = (118, 128, 144, alpha) if silver else (142, 92, 28, alpha)
    hi = (250, 252, 255, alpha) if silver else (255, 240, 180, alpha)
    d.ellipse([cx - r, cy - r + 1, cx + r, cy + r - 1], fill=fill, outline=edge)
    d.point((cx - r // 2, cy - 1), fill=hi)
    d.line([(cx, cy - r + 3), (cx, cy + r - 3)], fill=edge)


def draw_red_phone(cv, cx, cy, t, ringing=True):
    """Teléfono rojo retro que vibra y emite ondas al sonar."""
    d = ImageDraw.Draw(cv)
    jx = int(math.sin(t * 55) * 3) if ringing else 0
    jy = int(abs(math.cos(t * 55)) * 2) if ringing else 0
    x, y = cx + jx, cy - jy

    # Base trapezoidal roja
    d.polygon([(x - 18, y + 14), (x + 18, y + 14), (x + 12, y - 2), (x - 12, y - 2)],
              fill=(210, 44, 40, 255), outline=(*INK, 255))
    # Disco de marcar
    d.ellipse([x - 7, y + 1, x + 7, y + 12], fill=(242, 236, 224, 255), outline=(*INK, 255))
    d.ellipse([x - 2, y + 5, x + 2, y + 8], fill=(210, 44, 40, 255))
    # Tubo / auricular arriba
    hr_y = y - 8 - (2 if ringing and int(t * 18) % 2 == 0 else 0)
    d.rectangle([x - 20, hr_y - 4, x + 20, hr_y + 1], fill=(236, 58, 52, 255), outline=(*INK, 255))
    d.rectangle([x - 22, hr_y - 2, x - 14, hr_y + 4], fill=(180, 32, 30, 255), outline=(*INK, 255))
    d.rectangle([x + 14, hr_y - 2, x + 22, hr_y + 4], fill=(180, 32, 30, 255), outline=(*INK, 255))

    if ringing:
        for r_w in (26, 34):
            if int(t * 12 + r_w) % 2 == 0:
                d.arc([x - r_w, y - r_w, x + r_w, y + r_w], 200, 340, fill=(*GOLD, 255))
        draw_text(cv, "¡RING!", x, y - 30, "press", 8, GOLD, align="center")


# =========================================================================== ESCENAS (c2_01 .. c2_07)


def sc_c2_01_baer(t):
    """c2_01: Taller de Ralph Baer (1966-1968). Prototipo 'Brown Box' conectado al televisor CRT."""
    cv = bg("bg_baer_workshop_1968").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c2_01")
    t_preg = TL.word("c2_01", "pregunta")
    t_tv = TL.word("c2_01", "televisor")
    t_mirar = TL.word("c2_01", "mirar")

    # Pantalla del televisor en el banco de trabajo (x=330..378, y=130..170): pasa de estática a dos cuadrados controlables
    if t < t_preg + 0.4:
        # Líneas de transmisión de TV tradicional
        for yy in range(132, 169, 4):
            c_tv = 170 + ((yy + int(t * 30)) % 40)
            d.line([(332, yy), (376, yy)], fill=(c_tv, c_tv - 15, c_tv - 40, 200))
    else:
        # Dos puntos cuadrados luminosos controlados desde la Brown Box
        d.rectangle([330, 130, 378, 170], fill=(18, 22, 20, 240))
        d.line([(354, 131), (354, 169)], fill=(120, 140, 120, 220))
        y_l = 148 + int(math.sin(t * 4.2) * 10)
        y_r = 148 + int(math.cos(t * 3.6) * 10)
        bx = 340 + int((0.5 + 0.5 * math.sin(t * 5.0)) * 28)
        by = 148 + int(math.sin(t * 5.0) * 8)
        d.rectangle([334, y_l - 4, 337, y_l + 4], fill=(250, 248, 235, 255))
        d.rectangle([371, y_r - 4, 374, y_r + 4], fill=(250, 248, 235, 255))
        d.rectangle([bx - 2, by - 2, bx + 2, by + 2], fill=(*GOLD, 255))

    # Lámpara indicadora encendida en la "Brown Box" (x=212..294, y=138..188)
    if int(t * 4) % 2 == 0:
        d.ellipse([282, 148, 286, 152], fill=(255, 90, 70, 255))

    # Ralph Baer probando las perillas del prototipo
    char(cv, RALPH_BAER, 132, 266, t, scale=3,
         arms="think" if t_preg - 0.2 < t < t_mirar - 0.3 else "type",
         talk=talk_v(t, t0 < t < t_mirar), look=1, mood="happy" if t > t_mirar else "neutral")

    # Globo / ventana con la pregunta clave: "¿POR QUÉ SOLO MIRAR?"
    if t >= t_preg - 0.15:
        a, dy = pop(t, t_preg - 0.15, 0.35)
        warm_window(cv, 44, 14 + dy, 392, 46, border=GOLD)
        draw_text(cv, "40 MILLONES DE TELEVISORES EN EE.UU.", 240, 22 + dy, "silk", 8, GREY, align="center")
        draw_text(cv, "¿POR QUÉ SOLO MIRAR?", 240, 36 + dy, "press", 16, AMBER, align="center",
                  reveal=(t - t_preg) * 24)
        bubble(cv, "¿INTERACTUAR?", 132, 108 + dy, size=8, reveal=(t - t_preg - 0.3) * 24)

    lower_third(cv, "RALPH BAER", "INGENIERO · 1966", t, t0, TL.e("c2_01"), x=16, y=220)
    return vignette(cv, 0.35)


def sc_c2_02_odyssey(t):
    """c2_02: Sala de estar de 1972. Familia jugando ping-pong en la Magnavox Odyssey."""
    cv = bg("bg_living_1972").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c2_02")
    t_proto = TL.word("c2_02", "prototipo")
    t_72 = TL.word("c2_02", "setenta")
    t_ody = TL.word("c2_02", "Odyssey")

    # Consola blanca y negra Magnavox Odyssey sobre la mesa ratona (x=218..264, y=184..200)
    d.rectangle([218, 184, 264, 198], fill=(238, 234, 222, 255), outline=(*INK, 255))
    d.rectangle([226, 186, 256, 192], fill=(28, 26, 30, 255))
    # Cables hacia el televisor y hacia los controles
    d.line([(264, 192), (310, 204), (366, 196)], fill=(40, 36, 34, 255), width=1)

    # Juego de ping-pong brillando en la pantalla del TV del living (x=368..393, y=136..186)
    d.polygon([(368, 136), (393, 142), (393, 188), (368, 180)], fill=(16, 38, 24, 255))
    d.line([(380, 139), (380, 184)], fill=(180, 230, 190, 220))
    by_tv = 158 + int(math.sin(t * 6.0) * 12)
    bx_tv = 372 + int((0.5 + 0.5 * math.cos(t * 6.0)) * 17)
    d.rectangle([370, by_tv - 4, 372, by_tv + 4], fill=(255, 255, 240, 255))
    d.rectangle([389, 162 - (by_tv - 158) - 4, 391, 162 - (by_tv - 158) + 4], fill=(255, 255, 240, 255))
    d.rectangle([bx_tv - 1, by_tv - 1, bx_tv + 1, by_tv + 1], fill=(255, 255, 255, 255))

    # Familia de 1972 jugando frente al televisor
    char(cv, FATHER_1972, 92, 258, t, scale=3, sit=True, arms="hold", facing=1, look=1, mood="happy")
    char(cv, MOTHER_1972, 152, 260, t, scale=3, sit=True, arms="cheer" if int(t * 2) % 2 == 0 else "down",
         facing=1, look=1, mood="happy")
    hop = int(abs(math.sin(t * 7)) * 4)
    char(cv, KID_1972, 304, 262 - hop, t, scale=2, arms="hold", facing=1, look=1, mood="happy")

    # Placa superior: de "PROTOTIPO 'BROWN BOX' · 1968" a "MAGNAVOX ODYSSEY · 1972"
    if t < t_72 - 0.15:
        a, dy = pop(t, t0 + 0.1, 0.3)
        warm_window(cv, 68, 12 + dy, 344, 34, border=GOLD)
        draw_text(cv, "PROTOTIPO «BROWN BOX» · 1968", 240, 23 + dy, "press", 8, AMBER, align="center")
    else:
        a, dy = pop(t, t_72 - 0.15, 0.35)
        warm_window(cv, 36, 12 + dy, 408, 54, border=GOLD)
        draw_text(cv, "MAGNAVOX ODYSSEY · 1972", 240, 22 + dy, "press", 16, gradient=GOLD_RAMP, align="center")
        draw_text(cv, "PRIMERA CONSOLA HOGAREÑA", 240, 44 + dy, "press", 8, CYAN, align="center",
                  reveal=(t - t_72 - 0.1) * 28)
    return vignette(cv, 0.35)


def sc_c2_03_bushnell(t):
    """c2_03: Escena de demostración. El joven Nolan Bushnell observando atentamente el ping-pong; funda Atari."""
    cv = vgradient((24, 16, 12), (48, 30, 20), 12)
    d = ImageDraw.Draw(cv)
    # Piso de salón de demostración de 1972
    d.rectangle([0, 212, W, H], fill=(38, 24, 18, 255))
    for y in (212, 224, 240, 258):
        d.line([(0, y), (W, y)], fill=(62, 40, 28, 255))

    t0 = TL.s("c2_03")
    t_nolan = TL.word("c2_03", "Nolan")
    t_atari = TL.word("c2_03", "Atari")

    # Gran pantalla en primer plano jugando ping-pong electrónico a la derecha
    warm_window(cv, 198, 44, 254, 156, border=GOLD)
    draw_pong_screen(cv, 210, 56, 230, 124, t, score_l="04", score_r="05")
    draw_text(cv, "DEMOSTRACIÓN · PING-PONG", 325, 186, "silk", 8, AMBER, align="center")

    # Nolan Bushnell (scale=3, arms="think") mirando hipnotizado la pantalla
    arms_pose = "cheer" if t >= t_atari - 0.1 else "think"
    char(cv, NOLAN_BUSHNELL, 106, 264, t, scale=3, arms=arms_pose, facing=1, look=1,
         talk=talk_v(t, t_nolan < t < t_atari - 0.3), mood="happy")

    # Bombita de inspiración y placa al fundar Atari
    if t >= t_nolan + 0.3:
        on = prog(t, t_nolan + 0.3, t_nolan + 0.7)
        bulb(cv, 106, 94 - int(abs(math.sin(t * 5)) * 3), t, on)
    if t >= t_nolan + 0.6:
        a, dy = pop(t, t_nolan + 0.6, 0.35)
        warm_window(cv, 20, 10 + dy, 440, 28, border=CYAN)
        draw_text(cv, "SEMANAS DESPUÉS: FUNDA ATARI · 1972", 240, 18 + dy, "press", 8, CYAN, align="center",
                  reveal=(t - t_nolan - 0.6) * 26)

    lower_third(cv, "NOLAN BUSHNELL", "FUNDADOR DE ATARI · 1972", t, t0 + 0.2, TL.e("c2_03"), x=16, y=220)
    return vignette(cv, 0.35)


def sc_c2_04_tavern(t):
    """c2_04: Andy Capp's Tavern (1972). Fila de clientes esperando turno frente al gabinete de madera."""
    cv = bg("bg_tavern_1972").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c2_04")
    t_bar = TL.word("c2_04", "bar")

    # Reemplazamos la pantalla del gabinete del fondo (x=380..430, y=100..144) por Pong en vivo
    draw_pong_screen(cv, 380, 100, 50, 44, t, score_l="11", score_r="09")
    # Marquesina superior del gabinete sin logos, con luz cálida de bar
    d.rectangle([372, 66, 434, 82], fill=(242, 200, 106, 255), outline=(*INK, 255))
    draw_text(cv, "25¢", 403, 70, "press", 8, INK, align="center", outline=None, shadow=False)

    # Fila de parroquianos esperando turno frente a la máquina de monedas
    patrons = [
        (PATRON_3, 64, 260, 0.0),
        (PATRON_2, 134, 262, 0.15),
        (PATRON_1, 206, 264, 0.30),
        (AL_ALCORN, 284, 264, 0.45),
    ]
    for spec, px, pfeet, delay in patrons:
        a, dy = pop(t, t0 - 0.1 + delay, 0.3)
        if a > 0:
            is_front = (px == 284)
            char(cv, spec, px, pfeet + dy, t, scale=3 if is_front else 2, alpha=a,
                 facing=1, look=1, arms="point" if is_front else "hold", mood="happy")
            # Moneda brillante en la mano de los clientes de la fila
            if not is_front:
                draw_quarter(d, px + 14, pfeet - 48 + dy, r=4, silver=(px % 2 == 0))

    warm_window(cv, 16, 12, 448, 34, border=GOLD)
    draw_text(cv, "AL ALCORN · ANDY CAPP'S TAVERN · 1972", 240, 23, "press", 8, AMBER,
              align="center", reveal=(t - t0) * 28)
    return vignette(cv, 0.35)


def sc_c2_05_glitch(t):
    """c2_05: Primer plano del gabinete de madera: la pantalla se congela con falla, teléfono rojo suena."""
    cv = vgradient((26, 16, 12), (14, 10, 8), 10)
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c2_05")
    t_llam = TL.word("c2_05", "llamaron")
    t_andaba = TL.word("c2_05", "andaba")

    # Gabinete arcade de madera en primer plano (x=120..360, y=38..268)
    d.rectangle([116, 38, 364, 268], fill=(*WOOD_MID, 255), outline=(*INK, 255))
    d.rectangle([122, 42, 358, 266], fill=(*WOOD_LIGHT, 255), outline=(*WOOD_DARK, 255))
    for vx in range(130, 355, 16):
        d.line([(vx, 44), (vx, 264)], fill=(*WOOD_MID, 140))

    # Bisel y pantalla CRT congelada con interferencia cuando "no andaba"
    broken = t >= t_llam - 0.1
    d.rectangle([144, 54, 336, 192], fill=(32, 30, 28, 255), outline=(*INK, 255))
    draw_pong_screen(cv, 154, 62, 172, 122, t, score_l="00", score_r="00",
                     freeze_at=(t_llam - 0.1) if broken else None, glitch=broken)

    if broken:
        # Cartel de error parpadeando sobre la pantalla
        if int(t * 7) % 2 == 0:
            window(cv, 176, 106, 128, 32, fill=(90, 18, 18), border=RED_ALERT)
            draw_text(cv, "¡SIN FICHAS!", 240, 116, "press", 8, CREAM, align="center")

    # Panel de control y ranura de monedas atascada abajo
    d.rectangle([136, 198, 344, 222], fill=(40, 38, 36, 255), outline=(*INK, 255))
    d.ellipse([232, 204, 248, 216], fill=(210, 200, 170, 255), outline=(*INK, 255))
    d.rectangle([206, 228, 274, 266], fill=(54, 52, 50, 255), outline=(*INK, 255))
    d.rectangle([236, 236, 244, 250], fill=(*(RED_ALERT if broken else GOLD), 255))

    # Teléfono rojo sonando con sacudida a la izquierda
    if t >= t_llam - 0.25:
        warm_window(cv, 18, 86, 88, 96, border=RED_ALERT)
        draw_red_phone(cv, 62, 142, t, ringing=True)

    # Ventana superior de alerta
    warm_window(cv, 92, 8, 296, 28, border=RED_ALERT if broken else GOLD)
    draw_text(cv, "AVERÍA REPORTADA", 240, 16, "press", 8,
              RED_ALERT if (broken and int(t * 6) % 2 == 0) else CREAM, align="center",
              reveal=(t - t0 + 0.1) * 26)

    dx, dy = shake(t, t_andaba - 0.1, 0.35, 4)
    return vignette(offset_canvas(cv, dx, dy), 0.35)


_COINS_SPEC = [
    (
        (i * 37) % 130 - 65,           # offset X final desde la puerta
        0.55 + ((i * 19) % 10) * 0.08, # velocidad de caída
        (i % 2 == 0),                  # plateada o dorada
        (i * 13) % 28,                 # retraso escalonado
    )
    for i in range(64)
]


def sc_c2_06_coins(t):
    """c2_06: Al Alcorn abre la puerta de madera del monedero y cae una cascada masiva de monedas."""
    cv = vgradient((28, 18, 12), (14, 10, 8), 10)
    d = ImageDraw.Draw(cv)
    # Piso de madera del bar
    d.rectangle([0, 214, W, H], fill=(58, 36, 22, 255))
    for y in (214, 226, 242, 260):
        d.line([(0, y), (W, y)], fill=(38, 22, 14, 255))

    t0 = TL.s("c2_06")
    t_abrio = TL.word("c2_06", "abrio")
    t_monedas = TL.word("c2_06", "monedas")

    # Parte inferior del gabinete de madera de Pong (x=176..388, y=28..236)
    d.rectangle([176, 28, 388, 236], fill=(*WOOD_MID, 255), outline=(*INK, 255))
    d.rectangle([184, 34, 380, 230], fill=(*WOOD_LIGHT, 255), outline=(*WOOD_DARK, 255))
    for vx in range(196, 376, 18):
        d.line([(vx, 36), (vx, 228)], fill=(*WOOD_MID, 150))

    # Cavidad interna del monedero (repleta de monedas brillantes)
    cx_box, cy_box = 282, 138
    d.rectangle([cx_box - 52, cy_box - 56, cx_box + 52, cy_box + 64], fill=(22, 18, 16, 255), outline=(*INK, 255))

    open_p = ease_out(prog(t, t_abrio - 0.2, t_abrio + 0.35))
    if open_p > 0.1:
        # Montaña de monedas desbordando dentro de la caja metálica
        for r_row in range(8):
            for c_col in range(9):
                qx = cx_box - 40 + c_col * 10 + (r_row % 2) * 4
                qy = cy_box + 54 - r_row * 11
                draw_quarter(d, qx, qy, r=5, silver=((r_row + c_col) % 2 == 0))

    # Puerta del monedero que se abre hacia la derecha
    door_w = int(104 * (1.0 - 0.72 * open_p))
    if open_p < 0.25:
        d.rectangle([cx_box - 52, cy_box - 56, cx_box + 52, cy_box + 64], fill=(64, 62, 60, 255), outline=(*INK, 255))
        d.rectangle([cx_box - 12, cy_box - 38, cx_box + 12, cy_box - 14], fill=(42, 40, 38, 255), outline=(*INK, 255))
    else:
        # Puerta abierta en escorzo hacia la derecha
        d.polygon([
            (cx_box + 52, cy_box - 56),
            (cx_box + 52 + max(18, door_w), cy_box - 44),
            (cx_box + 52 + max(18, door_w), cy_box + 74),
            (cx_box + 52, cy_box + 64),
        ], fill=(74, 72, 68, 255), outline=(*INK, 255))

    # Cascada masiva de monedas doradas y plateadas cayendo al piso
    t_cascade = t_abrio + 0.15
    if t >= t_cascade:
        dt = t - t_cascade
        # Pila creciente de monedas en el piso
        pile_p = clamp01(dt / 1.6)
        pile_count = int(42 * pile_p)
        for i in range(pile_count):
            px = cx_box + ((i * 29) % 140) - 70
            py = 244 - (i // 10) * 6 + (i % 3) * 2
            draw_quarter(d, px, py, r=5, silver=(i % 2 == 0))

        # Monedas en el aire cayendo y rebotando
        for dx_end, spd, is_silv, delay_i in _COINS_SPEC:
            ct = (dt - delay_i * 0.035) * spd
            if ct <= 0:
                continue
            u = ct % 1.0
            qx = int(cx_box + dx_end * u)
            qy = int((cy_box + 20) + (242 - (cy_box + 20)) * (u * u) - abs(math.sin(u * math.pi * 2)) * 14 * (1 - u))
            draw_quarter(d, qx, qy, r=5, silver=is_silv)

        for i in range(5):
            sparkle(cv, cx_box - 50 + i * 26, 130 + (i % 2) * 55, t + i * 0.4, 3, GOLD)

    # Al Alcorn a la izquierda sorprendido / festejando el hallazgo
    char(cv, AL_ALCORN, 92, 262, t, scale=3, facing=1, look=1,
         arms="cheer" if t >= t_monedas - 0.2 else "point",
         mood="happy", talk=talk_v(t, t0 < t < t_monedas))

    # Placa bold en pantalla: "ESTABA LLENA DE MONEDAS"
    if t >= t_monedas - 0.45:
        a, dy = pop(t, t_monedas - 0.45, 0.35)
        warm_window(cv, 36, 12 + dy, 408, 44, border=GOLD)
        draw_text(cv, "NO ESTABA ROTA:", 240, 20 + dy, "silk", 8, CREAM, align="center")
        draw_text(cv, "ESTABA LLENA DE MONEDAS", 240, 32 + dy, "press", 16, gradient=GOLD_RAMP, align="center")

    dx, dy = shake(t, t_monedas - 0.1, 0.3, 3)
    return vignette(offset_canvas(cv, dx, dy), 0.35)


def sc_c2_07_pong(t):
    """c2_07: Placa retro icónica de pantalla completa: PONG gigante en el centro, paletas, pelota cuadrada y 07 | 08."""
    cv = new_canvas((8, 10, 14))
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c2_07") - 0.15

    # Marco blanco retro de monitor arcade
    d.rectangle([16, 12, 464, 258], outline=(235, 238, 230, 255), width=2)

    # Red central de trazos blancos verticales
    for yy in range(20, 252, 14):
        d.rectangle([238, yy, 242, yy + 8], fill=(220, 224, 218, 255))

    # Tanteador clásico arriba: 07 | 08
    draw_text(cv, "07", 172, 26, "press", 24, CREAM, align="center", outline=None, shadow=False)
    draw_text(cv, "08", 308, 26, "press", 24, CREAM, align="center", outline=None, shadow=False)

    # Dos paletas blancas verticales a izquierda y derecha
    period = 0.72
    u = ((t - t0) / period) % 2.0
    px_norm = u if u < 1.0 else (2.0 - u)
    by_norm = 0.5 + 0.34 * math.sin((t - t0) * 4.4)

    pad_h, pad_w = 46, 8
    lx, rx = 38, 434
    ly = int(135 - pad_h // 2 + math.sin((t - t0) * 4.4 - 0.2) * 58)
    ry = int(135 - pad_h // 2 + math.sin((t - t0) * 4.4 + 0.2) * 58)
    d.rectangle([lx, ly, lx + pad_w, ly + pad_h], fill=(248, 248, 242, 255))
    d.rectangle([rx, ry, rx + pad_w, ry + pad_h], fill=(248, 248, 242, 255))

    # Pelota cuadrada blanca con estela rebotando entre las dos paletas
    bx = int(lx + pad_w + 6 + (rx - lx - pad_w - 12) * px_norm)
    by = int(44 + 182 * by_norm)
    for k in range(4, 0, -1):
        tu = (((t - t0 - k * 0.03) / period) % 2.0)
        tp = tu if tu < 1.0 else (2.0 - tu)
        tx = int(lx + pad_w + 6 + (rx - lx - pad_w - 12) * tp)
        ty = int(44 + 182 * (0.5 + 0.34 * math.sin((t - t0 - k * 0.03) * 4.4)))
        a_tr = int(130 * (5 - k) / 5)
        d.rectangle([tx - 4, ty - 4, tx + 4, ty + 4], fill=(200, 210, 200, a_tr))
    d.rectangle([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 255, 245, 255))

    # Letras gigantes "PONG" en el centro
    a, dy = pop(t, TL.s("c2_07") - 0.05, 0.35)
    if a > 0:
        window(cv, 116, 94 + dy, 248, 82, fill=(14, 16, 24), border=GOLD, alpha=0.94)
        draw_text(cv, "PONG", 240, 108 + dy, "press", 48, align="center", gradient=GOLD_RAMP, outline_w=2, alpha=a)
        draw_text(cv, "ATARI · 1972 · NACE LA INDUSTRIA", 240, 158 + dy, "silk", 8, CYAN, align="center", alpha=a)
    return vignette(cv, 0.3)


# =========================================================================== MONTAJE (scenes, music, sfx)


def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (TL.chapter_start(2) - 0.3, make_card(2, ["LA CAJA DE MONEDAS"], "1966 – 1975"), None),
        (s("c2_01") - 0.2, sc_c2_01_baer,
         lambda t: cam_push(t, s("c2_01") - 0.2, s("c2_02") - 0.2, 1.0, 1.06, (210, 150), (235, 150))),
        (s("c2_02") - 0.2, sc_c2_02_odyssey,
         lambda t: (1.0 + cam_punch(t, [w("c2_02", "Odyssey")], 0.055), 240, 140)),
        (s("c2_03") - 0.2, sc_c2_03_bushnell,
         lambda t: (1.0 + cam_punch(t, [w("c2_03", "Atari")], 0.065), 240, 145)),
        (s("c2_04") - 0.2, sc_c2_04_tavern,
         lambda t: cam_push(t, s("c2_04") - 0.2, s("c2_05") - 0.2, 1.0, 1.06, (235, 140), (255, 140))),
        (s("c2_05") - 0.2, sc_c2_05_glitch,
         lambda t: (1.0 + cam_punch(t, [w("c2_05", "llamaron"), w("c2_05", "andaba")], 0.06), 240, 135)),
        (s("c2_06") - 0.2, sc_c2_06_coins,
         lambda t: (1.0 + cam_punch(t, [w("c2_06", "monedas")], 0.08), 240, 140)),
        (s("c2_07") - 0.15, sc_c2_07_pong,
         lambda t: (1.0 + cam_punch(t, [w("c2_07", "Pong")], 0.09), 240, 135)),
    ]


def music(A):
    s, e, w = TL.s, TL.e, TL.word
    t0 = TL.chapter_start(2) + 1.6
    # c2_01 & c2_02: taller de Baer y consola hogareña
    A.section(t0, s("c2_03") - 0.2, 106, [("C", "maj"), ("A", "min"), ("F", "maj"), ("G", "maj")], A.st_puzzle)
    # c2_03 & c2_04: Bushnell, Atari y el bar de California (corta abruptamente en c2_05 cuando llaman por la avería)
    A.section(s("c2_03") - 0.2, s("c2_05") - 0.15, 114,
              [("F", "maj"), ("G", "maj"), ("C", "maj"), ("A", "min")], A.st_bright)
    # En c2_05 la música se corta abruptamente ("la máquina no andaba")
    # En c2_06 cuando descubre que estaba llena de monedas y en c2_07 ("Se llamaba Pong") entra triunfo!
    t_triumph = w("c2_06", "monedas") - 0.25
    A.kick(A.music, t_triumph, 0.48)
    A.crash(A.music, t_triumph, 0.16)
    A.section(t_triumph, chapter_end(2) - 0.25, 120,
              [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_triumph)
    A.sting(w("c2_07", "Pong") - 0.05, [72, 76, 79, 84], inst_duty=0.5, vol=0.065, step=0.11, hold=1.1)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    # c2_01: Ralph Baer y la pregunta
    A.pop_sfx(w("c2_01", "pregunta") - 0.1, 620, 0.05)
    for k in range(4):
        A.plic(w("c2_01", "televisor") + 0.2 + k * 0.55, 880 if k % 2 == 0 else 1040, 0.055)

    # c2_02: Magnavox Odyssey
    A.pop_sfx(w("c2_02", "prototipo") - 0.1, 540, 0.05)
    A.join_jingle(w("c2_02", "Odyssey") - 0.1, 0.055)
    for k in range(5):
        A.plic(s("c2_02") + 0.8 + k * 0.7, 940 if k % 2 == 0 else 1120, 0.05)

    # c2_03: Nolan Bushnell funda Atari
    for k in range(5):
        A.plic(s("c2_03") + 0.3 + k * 0.65, 980 if k % 2 == 0 else 1180, 0.055)
    A.coin(w("c2_03", "Atari") - 0.1, 0.065)

    # c2_04: Andy Capp's Tavern (tonos bip-bop de Pong y monedas)
    A.coin(s("c2_04") + 0.25, 0.055)
    tt = s("c2_04") + 0.5
    idx = 0
    while tt < s("c2_05") - 0.25:
        A.plic(tt, 980 if idx % 2 == 0 else 490, 0.07)
        tt += 0.44
        idx += 1

    # c2_05: Avería reportada, teléfono sonando y corte abrupto
    t_llam = w("c2_05", "llamaron")
    A.freeze(t_llam - 0.1, 0.065)
    for k in range(3):
        tb = t_llam + k * 0.48
        A.blip(tb, 1680, 0.06, 0.045)
        A.blip(tb + 0.08, 1920, 0.06, 0.045)

    # c2_06: Abre la puerta y cae la cascada de monedas
    A.whoosh(w("c2_06", "abrio") - 0.1, 0.3, 0.055)
    A.coin_cascade(w("c2_06", "monedas") - 0.3)

    # c2_07: Se llamaba Pong
    A.plic(s("c2_07") - 0.05, 980, 0.08)
    A.plic(w("c2_07", "Pong") + 0.3, 1320, 0.08)
