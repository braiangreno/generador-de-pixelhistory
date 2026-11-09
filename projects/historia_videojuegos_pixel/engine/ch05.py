"""Capítulo 5: La traición (1991 – 1996)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *  # noqa

WD = TL.word

C = S.hexc
KUTARAGI = dict(
    name="Ken Kutaragi", skin=S.SKIN["asian"], hair=C("18161c"), hair_style="side",
    top="suit", top_color=C("2c3246"), shirt=C("eef2f8"), tie=C("8a2838"), pants=C("1e2230")
)
EXEC_1991 = dict(
    name="Ejecutivo 1991", skin=S.SKIN["fair"], hair=C("5a4838"), hair_style="slick",
    glasses="gold", top="suit", top_color=C("222638"), shirt=C("f4f2ec"), tie=C("d4a038"), pants=C("1a1c2a")
)
TEEN_A = dict(
    name="Teen 90s A", skin=S.SKIN["fair"], hair=C("6a4428"), hair_style="wavy",
    top="hoodie", top_color=C("2e6a9e"), pants=C("384460")
)
TEEN_B = dict(
    name="Teen 90s B", skin=S.SKIN["tan"], hair=C("1e1818"), hair_style="fringe",
    top="tshirt", top_color=C("b83a48"), pants=C("2e3446")
)

MAGENTA = (240, 75, 165)
GREEN_LED = (85, 250, 130)
RED_ALERT = (240, 75, 70)
SILVER = (215, 224, 236)


# =========================================================================== helpers

def draw_cd_disc(cv, cx, cy, r, t, spin_speed=4.0, glow_col=CYAN):
    """Dibuja un disco CD-ROM plateado girando con reflejos arcoíris/cian."""
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(*glow_col, 45))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*SILVER, 255), outline=(*INK, 255))
    ang0 = t * spin_speed
    for k in range(2):
        a = ang0 + k * math.pi
        for da, col in ((-0.25, (140, 235, 255)), (0.0, (255, 255, 255)), (0.25, (235, 160, 255))):
            x1 = cx + int(math.cos(a + da) * (r - 2))
            y1 = cy + int(math.sin(a + da) * (r - 2))
            x0 = cx + int(math.cos(a + da) * max(4, r // 3))
            y0 = cy + int(math.sin(a + da) * max(4, r // 3))
            d.line([(x0, y0), (x1, y1)], fill=(*col, 255), width=2 if da == 0.0 else 1)
    ir = max(4, r // 3)
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(150, 162, 180, 255), outline=(90, 100, 120, 255))
    hr = max(2, r // 6)
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(20, 24, 44, 255), outline=(*INK, 255))


def draw_ps1_unit(cv, cx, cy, scale=1.0, lid_open=0.0, power_on=True, t=0.0, wireframe=False):
    """Dibuja la consola gris de 1994 con tapa circular superior."""
    d = ImageDraw.Draw(cv)
    w, h = int(86 * scale), int(42 * scale)
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = x0 + w, y0 + h
    if wireframe:
        col = CYAN
        d.rectangle([x0, y0, x1, y1], outline=(*col, 235))
        d.rectangle([x0 + 4, y0 + 3, x1 - 4, y1 - 6], outline=(*col, 160))
        r = int(24 * scale)
        d.ellipse([cx - r, cy - r - 1, cx + r, cy + r - 1], outline=(*col, 245))
        d.ellipse([cx - 4, cy - 5, cx + 4, cy + 3], outline=(*GOLD, 240))
        return
    # Sombra base
    d.rectangle([x0 + 3, y0 + 4, x1 + 3, y1 + 4], fill=(0, 0, 0, 120))
    # Carcasa gris
    body = (176, 180, 190)
    dark = (128, 132, 144)
    light = (212, 216, 224)
    d.rectangle([x0, y0, x1, y1], fill=(*body, 255), outline=(*INK, 255))
    d.rectangle([x0 + 1, y1 - int(9 * scale), x1 - 1, y1 - 1], fill=(*dark, 255))
    d.line([(x0 + 1, y0 + 1), (x1 - 1, y0 + 1)], fill=(*light, 255))
    # Líneas laterales
    lx = x0 + int(16 * scale)
    rx = x1 - int(16 * scale)
    d.line([(lx, y0 + 1), (lx, y1 - 1)], fill=(*dark, 255))
    d.line([(rx, y0 + 1), (rx, y1 - 1)], fill=(*dark, 255))
    # Tapa circular de CD
    r = int(23 * scale)
    cy_lid = cy - int(3 * scale)
    d.ellipse([cx - r, cy_lid - r, cx + r, cy_lid + r], fill=(164, 168, 178, 255), outline=(*INK, 255))
    if lid_open > 0.05:
        draw_cd_disc(cv, cx, cy_lid, int(r * 0.82), t, spin_speed=6.0)
    else:
        d.ellipse([cx - 3, cy_lid - 3, cx + 3, cy_lid + 3], fill=(*dark, 255))
    # Botones POWER (izq) y OPEN (der)
    br = max(3, int(5 * scale))
    bx_l = x0 + int(8 * scale)
    bx_r = x1 - int(8 * scale)
    by_b = y1 - int(16 * scale)
    d.ellipse([bx_l - br, by_b - br, bx_l + br, by_b + br], fill=(140, 144, 156, 255), outline=(*INK, 255))
    d.ellipse([bx_r - br, by_b - br, bx_r + br, by_b + br], fill=(140, 144, 156, 255), outline=(*INK, 255))
    # LED verde de encendido
    if power_on:
        pulse = 0.65 + 0.35 * math.sin(t * 8.0)
        d.ellipse([bx_l - 5, by_b - 5, bx_l + 5, by_b + 5], fill=(80, 255, 120, int(110 * pulse)))
        d.rectangle([bx_l - 1, by_b - 1, bx_l + 1, by_b + 1], fill=(160, 255, 180, 255))
    # Puertos de control frontales
    for px in (cx - int(16 * scale), cx + int(6 * scale)):
        d.rectangle([px, y1 - int(7 * scale), px + int(10 * scale), y1 - int(3 * scale)],
                    fill=(60, 62, 72, 255), outline=(*INK, 255))


def project_3d(pts, rx, ry, rz, cx, cy, scale):
    """Proyecta una lista de vértices 3D (x,y,z) a 2D con rotación Euler."""
    crx, srx = math.cos(rx), math.sin(rx)
    cry, sry = math.cos(ry), math.sin(ry)
    crz, srz = math.cos(rz), math.sin(rz)
    out = []
    for x, y, z in pts:
        x1, z1 = x * cry + z * sry, -x * sry + z * cry
        y2, z2 = y * crx - z1 * srx, y * srx + z1 * crx
        x3, y3 = x1 * crz - y2 * srz, x1 * srz + y2 * crz
        fov = 4.2 / max(1.8, 4.2 - z2 * 0.65)
        sx = int(round(cx + x3 * scale * fov))
        sy = int(round(cy + y3 * scale * fov))
        out.append((sx, sy, z2))
    return out


# =========================================================================== escenas

def sc_c5_01(t):
    """c5_01: A principios de los noventa, Sony y Nintendo trabajaban juntas en un lector de CD."""
    cv = bg("bg_sony_lab_1991").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c5_01")
    t_sony = WD("c5_01", "Sony")
    t_nint = WD("c5_01", "Nintendo")
    t_cd = WD("c5_01", "lector")
    t_snes = WD("c5_01", "Super")

    # 1. Osciloscopio activo sobre la mesa (x: 112..142, y: 184..210)
    d.rectangle([113, 185, 141, 209], fill=(10, 34, 28, 255))
    pts = []
    for x in range(114, 141):
        yy = 197 + int(math.sin((x - 114) * 0.45 + t * 9.0) * 7)
        pts.append((x, yy))
    d.line(pts, fill=(95, 250, 155, 255), width=1)

    # 2. Indicadores LED parpadeando en el prototipo sobre la mesa (x: 288..380, y: 185..250)
    for i, (lx, ly, col) in enumerate(((308, 214, GREEN_LED), (314, 214, GOLD), (348, 224, CYAN))):
        if (int(t * 6) + i) % 2 == 0:
            d.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(*col, 90))
            d.rectangle([lx, ly, lx + 1, ly + 1], fill=(*col, 255))
    # Brillo del CD saliendo de la bandeja del prototipo
    draw_cd_disc(cv, 316, 230, 9, t, spin_speed=5.0, glow_col=CYAN)

    # 3. Placa superior principal (margen seguro para zoom)
    a_top, dy_top = pop(t, t0 - 0.1)
    window(cv, 44, 14 + dy_top, 392, 28, border=GOLD)
    draw_text(cv, "PROTOTIPO CD-ROM · SONY + NINTENDO", 240, 22 + dy_top, "press", 8,
              gradient=GOLD_RAMP, align="center")

    # 4. Panel técnico del proyecto conjunto en el centro superior
    if t >= t_sony - 0.15:
        a_p, dy_p = pop(t, t_sony - 0.15)
        window(cv, 54, 48 + dy_p, 372, 92, fill=(14, 20, 44), border=CYAN, alpha=0.92)
        window(cv, 64, 58 + dy_p, 104, 34, fill=(24, 34, 68), border=CYAN)
        draw_text(cv, "SONY", 116, 64 + dy_p, "press", 8, CYAN, align="center")
        draw_text(cv, "AUDIO + CD-ROM", 116, 77 + dy_p, "silk", 8, CREAM, align="center")

        if t >= t_nint - 0.1:
            draw_text(cv, "+", 183, 67 + dy_p, "press", 16, GOLD, align="center")
            window(cv, 198, 58 + dy_p, 114, 34, fill=(48, 22, 36), border=GOLD)
            draw_text(cv, "NINTENDO", 255, 64 + dy_p, "press", 8, GOLD, align="center")
            draw_text(cv, "CONSOLA 16-BIT", 255, 77 + dy_p, "silk", 8, CREAM, align="center")

        draw_cd_disc(cv, 372, 94 + dy_p, 28, t, spin_speed=4.5, glow_col=CYAN)

        if t >= t_cd - 0.1:
            d.rectangle([66, 100 + dy_p, 312, 130 + dy_p], fill=(10, 14, 30, 230), outline=(*GOLD, 200))
            draw_text(cv, "SUPER DISC · 650 MB", 189, 105 + dy_p, "press", 8, CREAM, align="center")
            p_bar = ease_out(prog(t, t_cd, t_snes + 0.6))
            d.rectangle([76, 118 + dy_p, 302, 124 + dy_p], fill=(24, 30, 56, 255))
            d.rectangle([76, 118 + dy_p, 76 + int(226 * p_bar), 124 + dy_p], fill=(*CYAN, 255))

    px = int(120 + (255 - 120) * (0.5 + 0.5 * math.sin(t * 3.2)))
    draw_phosphor_dot(cv, px, 54, r=2, color=GREEN_LED)

    return vignette(cv, 0.32)


def sc_c5_02(t):
    """c5_02: En 1991, Nintendo anunció que lo haría... con Philips."""
    cv = vgradient((10, 12, 30), (26, 28, 58), 12)
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c5_02")
    t_anun = WD("c5_02", "anuncio")
    t_phil = WD("c5_02", "Philips")
    # Mostramos la revelación de la nueva alianza desde el anuncio para que tenga excelente lectura en pantalla
    betray = t >= t_anun - 0.1

    # Telón de fondo de salón de convenciones (CES 1991)
    for x in range(0, W, 24):
        col = (22, 26, 54) if (x // 24) % 2 == 0 else (16, 20, 44)
        d.rectangle([x, 0, x + 23, 182], fill=(*col, 255))
    d.rectangle([0, 182, W, H], fill=(32, 24, 38, 255))
    d.line([(0, 182), (W, 182)], fill=(*GOLD, 255), width=2)

    sp_col = (255, 110, 95) if betray else (120, 210, 255)
    for sx in (130, 240, 350):
        cv = spotlight(cv, sx, 0, 184, 14, 88, color=sp_col, strength=0.18)
    d = ImageDraw.Draw(cv)

    # Gran cartel superior del escenario: "1991 · NUEVA ALIANZA: PHILIPS"
    if not betray:
        window(cv, 44, 14, 392, 42, fill=(18, 26, 58), border=GOLD)
        draw_text(cv, "FERIA CES · JUNIO 1991", 240, 22, "press", 8, GOLD, align="center")
        draw_text(cv, "ANUNCIO OFICIAL EN EL ESCENARIO", 240, 37, "silk", 8, CREAM, align="center")
    else:
        _, dy_b = pop(t, t_anun - 0.1)
        border_c = RED_ALERT if int(t * 8) % 2 == 0 else GOLD
        window(cv, 32, 14 + dy_b, 416, 46, fill=(64, 14, 24), border=border_c)
        draw_text(cv, "1991 · NUEVA ALIANZA: PHILIPS", 240, 24 + dy_b, "press", 8,
                  gradient=GOLD_RAMP, align="center")
        draw_text(cv, "CAMBIO SORPRESA EN PLENA FERIA", 240, 40 + dy_b, "silk", 8,
                  CREAM, align="center")

    # Orador en el podio central
    char(cv, EXEC_1991, 240, 224, t, scale=2,
         arms="wave" if not betray else "point",
         talk=talk_v(t, True),
         mood="happy")
    d.rectangle([212, 166, 268, 226], fill=(76, 48, 36, 255), outline=(*INK, 255))
    d.rectangle([208, 162, 272, 168], fill=(104, 68, 48, 255), outline=(*INK, 255))
    d.rectangle([226, 174, 254, 192], fill=(24, 30, 56, 255), outline=(*GOLD, 255))
    draw_text(cv, "1991", 240, 180, "silk", 8, GOLD, align="center", outline=None, shadow=False)

    # Ingeniero de Sony a la izquierda, perplejo
    char(cv, KUTARAGI, 78, 232, t, scale=2,
         arms="hold" if not betray else "shrug",
         mood="neutral" if not betray else "worried", look=1)
    if betray:
        _, dy_s = pop(t, t_anun + 0.1)
        draw_text(cv, "!?", 78, 114 + dy_s, "press", 16, RED_ALERT, align="center")

    # Siluetas del público en primer plano murmurando
    for i in range(9):
        px = 28 + i * 52
        bob = int(abs(math.sin(t * 7 + i * 1.3)) * (4 if betray else 1))
        py = 248 - bob + (i % 2) * 5
        d.ellipse([px - 13, py - 14, px + 13, py + 10], fill=(10, 10, 20, 255))
        d.rectangle([px - 19, py + 6, px + 19, H], fill=(10, 10, 20, 255))

    # Globos de murmullo y signos de exclamación en la audiencia
    if not betray:
        bubble(cv, "...", 156, 226)
        bubble(cv, "...", 346, 226)
    else:
        for i, (bx, txt) in enumerate(((142, "!"), (312, "¿PHILIPS?"), (402, "!"))):
            tb = t_anun + 0.15 + i * 0.15
            if t >= tb:
                _, dy_m = pop(t, tb)
                bubble(cv, txt, bx, 224 + dy_m)

    if t_phil - 0.05 <= t < t_phil + 0.18:
        k = 1.0 - (t - (t_phil - 0.05)) / 0.23
        cv = fade_to(cv, (255, 90, 90), 0.28 * k)
    dx, dy = shake(t, t_phil - 0.02, 0.32, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.38)


def sc_c5_03(t):
    """c5_03: En Sony, muchos querían dar vuelta la página. Un ingeniero, Ken Kutaragi, no."""
    base = bg("bg_sony_lab_1991").copy()
    cv = grade(base, mul=(0.52, 0.58, 0.78), add=(-8, -6, 6), sat=0.85, k=1.0)
    cv = spotlight(cv, 195, 36, 258, 30, 190, color=(255, 220, 135), strength=0.26)

    t0 = TL.s("c5_03")
    t_ing = WD("c5_03", "ingeniero")
    t_ken = WD("c5_03", "Ken")
    t_no = WD("c5_03", "no")

    # Esquema técnico en cian de la futura consola de discos (100% nítido, sin dithering de alfa en el texto)
    if t >= t_ing - 0.2:
        _, dy_bp = pop(t, t_ing - 0.2)
        window(cv, 248, 44 + dy_bp, 204, 112, fill=(10, 22, 48), border=CYAN, alpha=0.92)
        draw_text(cv, "PROYECTO: PS-X", 350, 52 + dy_bp, "press", 8, CYAN, align="center")
        draw_ps1_unit(cv, 350, 96 + dy_bp, scale=1.05, wireframe=True, t=t)
        draw_text(cv, "CONSOLA CD · 3D", 350, 136 + dy_bp, "silk", 8, GOLD, align="center")

    # Ken Kutaragi trabajando solo de noche en su mesa (scale=3, arms="write")
    arms = "write" if t < t_no - 0.05 else "point"
    mood = "worried" if t < t_ken else "happy"
    char(cv, KUTARAGI, 168, 266, t, scale=3, arms=arms, mood=mood, look=1)

    # Lámpara encendida y planos sobre la mesa
    bulb(cv, 92, 118, t, on=1.0)
    draw_paper(cv, 194, 222, 64, 26, color=(210, 232, 255))
    scribble(cv, 200, 230, 50, prog(t, t0, t_no), seed=3, color=(30, 90, 180))

    # Placa superior con margen seguro para cámara
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 24, 16 + dy_top, 212, 26, border=GOLD)
    draw_text(cv, "TOKIO · MEDIANOCHE", 130, 23 + dy_top, "press", 8, CREAM, align="center")

    # Remate "ÉL DIJO QUE NO" cuando nombra a Kutaragi / dice "no"
    if t >= t_ken + 0.25:
        _, dy_no = pop(t, t_ken + 0.25)
        window(cv, 248, 164 + dy_no, 204, 36, fill=(48, 16, 36), border=GOLD)
        draw_text(cv, "ÉL DIJO QUE NO.", 350, 172 + dy_no, "press", 8, GOLD, align="center")
        draw_text(cv, "SIGUIÓ EN SECRETO", 350, 185 + dy_no, "silk", 8, CREAM, align="center")

    # Lower third reglamentario: empieza en t_ing - 0.25 para estar 100% opaco durante toda la mención a Kutaragi
    lower_third(cv, "KEN KUTARAGI", "INGENIERO · SONY", t, t_ing - 0.25, TL.e("c5_03") + 0.35, x=20, y=210)

    return vignette(cv, 0.38)


OCTA_V = [(0, -1.3, 0), (1.1, 0, 0), (0, 0, 1.1), (-1.1, 0, 0), (0, 0, -1.1), (0, 1.3, 0)]
OCTA_F = [
    (0, 1, 2, (255, 195, 70)), (0, 2, 3, (235, 130, 45)),
    (0, 3, 4, (200, 85, 35)),  (0, 4, 1, (250, 160, 55)),
    (5, 2, 1, (220, 115, 40)), (5, 3, 2, (185, 70, 30)),
    (5, 4, 3, (160, 55, 28)),  (5, 1, 4, (210, 100, 38)),
]
CUBE_V = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
          (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
CUBE_E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
          (0, 4), (1, 5), (2, 6), (3, 7)]


def sc_c5_04(t):
    """c5_04: El 3 de diciembre de 1994, Sony lanzó en Japón su propia consola. Usaba CD. Apostaba todo al 3D."""
    cv = new_canvas((4, 6, 14))
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c5_04")
    t_con = WD("c5_04", "consola")
    t_cd = WD("c5_04", "Usaba")
    t_3d = WD("c5_04", "tres", occurrence=2)

    dt = max(0.0, t - (t0 - 0.15))

    # Grilla 3D en perspectiva en el piso
    g_alpha = clamp01(dt / 1.2)
    if g_alpha > 0:
        hzn = 176
        for i in range(1, 8):
            yy = hzn + int((i / 7) ** 1.6 * (H - hzn))
            c_line = tuple(int(v * g_alpha) for v in (28, 70, 120))
            d.line([(0, yy), (W, yy)], fill=(*c_line, 255))
        for k in range(-8, 9):
            x_top = 240 + k * 14
            x_bot = 240 + k * 54
            c_line = tuple(int(v * g_alpha) for v in (24, 58, 104))
            d.line([(x_top, hzn), (x_bot, H)], fill=(*c_line, 255))

    # Diamante poligonal 3D con flat-shading girando y ensamblándose en el centro
    assemble = ease_out(clamp01((dt - 0.15) / 1.1))
    if assemble > 0:
        pts2d = project_3d(OCTA_V, rx=0.35 + t * 0.9, ry=t * 1.45, rz=0.15, cx=240, cy=112, scale=44 * assemble)
        faces_sorted = sorted(
            OCTA_F,
            key=lambda f: (pts2d[f[0]][2] + pts2d[f[1]][2] + pts2d[f[2]][2]) / 3.0
        )
        for i0, i1, i2, col in faces_sorted:
            spread = int((1.0 - assemble) * 28)
            p0 = (pts2d[i0][0] - spread, pts2d[i0][1] - spread)
            p1 = (pts2d[i1][0] + spread, pts2d[i1][1])
            p2 = (pts2d[i2][0], pts2d[i2][1] + spread)
            d.polygon([p0, p1, p2], fill=(*col, 255), outline=(*GOLD, 255))

    if t >= t_con - 0.2:
        c_pts_l = project_3d(CUBE_V, rx=t * 1.3, ry=t * 1.1, rz=0.4, cx=88, cy=114, scale=22)
        for a, b in CUBE_E:
            d.line([(c_pts_l[a][0], c_pts_l[a][1]), (c_pts_l[b][0], c_pts_l[b][1])], fill=(*CYAN, 255))
    if t >= t_cd - 0.1:
        draw_cd_disc(cv, 392, 114, 28, t, spin_speed=6.5, glow_col=CYAN)
        draw_text(cv, "CD-ROM", 392, 148, "press", 8, CYAN, align="center")
    if t >= t_3d - 0.25:
        c_pts_r = project_3d(CUBE_V, rx=-t * 1.2, ry=t * 1.6, rz=0.7, cx=88, cy=114, scale=26)
        for a, b in CUBE_E:
            d.line([(c_pts_r[a][0], c_pts_r[a][1]), (c_pts_r[b][0], c_pts_r[b][1])], fill=(*MAGENTA, 255))
        draw_text(cv, "360.000 POLÍGONOS/S", 240, 162, "silk", 8, GOLD, align="center")

    # Consola gris en la parte inferior encendiendo su LED verde
    draw_ps1_unit(cv, 240, 222, scale=1.2, lid_open=0.0, power_on=(dt > 0.08), t=t)

    # Placa reglamentaria: "3 · 12 · 1994 · JAPÓN · ERA 3D"
    _, dy_w = pop(t, t0 - 0.1)
    window(cv, 52, 16 + dy_w, 376, 30, fill=(16, 20, 46), border=GOLD)
    draw_text(cv, "3 · 12 · 1994 · JAPÓN · ERA 3D", 240, 24 + dy_w, "press", 8,
              gradient=GOLD_RAMP, align="center")

    ox = 240 + int(math.cos(t * 3.5) * 62)
    oy = 112 + int(math.sin(t * 3.5) * 32)
    draw_phosphor_dot(cv, ox, oy, r=2, color=GREEN_LED)

    return vignette(cv, 0.35)


def sc_c5_05(t):
    """c5_05: Se llamaba PlayStation. Vendió más de ciento dos millones."""
    cv = bg("bg_living_1995").copy()
    d = ImageDraw.Draw(cv)
    t0 = TL.s("c5_05")
    t_ven = WD("c5_05", "Vendio")
    t_mill = WD("c5_05", "millones")

    # 1. Juego 3D de carreras poligonal en la pantalla del televisor de tubo
    d.rectangle([383, 105, 427, 147], fill=(18, 28, 68, 255))
    d.rectangle([383, 126, 427, 147], fill=(40, 44, 62, 255))
    road_off = int(math.sin(t * 4.0) * 6)
    d.polygon([(405 + road_off, 126), (386, 147), (424, 147)], fill=(78, 82, 100, 255))
    if int(t * 10) % 2 == 0:
        d.line([(405 + road_off, 127), (405, 146)], fill=(255, 230, 120, 255))
    d.rectangle([400, 138, 411, 144], fill=(235, 65, 65, 255), outline=(*INK, 255))

    # LED verde encendido en la PlayStation del piso
    d.ellipse([352, 236, 358, 242], fill=(80, 255, 120, 140))
    d.point((355, 239), fill=(200, 255, 210, 255))

    # 2. Dos adolescentes de los 90 jugando sentados frente al TV
    won = t >= t_mill - 0.1
    char(cv, TEEN_A, 198, 236, t, scale=3, sit=True,
         arms="cheer" if won else "hold",
         mood="happy", look=1)
    char(cv, TEEN_B, 282, 242, t, scale=3, sit=True,
         arms="cheer" if won else "type",
         mood="happy", look=1)

    # 3. Placa superior reglamentaria: "PLAYSTATION · +102 MILLONES"
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 48, 14 + dy_top, 384, 30, border=GOLD)
    draw_text(cv, "PLAYSTATION · +102 MILLONES", 240, 22 + dy_top, "press", 8,
              gradient=GOLD_RAMP, align="center")

    # 4. Contador animado que sube hasta +102 MILLONES
    if t >= t_ven - 0.15:
        _, dy_c = pop(t, t_ven - 0.15)
        window(cv, 48, 52 + dy_c, 268, 56, fill=(16, 22, 50), border=CYAN)
        p_cnt = ease_out(prog(t, t_ven - 0.05, t_mill + 0.15))
        val = int(round(102 * p_cnt))
        prefix = "+" if p_cnt >= 0.98 else ""
        draw_text(cv, f"{prefix}{val} MILLONES", 182, 60 + dy_c, "press", 16,
                  gradient=GOLD_RAMP if p_cnt >= 0.98 else CYAN_RAMP, align="center")
        draw_text(cv, "CONSOLAS VENDIDAS EN EL MUNDO", 182, 86 + dy_c, "silk", 8, CREAM, align="center")
        if p_cnt >= 0.98:
            for i in range(4):
                sparkle(cv, 72 + i * 72, 58 + dy_c + (i % 2) * 26, t + i * 0.7, 3, GOLD)

    return vignette(cv, 0.32)


def sc_c5_06(t):
    """c5_06: Nintendo había perdido un socio... Y había ganado un rival."""
    cv = vgradient((8, 10, 24), (18, 16, 38), 12)
    STARS.draw(cv, t * 0.3, alpha=0.45)
    d = ImageDraw.Draw(cv)

    t_perd = WD("c5_06", "perdido")
    t_soc = WD("c5_06", "socio")
    t_riv = WD("c5_06", "rival") - 0.15

    # Encabezado
    window(cv, 84, 14, 312, 26, fill=(18, 22, 48), border=GOLD)
    draw_text(cv, "EL CAMBIO DE ERA · 1991 → 1996", 240, 21, "press", 8, GOLD, align="center")

    # --- COLUMNA IZQUIERDA: SOCIO (se apaga a gris oscuro) ---
    dim = ease_in_out(prog(t, t_perd - 0.1, t_soc + 0.35))
    col_l_border = tuple(int(a + (b - a) * dim) for a, b in zip(CYAN, (68, 72, 88)))
    col_l_fill = tuple(int(a + (b - a) * dim) for a, b in zip((20, 32, 64), (18, 20, 28)))
    col_l_txt = tuple(int(a + (b - a) * dim) for a, b in zip(CREAM, (92, 96, 112)))

    window(cv, 22, 48, 208, 196, fill=col_l_fill, border=col_l_border)
    draw_text(cv, "SOCIO", 126, 64, "press", 24, col_l_txt, align="center")
    draw_text(cv, "ALIANZA 1991", 126, 98, "silk", 8, col_l_txt, align="center")

    cx_l, cy_l = 126, 152
    d.rectangle([cx_l - 48, cy_l - 14, cx_l - 8, cy_l + 14], fill=(*col_l_border, 255), outline=(*INK, 255))
    d.rectangle([cx_l + 8, cy_l - 14, cx_l + 48, cy_l + 14], fill=(*col_l_border, 255), outline=(*INK, 255))
    if dim < 0.5:
        d.line([(cx_l - 8, cy_l), (cx_l + 8, cy_l)], fill=(*GOLD, 255), width=3)
    else:
        d.line([(cx_l - 14, cy_l - 14), (cx_l + 14, cy_l + 14)], fill=(*RED_ALERT, 255), width=3)
        d.line([(cx_l - 14, cy_l + 14), (cx_l + 14, cy_l - 14)], fill=(*RED_ALERT, 255), width=3)
    draw_text(cv, "PROYECTO CANCELADO", 126, 206, "press", 8, col_l_txt, align="center")

    # --- COLUMNA DERECHA: RIVAL (se enciende en magenta/cian intenso en TL.word("c5_06", "rival") - 0.15) ---
    ignite = ease_out(prog(t, t_riv, t_riv + 0.35))
    if ignite <= 0:
        window(cv, 250, 48, 208, 196, fill=(14, 14, 24), border=(46, 48, 64))
        draw_text(cv, "RIVAL", 354, 64, "press", 24, (58, 60, 78), align="center")
    else:
        _, dy_r = pop(t, t_riv)
        b_col = MAGENTA if int((t - t_riv) * 8) % 2 == 0 else CYAN
        d.rectangle([247, 45 + dy_r, 461, 247 + dy_r], outline=(*MAGENTA, int(180 * ignite)), width=2)
        window(cv, 250, 48 + dy_r, 208, 196, fill=(38, 14, 52), border=b_col)
        draw_text(cv, "RIVAL", 354, 64 + dy_r, "press", 24, gradient=CYAN_RAMP, align="center", outline_w=2)
        draw_text(cv, "NUEVO LÍDER · 3D", 354, 98 + dy_r, "press", 8, MAGENTA, align="center")

        pts_r = project_3d(OCTA_V, rx=0.4 + t * 1.4, ry=t * 2.0, rz=0.2, cx=354, cy=152 + dy_r, scale=30)
        for i0, i1, i2, _ in OCTA_F[:4]:
            d.polygon([(pts_r[i0][0], pts_r[i0][1]), (pts_r[i1][0], pts_r[i1][1]), (pts_r[i2][0], pts_r[i2][1])],
                      fill=(210, 60, 150, 210), outline=(*CYAN, 255))
        draw_text(cv, "+102M CONSOLAS", 354, 206 + dy_r, "press", 8, GOLD, align="center")
        for i in range(5):
            sparkle(cv, 272 + i * 40, 58 + dy_r + (i % 2) * 168, t + i * 0.4, 3, CYAN if i % 2 else MAGENTA)
        draw_phosphor_dot(cv, 354, 152 + dy_r, r=3, color=CYAN)

    dx, dy = shake(t, t_riv, 0.3, 4)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


# =========================================================================== montaje

def scenes():
    c5s = TL.chapter_start(5)
    return [
        (c5s - 0.3, make_card(5, ["LA TRAICIÓN"], "1991 – 1996"), None),
        (TL.s("c5_01") - 0.2, sc_c5_01,
         lambda t: (cam_push(t, TL.s("c5_01"), TL.e("c5_01"), 1.0, 1.06, (240, 135), (240, 135))[0]
                    + cam_punch(t, [WD("c5_01", "Sony"), WD("c5_01", "Nintendo")], 0.05),
                    240, 135)),
        (TL.s("c5_02") - 0.2, sc_c5_02,
         lambda t: (1.0 + cam_punch(t, [WD("c5_02", "anuncio"), WD("c5_02", "Philips")], 0.08), 240, 135)),
        (TL.s("c5_03") - 0.2, sc_c5_03,
         lambda t: (cam_push(t, TL.s("c5_03"), TL.e("c5_03"), 1.0, 1.06, (240, 135), (240, 135))[0]
                    + cam_punch(t, [WD("c5_03", "Ken"), WD("c5_03", "no")], 0.06),
                    240, 135)),
        (TL.s("c5_04") - 0.2, sc_c5_04,
         lambda t: (cam_push(t, TL.s("c5_04"), TL.e("c5_04"), 1.0, 1.08, (240, 135), (240, 135))[0]
                    + cam_punch(t, [WD("c5_04", "consola"), WD("c5_04", "tres", occurrence=2)], 0.06),
                    240, 135)),
        (TL.s("c5_05") - 0.2, sc_c5_05,
         lambda t: (1.0 + cam_punch(t, [WD("c5_05", "PlayStation"), WD("c5_05", "ciento")], 0.07), 240, 135)),
        (TL.s("c5_06") - 0.15, sc_c5_06,
         lambda t: (1.0 + cam_punch(t, [WD("c5_06", "socio"), WD("c5_06", "rival") - 0.15], 0.08), 240, 135)),
    ]


# =========================================================================== audio

def music(A):
    c5s = TL.chapter_start(5) + 1.6
    t_betray = TL.s("c5_02")
    t_kuta = TL.s("c5_03")
    t_boot = TL.s("c5_04")
    t_ps = TL.s("c5_05")
    c5e = chapter_end(5)

    A.section(c5s, t_betray, 108, [("A", "min"), ("F", "maj"), ("G", "maj"), ("E", "min")], A.st_mystery)
    A.section(t_betray, t_kuta, 114, [("D", "min"), ("Bb", "maj"), ("A", "min"), ("A", "min")], A.st_rain)
    A.section(t_kuta, t_boot, 116, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_build)
    A.section(t_boot + 1.8, t_ps, 124, [("D", "min"), ("Bb", "maj"), ("F", "maj"), ("C", "maj")], A.st_bright)
    A.section(t_ps, c5e, 126, [("A", "min"), ("F", "maj"), ("C", "maj"), ("G", "maj")], A.st_triumph)


def sfx(A):
    A.pop_sfx(WD("c5_01", "Sony"), 540)
    A.pop_sfx(WD("c5_01", "Nintendo"), 660)
    A.blip(WD("c5_01", "lector"), 1350)

    A.whoosh(TL.s("c5_02") - 0.15)
    t_phil = WD("c5_02", "Philips")
    A.crash(A.sfx, t_phil - 0.04, 0.18)
    A.sting(t_phil, [62, 61, 57], vol=0.055, step=0.14, hold=0.8)

    A.join_jingle(WD("c5_03", "Ken") - 0.1)
    A.chalk(TL.s("c5_03") + 0.3, WD("c5_03", "no") - 0.2, vol=0.025)
    A.pop_sfx(WD("c5_03", "no"), 480)

    A.ps1_boot(TL.s("c5_04") - 0.05)
    A.pop_sfx(WD("c5_04", "tres", occurrence=2), 760)

    A.coin(WD("c5_05", "PlayStation"))
    A.text_blips(WD("c5_05", "Vendio"), 14, 18, f=1400)
    A.join_jingle(WD("c5_05", "millones"))

    A.crt_off(WD("c5_06", "socio") - 0.05, vol=0.05)
    t_riv = WD("c5_06", "rival") - 0.15
    A.whoosh(t_riv, 0.3, 0.07)
    A.sting(t_riv + 0.05, [69, 72, 76, 81], vol=0.06, step=0.1, hold=1.1)
