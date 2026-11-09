"""Capítulo 6: La ciudad abierta (2000 – 2005)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from common import *  # noqa

WD = TL.word

C = S.hexc
PED_A = dict(
    name="Peatón A", skin=S.SKIN["tan"], hair=C("181418"), hair_style="short",
    top="trench", top_color=C("384052"), shirt=C("d8dce4"), pants=C("222634")
)
PED_B = dict(
    name="Peatón B", skin=S.SKIN["fair"], hair=C("5a3824"), hair_style="crew",
    top="hoodie", top_color=C("285848"), pants=C("242a3a")
)

PS2_BLUE = (55, 155, 255)
PS2_CYAN = (110, 225, 255)
GREEN_LED = (85, 250, 130)
CITY_RAIN = Rain(110, seed=19, region=(0, 0, W, H), color=(150, 175, 210), speed=240, slant=0.18)


# =========================================================================== helpers

def draw_dvd_disc(cv, cx, cy, r, t, spin_speed=5.0):
    """Dibuja un disco DVD dorado/plateado girando con aura azul eléctrico."""
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(*PS2_BLUE, 55))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(210, 220, 240, 255), outline=(*INK, 255))
    ang0 = t * spin_speed
    for k in range(2):
        a = ang0 + k * math.pi
        for da, col in ((-0.22, PS2_BLUE), (0.0, (255, 255, 255)), (0.22, GOLD)):
            x1 = cx + int(math.cos(a + da) * (r - 2))
            y1 = cy + int(math.sin(a + da) * (r - 2))
            x0 = cx + int(math.cos(a + da) * max(4, r // 3))
            y0 = cy + int(math.sin(a + da) * max(4, r // 3))
            d.line([(x0, y0), (x1, y1)], fill=(*col, 255), width=2 if da == 0.0 else 1)
    ir = max(4, r // 3)
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(90, 130, 190, 255), outline=(*INK, 255))
    hr = max(2, r // 6)
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(14, 18, 36, 255))


def draw_ps2_aura(cv, t, boost=1.0):
    """Aura azul eléctrico pulsante alrededor del monolito negro de PS2 en bg_ps2_shelf_2000."""
    d = ImageDraw.Draw(cv)
    pulse = (0.55 + 0.45 * math.sin(t * 5.0)) * boost
    for pad, alpha in ((10, int(28 * pulse)), (6, int(52 * pulse)), (3, int(85 * pulse))):
        d.rectangle([162 - pad, 76 - pad, 208 + pad, 194 + pad], outline=(*PS2_BLUE, alpha), width=2)
    d.ellipse([178, 82, 184, 88], fill=(80, 190, 255, 220))
    d.point((181, 85), fill=(220, 248, 255, 255))
    d.ellipse([190, 82, 196, 88], fill=(80, 255, 140, 200))
    d.point((193, 85), fill=(220, 255, 230, 255))
    for i in range(10):
        px = 135 + (i * 23) % 210
        py = 190 - int(((t * 24 + i * 19) % 140))
        sz = 2 if i % 3 == 0 else 1
        d.rectangle([px, py, px + sz, py + sz], fill=(*PS2_CYAN, int(150 * pulse)))


def draw_pixel_car(cv, x, y, direction=1, body_col=(210, 55, 55), lights_on=True):
    """Dibuja un auto en pixel art con faros y reflejos sobre el asfalto mojado."""
    d = ImageDraw.Draw(cv)
    w, h = 38, 16
    x0, y0 = int(x) - w // 2, int(y) - h
    x1, y1 = x0 + w, y0 + h
    d.rectangle([x0 + 2, y1, x1 - 2, y1 + 3], fill=(10, 12, 22, 160))
    if lights_on:
        if direction > 0:
            d.polygon([(x1, y0 + 7), (x1 + 44, y0 + 2), (x1 + 44, y1 + 5), (x1, y0 + 12)],
                      fill=(255, 240, 165, 75))
            d.rectangle([x1 - 2, y1 + 1, x1 + 16, y1 + 3], fill=(255, 220, 120, 90))
        else:
            d.polygon([(x0, y0 + 7), (x0 - 44, y0 + 2), (x0 - 44, y1 + 5), (x0, y0 + 12)],
                      fill=(255, 240, 165, 75))
            d.rectangle([x0 - 16, y1 + 1, x0 + 2, y1 + 3], fill=(255, 220, 120, 90))
    d.rectangle([x0, y0 + 6, x1, y1 - 2], fill=(*body_col, 255), outline=(*INK, 255))
    cx0 = x0 + (7 if direction > 0 else 9)
    cx1 = x1 - (9 if direction > 0 else 7)
    d.rectangle([cx0, y0, cx1, y0 + 7], fill=(*shade(body_col, 0.88), 255), outline=(*INK, 255))
    d.rectangle([cx0 + 2, y0 + 2, cx1 - 2, y0 + 6], fill=(50, 80, 115, 255))
    for wx in (x0 + 6, x1 - 10):
        d.rectangle([wx, y1 - 4, wx + 6, y1], fill=(24, 24, 32, 255), outline=(*INK, 255))
        d.rectangle([wx + 2, y1 - 2, wx + 4, y1 - 1], fill=(140, 146, 160, 255))
    if direction > 0:
        d.rectangle([x1 - 2, y0 + 8, x1, y0 + 11], fill=(255, 248, 190, 255))
        d.rectangle([x0, y0 + 8, x0 + 2, y0 + 11], fill=(240, 50, 50, 255))
    else:
        d.rectangle([x0, y0 + 8, x0 + 2, y0 + 11], fill=(255, 248, 190, 255))
        d.rectangle([x1 - 2, y0 + 8, x1, y0 + 11], fill=(240, 50, 50, 255))


def draw_radar_minimap(cv, cx, cy, r, t):
    """Dibuja el clásico radar circular de mundo abierto en la esquina inferior."""
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(*INK, 240))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 38, 48, 235), outline=(180, 200, 215, 255))
    off_x = int((t * 14) % 14) - 7
    for k in (-10, 0, 10):
        xx = cx + k - off_x
        if cx - r + 4 < xx < cx + r - 4:
            d.line([(xx, cy - r + 5), (xx, cy + r - 5)], fill=(58, 78, 92, 255), width=3)
        yy = cy + k
        if cy - r + 4 < yy < cy + r - 4:
            d.line([(cx - r + 5, yy), (cx + r - 5, yy)], fill=(58, 78, 92, 255), width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*CYAN, 220), width=2)
    d.rectangle([cx - 5, cy - r - 5, cx + 5, cy - r + 4], fill=(*INK, 255), outline=(*GOLD, 255))
    draw_text(cv, "N", cx, cy - r - 4, "silk", 8, GOLD, align="center", outline=None, shadow=False)
    if int(t * 5) % 2 == 0:
        d.rectangle([cx + 8, cy - 10, cx + 12, cy - 6], fill=(255, 85, 85, 255), outline=(*INK, 255))
    d.rectangle([cx - 12, cy + 6, cx - 8, cy + 10], fill=(*GOLD, 255), outline=(*INK, 255))
    d.polygon([(cx, cy - 5), (cx - 4, cy + 4), (cx + 4, cy + 4)], fill=(*CREAM, 255), outline=(*INK, 255))


def draw_topdown_city(t, zoom_step=1):
    """Mapa cenital 2D de ciudad nocturna (tipo GTA clásico) con zoom por pasos enteros."""
    w0, h0 = W // zoom_step, H // zoom_step
    im = Image.new("RGBA", (w0, h0), (14, 18, 28, 255))
    d = ImageDraw.Draw(im)
    block = 36
    for x in range(12, w0, block):
        d.rectangle([x, 0, x + 10, h0], fill=(34, 40, 54, 255))
        for y in range(2, h0, 8):
            d.point((x + 5, y), fill=(210, 180, 90, 200))
    for y in range(10, h0, block):
        d.rectangle([0, y, w0, y + 10], fill=(34, 40, 54, 255))
        for x in range(2, w0, 8):
            d.point((x, y + 5), fill=(210, 180, 90, 200))
    for bx in range(24, w0 - 12, block):
        for by in range(22, h0 - 12, block):
            d.rectangle([bx, by, bx + 22, by + 22], fill=(22, 28, 44, 255), outline=(48, 60, 86, 255))
            d.rectangle([bx + 3, by + 3, bx + 19, by + 19], fill=(28, 36, 56, 255))
            if (bx + by) % 3 == 0:
                d.point((bx + 6, by + 6), fill=(255, 210, 110, 255))
                d.point((bx + 14, by + 12), fill=(110, 220, 255, 255))
    for i in range(6):
        vx = int((t * 28 + i * 47) % max(1, w0))
        vy = 10 + (i % 4) * block + 3
        col = (240, 70, 70) if i % 2 == 0 else (255, 220, 90)
        d.rectangle([vx, vy, vx + 4, vy + 2], fill=(*col, 255))
    arr = upscale(np.array(im), zoom_step)[:H, :W]
    return Image.fromarray(arr, "RGBA")


# =========================================================================== escenas

def sc_c6_01(t):
    """c6_01: En el año 2000 llegó la PlayStation 2. Además de juegos, leía DVD."""
    cv = bg("bg_ps2_shelf_2000").copy()
    draw_ps2_aura(cv, t, boost=1.0)

    t0 = TL.s("c6_01")
    t_ps2 = WD("c6_01", "PlayStation")
    t_jue = WD("c6_01", "juegos")
    t_dvd = WD("c6_01", "leia")
    t_pel = WD("c6_01", "peliculas")

    # Placa superior reglamentaria: "PLAYSTATION 2 · 2000 · JUEGOS + DVD"
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 36, 14 + dy_top, 408, 30, fill=(12, 20, 46), border=PS2_CYAN)
    draw_text(cv, "PLAYSTATION 2 · 2000 · JUEGOS + DVD", 240, 22 + dy_top, "press", 8,
              gradient=CYAN_RAMP, align="center")

    # Etiqueta sobre el monolito negro (izquierda, dentro de margen seguro x >= 24)
    if t >= t_ps2 - 0.15:
        _, dy_m = pop(t, t_ps2 - 0.15)
        window(cv, 24, 86 + dy_m, 126, 54, fill=(10, 18, 42), border=PS2_BLUE)
        draw_text(cv, "MONOLITO", 87, 94 + dy_m, "press", 8, PS2_CYAN, align="center")
        draw_text(cv, "128 BITS", 87, 108 + dy_m, "press", 8, CREAM, align="center")
        draw_text(cv, "MARZO 2000", 87, 122 + dy_m, "silk", 8, GOLD, align="center")

    # Panel derecho con disco DVD girando (dentro de margen seguro x1 <= 448)
    if t >= t_jue - 0.15:
        _, dy_d = pop(t, t_jue - 0.15)
        window(cv, 220, 50 + dy_d, 224, 62, fill=(12, 22, 50), border=GOLD)
        draw_dvd_disc(cv, 254, 81 + dy_d, 21, t, spin_speed=5.5)
        draw_text(cv, "+ JUEGOS 3D", 288, 59 + dy_d, "press", 8, PS2_CYAN)
        if t >= t_dvd - 0.1:
            draw_text(cv, "+ LECTOR DVD", 288, 75 + dy_d, "press", 8, GOLD)
        if t >= t_pel - 0.25:
            draw_text(cv, "CINE EN CASA", 288, 91 + dy_d, "silk", 8, CREAM)

    if t >= t_dvd:
        for i in range(4):
            sparkle(cv, 256 + i * 28, 128 + (i % 2) * 34, t + i * 0.6, 3, PS2_CYAN)

    return vignette(cv, 0.32)


def sc_c6_02(t):
    """c6_02: Vendió más de 160 millones: todavía hoy es la consola más vendida de la historia."""
    cv = bg("bg_ps2_shelf_2000").copy()
    draw_ps2_aura(cv, t, boost=1.25)

    t0 = TL.s("c6_02")
    t_mill = WD("c6_02", "millones")
    t_ven = WD("c6_02", "vendida")

    # Placa superior reglamentaria: "+160 MILLONES · LA CONSOLA MÁS VENDIDA"
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 20, 12 + dy_top, 440, 30, fill=(14, 22, 52), border=GOLD)
    draw_text(cv, "+160 MILLONES · LA CONSOLA MÁS VENDIDA", 240, 20 + dy_top, "press", 8,
              gradient=GOLD_RAMP, align="center")

    # Gran contador central animado que sube de 0 a +160 MILLONES
    p_cnt = ease_out(prog(t, t0 - 0.05, t_mill + 0.1))
    val = int(round(160 * p_cnt))
    locked = p_cnt >= 0.99

    border_c = GOLD if locked else PS2_CYAN
    window(cv, 64, 56, 352, 92, fill=(10, 18, 44), border=border_c, alpha=0.94)
    prefix = "+" if locked else ""
    draw_text(cv, f"{prefix}{val}", 240, 66, "press", 32,
              gradient=GOLD_RAMP if locked else CYAN_RAMP, align="center", outline_w=2)
    draw_text(cv, "MILLONES DE UNIDADES", 240, 106, "press", 8, CREAM, align="center")
    draw_text(cv, "RÉCORD MUNDIAL ABSOLUTO", 240, 124, "silk", 8, GOLD if locked else PS2_CYAN, align="center")

    if t >= t_ven - 0.15:
        _, dy_r = pop(t, t_ven - 0.15)
        window(cv, 96, 160 + dy_r, 288, 34, fill=(48, 34, 14), border=GOLD)
        draw_text(cv, "#1 EN TODA LA HISTORIA", 240, 171 + dy_r, "press", 8,
                  gradient=GOLD_RAMP, align="center")

    if locked:
        for i in range(8):
            sx = 80 + i * 44
            sy = 64 + (i % 3) * 32
            sparkle(cv, sx, sy, t + i * 0.45, 4, GOLD if i % 2 == 0 else PS2_CYAN)
        draw_phosphor_dot(cv, 240, 50, r=3, color=GOLD)

    dx, dy = shake(t, t_mill + 0.05, 0.25, 3)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.32)


def sc_c6_03(t):
    """c6_03: Y en octubre de 2001, un estudio de Edimburgo publicó un juego que cambió las reglas: GTA III."""
    t0 = TL.s("c6_03")
    t_edi = WD("c6_03", "Edimburgo")
    t_jue = WD("c6_03", "juego")
    t_reg = WD("c6_03", "reglas")
    t_gta = WD("c6_03", "Grand")

    # Vista cenital nocturna que baja por pasos enteros de zoom (1 -> 2 -> 3) hacia nivel de calle
    if t < t_edi:
        cv = draw_topdown_city(t, zoom_step=1)
        step_label = "VISTA CENITAL 2D · ZOOM 1X"
    elif t < t_jue:
        cv = draw_topdown_city(t, zoom_step=2)
        step_label = "ACERCAMIENTO · ZOOM 2X"
    elif t < t_reg:
        cv = draw_topdown_city(t, zoom_step=3)
        step_label = "DESCENSO A LA CALLE · ZOOM 3X"
    else:
        top_cv = draw_topdown_city(t, zoom_step=3)
        street_cv = bg("bg_open_city_2001").copy()
        CITY_RAIN.draw(street_cv, t, alpha=160)
        k = ease_in_out(prog(t, t_reg, t_reg + 0.45))
        cv = dither_mix(top_cv, street_cv, k)
        step_label = "SALTO AL 3D · LIBERTY CITY"

    d = ImageDraw.Draw(cv)
    if t < t_reg + 0.2:
        d.rectangle([16, 48, 464, 254], outline=(*CYAN, 110))
        d.line([(240, 48), (240, 254)], fill=(*CYAN, 70))
        d.line([(16, 151), (464, 151)], fill=(*CYAN, 70))

    # Placa superior reglamentaria: "GTA III · 2001 · EDIMBURGO"
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 64, 12 + dy_top, 352, 30, fill=(16, 20, 42), border=GOLD)
    draw_text(cv, "GTA III · 2001 · EDIMBURGO", 240, 20 + dy_top, "press", 8,
              gradient=GOLD_RAMP, align="center")

    window(cv, 24, 48, 224, 24, fill=(12, 18, 36), border=CYAN)
    draw_text(cv, step_label, 136, 55, "silk", 8, CYAN, align="center")

    # Placa de título cuando cambia las reglas -> Grand Theft Auto III
    if t >= t_reg + 0.15:
        _, dy_g = pop(t, t_reg + 0.15)
        window(cv, 44, 182 + dy_g, 392, 62, fill=(14, 16, 30), border=GOLD, alpha=0.94)
        draw_text(cv, "GRAND THEFT AUTO III", 240, 192 + dy_g, "press", 16,
                  gradient=GOLD_RAMP, align="center")
        draw_text(cv, "OCTUBRE 2001 · CAMBIÓ LAS REGLAS", 240, 218 + dy_g, "press", 8,
                  CREAM, align="center")

    dx, dy = shake(t, t_gta - 0.05, 0.28, 3)
    cv = offset_canvas(cv, dx, dy)
    return vignette(cv, 0.35)


def sc_c6_04(t):
    """c6_04: Una ciudad entera, en 3D, donde podías ir a donde quisieras. Ya no era un nivel. Era un mundo."""
    cv = bg("bg_open_city_2001").copy()
    d = ImageDraw.Draw(cv)

    t0 = TL.s("c6_04")
    t_qui = WD("c6_04", "quisieras")
    t_niv = WD("c6_04", "nivel")
    t_mun = WD("c6_04", "mundo")

    # 1. Semáforos cambiando rojo / amarillo / verde
    state = int((t - t0) * 1.4) % 3
    sem_cols = [(255, 65, 65), (255, 215, 70), (75, 250, 115)]
    active_col = sem_cols[state]
    for sx, sy in ((192, 134), (242, 141), (250, 141)):
        d.rectangle([sx - 3, sy - 2, sx + 3, sy + 14], fill=(18, 20, 28, 240), outline=(*INK, 255))
        ly = sy + state * 4
        d.ellipse([sx - 4, ly - 3, sx + 4, ly + 5], fill=(*active_col, 95))
        d.rectangle([sx - 1, ly, sx + 1, ly + 2], fill=(*active_col, 255))

    # 2. Peatones caminando por las veredas
    px1, ph1 = walk(t, t0 - 0.5, TL.e("c6_04") + 1.0, 96, 178)
    char(cv, PED_A, px1, 204, t, scale=1, walk=ph1, arms="down", facing=1)
    px2, ph2 = walk(t, t0 - 0.5, TL.e("c6_04") + 1.0, 396, 308)
    char(cv, PED_B, px2, 206, t, scale=1, walk=ph2, arms="down", facing=-1)

    # 3. Autos pixelados con faros cruzando la calle mojada (frecuencia para que siempre haya autos en pantalla)
    car1_x = 60 + ((t - t0) * 78) % 360
    car2_x = 420 - ((t - t0 + 1.4) * 68) % 360
    draw_pixel_car(cv, car2_x, 210, direction=-1, body_col=(65, 135, 220), lights_on=True)
    draw_pixel_car(cv, car1_x, 228, direction=1, body_col=(215, 60, 60), lights_on=True)

    # Lluvia nocturna suave
    CITY_RAIN.draw(cv, t, alpha=150)

    # 4. Mini-mapa radar circular en esquina inferior izquierda (con margen seguro para el paneo de cámara)
    draw_radar_minimap(cv, 76, 218, 24, t)

    # 5. Placa superior reglamentaria: "YA NO ERA UN NIVEL · ERA UN MUNDO" (en y=18 para margen con zoom 1.08)
    _, dy_top = pop(t, t0 - 0.1)
    window(cv, 44, 18 + dy_top, 392, 30, fill=(14, 18, 38), border=GOLD)
    draw_text(cv, "YA NO ERA UN NIVEL · ERA UN MUNDO", 240, 26 + dy_top, "press", 8,
              gradient=GOLD_RAMP, align="center")

    # Etiquetas dinámicas sincronizadas con la voz
    if t >= t_qui - 0.15 and t < t_niv - 0.1:
        _, dy_q = pop(t, t_qui - 0.15)
        window(cv, 128, 54 + dy_q, 224, 24, fill=(14, 24, 48), border=CYAN)
        draw_text(cv, "LIBERTAD TOTAL EN 3D", 240, 61 + dy_q, "press", 8, CYAN, align="center")
    elif t >= t_niv - 0.1:
        _, dy_m = pop(t, t_niv - 0.1)
        window(cv, 108, 54 + dy_m, 264, 38, fill=(16, 22, 48), border=GOLD)
        draw_text(cv, "NIVEL LINEAL: NO", 240, 60 + dy_m, "silk", 8, GREY, align="center")
        draw_text(cv, "MUNDO ABIERTO VIVO", 240, 74 + dy_m, "press", 8, GOLD, align="center",
                  reveal=(t - (t_niv - 0.05)) * 28)

    return vignette(cv, 0.34)


def sc_c6_05(t):
    """c6_05: Recuerda ese nombre. Va a volver."""
    city = bg("bg_open_city_2001").copy()
    CITY_RAIN.draw(city, t, alpha=120)

    t0 = TL.s("c6_05")
    t_nom = WD("c6_05", "nombre")
    t_vol = WD("c6_05", "volver")

    # La ciudad nocturna se oscurece gradualmente a negro puro con fade_to
    dark_k = ease_in_out(prog(t, t0 - 0.15, t_nom + 0.35))
    cv = fade_to(city, (0, 0, 0), dark_k)
    d = ImageDraw.Draw(cv)

    pulse = 0.6 + 0.4 * math.sin(t * 5.0)
    border_c = GOLD if int(t * 4) % 2 == 0 else CYAN

    d.rectangle([38, 76, 442, 194], outline=(*GOLD, int(110 * pulse)), width=2)
    window(cv, 42, 80, 396, 110, fill=(12, 14, 28), border=border_c, alpha=0.96)

    draw_text(cv, "GRAND THEFT AUTO", 240, 98, "press", 16,
              gradient=GOLD_RAMP, align="center", outline_w=2)

    ln_w = int(150 * ease_out(prog(t, t0, t_nom + 0.2)))
    d.line([(240 - ln_w, 126), (240 + ln_w, 126)], fill=(*CYAN, 255), width=2)

    draw_text(cv, "RECUERDA ESE NOMBRE.", 240, 138, "press", 8, CREAM, align="center",
              reveal=(t - (t0 - 0.05)) * 26)

    if t >= t_vol - 0.25:
        _, dy_v = pop(t, t_vol - 0.25)
        draw_text(cv, "VA A VOLVER.", 240, 158 + dy_v, "press", 16,
                  gradient=CYAN_RAMP, align="center")

    draw_phosphor_dot(cv, 240, 218, r=3, color=GREEN_LED)

    return cv


# =========================================================================== montaje

def scenes():
    c6s = TL.chapter_start(6)
    return [
        (c6s - 0.3, make_card(6, ["LA CIUDAD ABIERTA"], "2000 – 2005"), None),
        (TL.s("c6_01") - 0.2, sc_c6_01,
         lambda t: (cam_push(t, TL.s("c6_01"), TL.e("c6_01"), 1.0, 1.05, (240, 135), (240, 135))[0]
                    + cam_punch(t, [WD("c6_01", "PlayStation"), WD("c6_01", "leia")], 0.05),
                    240, 135)),
        (TL.s("c6_02") - 0.2, sc_c6_02,
         lambda t: (1.0 + cam_punch(t, [WD("c6_02", "millones"), WD("c6_02", "vendida")], 0.07), 240, 135)),
        (TL.s("c6_03") - 0.2, sc_c6_03,
         lambda t: (1.0 + cam_punch(t, [WD("c6_03", "Edimburgo"), WD("c6_03", "reglas"), WD("c6_03", "Grand")], 0.06),
                    240, 135)),
        (TL.s("c6_04") - 0.2, sc_c6_04,
         lambda t: cam_push(t, TL.s("c6_04") - 0.2, TL.e("c6_04"), 1.08, 1.08, (228, 135), (252, 135))),
        (TL.s("c6_05") - 0.15, sc_c6_05,
         lambda t: (1.0 + cam_punch(t, [WD("c6_05", "volver")], 0.07), 240, 135)),
    ]


# =========================================================================== audio

def music(A):
    c6s = TL.chapter_start(6) + 1.6
    t_rec = TL.s("c6_02")
    t_gta = TL.s("c6_03")
    t_open = TL.s("c6_04")
    t_rem = TL.s("c6_05")
    c6e = chapter_end(6)

    A.section(c6s, t_rec, 118, [("E", "min"), ("C", "maj"), ("G", "maj"), ("D", "maj")], A.st_build)
    A.section(t_rec, t_gta, 124, [("E", "min"), ("C", "maj"), ("G", "maj"), ("D", "maj")], A.st_triumph)
    A.section(t_gta, t_open, 116, [("A", "min"), ("F", "maj"), ("D", "min"), ("E", "maj")], A.st_puzzle)
    A.section(t_open, t_rem, 122, [("A", "min"), ("G", "maj"), ("F", "maj"), ("E", "maj")], A.st_bright)
    A.section(t_rem, c6e, 96, [("A", "min"), ("F", "maj")], A.st_mystery)


def sfx(A):
    A.whoosh(TL.s("c6_01") - 0.1, 0.35, 0.05)
    A.pop_sfx(WD("c6_01", "PlayStation"), 560)
    A.blip(WD("c6_01", "juegos"), 1300)
    A.coin(WD("c6_01", "leia"))

    A.text_blips(TL.s("c6_02") + 0.1, 18, 16, f=1450)
    A.join_jingle(WD("c6_02", "millones"))
    A.pop_sfx(WD("c6_02", "vendida"), 720)

    A.blip(WD("c6_03", "Edimburgo"), 980)
    A.blip(WD("c6_03", "juego"), 1180)
    A.whoosh(WD("c6_03", "reglas"), 0.35, 0.06)
    A.sting(WD("c6_03", "Grand"), [57, 64, 69, 76], vol=0.055, step=0.11, hold=0.9)

    A.rain_amb(TL.s("c6_04") - 0.1, TL.e("c6_04"), vol=0.025)
    A.pop_sfx(WD("c6_04", "quisieras"), 620)
    A.join_jingle(WD("c6_04", "mundo"))

    A.whoosh(TL.s("c6_05") - 0.1, 0.4, 0.05)
    A.sting(WD("c6_05", "volver") - 0.05, [69, 64, 57], vol=0.06, step=0.16, hold=1.3)
