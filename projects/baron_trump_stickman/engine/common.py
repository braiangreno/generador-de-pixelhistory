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
    """Dibuja un personaje Stickman Histórico 2D en alta definición 1080p con los pies en (x, feet)."""
    spec = S.CAST[key] if isinstance(key, str) else key
    arr = S.render(spec, t, scale=scale, **pose)
    if shadow and alpha > 0.3:
        shadow_ellipse(cv, int(x), int(feet), 18 * scale, 4 * scale, 80)
    paste_arr(cv, arr, int(x) - S.SW * scale // 2, int(feet) - FEET_OFFSET * scale, alpha)


def floor_prop(cv, fn_draw, x, feet=250):
    """Dibuja un objeto apoyado sobre el piso en (x, feet)."""
    vctx = getattr(sys.modules.get("core"), "_VCTX", None)
    if vctx is not None and isinstance(cv, Image.Image) and cv.size in ((W, H), (W * 4, H * 4)):
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
    """Devuelve el fotograma final 1920x1080 aplicando zoom suave LANCZOS (CERO pixel art)."""
    if not cam or abs(cam[0] - 1.0) < 1e-3:
        return img if img.size == (1920, 1080) else img.resize((1920, 1080), Image.LANCZOS)
    z, cx, cy = cam
    z = min(1.035, max(1.0, z))
    k = 4 if img.size == (1920, 1080) else 1
    w, h = (W * k) / z, (H * k) / z
    x0 = min(max(0, cx * k - w / 2), W * k - w)
    y0 = min(4.0 * k, max(0, cy * k - h / 2), H * k - h)
    return img.resize((1920, 1080), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h))


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


def draw_scanline_beam(cv, x0, y0, w, h, t, rows=9, speed=1.35, color=(128, 238, 158),
                       beam_col=(210, 255, 225), bg_fill=(10, 24, 18), border=(72, 168, 118), alpha=1.0):
    """Dibuja el motivo visual de LÍNEA POR LÍNEA: un haz de electrones pintando renglones
    horizontales de izquierda a derecha y de arriba abajo, con punto de fósforo brillante."""
    if alpha <= 0 or w <= 4 or h <= 4:
        return
    d = ImageDraw.Draw(cv)
    a_int = int(255 * clamp01(alpha))
    if bg_fill is not None:
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(*bg_fill, int(225 * clamp01(alpha))))
    if border is not None:
        d.rectangle([x0, y0, x0 + w, y0 + h], outline=(*border, a_int), width=1)

    cyc = (t * speed) % 1.0
    total_pos = cyc * rows
    active_row = int(total_pos)
    row_frac = total_pos - active_row
    pad_x = 4
    pad_y = 4
    inner_w = max(2, w - pad_x * 2)
    step_y = max(2, (h - pad_y * 2) / float(max(1, rows - 1)))

    for r_i in range(rows):
        ry = int(round(y0 + pad_y + r_i * step_y))
        # Surco tenue de fondo
        d.line([(x0 + pad_x, ry), (x0 + w - pad_x, ry)], fill=(*shade(color, 0.32), int(140 * alpha)), width=1)
        if r_i < active_row:
            d.line([(x0 + pad_x, ry), (x0 + w - pad_x, ry)], fill=(*color, a_int), width=2)
        elif r_i == active_row:
            bx = int(round(x0 + pad_x + inner_w * row_frac))
            if bx > x0 + pad_x:
                d.line([(x0 + pad_x, ry), (bx, ry)], fill=(*color, a_int), width=2)
            # Haz / punto brillante de fósforo en la punta
            glow(cv, bx, ry, 6, color, 0.55 * alpha)
            d.rectangle([bx - 1, ry - 1, bx + 1, ry + 1], fill=(*beam_col, a_int))


def draw_crt_tv(cv, x, y, w, h, t, mode="scan", wood=(108, 68, 38)):
    """Dibuja un televisor de tubo / pantalla CRT en (x, y, w, h) con distintos modos de imagen."""
    d = ImageDraw.Draw(cv)
    # Gabinete de madera con perillas a la derecha
    d.rectangle([x, y, x + w, y + h], fill=(*wood, 255), outline=(*INK, 255))
    d.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=(*shade(wood, 1.32), 255))
    scr_w = int(w * 0.76)
    sx0, sy0 = x + 5, y + 5
    sx1, sy1 = sx0 + scr_w, y + h - 5
    # Perillas sintonizadoras y parlante a la derecha
    kx = sx1 + (x + w - sx1) // 2
    for ky in (y + int(h * 0.28), y + int(h * 0.52)):
        d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(214, 184, 112, 255), outline=(*INK, 255))
    for gy in range(y + int(h * 0.70), y + h - 5, 3):
        d.line([(sx1 + 3, gy), (x + w - 4, gy)], fill=(*shade(wood, 0.55), 255))

    # Pantalla de vidrio
    d.rectangle([sx0, sy0, sx1, sy1], fill=(12, 28, 22, 255), outline=(*INK, 255))
    scx, scy = (sx0 + sx1) // 2, (sy0 + sy1) // 2
    sw, sh = sx1 - sx0, sy1 - sy0

    if mode == "scan":
        draw_scanline_beam(cv, sx0 + 1, sy0 + 1, sw - 2, sh - 2, t, rows=max(5, sh // 5), speed=1.5,
                           color=CHALK_GREEN, bg_fill=None, border=None)
    elif mode == "line":
        glow(cv, scx, scy, max(8, sw // 3), CHALK_GREEN, 0.55)
        d.line([(sx0 + 4, scy), (sx1 - 4, scy)], fill=(195, 255, 215, 255), width=2)
    elif mode == "dollar":
        glow(cv, scx, scy, max(10, sw // 3), CHALK_GREEN, 0.55)
        for ry in range(sy0 + 2, sy1 - 1, 3):
            d.line([(sx0 + 2, ry), (sx1 - 2, ry)], fill=(24, 62, 42, 180))
        draw_text(cv, "$", scx, scy - 7, "press", 16 if sh >= 26 else 8, CHALK_GREEN, align="center")
    elif mode == "pem":
        for ry in range(sy0 + 2, sy1 - 1, 3):
            d.line([(sx0 + 2, ry), (sx1 - 2, ry)], fill=(28, 74, 48, 200))
        d.ellipse([scx - 7, scy - 8, scx + 7, scy + 6], fill=(138, 242, 168, 255), outline=(34, 92, 56, 255))
        d.arc([scx - 8, scy - 10, scx + 8, scy + 2], 180, 360, fill=(52, 134, 82, 255), width=3)
        d.point((scx - 3, scy - 2), fill=(18, 44, 28, 255))
        d.point((scx + 3, scy - 2), fill=(18, 44, 28, 255))
        d.line([(scx - 2, scy + 2), (scx + 2, scy + 2)], fill=(18, 44, 28, 255))
    elif mode == "color_rgb":
        cols = [(248, 88, 88), (98, 238, 128), (88, 168, 255)]
        for idx_c, col_c in enumerate(cols):
            cx_d = scx + (idx_c - 1) * max(6, sw // 4)
            glow(cv, cx_d, scy, 7, col_c, 0.5)
            d.ellipse([cx_d - 4, scy - 4, cx_d + 4, scy + 4], fill=(*col_c, 255))
    elif mode == "moon":
        d.rectangle([sx0 + 1, sy0 + 1, sx1 - 1, sy1 - 1], fill=(18, 24, 34, 255))
        d.rectangle([sx0 + 2, sy1 - max(6, sh // 3), sx1 - 2, sy1 - 1], fill=(168, 176, 188, 255))
        # Bandera y dos astronautas en blanco y negro
        d.rectangle([scx - 6, scy - 4, scx - 2, scy + 4], fill=(238, 242, 248, 255))
        d.rectangle([scx + 4, scy - 4, scx + 8, scy + 4], fill=(218, 224, 234, 255))
        for ry in range(sy0 + 2, sy1 - 1, 3):
            d.line([(sx0 + 2, ry), (sx1 - 2, ry)], fill=(180, 200, 220, 75))
    elif mode == "youtube":
        d.rectangle([sx0 + 1, sy0 + 1, sx1 - 1, sy1 - 1], fill=(22, 18, 28, 255))
        d.rectangle([scx - 10, scy - 7, scx + 10, scy + 7], fill=(232, 48, 48, 255), outline=(255, 255, 255, 255))
        d.polygon([(scx - 3, scy - 4), (scx - 3, scy + 4), (scx + 4, scy)], fill=(255, 255, 255, 255))


def draw_employee_badge(cv, cx, cy, num_str="0", name_str="", flip_p=1.0, scale=1,
                        bar_col=(42, 114, 218), num_col=INK):
    """Dibuja el motivo visual central del documental de Apple: la credencial de plástico
    con franja azul arriba, broche metálico y un número grande en píxeles (#0, #1, #2)."""
    d = ImageDraw.Draw(cv)
    k_flip = abs(float(flip_p))
    bw = max(4, int(round(28 * scale * max(0.12, k_flip))))
    bh = int(round(36 * scale))
    x0, y0 = int(cx - bw // 2), int(cy - bh // 2)
    x1, y1 = x0 + bw, y0 + bh
    # Sombra
    d.rectangle([x0 + 2, y0 + 2, x1 + 2, y1 + 2], fill=(0, 0, 0, 120))
    # Broche metálico superior
    clip_w = max(2, int(round(8 * scale * max(0.2, k_flip))))
    d.rectangle([int(cx - clip_w // 2), y0 - int(4 * scale), int(cx + clip_w // 2), y0],
                fill=(186, 194, 210, 255), outline=(*INK, 255))
    # Cuerpo plástico crema/blanco
    d.rectangle([x0, y0, x1, y1], fill=(244, 242, 234, 255), outline=(*INK, 255))
    # Franja azul superior
    bar_h = max(4, int(round(9 * scale)))
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + bar_h], fill=(*bar_col, 255))
    if k_flip > 0.45:
        sz = 16 if scale >= 2 else 8
        ny = y0 + bar_h + (4 * scale if not name_str else 2 * scale)
        draw_text(cv, str(num_str), int(cx), int(ny), "press", sz, num_col, align="center",
                  outline=num_col, shadow=False)
        if name_str and scale >= 2:
            draw_text(cv, name_str, int(cx), int(y1 - 11), "silk", 8, INK, align="center",
                      outline=INK, shadow=False)


def make_card(num, lines, years, snow=False, robot_face="question"):
    """Escena de placa de capítulo clásica de Pixeloide (estilo RPG a pantalla completa)
    con el motivo visual de EL EMPLEADO NÚMERO CERO: la credencial plástica #0 girando."""
    def sc(t):
        cv = vgradient((8, 14, 24), (18, 36, 48), 10) if not snow else vgradient((8, 12, 24), (24, 34, 58), 10)
        STARS.draw(cv, t, alpha=0.75)
        if snow:
            SNOW.draw(cv, t, density=0.6)
        d = ImageDraw.Draw(cv)
        # Horizonte nocturno con trazas de placa verde (1976-2026)
        d.rectangle([0, 232, W, H], fill=(14, 24, 20, 245))
        for ry in range(236, H, 7):
            d.line([(0, ry), (W, ry)], fill=(58, 154, 96, 125), width=1)
        # Credenciales #0 girando suavemente en los flancos superiores
        flip = math.cos(t * 2.2)
        draw_employee_badge(cv, 54, 42, num_str="0", flip_p=flip, scale=1)
        draw_employee_badge(cv, 426, 42, num_str=str(num), flip_p=-flip, scale=1)
        t0 = TL.chapter_start(num) - 0.15
        chapter_card(cv, t, t0, num, lines, years, ramp_title=GOLD_RAMP)
        return vignette(cv, 0.32)
    return sc


def chapter_end(num):
    """Inicio del capítulo siguiente (o fin del video)."""
    max_ch = max(TL.chapters) if hasattr(TL, "chapters") and TL.chapters else 8
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
CORAL = (248, 108, 98)
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


def draw_chapter_header(cv, a1, a2, a3, a4, place_es=None, border=GOLD):
    """Encabezado superior estilo Stickman Histórico 2D (OverSimplified):
    acepta tanto (cv, t, t0, ch_num, title_es, place_es) como (cv, title_es, place_es, t, t0)."""
    if isinstance(a1, str):
        full_title, place_es, t, t0 = a1, a2, float(a3), float(a4)
    else:
        t, t0, ch_num, title_es = float(a1), float(a2), a3, a4
        full_title = f"{ch_num} · {title_es}"
    dt = t - t0
    if dt < -0.35:
        return
    window(cv, 14, 8, 452, 34 if place_es else 24, fill=(184, 38, 34), border=(248, 236, 200), alpha=0.96, inner=(124, 22, 20))
    draw_text(cv, full_title, 240, 12, "press", 8, (255, 246, 214), align="center",
              reveal=max(1, int((dt + 0.15) * 38)))
    if place_es:
        rev_p = max(0, int((dt - 0.15) * 28))
        draw_text(cv, place_es, 240, 26, "silk", 8, CREAM, align="center", reveal=rev_p)


def draw_place_only(cv, place_es, t, t0, border=AMBER):
    """Rótulo superior estilo Stickman Histórico 2D (franja carmesí/crema documental)."""
    if t < t0 - 0.1:
        return
    dt = max(0.0, t - t0)
    window(cv, 20, 8, 440, 22, fill=(184, 38, 34), border=(248, 236, 200), alpha=0.95, inner=(124, 22, 20))
    draw_text(cv, place_es, 240, 14, "press", 8, (255, 246, 214), align="center", reveal=max(1, int(dt * 26)))


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

def person_card(cv, portrait_key, name, subtitle, t, t0, y=166, frame=GOLD, dur=2.8):
    """Dibuja la tarjeta clásica de presentación de personaje con retrato 64x64 a la izquierda
    y ventana RPG de nombre + subtítulo a la derecha (idéntica al Episodio 1 de IA).
    En 9:16 se registra en vctx.person_cards para redibujarse limpia sin dividirse."""
    if t < t0 - 0.15:
        return
    if dur is not None and t > t0 + dur + 0.35:
        return
    vctx = getattr(sys.modules.get("core"), "_VCTX", None)
    if vctx is not None and isinstance(cv, Image.Image) and cv.size == (W, H):
        if hasattr(vctx, "person_cards"):
            vctx.person_cards.append({
                "key": portrait_key,
                "name": name,
                "sub": subtitle,
                "t": t,
                "t0": t0,
                "frame": frame,
            })
            return
    def _draw_pc(target_cv):
        a = prog(t, t0 - 0.15, t0 + 0.25)
        a_out = prog(t, t0 + dur, t0 + dur + 0.35) if dur is not None else 0.0
        off = int((1 - ease_out(a)) * -140) + int(ease_in_out(a_out) * -380)
        portrait_card(target_cv, portrait_key, 14 + off, y, frame=frame)
        tw_name, _ = text_size(name, "press", 16)
        tw_sub, _ = text_size(subtitle, "silk", 8)
        tw = min(376, max(268, max(tw_name, tw_sub) + 24))
        window(target_cv, 86 + off, y + 14, tw, 46, border=frame)
        name_sz = 16 if tw_name <= (tw - 20) else 8
        name_y = (y + 24) if name_sz == 16 else (y + 26)
        draw_text(target_cv, name, 96 + off, name_y, "press", name_sz, CREAM)
        draw_text(target_cv, subtitle, 96 + off, y + 44, "silk", 8, GREY)

    if isinstance(cv, Image.Image) and cv.size in ((W, H), (W * 4, H * 4)):
        q = getattr(cv, "_deferred_person_cards", None)
        if q is None:
            q = []
            cv._deferred_person_cards = q
        q.append(_draw_pc)
    else:
        _draw_pc(cv)


# ===========================================================================
# PROPS APOYADOS EN EL SUELO (floor_prop) PARA «EL EMPLEADO NÚMERO CERO»
# ===========================================================================

def draw_office_desk_1977(cv, x, feet):
    """Escritorio de oficina de 1977 apoyado en el suelo con carpeta verde y credenciales."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    # Patas metálicas apoyadas en feet
    d.rectangle([x - 36, feet - 32, x - 31, feet], fill=(78, 82, 96, 255), outline=(*INK, 255))
    d.rectangle([x + 31, feet - 32, x + 36, feet], fill=(78, 82, 96, 255), outline=(*INK, 255))
    # Frente de madera y tablero
    d.rectangle([x - 38, feet - 34, x + 38, feet - 16], fill=(138, 92, 52, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 38, x + 42, feet - 33], fill=(176, 122, 72, 255), outline=(*INK, 255))
    # Carpeta verde y credenciales apoyadas arriba
    d.rectangle([x - 28, feet - 43, x - 6, feet - 38], fill=(48, 134, 78, 255), outline=(*INK, 255))
    d.rectangle([x + 2, feet - 44, x + 14, feet - 38], fill=(244, 242, 232, 255), outline=(*INK, 255))
    d.rectangle([x + 3, feet - 43, x + 13, feet - 41], fill=(42, 114, 218, 255))
    d.rectangle([x + 18, feet - 44, x + 30, feet - 38], fill=(244, 242, 232, 255), outline=(*INK, 255))
    d.rectangle([x + 19, feet - 43, x + 29, feet - 41], fill=(42, 114, 218, 255))


def draw_payphone_booth_prop(cv, x, feet):
    """Cabina / poste de teléfono público de 1971 apoyado en el pavimento."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 22, 4, 95)
    # Poste metálico hasta el suelo
    d.rectangle([x - 5, feet - 52, x + 5, feet], fill=(92, 98, 114, 255), outline=(*INK, 255))
    d.rectangle([x - 12, feet - 4, x + 12, feet], fill=(64, 68, 82, 255), outline=(*INK, 255))
    # Caja del teléfono público
    d.rectangle([x - 15, feet - 84, x + 15, feet - 48], fill=(52, 58, 72, 255), outline=(*INK, 255))
    d.rectangle([x - 11, feet - 80, x + 11, feet - 54], fill=(186, 194, 208, 255), outline=(*INK, 255))
    # Teclado y ranura de monedas
    for r in range(3):
        for c in range(3):
            px = x - 6 + c * 5
            py = feet - 70 + r * 4
            d.rectangle([px, py, px + 2, py + 2], fill=(40, 44, 54, 255))
    # Auricular colgado a la izquierda
    d.rectangle([x - 20, feet - 78, x - 15, feet - 58], fill=(28, 30, 38, 255), outline=(*INK, 255))


def draw_vatican_table_prop(cv, x, feet):
    """Mesita de madera del Vaticano apoyada en el suelo con teléfono negro y candelabro con vela apoyada."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 28, 4, 95)
    # Patas de madera tallada hasta el piso
    d.rectangle([x - 20, feet - 32, x - 15, feet], fill=(104, 64, 36, 255), outline=(*INK, 255))
    d.rectangle([x + 15, feet - 32, x + 20, feet], fill=(104, 64, 36, 255), outline=(*INK, 255))
    d.rectangle([x - 24, feet - 37, x + 24, feet - 31], fill=(146, 94, 52, 255), outline=(*INK, 255))
    # Mantelito dorado
    d.rectangle([x - 16, feet - 38, x + 16, feet - 35], fill=(214, 172, 74, 255), outline=(*INK, 255))
    # Teléfono negro antiguo a la izquierda
    d.rectangle([x - 17, feet - 46, x - 3, feet - 38], fill=(28, 28, 36, 255), outline=(*INK, 255))
    d.ellipse([x - 13, feet - 44, x - 7, feet - 39], fill=(218, 212, 196, 255))
    d.rectangle([x - 19, feet - 49, x - 1, feet - 46], fill=(42, 42, 54, 255), outline=(*INK, 255))
    # Candelabro con vela APOYADO sobre la mesa (nunca flotando)
    d.rectangle([x + 6, feet - 40, x + 16, feet - 38], fill=(218, 176, 72, 255), outline=(*INK, 255))
    d.rectangle([x + 9, feet - 50, x + 13, feet - 40], fill=(246, 240, 222, 255), outline=(*INK, 255))
    glow(cv, x + 11, feet - 53, 10, AMBER, 0.55)
    d.polygon([(x + 11, feet - 56), (x + 8, feet - 51), (x + 14, feet - 51)], fill=(255, 222, 96, 255))


def draw_atari_bench_prop(cv, x, feet):
    """Mesa de taller electrónico de 1974 apoyada en el suelo con osciloscopio y cajón de manzanas."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 36, feet - 32, x - 31, feet], fill=(82, 64, 44, 255), outline=(*INK, 255))
    d.rectangle([x + 31, feet - 32, x + 36, feet], fill=(82, 64, 44, 255), outline=(*INK, 255))
    d.rectangle([x - 40, feet - 37, x + 40, feet - 31], fill=(142, 98, 56, 255), outline=(*INK, 255))
    # Osciloscopio y placa verde
    d.rectangle([x - 32, feet - 53, x - 10, feet - 37], fill=(168, 176, 184, 255), outline=(*INK, 255))
    d.rectangle([x - 29, feet - 50, x - 16, feet - 41], fill=(16, 48, 32, 255))
    d.line([(x - 28, feet - 45), (x - 23, feet - 48), (x - 18, feet - 43)], fill=(110, 248, 148, 255))
    d.rectangle([x - 4, feet - 41, x + 18, feet - 37], fill=(42, 136, 74, 255), outline=(*INK, 255))
    # Cajón de madera con manzanas enteras (sin mordisco) apoyado sobre la mesa
    d.rectangle([x + 20, feet - 45, x + 36, feet - 37], fill=(164, 112, 62, 255), outline=(*INK, 255))
    for ax in (x + 24, x + 31):
        d.ellipse([ax - 3, feet - 49, ax + 3, feet - 44], fill=(218, 52, 48, 255), outline=(*INK, 255))


def draw_arcade_cabinet_prop(cv, x, feet):
    """Gabinete de arcade de 1974 apoyado en el suelo con pantalla de ladrillos de colores."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 22, 4, 95)
    # Cuerpo de madera y lateral amarillo/naranja
    d.rectangle([x - 16, feet - 74, x + 16, feet], fill=(118, 68, 34, 255), outline=(*INK, 255))
    d.rectangle([x - 14, feet - 72, x + 14, feet - 64], fill=(238, 174, 52, 255), outline=(*INK, 255))
    # Pantalla con filas de ladrillos (Breakout)
    d.rectangle([x - 12, feet - 62, x + 12, feet - 40], fill=(14, 18, 28, 255), outline=(*INK, 255))
    brick_cols = [(232, 68, 62), (242, 158, 54), (92, 214, 112), (84, 178, 248)]
    for r_i, bcol in enumerate(brick_cols):
        by = feet - 59 + r_i * 3
        d.line([(x - 10, by), (x + 10, by)], fill=(*bcol, 255), width=2)
    # Paleta abajo y pelotita
    d.rectangle([x - 4, feet - 43, x + 4, feet - 42], fill=(240, 244, 255, 255))
    d.rectangle([x + 1, feet - 48, x + 3, feet - 46], fill=(255, 255, 255, 255))
    # Panel de control y monedero
    d.rectangle([x - 15, feet - 39, x + 15, feet - 33], fill=(42, 46, 58, 255), outline=(*INK, 255))
    d.rectangle([x - 6, feet - 24, x + 6, feet - 8], fill=(32, 34, 44, 255), outline=(*INK, 255))


def draw_garage_bench_1976(cv, x, feet):
    """Mesa de madera del garaje de Los Altos (1976) apoyada en el suelo con placas verdes Apple I."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 48, 5, 95)
    d.rectangle([x - 40, feet - 32, x - 34, feet], fill=(104, 72, 42, 255), outline=(*INK, 255))
    d.rectangle([x + 34, feet - 32, x + 40, feet], fill=(104, 72, 42, 255), outline=(*INK, 255))
    d.rectangle([x - 44, feet - 38, x + 44, feet - 31], fill=(158, 112, 66, 255), outline=(*INK, 255))
    # Dos placas de circuito verde con chips negros encima
    for bx in (x - 32, x + 4):
        d.rectangle([bx, feet - 43, bx + 26, feet - 38], fill=(38, 138, 74, 255), outline=(*INK, 255))
        for cx_i in range(bx + 3, bx + 23, 6):
            d.rectangle([cx_i, feet - 42, cx_i + 4, feet - 40], fill=(28, 30, 38, 255))


def draw_clerk_window_prop(cv, x, feet):
    """Mostrador de oficina pública de 1976 apoyado en el suelo con sello y billetes de 800 dólares."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 42, 5, 95)
    d.rectangle([x - 38, feet - 38, x + 38, feet], fill=(122, 82, 46, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 43, x + 42, feet - 37], fill=(168, 118, 68, 255), outline=(*INK, 255))
    # Ventanilla con barrotes superiores
    d.rectangle([x - 34, feet - 76, x + 34, feet - 43], outline=(168, 118, 68, 255), width=2)
    # Contrato y fajo de billetes verdes ($800) sobre el mostrador
    d.rectangle([x - 24, feet - 47, x - 4, feet - 43], fill=(244, 240, 224, 255), outline=(*INK, 255))
    d.rectangle([x + 6, feet - 48, x + 26, feet - 43], fill=(74, 168, 92, 255), outline=(*INK, 255))


def draw_vw_van_prop(cv, x, feet):
    """Camioneta combi de los años 70 apoyada sobre sus ruedas en el suelo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 46, 5, 100)
    # Carrocería bicolor (crema arriba, rojo/naranja abajo)
    d.rectangle([x - 40, feet - 36, x + 40, feet - 7], fill=(208, 78, 54, 255), outline=(*INK, 255))
    d.rectangle([x - 38, feet - 54, x + 38, feet - 34], fill=(242, 236, 218, 255), outline=(*INK, 255))
    # Ventanillas
    for wx in (x - 32, x - 14, x + 4, x + 22):
        d.rectangle([wx, feet - 50, wx + 12, feet - 38], fill=(84, 148, 196, 255), outline=(*INK, 255))
    # Ruedas apoyadas en feet
    for rx in (x - 24, x + 24):
        d.ellipse([rx - 9, feet - 16, rx + 9, feet], fill=(28, 30, 38, 255), outline=(*INK, 255))
        d.ellipse([rx - 4, feet - 11, rx + 4, feet - 3], fill=(192, 198, 210, 255))


def draw_fair_booth_prop(cv, x, feet):
    """Mesa de stand de la Feria de San Francisco (1977) con computadora beige Apple II arriba."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 46, 5, 95)
    # Mantel azul oscuro hasta el suelo
    d.rectangle([x - 42, feet - 34, x + 42, feet], fill=(32, 64, 124, 255), outline=(*INK, 255))
    d.rectangle([x - 44, feet - 38, x + 44, feet - 33], fill=(232, 224, 204, 255), outline=(*INK, 255))
    # Computadora beige de carcasa plástica (Apple II) apoyada sobre la mesa
    d.rectangle([x - 22, feet - 48, x + 6, feet - 38], fill=(228, 218, 192, 255), outline=(*INK, 255))
    d.rectangle([x - 19, feet - 64, x + 3, feet - 48], fill=(218, 208, 182, 255), outline=(*INK, 255))
    d.rectangle([x - 16, feet - 61, x, feet - 51], fill=(18, 48, 28, 255))
    # Pilas de folletos turquesa "ZALTAIR" a la derecha
    d.rectangle([x + 14, feet - 45, x + 34, feet - 38], fill=(72, 208, 214, 255), outline=(*INK, 255))


def draw_pirate_flag_prop(cv, x, feet):
    """Mástil apoyado en el suelo con la bandera pirata del equipo Macintosh (calavera con parche liso, sin logos)."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 18, 4, 95)
    # Base y mástil
    d.rectangle([x - 12, feet - 5, x + 12, feet], fill=(86, 92, 108, 255), outline=(*INK, 255))
    d.rectangle([x - 2, feet - 96, x + 2, feet - 5], fill=(186, 192, 208, 255), outline=(*INK, 255))
    # Paño negro ondeando hacia la derecha
    fx0, fy0 = x + 2, feet - 94
    fw, fh = 48, 30
    d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=(20, 20, 28, 255), outline=(*CREAM, 255))
    # Calavera blanca con parche negro liso (sin manzana ni logos)
    scx, scy = fx0 + fw // 2, fy0 + fh // 2 - 2
    d.ellipse([scx - 7, scy - 7, scx + 7, scy + 5], fill=(244, 242, 234, 255), outline=(*INK, 255))
    d.rectangle([scx - 4, scy + 4, scx + 4, scy + 8], fill=(244, 242, 234, 255), outline=(*INK, 255))
    # Ojo izquierdo normal y ojo derecho con parche pirata liso
    d.rectangle([scx - 4, scy - 2, scx - 2, scy], fill=(20, 20, 28, 255))
    d.ellipse([scx + 1, scy - 3, scx + 5, scy + 1], fill=(20, 20, 28, 255))
    d.line([(scx - 6, scy - 5), (scx + 6, scy - 1)], fill=(20, 20, 28, 255), width=1)
    # Huesos cruzados debajo
    d.line([(scx - 11, scy + 9), (scx + 11, scy + 13)], fill=(244, 242, 234, 255), width=2)
    d.line([(scx - 11, scy + 13), (scx + 11, scy + 9)], fill=(244, 242, 234, 255), width=2)


def draw_mac_1984_podium_prop(cv, x, feet):
    """Mesa de escenario de enero de 1984 con bolso abierto y la Macintosh compacta diciendo HELLO."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 40, 5, 95)
    d.rectangle([x - 34, feet - 34, x + 34, feet], fill=(28, 32, 48, 255), outline=(*INK, 255))
    d.rectangle([x - 36, feet - 38, x + 36, feet - 33], fill=(198, 188, 168, 255), outline=(*INK, 255))
    # Bolso de lona oscura a la izquierda
    d.rectangle([x - 30, feet - 52, x - 10, feet - 38], fill=(56, 62, 78, 255), outline=(*INK, 255))
    # Macintosh 1984 vertical beige a la derecha
    mx0, my0 = x - 2, feet - 68
    d.rectangle([mx0, my0, mx0 + 24, feet - 38], fill=(234, 224, 198, 255), outline=(*INK, 255))
    # Pantalla blanca luminosa con carita / saludo
    d.rectangle([mx0 + 3, my0 + 3, mx0 + 21, my0 + 17], fill=(238, 248, 255, 255), outline=(*INK, 255))
    d.line([(mx0 + 6, my0 + 10), (mx0 + 18, my0 + 10)], fill=(24, 32, 48, 255), width=2)
    # Ranura de disquete
    d.line([(mx0 + 12, my0 + 21), (mx0 + 19, my0 + 21)], fill=(40, 40, 48, 255), width=2)


def draw_next_cube_prop(cv, x, feet):
    """Pedestal apoyado en el suelo con el cubo negro perfecto de magnesio (1988)."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 28, 4, 95)
    # Pedestal gris oscuro hasta el piso
    d.rectangle([x - 20, feet - 34, x + 20, feet], fill=(64, 68, 82, 255), outline=(*INK, 255))
    d.rectangle([x - 24, feet - 38, x + 24, feet - 33], fill=(112, 118, 134, 255), outline=(*INK, 255))
    # Cubo negro mate de 30x30 cm
    d.rectangle([x - 16, feet - 70, x + 16, feet - 38], fill=(22, 24, 30, 255), outline=(92, 98, 114, 255))
    d.line([(x - 15, feet - 69), (x + 15, feet - 69)], fill=(120, 128, 144, 255))
    d.line([(x - 12, feet - 54), (x + 12, feet - 54)], fill=(48, 52, 64, 255))


def draw_lawyer_desk_prop(cv, x, feet):
    """Escritorio de abogados de Londres (1989) apoyado en el suelo con carta lacrada."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 38, feet - 34, x + 38, feet], fill=(96, 52, 34, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 38, x + 42, feet - 33], fill=(138, 78, 48, 255), outline=(*INK, 255))
    # Carta legal con sello rojo y carpeta
    d.rectangle([x - 24, feet - 44, x - 2, feet - 38], fill=(246, 240, 224, 255), outline=(*INK, 255))
    d.ellipse([x - 15, feet - 43, x - 11, feet - 39], fill=(214, 48, 48, 255))
    # Monitor compacto de 1989 a la derecha para Jim Reekes
    d.rectangle([x + 6, feet - 62, x + 28, feet - 38], fill=(228, 220, 198, 255), outline=(*INK, 255))
    d.rectangle([x + 9, feet - 59, x + 25, feet - 47], fill=(180, 224, 248, 255), outline=(*INK, 255))


def draw_silver_car_prop(cv, x, feet):
    """Auto deportivo plateado sin patente trasera, apoyado sobre sus ruedas en el estacionamiento."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 48, 5, 105)
    # Carrocería plateada aerodinámica
    d.polygon([(x - 42, feet - 8), (x - 38, feet - 22), (x - 16, feet - 24),
               (x - 6, feet - 34), (x + 18, feet - 34), (x + 38, feet - 22), (x + 42, feet - 8)],
              fill=(196, 204, 218, 255), outline=(*INK, 255))
    d.line([(x - 36, feet - 20), (x + 36, feet - 20)], fill=(238, 244, 255, 255))
    # Parabrisas
    d.polygon([(x - 14, feet - 23), (x - 5, feet - 32), (x + 14, feet - 32), (x + 18, feet - 23)],
              fill=(72, 118, 164, 255), outline=(*INK, 255))
    # Ruedas apoyadas en feet
    for rx in (x - 24, x + 24):
        d.ellipse([rx - 9, feet - 16, rx + 9, feet], fill=(26, 28, 36, 255), outline=(*INK, 255))
        d.ellipse([rx - 5, feet - 12, rx + 5, feet - 2], fill=(168, 176, 190, 255))
    # Hueco de patente vacío resaltado en rojo/dorado a la izquierda
    d.rectangle([x - 42, feet - 17, x - 35, feet - 11], fill=(42, 46, 58, 255), outline=(238, 84, 78, 255))


def draw_iphone_podium_prop(cv, x, feet):
    """Mesa de escenario de enero de 2007 apoyada en el suelo con los tres teléfonos de prueba."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 38, 5, 95)
    d.rectangle([x - 32, feet - 34, x + 32, feet], fill=(24, 28, 40, 255), outline=(*INK, 255))
    d.rectangle([x - 36, feet - 38, x + 36, feet - 33], fill=(74, 82, 102, 255), outline=(*INK, 255))
    # Tres teléfonos apoyados en fila + cable oculto
    for idx_p, px in enumerate((x - 20, x, x + 20)):
        d.rectangle([px - 5, feet - 50, px + 5, feet - 38], fill=(32, 36, 48, 255), outline=(186, 196, 214, 255))
        d.rectangle([px - 4, feet - 48, px + 4, feet - 40], fill=(74, 168, 238, 255))
    # Cable secreto que baja por detrás de la mesa
    d.line([(x, feet - 38), (x, feet)], fill=(242, 196, 68, 255), width=2)


def draw_apple_park_stage_prop(cv, x, feet):
    """Piano y arco iris concéntrico del escenario de Apple Park (marzo 2026) apoyados en el suelo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 46, 5, 95)
    # Arcos concéntricos de colores detrás del piano, apoyados en feet - 32
    arch_cols = [(232, 68, 62), (244, 154, 52), (248, 216, 72), (88, 204, 104), (74, 164, 242), (168, 104, 232)]
    for i, acol in enumerate(arch_cols):
        r = 38 - i * 4
        d.arc([x - r, feet - 34 - r, x + r, feet - 34 + r], 180, 360, fill=(*acol, 255), width=3)
    # Tarima y piano de cola negro apoyado en el suelo
    d.rectangle([x - 42, feet - 8, x + 42, feet], fill=(44, 48, 62, 255), outline=(*INK, 255))
    d.rectangle([x - 26, feet - 28, x + 24, feet - 8], fill=(22, 24, 32, 255), outline=(*INK, 255))
    d.rectangle([x - 24, feet - 22, x - 4, feet - 18], fill=(244, 242, 234, 255))


# ===========================================================================
# PROPS Y MOTIVOS PARA «UN CHICO LLAMADO BARON TRUMP»
# ===========================================================================

def draw_pocket_watch(cv, cx, cy, t, r=18, reverse=True, speed=1.8, stopped=False):
    """Motivo visual del episodio: reloj de bolsillo antiguo cuyas agujas giran al revés."""
    d = ImageDraw.Draw(cv)
    # Aro superior y corona
    d.ellipse([cx - 5, cy - r - 9, cx + 5, cy - r - 1], outline=(*GOLD, 255), width=2)
    d.rectangle([cx - 3, cy - r - 3, cx + 3, cy - r + 1], fill=(*GOLD_D, 255), outline=(*INK, 255))
    # Caja dorada y esfera crema
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(*GOLD, 255), outline=(*INK, 255), width=2)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=(248, 242, 224, 255), outline=(*GOLD_D, 255))
    # Marcas de horas
    for i in range(12):
        ang = i * math.pi / 6
        x0 = cx + math.cos(ang) * (r - 6)
        y0 = cy + math.sin(ang) * (r - 6)
        x1 = cx + math.cos(ang) * (r - 3)
        y1 = cy + math.sin(ang) * (r - 3)
        d.line([(x0, y0), (x1, y1)], fill=(*INK, 255), width=1)
    # Agujas girando al revés (antihorario) o detenidas
    sgn = -1.0 if reverse else 1.0
    ang_m = -math.pi / 2 if stopped else (-math.pi / 2 + sgn * t * speed * 2.2)
    ang_h = -math.pi / 6 if stopped else (-math.pi / 2 + sgn * t * speed * 0.35)
    d.line([(cx, cy), (cx + math.cos(ang_h) * (r * 0.48), cy + math.sin(ang_h) * (r * 0.48))],
           fill=(*INK, 255), width=2)
    d.line([(cx, cy), (cx + math.cos(ang_m) * (r * 0.72), cy + math.sin(ang_m) * (r * 0.72))],
           fill=(186, 42, 42, 255), width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(*GOLD_D, 255), outline=(*INK, 255))


def draw_library_table_prop(cv, x, feet, t=0.0, book_open=False):
    """Mesa de madera de biblioteca 1893 apoyada en el suelo con libro de tapa de tela y reloj de bolsillo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 36, feet - 32, x - 30, feet], fill=(92, 58, 34, 255), outline=(*INK, 255))
    d.rectangle([x + 30, feet - 32, x + 36, feet], fill=(92, 58, 34, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 38, x + 42, feet - 31], fill=(138, 88, 48, 255), outline=(*INK, 255))
    if book_open:
        d.rectangle([x - 30, feet - 44, x + 10, feet - 38], fill=(122, 42, 38, 255), outline=(*INK, 255))
        d.rectangle([x - 28, feet - 47, x - 11, feet - 39], fill=(246, 238, 214, 255), outline=(*INK, 255))
        d.rectangle([x - 9, feet - 47, x + 8, feet - 39], fill=(246, 238, 214, 255), outline=(*INK, 255))
    else:
        d.rectangle([x - 26, feet - 46, x + 6, feet - 38], fill=(122, 42, 38, 255), outline=(*INK, 255))
        d.line([(x - 22, feet - 42), (x + 2, feet - 42)], fill=(*GOLD, 255), width=1)
    # Reloj de bolsillo apoyado sobre la mesa
    draw_pocket_watch(cv, x + 24, feet - 48, t, r=9, reverse=True, speed=1.4)


def draw_bulger_dog_prop(cv, x, feet):
    """Perro enorme Bulger (personaje literario de 1893) apoyado sobre sus cuatro patas en el suelo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 22, 4, 90)
    col = (146, 102, 62)
    col_d = (104, 68, 38)
    # Patas apoyadas en feet
    for lx in (x - 14, x - 8, x + 6, x + 12):
        d.rectangle([lx - 2, feet - 14, lx + 2, feet], fill=(*col_d, 255), outline=(*INK, 255))
    # Cuerpo y cola
    d.ellipse([x - 18, feet - 28, x + 16, feet - 10], fill=(*col, 255), outline=(*INK, 255), width=2)
    d.line([(x - 16, feet - 22), (x - 24, feet - 30)], fill=(*col_d, 255), width=3)
    # Cabeza grande y oreja caída
    d.ellipse([x + 8, feet - 36, x + 24, feet - 20], fill=(*col, 255), outline=(*INK, 255), width=2)
    d.ellipse([x + 10, feet - 32, x + 15, feet - 22], fill=(*col_d, 255), outline=(*INK, 255))
    d.ellipse([x + 17, feet - 31, x + 20, feet - 28], fill=(*WHITE, 255), outline=(*INK, 255))
    d.point((x + 19, feet - 29), fill=(*INK, 255))
    d.ellipse([x + 22, feet - 27, x + 25, feet - 24], fill=(*INK, 255))


def draw_lawyer_desk_1893_prop(cv, x, feet):
    """Escritorio de abogado del siglo XIX apoyado en el suelo con manuscritos y tintero."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 36, feet - 34, x + 36, feet], fill=(88, 54, 34, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 39, x + 42, feet - 33], fill=(132, 82, 48, 255), outline=(*INK, 255))
    # Hojas manuscritas y tintero con pluma
    d.rectangle([x - 26, feet - 44, x + 2, feet - 39], fill=(246, 238, 214, 255), outline=(*INK, 255))
    d.rectangle([x + 12, feet - 46, x + 20, feet - 39], fill=(28, 32, 44, 255), outline=(*INK, 255))
    d.line([(x + 16, feet - 46), (x + 24, feet - 58)], fill=(248, 244, 230, 255), width=2)


def draw_book_stack_prop(cv, x, feet):
    """Mesita con los tres libros olvidados apilados."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 34, 4, 95)
    d.rectangle([x - 28, feet - 30, x - 23, feet], fill=(86, 54, 34, 255), outline=(*INK, 255))
    d.rectangle([x + 23, feet - 30, x + 28, feet], fill=(86, 54, 34, 255), outline=(*INK, 255))
    d.rectangle([x - 32, feet - 35, x + 32, feet - 29], fill=(134, 86, 48, 255), outline=(*INK, 255))
    # 3 libros apilados
    d.rectangle([x - 20, feet - 42, x + 20, feet - 35], fill=(122, 42, 38, 255), outline=(*INK, 255))
    d.rectangle([x - 18, feet - 49, x + 18, feet - 42], fill=(42, 74, 114, 255), outline=(*INK, 255))
    d.rectangle([x - 16, feet - 54, x + 16, feet - 49], fill=(64, 108, 68, 255), outline=(*INK, 255))


def draw_tesla_table_prop(cv, x, feet, powered=True, t=0.0):
    """Mesa de hotel de 1943 con planos, bobina de Tesla y reloj de bolsillo apoyados."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 36, feet - 32, x - 31, feet], fill=(72, 54, 42, 255), outline=(*INK, 255))
    d.rectangle([x + 31, feet - 32, x + 36, feet], fill=(72, 54, 42, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 38, x + 42, feet - 31], fill=(112, 82, 62, 255), outline=(*INK, 255))
    # Planos azules a la izquierda
    d.rectangle([x - 34, feet - 42, x - 10, feet - 38], fill=(44, 104, 178, 255), outline=(*INK, 255))
    # Bobina de Tesla en el centro
    d.rectangle([x - 4, feet - 43, x + 14, feet - 38], fill=(62, 66, 78, 255), outline=(*INK, 255))
    d.rectangle([x + 1, feet - 64, x + 9, feet - 43], fill=(176, 112, 52, 255), outline=(*INK, 255))
    d.ellipse([x - 4, feet - 70, x + 14, feet - 62], fill=(182, 194, 212, 255), outline=(*INK, 255))
    if powered:
        glow(cv, x + 5, feet - 66, 22, (72, 198, 255), 0.55)
        for k in range(3):
            ang = t * 5.0 + k * 2.1
            sx = x + 5 + int(math.cos(ang) * 14)
            sy = feet - 66 + int(math.sin(ang) * 10)
            d.line([(x + 5, feet - 66), (sx, sy)], fill=(156, 236, 255, 255), width=2)
    # Reloj de bolsillo a la derecha
    draw_pocket_watch(cv, x + 28, feet - 47, t, r=8, reverse=True, speed=1.2)


def draw_trunk_prop(cv, x, feet):
    """Baúl de madera y metal de Tesla apoyado en el suelo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 28, 4, 95)
    d.rectangle([x - 24, feet - 26, x + 24, feet], fill=(92, 62, 38, 255), outline=(*INK, 255), width=2)
    d.rectangle([x - 24, feet - 26, x + 24, feet - 20], fill=(118, 82, 50, 255), outline=(*INK, 255))
    d.line([(x - 14, feet - 26), (x - 14, feet)], fill=(64, 68, 78, 255), width=2)
    d.line([(x + 14, feet - 26), (x + 14, feet)], fill=(64, 68, 78, 255), width=2)
    d.rectangle([x - 4, feet - 22, x + 4, feet - 16], fill=(*GOLD, 255), outline=(*INK, 255))


def draw_mit_desk_prop(cv, x, feet):
    """Escritorio de ingeniería de 1943 con lámpara verde, planos y carpeta de informe."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 44, 5, 95)
    d.rectangle([x - 38, feet - 34, x + 38, feet], fill=(74, 80, 92, 255), outline=(*INK, 255))
    d.rectangle([x - 42, feet - 39, x + 42, feet - 33], fill=(112, 118, 132, 255), outline=(*INK, 255))
    # Carpeta de informe
    d.rectangle([x - 20, feet - 44, x + 6, feet - 39], fill=(224, 196, 138, 255), outline=(*INK, 255))
    # Lámpara verde de banquero apoyada
    d.rectangle([x + 18, feet - 42, x + 28, feet - 39], fill=(*GOLD_D, 255), outline=(*INK, 255))
    d.line([(x + 23, feet - 42), (x + 23, feet - 54)], fill=(*GOLD_D, 255), width=2)
    d.polygon([(x + 14, feet - 53), (x + 32, feet - 53), (x + 28, feet - 60), (x + 18, feet - 60)],
              fill=(42, 148, 86, 255), outline=(*INK, 255))
    glow(cv, x + 23, feet - 52, 16, (148, 255, 178), 0.35)


def draw_forum_desk_prop(cv, x, feet):
    """Escritorio moderno de 2017 con dos monitores genéricos encendidos."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 46, 5, 95)
    d.rectangle([x - 38, feet - 32, x - 33, feet], fill=(54, 58, 72, 255), outline=(*INK, 255))
    d.rectangle([x + 33, feet - 32, x + 38, feet], fill=(54, 58, 72, 255), outline=(*INK, 255))
    d.rectangle([x - 44, feet - 37, x + 44, feet - 31], fill=(82, 88, 108, 255), outline=(*INK, 255))
    for mx in (x - 24, x + 4):
        d.rectangle([mx + 8, feet - 41, mx + 14, feet - 37], fill=(42, 46, 58, 255), outline=(*INK, 255))
        d.rectangle([mx, feet - 60, mx + 22, feet - 41], fill=(28, 34, 48, 255), outline=(*INK, 255))
        d.rectangle([mx + 2, feet - 58, mx + 20, feet - 43], fill=(74, 168, 232, 255))


def draw_party_table_prop(cv, x, feet):
    """Mesa elegante de la fiesta de Hawking (Cambridge 2009) con mantel, copas de champán y bocaditos."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 52, 5, 95)
    # Mantel blanco crema hasta el suelo
    d.rectangle([x - 48, feet - 34, x + 48, feet], fill=(242, 238, 226, 255), outline=(*INK, 255), width=2)
    d.rectangle([x - 50, feet - 38, x + 50, feet - 32], fill=(184, 42, 46, 255), outline=(*INK, 255))
    # Copas de champán servidas apoyadas sobre la mesa
    for cx_c in (x - 30, x - 14, x + 2, x + 18):
        d.line([(cx_c, feet - 38), (cx_c, feet - 46)], fill=(210, 224, 240, 255), width=2)
        d.line([(cx_c - 3, feet - 38), (cx_c + 3, feet - 38)], fill=(210, 224, 240, 255), width=2)
        d.polygon([(cx_c - 4, feet - 54), (cx_c + 4, feet - 54), (cx_c + 2, feet - 46), (cx_c - 2, feet - 46)],
                  fill=(248, 226, 126, 255), outline=(*INK, 255))
    # Bandeja de bocaditos a la derecha
    d.rectangle([x + 28, feet - 42, x + 44, feet - 38], fill=(192, 198, 210, 255), outline=(*INK, 255))
    for bx in (x + 32, x + 38):
        d.ellipse([bx - 3, feet - 46, bx + 3, feet - 41], fill=(216, 152, 84, 255), outline=(*INK, 255))


def draw_printer_table_prop(cv, x, feet, p_out=0.5):
    """Mesa con impresora sacando el sobre de invitación al día siguiente."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 38, 4, 95)
    d.rectangle([x - 32, feet - 32, x - 27, feet], fill=(74, 78, 92, 255), outline=(*INK, 255))
    d.rectangle([x + 27, feet - 32, x + 32, feet], fill=(74, 78, 92, 255), outline=(*INK, 255))
    d.rectangle([x - 36, feet - 37, x + 36, feet - 31], fill=(122, 128, 144, 255), outline=(*INK, 255))
    # Impresora
    d.rectangle([x - 22, feet - 54, x + 22, feet - 37], fill=(214, 218, 226, 255), outline=(*INK, 255), width=2)
    d.rectangle([x - 16, feet - 45, x + 16, feet - 41], fill=(32, 36, 48, 255))
    # Sobre saliendo
    ext = int(clamp01(p_out) * 14)
    if ext > 1:
        d.rectangle([x - 10, feet - 44, x + 10, feet - 44 + ext], fill=(252, 248, 232, 255), outline=(*INK, 255))


def draw_tombstone_prop(cv, x, feet):
    """Lápida sencilla de piedra de 1918 apoyada en el suelo."""
    d = ImageDraw.Draw(cv)
    shadow_ellipse(cv, x, feet, 26, 4, 95)
    d.rectangle([x - 22, feet - 8, x + 22, feet], fill=(108, 112, 118, 255), outline=(*INK, 255), width=2)
    d.rectangle([x - 16, feet - 46, x + 16, feet - 8], fill=(148, 152, 158, 255), outline=(*INK, 255), width=2)
    d.chord([x - 16, feet - 58, x + 16, feet - 34], 180, 360, fill=(148, 152, 158, 255), outline=(*INK, 255), width=2)
    d.line([(x - 8, feet - 36), (x + 8, feet - 36)], fill=(78, 82, 88, 255), width=2)
    d.line([(x - 6, feet - 28), (x + 6, feet - 28)], fill=(78, 82, 88, 255), width=2)


