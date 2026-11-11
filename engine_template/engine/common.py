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


def silhouette(cv, key, x, feet, t, color=(12, 10, 22), scale=1, **pose):
    spec = S.CAST[key] if isinstance(key, str) else key
    arr = S.render(spec, t, **pose).copy()
    m = arr[..., 3] > 0
    arr[m, :3] = color
    arr = upscale(arr, scale)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale)


def robot(cv, x, feet, t, face="happy", frozen=False, alpha=1.0, sil=False, scale=1):
    # Sin robot de IA en La Historia de los Videojuegos
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
    """Devuelve el fotograma final 1920x1080 aplicando la cámara (zoom, cx, cy)."""
    if not cam or abs(cam[0] - 1.0) < 1e-3:
        return img.resize((1920, 1080), Image.NEAREST)
    z, cx, cy = cam
    z = max(1.0, z)
    w, h = W / z, H / z
    x0 = min(max(0, cx - w / 2), W - w)
    y0 = min(max(0, cy - h / 2), H - h)
    return img.resize((1920, 1080), Image.NEAREST, box=(x0, y0, x0 + w, y0 + h))


def walk(t, t0, t1, x0, x1):
    p = prog(t, t0, t1)
    x = x0 + (x1 - x0) * ease_in_out(p) if False else x0 + (x1 - x0) * p
    return x, ((t * 2.6) % 1.0 if 0 < p < 1 else None)


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


def bulb(cv, cx, cy, t, on=1.0):
    d = ImageDraw.Draw(cv)
    glow = int(200 * on)
    if on > 0:
        for r, a in ((13, 40), (10, 70)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 240, 140, int(a * on)))
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
    draw_text(cv, years, 240, 172, "press", 8, CYAN, align="center", reveal=(tt - 1.0) * 30)


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


def draw_phosphor_dot(cv, x, y, r=3, trail=None, color=(100, 255, 140)):
    """El motivo visual del documental: el punto de luz de Tennis for Two con estela de fósforo."""
    d = ImageDraw.Draw(cv)
    if trail:
        for i, (tx, ty) in enumerate(trail):
            a = int(150 * ((i + 1) / (len(trail) + 1)) ** 1.4)
            tr = max(1, r - 1)
            d.rectangle([int(tx) - tr, int(ty) - tr, int(tx) + tr, int(ty) + tr], fill=(*color, a))
    for gr, ga in ((r + 6, 35), (r + 3, 85)):
        d.ellipse([int(x) - gr, int(y) - gr, int(x) + gr, int(y) + gr], fill=(*color, ga))
    d.rectangle([int(x) - r, int(y) - r, int(x) + r, int(y) + r], fill=(235, 255, 240, 255))


def make_card(num, lines, years, snow=False, robot_face="question"):
    """Escena genérica de placa de capítulo (ventana RPG + la pelota de luz que cae sobre el número)."""
    def sc(t):
        cv = vgradient((4, 10, 12), (10, 24, 30), 10) if not snow else vgradient((4, 6, 16), (20, 30, 56), 10)
        if snow:
            SNOW.draw(cv, t, density=0.7)
        else:
            STARS.draw(cv, t * 0.5, alpha=0.6)
        t0 = TL.chapter_start(num) - 0.3
        chapter_card(cv, t, t0, num, lines, years)
        # El motivo: el punto de luz cae y rebota sobre el título del capítulo
        dt = max(0.0, t - t0)
        bx = min(240, int(90 + dt * 160))
        by = int(76 - abs(math.sin(dt * 5.8)) * 42 * math.exp(-dt * 0.7))
        trail = []
        for k in range(5, 0, -1):
            td = max(0.0, dt - k * 0.045)
            tx = min(240, int(90 + td * 160))
            ty = int(76 - abs(math.sin(td * 5.8)) * 42 * math.exp(-td * 0.7))
            trail.append((tx, ty))
        draw_phosphor_dot(cv, bx, by, r=3, trail=trail)
        if robot_face and t > t0 + 0.8:  # sin robot_face (None) no hay robot: va solo en documentales de IA
            robot(cv, 240, 256, t, face=robot_face, alpha=prog(t, t0 + 0.8, t0 + 1.1))
        return cv
    return sc


def chapter_end(num):
    """Inicio del capítulo siguiente (o fin del video si es el último capítulo, sea cual sea su número)."""
    ultimo = max(TL.chapters) if getattr(TL, "chapters", None) else 8
    return TL.chapter_start(num + 1) if num < ultimo else TL.total
