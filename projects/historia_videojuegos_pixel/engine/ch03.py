"""Capítulo 3: La fiebre y el entierro (1977 – 1985)."""
from common import *  # noqa
import random

RED = (232, 64, 58)
GREEN_CRT = (100, 250, 150)
FIRE_RAMP = [(255, 244, 190), (255, 180, 90), (240, 90, 60), (190, 40, 40)]

KID_A = dict(name="Chico 1", skin=S.SKIN["fair"], hair=S.hexc("4a2e1c"), hair_style="wavy",
             top="tshirt", top_color=S.hexc("d84a3a"), pants=S.hexc("2e4a7a"), shoes=S.hexc("d8d4cc"))
KID_B = dict(name="Chico 2", skin=S.SKIN["tan"], hair=S.hexc("1e1818"), hair_style="curly",
             top="sweater", top_color=S.hexc("e8a838"), shirt=S.hexc("f4f0e6"), pants=S.hexc("3a3a48"))

ARCADE_P1 = dict(name="Arcade 1", skin=S.SKIN["light"], hair=S.hexc("6a3a1e"), hair_style="long",
                 top="hoodie", top_color=S.hexc("2e5a9a"), pants=S.hexc("242634"))
ARCADE_P2 = dict(name="Arcade 2", skin=S.SKIN["olive"], hair=S.hexc("1a1414"), hair_style="short",
                 top="tshirt", top_color=S.hexc("c83a6a"), pants=S.hexc("303446"))
ARCADE_P3 = dict(name="Arcade 3", skin=S.SKIN["brown"], hair=S.hexc("181414"), hair_style="curly",
                 top="shirt", top_color=S.hexc("4aa878"), pants=S.hexc("2a2c38"))


def fmt_dots(n):
    return f"{int(n):,}".replace(",", ".")


def draw_cartridge(cv, x, y, label_col=(220, 70, 50), angle=0, scale=1):
    """Dibuja un cartucho negro de 1977 con etiqueta de color."""
    d = ImageDraw.Draw(cv)
    w, h = 14 * scale, 10 * scale
    d.rectangle([x, y, x + w, y + h], fill=(28, 28, 34, 255), outline=(*INK, 255))
    d.rectangle([x + 2 * scale, y + 2 * scale, x + w - 2 * scale, y + 6 * scale], fill=(*label_col, 255))
    d.line([(x + 3 * scale, y + 4 * scale), (x + w - 3 * scale, y + 4 * scale)], fill=(255, 240, 210, 220))


def draw_joystick_77(cv, x, y):
    """Joystick negro clásico de 1977 con un botón rojo."""
    d = ImageDraw.Draw(cv)
    # base negra
    d.rectangle([x - 8, y, x + 8, y + 6], fill=(26, 26, 32, 255), outline=(*INK, 255))
    d.rectangle([x - 6, y + 1, x + 6, y + 2], fill=(60, 60, 70, 255))
    # botón rojo arriba a la izquierda
    d.rectangle([x - 5, y - 1, x - 3, y + 1], fill=(235, 55, 45, 255))
    # palanca vertical con borde naranja en la base
    d.rectangle([x - 2, y - 1, x + 2, y + 2], fill=(220, 120, 40, 255))
    d.rectangle([x - 1, y - 10, x + 1, y], fill=(32, 32, 38, 255), outline=(*INK, 255))
    d.rectangle([x - 2, y - 12, x + 2, y - 9], fill=(50, 50, 58, 255), outline=(*INK, 255))


def draw_console_77(cv, x, y, active_col=(230, 70, 50)):
    """Consola de 1977 con frente de madera y ranura de cartuchos."""
    d = ImageDraw.Draw(cv)
    # cuerpo negro acanalado
    d.rectangle([x, y, x + 52, y + 20], fill=(28, 28, 34, 255), outline=(*INK, 255))
    for yy in range(y + 3, y + 12, 2):
        d.line([(x + 3, yy), (x + 49, yy)], fill=(48, 48, 56, 255))
    # frente de madera
    d.rectangle([x + 1, y + 13, x + 51, y + 19], fill=(156, 94, 44, 255), outline=(*INK, 255))
    d.line([(x + 2, y + 15), (x + 50, y + 15)], fill=(120, 68, 28, 255))
    # interruptores plateados
    for sx in (x + 6, x + 12, x + 18, x + 34, x + 40, x + 46):
        d.rectangle([sx, y + 8, sx + 1, y + 11], fill=(200, 204, 212, 255))
    # ranura central con cartucho insertado
    d.rectangle([x + 22, y + 5, x + 30, y + 11], fill=(14, 14, 18, 255))
    d.rectangle([x + 23, y + 1, x + 29, y + 9], fill=(36, 36, 44, 255), outline=(*INK, 255))
    d.rectangle([x + 24, y + 2, x + 28, y + 6], fill=(*active_col, 255))


def draw_tv_screen_77(cv, t, mode=0):
    """Dibuja un juego colorido de 1977 en la pantalla del televisor de bg_living_1972."""
    # La pantalla del TV está en x: 368..392, y: 126..182 (en perspectiva oblicua)
    poly = [(369, 125), (392, 133), (392, 184), (369, 171)]
    d = ImageDraw.Draw(cv)
    if mode == 0:
        # Juego de tanques / combate
        d.polygon(poly, fill=(36, 74, 156, 255))
        by = 148 + int(math.sin(t * 6) * 10)
        d.rectangle([373, by, 377, by + 5], fill=(250, 210, 80, 255))
        d.rectangle([385, 160 - (by - 148), 389, 165 - (by - 148)], fill=(100, 240, 130, 255))
        px = 375 + int((t * 35) % 14)
        d.rectangle([px, 152, px + 2, 154], fill=(255, 255, 255, 255))
    elif mode == 1:
        # Juego espacial
        d.polygon(poly, fill=(14, 16, 42, 255))
        for i in range(4):
            iy = 136 + i * 8 + int(math.sin(t * 5 + i) * 2)
            d.rectangle([374 + (i % 2) * 8, iy, 378 + (i % 2) * 8, iy + 3], fill=(255, 90, 120, 255))
        sy = 166
        sx = 374 + int((math.sin(t * 4) * 0.5 + 0.5) * 12)
        d.rectangle([sx, sy, sx + 4, sy + 3], fill=(90, 240, 255, 255))
        ly = 164 - int((t * 60) % 26)
        d.line([(sx + 2, ly), (sx + 2, ly + 4)], fill=(255, 240, 100, 255))
    else:
        # Juego de carreras / aventuras
        d.polygon(poly, fill=(38, 120, 56, 255))
        d.polygon([(376, 129), (385, 132), (388, 181), (373, 173)], fill=(90, 92, 104, 255))
        cy = 160 + int(math.sin(t * 8) * 4)
        d.rectangle([379, cy, 383, cy + 7], fill=(255, 70, 60, 255))


# =========================================================================== ESCENAS

def sc_1977_cartridges(t):
    """c3_01: En 1977, Atari lanzó una consola con cartuchos: una sola máquina, todos los juegos que quisieras."""
    cv = bg("bg_living_1972").copy()
    w = TL.word
    t0 = TL.s("c3_01")
    t_77 = w("c3_01", "setenta")
    t_con = w("c3_01", "consola")
    t_cart = w("c3_01", "cartuchos")
    t_sola = w("c3_01", "sola")
    t_todos = w("c3_01", "todos")

    # Modo de juego cambia dinámicamente para mostrar "todos los juegos que quisieras"
    cart_cols = [(230, 70, 50), (60, 160, 240), (90, 210, 90), (235, 180, 50), (190, 90, 230)]
    mode = int(max(0, t - t_cart) * 1.4) % 3
    active_col = cart_cols[int(max(0, t - t_cart) * 1.4) % len(cart_cols)]

    draw_tv_screen_77(cv, t, mode=mode)
    # Resplandor cálido del televisor hacia la sala
    cv = spotlight(cv, 368, 130, 255, 36, 170, color=(120, 210, 255), strength=0.18)

    d = ImageDraw.Draw(cv)
    # Consola con frente de madera en la alfombra, conectada al TV por un cable negro
    cx_con, cy_con = 278, 224
    d.line([(cx_con + 48, cy_con + 12), (345, 222), (368, 198)], fill=(20, 20, 26, 255), width=2)
    draw_console_77(cv, cx_con, cy_con, active_col=active_col)

    # Cartuchos de colores desparramados en la alfombra
    scattered = [
        (225, 244, (235, 75, 55)),
        (248, 250, (70, 175, 245)),
        (274, 248, (110, 215, 85)),
        (302, 245, (245, 190, 55)),
        (325, 252, (195, 95, 235)),
        (202, 252, (240, 125, 45)),
    ]
    for i, (kx, ky, col) in enumerate(scattered):
        if t >= t0 + i * 0.12:
            draw_cartridge(cv, kx, ky, label_col=col, scale=1)

    # Dos chicos sentados en la alfombra jugando con joysticks de un botón
    j1_bop = int(math.sin(t * 14) * 2)
    j2_bop = int(math.cos(t * 12) * 2)
    char(cv, KID_A, 122, 254, t, scale=3, sit=True, facing=1, arms="hold", mood="happy",
         talk=talk_v(t, t_con < t < t_sola))
    char(cv, KID_B, 188, 258, t, scale=3, sit=True, facing=1, arms="hold", mood="happy",
         talk=talk_v(t, t > t_todos))

    # Cables de los joysticks a la consola y los joysticks en sus manos
    d.line([(134, 214), (210, 236), (cx_con + 6, cy_con + 16)], fill=(22, 22, 28, 255), width=2)
    d.line([(200, 218), (242, 238), (cx_con + 14, cy_con + 16)], fill=(22, 22, 28, 255), width=2)
    draw_joystick_77(cv, 134, 210 + j1_bop)
    draw_joystick_77(cv, 200, 214 + j2_bop)

    # Ventana superior izquierda: placa histórica (dentro de zona segura de zoom)
    a_win, dy_win = pop(t, t0 - 0.1)
    if a_win > 0:
        window(cv, 26, 20 + dy_win, 292, 42)
        draw_text(cv, "1977 · CARTUCHOS INTERCAMBIABLES", 36, 28 + dy_win, "press", 8, GOLD)
        draw_text(cv, "UNA SOLA CONSOLA · TODOS LOS JUEGOS", 36, 44 + dy_win, "silk", 8, CREAM)

    # Galería de cartuchos que aparecen al decir "cartuchos" / "todos los juegos"
    if t >= t_cart - 0.15:
        a_g, dy_g = pop(t, t_cart - 0.15)
        window(cv, 26, 68 + dy_g, 226, 50)
        draw_text(cv, "1 MÁQUINA = INFINITOS JUEGOS", 139, 75 + dy_g, "silk", 8, CYAN, align="center")
        labels = ["COMBATE", "ESPACIO", "CARRERAS", "AVENTURA"]
        for i, (col, lab) in enumerate(zip(cart_cols[:4], labels)):
            appear = prog(t, t_cart + i * 0.22, t_cart + i * 0.22 + 0.2)
            if appear > 0:
                cx_i = 38 + i * 52
                cy_i = 90 + dy_g + int((1 - ease_out_back(appear)) * -8)
                draw_cartridge(cv, cx_i, cy_i, label_col=col, scale=2)
                if i == mode % 4 and t > t_sola:
                    sparkle(cv, cx_i + 14, cy_i + 4, t, 3, GOLD)

    return vignette(cv, 0.32)


def sc_1982_arcade_boom(t):
    """c3_02: Los salones se llenaron de luces y de ruido. En 1983, los videojuegos hogareños ya movían unos 3.200 millones de dólares."""
    cv = bg("bg_arcade_1982").copy()
    w = TL.word
    t0 = TL.s("c3_02")
    t_luces = w("c3_02", "luces")
    t_83 = w("c3_02", "ochenta")
    t_tres = w("c3_02", "tres mil")
    t_mill = w("c3_02", "millones")

    d = ImageDraw.Draw(cv)
    # Luces de neón parpadeantes y pantallas activas en los gabinetes
    neon_cols = [(255, 70, 210), (70, 240, 255), (255, 220, 70), (110, 255, 140)]
    for i, (cab_x, cab_y, cab_w, cab_h) in enumerate([
        (48, 102, 34, 42), (114, 110, 28, 34), (162, 114, 20, 26),
        (398, 110, 28, 36), (442, 100, 32, 44)
    ]):
        c = neon_cols[(i + int(t * 8)) % len(neon_cols)]
        # destellos de píxeles en las pantallas de arcade
        for k in range(4):
            px = cab_x + ((i * 7 + k * 9 + int(t * 20)) % max(4, cab_w - 4))
            py = cab_y + ((i * 11 + k * 7 + int(t * 15)) % max(4, cab_h - 4))
            d.rectangle([px, py, px + 2, py + 2], fill=(*c, 220))

    # Haces de luz de neón en el techo
    pulse_c = neon_cols[int(t * 6) % len(neon_cols)]
    cv = spotlight(cv, 240, 0, 268, 90, 280, color=pulse_c, strength=0.14)

    # Jugadores frente a las máquinas de arcade
    char(cv, ARCADE_P1, 92, 258, t, scale=3, facing=-1, arms="type", mood="happy")
    char(cv, ARCADE_P2, 178, 236, t, scale=2, facing=-1, arms="type", mood="happy")
    char(cv, ARCADE_P3, 376, 252, t, scale=3, facing=1, arms="cheer" if int(t * 3) % 2 else "type", mood="happy")

    # Placa inicial: FIEBRE DEL ARCADE
    if t < t_83 + 0.15:
        a, dy = pop(t, t0 - 0.05)
        window(cv, 110, 14 + dy, 260, 42)
        draw_text(cv, "LA FIEBRE DEL VIDEOJUEGO", 240, 22 + dy, "press", 8, GOLD, align="center")
        draw_text(cv, "SALONES LLENOS · LUCES Y RUIDO", 240, 38 + dy, "silk", 8, CYAN, align="center")

    # Gran tablero contador en 1983: US$ 3.200 MILLONES
    if t >= t_83 - 0.1:
        a, dy = pop(t, t_83 - 0.1)
        wx, wy, ww, wh = 44, 18 + dy, 392, 92
        window(cv, wx, wy, ww, wh, fill=(16, 20, 46), border=GOLD)
        draw_text(cv, "MERCADO EN EE.UU. · PICO HISTÓRICO", 240, wy + 10, "silk", 8, CYAN, align="center")

        p_cnt = ease_out(prog(t, t_83, t_mill + 0.2))
        val = int(round(3200 * p_cnt))
        txt_main = f"1983 · US$ {fmt_dots(val)} MILLONES" if p_cnt >= 0.98 else f"US$ {fmt_dots(val)} MILLONES"
        draw_text(cv, "1983 · US$ 3.200 MILLONES" if p_cnt >= 0.95 else txt_main,
                  240, wy + 28, "press", 16 if len(txt_main) <= 22 else 8,
                  align="center", gradient=GOLD_RAMP, outline_w=2)

        # Barra de fiebre dorada
        bx0, by0, bx1, by1 = wx + 24, wy + 58, wx + ww - 24, wy + 72
        d = ImageDraw.Draw(cv)
        d.rectangle([bx0, by0, bx1, by1], fill=(10, 12, 24, 255), outline=(*INK, 255))
        fill_w = int((bx1 - bx0 - 2) * p_cnt)
        if fill_w > 0:
            d.rectangle([bx0 + 1, by0 + 1, bx0 + 1 + fill_w, by1 - 1], fill=(*GOLD, 255))
            d.rectangle([bx0 + 1, by0 + 1, bx0 + 1 + fill_w, by0 + 4], fill=(255, 245, 190, 255))
        draw_text(cv, "RÉCORD DE VENTAS EN HOGARES Y SALONES", 240, wy + 76, "silk", 8, CREAM, align="center")

        if p_cnt >= 0.95:
            for k in range(4):
                sparkle(cv, wx + 32 + k * 108, wy + 32 + (k % 2) * 14, t + k * 0.8, 3, GOLD)

    return vignette(cv, 0.35)


def sc_1983_crt_shutoff(t):
    """c3_03: Y entonces, todo se vino abajo. (Transición de apagado de TV de tubo CRT)."""
    t0 = TL.s("c3_03")
    t_abajo = TL.word("c3_03", "abajo")
    dt = t - t0

    if dt <= 0:
        base = sc_1982_arcade_boom(t)
        dx, dy = shake(t, t0 - 0.15, 0.25, 4)
        return offset_canvas(base, dx, dy)

    cv = new_canvas((4, 4, 8))
    d = ImageDraw.Draw(cv)

    # Fase 1 (0.0 .. 1.0s): la imagen se sacude y se comprime verticalmente hacia una línea blanca/cian
    if dt < 1.0:
        k = ease_in_out(dt / 1.0)
        base = sc_1982_arcade_boom(t0)
        base = grade(base, mul=(1.2, 0.9, 1.3), add=(30, 20, 40), sat=0.4, k=k * 0.7)
        new_h = max(3, int(H * (1 - k) ** 1.7))
        squished = base.resize((W, new_h), Image.NEAREST)
        y_top = (H - new_h) // 2
        paste(cv, squished, 0, y_top)
        d.rectangle([0, max(0, y_top - 2), W, min(H, y_top + new_h + 2)], outline=(*CYAN, 230))
        if new_h <= 10:
            d.rectangle([0, 134, W, 136], fill=(245, 255, 255, 255))
        dx = int(math.sin(t * 110) * 5 * (1 - k))
        cv = offset_canvas(cv, dx, 0, fill=(4, 4, 8))
    # Fase 2 (1.0 .. 2.3s): la línea horizontal blanca/cian se contrae hacia un punto central brillante
    elif dt < 2.3:
        k = ease_out((dt - 1.0) / 1.3)
        half_w = max(4, int((W // 2) * (1 - k) ** 1.4))
        # halo cian exterior
        d.rectangle([240 - half_w - 8, 131, 240 + half_w + 8, 139], fill=(70, 210, 255, int(130 * (1 - k * 0.4))))
        # línea central blanca incandescente
        d.rectangle([240 - half_w, 133, 240 + half_w, 137], fill=(245, 255, 255, 255))
        draw_phosphor_dot(cv, 240, 135, r=5, color=CYAN)
    # Fase 3 (2.3s+): el único punto de fósforo se apaga dejando la pantalla negra
    else:
        k = clamp01((dt - 2.3) / 0.65)
        r = max(1, int(5 * (1 - k)))
        if k < 0.9:
            draw_phosphor_dot(cv, 240, 135, r=r, color=CYAN)

    # Texto stark arriba de la línea/punto de CRT al decir "todo se vino abajo"
    if t >= t_abajo - 0.35:
        a_t, dy_t = pop(t, t_abajo - 0.35, 0.25)
        window(cv, 44, 46 + dy_t, 392, 38, fill=(24, 10, 16), border=RED)
        draw_text(cv, "TODO SE VINO ABAJO", 240, 58 + dy_t, "press", 16, CREAM, align="center")

    return cv


def sc_1983_bargain_bins(t):
    """c3_04: Demasiadas consolas. Demasiados juegos hechos a las apuradas. La gente dejó de confiar... y dejó de comprar."""
    cv = vgradient((18, 16, 28), (10, 10, 18), 10)
    w = TL.word
    t0 = TL.s("c3_04")
    t_dem = w("c3_04", "Demasiados")
    t_conf = w("c3_04", "confiar")
    t_comp = w("c3_04", "comprar")

    d = ImageDraw.Draw(cv)
    # Pared de tienda abarrotada con 3 estantes repletos de cajas genéricas y consolas clonadas
    shelf_ys = [88, 146, 204]
    box_cols = [
        (170, 56, 52), (56, 112, 168), (148, 118, 48), (96, 64, 140),
        (52, 132, 96), (164, 84, 44), (110, 116, 128), (144, 52, 96)
    ]
    rnd = random.Random(83)
    for s_idx, sy in enumerate(shelf_ys):
        # fondo del estante
        d.rectangle([16, sy - 44, 464, sy], fill=(26, 24, 38, 255))
        # cajas apiladas sin vender
        x = 22
        b_i = 0
        while x < 444:
            bw = 22 + ((s_idx * 7 + b_i * 5) % 8)
            bh = 34 + ((s_idx * 3 + b_i * 11) % 8)
            col = box_cols[(s_idx * 5 + b_i) % len(box_cols)]
            # caja sombreada
            d.rectangle([x, sy - bh, x + bw, sy - 1], fill=(*col, 255), outline=(*INK, 255))
            d.rectangle([x + 2, sy - bh + 3, x + bw - 2, sy - bh + 11], fill=(*shade(col, 1.3), 255))
            d.line([(x + 3, sy - bh + 16), (x + bw - 3, sy - bh + 16)], fill=(230, 225, 210, 190))
            # cartuchos sueltos caídos encima
            if (b_i + s_idx) % 3 == 0:
                draw_cartridge(cv, x + 2, sy - bh - 9, label_col=box_cols[(b_i + 2) % len(box_cols)])
            x += bw + 3
            b_i += 1
        # tabla de la estantería metálica
        d.rectangle([12, sy, 468, sy + 6], fill=(92, 96, 112, 255), outline=(*INK, 255))
        d.line([(14, sy + 1), (466, sy + 1)], fill=(150, 156, 172, 255))

    # Piso de tienda
    d.rectangle([0, 210, W, H], fill=(32, 28, 36, 255))
    for y_fl in (220, 236, 254):
        d.line([(0, y_fl), (W, y_fl)], fill=(24, 20, 28, 255))

    # Comprador que mira con desconfianza y se va sin comprar
    if t >= t_conf - 0.4:
        x_cust, ph = walk(t, t_comp - 0.2, t_comp + 1.8, 370, 520)
        char(cv, "judge", x_cust, 264, t, scale=3, walk=ph,
             facing=1 if ph is not None else -1,
             arms="shrug" if ph is None else "down", mood="sad")
        if t < t_comp:
            bubble(cv, "NI REGALADO...", int(x_cust), 108)

    # Etiquetas rojas parpadeantes de liquidación por toda la estantería
    tags = [
        (36, 56, "LIQUIDACIÓN", t0 + 0.15),
        (210, 52, "-80%", t0 + 0.45),
        (342, 58, "OFERTA", t0 + 0.75),
        (82, 114, "-80%", t_dem + 0.05),
        (246, 112, "LIQUIDACIÓN", t_dem + 0.30),
        (140, 172, "OFERTA", t_conf - 0.10),
        (292, 170, "-90%", t_conf + 0.20),
    ]
    flash_on = (int(t * 7) % 2) == 0
    for tx, ty, txt, t_ap in tags:
        if t >= t_ap:
            a, dy = pop(t, t_ap, 0.22)
            tw, _ = text_size(txt, "press", 8)
            pw = tw + 14
            fill_c = (225, 42, 42) if flash_on else (165, 26, 26)
            border_c = (255, 220, 90) if flash_on else GOLD
            window(cv, tx, ty + dy, pw, 22, fill=fill_c, border=border_c, inner=(255, 110, 90))
            draw_text(cv, txt, tx + pw // 2, ty + 7 + dy, "press", 8, CREAM, align="center")

    # Placa superior explicativa
    window(cv, 14, 10, 452, 32, fill=(16, 18, 36), border=RED)
    draw_text(cv, "SATURACIÓN · CONSOLAS Y JUEGOS A LAS APURADAS", 240, 16, "press", 8, CREAM, align="center")
    draw_text(cv, "NADIE COMPRA · ESTANTERÍAS DESBORDADAS", 240, 29, "silk", 8, GOLD, align="center")

    return vignette(cv, 0.42)


def draw_dump_truck(cv, x, y, tilt_p, t):
    """Dibuja un camión volcador en pixel art inclinando su caja hacia la zanja (izquierda)."""
    d = ImageDraw.Draw(cv)
    # Chasis inferior y ruedas
    d.rectangle([x - 4, y + 20, x + 78, y + 28], fill=(42, 38, 46, 255), outline=(*INK, 255))
    for wx in (x + 8, x + 28, x + 60):
        d.ellipse([wx - 8, y + 20, wx + 8, y + 36], fill=(22, 20, 26, 255), outline=(*INK, 255))
        d.ellipse([wx - 4, y + 24, wx + 4, y + 32], fill=(90, 86, 78, 255))

    # Cabina (derecha, mirando a la derecha)
    d.rectangle([x + 50, y - 4, x + 76, y + 20], fill=(196, 138, 54, 255), outline=(*INK, 255))
    d.rectangle([x + 56, y - 1, x + 73, y + 9], fill=(90, 130, 150, 255), outline=(*INK, 255))
    # Faro encendido
    d.rectangle([x + 75, y + 12, x + 78, y + 16], fill=(255, 240, 170, 255))

    # Caja volcadora (se levanta del lado derecho y vuelca hacia la izquierda x-10)
    lift = int(tilt_p * 22)
    bed_poly = [
        (x - 8, y + 18),                  # abajo-izq (pivote)
        (x + 46, y + 18 - lift),          # abajo-der (se eleva)
        (x + 42, y - 4 - lift),           # arriba-der
        (x - 14, y - 2),                  # arriba-izq
    ]
    # Pistón hidráulico
    d.line([(x + 32, y + 20), (x + 34, y + 16 - lift)], fill=(180, 186, 196, 255), width=3)
    d.polygon(bed_poly, fill=(168, 112, 44, 255), outline=(*INK, 255))
    d.line([bed_poly[3], bed_poly[2]], fill=(214, 156, 74, 255), width=2)


def sc_1983_desert_landfill(t):
    """c3_05: En septiembre de 1983, camiones de Atari descargaron cartuchos sin vender en un basural del desierto de Nuevo México."""
    cv = bg("bg_desert_landfill_1983").copy()
    w = TL.word
    t0 = TL.s("c3_05")
    t_cam = w("c3_05", "camiones")
    t_desc = w("c3_05", "descargaron")
    t_bas = w("c3_05", "basural")

    # Camión volcador posicionado junto al borde derecho de la zanja (x=250, y=146)
    tilt = ease_in_out(prog(t, t0 + 0.3, t_desc + 0.8))
    draw_dump_truck(cv, 248, 146, tilt, t)

    # Cientos de cartuchos cayendo desde la caja del camión hacia la fosa iluminada
    d = ImageDraw.Draw(cv)
    cart_cols = [(220, 70, 50), (70, 160, 230), (220, 175, 55), (100, 195, 90), (185, 85, 210)]
    if tilt > 0.15:
        for i in range(28):
            cyc = ((t - t0) * 1.9 + i * 0.17) % 1.0
            # trayectoria parabólica desde (236, 154) hacia la fosa (110..225, 195..228)
            sx, sy = 236 - (i % 4) * 3, 150 - int(tilt * 6)
            tx = 118 + (i * 19) % 108
            ty = 196 + (i * 13) % 32
            cx = int(sx + (tx - sx) * cyc)
            cy = int(sy + (ty - sy) * cyc - math.sin(cyc * math.pi) * 16)
            col = cart_cols[i % len(cart_cols)]
            d.rectangle([cx, cy, cx + 7, cy + 5], fill=(32, 32, 38, 255), outline=(*INK, 255))
            d.rectangle([cx + 1, cy + 1, cx + 5, cy + 3], fill=(*col, 255))

    # Pila creciente de cartuchos en el fondo de la zanja
    pile_n = int(prog(t, t0 + 0.5, t_bas + 1.5) * 36)
    rnd = random.Random(1983)
    for i in range(pile_n):
        px = 96 + int(rnd.random() * 134)
        py = 198 + int(rnd.random() * 34)
        col = cart_cols[i % len(cart_cols)]
        d.rectangle([px, py, cx_p := px + 8, py + 5], fill=(28, 28, 34, 255), outline=(*INK, 255))
        d.rectangle([px + 1, py + 1, px + 6, py + 3], fill=(*col, 255))

    # Polvo del desierto soplando bajo los reflectores
    for i in range(45):
        dx_p = int((i * 37 + t * (48 + (i % 5) * 12)) % W)
        dy_p = 110 + ((i * 29 + int(math.sin(t * 2 + i) * 6)) % 145)
        alpha_p = 90 + (i % 3) * 45
        d.rectangle([dx_p, dy_p, dx_p + (1 if i % 2 else 2), dy_p], fill=(218, 178, 120, alpha_p))

    # Destacado en primer plano del famoso cartucho de E.T. (1982), ícono del entierro de Atari
    if t >= t0 + 0.55:
        a_et, dy_et = pop(t, t0 + 0.55, 0.35)
        wx, wy, ww, wh = 16, 174 + dy_et, 186, 72
        window(cv, wx, wy, ww, wh, fill=(18, 24, 22), border=GOLD, alpha=0.95)
        # Cartucho grande de Atari 2600 con etiqueta de E.T. a la izquierda de la tarjeta
        cx0, cy0 = wx + 10, wy + 12
        d.rectangle([cx0, cy0, cx0 + 42, cy0 + 48], fill=(34, 34, 40, 255), outline=(*INK, 255))
        for ry in range(cy0 + 3, cy0 + 10, 2):
            d.line([(cx0 + 4, ry), (cx0 + 38, ry)], fill=(58, 58, 68, 255))
        # Etiqueta verde/dorada con "E.T."
        d.rectangle([cx0 + 4, cy0 + 12, cx0 + 38, cy0 + 42], fill=(38, 128, 68, 255), outline=(*GOLD, 255))
        draw_text(cv, "E.T.", cx0 + 21, cy0 + 21, "press", 8, GOLD, align="center")
        # Texto documental a la derecha del cartucho
        draw_text(cv, "EL JUEGO DEL DESASTRE", wx + 60, wy + 14, "silk", 8, CYAN)
        draw_text(cv, "E.T. (ATARI)", wx + 60, wy + 29, "press", 8, GOLD)
        draw_text(cv, "MILLONES SIN VENDER", wx + 60, wy + 46, "silk", 8, CREAM)

    # Placa documental arriba a la derecha (dentro de zona segura de zoom)
    a, dy = pop(t, t0 - 0.05)
    window(cv, 124, 18 + dy, 332, 42)
    draw_text(cv, "SEPTIEMBRE DE 1983 · NUEVO MÉXICO", 290, 26 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "ENTIERRO DE E.T. Y CARTUCHOS EN EL DESIERTO", 290, 42 + dy, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.38)


def sc_1985_crash_dashboard(t):
    """c3_06: Para 1985, el mercado había caído casi un 97 %."""
    # Fondo del basural oscurecido
    cv = sc_1983_desert_landfill(t)
    cv = grade(cv, mul=(0.38, 0.36, 0.48), add=(4, 4, 12), sat=0.35)

    w = TL.word
    t0 = TL.s("c3_06")
    t_85 = w("c3_06", "ochenta")
    t_caido = w("c3_06", "caido")
    t_97 = w("c3_06", "noventa")

    # Progreso del desplome
    p_drop = ease_in_out(prog(t, t0 + 0.2, t_97 + 0.35))
    rev = int(round(3200 - (3200 - 100) * p_drop))

    # Gran tablero financiero central
    wx, wy, ww, wh = 26, 20, 428, 224
    window(cv, wx, wy, ww, wh, fill=(14, 16, 34), border=RED if p_drop > 0.5 else GOLD)
    d = ImageDraw.Draw(cv)

    draw_text(cv, "EL GRAN CRASH DE LOS VIDEOJUEGOS (1983 -> 1985)", 240, wy + 12, "press", 8, CYAN, align="center")
    d.line([(wx + 16, wy + 26), (wx + ww - 16, wy + 26)], fill=(60, 70, 110, 255))

    # Contador que se desploma de US$ 3.200 MILLONES a US$ 100 MILLONES
    draw_text(cv, "INGRESOS ANUALES EN EE.UU.:", wx + 20, wy + 36, "silk", 8, GREY)
    col_rev = GOLD if p_drop < 0.3 else ((255, 140, 80) if p_drop < 0.8 else RED)
    draw_text(cv, f"US$ {fmt_dots(rev)} MILLONES", wx + 20, wy + 50, "press", 16, col_rev, outline_w=2)

    # Gráfico de barras comparativo (1982, 1983, 1984, 1985)
    gx0, gy0, gx1, gy1 = wx + 28, wy + 86, wx + 248, wy + 196
    d.rectangle([gx0, gy0, gx1, gy1], fill=(8, 10, 22, 255), outline=(*INK, 255))
    for gy_grid in range(gy0 + 22, gy1, 22):
        d.line([(gx0 + 2, gy_grid), (gx1 - 2, gy_grid)], fill=(24, 28, 52, 255))

    bars = [
        ("1982", 0.72, (90, 180, 235)),
        ("1983", 0.92, GOLD),
        ("1984", max(0.28, 0.92 - 0.64 * min(1.0, p_drop * 1.4)), (235, 120, 65)),
        ("1985", max(0.04, 0.92 - 0.88 * p_drop), RED),
    ]
    max_bh = (gy1 - gy0) - 26
    for i, (yr, h_frac, bcol) in enumerate(bars):
        bx = gx0 + 16 + i * 50
        bh = max(3, int(max_bh * h_frac))
        by_top = gy1 - 16 - bh
        d.rectangle([bx, by_top, bx + 30, gy1 - 16], fill=(*bcol, 255), outline=(*INK, 255))
        d.rectangle([bx + 1, by_top + 1, bx + 29, min(gy1 - 16, by_top + 4)], fill=(*shade(bcol, 1.3), 255))
        draw_text(cv, yr, bx + 15, gy1 - 12, "silk", 8, CREAM, align="center")

    # Flecha roja de caída libre
    if p_drop > 0.15:
        d.line([(gx0 + 82, gy0 + 18), (gx0 + 182, gy1 - 26)], fill=(*RED, 255), width=3)
        d.polygon([(gx0 + 186, gy1 - 22), (gx0 + 174, gy1 - 24), (gx0 + 182, gy1 - 34)], fill=(*RED, 255))

    # Gran insignia derecha: 1985 · -97 %
    if t >= t_caido - 0.2:
        a_b, dy_b = pop(t, t_caido - 0.2, 0.3)
        bx, by, bw, bh = wx + 262, wy + 86 + dy_b, 146, 110
        window(cv, bx, by, bw, bh, fill=(42, 12, 18), border=RED, inner=(120, 30, 40))
        draw_text(cv, "1985 · -97 %", bx + bw // 2, by + 16, "press", 8, GOLD, align="center")
        pct_val = int(round(97 * p_drop))
        draw_text(cv, f"-{pct_val}%", bx + bw // 2, by + 38, "press", 24,
                  align="center", gradient=FIRE_RAMP, outline_w=2)
        draw_text(cv, "COLAPSO TOTAL", bx + bw // 2, by + 76, "silk", 8, CREAM, align="center")
        draw_text(cv, "DE LA INDUSTRIA", bx + bw // 2, by + 88, "silk", 8, GREY, align="center")

    draw_text(cv, "DE US$ 3.200 MILLONES A US$ 100 MILLONES EN DOS AÑOS", 240, wy + 206, "silk", 8, CREAM, align="center")

    dx, dy = shake(t, t_97, 0.35, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.42)


def sc_1985_epitaph(t):
    """c3_07: Los analistas dijeron que era una moda... Y que se había terminado. (+ 1.5s de silencio con viento)."""
    cv = new_canvas((4, 4, 8))
    d = ImageDraw.Draw(cv)

    w = TL.word
    t0 = TL.s("c3_07")
    t_moda = w("c3_07", "moda")
    t_remate = w("c3_07", "Y que")
    t_term = w("c3_07", "terminado")

    # Partículas de polvo del desierto flotando en la oscuridad absoluta
    for i in range(55):
        px = int((i * 43 + t * (22 + (i % 4) * 7)) % W)
        py = int((i * 29 + math.sin(t * 0.9 + i) * 14) % H)
        a = 45 + (i % 4) * 28
        c = (190, 155, 110, a) if i % 3 else (130, 135, 155, a)
        d.point((px, py), fill=c)

    # Placa austera en el centro de la pantalla negra
    a_w, dy_w = pop(t, t0 - 0.05, 0.35)
    wx, wy, ww, wh = 44, 78 + dy_w, 392, 112
    window(cv, wx, wy, ww, wh, fill=(10, 12, 24), border=GREY, inner=(38, 42, 64))

    draw_text(cv, "VEREDICTO DE LOS ANALISTAS · 1985", 240, wy + 14, "silk", 8, GREY, align="center")
    if t >= t_moda - 0.5:
        draw_text(cv, "¿EL FIN DE UNA MODA?", 240, wy + 38, "press", 16, CREAM, align="center",
                  reveal=(t - (t_moda - 0.5)) * 28)

    if t >= t_remate - 0.15:
        a_r = prog(t, t_remate - 0.15, t_term)
        d.line([(wx + 36, wy + 66), (wx + ww - 36, wy + 66)], fill=(90, 32, 38, int(255 * a_r)))
        draw_text(cv, "Y QUE SE HABÍA TERMINADO.", 240, wy + 78, "press", 8, RED, align="center",
                  reveal=(t - (t_remate - 0.15)) * 45)

    return vignette(cv, 0.5)


# =========================================================================== MONTAJE

def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (TL.chapter_start(3) - 0.3,
         make_card(3, ["LA FIEBRE Y", "EL ENTIERRO"], "1977 – 1985", robot_face="sad"),
         None),
        (s("c3_01") - 0.2, sc_1977_cartridges,
         lambda t: (cam_push(t, s("c3_01"), e("c3_01"), 1.0, 1.08, (240, 145), (255, 155))[0]
                    + cam_punch(t, [w("c3_01", "cartuchos"), w("c3_01", "todos")], 0.05), 245, 150)),
        (s("c3_02") - 0.2, sc_1982_arcade_boom,
         lambda t: (cam_push(t, s("c3_02"), e("c3_02"), 1.0, 1.08, (240, 135), (240, 125))[0]
                    + cam_punch(t, [w("c3_02", "tres mil"), w("c3_02", "millones")], 0.06), 240, 130)),
        (s("c3_03") - 0.15, sc_1983_crt_shutoff, None),
        (s("c3_04") - 0.2, sc_1983_bargain_bins,
         lambda t: cam_push(t, s("c3_04"), e("c3_04"), 1.0, 1.07, (240, 135), (240, 135))),
        (s("c3_05") - 0.2, sc_1983_desert_landfill,
         lambda t: (cam_push(t, s("c3_05"), e("c3_05"), 1.0, 1.09, (240, 145), (225, 155))[0]
                    + cam_punch(t, [w("c3_05", "descargaron")], 0.05), 232, 150)),
        (s("c3_06") - 0.2, sc_1985_crash_dashboard,
         lambda t: (1.0 + cam_punch(t, [w("c3_06", "caido"), w("c3_06", "noventa")], 0.07), 240, 135)),
        (s("c3_07") - 0.15, sc_1985_epitaph,
         lambda t: cam_push(t, s("c3_07"), chapter_end(3), 1.0, 1.05, (240, 135), (240, 135))),
    ]


# =========================================================================== AUDIO

def music(A):
    s = TL.s
    t0 = TL.chapter_start(3) + 1.6
    # Fiebre de los cartuchos (1977) y boom de los arcades (1983): chiptune alegre a máxima energía
    A.section(t0, s("c3_02") - 0.1, 118,
              [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_bright)
    A.section(s("c3_02") - 0.1, s("c3_03") + 0.08, 132,
              [("C", "maj"), ("A", "min"), ("F", "maj"), ("G", "maj")], A.st_summer_lead)
    # Al llegar c3_03 el televisor se apaga y la música corta en seco.
    # Durante c3_04 y c3_05 solo hay pulsos graves muy tenues; en c3_07 silencio total salvo el viento.
    for k, tp in enumerate([s("c3_04") + 0.4, s("c3_04") + 3.8, s("c3_06") + 0.3, s("c3_06") + 3.2]):
        A.note(A.music, tp, A.midi_hz(38 - (k % 2) * 3), 2.2, "tri", vol=0.12, a=0.2, s=0.7, r=0.8)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    # c3_01: clicks de cartuchos y bleeps de consola
    A.pop_sfx(s("c3_01") - 0.05, 520, 0.05)
    t_cart = w("c3_01", "cartuchos")
    for i in range(4):
        A.blip(t_cart + i * 0.22, 780 + i * 140, 0.04, 0.04, 0.25)
    A.coin(w("c3_01", "todos"), 0.05)

    # c3_02: ambiente de salón arcade y contador de 3.200 millones
    t_luc = w("c3_02", "luces")
    for i in range(10):
        A.blip(t_luc + i * 0.18, 920 + ((i * 230) % 700), 0.03, 0.025, 0.5)
    t_83 = w("c3_02", "ochenta")
    A.pop_sfx(t_83 - 0.05, 640, 0.06)
    for i in range(12):
        A.blip(t_83 + i * 0.12, 600 + i * 75, 0.025, 0.028, 0.25)
    A.coin(w("c3_02", "millones"), 0.065)

    # c3_03: apagado de televisor de tubo y cinta que se frena
    A.crt_off(s("c3_03") + 0.1)
    A.kick(A.sfx, w("c3_03", "abajo"), 0.38)

    # c3_04: etiquetas de liquidación
    t04 = s("c3_04")
    for dt in (0.15, 0.45, 0.75, 1.35, 1.65):
        A.pop_sfx(t04 + dt, 340, 0.045)

    # c3_05..c3_07: viento del desierto de Nuevo México hasta el final del capítulo (incluye el 1.5s de silencio)
    A.wind(s("c3_05") - 0.2, chapter_end(3), 0.055)
    # Golpes graves de las cajas de cartuchos cayendo a la zanja
    t_desc = w("c3_05", "descargaron")
    for i in range(7):
        thud_t = t_desc - 0.3 + i * 0.42
        A.kick(A.sfx, thud_t, 0.22)
        A.note(A.sfx, thud_t + 0.02, 75 + (i % 3) * 12, 0.12, "tri", vol=0.08, s=0.4, r=0.05)

    # c3_06: caída del -97%
    t_caido = w("c3_06", "caido")
    for i in range(9):
        A.blip(t_caido + i * 0.11, 1100 - i * 95, 0.04, 0.03, 0.25)
    A.kick(A.sfx, w("c3_06", "noventa"), 0.45)

    # c3_07: tipeo sobrio del epitafio
    A.text_blips(w("c3_07", "moda") - 0.4, 16, 26, 0.016, 1100)
    A.text_blips(w("c3_07", "terminado") - 0.2, 20, 28, 0.016, 820)
