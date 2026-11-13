"""Helpers compartidos por todas las escenas (personajes, UI, efectos, camara)."""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import sprites as S
from timeline import TL

FEET_OFFSET = 50  # fila de los pies dentro del sprite

# =========================================================================== helpers

def talk_v(t, on=True):
    return [0, 1, 2, 1][int(t * 11) % 4] if on else 0


def upscale(arr, k):
    k = int(k)
    if k <= 1:
        return arr
    return np.repeat(np.repeat(arr, k, axis=0), k, axis=1)


def char(cv, key, x, feet, t, alpha=1.0, shadow=True, scale=1, **pose):
    """Dibuja un personaje con los pies en (x, feet). scale = 1, 2 o 3 (píxeles enteros)."""
    spec = S.CAST[key] if isinstance(key, str) else key  # clave del reparto o dict propio
    arr = upscale(S.render(spec, t, **pose), scale)
    if shadow and alpha > 0.3:
        shadow_ellipse(cv, int(x), int(feet), 18 * scale, 4 * scale, 80)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale, alpha)


def floor_prop(cv, fn_draw, x, feet=250):
    """Dibuja un objeto apoyado sobre el piso (mesas con velas, mascotas, maletas, podios)
    en (x, feet) en 16:9 y sobre el suelo vertical (vfeet=452) en 9:16 para que jamás flote."""
    vctx = getattr(sys.modules.get("core"), "_VCTX", None)
    if vctx is not None and isinstance(cv, Image.Image) and cv.size == (W, H):
        vctx.chars.append({
            "kind": "prop",
            "fn": fn_draw,
            "x": x,
            "feet": feet,
            "scale": 1,
        })
        return
    fn_draw(cv, int(x), int(feet))


def pace(t, t0, x_a, x_b, period=3.6, pause=0.28):
    """Hace que un personaje camine con ritmo entre x_a y x_b, deteniéndose brevemente en cada extremo.
    Devuelve (x, walk_phase, look_dir)."""
    if t <= t0:
        return x_a, None, (1 if x_b >= x_a else -1)
    dt = t - t0
    leg = (dt / period) % 2.0
    going_b = leg < 1.0
    u_raw = leg if going_b else (leg - 1.0)
    move_frac = max(0.2, 1.0 - pause)
    if u_raw < move_frac:
        p = ease_in_out(u_raw / move_frac)
        x = (x_a + (x_b - x_a) * p) if going_b else (x_b + (x_a - x_b) * p)
        wph = (t * 3.4) % 1.0
        look = (1 if x_b >= x_a else -1) if going_b else (-1 if x_b >= x_a else 1)
        return x, wph, look
    else:
        x = x_b if going_b else x_a
        # Al detenerse en el extremo, mira hacia el centro de la escena (x=240)
        look = 1 if x < 240 else -1
        return x, None, look


def silhouette(cv, key, x, feet, t, color=(12, 10, 22), scale=1, **pose):
    spec = S.CAST[key] if isinstance(key, str) else key
    arr = S.render(spec, t, **pose).copy()
    m = arr[..., 3] > 0
    arr[m, :3] = color
    arr = upscale(arr, scale)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale)


def robot(cv, x, feet, t, face="happy", frozen=False, alpha=1.0, sil=False, scale=1):
    """Desactivado en Dune: el robot retro pertenece únicamente al documental de IA."""
    return


# --------------------------------------------------------------------------- cámara
# Cada escena puede definir una cámara: (zoom, cx, cy) en coordenadas del lienzo 480x270.
# El zoom se aplica al escalar a 1080p, por eso es suave y no rompe el pixel art.

def cam_push(t, t0, t1, z0=1.0, z1=1.12, c0=(240, 135), c1=None):
    """Acercamiento lento (Ken Burns) entre t0 y t1."""
    p = ease_in_out(prog(t, t0, t1))
    c1 = c1 or c0
    return (z0 + (z1 - z0) * p, c0[0] + (c1[0] - c0[0]) * p, c0[1] + (c1[1] - c0[1]) * p)


def cam_punch(t, beats, amp=0.06, dur=0.35):
    """Pequeño golpe de zoom en cada instante de `beats` (para dar ritmo). Devuelve zoom extra."""
    z = 0.0
    for b in beats:
        if b <= t < b + dur:
            z = max(z, amp * (1 - (t - b) / dur) ** 2)
    return z


def apply_cam(img, cam):
    """Devuelve el fotograma final 1920x1080 aplicando la cámara (zoom, cx, cy) sin cortar los carteles superiores."""
    if not cam or abs(cam[0] - 1.0) < 1e-3:
        return img.resize((1920, 1080), Image.NEAREST)
    z, cx, cy = cam
    z = min(1.035, max(1.0, z))
    w, h = W / z, H / z
    x0 = min(max(0, cx - w / 2), W - w)
    y0 = min(4.0, max(0, cy - h / 2), H - h)
    return img.resize((1920, 1080), Image.NEAREST, box=(x0, y0, x0 + w, y0 + h))


def walk(t, t0, t1, x0, x1):
    p = prog(t, t0, t1)
    x = x0 + (x1 - x0) * ease_in_out(p)
    return x, ((t * 3.2) % 1.0 if 0 < p < 1 else None)


def pop(t, t0, dur=0.35):
    """Devuelve (alpha, dy) para una aparición con rebote."""
    p = prog(t, t0, t0 + dur)
    if p <= 0:
        return 0.0, 0
    return min(1.0, p * 2), int(round((1 - ease_out_back(p)) * -10))


def bigyear(cv, text, cx, y, t, t0, size=48, ramp=GOLD_RAMP):
    p = prog(t, t0, t0 + 0.55)
    if p <= 0:
        return
    yy = y - (1 - ease_out_back(p, 2.2)) * 50
    draw_text(cv, text, cx, int(yy), "press", size, align="center", gradient=ramp, outline_w=2,
              alpha=min(1, p * 3))
    if p >= 1:
        tw, _ = text_size(text, "press", size)
        for i, ph in enumerate((0.0, 1.7, 3.1)):
            sx = cx - tw // 2 + int((i + 0.5) * tw / 3)
            sparkle(cv, sx + (i * 7) % 11, y + 4 + (i * 13) % size, t + ph, 3)


def lower_third(cv, title, sub, t, t0, t1, x=16, y=222):
    a = prog(t, t0, t0 + 0.4) * (1 - prog(t, t1 - 0.4, t1))
    if a <= 0:
        return
    p_in = ease_out(prog(t, t0, t0 + 0.45))
    dy = int(round((1 - p_in) * 10))
    x = max(24, x)
    y = min(214, y)
    tw, _ = text_size(title, "press", 16)
    sw, _ = text_size(sub, "silk", 8)
    ww = max(tw, sw) + 22
    if x - 8 + ww > W - 16:
        x = max(16, W - 16 - ww + 8)
    window(cv, x - 8, y - 8 + dy, ww, 48, alpha=0.88 * a)
    ImageDraw.Draw(cv).rectangle([x, y - 2 + dy, x + int(24 * ease_out(prog(t, t0, t0 + 0.6))), y - 1 + dy],
                                 fill=(*GOLD, int(255 * a)))
    draw_text(cv, title, x, y + 4 + dy, "press", 16, CREAM, alpha=a)
    draw_text(cv, sub, x + 1, y + 24 + dy, "silk", 8, GREY, alpha=a)


def draw_sun(cv, cx, cy, r, t, face=True, alpha=255):
    d = ImageDraw.Draw(cv)
    for i in range(12):
        ang = i * math.pi / 6 + t * 0.4
        l0, l1 = r + 3, r + 6 + (2 if i % 2 else 0)
        x0, y0 = cx + math.cos(ang) * l0, cy + math.sin(ang) * l0
        x1, y1 = cx + math.cos(ang) * l1, cy + math.sin(ang) * l1
        d.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=(255, 214, 90, alpha), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 226, 110, alpha), outline=(214, 140, 40, alpha))
    d.ellipse([cx - r + 3, cy - r + 3, cx - r // 3, cy - r // 3], fill=(255, 246, 190, alpha))
    if face:
        d.rectangle([cx - 5, cy - 3, cx - 4, cy - 1], fill=(120, 60, 20, alpha))
        d.rectangle([cx + 4, cy - 3, cx + 5, cy - 1], fill=(120, 60, 20, alpha))
        d.line([(cx - 4, cy + 4), (cx - 2, cy + 6), (cx + 2, cy + 6), (cx + 4, cy + 4)], fill=(120, 60, 20, alpha))


def draw_moon(cv, cx, cy, r=9, alpha=255):
    d = ImageDraw.Draw(cv)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 240, 255, alpha))
    d.ellipse([cx - r + 5, cy - r - 2, cx + r + 5, cy + r - 2], fill=(0, 0, 0, 0))


def draw_paper(cv, x, y, w, h, color=(246, 240, 222)):
    d = ImageDraw.Draw(cv)
    d.rectangle([x + 3, y + 3, x + w + 3, y + h + 3], fill=(0, 0, 0, 110))
    d.rectangle([x, y, x + w, y + h], fill=(*color, 255), outline=(*INK, 255))
    d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=(*shade(color, 0.85), 255))
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=(*shade(color, 0.85), 255))


def scribble(cv, x, y, w, p, seed, color=(30, 40, 110)):
    """Firma manuscrita que se dibuja progresivamente (p 0..1)."""
    d = ImageDraw.Draw(cv)
    n = int(w * p)
    prev = None
    for i in range(n):
        yy = y + math.sin(i * 0.9 + seed) * 2.5 + math.sin(i * 0.37 + seed * 2) * 1.5
        pt = (x + i, int(yy))
        if prev:
            d.line([prev, pt], fill=(*color, 255))
        prev = pt


def bulb(cv, cx, cy, t, on=1.0, cord_top=None):
    d = ImageDraw.Draw(cv)
    if cord_top is not None and cy - 9 > cord_top:
        d.line([(cx, int(cord_top)), (cx, cy - 9)], fill=(*INK, 255), width=2)
        d.rectangle([cx - 3, cy - 10, cx + 3, cy - 6], fill=(140, 140, 152, 255), outline=(*INK, 255))
    if on > 0:
        glow(cv, cx, cy, 14, (255, 240, 140), 0.45 * on)
    d.ellipse([cx - 6, cy - 7, cx + 6, cy + 5], fill=(255, 240, 150, 255) if on > 0.5 else (200, 200, 190, 255),
              outline=(*INK, 255))
    d.rectangle([cx - 3, cy + 5, cx + 3, cy + 9], fill=(160, 160, 170, 255), outline=(*INK, 255))
    d.point((cx - 3, cy - 4), fill=(255, 255, 255, 255))


def spotlight(cv, cx, top, bottom, w_top, w_bot, color=(120, 220, 255), strength=0.22):
    a = np.array(cv)
    th = bayer_tile(W, H)
    for y in range(max(0, top), min(H, bottom)):
        k = (y - top) / max(1, bottom - top)
        half = (w_top + (w_bot - w_top) * k) / 2
        x0, x1 = int(max(0, cx - half)), int(min(W, cx + half))
        if x1 <= x0:
            continue
        m = th[y, x0:x1] < strength * (1 - 0.3 * k)
        row = a[y, x0:x1, :3].astype(np.int32)
        row[m] = (row[m] * 0.4 + np.array(color) * 0.6).astype(np.int32)
        a[y, x0:x1, :3] = row
    return Image.fromarray(a, "RGBA")


def orb(cv, cx, cy, t, on):
    if on <= 0:
        return
    d = ImageDraw.Draw(cv)
    r = 3 + int(on * 1)
    pulse = 0.5 + 0.5 * math.sin(t * 4 + cx)
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(90, 220, 255, int(60 * on * pulse)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 230, 255, 255), outline=(30, 110, 160, 255))
    d.point((cx - 1, cy - 1), fill=(240, 255, 255, 255))


def terminal(cv, x, y, t, on=True):
    """Terminal CRT de 30x24."""
    d = ImageDraw.Draw(cv)
    d.rectangle([x, y, x + 30, y + 22], fill=(214, 204, 178, 255), outline=(*INK, 255))
    d.rectangle([x + 3, y + 3, x + 27, y + 17], fill=(14, 40, 26, 255))
    if on:
        for i in range(3):
            ll = 6 + ((i * 7 + int(t * 3)) % 14)
            d.line([(x + 5, y + 6 + i * 4), (x + 5 + ll, y + 6 + i * 4)], fill=(100, 250, 150, 255))
        if int(t * 3) % 2:
            d.rectangle([x + 5, y + 14, x + 7, y + 15], fill=(100, 250, 150, 255))
    d.rectangle([x + 10, y + 23, x + 20, y + 26], fill=(150, 140, 120, 255), outline=(*INK, 255))


def desk(cv, x0, x1, top, bottom, color=(110, 72, 44)):
    d = ImageDraw.Draw(cv)
    d.rectangle([x0, top, x1, bottom], fill=(*color, 255), outline=(*INK, 255))
    d.line([(x0 + 1, top + 1), (x1 - 1, top + 1)], fill=(*shade(color, 1.35), 255))
    d.line([(x0 + 1, top + 4), (x1 - 1, top + 4)], fill=(*shade(color, 0.7), 255))
    for xx in range(x0 + 12, x1 - 6, 24):
        d.rectangle([xx, top + 8, xx + 10, top + 12], fill=(*shade(color, 0.8), 255), outline=(*shade(color, 0.5), 255))


def quest_window(cv, lines, x, y, t, t0, w=210):
    a = prog(t, t0, t0 + 0.3)
    if a <= 0:
        return
    if lines:
        max_tw = max(text_size(txt, "press", 8)[0] for txt, _ in lines)
        w = max(w, max_tw + 18)
        x = min(x, W - w - 6)
    h = 14 + 12 * len(lines)
    window(cv, x, y, w, h)
    for i, (txt, col) in enumerate(lines):
        draw_text(cv, txt, x + 8, y + 8 + i * 12, "press", 8, col)


def shake(t, t0, dur=0.25, amp=3):
    if t0 <= t < t0 + dur:
        k = 1 - (t - t0) / dur
        return int(round(math.sin(t * 90) * amp * k)), int(round(math.cos(t * 77) * amp * k))
    return 0, 0


def offset_canvas(cv, dx, dy, fill=(0, 0, 0)):
    if dx == 0 and dy == 0:
        return cv
    out = Image.new("RGBA", cv.size, (*fill, 255))
    out.paste(cv, (dx, dy))
    return out


def sky_cycle(phase):
    """phase 0..1 -> nivel de noche 0..1 (0 = mediodía)."""
    return 0.5 - 0.5 * math.cos(phase * 2 * math.pi)


def bars70(cv, lit, t, y=252, x0=30, alpha=1.0, cur_glow=True):
    d = ImageDraw.Draw(cv)
    d.rectangle([x0 - 6, y - 5, x0 + 70 * 6 + 2, y + 15], fill=(10, 10, 20, int(190 * alpha)))
    for i in range(70):
        x = x0 + i * 6
        if i < lit:
            c = (255, 250, 220) if (i == int(lit) - 1 and cur_glow) else GOLD
            hgt = 10
        else:
            c = (60, 56, 70)
            hgt = 6
        d.rectangle([x, y + 10 - hgt, x + 3, y + 10], fill=(*c, 255))


def chapter_card(cv, t, t0, num, lines, years, ramp_title=CREAM_RAMP):
    open_p = ease_out(prog(t, t0, t0 + 0.35))
    if open_p <= 0:
        return
    # tamaño adaptable para evitar que el texto desborde la caja
    w24 = max(text_size(l, "press", 24)[0] for l in lines) if lines else 0
    size = 24 if (len(lines) == 1 and w24 <= 320) else 16
    max_w = max(text_size(l, "press", size)[0] for l in lines) if lines else 200
    card_w = min(440, max(360, max_w + 48))
    w = int(card_w * open_p)
    h = 124
    window(cv, 240 - w // 2, 68, max(8, w), h)
    if open_p < 1:
        return
    tt = t - t0 - 0.35
    d = ImageDraw.Draw(cv)
    lab = f"CAPÍTULO {num}"
    lw, _ = text_size(lab, "press", 8)
    draw_text(cv, lab, 240, 84, "press", 8, GOLD, align="center", reveal=tt * 30)
    ln = int(min(1, tt * 2) * 50)
    d.line([(240 - lw // 2 - 8 - ln, 87), (240 - lw // 2 - 8, 87)], fill=(*GOLD, 255))
    d.line([(240 + lw // 2 + 8, 87), (240 + lw // 2 + 8 + ln, 87)], fill=(*GOLD, 255))
    for i, line in enumerate(lines):
        yy = 112 if len(lines) == 1 else 104 + i * 22
        draw_text(cv, line, 240, yy, "press", size, align="center", gradient=ramp_title,
                  reveal=(tt - 0.25 - i * 0.4) * 26)
    draw_text(cv, years, 240, 172, "press", 8, CYAN, align="center", reveal=(tt - 0.45) * 45)


STARS = Stars(140, seed=11, region=(0, 0, W, 210))
RAIN = Rain(110, seed=4, region=(192, 8, 428, 142), color=(196, 210, 226), speed=210)
SNOW = Snow(260, seed=8)
CONF = Confetti(110, seed=6)
FOUR = ["mccarthy", "minsky", "shannon", "rochester"]


def scaled(cv, fn, w, h, x, y, k=2):
    """Dibuja con fn(img) en un lienzo chico (w x h) y lo pega ampliado x k (pixel art)."""
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fn(tmp)
    a = upscale(np.array(tmp), k)
    paste_arr(cv, a, x, y)


# --------------------------------------------------------------------------- placas de capítulo

CARD_YEARS = {}


def draw_sand_ripple(cv, t, y_base=248, x_start=10, x_end=470, progress=None,
                     color=(238, 194, 110), highlight=(255, 232, 168), shadow=(138, 96, 42)):
    """Brisa de arena suave al ras del suelo (sin forma de gusano), usada solo en desierto."""
    d = ImageDraw.Draw(cv)
    span = max(1, x_end - x_start)
    for i in range(18):
        speed = 54 + (i % 4) * 18
        gx = x_start + int((i * 37 + t * speed) % span)
        gy = y_base - 6 + int(round(math.sin(t * 3.5 + i * 0.9) * 4))
        col_g = highlight if i % 3 == 0 else color
        d.line([(gx, gy), (min(x_end, gx + 5 + (i % 3) * 2), gy)], fill=(*col_g, 165), width=1)


def draw_sand_wind(cv, t, density=42, color=(238, 202, 132), y_min=20, y_max=265):
    """Granos de arena llevados por el viento de izquierda a derecha."""
    d = ImageDraw.Draw(cv)
    for i in range(density):
        speed = 46 + (i % 5) * 16
        x = int((i * 47 + t * speed) % W)
        y = y_min + int((i * 29 + math.sin(t * 2.5 + i) * 5) % max(1, (y_max - y_min)))
        a = 115 + (i % 4) * 32
        d.rectangle([x, y, x + (1 if i % 3 else 2), y], fill=(*color, a))


def draw_phosphor_dot(cv, x, y, r=3, trail=None, color=(245, 200, 110)):
    """Punto luminoso cálido (ámbar/arena) para indicadores y destellos."""
    d = ImageDraw.Draw(cv)
    if trail:
        for i, (tx, ty) in enumerate(trail):
            tr = max(1, r - 1)
            d.rectangle([int(tx) - tr, int(ty) - tr, int(tx) + tr, int(ty) + tr], fill=(*color, 255))
    glow(cv, int(x), int(y), r + 6, color, 0.45)
    d.rectangle([int(x) - r, int(y) - r, int(x) + r, int(y) + r], fill=(255, 245, 215, 255))


def make_card(num, lines, years, snow=False, robot_face="question"):
    """Escena de placa de capítulo clásica de Pixeloide (estilo RPG a pantalla completa)
    con el motivo de «Un caballo en el aire»: cinta de celuloide perforada de 35 mm y caballo al galope."""
    def sc(t):
        cv = vgradient((10, 12, 26), (26, 22, 48), 10) if not snow else vgradient((8, 12, 24), (24, 34, 58), 10)
        STARS.draw(cv, t, alpha=0.70)
        if snow:
            SNOW.draw(cv, t, density=0.6)
        # Cinta de película perforada de 35mm corriendo arriba y abajo
        draw_filmstrip(cv, 0, 12, W, 38, t, speed=46.0, sepia=True, alpha=0.85)
        draw_filmstrip(cv, 0, 222, W, 38, t, speed=-46.0, sepia=True, alpha=0.85)
        # Siluetas doradas de Sallie Gardner galopando a 12 cuadros por segundo en los flancos
        draw_galloping_horse(cv, 54, 134, t * 0.9, scale=1, silhouette_col=GOLD, rider=True)
        draw_galloping_horse(cv, 426, 134, t * 0.9 + 0.25, scale=1, silhouette_col=GOLD, rider=True)
        t0 = TL.chapter_start(num) - 0.15
        chapter_card(cv, t, t0, num, lines, years, ramp_title=GOLD_RAMP)
        return vignette(cv, 0.32)
    return sc


def chapter_end(num):
    """Inicio del capítulo siguiente (o fin del video)."""
    max_ch = max(TL.chapters) if hasattr(TL, "chapters") and TL.chapters else 7
    return TL.chapter_start(num + 1) if num < max_ch else TL.total



# ===========================================================================
# MOTIVOS VISUALES DE «EL DIBUJO QUE ENCENDIÓ EL MUNDO» (NIKOLA TESLA)
# ===========================================================================

AMBER = (255, 196, 92)
AMBER_DIM = (186, 124, 48)
TESLA_VIOLET = (188, 126, 255)
TESLA_CYAN = (108, 236, 255)
TESLA_SPARK = (210, 248, 255)
SOFT_GRAY = (176, 186, 206)
CHALK_WHITE = (242, 244, 236)
CHALK_YELLOW = (252, 224, 126)
CHALK_CYAN = (138, 234, 245)
CHALK_GREEN = (128, 238, 158)
CHALK_RED = (248, 112, 98)
BOARD_GREEN = (20, 48, 34)
BOARD_DARK = (12, 32, 22)
WOOD_FRAME = (112, 72, 38)


def glow(cv, cx, cy, r, color=GOLD, alpha=0.5):
    """Dibuja un resplandor suave concéntrico mezclando RGB con alpha real sobre cv."""
    if r <= 0 or alpha <= 0:
        return
    ov = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for k, frac in ((1.0, 0.16), (0.68, 0.30), (0.38, 0.48)):
        rk = max(1, int(round(r * k)))
        ak = int(255 * clamp01(alpha * frac))
        d.ellipse([int(cx) - rk, int(cy) - rk, int(cx) + rk, int(cy) + rk], fill=(*color[:3], ak))
    comp = Image.alpha_composite(cv.convert("RGBA"), ov)
    cv.paste(comp, (0, 0))


def tint(cv, color=(10, 14, 24), strength=0.5):
    """Tiñe el lienzo cv hacia color con intensidad strength (0..1)."""
    return fade_to(cv, color, clamp01(strength))


def draw_rotating_arrows(cv, cx, cy, r, t, speed=2.2, color=GOLD, glow=None,
                         progress=1.0, sand_groove=False, alpha=1.0, pulse=None):
    """Dibuja el motivo central del documental: el círculo con cuatro flechas curvas
    (el campo magnético giratorio dibujado en la arena de Budapest)."""
    if progress <= 0 or alpha <= 0:
        return
    if pulse is not None and glow is None:
        glow = color
    d = ImageDraw.Draw(cv)
    ang_base = t * speed
    a_int = int(255 * clamp01(alpha))

    if sand_groove:
        d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
                  fill=(82, 56, 30, int(130 * alpha)), outline=(58, 38, 18, int(190 * alpha)))

    if glow is not None:
        d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4],
                  outline=(*glow, int(95 * alpha)), width=3)

    n_arrows = 4
    total_arcs = clamp01(progress) * n_arrows
    for k in range(n_arrows):
        arc_p = clamp01(total_arcs - k)
        if arc_p <= 0:
            continue
        a0 = ang_base + k * (math.pi / 2.0) + 0.16
        a1 = a0 + (math.pi / 2.0 - 0.34) * arc_p
        steps = max(4, int(14 * arc_p))
        pts = []
        for s_i in range(steps + 1):
            aa = a0 + (a1 - a0) * (s_i / float(steps))
            px = int(round(cx + math.cos(aa) * r))
            py = int(round(cy + math.sin(aa) * r))
            pts.append((px, py))
        if len(pts) >= 2:
            # Sombra / surco
            pts_sh = [(px + 1, py + 1) for (px, py) in pts]
            d.line(pts_sh, fill=(*INK, a_int), width=3)
            d.line(pts, fill=(*color, a_int), width=2)
            # Punta de flecha tangencial en el extremo a1
            if arc_p > 0.65:
                tx, ty = pts[-1]
                # Vector tangente en sentido horario (donde aumenta el ángulo)
                tang_x = -math.sin(a1)
                tang_y = math.cos(a1)
                norm_x = -math.cos(a1)
                norm_y = -math.sin(a1)
                head_len = max(4, int(r * 0.24))
                wing = max(3, int(r * 0.16))
                p_tip = (int(round(tx + tang_x * 2)), int(round(ty + tang_y * 2)))
                p_l = (int(round(tx - tang_x * head_len + norm_x * wing)),
                       int(round(ty - tang_y * head_len + norm_y * wing)))
                p_r = (int(round(tx - tang_x * head_len - norm_x * wing)),
                       int(round(ty - tang_y * head_len - norm_y * wing)))
                d.polygon([p_tip, p_l, p_r], fill=(*color, a_int), outline=(*INK, a_int))


def draw_chapter_header(cv, t, t0, ch_num, title_es, place_es=None, border=GOLD):
    """Encabezado superior de capítulo y lugar tipeado con cursor ('Lugares tipeados con cursor')."""
    dt = t - t0
    if dt < -0.35:
        return
    # Ventana superior de capítulo + lugar (compatible 100% con vertical.py y 16:9)
    full_title = f"{ch_num} · {title_es}"
    window(cv, 14, 8, 452, 34 if place_es else 24, fill=(16, 18, 34), border=border, alpha=0.94)
    draw_text(cv, full_title, 240, 12, "press", 8, border, align="center",
              reveal=max(1, int((dt + 0.15) * 38)))
    if place_es:
        rev_p = max(0, int((dt - 0.15) * 28))
        draw_text(cv, place_es, 240, 26, "silk", 8, CREAM, align="center", reveal=rev_p)


def draw_place_only(cv, place_es, t, t0, border=AMBER):
    """Muestra un rótulo de lugar tipeado con cursor en el encabezado superior."""
    if t < t0 - 0.1:
        return
    dt = max(0.0, t - t0)
    window(cv, 20, 8, 440, 22, fill=(16, 18, 34), border=border, alpha=0.92)
    draw_text(cv, place_es, 240, 14, "press", 8, CREAM, align="center", reveal=max(1, int(dt * 26)))


def draw_pizarra_frame(arg1, arg2, arg3=None, arg4=None, summary_es=None, t_summary=None):
    """Crea o dibuja en el lienzo el marco de 'LA PIZARRA': pizarra verde con marco de madera,
    encabezado 'LA PIZARRA · TEMA' y placa final opcional 'EN UNA FRASE'.
    Soporta tanto draw_pizarra_frame(t, t0, topic_es, ...) como draw_pizarra_frame(cv, full_title, t, t0)."""
    is_vert = getattr(sys.modules.get("core"), "_VCTX", None) is not None
    if isinstance(arg1, Image.Image):
        target_cv = arg1
        full_hdr = str(arg2)
        t = float(arg3) if arg3 is not None else 0.0
        t0 = float(arg4) if arg4 is not None else 0.0
        base_cv = vgradient(BOARD_GREEN, BOARD_DARK, 8)
        target_cv.paste(base_cv, (0, 0))
        cv = target_cv
    else:
        t = float(arg1)
        t0 = float(arg2)
        topic_es = str(arg3)
        full_hdr = topic_es if topic_es.startswith("LA PIZARRA") else f"LA PIZARRA · {topic_es}"
        cv = vgradient(BOARD_GREEN, BOARD_DARK, 8)

    if not is_vert:
        d = ImageDraw.Draw(cv)
        # Textura de polvo de tiza sutil y cuadrícula tenue (solo en 16:9; en 9:16 el fondo se genera limpio)
        for gx in range(24, W - 24, 24):
            d.line([(gx, 36), (gx, H - 22)], fill=(28, 62, 44, 90))
        for gy in range(44, H - 22, 24):
            d.line([(24, gy), (W - 24, gy)], fill=(28, 62, 44, 90))
        # Marco de madera alrededor
        d.rectangle([0, 0, W - 1, H - 1], outline=(*WOOD_FRAME, 255), width=4)
        d.rectangle([4, 4, W - 5, H - 5], outline=(*shade(WOOD_FRAME, 0.7), 255), width=2)
        # Bandeja inferior con tizas blancas y amarillas
        d.rectangle([16, H - 12, W - 16, H - 5], fill=(*WOOD_FRAME, 255), outline=(*INK, 255))
        d.rectangle([68, H - 14, 82, H - 12], fill=(*CHALK_WHITE, 255))
        d.rectangle([112, H - 14, 124, H - 12], fill=(*CHALK_YELLOW, 255))

    # Encabezado de La Pizarra
    window(cv, 24, 8, 432, 24, fill=(14, 36, 26), border=CHALK_YELLOW, alpha=0.96, inner=(42, 86, 62))
    draw_text(cv, full_hdr, 240, 15, "press", 8, CHALK_YELLOW, align="center",
              reveal=max(1, int((t - t0 + 0.2) * 36)))

    # Si llegó el momento de 'EN UNA FRASE', dibujar la placa resumen abajo (dentro de x=116..364)
    if summary_es and t_summary is not None and t >= t_summary - 0.1:
        a, dy = pop(t, t_summary - 0.1)
        window(cv, 116, 206 + dy, 248, 44, fill=(16, 40, 28), border=CHALK_WHITE, alpha=0.96, inner=CHALK_YELLOW)
        draw_text(cv, "EN UNA FRASE:", 240, 213 + dy, "silk", 8, CHALK_CYAN, align="center")
        draw_text(cv, summary_es, 240, 229 + dy, "silk", 8, CHALK_YELLOW, align="center",
                  reveal=max(1, int((t - t_summary + 0.15) * 32)))
    return cv


def draw_chalk_hand(cv, x, y, t):
    """Mano genérica en pixel art sosteniendo una tiza blanca que dibuja en la pizarra."""
    d = ImageDraw.Draw(cv)
    jx = int(round(math.sin(t * 14.0) * 2))
    jy = int(round(math.cos(t * 11.0) * 1.5))
    hx, hy = int(x) + jx, int(y) + jy
    # Tiza blanca
    d.rectangle([hx - 6, hy - 2, hx + 2, hy + 1], fill=(*CHALK_WHITE, 255), outline=(*INK, 255))
    # Dedos y dorso de la mano
    skin = (234, 184, 142, 255)
    skin_sh = (196, 144, 104, 255)
    d.rectangle([hx + 1, hy - 4, hx + 11, hy + 5], fill=skin, outline=(*INK, 255))
    d.rectangle([hx + 8, hy - 3, hx + 11, hy + 4], fill=skin_sh)
    # Puño de camisa y manga oscura
    d.rectangle([hx + 11, hy - 4, hx + 15, hy + 5], fill=(240, 238, 230, 255), outline=(*INK, 255))
    d.rectangle([hx + 15, hy - 5, hx + 26, hy + 6], fill=(32, 36, 52, 255), outline=(*INK, 255))


def draw_copper_egg(cv, cx, cy, t, spin_speed=0.0, upright=0.0, stand_p=None, scale=1):
    """Dibuja el huevo de cobre de Tesla sobre una mesa/pedestal.
    upright: 0.0 (acostado) -> 1.0 (parado sobre su punta bailando)."""
    if stand_p is not None:
        upright = stand_p
    d = ImageDraw.Draw(cv)
    rx = int(round((11 * (1 - upright) + 7 * upright) * scale))
    ry = int(round((7 * (1 - upright) + 12 * upright) * scale))
    wobble = int(round(math.sin(t * max(4.0, spin_speed)) * 2 * scale)) if spin_speed > 0 else 0
    ey = int(round(cy - ry))
    ex = int(round(cx + (wobble if upright < 0.85 else int(wobble * 0.4))))
    # Sombra en la mesa
    shadow_ellipse(cv, int(cx), int(cy) + 2, rx + 3, max(2, int(round(3 * scale))), 110)
    # Cuerpo de cobre en 3 tonos
    c_dark = (142, 68, 28, 255)
    c_mid = (212, 118, 54, 255)
    c_hi = (252, 198, 128, 255)
    d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=c_mid, outline=(*INK, 255))
    d.ellipse([ex - rx + 2, ey - ry + 2, ex + rx - 2, ey + ry - 2], fill=c_dark)
    d.ellipse([ex - rx + 2, ey - ry + 2, ex + int(rx * 0.5), ey + int(ry * 0.6)], fill=c_mid)
    # Brillo especular que gira con spin_speed
    hx_off = int(round(math.cos(t * max(1.0, spin_speed)) * (rx * 0.45))) if spin_speed > 0 else -rx // 3
    hs = max(1, int(round(2 * scale)))
    d.ellipse([ex + hx_off - hs, ey - ry // 2, ex + hx_off + hs, ey], fill=c_hi)
    if spin_speed > 6.0:
        # Líneas de velocidad alrededor del huevo
        for dy_s in (-ry // 2, 0, ry // 2):
            d.line([(ex - rx - 5, ey + dy_s), (ex - rx - 2, ey + dy_s)], fill=(*AMBER, 190))
            d.line([(ex + rx + 2, ey + dy_s), (ex + rx + 5, ey + dy_s)], fill=(*AMBER, 190))


def draw_tesla_sparks(cv, x0, y0, t, rays=5, max_len=75, color=TESLA_VIOLET, core_col=(238, 252, 255),
                      seed=0, radius=None, count=None):
    """Dibuja rayos y descargas de alta frecuencia en pixel art desde (x0, y0)."""
    if radius is not None:
        max_len = radius
    if count is not None:
        rays = count
    d = ImageDraw.Draw(cv)
    step_t = int(t * 14) + seed
    for r_i in range(rays):
        base_ang = -math.pi * 0.85 + (r_i / float(max(1, rays - 1))) * (math.pi * 0.70) if rays > 1 else -math.pi / 2
        ang = base_ang + math.sin(step_t * 1.7 + r_i * 2.3) * 0.28
        segs = 6
        px, py = float(x0), float(y0)
        pts = [(int(px), int(py))]
        seg_len = max_len / float(segs)
        for s_i in range(1, segs + 1):
            jit = math.sin(step_t * 3.1 + r_i * 5.7 + s_i * 1.9) * 0.55
            px += math.cos(ang + jit) * seg_len
            py += math.sin(ang + jit) * seg_len
            pts.append((int(round(px)), int(round(py))))
        d.line(pts, fill=(*color, 215), width=3)
        d.line(pts, fill=(*core_col, 255), width=1)


def draw_pigeon(cv, x, y, t, white=False, flying=False, peck=False, flip=False, scale=1):
    """Dibuja una paloma en pixel art (gris urbana o la paloma blanca de Tesla)."""
    d = ImageDraw.Draw(cv)
    body_c = (244, 246, 252, 255) if white else (126, 136, 156, 255)
    wing_c = (216, 226, 242, 255) if white else (88, 96, 116, 255)
    neck_c = (188, 232, 245, 255) if white else (92, 168, 148, 255)
    dir_x = -1 if flip else 1

    if flying:
        flap = int(round(math.sin(t * 18.0 + x * 0.1) * 4))
        d.ellipse([x - 5 * scale, y - 2 * scale, x + 5 * scale, y + 2 * scale], fill=body_c, outline=(*INK, 255))
        d.polygon([(x - 2 * scale, y), (x - 6 * scale, y - (5 + flap) * scale), (x + 2 * scale, y - 1 * scale)],
                  fill=wing_c, outline=(*INK, 255))
        d.polygon([(x + 1 * scale, y), (x + 5 * scale, y - (4 - flap) * scale), (x + 4 * scale, y + 1 * scale)],
                  fill=wing_c, outline=(*INK, 255))
        hx = x + dir_x * 5 * scale
        d.ellipse([hx - 2 * scale, y - 3 * scale, hx + 2 * scale, y + 1 * scale], fill=body_c, outline=(*INK, 255))
        d.point((hx + dir_x * 3 * scale, y - 1 * scale), fill=(242, 174, 72, 255))
    else:
        head_dy = 3 * scale if (peck and int(t * 5 + x) % 3 == 0) else 0
        # Patitas
        d.line([(x - 1 * scale, y - 2 * scale), (x - 1 * scale, y)], fill=(218, 112, 74, 255))
        d.line([(x + 2 * scale, y - 2 * scale), (x + 2 * scale, y)], fill=(218, 112, 74, 255))
        # Cuerpo y ala
        d.ellipse([x - 5 * scale, y - 7 * scale, x + 4 * scale, y - 2 * scale], fill=body_c, outline=(*INK, 255))
        d.ellipse([x - 3 * scale, y - 6 * scale, x + 2 * scale, y - 3 * scale], fill=wing_c)
        # Cabeza y cuello tornasolado
        hx = x + dir_x * 4 * scale
        hy = y - 8 * scale + head_dy
        d.rectangle([hx - 1 * scale, hy + 1 * scale, hx + 1 * scale, hy + 3 * scale], fill=neck_c)
        d.ellipse([hx - 2 * scale, hy - 2 * scale, hx + 2 * scale, hy + 2 * scale], fill=body_c, outline=(*INK, 255))
        d.rectangle([hx + dir_x * 2 * scale, hy, hx + dir_x * 3 * scale, hy + 1 * scale], fill=(242, 174, 72, 255))


def draw_black_cat(cv, x, y, t, sparks=False):
    """Dibuja el gato negro del capítulo 1 con chispitas de estática en el lomo."""
    d = ImageDraw.Draw(cv)
    c_cat = (24, 22, 34, 255)
    c_hi = (52, 48, 72, 255)
    # Cuerpo arqueado
    d.ellipse([x - 14, y - 14, x + 12, y - 2], fill=c_cat, outline=(*INK, 255))
    d.arc([x - 12, y - 13, x + 10, y - 4], 200, 340, fill=c_hi, width=2)
    # Patas
    for lx in (x - 10, x - 6, x + 4, x + 8):
        d.rectangle([lx, y - 4, lx + 2, y], fill=c_cat)
    # Cabeza y orejas
    hx, hy = x + 12, y - 14
    d.ellipse([hx - 6, hy - 5, hx + 6, hy + 5], fill=c_cat, outline=(*INK, 255))
    d.polygon([(hx - 5, hy - 4), (hx - 3, hy - 9), (hx, hy - 4)], fill=c_cat)
    d.polygon([(hx + 1, hy - 4), (hx + 4, hy - 9), (hx + 6, hy - 4)], fill=c_cat)
    # Ojos amarillos brillantes
    d.point((hx + 1, hy - 1), fill=(255, 228, 84, 255))
    d.point((hx + 4, hy - 1), fill=(255, 228, 84, 255))
    # Cola ondulante
    tw = int(round(math.sin(t * 4.5) * 4))
    d.line([(x - 13, y - 9), (x - 19, y - 16), (x - 17 + tw, y - 24)], fill=c_cat, width=3)
    if sparks:
        for i in range(4):
            sx = x - 8 + ((i * 7 + int(t * 15)) % 18)
            sy = y - 16 - ((i * 5 + int(t * 19)) % 8)
            sparkle(cv, sx, sy, t * 4 + i, 2, TESLA_CYAN)


# ===========================================================================
# MOTIVOS VISUALES DE «UN CABALLO EN EL AIRE» (LA HISTORIA DEL CINE)
# ===========================================================================

# Las 12 fases del galope de Sallie Gardner (Muybridge, 1878).
# Cada tupla define ángulos/offsets de (delantera_izq, delantera_der, trasera_izq, trasera_der, dy_cuerpo).
# ¡En los cuadros 2 y 3 (índices 2 y 3, es decir fotos 3 y 4) las 4 patas están recogidas en el aire bajo la panza!
HORSE_12_FRAMES = [
    # 0: impulso trasero, delanteras recogiendo
    ((-4, 4, -8, 6), (-8, 5, -12, 7), (-6, 9, -2, 14), (-10, 8, -14, 14), 0),
    # 1: despegando del suelo
    ((-6, 4, -12, 5), (-9, 4, -14, 6), (-8, 6, -14, 9), (-11, 5, -16, 8), -2),
    # 2: ¡FOTO 3 — LAS 4 PATAS EN EL AIRE RECOGIDAS BAJO LA PANZA!
    ((6, 5, -2, 7), (4, 6, -4, 8), (-6, 5, 2, 7), (-4, 6, 4, 8), -5),
    # 3: ¡FOTO 4 — LAS 4 PATAS EN EL AIRE RECOGIDAS BAJO LA PANZA!
    ((8, 4, 0, 7), (5, 5, -3, 8), (-8, 4, 0, 7), (-5, 5, 3, 8), -5),
    # 4: preparando extensión delantera
    ((10, 4, 14, 8), (6, 5, 2, 9), (-8, 5, -12, 9), (-6, 6, -4, 9), -3),
    # 5: estirando mano delantera
    ((12, 5, 18, 11), (8, 5, 12, 10), (-10, 6, -16, 11), (-8, 6, -12, 10), -1),
    # 6: toque delantero derecho en tierra
    ((10, 6, 15, 14), (6, 6, 10, 13), (-10, 6, -16, 11), (-7, 6, -11, 11), 0),
    # 7: apoyo delantero completo
    ((4, 6, 6, 14), (8, 6, 11, 14), (-8, 6, -12, 12), (-4, 6, -6, 11), 1),
    # 8: cuerpo pasa sobre las manos
    ((-2, 6, -4, 14), (2, 6, 3, 14), (-4, 6, -2, 12), (0, 6, 3, 11), 1),
    # 9: despegue delantero, posteriores adelantan
    ((-8, 5, -12, 10), (-4, 6, -6, 13), (2, 6, 6, 13), (5, 6, 9, 14), 0),
    # 10: apoyo posterior
    ((-9, 5, -14, 8), (-6, 5, -10, 9), (4, 6, 6, 14), (0, 6, 1, 14), 0),
    # 11: empuje posterior fuerte
    ((-7, 4, -11, 7), (-10, 5, -14, 8), (0, 6, -2, 14), (-4, 6, -7, 14), -1),
]


def draw_galloping_horse(cv, x, y, phase=0.0, scale=1, frame=None, rider=True,
                         painting_spread=False, silhouette_col=None, highlight_air=False,
                         facing=1):
    """Dibuja a la yegua Sallie Gardner (con o sin jinete) en cualquiera de los 12 fotogramas
    de Muybridge (1878).
    - Si `painting_spread=True`: dibuja la pose falsa de los cuadros antiguos (las 4 patas estiradas
      hacia adelante y hacia atrás como caballito de calesita).
    - En `frame in (2, 3)` (o cuando `phase` cae ahí): las 4 patas están en el aire recogidas bajo la panza."""
    d = ImageDraw.Draw(cv)
    if frame is not None:
        f_idx = int(frame) % 12
    else:
        f_idx = int(float(phase) * 12) % 12

    if painting_spread:
        fl1, fl2 = (14, 3, 22, 6), (11, 4, 19, 8)
        bl1, bl2 = (-14, 3, -22, 6), (-11, 4, -19, 8)
        dy_b = -4
        in_air = True
    else:
        fl1, fl2, bl1, bl2, dy_b = HORSE_12_FRAMES[f_idx]
        in_air = f_idx in (2, 3)

    s = scale
    dir_x = 1 if facing >= 0 else -1
    cy = int(y + dy_b * s)
    cx = int(x)

    if silhouette_col is not None:
        c_body = (*silhouette_col[:3], 255)
        c_dark = (*shade(silhouette_col[:3], 0.75), 255)
        c_mane = (*shade(silhouette_col[:3], 0.6), 255)
        c_hoof = (*shade(silhouette_col[:3], 0.5), 255)
        c_outline = (*INK, 255)
    else:
        c_body = (168, 102, 54, 255)
        c_dark = (124, 72, 36, 255)
        c_mane = (48, 28, 18, 255)
        c_hoof = (32, 22, 16, 255)
        c_outline = (*INK, 255)

    # Sombra en el suelo (fija en y + 14*s para que se note el despegue cuando salta)
    ground_y = int(y + 14 * s)
    sh_w = int((22 if in_air else 28) * s)
    shadow_ellipse(cv, cx, ground_y, sh_w, max(2, int(3 * s)), 65 if in_air else 95)

    def _draw_leg(leg_tuple, col):
        kx, ky, hx, hy = leg_tuple
        p0 = (cx + dir_x * int(kx * 0.45 * s), cy + int(2 * s))
        p1 = (cx + dir_x * int(kx * s), cy + int(ky * s))
        p2 = (cx + dir_x * int(hx * s), cy + int(hy * s))
        d.line([p0, p1, p2], fill=c_outline, width=max(2, int(3 * s)))
        d.line([p0, p1, p2], fill=col, width=max(1, int(2 * s)))
        d.rectangle([p2[0] - s, p2[1] - s, p2[0] + s, p2[1] + s], fill=c_hoof)

    # Patas traseras y delanteras del lado en sombra
    _draw_leg(bl2, c_dark)
    _draw_leg(fl2, c_dark)

    # Cola al viento
    tx0, ty0 = cx - dir_x * int(12 * s), cy - int(2 * s)
    tw_y = int(round(math.sin(f_idx * 0.6) * 2 * s))
    d.line([(tx0, ty0), (tx0 - dir_x * int(8 * s), ty0 + int(2 * s) + tw_y)],
           fill=c_mane, width=max(2, int(3 * s)))

    # Torso / panza del caballo
    x_l = cx - int(12 * s)
    x_r = cx + int(12 * s)
    d.ellipse([x_l, cy - int(5 * s), x_r, cy + int(5 * s)], fill=c_body, outline=c_outline)

    # Cuello y cabeza estirados hacia adelante
    nx0, ny0 = cx + dir_x * int(9 * s), cy - int(2 * s)
    nx1, ny1 = cx + dir_x * int(16 * s), cy - int(9 * s)
    d.line([(nx0, ny0), (nx1, ny1)], fill=c_outline, width=max(3, int(5 * s)))
    d.line([(nx0, ny0), (nx1, ny1)], fill=c_body, width=max(2, int(3 * s)))
    # Crin
    d.line([(cx + dir_x * int(7 * s), cy - int(4 * s)), (cx + dir_x * int(14 * s), cy - int(10 * s))],
           fill=c_mane, width=max(1, int(2 * s)))
    # Cabeza y hocico
    hx1, hy1 = nx1 + dir_x * int(5 * s), ny1 + int(2 * s)
    d.line([(nx1, ny1), (hx1, hy1)], fill=c_outline, width=max(3, int(4 * s)))
    d.line([(nx1, ny1), (hx1, hy1)], fill=c_body, width=max(2, int(3 * s)))
    # Orejas
    d.line([(nx1, ny1 - int(2 * s)), (nx1, ny1)], fill=c_body, width=max(1, int(s)))

    # Patas del lado iluminado
    _draw_leg(bl1, c_body)
    _draw_leg(fl1, c_body)

    # Jinete (jockey) inclinado sobre la montura
    if rider:
        j_col = c_dark if silhouette_col else (238, 224, 192, 255)
        j_hat = c_body if silhouette_col else (214, 68, 58, 255)
        j_pants = c_dark if silhouette_col else (42, 52, 78, 255)
        jx, jy = cx + dir_x * int(1 * s), cy - int(6 * s)
        d.ellipse([jx - int(4 * s), jy - int(4 * s), jx + int(4 * s), jy + int(2 * s)],
                  fill=j_col, outline=c_outline)
        d.line([(jx, jy + int(1 * s)), (jx + dir_x * int(2 * s), jy + int(6 * s))],
               fill=j_pants, width=max(1, int(2 * s)))
        d.ellipse([jx + dir_x * int(3 * s) - int(3 * s), jy - int(7 * s),
                   jx + dir_x * int(3 * s) + int(3 * s), jy - int(2 * s)],
                  fill=j_hat, outline=c_outline)

    # Indicador de aire bajo las 4 patas cuando se pide resaltar el instante clave
    if highlight_air and in_air:
        d.line([(cx - int(14 * s), ground_y - int(3 * s)), (cx + int(14 * s), ground_y - int(3 * s))],
               fill=(*TESLA_CYAN, 235), width=max(1, int(s)))
        sparkle(cv, cx, ground_y - int(4 * s), float(phase) * 3.0, 2 * s, GOLD)


def draw_filmstrip(cv, x, y, w, h, t=0.0, speed=36.0, sepia=False, color_frames=False,
                   optical_track=False, alpha=1.0):
    """Dibuja una tira de película perforada de 35 mm horizontal en (x, y, w, h)
    con fotogramas del caballo corriendo (o colores RGB) y perforaciones animadas."""
    if alpha <= 0 or w <= 4 or h <= 8:
        return
    ov = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    a = int(255 * clamp01(alpha))

    # Cuerpo negro/celuloide de la tira
    d.rectangle([x, y, x + w, y + h], fill=(18, 16, 24, a), outline=(*GOLD, a))
    perf_h = max(2, min(4, h // 8))
    perf_w = max(3, min(5, h // 7))
    scroll = int(t * speed)

    # Perforaciones superiores e inferiores
    step_p = perf_w + 4
    off_p = (-scroll) % step_p
    for px in range(x + off_p - step_p, x + w + step_p, step_p):
        if x + 2 <= px and px + perf_w <= x + w - 2:
            d.rectangle([px, y + 2, px + perf_w, y + 2 + perf_h], fill=(238, 232, 214, a))
            d.rectangle([px, y + h - 2 - perf_h, px + perf_w, y + h - 2], fill=(238, 232, 214, a))

    # Fotogramas interiores
    fy0 = y + perf_h + 4
    fy1 = y + h - perf_h - 4
    if optical_track:
        fy0 += 4
        # Pista óptica de sonido (sombra dentada variable) junto a los fotogramas
        pts_opt = []
        for ox in range(x + 2, x + w - 2, 2):
            wave_w = int(1.5 + 1.5 * math.sin((ox + scroll) * 0.25))
            pts_opt.append((ox, y + perf_h + 3 + wave_w))
        if len(pts_opt) >= 2:
            d.line(pts_opt, fill=(*TESLA_CYAN, a), width=2)

    fh = max(6, fy1 - fy0)
    fw = max(12, int(fh * 1.35))
    step_f = fw + 4
    off_f = (-scroll) % step_f
    palette_rgb = [(238, 76, 76), (78, 214, 118), (82, 164, 248), (246, 198, 76)]
    for idx_f, fx in enumerate(range(x + off_f - step_f, x + w + step_f, step_f)):
        fx0 = max(x + 2, fx)
        fx1 = min(x + w - 2, fx + fw)
        if fx1 - fx0 < 6:
            continue
        frame_num = (idx_f + int(scroll // max(1, step_f))) % 12
        if color_frames:
            bg_f = (*palette_rgb[frame_num % len(palette_rgb)], a)
        elif sepia:
            bg_f = (218, 192, 146, a)
        else:
            bg_f = (226, 224, 216, a)
        d.rectangle([fx0, fy0, fx1, fy1], fill=bg_f, outline=(42, 34, 28, a))
        if fx1 - fx0 >= fw - 2 and fh >= 14:
            # Mini silueta del caballo dentro de cada fotograma
            mcx = (fx0 + fx1) // 2
            mcy = (fy0 + fy1) // 2
            d.ellipse([mcx - 5, mcy - 2, mcx + 4, mcy + 2], fill=(42, 28, 18, a))
            leg_off = (frame_num % 3) - 1
            d.line([(mcx - 3, mcy + 2), (mcx - 4 + leg_off, mcy + 5)], fill=(42, 28, 18, a))
            d.line([(mcx + 3, mcy + 2), (mcx + 4 - leg_off, mcy + 5)], fill=(42, 28, 18, a))

    comp = Image.alpha_composite(cv.convert("RGBA"), ov)
    cv.paste(comp, (0, 0))


def draw_wooden_camera(cv, x, feet=248, t=0.0, scale=1, flash=False, facing=1, label=None):
    """Cámara fotográfica o de cine de madera sobre trípode firme apoyado en el suelo (feet=248).
    Envuelta en floor_prop para no flotar jamás ni en 16:9 ni en 9:16."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        s = scale
        dir_x = 1 if facing >= 0 else -1
        top_y = fy - int(36 * s)
        # Sombra sobre el suelo
        shadow_ellipse(canvas, cx, fy, int(22 * s), max(2, int(4 * s)), 85)
        # 3 patas de madera del trípode hasta fy
        leg_c = (92, 58, 32, 255)
        for lx_end in (cx - int(12 * s), cx, cx + int(12 * s)):
            d.line([(cx, top_y + int(10 * s)), (lx_end, fy)], fill=(*INK, 255), width=max(2, int(3 * s)))
            d.line([(cx, top_y + int(10 * s)), (lx_end, fy)], fill=leg_c, width=max(1, int(2 * s)))
        # Caja de caoba y fuelle
        bx0, bx1 = cx - int(9 * s), cx + int(9 * s)
        d.rectangle([bx0, top_y, bx1, top_y + int(12 * s)], fill=(138, 84, 42, 255), outline=(*INK, 255))
        d.rectangle([bx0 + int(2 * s), top_y + int(2 * s), bx1 - int(2 * s), top_y + int(10 * s)],
                    outline=(214, 168, 72, 255))
        # Lente de bronce
        lx0 = bx1 if dir_x > 0 else bx0 - int(5 * s)
        lx1 = bx1 + int(5 * s) if dir_x > 0 else bx0
        d.rectangle([lx0, top_y + int(3 * s), lx1, top_y + int(9 * s)],
                    fill=(214, 168, 72, 255), outline=(*INK, 255))
        if flash:
            fx = lx1 + int(3 * s) if dir_x > 0 else lx0 - int(3 * s)
            fy_l = top_y + int(6 * s)
            glow(canvas, fx, fy_l, int(14 * s), GOLD, 0.7)
            sparkle(canvas, fx, fy_l, t * 5.0, int(4 * s), CREAM)
        if label:
            draw_text(canvas, str(label), cx, top_y - int(9 * s), "silk", 8, GOLD, align="center")

    floor_prop(cv, _draw, x, feet)


def draw_zoopraxiscope_table(cv, x, feet=248, t=0.0, spin=True, beam=True):
    """Zoopraxiscopio de Muybridge (rueda de vidrio con siluetas + linterna de proyección)
    apoyado sobre una mesa de madera firme con patas hasta el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        top_y = fy - 38
        shadow_ellipse(canvas, cx, fy, 32, 4, 85)
        # Patas y tapa de la mesa
        d.rectangle([cx - 24, top_y + 4, cx - 19, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx + 19, top_y + 4, cx + 24, fy], fill=(82, 52, 28, 255), outline=(*INK, 255))
        d.rectangle([cx - 28, top_y, cx + 28, top_y + 5], fill=(128, 82, 44, 255), outline=(*INK, 255))
        # Base y linterna mágica
        d.rectangle([cx - 20, top_y - 16, cx - 4, top_y], fill=(64, 58, 68, 255), outline=(*INK, 255))
        d.rectangle([cx - 16, top_y - 22, cx - 8, top_y - 16], fill=(184, 138, 58, 255), outline=(*INK, 255))
        # Rueda giratoria con las fotos del caballo
        w_cx, w_cy, r = cx + 8, top_y - 16, 13
        d.ellipse([w_cx - r, w_cy - r, w_cx + r, w_cy + r], fill=(224, 214, 184, 230), outline=(184, 138, 58, 255))
        ang0 = (t * 4.5) if spin else 0.0
        for k in range(8):
            ang = ang0 + k * (math.pi / 4.0)
            px = int(round(w_cx + math.cos(ang) * (r - 3)))
            py = int(round(w_cy + math.sin(ang) * (r - 3)))
            d.line([(w_cx, w_cy), (px, py)], fill=(92, 64, 34, 200), width=1)
            d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(32, 22, 16, 255))
        d.rectangle([w_cx - 2, w_cy, w_cx + 2, top_y], fill=(142, 102, 44, 255), outline=(*INK, 255))
        if beam:
            pts_b = [(w_cx + r, w_cy - 3), (w_cx + r + 52, w_cy - 22), (w_cx + r + 52, w_cy + 14), (w_cx + r, w_cy + 3)]
            ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).polygon(pts_b, fill=(255, 232, 148, 72))
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), ov), (0, 0))

    floor_prop(cv, _draw, x, feet)


def draw_kinetoscope_box(cv, x, feet=248, t=0.0, peep_glow=True):
    """El Kinetoscopio de Edison (caja alta de madera con mirilla superior y ranura de moneda)
    apoyado directamente en el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        shadow_ellipse(canvas, cx, fy, 26, 4, 90)
        # Gabinete vertical de madera de roble (y = fy-54 .. fy)
        top_y = fy - 54
        d.rectangle([cx - 14, top_y, cx + 14, fy], fill=(132, 82, 42, 255), outline=(*INK, 255))
        d.rectangle([cx - 11, top_y + 5, cx + 11, fy - 4], fill=(104, 62, 30, 255), outline=(176, 124, 62, 255))
        # Mirilla ocular arriba
        d.rectangle([cx - 7, top_y - 6, cx + 7, top_y], fill=(54, 48, 58, 255), outline=(*INK, 255))
        if peep_glow:
            glow(canvas, cx, top_y - 6, 12, GOLD, 0.5)
        # Ranura de moneda dorada
        d.rectangle([cx - 5, top_y + 12, cx + 5, top_y + 18], fill=(214, 168, 72, 255), outline=(*INK, 255))
        # Ventana lateral mostrando los rodillos internos de película en zigzag
        d.rectangle([cx - 8, top_y + 24, cx + 8, fy - 8], fill=(24, 22, 32, 255), outline=(184, 142, 64, 255))
        for rx in range(cx - 5, cx + 6, 4):
            d.ellipse([rx - 1, top_y + 27, rx + 1, top_y + 29], fill=(214, 168, 72, 255))
            d.ellipse([rx - 1, fy - 12, rx + 1, fy - 10], fill=(214, 168, 72, 255))
            d.line([(rx, top_y + 28), (rx, fy - 11)], fill=(218, 206, 178, 200))

    floor_prop(cv, _draw, x, feet)


def draw_cinematograph_tripod(cv, x, feet=248, t=0.0, beam=False, crank=True, facing=1):
    """El Cinematógrafo de Auguste y Louis Lumière (cajita compacta que filma, copia y proyecta)
    sobre trípode de madera apoyado en el suelo (feet=248)."""
    def _draw(canvas, cx, fy):
        d = ImageDraw.Draw(canvas)
        dir_x = 1 if facing >= 0 else -1
        top_y = fy - 40
        shadow_ellipse(canvas, cx, fy, 24, 4, 85)
        # Trípode firme hasta fy
        for lx_end in (cx - 13, cx, cx + 13):
            d.line([(cx, top_y + 12), (lx_end, fy)], fill=(*INK, 255), width=3)
            d.line([(cx, top_y + 12), (lx_end, fy)], fill=(104, 66, 36, 255), width=2)
        # Caja de madera fina de los Lumière
        d.rectangle([cx - 9, top_y - 2, cx + 9, top_y + 12], fill=(154, 98, 48, 255), outline=(*INK, 255))
        d.rectangle([cx - 7, top_y, cx + 7, top_y + 10], outline=(224, 178, 82, 255))
        # Lente de proyección/filmación
        lx0 = cx + 9 if dir_x > 0 else cx - 14
        lx1 = cx + 14 if dir_x > 0 else cx - 9
        d.rectangle([lx0, top_y + 2, lx1, top_y + 8], fill=(224, 178, 82, 255), outline=(*INK, 255))
        # Manivela giratoria
        if crank:
            ang = t * 8.0
            hx = cx + int(round(math.cos(ang) * 5))
            hy = top_y + 5 + int(round(math.sin(ang) * 5))
            d.line([(cx, top_y + 5), (hx, hy)], fill=(238, 232, 214, 255), width=2)
        if beam:
            bx = lx1 if dir_x > 0 else lx0
            pts_b = [(bx, top_y + 3), (bx + dir_x * 68, top_y - 20),
                     (bx + dir_x * 68, top_y + 24), (bx, top_y + 7)]
            ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).polygon(pts_b, fill=(255, 240, 172, 78))
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), ov), (0, 0))

    floor_prop(cv, _draw, x, feet)


def draw_melies_moon(cv, cx, cy, r=28, rocket_p=1.0, t=0.0):
    """La Luna de Georges Méliès (Viaje a la Luna, 1902) con rostro expresivo y el cohete-bala
    clavado en su ojo derecho."""
    d = ImageDraw.Draw(cv)
    glow(cv, cx, cy, r + 12, (255, 238, 174), 0.45)
    # Disco lunar crema/dorado con cráteres
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(242, 232, 194, 255), outline=(*INK, 255))
    d.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], outline=(214, 196, 148, 255))
    # Ojo izquierdo abierto y cejas
    d.ellipse([cx - int(r * 0.45), cy - int(r * 0.28), cx - int(r * 0.15), cy - int(r * 0.04)],
              fill=(255, 255, 255, 255), outline=(*INK, 255))
    d.ellipse([cx - int(r * 0.34), cy - int(r * 0.20), cx - int(r * 0.24), cy - int(r * 0.10)],
              fill=(*INK, 255))
    # Ojo derecho (guiñando de sorpresa cuando se clava la nave)
    rx_eye, ry_eye = cx + int(r * 0.30), cy - int(r * 0.16)
    d.ellipse([rx_eye - int(r * 0.16), ry_eye - int(r * 0.14), rx_eye + int(r * 0.16), ry_eye + int(r * 0.14)],
              fill=(218, 198, 152, 255), outline=(*INK, 255))
    # Nariz y boca de asombro/mueca teatral
    d.polygon([(cx, cy - int(r * 0.12)), (cx - 4, cy + int(r * 0.16)), (cx + 4, cy + int(r * 0.16))],
              fill=(218, 198, 152, 255), outline=(*INK, 255))
    if rocket_p >= 0.85:
        d.ellipse([cx - int(r * 0.26), cy + int(r * 0.26), cx + int(r * 0.26), cy + int(r * 0.56)],
                  fill=(82, 34, 38, 255), outline=(*INK, 255))
    else:
        d.arc([cx - int(r * 0.30), cy + int(r * 0.18), cx + int(r * 0.30), cy + int(r * 0.50)],
              10, 170, fill=(*INK, 255), width=2)

    # Cohete-proyectil viajando o clavado en el ojo derecho
    if rocket_p > 0:
        p = clamp01(rocket_p)
        sx = int(round((cx + r + 54) * (1 - p) + rx_eye * p))
        sy = int(round((cy - r - 24) * (1 - p) + ry_eye * p))
        # Cuerpo de bronce/acero del proyectil
        pts_rk = [
            (sx - 6, sy + 2),
            (sx + 4, sy - 6),
            (sx + 16, sy - 9),
            (sx + 18, sy - 2),
            (sx + 6, sy + 4),
        ]
        d.polygon(pts_rk, fill=(196, 156, 78, 255), outline=(*INK, 255))
        # Ventanitas circulares del cohete
        d.ellipse([sx + 5, sy - 4, sx + 9, sy], fill=(138, 234, 245, 255), outline=(*INK, 255))
        if p >= 0.9:
            sparkle(cv, rx_eye - 4, ry_eye - 4, t * 4.0, 3, GOLD)


