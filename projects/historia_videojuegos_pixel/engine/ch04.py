"""Capítulo 4: El caballo de Troya (1983 – 1990)."""
from common import *  # noqa

RED = (232, 64, 58)
RED_FAM = (198, 42, 46)
MAGENTA_BAR = (238, 52, 98)

JP_DAD = dict(name="Padre JP", skin=S.SKIN["asian"], hair=S.hexc("181418"), hair_style="side",
              top="sweater", top_color=S.hexc("345a8a"), shirt=S.hexc("f0eee8"), pants=S.hexc("323442"))
JP_MOM = dict(name="Madre JP", skin=S.SKIN["asian"], hair=S.hexc("161216"), hair_style="bun",
              top="shirt", top_color=S.hexc("d46a64"), skirt=True, skirt_color=S.hexc("3c3e58"), pants=S.hexc("3c3e58"))
JP_KID = dict(name="Niño JP", skin=S.SKIN["asian"], hair=S.hexc("141014"), hair_style="fringe",
              top="tshirt", top_color=S.hexc("e8b838"), pants=S.hexc("2c4870"))

US_CLERK = dict(name="Vendedor US", skin=S.SKIN["fair"], hair=S.hexc("5a3822"), hair_style="side",
                mustache=True, top="vest", top_color=S.hexc("2e4a78"), shirt=S.hexc("f2efe6"),
                tie=S.hexc("b83232"), pants=S.hexc("363844"))

NY_WALKER_1 = dict(name="Peatón NY 1", skin=S.SKIN["light"], hair=S.hexc("3a2618"), hair_style="short",
                   top="trench", top_color=S.hexc("8c7658"), pants=S.hexc("2c303c"))
NY_WALKER_2 = dict(name="Peatón NY 2", skin=S.SKIN["tan"], hair=S.hexc("1a1618"), hair_style="curly",
                   top="hoodie", top_color=S.hexc("9e3848"), pants=S.hexc("28344e"))

BUS_KID = dict(name="Chico Game Boy", skin=S.SKIN["fair"], hair=S.hexc("643c20"), hair_style="wavy",
               top="hoodie", top_color=S.hexc("3268b8"), pants=S.hexc("323648"))


def fmt_dots(n):
    return f"{int(n):,}".replace(",", ".")


def draw_nes_cartridge(cv, cx, cy, scale=2, label_col=(220, 56, 48)):
    """Cartucho gris de 8 bits con muescas laterales y etiqueta."""
    d = ImageDraw.Draw(cv)
    w, h = 22 * scale, 26 * scale
    x0, y0 = int(cx - w // 2), int(cy - h // 2)
    # cuerpo gris claro y sombra derecha
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(186, 190, 198, 255), outline=(*INK, 255))
    d.rectangle([x0 + w - 4 * scale, y0 + 1, x0 + w - 1, y0 + h - 1], fill=(142, 146, 156, 255))
    # ranuras horizontales de agarre en la izquierda
    for r in range(4):
        ry = y0 + (3 + r * 3) * scale
        d.rectangle([x0 + 2 * scale, ry, x0 + 6 * scale, ry + scale], fill=(130, 134, 144, 255))
    # etiqueta de color
    lx0, ly0 = x0 + 7 * scale, y0 + 3 * scale
    lx1, ly1 = x0 + w - 3 * scale, y0 + 16 * scale
    d.rectangle([lx0, ly0, lx1, ly1], fill=(*label_col, 255), outline=(*INK, 255))
    d.rectangle([lx0 + scale, ly0 + scale, lx1 - scale, ly0 + 4 * scale], fill=(255, 224, 96, 255))
    # conector inferior más angosto
    d.rectangle([x0 + 3 * scale, y0 + h, x0 + w - 3 * scale, y0 + h + 2 * scale],
                fill=(136, 140, 150, 255), outline=(*INK, 255))


def draw_famicom(cv, x, y):
    """Consola familiar roja y blanca de 1983 sobre el tatami."""
    d = ImageDraw.Draw(cv)
    # base blanca y borde rojo inferior
    d.rectangle([x, y, x + 44, y + 18], fill=(242, 238, 228, 255), outline=(*INK, 255))
    d.rectangle([x + 1, y + 12, x + 43, y + 17], fill=(*RED_FAM, 255))
    # ranura roja central con cartucho colorido insertado
    d.rectangle([x + 14, y + 3, x + 30, y + 10], fill=(*RED_FAM, 255), outline=(*INK, 255))
    d.rectangle([x + 16, y - 3, x + 28, y + 6], fill=(245, 190, 50, 255), outline=(*INK, 255))
    # controles dorados/rojos a los costados
    d.rectangle([x + 3, y + 4, x + 10, y + 11], fill=(*RED_FAM, 255))
    d.rectangle([x + 4, y + 5, x + 9, y + 10], fill=(224, 184, 96, 255))
    d.rectangle([x + 34, y + 4, x + 41, y + 11], fill=(*RED_FAM, 255))
    d.rectangle([x + 35, y + 5, x + 40, y + 10], fill=(224, 184, 96, 255))


def draw_grey_box_console(cv, x, y, scale=1, lid_open=False, led_on=True):
    """Consola gris de carga frontal estilo 1985."""
    d = ImageDraw.Draw(cv)
    w, h = 48 * scale, 22 * scale
    # mitad superior gris clara, mitad inferior gris oscura
    d.rectangle([x, y, x + w, y + h // 2], fill=(202, 204, 210, 255), outline=(*INK, 255))
    d.rectangle([x + 2 * scale, y + h // 2, x + w - 2 * scale, y + h], fill=(116, 120, 130, 255), outline=(*INK, 255))
    # franja negra vertical derecha
    d.rectangle([x + w - 12 * scale, y + 1, x + w - 5 * scale, y + h - 1], fill=(26, 26, 32, 255))
    # tapa frontal de cartuchos
    if lid_open:
        d.rectangle([x + 6 * scale, y + 2 * scale, x + 32 * scale, y + 9 * scale], fill=(28, 30, 38, 255), outline=(*INK, 255))
    else:
        d.rectangle([x + 6 * scale, y + 3 * scale, x + 32 * scale, y + 9 * scale], fill=(182, 186, 194, 255), outline=(*INK, 255))
    # botones power/reset y LED rojo
    d.rectangle([x + 7 * scale, y + h - 6 * scale, x + 12 * scale, y + h - 3 * scale], fill=(80, 84, 94, 255))
    d.rectangle([x + 14 * scale, y + h - 6 * scale, x + 19 * scale, y + h - 3 * scale], fill=(80, 84, 94, 255))
    if led_on:
        d.rectangle([x + 4 * scale, y + h - 5 * scale, x + 5 * scale, y + h - 4 * scale], fill=(255, 60, 50, 255))
    # puertos de control negros
    d.rectangle([x + w - 11 * scale, y + h - 7 * scale, x + w - 6 * scale, y + h - 2 * scale], fill=(18, 18, 24, 255))


# =========================================================================== ESCENAS

def sc_card_ch04(t):
    """Placa del Capítulo 4: El caballo de Troya, con un cartucho gris de 8 bits que baja de golpe."""
    base_fn = make_card(4, ["EL CABALLO DE TROYA"], "1983 – 1990", robot_face="happy")
    cv = base_fn(t)
    t0 = TL.chapter_start(4) - 0.3
    t_slam = TL.chapter_start(4) - 0.15
    if t >= t0:
        p = ease_out(prog(t, t0, t_slam))
        cy = int(-40 + p * 74)
        draw_nes_cartridge(cv, 240, cy, scale=2, label_col=(60, 150, 240))
        dx, dy = shake(t, t_slam, 0.25, 4)
        cv = offset_canvas(cv, dx, dy)
    return cv


def sc_1983_famicom_japan(t):
    """c4_01: Del otro lado del mundo, Nintendo vendía desde 1983 una consola familiar: la Famicom."""
    cv = bg("bg_tokyo_living_1983").copy()
    w = TL.word
    t0 = TL.s("c4_01")
    t_83 = w("c4_01", "ochenta")
    t_fam = w("c4_01", "Famicom")

    d = ImageDraw.Draw(cv)
    # Juego de 8 bits colorido en la pantalla del televisor izquierdo (x: 52..88, y: 124..166)
    poly_tv = [(53, 125), (87, 124), (87, 165), (53, 167)]
    d.polygon(poly_tv, fill=(92, 148, 252, 255))
    # Suelo de ladrillos y bloques dorados en el TV
    d.rectangle([53, 158, 87, 166], fill=(200, 76, 12, 255))
    bx_tv = 62 + int((t * 16) % 18)
    by_tv = 152 - int(abs(math.sin(t * 9)) * 9)
    d.rectangle([bx_tv, by_tv, bx_tv + 4, by_tv + 5], fill=(252, 216, 168, 255))
    d.rectangle([68, 138, 73, 143], fill=(252, 152, 56, 255))

    # Resplandor de la pantalla del televisor
    cv = spotlight(cv, 72, 120, 235, 30, 130, color=(130, 215, 255), strength=0.18)
    d = ImageDraw.Draw(cv)

    # Consola Famicom blanca y roja sobre el tatami frente al mueble del TV
    fx, fy = 122, 224
    d.line([(92, 188), (112, 218), (fx + 4, fy + 10)], fill=(30, 26, 32, 255), width=2)
    draw_famicom(cv, fx, fy)

    # Familia japonesa jugando junta en el tatami
    char(cv, JP_KID, 198, 246, t, scale=2, sit=True, facing=-1, arms="hold", mood="happy",
         talk=talk_v(t, t > t_fam - 0.3))
    char(cv, JP_DAD, 248, 252, t, scale=3, sit=True, facing=-1, arms="hold", mood="happy",
         talk=talk_v(t, t0 + 0.3 < t < t_83))
    char(cv, JP_MOM, 314, 248, t, scale=3, sit=True, facing=-1, arms="cheer" if t > t_fam else "down", mood="happy")

    # Cables de los controles hacia los jugadores
    d.line([(fx + 38, fy + 14), (164, 236), (192, 220)], fill=(40, 32, 36, 255), width=2)
    d.line([(fx + 40, fy + 16), (190, 244), (236, 216)], fill=(40, 32, 36, 255), width=2)

    # Placa superior: JAPÓN · 1983 · FAMICOM (dentro de margen seguro de cámara)
    a, dy = pop(t, t0 - 0.1)
    window(cv, 24, 18 + dy, 258, 42, border=GOLD)
    draw_text(cv, "JAPÓN · 1983 · FAMICOM", 36, 26 + dy, "press", 8, GOLD)
    draw_text(cv, "LA CONSOLA FAMILIAR DE NINTENDO", 36, 42 + dy, "silk", 8, CREAM)

    # Tarjeta destacada de la consola cuando se nombra "Famicom"
    if t >= t_fam - 0.25:
        a2, dy2 = pop(t, t_fam - 0.25)
        window(cv, 294, 18 + dy2, 160, 52, border=CYAN)
        draw_text(cv, "FAMILY COMPUTER", 374, 26 + dy2, "silk", 8, CYAN, align="center")
        draw_famicom(cv, 352, 40 + dy2)
        sparkle(cv, 338, 48 + dy2, t, 3, GOLD)
        sparkle(cv, 412, 46 + dy2, t + 1.2, 3, GOLD)

    return vignette(cv, 0.32)


def sc_1984_us_retail_rejection(t):
    """c4_02: Quería llegar a Estados Unidos. Pero allá, después del desastre, las tiendas no querían ni oír la palabra videojuego."""
    cv = vgradient((26, 28, 44), (16, 18, 30), 10)
    w = TL.word
    t0 = TL.s("c4_02")
    t_eeuu = w("c4_02", "Estados")
    t_des = w("c4_02", "desastre")
    t_tiendas = w("c4_02", "tiendas")
    t_vid = w("c4_02", "videojuego")

    d = ImageDraw.Draw(cv)
    # Interior de juguetería estadounidense: estantería vacía a la izquierda con cartel "VIDEOJUEGOS"
    sx0, sy0, sx1, sy1 = 24, 62, 236, 212
    d.rectangle([sx0, sy0, sx1, sy1], fill=(20, 22, 36, 255), outline=(*INK, 255))
    # Cartel de sección arriba del estante
    window(cv, sx0 + 16, sy0 + 8, 180, 26, fill=(48, 20, 28), border=RED)
    draw_text(cv, "VIDEOJUEGOS", (sx0 + sx1) // 2, sy0 + 17, "press", 8, CREAM, align="center")

    # Estantes completamente vacíos con telaraña y polvo
    for y_sh in (122, 164, 204):
        d.rectangle([sx0 + 6, y_sh, sx1 - 6, y_sh + 6], fill=(86, 90, 108, 255), outline=(*INK, 255))
    # Telaraña pixelada en la esquina del estante
    d.line([(sx0 + 8, 92), (sx0 + 34, 121)], fill=(120, 126, 144, 180))
    d.line([(sx0 + 8, 106), (sx0 + 22, 121)], fill=(120, 126, 144, 180))
    draw_text(cv, "(VACÍO)", (sx0 + sx1) // 2, 140, "silk", 8, GREY, align="center")

    # Cruz roja de prohibido sobre la sección VIDEOJUEGOS cuando dice "ni oír la palabra videojuego"
    if t >= t_vid - 0.35:
        p_x = prog(t, t_vid - 0.35, t_vid + 0.05)
        d.line([(sx0 + 24, sy0 + 42), (sx0 + 24 + int(164 * p_x), sy0 + 42 + int(112 * p_x))],
               fill=(*RED, 255), width=4)
        if p_x > 0.5:
            p_x2 = (p_x - 0.5) * 2
            d.line([(sx1 - 24, sy0 + 42), (sx1 - 24 - int(164 * p_x2), sy0 + 42 + int(112 * p_x2))],
                   fill=(*RED, 255), width=4)

    # Piso y mostrador de la tienda a la derecha
    d.rectangle([0, 212, W, H], fill=(48, 38, 34, 255))
    for yf in (224, 242, 260):
        d.line([(0, yf), (W, yf)], fill=(36, 28, 24, 255))

    # Vendedor estadounidense detrás del mostrador negando con la cabeza y brazos cruzados
    head_shake = -1 if int(t * 6) % 2 == 0 else 1
    char(cv, US_CLERK, 356, 262, t, scale=3, facing=-1,
         arms="cross", mood="worried",
         look=head_shake if t >= t_tiendas - 0.2 else 0,
         talk=talk_v(t, t_tiendas < t < t_vid + 0.3))
    desk(cv, 268, 456, 206, 264, color=(104, 68, 42))

    if t >= t_tiendas - 0.15:
        a_b, dy_b = pop(t, t_tiendas - 0.15)
        bubble(cv, "¡VIDEOJUEGOS NO!", 356, 102 + dy_b)

    # Placa superior
    a, dy = pop(t, t0 - 0.1)
    window(cv, 14, 12 + dy, 452, 40)
    draw_text(cv, "ESTADOS UNIDOS · DESPUÉS DEL CRASH", 240, 20 + dy, "press", 8, GOLD, align="center")
    draw_text(cv, "LAS TIENDAS RECHAZAN CUALQUIER CONSOLA", 240, 36 + dy, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.38)


def sc_1985_trojan_rebrand(t):
    """c4_03: Entonces Nintendo no vendió un videojuego... Vendió un juguete."""
    cv = vgradient((8, 12, 28), (18, 26, 56), 12)
    d = ImageDraw.Draw(cv)
    # Grilla de 8 bits en el fondo
    for x in range(0, W, 24):
        d.line([(x, 0), (x, H)], fill=(22, 32, 68, 255))
    for y in range(0, H, 24):
        d.line([(0, y), (W, y)], fill=(22, 32, 68, 255))

    w = TL.word
    t0 = TL.s("c4_03")
    t_no = w("c4_03", "no")
    t_vid = w("c4_03", "videojuego")
    t_vend = w("c4_03", "Vendio")
    t_jug = w("c4_03", "juguete")

    # Placa de estrategia arriba
    window(cv, 70, 14, 340, 34, border=GOLD)
    draw_text(cv, "LA ESTRATEGIA DEL CABALLO DE TROYA", 240, 22, "press", 8, GOLD, align="center")
    draw_text(cv, "CAMBIAR LAS PALABRAS PARA ENTRAR A LAS TIENDAS", 240, 35, "silk", 8, CREAM, align="center")

    # Caja superior: VIDEOJUEGO tachado con barra gruesa roja/magenta (sin tapar la palabra)
    wx, wy, ww, wh = 44, 60, 392, 82
    window(cv, wx, wy, ww, wh, fill=(24, 16, 36), border=MAGENTA_BAR if t >= t_vid else GREY)
    draw_text(cv, "LO QUE LAS TIENDAS PROHIBÍAN:", 240, wy + 12, "silk", 8, GREY, align="center")
    draw_text(cv, "VIDEOJUEGO", 240, wy + 34, "press", 24, CREAM if t < t_vid else (175, 165, 185),
              align="center", outline_w=2)

    if t >= t_no:
        p_bar = ease_out(prog(t, t_no, t_vid + 0.15))
        bx0 = 240 - 134
        bx1 = bx0 + int(268 * p_bar)
        d.line([(bx0, wy + 49), (bx1, wy + 39)], fill=(*INK, 255), width=7)
        d.line([(bx0, wy + 49), (bx1, wy + 39)], fill=(*MAGENTA_BAR, 255), width=3)

    # Caja inferior: JUGUETE aparece con rebote en cian y dorado brillante
    if t >= t_vend - 0.1:
        a_j, dy_j = pop(t, t_jug - 0.15, 0.35)
        jy = 156 + dy_j
        window(cv, 44, jy, 392, 94, fill=(14, 28, 54), border=CYAN, inner=(40, 110, 160))
        draw_text(cv, "EL CABALLO DE TROYA DE NINTENDO:", 240, jy + 12, "silk", 8, CYAN, align="center")
        draw_text(cv, "JUGUETE", 240, jy + 32, "press", 24, align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, "CONSOLA -> ENTERTAINMENT SYSTEM · CARTUCHO -> GAME PAK",
                  240, jy + 70, "silk", 8, CREAM, align="center")
        for i in range(5):
            sparkle(cv, 76 + i * 82, jy + 38 + (i % 2) * 16, t + i * 0.7, 3, CYAN if i % 2 else GOLD)

    dx, dy = shake(t, t_jug, 0.25, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


def sc_1985_ny_toy_store(t):
    """c4_04: Le cambió la forma, le cambió el nombre, y le puso al lado un robot. El 18 de octubre de 1985 la probó en Nueva York."""
    cv = bg("bg_toy_store_ny_1985").copy()
    w = TL.word
    t0 = TL.s("c4_04")
    t_rob = w("c4_04", "robot")
    t_18 = w("c4_04", "dieciocho")
    t_ny = w("c4_04", "Nueva")

    d = ImageDraw.Draw(cv)
    # Resplandor cálido de la vidriera iluminada hacia la vereda nocturna
    cv = spotlight(cv, 305, 110, 240, 110, 180, color=(255, 230, 160), strength=0.14)
    d = ImageDraw.Draw(cv)

    # Animación del pequeño robot gris R.O.B. en la vidriera (está en x=308, y=166..196 en el fondo)
    # Le animamos la cabeza girando a izquierda y derecha con ojos rojos brillantes
    rob_turn = int(round(math.sin(t * 4.5) * 2))
    hx, hy = 308 + rob_turn, 170
    d.rectangle([hx - 6, hy - 4, hx + 6, hy + 3], fill=(184, 188, 196, 255), outline=(*INK, 255))
    # Ojos LED rojos encendidos
    eye_col = (255, 55, 55, 255) if int(t * 6) % 4 != 0 else (180, 30, 30, 255)
    d.rectangle([hx - 4, hy - 2, hx - 2, hy], fill=eye_col)
    d.rectangle([hx + 2, hy - 2, hx + 4, hy], fill=eye_col)
    # LED rojo de la consola gris en el pedestal izquierdo (x=265..296, y=170..186)
    d.rectangle([268, 181, 270, 183], fill=(255, 60, 50, 255))

    # Peatones en la vereda de Nueva York mirando la vidriera
    x_w1, ph1 = walk(t, t0 - 0.2, t0 + 3.2, 80, 214)
    char(cv, NY_WALKER_1, x_w1, 252, t, scale=2, walk=ph1, facing=1,
         arms="point" if ph1 is None and t > t_rob else "down", mood="happy")
    char(cv, NY_WALKER_2, 368, 254, t, scale=2, facing=-1,
         arms="think" if t < t_18 else "cheer", mood="happy")

    # Etiquetas flotantes señalando la caja gris y el robot en la vidriera
    if t >= t0 + 0.3 and t < t_18 - 0.2:
        window(cv, 218, 86, 178, 38, border=CYAN)
        draw_text(cv, "CAJA GRIS + ROBOT", 307, 94, "press", 8, CYAN, align="center")
        draw_text(cv, "PARECE UN JUGUETE DEL FUTURO", 307, 108, "silk", 8, CREAM, align="center")

    # Placa principal: NUEVA YORK · 18 · 10 · 1985 (dentro de margen seguro de cámara)
    a, dy = pop(t, t_18 - 0.15 if t >= t_18 - 0.15 else t0 - 0.1)
    window(cv, 34, 22 + dy, 268, 44, border=GOLD)
    draw_text(cv, "NUEVA YORK · 18 · 10 · 1985", 46, 30 + dy, "press", 8, GOLD)
    draw_text(cv, "LANZAMIENTO DE PRUEBA EN EE.UU.", 46, 46 + dy, "silk", 8, CREAM)

    return vignette(cv, 0.34)


def draw_scope_1958_half(cv, t):
    """Dibuja la mitad izquierda (x=0..239) con el osciloscopio de Tennis for Two (18·10·1958)."""
    lab = bg("bg_brookhaven_lab_1958").copy().crop((160, 0, 400, H))
    lab = grade(lab, mul=(0.55, 0.75, 0.65), add=(4, 12, 8), sat=0.5)
    cv.paste(lab, (0, 0))
    d = ImageDraw.Draw(cv)

    # Gran círculo de osciloscopio de 5 pulgadas centrado en (120, 140)
    cx, cy, r = 120, 142, 62
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(54, 58, 52, 255), outline=(*INK, 255))
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(28, 32, 28, 255), outline=(90, 98, 88, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 34, 20, 255), outline=(40, 110, 65, 255))

    # Retícula del osciloscopio
    for gx in range(cx - 48, cx + 49, 16):
        d.line([(gx, cy - r + 10), (gx, cy + r - 10)], fill=(18, 56, 34, 255))
    for gy in range(cy - 48, cy + 49, 16):
        d.line([(cx - r + 10, gy), (cx + r - 10, gy)], fill=(18, 56, 34, 255))

    # Cancha y red en fósforo verde
    court_y = cy + 24
    d.line([(cx - 46, court_y), (cx + 46, court_y)], fill=(90, 255, 135, 255), width=2)
    d.line([(cx, court_y - 18), (cx, court_y)], fill=(90, 255, 135, 255), width=2)

    # Pelota de luz rebotando con estela de fósforo
    cyc = (t * 1.45) % 2.0
    u = cyc if cyc <= 1.0 else 2.0 - cyc
    bx = cx - 38 + u * 76
    by = court_y - 3 - abs(math.sin(u * math.pi * 2)) * 34
    trail = []
    for k in range(6, 0, -1):
        tc = ((t - k * 0.035) * 1.45) % 2.0
        tu = tc if tc <= 1.0 else 2.0 - tc
        tx = cx - 38 + tu * 76
        ty = court_y - 3 - abs(math.sin(tu * math.pi * 2)) * 34
        trail.append((tx, ty))
    draw_phosphor_dot(cv, bx, by, r=3, trail=trail)

    # Etiqueta inferior de la mitad 1958
    window(cv, 16, 214, 208, 42, fill=(10, 26, 20), border=(100, 255, 140))
    draw_text(cv, "18 · 10 · 1958", 120, 222, "press", 8, (100, 255, 140), align="center")
    draw_text(cv, "TENNIS FOR TWO · BROOKHAVEN", 120, 238, "silk", 8, CREAM, align="center")


def sc_1985_split_1958_callback(t):
    """c4_05: Veintisiete años exactos después de Tennis for Two. (Split screen 18·10·1958 <-> 18·10·1985)."""
    cv = new_canvas((10, 12, 22))

    # Mitad izquierda (x=0..239): osciloscopio de 1958
    draw_scope_1958_half(cv, t)

    # Mitad derecha (x=241..480): vidriera de Nueva York de 1985 centrada en la consola y R.O.B.
    ny_crop = bg("bg_toy_store_ny_1985").copy().crop((170, 0, 410, H))
    cv.paste(ny_crop, (240, 0))

    d = ImageDraw.Draw(cv)
    # Ojos brillantes del robot en la mitad derecha (ajustado al recorte x-170+240 = +70 -> x=378)
    rob_turn = int(round(math.sin(t * 4.5) * 2))
    hx, hy = 378 + rob_turn, 170
    d.rectangle([hx - 6, hy - 4, hx + 6, hy + 3], fill=(184, 188, 196, 255), outline=(*INK, 255))
    d.rectangle([hx - 4, hy - 2, hx - 2, hy], fill=(255, 55, 55, 255))
    d.rectangle([hx + 2, hy - 2, hx + 4, hy], fill=(255, 55, 55, 255))

    # Etiqueta inferior de la mitad 1985
    window(cv, 256, 214, 208, 42, fill=(20, 24, 52), border=CYAN)
    draw_text(cv, "18 · 10 · 1985", 360, 222, "press", 8, CYAN, align="center")
    draw_text(cv, "NINTENDO EN NUEVA YORK", 360, 238, "silk", 8, CREAM, align="center")

    # Línea divisoria central brillante
    d.rectangle([238, 0, 241, H], fill=(*GOLD, 255))
    d.line([(239, 0), (239, H)], fill=(255, 250, 210, 255))

    # Banner superior unificador: 18 · 10 · 1958 <-> 18 · 10 · 1985 / 27 AÑOS EXACTOS
    a, dy = pop(t, TL.s("c4_05") - 0.1)
    window(cv, 24, 12 + dy, 432, 48, fill=(14, 18, 40), border=GOLD)
    draw_text(cv, "18 · 10 · 1958  <->  18 · 10 · 1985", 240, 20 + dy, "press", 8, CYAN, align="center")
    draw_text(cv, "27 AÑOS EXACTOS", 240, 36 + dy, "press", 16, align="center", gradient=GOLD_RAMP)

    return vignette(cv, 0.32)


def sc_1985_super_mario(t):
    """c4_06: Entre sus juegos había uno con un plomero. Super Mario Bros. vendió más de 40 millones de copias."""
    w = TL.word
    t0 = TL.s("c4_06")
    t_mario = w("c4_06", "Mario")
    t_40 = w("c4_06", "cuarenta")

    # Cielo azul brillante de 8 bits
    cv = vgradient((92, 148, 252), (132, 180, 255), 8)
    d = ImageDraw.Draw(cv)

    # Desplazamiento horizontal continuo de escenario de plataformas 8-bit (sin sprites con copyright)
    scroll = int((t - t0) * 58)

    # Nubes blancas y colinas verdes
    for i in range(6):
        cx_c = ((i * 120 - scroll // 3) % (W + 80)) - 40
        cy_c = 78 + (i % 2) * 18
        d.ellipse([cx_c, cy_c, cx_c + 36, cy_c + 18], fill=(252, 252, 252, 255), outline=(*INK, 255))
        d.ellipse([cx_c + 12, cy_c - 6, cx_c + 44, cy_c + 14], fill=(252, 252, 252, 255), outline=(*INK, 255))

    for i in range(5):
        hx = ((i * 150 - scroll // 2) % (W + 100)) - 50
        hy = 230
        d.polygon([(hx, hy), (hx + 38, hy - 34), (hx + 76, hy)], fill=(0, 168, 0, 255), outline=(*INK, 255))

    # Piso de bloques de ladrillo (y=230..270)
    brick_w, brick_h = 16, 16
    for y_b in range(230, H, brick_h):
        for x_b in range(-brick_w, W + brick_w, brick_w):
            xx = x_b - (scroll % brick_w)
            d.rectangle([xx, y_b, xx + brick_w - 1, y_b + brick_h - 1],
                        fill=(200, 76, 12, 255), outline=(*INK, 255))
            d.line([(xx + 1, y_b + 1), (xx + brick_w - 2, y_b + 1)], fill=(252, 188, 176, 255))
            d.line([(xx + brick_w // 2, y_b), (xx + brick_w // 2, y_b + brick_h - 1)], fill=(*INK, 255))

    # Tuberías verdes clásicas
    for p_idx in range(4):
        px = ((p_idx * 160 + 90 - scroll) % (W + 120)) - 40
        ph = 36 + (p_idx % 2) * 14
        py = 230 - ph
        # cuerpo de la tubería
        d.rectangle([px + 3, py + 12, px + 33, 230], fill=(0, 168, 0, 255), outline=(*INK, 255))
        d.rectangle([px + 7, py + 13, px + 13, 229], fill=(128, 208, 16, 255))
        # boca superior
        d.rectangle([px, py, px + 36, py + 12], fill=(0, 168, 0, 255), outline=(*INK, 255))
        d.rectangle([px + 4, py + 1, px + 12, py + 11], fill=(128, 208, 16, 255))

    # Fila de bloques de ladrillo y bloques de signo "?" con monedas saltando
    for b_idx in range(8):
        bx = ((b_idx * 72 + 40 - scroll) % (W + 72)) - 24
        by = 148
        is_q = (b_idx % 2 == 0)
        b_bump = int(abs(math.sin(t * 7 + b_idx)) * 4) if is_q else 0
        by_cur = by - b_bump
        col_b = (252, 152, 56) if is_q else (200, 76, 12)
        d.rectangle([bx, by_cur, bx + 16, by_cur + 16], fill=(*col_b, 255), outline=(*INK, 255))
        if is_q:
            draw_text(cv, "?", bx + 9, by_cur + 4, "press", 8, (100, 40, 0), align="center", outline=None, shadow=False)
            # moneda dorada que salta arriba del bloque
            coin_phase = (t * 2.2 + b_idx * 0.37) % 1.0
            if coin_phase < 0.65:
                cy_coin = by_cur - 6 - int(math.sin(coin_phase / 0.65 * math.pi) * 26)
                d.ellipse([bx + 5, cy_coin - 5, bx + 11, cy_coin + 5],
                          fill=(255, 220, 70, 255), outline=(*INK, 255))

    # Consola gris con cartucho entrando de golpe en la esquina inferior izquierda
    slam_p = ease_out(prog(t, t0 - 0.1, t0 + 0.25))
    cart_y = int(172 + slam_p * 26)
    draw_nes_cartridge(cv, 62, cart_y, scale=1, label_col=(235, 175, 45))
    draw_grey_box_console(cv, 26, 198, scale=1, lid_open=(slam_p < 0.9), led_on=True)

    # Gran ventana de ventas cuando menciona "Super Mario Bros. vendió más de 40 millones"
    a, dy = pop(t, t0 + 0.05)
    wx, wy, ww, wh = 26, 14 + dy, 428, 92
    window(cv, wx, wy, ww, wh, fill=(16, 22, 54), border=GOLD)
    draw_text(cv, "EL JUEGO QUE SALVÓ LA INDUSTRIA · 1985", 240, wy + 10, "silk", 8, CYAN, align="center")

    if t >= t_mario - 0.2:
        p_cnt = ease_out(prog(t, t_mario, t_40 + 0.4))
        val = int(round(40 * p_cnt))
        label_main = "SUPER MARIO BROS. · +40 MILLONES" if p_cnt >= 0.95 else f"SUPER MARIO BROS. · +{val} MILLONES"
        draw_text(cv, label_main, 240, wy + 30, "press", 8, GOLD, align="center")
        draw_text(cv, f"+{val} MILLONES DE COPIAS", 240, wy + 48, "press", 16,
                  align="center", gradient=GOLD_RAMP, outline_w=2)
        draw_text(cv, "RÉCORD HISTÓRICO EN CONSOLAS HOGAREÑAS", 240, wy + 74, "silk", 8, CREAM, align="center")
        if p_cnt >= 0.95:
            for k in range(4):
                sparkle(cv, wx + 44 + k * 110, wy + 52, t + k * 0.6, 3, GOLD)
    else:
        draw_text(cv, "UN PLOMERO EN UN MUNDO DE BLOQUES Y TUBERÍAS", 240, wy + 40, "press", 8, CREAM, align="center")

    dx, dy_s = shake(t, t0 + 0.22, 0.22, 3)
    cv = offset_canvas(cv, dx, dy_s)
    return vignette(cv, 0.3)


def draw_gameboy_inset(cv, x0, y0, t, t0):
    """Dibuja la carcasa portátil gris y un zoom de su pantalla verde oliva con bloques de Tetris."""
    d = ImageDraw.Draw(cv)
    # Marco exterior estilo carcasa portátil gris con bordes redondeados
    bw, bh = 188, 194
    d.rectangle([x0 + 3, y0 + 3, x0 + bw + 3, y0 + bh + 3], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(204, 204, 198, 255), outline=(*INK, 255))
    # bisel gris oscuro de la pantalla
    d.rectangle([x0 + 12, y0 + 12, x0 + bw - 12, y0 + 144], fill=(104, 104, 118, 255), outline=(*INK, 255))
    draw_text(cv, "DOT MATRIX", x0 + bw // 2, y0 + 16, "silk", 8, CREAM, align="center")
    # LED de batería rojo a la izquierda
    d.ellipse([x0 + 18, y0 + 68, x0 + 24, y0 + 74], fill=(245, 50, 45, 255), outline=(*INK, 255))

    # Pantalla verde oliva clásica (10 x 12 celdas de 8 px)
    sx, sy = x0 + 34, y0 + 28
    cols, rows, cell = 10, 13, 8
    sw, sh = cols * cell, rows * cell
    c_bg = (155, 188, 15, 255)
    c_grid = (139, 172, 15, 255)
    c_mid = (48, 98, 48, 255)
    c_dark = (15, 56, 15, 255)

    d.rectangle([sx - 2, sy - 2, sx + sw + 2, sy + sh + 2], fill=c_dark)
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=c_bg)

    # Grilla sutil de matriz de puntos
    for gx in range(sx, sx + sw + 1, cell):
        d.line([(gx, sy), (gx, sy + sh)], fill=c_grid)
    for gy in range(sy, sy + sh + 1, cell):
        d.line([(sx, gy), (sx + sw, gy)], fill=c_grid)

    def draw_cell(cx_i, cy_i, flash=False):
        if not (0 <= cx_i < cols and 0 <= cy_i < rows):
            return
        px, py = sx + cx_i * cell, sy + cy_i * cell
        if flash:
            d.rectangle([px, py, px + cell - 1, py + cell - 1], fill=(220, 240, 150, 255), outline=c_dark)
        else:
            d.rectangle([px, py, px + cell - 1, py + cell - 1], fill=c_mid, outline=c_dark)
            d.rectangle([px + 2, py + 2, px + cell - 3, py + cell - 3], fill=c_bg, outline=c_dark)

    # Bloques acumulados en la base dejando el hueco central (col 4) para una pieza I vertical
    static_rows = [
        (12, [0, 1, 2, 3, 5, 6, 7, 8, 9]),
        (11, [0, 1, 2, 3, 5, 6, 7, 8, 9]),
        (10, [0, 1, 2, 5, 6, 7, 8, 9]),
        (9,  [0, 1, 6, 7, 8, 9]),
    ]
    dt = max(0.0, t - t0)
    cyc = dt % 3.6
    line_cleared = cyc > 2.4

    for r_i, xs in static_rows:
        # Si ya limpió las 2 filas inferiores, bajan 2 filas
        if line_cleared and r_i in (11, 12):
            continue
        r_draw = r_i + (2 if line_cleared and r_i < 11 else 0)
        flashing = (2.0 <= cyc <= 2.4) and r_i in (11, 12) and (int(t * 18) % 2 == 0)
        for c_i in xs:
            draw_cell(c_i, r_draw, flash=flashing)

    # Pieza I vertical cayendo en la columna 4 para completar las líneas
    if cyc < 2.0:
        fall_y = int((cyc / 2.0) * 9)
        for dy_cell in range(4):
            draw_cell(4, fall_y + dy_cell)
    elif 2.0 <= cyc <= 2.4:
        flashing = (int(t * 18) % 2 == 0)
        for dy_cell in range(4):
            draw_cell(4, 9 + dy_cell, flash=flashing)
    else:
        # Nueva pieza T empezando a caer arriba
        fall2 = int(((cyc - 2.4) / 1.2) * 4)
        for dx_c, dy_c in ((3, 0), (4, 0), (5, 0), (4, 1)):
            draw_cell(dx_c, fall2 + dy_c)

    # Controles inferiores de la carcasa portátil: cruceta negra y botones A/B magenta
    cx_pad, cy_pad = x0 + 46, y0 + 168
    d.rectangle([cx_pad - 12, cy_pad - 4, cx_pad + 12, cy_pad + 4], fill=(28, 28, 34, 255), outline=(*INK, 255))
    d.rectangle([cx_pad - 4, cy_pad - 12, cx_pad + 4, cy_pad + 12], fill=(28, 28, 34, 255), outline=(*INK, 255))
    # Botones A y B
    for bx_btn, by_btn in ((x0 + 146, y0 + 162), (x0 + 126, y0 + 170)):
        d.ellipse([bx_btn - 6, by_btn - 6, bx_btn + 6, by_btn + 6],
                  fill=(168, 34, 82, 255), outline=(*INK, 255))


def sc_1989_gameboy_tetris(t):
    """c4_07: Y en 1989, Nintendo puso los videojuegos en el bolsillo: el Game Boy. Con Tetris en la caja."""
    cv = bg("bg_bus_interior_1989").copy()
    w = TL.word
    t0 = TL.s("c4_07")
    t_gb = w("c4_07", "Game")
    t_tet = w("c4_07", "Tetris")

    # Chico sentado en el asiento izquierdo del colectivo jugando con su portátil gris
    char(cv, BUS_KID, 134, 252, t, scale=3, sit=True, facing=1, arms="hold", mood="happy")
    d = ImageDraw.Draw(cv)
    # Pequeña consola portátil gris en las manos del chico
    d.rectangle([142, 170, 158, 192], fill=(204, 204, 198, 255), outline=(*INK, 255))
    d.rectangle([145, 173, 155, 181], fill=(139, 172, 15, 255))

    # Zoom grande a la derecha de la pantalla verde oliva con bloques de Tetris cayendo
    draw_gameboy_inset(cv, 262, 54, t, t0)

    # Placa superior izquierda: GAME BOY · 1989 · TETRIS (dentro de margen seguro de cámara)
    a, dy = pop(t, t0 - 0.1)
    window(cv, 32, 20 + dy, 222, 44, border=GOLD)
    draw_text(cv, "GAME BOY · 1989 · TETRIS", 42, 28 + dy, "press", 8, GOLD)
    draw_text(cv, "LOS VIDEOJUEGOS EN EL BOLSILLO", 42, 44 + dy, "silk", 8, CREAM)

    if t >= t_tet - 0.2:
        a2, dy2 = pop(t, t_tet - 0.2)
        window(cv, 32, 70 + dy2, 222, 34, border=CYAN)
        draw_text(cv, "CON TETRIS EN LA CAJA", 143, 78 + dy2, "press", 8, CYAN, align="center")
        draw_text(cv, "EL COMBO PORTÁTIL DEFINITIVO", 143, 91 + dy2, "silk", 8, CREAM, align="center")

    return vignette(cv, 0.34)


# =========================================================================== MONTAJE

def scenes():
    s, e, w = TL.s, TL.e, TL.word
    return [
        (TL.chapter_start(4) - 0.3, sc_card_ch04, None),
        (s("c4_01") - 0.2, sc_1983_famicom_japan,
         lambda t: (cam_push(t, s("c4_01"), e("c4_01"), 1.0, 1.08, (240, 140), (230, 145))[0]
                    + cam_punch(t, [w("c4_01", "Famicom")], 0.06), 235, 142)),
        (s("c4_02") - 0.2, sc_1984_us_retail_rejection,
         lambda t: (1.0 + cam_punch(t, [w("c4_02", "videojuego")], 0.07), 240, 135)),
        (s("c4_03") - 0.15, sc_1985_trojan_rebrand,
         lambda t: (1.0 + cam_punch(t, [w("c4_03", "videojuego"), w("c4_03", "juguete")], 0.08), 240, 135)),
        (s("c4_04") - 0.2, sc_1985_ny_toy_store,
         lambda t: (cam_push(t, s("c4_04"), e("c4_04"), 1.0, 1.09, (250, 140), (280, 150))[0]
                    + cam_punch(t, [w("c4_04", "dieciocho")], 0.05), 265, 145)),
        (s("c4_05") - 0.2, sc_1985_split_1958_callback,
         lambda t: (1.0 + cam_punch(t, [w("c4_05", "Veintisiete"), w("c4_05", "Tennis")], 0.06), 240, 135)),
        (s("c4_06") - 0.2, sc_1985_super_mario,
         lambda t: (cam_push(t, s("c4_06"), e("c4_06"), 1.0, 1.06, (240, 135), (240, 135))[0]
                    + cam_punch(t, [w("c4_06", "Mario"), w("c4_06", "cuarenta")], 0.06), 240, 135)),
        (s("c4_07") - 0.2, sc_1989_gameboy_tetris,
         lambda t: (cam_push(t, s("c4_07"), chapter_end(4), 1.0, 1.08, (250, 135), (275, 135))[0]
                    + cam_punch(t, [w("c4_07", "Game"), w("c4_07", "Tetris")], 0.06), 265, 135)),
    ]


# =========================================================================== AUDIO

def music(A):
    s = TL.s
    t0 = TL.chapter_start(4) + 1.6
    t_end = chapter_end(4) - 0.2
    # c4_01: Famicom en Japón (alegre y rítmico)
    A.section(t0, s("c4_02") - 0.15, 114,
              [("F", "maj"), ("G", "maj"), ("E", "min"), ("A", "min")], A.st_bright)
    # c4_02..c4_03: Tensión y plan del caballo de Troya en EE.UU.
    A.section(s("c4_02") - 0.15, s("c4_04") - 0.15, 102,
              [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "maj")], A.st_mystery)
    # c4_04..c4_05: Nueva York 1985 y conexión con 1958
    A.section(s("c4_04") - 0.15, s("c4_06") - 0.15, 116,
              [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_build)
    # c4_06: Super Mario Bros. (explosión de energía 8-bit)
    A.section(s("c4_06") - 0.15, s("c4_07") - 0.15, 132,
              [("C", "maj"), ("G", "maj"), ("A", "min"), ("F", "maj")], A.st_summer_lead)
    # c4_07: Game Boy y Tetris (estilo puzzle rítmico de 8 bits)
    A.section(s("c4_07") - 0.15, t_end, 126,
              [("A", "min"), ("E", "maj"), ("D", "min"), ("E", "maj")], A.st_puzzle)


def sfx(A):
    s, e, w = TL.s, TL.e, TL.word
    # Golpe seco del cartucho gris en la apertura del capítulo 4
    A.cartridge_slam(TL.chapter_start(4) - 0.15)

    # c4_01: Famicom en Japón
    A.pop_sfx(s("c4_01") - 0.05, 580, 0.05)
    A.join_jingle(w("c4_01", "Famicom") - 0.1, 0.055)

    # c4_02: Rechazo en las tiendas de EE.UU.
    A.pop_sfx(w("c4_02", "tiendas") - 0.1, 420, 0.05)
    t_vid2 = w("c4_02", "videojuego")
    A.note(A.sfx, t_vid2, 130, 0.22, duty=0.5, vol=0.06, s=0.8, r=0.05)

    # c4_03: Tacha VIDEOJUEGO -> aparece JUGUETE
    A.whoosh(w("c4_03", "no"), 0.28, 0.055)
    A.kick(A.sfx, w("c4_03", "videojuego"), 0.35)
    t_jug = w("c4_03", "juguete")
    A.pop_sfx(t_jug - 0.05, 680, 0.065)
    A.coin(t_jug + 0.05, 0.065)

    # c4_04: Robot R.O.B. y estreno en Nueva York el 18/10/1985
    A.robot_beep(w("c4_04", "robot"), 0.05)
    A.pop_sfx(w("c4_04", "dieciocho") - 0.05, 600, 0.055)

    # c4_05: El 'plic' original de 1958 al nombrar Tennis for Two (27 años exactos)
    A.pop_sfx(w("c4_05", "Veintisiete") - 0.05, 540, 0.05)
    A.plic(w("c4_05", "Tennis"))
    A.plic(w("c4_05", "Tennis") + 0.45, 1180, 0.065)

    # c4_06: Cartucho entrando en la consola + monedas y contador de Super Mario Bros.
    A.cartridge_slam(s("c4_06") + 0.12)
    t_mar = w("c4_06", "Mario")
    A.coin(t_mar, 0.065)
    for i in range(8):
        A.blip(t_mar + 0.15 + i * 0.11, 700 + i * 80, 0.025, 0.028, 0.25)
    A.coin(w("c4_06", "cuarenta"), 0.07)

    # c4_07: Game Boy y Tetris
    A.pop_sfx(w("c4_07", "Game") - 0.05, 640, 0.055)
    t_tet = w("c4_07", "Tetris")
    for i, m in enumerate([76, 71, 72, 74, 72, 71, 69]):
        A.note(A.sfx, t_tet + i * 0.11, A.midi_hz(m), 0.08, duty=0.25, vol=0.04, s=0.6, r=0.02)
